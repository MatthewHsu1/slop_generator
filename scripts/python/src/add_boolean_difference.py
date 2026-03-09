import bpy

def add_boolean_difference(target_object_name: str, cutter_object_name: str):
    """
    Add a Boolean modifier (Difference) to target_object, using cutter_object as the operand.
    """

    target = bpy.data.objects.get(target_object_name)
    cutter = bpy.data.objects.get(cutter_object_name)

    if not target or not cutter:
        raise ValueError("One or both objects not found")
    if target.type != "MESH" or cutter.type != "MESH":
        raise ValueError("Both objects must be meshes")

    mod = target.modifiers.new(name="Boolean", type="BOOLEAN")

    mod.operation = "DIFFERENCE"
    
    mod.object = cutter

    bpy.ops.object.select_all(action='DESELECT')

    target.select_set(True)

    bpy.context.view_layer.objects.active = target
    
    bpy.ops.object.modifier_apply(modifier=mod.name)