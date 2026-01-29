import bpy

class UnityExportSettings(bpy.types.PropertyGroup):
    export_path: bpy.props.StringProperty(
        name="导出路径",
        subtype='DIR_PATH',
        default="//"
    )

    use_batch_export: bpy.props.BoolProperty(
        name="批量分别导出",
        default=True
    )

    apply_transform: bpy.props.BoolProperty(
        name="自动应用变换",
        default=True
    )

    center_pivot: bpy.props.BoolProperty(
        name="原点移至底部",
        default=False
    )