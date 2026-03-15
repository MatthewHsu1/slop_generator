import itertools
import math
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class OptimizationResult:
    rotation_radians: tuple[float, float, float]
    scale_multiplier: float
    remaining_volume: float


def _generate_euler_grid(step_degrees: int) -> list[tuple[float, float, float]]:
    if step_degrees <= 0 or step_degrees > 360:
        raise ValueError("step_degrees must be in the range [1, 360]")
    if 360 % step_degrees != 0:
        raise ValueError("step_degrees must divide 360 exactly")

    angles = [math.radians(d) for d in range(0, 360, step_degrees)]
    return [(rx, ry, rz) for rx, ry, rz in itertools.product(angles, repeat=3)]


def _binary_search_min_feasible(
    low: float,
    high: float,
    predicate: Callable[[float], bool],
    iterations: int = 30,
) -> float:
    if iterations <= 0:
        raise ValueError("iterations must be > 0")
    if high < low:
        raise ValueError("high must be >= low")
    if predicate(low):
        return low
    if not predicate(high):
        raise ValueError("predicate must be true at high")

    left = low
    right = high
    for _ in range(iterations):
        mid = (left + right) / 2.0
        if predicate(mid):
            right = mid
        else:
            left = mid

    return right


def optimize_boolean_difference_fit(
    target_object_name: str,
    cutter_object_name: str,
    rotation_step_degrees: int = 30,
    clearance: float = 1e-4,
    binary_iterations: int = 24,
    max_scale_multiplier: float = 10.0,
    scale_growth_factor: float = 1.25,
    apply_difference: bool = True,
) -> dict:
    try:
        import bmesh
        import bpy
    except ImportError as exc:
        raise RuntimeError("This function must run inside Blender (bpy available)") from exc

    if clearance < 0:
        raise ValueError("clearance must be >= 0")
    if max_scale_multiplier <= 0:
        raise ValueError("max_scale_multiplier must be > 0")
    if scale_growth_factor <= 1.0:
        raise ValueError("scale_growth_factor must be > 1")

    target = bpy.data.objects.get(target_object_name)
    cutter = bpy.data.objects.get(cutter_object_name)

    if not target or not cutter:
        raise ValueError("One or both objects not found")
    if target.type != "MESH" or cutter.type != "MESH":
        raise ValueError("Both objects must be meshes")

    depsgraph = bpy.context.evaluated_depsgraph_get()
    target_base_scale = tuple(target.scale)

    if any(abs(v) < 1e-12 for v in target_base_scale):
        raise ValueError("Target object has zero scale on at least one axis; apply/reset scale first.")

    def _link_duplicate(obj, suffix: str):
        dup = obj.copy()
        dup.data = obj.data.copy()
        dup.name = f"{obj.name}{suffix}"
        collection = obj.users_collection[0] if obj.users_collection else bpy.context.scene.collection
        collection.objects.link(dup)
        dup.matrix_world = obj.matrix_world.copy()
        return dup

    def _remove_object(obj):
        mesh = obj.data if obj and obj.type == "MESH" else None
        bpy.data.objects.remove(obj, do_unlink=True)
        if mesh and mesh.users == 0:
            bpy.data.meshes.remove(mesh)

    def _world_mesh_volume(obj) -> float:
        evaluated = obj.evaluated_get(depsgraph)
        mesh = evaluated.to_mesh()
        if mesh is None:
            return 0.0

        bm = bmesh.new()
        bm.from_mesh(mesh)
        local_volume = abs(bm.calc_volume(signed=True))
        bm.free()
        evaluated.to_mesh_clear()

        sx, sy, sz = obj.matrix_world.to_scale()
        world_scale = abs(sx * sy * sz)
        return local_volume * world_scale

    def _all_vertices_inside(container_obj, inner_obj, eps: float) -> bool:
        container_eval = container_obj.evaluated_get(depsgraph)
        inv_world = container_obj.matrix_world.inverted()

        for vertex in inner_obj.data.vertices:
            world_point = inner_obj.matrix_world @ vertex.co
            local_point = inv_world @ world_point
            success, closest, normal, _ = container_eval.closest_point_on_mesh(local_point)
            if not success:
                return False

            signed_distance = (local_point - closest).dot(normal)
            if signed_distance > -eps:
                return False

        return True

    def _set_uniform_scale(obj, multiplier: float):
        obj.scale = tuple(base * multiplier for base in target_base_scale)
        bpy.context.view_layer.update()

    def _remaining_volume_after_difference(target_obj, cutter_obj) -> float:
        temp_target = _link_duplicate(target_obj, "__tmp_diff_target")
        temp_cutter = _link_duplicate(cutter_obj, "__tmp_diff_cutter")

        try:
            mod = temp_target.modifiers.new(name="Boolean", type="BOOLEAN")
            mod.operation = "DIFFERENCE"
            mod.solver = "EXACT"
            mod.object = temp_cutter

            bpy.ops.object.select_all(action="DESELECT")
            temp_target.select_set(True)
            bpy.context.view_layer.objects.active = temp_target
            bpy.ops.object.modifier_apply(modifier=mod.name)

            return _world_mesh_volume(temp_target)
        finally:
            _remove_object(temp_target)
            _remove_object(temp_cutter)

    def _find_min_feasible_scale() -> float | None:
        low = 1e-6
        high = 1.0

        _set_uniform_scale(target_work, high)
        while not _all_vertices_inside(target_work, cutter_work, clearance):
            high *= scale_growth_factor
            if high > max_scale_multiplier:
                return None
            _set_uniform_scale(target_work, high)

        def _predicate(multiplier: float) -> bool:
            _set_uniform_scale(target_work, multiplier)
            return _all_vertices_inside(target_work, cutter_work, clearance)

        return _binary_search_min_feasible(low, high, _predicate, iterations=binary_iterations)

    target_work = _link_duplicate(target, "__tmp_opt_target")
    cutter_work = _link_duplicate(cutter, "__tmp_opt_cutter")

    best: OptimizationResult | None = None
    try:
        for rotation in _generate_euler_grid(rotation_step_degrees):
            target_work.rotation_euler = rotation
            bpy.context.view_layer.update()

            min_scale = _find_min_feasible_scale()
            if min_scale is None:
                continue

            _set_uniform_scale(target_work, min_scale)
            remaining_volume = _remaining_volume_after_difference(target_work, cutter_work)

            if best is None or remaining_volume > best.remaining_volume:
                best = OptimizationResult(
                    rotation_radians=rotation,
                    scale_multiplier=min_scale,
                    remaining_volume=remaining_volume,
                )

        if best is None:
            raise RuntimeError("Could not find a feasible scale/rotation pair")

        target.scale = tuple(base * best.scale_multiplier for base in target_base_scale)
        target.rotation_euler = best.rotation_radians
        bpy.context.view_layer.update()

        if apply_difference:
            try:
                from src.add_boolean_difference import add_boolean_difference
            except ImportError:
                from add_boolean_difference import add_boolean_difference
            add_boolean_difference(target_object_name, cutter_object_name)

        return {
            "rotation_radians": best.rotation_radians,
            "rotation_degrees": tuple(round(math.degrees(v), 6) for v in best.rotation_radians),
            "scale_multiplier": best.scale_multiplier,
            "remaining_volume": best.remaining_volume,
            "target_scale": tuple(target.scale),
        }
    finally:
        _remove_object(target_work)
        _remove_object(cutter_work)