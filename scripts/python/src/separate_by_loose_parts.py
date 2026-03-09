import bpy

def separate_by_loose_parts(object_name: str):
    """
    Separate the mesh into multiple objects by loose parts (disconnected geometry).
    Returns a list of the resulting object names (original + newly created).
    """

    obj = bpy.data.objects.get(object_name)
    
    if not obj:
        raise ValueError(f"Object '{object_name}' not found")
    if obj.type != "MESH":
        raise ValueError("Object must be a mesh")

    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    # Must be in Edit mode with geometry selected
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.mode_set(mode='OBJECT')

    # Collect resulting objects (they're selected after separate)
    result_names = [o.name for o in bpy.context.selected_objects]
    return result_names