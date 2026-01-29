import bpy

class MY_PT_ExportPanel(bpy.types.Panel):
    bl_label = "Unity 自动化管线"
    bl_idname = "MY_PT_export_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Unity Tools'

    def draw(self, context):
        layout = self.layout
        settings = context.scene.unity_export_tool

        box = layout.box()
        box.prop(settings, "export_path")
        box.prop(settings, "use_batch_export")
        box.prop(settings, "apply_transform")

        if settings.apply_transform:
            box.prop(settings, "center_pivot")

        row = layout.row()
        row.scale_y = 1.5
        row.operator("export.to_unity", icon='EXPORT')