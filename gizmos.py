import bpy
from .gizmotshape import PUrP_CornerShapeWidget
from .gizmotshape import PUrP_ArrowShapeWidget
from .gizmotshape import PUrP_linecountShapeWidget
from .gizmotshape import PUrP_LineLengthShapeWidget
from .gizmotshape import PUrP_LineDistanceShapeWidget
from .gizmotshape import PUrP_ThicknessShapeWidget
from bpy.types import (
    Operator,
    GizmoGroup,
)
import mathutils
from math import radians


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

            # print(f"MouspositionX: {self.value}")
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

            # print(f"MouspositionX: {self.value}")
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


class PUrP_SinglCoupGizmo(GizmoGroup):
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
                    # print(f"isnt {isnt_order(ob)}")
                    return True
            return False

    def setup(self, context):
        # Run an operator using the dial gizmo
        ob = context.object

        # matrixWorld = context.object[:]
        mpr = self.gizmos.new("GIZMO_GT_dial_3d")
        props = mpr.target_set_operator("object.oversize")
        # props.constraint_axis = True, True, True
        # props.orient_type = 'LOCAL'
        # props.release_confirm = True

        mpr.matrix_basis = ob.matrix_world.normalized()

        mpr.line_width = 3

        mpr.color = 0.05, 0.2, 0.8
        mpr.alpha = 0.5

        mpr.color_highlight = 0.03, 0.05, 1.0
        mpr.alpha_highlight = 1.0

        self.roll_widget = mpr

        # couple size gizmot
        mpa = self.gizmos.new("GIZMO_GT_dial_3d")
        props = mpa.target_set_operator("object.couplesize")
        # props.constraint_axis = True, True, True
        # props.orient_type = 'LOCAL'
        # props.release_confirm = True

        mpa.matrix_basis = ob.matrix_world.normalized()
        mpa.line_width = 3

        mpa.color = 0.2, 0.2, 0.8
        mpa.alpha = 0.5

        mpa.color_highlight = 0.2, 0.03, 0.9
        mpa.alpha_highlight = 1.0
        mpa.scale_basis = 2
        self.roll_widge = mpa

        # zscale gizmot
        mph = self.gizmos.new("GIZMO_GT_arrow_3d")
        mph.target_set_operator("object.zscale")

        mph.matrix_basis = ob.matrix_world.normalized()
        mph.draw_style = 'BOX'

        mph.color = 1.0, 0.03, 0.03
        mph.alpha = 0.5
        mph.color_highlight = 1.0, 0.03, 0.04
        mph.alpha_highlight = 0.5
        self.roll_widg = mph

        # Bevel offset gizmot
        mpo = self.gizmos.new(PUrP_CornerShapeWidget.bl_idname)
        # mpo = self.gizmos.new("GIZMO_GT_dial_3d")
        mpo.target_set_operator("purp.bevoffset")

        mpo.matrix_basis = ob.matrix_world.normalized()
        mpo.matrix_offset.col[3][0] += 0.5  # [3] - location, 0 -x
        # mpo.matrix_basis[2][3] += 8
        # mpo.matrix_basis[0][3] += 3
        mpo.line_width = 10

        mpo.color = 0.05, 0.9, 0.05
        mpo.alpha = 0.5

        mpo.color_highlight = 0.03, 1.0, 0.03
        mpo.alpha_highlight = 1.0
        mpo.scale_basis = 0.5

        mpo.use_draw_value

        self.roll_wid = mpo

        # Bevel segments gizmot
        mps = self.gizmos.new(PUrP_CornerShapeWidget.bl_idname)
        # mps = self.gizmos.new("GIZMO_GT_dial_3d")
        mps.target_set_operator("purp.bevseggiz")

        mps.matrix_basis = ob.matrix_world.normalized()
        mps.matrix_offset.col[3][0] += 0.2
        mps.matrix_offset.col[3][2] -= 0.5
        # mps.matrix_basis[2][3] += 0.8
        # mps.matrix_basis[0][3] += 0.5
        mps.line_width = 10

        mps.color = 0.03, 0.8, 0.03
        mps.alpha = 0.5

        mps.color_highlight = 0.01, 1.0, 0.01
        mps.alpha_highlight = 1.0
        mps.scale_basis = 0.2
        mps.use_draw_value

        self.bevseggizm = mps

    def refresh(self, context):
        ob = context.object

        mpr = self.roll_widget
        mpa = self.roll_widge
        mph = self.roll_widg
        mpo = self.roll_wid
        mps = self.bevseggizm

        mpa.matrix_basis = ob.matrix_world.normalized()
        mph.matrix_basis = ob.matrix_world.normalized()
        mpr.matrix_basis = ob.matrix_world.normalized()

        mpo.matrix_basis = ob.matrix_world.normalized()
        mpo.matrix_basis[2][3] += 1
        mps.matrix_basis = ob.matrix_world.normalized()
        mps.matrix_basis[2][3] += 1


# planar connector gizmos

def has_stopper(obj):
    lowestvert = 0
    for vert in obj.data.vertices:  # find lowest z coordinate
        if vert.co.z <= lowestvert:
            lowestvert = vert.co.z

    lowestlist = []
    lowestexample = obj.data.vertices[0]
    for vert in obj.data.vertices:  # collect all verts with lowest co.z values
        if vert.co.z == lowestvert:
            lowestlist.append(vert.co.z)
            lowestexample = vert  # example for stopperheight evaluation

    # PUrP.StopperBool = False
    if len(lowestlist) == 4:  # with 4 verts its a stopper
        return True
    return False


class PUrP_PlanarGizmo(GizmoGroup):
    bl_idname = "OBJECT_GGT_PLANARCONNECTOR"
    bl_label = "Object Camera Test Widget"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT'}

    @classmethod
    def poll(cls, context):
        ob = context.object
        if ob != None:
            if ("PUrP" in ob.name) and ("Planar" in ob.name):
                return True
            return False

    def setup(self, context):
        # Run an operator using the dial gizmo
        ob = context.object

        mpr = self.gizmos.new(PUrP_ArrowShapeWidget.bl_idname)
        props = mpr.target_set_operator("purp.roffsetgiz")

        mpr.matrix_basis = ob.matrix_world.normalized()

        # mat_rot1 = mathutils.Matrix.Rotation(radians(-90.0), 4, 'X')  # rotate
        # mat_rot2 = mathutils.Matrix.Rotation(radians(90.0), 4, 'Y')  # rotate

        #mat_rot = mat_rot1 @ mat_rot2
        #mat_trans = mathutils.Matrix.Translation(ob.location)
       # mat = mat_trans @ mat_rot1
        #mpr.matrix_basis = mat
        #mpr.matrix_basis[0][3] += 0.4

        #mpr.scale_basis = 0.5
        mpr.line_width = 3
        mpr.color = 0.05, 0.2, 0.8
        mpr.alpha = 0.5
        mpr.color_highlight = 0.03, 0.05, 1.0
        mpr.alpha_highlight = 1.0

        self.Roffset = mpr

        # left offset
        mpl = self.gizmos.new(PUrP_ArrowShapeWidget.bl_idname)
        props = mpl.target_set_operator("purp.loffsetgiz")
        # props.constraint_axis = True, True, True
        # props.orient_type = 'LOCAL'
        # props.release_confirm = True

        mpl.matrix_basis = ob.matrix_world.normalized()

        # mat_rot1 = mathutils.Matrix.Rotation(radians(90.0), 4, 'Z')  # rotate
        mat_rot2 = mathutils.Matrix.Rotation(radians(-90.0), 4, 'Y')  # rotate

        #mat_rot = mat_rot1 @ mat_rot2
        mat_trans = mathutils.Matrix.Translation(ob.location)
        mat = mat_trans @ mat_rot2
        mpl.matrix_basis = mat
        #mpl.matrix_basis[0][3] += 0.4

        #mpl.scale_basis = 0.5
        mpl.line_width = 3
        mpl.color = 0.05, 0.2, 0.8
        mpl.alpha = 0.5
        mpl.color_highlight = 0.03, 0.05, 1.0
        mpl.alpha_highlight = 1.0

        self.Loffset = mpl

        # zscale
        mpz = self.gizmos.new(PUrP_ArrowShapeWidget.bl_idname)
        props = mpz.target_set_operator("purp.planzscalegiz")
        # props.constraint_axis = True, True, True
        # props.orient_type = 'LOCAL'
        # props.release_confirm = True

        mpz.matrix_basis = ob.matrix_world.normalized()

        #
        # mat_rot1 = mathutils.Matrix.Rotation(radians(90.0), 4, 'Z')  # rotate
        mat_rot2 = mathutils.Matrix.Rotation(radians(90.0), 4, 'Y')  # rotate

        # mat_rot = mat_rot1 @ mat_rot2
        mat_trans = mathutils.Matrix.Translation(ob.location)
        mat = mat_trans @ mat_rot2
        mpz.matrix_basis = mat
        #mpz.matrix_basis[0][3] += 0.4

        #mpz.scale_basis = 0.5
        mpz.line_width = 3
        mpz.color = 0.05, 0.2, 0.8
        mpz.alpha = 0.5
        mpz.color_highlight = 0.03, 0.05, 1.0
        mpz.alpha_highlight = 1.0

        self.zScale = mpz

        # stopper scale

        # if has_stopper():
        mps = self.gizmos.new(PUrP_ArrowShapeWidget.bl_idname)
        props = mps.target_set_operator("purp.stopperheightgiz")
        # props.constraint_axis = True, True, True
        # props.orient_type = 'LOCAL'
        # props.release_confirm = True

        mps.matrix_basis = ob.matrix_world.normalized()

        #
        # mat_rot1 = mathutils.Matrix.Rotation(radians(90.0), 4, 'Z')  # rotate
        mat_rot2 = mathutils.Matrix.Rotation(
            radians(180.0), 4, 'Y')  # rotate

        # mat_rot = mat_rot1 @ mat_rot2
        mat_trans = mathutils.Matrix.Translation(ob.location)
        mat = mat_trans @ mat_rot2
        mps.matrix_basis = mat
        #mps.matrix_basis[2][3] -= 0.4

        #mps.scale_basis = 0.5
        mps.line_width = 3
        mps.color = 0.05, 0.2, 0.8
        mps.alpha = 0.5
        mps.color_highlight = 0.03, 0.05, 1.0
        mps.alpha_highlight = 1.0

        self.stopper = mps

        # lineCount

        mpcount = self.gizmos.new(PUrP_linecountShapeWidget.bl_idname)
        # mpcount.target_set_prop("offset", context.scene.PUrP, "LineCount")
        props = mpcount.target_set_operator("purp.linecountgiz")
        # props.constraint_axis = True, True, True
        # props.orient_type = 'LOCAL'
        # props.release_confirm = True

        mpcount.matrix_basis = ob.matrix_world.normalized()

        #
        # mat_rot1 = mathutils.Matrix.Rotation(radians(90.0), 4, 'Z')  # rotate
        mat_rot2 = mathutils.Matrix.Rotation(radians(90.0), 4, 'X')  # rotate

        # mat_rot = mat_rot1 @ mat_rot2
        mat_trans = mathutils.Matrix.Translation(ob.location)
        mat = mat_trans @ mat_rot2
        mpcount.matrix_basis = mat
        #mpcount.matrix_basis[2][3] += 0.4
        #mpcount.matrix_basis[0][3] += 0.4
        #mpcount.matrix_basis[1][3] += 0.4

        #mpcount.scale_basis = 0.5
        mpcount.line_width = 3
        mpcount.color = 0.05, 0.2, 0.8
        mpcount.alpha = 0.5
        mpcount.color_highlight = 0.03, 0.05, 1.0
        mpcount.alpha_highlight = 1.0

        self.linecount = mpcount

        # linelength

        mplength = self.gizmos.new(PUrP_LineLengthShapeWidget.bl_idname)
        # mpcount.target_set_prop("offset", context.scene.PUrP, "LineCount")
        props = mplength.target_set_operator("purp.linelengthgiz")
        # props.constraint_axis = True, True, True
        # props.orient_type = 'LOCAL'
        # props.release_confirm = True

        mplength.matrix_basis = ob.matrix_world.normalized()

        #
        # mat_rot1 = mathutils.Matrix.Rotation(radians(90.0), 4, 'Z')  # rotate
        mat_rot2 = mathutils.Matrix.Rotation(radians(90.0), 4, 'X')  # rotate

        # mat_rot = mat_rot1 @ mat_rot2
        mat_trans = mathutils.Matrix.Translation(ob.location)
        mat = mat_trans @ mat_rot2
        mplength.matrix_basis = mat
        mplength.matrix_basis[2][3] += 0.4
        mplength.matrix_basis[1][3] += 0.4
        mplength.matrix_basis[2][3] -= 0.4

        #mplength.scale_basis = 0.5
        mplength.line_width = 3
        mplength.color = 0.05, 0.2, 0.8
        mplength.alpha = 0.5
        mplength.color_highlight = 0.03, 0.05, 1.0
        mplength.alpha_highlight = 1.0

        self.linelength = mplength

        # linedistance

        mpdistance = self.gizmos.new(PUrP_LineDistanceShapeWidget.bl_idname)
        # mpcount.target_set_prop("offset", context.scene.PUrP, "LineCount")
        props = mpdistance.target_set_operator("purp.linedistancegiz")
        # props.constraint_axis = True, True, True
        # props.orient_type = 'LOCAL'
        # props.release_confirm = True

        mpdistance.matrix_basis = ob.matrix_world.normalized()

       
        #mpdistance.scale_basis = 0.5
        mpdistance.line_width = 3
        mpdistance.color = 0.05, 0.2, 0.8
        mpdistance.alpha = 0.5
        mpdistance.color_highlight = 0.03, 0.05, 1.0
        mpdistance.alpha_highlight = 1.0

        self.linedistance = mpdistance

        # thickness 

        mpthickness = self.gizmos.new(PUrP_ThicknessShapeWidget.bl_idname)
        # mpcount.target_set_prop("offset", context.scene.PUrP, "LineCount")
        props = mpthickness.target_set_operator("purp.thicknessgiz")
        # props.constraint_axis = True, True, True
        # props.orient_type = 'LOCAL'
        # props.release_confirm = True

        mpthickness.matrix_basis = ob.matrix_world.normalized()

        #
        # mat_rot1 = mathutils.Matrix.Rotation(radians(90.0), 4, 'Z')  # rotate
        mat_rot2 = mathutils.Matrix.Rotation(radians(90.0), 4, 'X')  # rotate

        # mat_rot = mat_rot1 @ mat_rot2
        mat_trans = mathutils.Matrix.Translation(ob.location)
        mat = mat_trans @ mat_rot2
        mpthickness.matrix_basis = mat
        #mpdistance.matrix_basis[2][3] += 0.4
        #mpdistance.matrix_basis[1][3] -= 0.4
        #mpdistance.matrix_basis[0][3] -= 0.4

        #mpdistance.scale_basis = 0.5
        mpthickness.line_width = 3
        mpthickness.color = 0.05, 0.2, 0.8
        mpthickness.alpha = 0.5
        mpthickness.color_highlight = 0.03, 0.05, 1.0
        mpthickness.alpha_highlight = 1.0

        self.thickness = mpthickness

    def refresh(self, context):
        ob = context.object
        # if has_stopper(ob):
        mpr = self.Roffset

        #mat_rot1 = mathutils.Matrix.Rotation(radians(-90.0), 4, 'Z')  # rotate
        mat_rot2 = mathutils.Matrix.Rotation(radians(-90.0), 4, 'Y')  # rotate

        #mat_rot = mat_rot1 @ mat_rot2
        mat_trans = mathutils.Matrix.Translation(ob.location)
        mat = mat_trans @ mat_rot2
        mpr.matrix_basis = mat
        #mpr.matrix_basis[0][3] += 0.4

        mpl = self.Loffset

        #mat_rot1 = mathutils.Matrix.Rotation(radians(90.0), 4, 'Z')  # rotate
        mat_rot2 = mathutils.Matrix.Rotation(radians(90.0), 4, 'Y')  # rotate

        #mat_rot = mat_rot1 @ mat_rot2
        mat_trans = mathutils.Matrix.Translation(ob.location)
        mat = mat_trans @ mat_rot2
        mpl.matrix_basis = mat
        #mpl.matrix_basis[0][3] -= 0.4

        mpz = self.zScale

        #mat_rot2 = mathutils.Matrix.Rotation(radians(90.0), 4, 'X')  # rotate

        # mat_rot = mat_rot1 @ mat_rot2
        #mat_trans = mathutils.Matrix.Translation(ob.location)
        #mat = mat_trans @ mat_rot2
        mpz.matrix_basis = ob.matrix_world.normalized()
        #mpz.matrix_basis[2][3] += 0.4

        if has_stopper(ob):
            mps = self.stopper

            mat_rot2 = mathutils.Matrix.Rotation(
                radians(180.0), 4, 'Y')  # rotate
            mat_trans = mathutils.Matrix.Translation(ob.location)
            mat = mat_trans @ mat_rot2
            mps.matrix_basis = mat
            #mps.matrix_basis[2][3] -= 0.4
            mps.scale_basis = 0.5
        else:

            mps = self.stopper

            mat_rot2 = mathutils.Matrix.Rotation(
                radians(-90.0), 4, 'X')  # rotate
            mat_trans = mathutils.Matrix.Translation(ob.location)
            mat = mat_trans @ mat_rot2
            mps.matrix_basis = mat
            #mps.matrix_basis[2][3] -= 0.4
            mps.scale_basis = 0.0001

        mpcount = self.linecount
        mpcount.matrix_basis = ob.matrix_world.normalized()
        #mpcount.matrix_basis[2][3] += 0.4
        #mpcount.matrix_basis[0][3] += 0.4
        #mpcount.matrix_basis[1][3] += 0.4
        #mpcount.scale_basis = 0.5

        mplength = self.linelength
        mplength.matrix_basis = ob.matrix_world.normalized()
        #mplength.matrix_basis[2][3] += 0.4
        #mplength.matrix_basis[0][3] -= 0.4
        #mplength.matrix_basis[1][3] += 0.4
        #mplength.scale_basis = 0.5

        mpdistance = self.linedistance
        mpdistance.matrix_basis = ob.matrix_world.normalized()
        #mpdistance.matrix_basis[2][3] += 0.4
        #mpdistance.matrix_basis[0][3] -= 0.4
        #mpdistance.matrix_basis[1][3] -= 0.4
        #mpdistance.scale_basis = 0.5

        mpthickness = self.thickness
        mpthickness.matrix_basis = ob.matrix_world.normalized()

class PP_OT_PlanarRoffsetGizmo(bpy.types.Operator):
    '''Change the beveloffset of the coupling'''
    bl_idname = "purp.roffsetgiz"
    bl_label = "couplsize"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):
        ob = context.object
        for v in self.rightestV:
            v.co.x = self.value

        context.scene.PUrP.OffsetRight = ob.data.vertices[0].co.x*4 - 1.5
        return {'FINISHED'}

    def modal(self, context, event):

        if event.type == 'MOUSEMOVE':  # Apply

            self.delta = event.mouse_x - self.init_value
            self.value = self.init_position + self.delta / 1000

            self.execute(context)
        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            for v in self.rightestV:
                v.co.x = self.init_position

            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        ob = context.object
        #
        rightestx = 0
        for v in ob.data.vertices:
            if v.co.x > rightestx:
                rightestx = v.co.x
        # rightestx is now
        self.rightestV = []
        for v in ob.data.vertices:
            if rightestx == v.co.x:
                self.rightestV.append(v)
        self.init_position = rightestx
        self.init_value = event.mouse_x

        # event.mouse_x #- self.window_width/21   ################mach mal start value einfach 00
        self.value = rightestx  # ???

        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class PP_OT_PlanarLoffsetGizmo(bpy.types.Operator):
    '''Change the beveloffset of the coupling'''
    bl_idname = "purp.loffsetgiz"
    bl_label = "couplsize"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):
        ob = context.object
        for v in self.leftestV:
            v.co.x = self.value

        context.scene.PUrP.OffsetLeft = - ob.data.vertices[1].co.x*4 - 1.5
        return {'FINISHED'}

    def modal(self, context, event):

        if event.type == 'MOUSEMOVE':  # Apply

            self.delta = event.mouse_x - self.init_value
            self.value = self.init_position + self.delta / 1000

            self.execute(context)
        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            for v in self.leftestV:
                v.co.x = self.init_position

            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        ob = context.object
        #
        leftestx = 0
        for v in ob.data.vertices:
            if v.co.x < leftestx:
                leftestx = v.co.x
        # rightestx is now
        self.leftestV = []
        for v in ob.data.vertices:
            if leftestx == v.co.x:
                self.leftestV.append(v)
        self.init_position = leftestx
        self.init_value = event.mouse_x

        # event.mouse_x #- self.window_width/21   ################mach mal start value einfach 00
        self.value = leftestx  # ???

        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class PP_OT_PlanarzScaleGizmo(bpy.types.Operator):
    '''Change the Zscale of the coupling'''
    bl_idname = "purp.planzscalegiz"
    bl_label = "couplsize"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):

        if self.has_stopper:
            if self.valuemiddle >= 0:  # upper limiter
                for v in self.middleV:
                    v.co.z = -0.01
                for v in self.lowestV:
                    v.co.z = -0.01 - context.scene.PUrP.StopperHeight
                context.scene.PUrP.zScale = 0.01
            else:  # positioning

                for v in self.middleV:
                    v.co.z = self.valuemiddle

                for v in self.lowestV:
                    v.co.z = self.valuelow

                context.scene.PUrP.zScale = -self.valuemiddle
        else:  # no stopper
            if self.valuelow >= 0:
                for v in self.lowestV:
                    v.co.z = -0.01
                context.scene.PUrP.zScale = 0.01
            else:
                for v in self.lowestV:
                    v.co.z = self.valuelow
                context.scene.PUrP.zScale = -self.valuelow

                # if self.has_stopper:
                #    for v in self.middleV:
                #        v.co.z = self.valuemiddle

        return {'FINISHED'}

    def modal(self, context, event):

        if event.type == 'MOUSEMOVE':  # Apply

            self.delta = event.mouse_y - self.init_value
            self.valuelow = self.lowestz + self.delta / 100
            # if self.has_stopper:
            self.valuemiddle = self.middlez + self.delta / 100

            self.execute(context)

        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            for v in self.lowestV:
                v.co.z = self.lowestz
            if self.has_stopper:
                for v in self.middleV:
                    v.co.z = self.middlez
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        ob = context.object
        self.middleV = []
        self.lowestV = []
        self.lowestz = 0
        self.middlez = 0
        for v in ob.data.vertices:
            if v.co.z < self.lowestz:
                self.lowestz = v.co.z

        self.has_stopper = has_stopper(ob)

        if self.has_stopper:  # zscale with stopper is like moving all below the top line

            for v in ob.data.vertices:
                if v.co.z != 0 and v.co.z != self.lowestz:
                    self.middlez = v.co.z
                    self.middleV.append(v)

            for v in ob.data.vertices:
                if v.co.z == self.lowestz:
                    self.lowestV.append(v)

            # for v in ob.data.vertices:
            #    if v.co.z == self.middlez:
            #        self.middleV.append(v)

        else:
            self.lowestz = 0
            for v in ob.data.vertices:
                if v.co.z < self.lowestz:
                    self.lowestz = v.co.z
            # self.lowestV = []
            for v in ob.data.vertices:
                if v.co.z == self.lowestz:
                    self.lowestV.append(v)
            # coordinaten aller

        # self.init_position1 = lowestz
        # self.init_position2 = self.middlez

        self.init_value = event.mouse_y

        # event.mouse_x #- self.window_width/21   ################mach mal start value einfach 00
        self.valuelow = self.lowestz
        if self.has_stopper:
            self.valuemiddle = self.middlez

        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class PP_OT_PlanarStopperHeightGizmo(bpy.types.Operator):
    '''Change the Zscale of the coupling'''
    bl_idname = "purp.stopperheightgiz"
    bl_label = "couplsize"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):
        zscale = -context.scene.PUrP.zScale
        if self.value - zscale >= 0:
            for v in self.lowestV:
                v.co.z = zscale - 0.01
            context.scene.PUrP.StopperHeight = 0.01
        else:
            for v in self.lowestV:
                v.co.z = self.value
            context.scene.PUrP.StopperHeight = -self.value + zscale
        return {'FINISHED'}

    def modal(self, context, event):

        if event.type == 'MOUSEMOVE':  # Apply

            self.delta = event.mouse_y - self.init_value
            self.value = self.lowestz + self.delta / 100

            self.execute(context)

        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            for v in self.lowestV:
                v.co.z = self.lowestz

            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        ob = context.object
        self.lowestV = []
        self.lowestz = 0
        for v in ob.data.vertices:
            if v.co.z < self.lowestz:
                self.lowestz = v.co.z

        for v in ob.data.vertices:
            if v.co.z == self.lowestz:
                self.lowestV.append(v)
            # coordinaten aller

        # self.init_position1 = lowestz
        # self.init_position2 = self.middlez

        self.init_value = event.mouse_y

        # event.mouse_x #- self.window_width/21   ################mach mal start value einfach 00
        self.value = self.lowestz

        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class PP_OT_PlanarLineCountGizmo(bpy.types.Operator):
    '''Change the Zscale of the coupling'''
    bl_idname = "purp.linecountgiz"
    bl_label = "couplsize"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):
        ob = context.object
        ob.modifiers["PUrP_Array_2"].count = int(self.value)

        context.scene.PUrP.LineCount = int(self.value)
        return {'FINISHED'}

    def modal(self, context, event):

        if event.type == 'MOUSEMOVE':  # Apply

            self.delta = event.mouse_y - self.init_value
            self.value = self.value + self.delta / 1000

            self.execute(context)

        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            ob.modifiers["PUrP_Array_2"].count = self.init_count

            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        ob = context.object

        self.init_value = event.mouse_y

        # event.mouse_x #- self.window_width/21   ################mach mal start value einfach 00
        self.value = ob.modifiers["PUrP_Array_2"].count

        self.init_count = ob.modifiers["PUrP_Array_2"].count

        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class PP_OT_PlanarLineLengthGizmo(bpy.types.Operator):
    '''Change the Zscale of the coupling'''
    bl_idname = "purp.linelengthgiz"
    bl_label = "couplsize"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):
        ob = context.object
        ob.modifiers["PUrP_Array_1"].count = int(self.value)

        context.scene.PUrP.LineLength = int(self.value)
        return {'FINISHED'}

    def modal(self, context, event):

        if event.type == 'MOUSEMOVE':  # Apply

            self.delta = event.mouse_y - self.init_value
            self.value = self.value + self.delta / 1000

            self.execute(context)

        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            ob.modifiers["PUrP_Array_1"].count = self.init_count

            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        ob = context.object

        self.init_value = event.mouse_y

        # event.mouse_x #- self.window_width/21   ################mach mal start value einfach 00
        self.value = ob.modifiers["PUrP_Array_1"].count

        self.init_count = ob.modifiers["PUrP_Array_1"].count

        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class PP_OT_PlanarLineDistanceGizmo(bpy.types.Operator):
    '''Change the Zscale of the coupling'''
    bl_idname = "purp.linedistancegiz"
    bl_label = "couplsize"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):
        ob = context.object

        ob.modifiers["PUrP_Array_2"].relative_offset_displace[1] = self.value

        context.scene.PUrP.LineDistance = self.value
        return {'FINISHED'}

    def modal(self, context, event):

        if event.type == 'MOUSEMOVE':  # Apply

            self.delta = event.mouse_y - self.init_value
            self.value = self.value + self.delta / 1000

            self.execute(context)

        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            ob.modifiers["PUrP_Array_2"].relative_offset_displace[1] = self.init_count

            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        ob = context.object

        self.init_value = event.mouse_y

        # event.mouse_x #- self.window_width/21   ################mach mal start value einfach 00
        self.value = ob.modifiers["PUrP_Array_2"].relative_offset_displace[1]

        self.init_count = ob.modifiers["PUrP_Array_2"].relative_offset_displace[1]

        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class PP_OT_PlanarThicknessGizmo(bpy.types.Operator):
    '''Change the Oversize (Thickness) of the planar connector'''
    bl_idname = "purp.thicknessgiz"
    bl_label = "couplsize"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):
        ob = context.object

        ob.modifiers["PUrP_Solidify"].thickness = self.value

        context.scene.PUrP.Oversize = self.value
        return {'FINISHED'}

    def modal(self, context, event):

        if event.type == 'MOUSEMOVE':  # Apply

            self.delta = event.mouse_y - self.init_value
            self.value = self.value + self.delta / 1000

            self.execute(context)

        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            ob.modifiers["PUrP_Solidify"].thickness = self.init_count

            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        ob = context.object

        self.init_value = event.mouse_y

        # event.mouse_x #- self.window_width/21   ################mach mal start value einfach 00
        self.value = ob.modifiers["PUrP_Solidify"].thickness

        self.init_count = ob.modifiers["PUrP_Solidify"].thickness

        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
