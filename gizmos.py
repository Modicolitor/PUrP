import bpy
from bpy.types import (
    Operator,
    GizmoGroup,
)


class PP_OT_OversizeGizmo(bpy.types.Operator):
    '''Change the Oversize of the coupling'''
    bl_idname = "object.oversize"
    bl_label = "oversize"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):

        context.object.children[1].scale.x = self.valuex
        context.object.children[1].scale.y = self.valuey
        context.object.children[1].scale.z = self.valuez
        return {'FINISHED'}

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':  # Apply
            # if context.object.children[0].scale.x <= context.object.children[1].scale.x:  ####not bigger than the outer object
            self.delta = event.mouse_x - self.init_value
            # else:
            #    self.delta =  self.init_value

            self.valuex = self.init_scale_x + self.delta / \
                1000  # - self.window_width/2 #(HD Screen 800)
            self.valuey = self.init_scale_y + self.delta/1000
            self.valuez = self.init_scale_z + self.delta/1000

            #print(f"MouspositionX: {self.value}")
            self.execute(context)
        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            context.object.children[1].scale.x = self.init_scale_x
            context.object.children[1].scale.y = self.init_scale_y
            context.object.chilrend[1].scale.z = self.init_scale_z
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
       # self.window_width = context.window.width
        self.init_scale_x = context.object.children[1].scale.x
        self.init_scale_y = context.object.children[1].scale.y
        self.init_scale_z = context.object.children[1].scale.z
        self.init_value = event.mouse_x

        # event.mouse_x #- self.window_width/21   ################mach mal start value einfach 00
        self.valuex = context.object.children[1].scale.x
        self.valuey = context.object.children[1].scale.y
        self.valuez = context.object.children[1].scale.z

        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class PP_OT_CouplSizeGizmo(bpy.types.Operator):
    '''Change the scale of the coupling'''
    bl_idname = "object.couplesize"
    bl_label = "couplsize"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):

        # - (context.object.children[0].scale.x - context.object.children[1].scale.x )
        context.object.children[1].scale.x = self.valuex1
        # - (context.object.children[0].scale.y - context.object.children[1].scale.y )
        context.object.children[1].scale.y = self.valuey1
        # - (context.object.children[0].scale.z - context.object.children[1].scale.z )
        context.object.children[1].scale.z = self.valuez1
        context.object.children[0].scale.x = self.valuex0
        context.object.children[0].scale.y = self.valuey0
        context.object.children[0].scale.z = self.valuez0
        return {'FINISHED'}

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':  # Apply
            # if context.object.children[0].scale.x <= context.object.children[1].scale.x:  ####not bigger than the outer object
            self.delta = event.mouse_x - self.init_value
            # else:
            #    self.delta =  self.init_value

            self.valuex1 = self.init_scale_x1 + self.delta / \
                1000  # - self.window_width/2 #(HD Screen 800)
            self.valuey1 = self.init_scale_y1 + self.delta/1000
            self.valuez1 = self.init_scale_z1 + self.delta/1000

            self.valuex0 = self.init_scale_x0 + self.delta / \
                1000  # - self.window_width/2 #(HD Screen 800)
            self.valuey0 = self.init_scale_y0 + self.delta/1000
            self.valuez0 = self.init_scale_z0 + self.delta/1000

            #print(f"MouspositionX: {self.value}")
            self.execute(context)
        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            context.object.children[0].scale.x = self.init_scale_x0
            context.object.children[0].scale.y = self.init_scale_y0
            context.object.chilrend[0].scale.z = self.init_scale_z0
            context.object.children[1].scale.x = self.init_scale_x1
            context.object.children[1].scale.y = self.init_scale_y1
            context.object.chilrend[1].scale.z = self.init_scale_z1
            return {'CANCELLED'}
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
       # self.window_width = context.window.width
        self.init_scale_x0 = context.object.children[0].scale.x
        self.init_scale_y0 = context.object.children[0].scale.y
        self.init_scale_z0 = context.object.children[0].scale.z
        self.init_scale_y1 = context.object.children[1].scale.y
        self.init_scale_z1 = context.object.children[1].scale.z
        self.init_scale_x1 = context.object.children[1].scale.x

        self.init_value = event.mouse_x

        # event.mouse_x #- self.window_width/21   ################mach mal start value einfach 00
        self.valuex1 = context.object.children[1].scale.x
        self.valuey1 = context.object.children[1].scale.y
        self.valuez1 = context.object.children[1].scale.z
        self.valuex0 = context.object.children[0].scale.x
        self.valuey0 = context.object.children[0].scale.y
        self.valuez0 = context.object.children[0].scale.z

        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class PP_OT_zScaleGizmo(bpy.types.Operator):
    '''Change the z-scale of the coupling'''
    bl_idname = "object.zscale"
    bl_label = "couplsize"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):
        context.object.children[1].scale.z = self.value - (
            context.object.children[0].scale.z - context.object.children[1].scale.z)
        context.object.children[0].scale.z = self.value

        return {'FINISHED'}

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':  # Apply
            # if context.object.children[0].scale.x <= context.object.children[1].scale.x:  ####not bigger than the outer object
            self.delta = event.mouse_y - self.init_value
            # else:
            #    self.delta =  self.init_value

            self.value = self.init_scale_z + self.delta / \
                1000  # - self.window_width/2 #(HD Screen 800)
            #print(f"MouspositionX: {self.value}")
            self.execute(context)
        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            context.object.chilrend[0].location.z = self.init_scale_z
            context.object.chilrend[1].location.z = self.init_scale_z
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.init_scale_z = context.object.children[0].scale.z

        self.init_value = event.mouse_y

        # event.mouse_x #- self.window_width/21   ################mach mal start value einfach 00
        self.value = context.object.children[0].scale.z

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

        #matrixWorld = context.object[:]
        mpr = self.gizmos.new("GIZMO_GT_dial_3d")
        props = mpr.target_set_operator("object.oversize")
        #props.constraint_axis = True, True, True
        #props.orient_type = 'LOCAL'
        #props.release_confirm = True
        print(
            f"Oversize matrix world object name{ob.name} {ob.matrix_world.normalized()}")
        mpr.matrix_basis = ob.matrix_world.normalized()

        mpr.line_width = 3

        mpr.color = 0.8, 0.2, 0.8
        mpr.alpha = 0.5

        mpr.color_highlight = 1.0, 0.5, 1.0
        mpr.alpha_highlight = 1.0

        self.roll_widget = mpr

        # second gizmo
        mpa = self.gizmos.new("GIZMO_GT_dial_3d")
        props = mpa.target_set_operator("object.couplesize")
        #props.constraint_axis = True, True, True
        #props.orient_type = 'LOCAL'
        #props.release_confirm = True
        print(
            f"Size matrix world object name{ob.name} {ob.matrix_world.normalized()}")
        mpa.matrix_basis = ob.matrix_world.normalized()
        mpa.line_width = 3

        mpa.color = 0.2, 0.2, 0.8
        mpa.alpha = 0.5

        mpa.color_highlight = 0.3, 0.5, 1.0
        mpa.alpha_highlight = 1.0
        mpa.scale_basis = 2
        self.roll_widge = mpa

        mph = self.gizmos.new("GIZMO_GT_arrow_3d")
        mph.target_set_operator("object.zscale")
        print(
            f"ZScale matrix world object name{ob.name} {ob.matrix_world.normalized()}")
        mph.matrix_basis = ob.matrix_world.normalized()
        mph.draw_style = 'BOX'

        mph.color = 1.0, 0.5, 0.0
        mph.alpha = 0.5
        mph.color_highlight = 1.0, 0.5, 1.0
        mph.alpha_highlight = 0.5
        self.roll_widg = mph

    def refresh(self, context):
        ob = context.object

        mpr = self.roll_widget
        mpa = self.roll_widge
        mph = self.roll_widg

        mpa.matrix_basis = ob.matrix_world.normalized()
        mph.matrix_basis = ob.matrix_world.normalized()
        mpr.matrix_basis = ob.matrix_world.normalized()
