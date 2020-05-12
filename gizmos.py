import bpy
from bpy.types import (
    Operator,
    GizmoGroup,
)

class PP_OT_OversizeGizmo(bpy.types.Operator):
    bl_idname = "object.oversize"
    bl_label = "oversize"
    bl_options = {'REGISTER',"UNDO"}

    @classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):
        
        context.object.children[1].scale.x = self.value 
        context.object.children[1].scale.y = self.value 
        context.object.children[1].scale.z = self.value 
        return {'FINISHED'}

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':  # Apply
            #if context.object.children[0].scale.x <= context.object.children[1].scale.x:  ####not bigger than the outer object
            self.delta = event.mouse_x - self.init_value
            #else:
            #    self.delta =  self.init_value
            
            self.value = self.init_scale_x + self.delta/1000  #- self.window_width/2 #(HD Screen 800)
            #print(f"MouspositionX: {self.value}")
            self.execute(context)
        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            context.object.children[1].location.x = self.init_scale_x
            context.object.children[1].location.y = self.init_scale_y
            context.object.chilrend[1].location.z = self.init_scale_z
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
       # self.window_width = context.window.width 
        self.init_scale_x = context.object.children[1].scale.x 
        self.init_scale_y = context.object.children[1].scale.y 
        self.init_scale_z = context.object.children[1].scale.z
        self.init_value = event.mouse_x

        self.value = context.object.children[1].scale.x           ##event.mouse_x #- self.window_width/21   ################mach mal start value einfach 00
        
        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class PP_OT_CouplSizeGizmo(bpy.types.Operator):
    bl_idname = "object.couplesize"
    bl_label = "couplsize"
    bl_options = {'REGISTER',"UNDO"}

    @classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):
        
        context.object.children[1].scale.x = self.value 
        context.object.children[1].scale.y = self.value 
        context.object.children[1].scale.z = self.value 
        context.object.children[0].scale.x = self.value 
        context.object.children[0].scale.y = self.value 
        context.object.children[0].scale.z = self.value 
        return {'FINISHED'}

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':  # Apply
            #if context.object.children[0].scale.x <= context.object.children[1].scale.x:  ####not bigger than the outer object
            self.delta = event.mouse_x - self.init_value
            #else:
            #    self.delta =  self.init_value
            
            self.value = self.init_scale_x + self.delta/1000  #- self.window_width/2 #(HD Screen 800)
            #print(f"MouspositionX: {self.value}")
            self.execute(context)
        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            context.object.children[0].location.x = self.init_scale_x
            context.object.children[0].location.y = self.init_scale_y
            context.object.chilrend[0].location.z = self.init_scale_z
            context.object.children[1].location.x = self.init_scale_x
            context.object.children[1].location.y = self.init_scale_y
            context.object.chilrend[1].location.z = self.init_scale_z
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
       # self.window_width = context.window.width 
        self.init_scale_x = context.object.children[1].scale.x 
        self.init_scale_y = context.object.children[1].scale.y 
        self.init_scale_z = context.object.children[1].scale.z
        
        self.init_value = event.mouse_x

        self.value = context.object.children[1].scale.x           ##event.mouse_x #- self.window_width/21   ################mach mal start value einfach 00
        
        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}



class PUrP_OversizeGizmo(GizmoGroup):
    bl_idname = "OBJECT_GGT_test_camera"
    bl_label = "Object Camera Test Widget"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT'}

    @classmethod
    def poll(cls, context):
        ob = context.object
        return (ob and ob.type == 'MESH' and "SingleConnector" in context.view_layer.objects.active.name)

    def setup(self, context):
        # Run an operator using the dial gizmo
        ob = context.object
        mpr = self.gizmos.new("GIZMO_GT_dial_3d")
        props = mpr.target_set_operator("object.oversize")
        #props.constraint_axis = True, True, True
        #props.orient_type = 'LOCAL'
        #props.release_confirm = True

        mpr.matrix_basis = ob.matrix_world.normalized()
        mpr.line_width = 3

        mpr.color = 0.8, 0.2, 0.8
        mpr.alpha = 0.5

        mpr.color_highlight = 1.0, 0.5, 1.0
        mpr.alpha_highlight = 1.0

        self.roll_widget = mpr
        
        #########################second gizmo
        mpr = self.gizmos.new("GIZMO_GT_dial_3d")
        props = mpr.target_set_operator("object.couplesize")
        #props.constraint_axis = True, True, True
        #props.orient_type = 'LOCAL'
        #props.release_confirm = True

        mpr.matrix_basis = ob.matrix_world.normalized()
        mpr.line_width = 3

        mpr.color = 0.2, 0.2, 0.8
        mpr.alpha = 0.5

        mpr.color_highlight = 0.3, 0.5, 1.0
        mpr.alpha_highlight = 1.0
        mpr.scale_basis = 2
        self.roll_widget = mpr

    def refresh(self, context):
        ob = context.object
        mpr = self.roll_widget
        mpr.matrix_basis = ob.matrix_world.normalized()     
    


