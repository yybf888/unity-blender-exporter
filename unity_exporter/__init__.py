

bl_info = {
    "name": "Unity 自动化导出工具",
    "author": "yybf888",
    "version": (1, 0, 0),
    "blender": (5, 0, 1),  # 你的 Blender 版本
    "location": "View3D > 侧边栏 > Unity Tools",
    "description": "一键将模型按 Unity 规范导出 FBX",
    "warning": "",
    "doc_url": "",
    "category": "Import-Export",
}

import bpy
from .properties import UnityExportSettings
from .panel import MY_PT_ExportPanel
from .operator import MY_OT_ExportToUnity

classes = (
    UnityExportSettings,
    MY_PT_ExportPanel,
    MY_OT_ExportToUnity,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.unity_export_tool = bpy.props.PointerProperty(
        type=UnityExportSettings
    )

def unregister():
    del bpy.types.Scene.unity_export_tool
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)