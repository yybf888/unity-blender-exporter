import bpy
import os

def get_export_path(raw_path):
    """将 Blender 路径转为绝对路径并校验"""
    final_path = bpy.path.abspath(raw_path)
    if not os.path.exists(final_path):
        return None
    return final_path


def save_selection(context):
    """保存当前选择状态"""
    return (
        context.view_layer.objects.active,
        list(context.selected_objects)
    )


def restore_selection(context, state):
    """恢复选择状态"""
    active, selected = state
    bpy.ops.object.select_all(action='DESELECT')
    for obj in selected:
        obj.select_set(True)
    context.view_layer.objects.active = active


def export_fbx_unity(filepath):
    """统一的 Unity FBX 导出参数"""
    bpy.ops.export_scene.fbx(
        filepath=filepath,
        use_selection=True,
        axis_forward='-Z',
        axis_up='Y',
        apply_unit_scale=True,
        apply_scale_options='FBX_SCALE_ALL',
        bake_space_transform=True,
        object_types={'MESH'},
        use_mesh_modifiers=True,
    )
