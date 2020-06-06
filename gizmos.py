import bpy
from bpy.types import (
    Operator,
    GizmoGroup,
)
import mathutils


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
        children = context.object.children
        context.object.children[1].scale.x = self.valuex
        context.object.children[1].scale.y = self.valuey
        context.object.children[1].scale.z = self.valuez
        context.scene.PUrP.Oversize = (
            children[0].scale.x - children[1].scale.x)/2
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
        context.scene.PUrP.CoupSize = self.valuex0
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
        context.scene.PUrP.zScale = self.value
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


class PP_OT_BevelOffsetGizmo(bpy.types.Operator):
    '''Change the beveloffset of the coupling'''
    bl_idname = "purp.bevoffset"
    bl_label = "couplsize"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):

        children = context.object.children
        children[1].modifiers[0].width = self.value
        children[0].modifiers[0].width = self.value
        context.scene.PUrP.BevelOffset = self.value
        return {'FINISHED'}

    def modal(self, context, event):
        children = context.object.children
        if event.type == 'MOUSEMOVE':  # Apply

            self.delta = event.mouse_y - self.init_value
            self.value = self.init_width + self.delta / 1000

            self.execute(context)
        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            children[0].modifiers[0].width = self.init_width
            children[1].modifiers[0].width = self.init_width
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        children = context.object.children
        self.init_width = children[0].modifiers[0].width

        self.init_value = event.mouse_y

        # event.mouse_x #- self.window_width/21   ################mach mal start value einfach 00
        self.value = children[0].modifiers[0].width

        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class PP_OT_BevelSegmentGizmo(bpy.types.Operator):
    '''Change the beveloffset of the coupling'''
    bl_idname = "purp.bevseggiz"
    bl_label = "couplsize"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):

        children = context.object.children
        children[1].modifiers[0].segments = int(self.value)
        children[0].modifiers[0].segments = int(self.value)
        context.scene.PUrP.BevelSegments = int(self.value)
        # print(self.value)
        return {'FINISHED'}

    def modal(self, context, event):
        children = context.object.children
        if event.type == 'MOUSEMOVE':  # Apply

            self.delta = event.mouse_y - self.init_value
            self.value = self.init_segments + self.delta / 10

            self.execute(context)
        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            children[0].modifiers[0].segments = self.init_segments
            children[1].modifiers[0].segments = self.init_segments
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        children = context.object.children
        self.init_segments = children[0].modifiers[0].segments

        self.init_value = event.mouse_y

        # event.mouse_x #- self.window_width/21   ################mach mal start value einfach 00
        self.value = children[0].modifiers[0].segments

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
        if ob != None:
            if ("PUrP" in ob.name) and ("diff" and "fix" and "union" not in ob.name):
                if len(ob.children) > 1:  # flatcut has zero or
                    # 1 (order) child... excluded from gizmos
                    # if len(ob.children) != 1 and isnt_order(ob):
                    #print(f"isnt {isnt_order(ob)}")
                    return True
            return False

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

        # couple size gizmot
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

        # zscale gizmot
        mph = self.gizmos.new("GIZMO_GT_arrow_3d")
        mph.target_set_operator("object.zscale")

        mph.matrix_basis = ob.matrix_world.normalized()
        mph.draw_style = 'BOX'

        mph.color = 1.0, 0.5, 0.0
        mph.alpha = 0.5
        mph.color_highlight = 1.0, 0.5, 1.0
        mph.alpha_highlight = 0.5
        self.roll_widg = mph

        # Bevel offset gizmot
        mpo = self.gizmos.new("GIZMO_GT_dial_3d")
        mpo.target_set_operator("purp.bevoffset")

        mpo.matrix_basis = ob.matrix_world.normalized()
        mpo.matrix_basis[2][3] += 1
        mpo.line_width = 3

        mpo.color = 0.2, 0.2, 0.8
        mpo.alpha = 0.5

        mpo.color_highlight = 0.0, 0.5, 0.3
        mpo.alpha_highlight = 1.0
        mpo.scale_basis = 2

        mpo.use_draw_value

        self.roll_wid = mpo

        # Bevel segments gizmot
        mps = self.gizmos.new("GIZMO_GT_dial_3d")
        mps.target_set_operator("purp.bevseggiz")

        mps.matrix_basis = ob.matrix_world.normalized()
        mps.matrix_basis[2][3] += 1
        mps.line_width = 3

        mps.color = 0.2, 0.2, 0.8
        mps.alpha = 0.5

        mps.color_highlight = 0.0, 0.5, 0.3
        mps.alpha_highlight = 1.0
        mps.scale_basis = 1
        mps.use_draw_value

        self.roll_wi = mps

    def refresh(self, context):
        ob = context.object

        mpr = self.roll_widget
        mpa = self.roll_widge
        mph = self.roll_widg
        mpo = self.roll_wid
        mps = self.roll_wi

        mpa.matrix_basis = ob.matrix_world.normalized()
        mph.matrix_basis = ob.matrix_world.normalized()
        mpr.matrix_basis = ob.matrix_world.normalized()

        mpo.matrix_basis = ob.matrix_world.normalized()
        mpo.matrix_basis[2][3] += 1
        mps.matrix_basis = ob.matrix_world.normalized()
        mps.matrix_basis[2][3] += 1
