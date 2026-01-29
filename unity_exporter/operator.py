import bpy
import os


class MY_OT_ExportToUnity(bpy.types.Operator):
    bl_idname = "export.to_unity"
    bl_label = "Export To Unity"
    bl_description = "根据设置导出模型到 Unity"

    def execute(self, context):
        scene = context.scene
        mysettings = scene.unity_export_tool
        
        # 1. 检查路径有效性
        raw_path = mysettings.export_path
        # 处理相对路径 (//) 转为 绝对路径
        final_path = bpy.path.abspath(raw_path)
        
        if not os.path.exists(final_path):
            self.report({'ERROR'}, f"路径不存在: {final_path}")
            return {'CANCELLED'}
        
        # 2. 检查有没有选东西
        selected_objs = context.selected_objects
        if not selected_objs:
            self.report({'WARNING'}, "请先选择至少一个模型！")
            return {'CANCELLED'}

        # 3. 记录当前模式，导出完要恢复回去 (避免破坏场景)
        active_obj_original = context.view_layer.objects.active
        
        # 定义导出函数 (内部使用)
        def process_and_export(obj, filepath):
            # 确保只有当前这个物体被选中
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            context.view_layer.objects.active = obj
            
            # --- 核心管线处理 ---
            if mysettings.apply_transform:
                # 应用旋转和缩放 (位置通常不应用，除非你想让它跑到世界中心)
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                
                if mysettings.center_pivot:
                    # 原点设为几何中心
                    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
                    # 移动游标到选中项底部
                    cursor_loc = context.scene.cursor.location.copy() # 备份游标
                    # 简单算法：把原点移到底部 (Z轴最小值)
                    # 这里用简单的 Origin to Geometry -> Bounds Center 替代，
                    # 如果要精确到底部中心需要更复杂的 Bounding Box 计算。
                    # 为了演示简单，这里暂用 Blender 自带的“原点移至几何中心”
                    pass

            # --- 导出 FBX ---
            bpy.ops.export_scene.fbx(
                filepath=filepath,
                use_selection=True,      # 只导选中的
                axis_forward='-Z',       # Unity 标准
                axis_up='Y',             # Unity 标准
                apply_unit_scale=True,
                apply_scale_options='FBX_SCALE_ALL', # 修复 Unity 缩放问题
                bake_space_transform=True,
                object_types={'MESH'},   # 只导模型，不导灯光摄像机
                use_mesh_modifiers=True, # 应用修改器
                use_triangles=False      # 保持四边面
            )
            print(f"已导出: {filepath}")

        # 4. 开始循环导出
        if mysettings.use_batch_export:
            # --- 批量模式：每个物体一个文件 ---
            count = 0
            for obj in selected_objs:
                # 跳过非模型物体 (灯光、相机等)
                if obj.type != 'MESH':
                    continue
                    
                target_file = os.path.join(final_path, obj.name + ".fbx")
                process_and_export(obj, target_file)
                count += 1
            
            self.report({'INFO'}, f"批量导出完成！共 {count} 个文件")
            
        else:
            # --- 合并模式：所有选中的存为一个文件 ---
            # 用“激活物体”的名字作为文件名，或者默认名
            filename = active_obj_original.name if active_obj_original else "Exported_Model"
            target_file = os.path.join(final_path, filename + ".fbx")
            
            # 选中所有原本选中的
            for obj in selected_objs:
                obj.select_set(True)
                
            # 直接导出所有选中的
            bpy.ops.export_scene.fbx(
                filepath=target_file,
                use_selection=True,
                axis_forward='-Z', axis_up='Y',
                apply_unit_scale=True,
                apply_scale_options='FBX_SCALE_ALL',
                object_types={'MESH'}
            )
            self.report({'INFO'}, f"合并导出完成: {filename}.fbx")

        # 5. 恢复选区状态
        for obj in selected_objs:
            obj.select_set(True)
        context.view_layer.objects.active = active_obj_original
        
        return {'FINISHED'}