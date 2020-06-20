# Example of a custom widget that defines it's own geometry.
#
# Usage: Select a light in the 3D view and drag the arrow at it's rear
# to change it's energy value.
#
import bpy
import mathutils
from bpy.types import (
    Gizmo,
    GizmoGroup,
)

Vector = mathutils.Vector
# vertices
v0 = Vector((-1.0, -0.5, 1.0))
v1 = Vector((-1.0, 0.5, 1.0))
v2 = Vector((1.0, -0.5, -1.0))
v3 = Vector((1.0, -0.5, 1.0))
v4 = Vector((1.0, 0.5, -1.0))
v5 = Vector((1.0, 0.5, 1.0))
v6 = Vector((-1.0, -0.5, -0.0))
v7 = Vector((-1.0, 0.5, -0.0))
v8 = Vector((1.0, 0.5, -0.0))
v9 = Vector((1.0, -0.5, -0.0))
v10 = Vector((0.0, 0.5, -1.0))
v11 = Vector((0.0, 0.5, 1.0))
v12 = Vector((0.0, -0.5, -1.0))
v13 = Vector((0.0, -0.5, 1.0))
v14 = Vector((0.0, -0.5, -0.0))
v15 = Vector((0.0, 0.5, -0.0))


# Coordinates (each one is a triangle).
custom_shape_verts = (
    v0, v1, v13,
    v0, v1, v7,
    v0, v7, v6,
    v0, v6, v13,
    v1, v11, v13,
    v11, v13, v3,
    v11, v5, v3,
    v6, v14, v13,
    v13, v3, v14,
    v14, v3, v9,
    v14, v9, v12,
    v9, v12, v2,
    v1, v15, v7,
    v1, v11, v15,
    v11, v8, v15,
    v5, v11, v5,
    v8, v4, v15,
    v4, v15, v10,
    v3, v5, v9,
    v9, v5, v8,
    v9, v8, v2,
    v2, v8, v4,
    v2, v4, v12,
    v12, v10, v4,
    v12, v10, v15,
    v12, v14, v15,
    v14, v15, v6,
    v15, v6, v7,
    v5, v11, v8

    # (3.0, 1.0, -1.0), (2.0, 2.0, -1.0), (3.0, 3.0, -1.0),
    # (1.0, 3.0, 1.0), (3.0, 3.0, -1.0), (1.0, 3.0, -1.0),
    # (3.0, 3.0, 1.0), (3.0, 1.0, -1.0), (3.0, 3.0, -1.0),
    # (2.0, 0.0, 1.0), (3.0, 1.0, -1.0), (3.0, 1.0, 1.0),
    # (2.0, 0.0, -1.0), (2.0, 2.0, 1.0), (2.0, 2.0, -1.0),
    # (2.0, 2.0, -1.0), (0.0, 2.0, 1.0), (0.0, 2.0, -1.0),
    # (1.0, 3.0, 1.0), (2.0, 2.0, 1.0), (3.0, 3.0, 1.0),
    # (0.0, 2.0, -1.0), (1.0, 3.0, 1.0), (1.0, 3.0, -1.0),
    # (2.0, 2.0, 1.0), (3.0, 1.0, 1.0), (3.0, 3.0, 1.0),
    # (2.0, 2.0, -1.0), (1.0, 3.0, -1.0), (3.0, 3.0, -1.0),
    # (-3.0, -1.0, -1.0), (-2.0, -2.0, -1.0), (-3.0, -3.0, -1.0),
    # (-1.0, -3.0, 1.0), (-3.0, -3.0, -1.0), (-1.0, -3.0, -1.0),
    # (-3.0, -3.0, 1.0), (-3.0, -1.0, -1.0), (-3.0, -3.0, -1.0),
    # (-2.0, 0.0, 1.0), (-3.0, -1.0, -1.0), (-3.0, -1.0, 1.0),
    # (-2.0, 0.0, -1.0), (-2.0, -2.0, 1.0), (-2.0, -2.0, -1.0),
    # (-2.0, -2.0, -1.0), (0.0, -2.0, 1.0), (0.0, -2.0, -1.0),
    # (-1.0, -3.0, 1.0), (-2.0, -2.0, 1.0), (-3.0, -3.0, 1.0),
    # (0.0, -2.0, -1.0), (-1.0, -3.0, 1.0), (-1.0, -3.0, -1.0),
    # (-2.0, -2.0, 1.0), (-3.0, -1.0, 1.0), (-3.0, -3.0, 1.0),
    # (-2.0, -2.0, -1.0), (-1.0, -3.0, -1.0), (-3.0, -3.0, -1.0),
    # (1.0, -1.0, 0.0), (-1.0, -1.0, 0.0), (0.0, 0.0, -5.0),
    # (-1.0, -1.0, 0.0), (1.0, -1.0, 0.0), (0.0, 0.0, 5.0),
    # (1.0, -1.0, 0.0), (1.0, 1.0, 0.0), (0.0, 0.0, 5.0),
    # (1.0, 1.0, 0.0), (-1.0, 1.0, 0.0), (0.0, 0.0, 5.0),
    # (-1.0, 1.0, 0.0), (-1.0, -1.0, 0.0), (0.0, 0.0, 5.0),
    # #(-1.0, -1.0, 0.0), (-1.0, 1.0, 0.0), (0.0, 0.0, -5.0),
    # (-1.0, 1.0, 0.0), (1.0, 1.0, 0.0), (0.0, 0.0, -5.0),
    # (1.0, 1.0, 0.0), (1.0, -1.0, 0.0), (0.0, 0.0, -5.0),
    # (3.0, 1.0, -1.0), (2.0, 0.0, -1.0), (2.0, 2.0, -1.0),
    # (1.0, 3.0, 1.0), (3.0, 3.0, 1.0), (3.0, 3.0, -1.0),
    # (3.0, 3.0, 1.0), (3.0, 1.0, 1.0), (3.0, 1.0, -1.0),
    # (2.0, 0.0, 1.0), (2.0, 0.0, -1.0), (3.0, 1.0, -1.0),
    # (2.0, 0.0, -1.0), (2.0, 0.0, 1.0), (2.0, 2.0, 1.0),
    # (2.0, 2.0, -1.0), (2.0, 2.0, 1.0), (0.0, 2.0, 1.0),
    # (1.0, 3.0, 1.0), (0.0, 2.0, 1.0), (2.0, 2.0, 1.0),
    # (0.0, 2.0, -1.0), (0.0, 2.0, 1.0), (1.0, 3.0, 1.0),
    # (2.0, 2.0, 1.0), (2.0, 0.0, 1.0), (3.0, 1.0, 1.0),
    # (2.0, 2.0, -1.0), (0.0, 2.0, -1.0), (1.0, 3.0, -1.0),
    # (-3.0, -1.0, -1.0), (-2.0, 0.0, -1.0), (-2.0, -2.0, -1.0),
    # (-1.0, -3.0, 1.0), (-3.0, -3.0, 1.0), (-3.0, -3.0, -1.0),
    # (-3.0, -3.0, 1.0), (-3.0, -1.0, 1.0), (-3.0, -1.0, -1.0),
    # (-2.0, 0.0, 1.0), (-2.0, 0.0, -1.0), (-3.0, -1.0, -1.0),
    # (-2.0, 0.0, -1.0), (-2.0, 0.0, 1.0), (-2.0, -2.0, 1.0),
    # (-2.0, -2.0, -1.0), (-2.0, -2.0, 1.0), (0.0, -2.0, 1.0),
    # (-1.0, -3.0, 1.0), (0.0, -2.0, 1.0), (-2.0, -2.0, 1.0),
    # (0.0, -2.0, -1.0), (0.0, -2.0, 1.0), (-1.0, -3.0, 1.0),
    # (-2.0, -2.0, 1.0), (-2.0, 0.0, 1.0), (-3.0, -1.0, 1.0),
    # (-2.0, -2.0, -1.0), (0.0, -2.0, -1.0), (-1.0, -3.0, -1.0),
)


class PUrP_CustomShapeWidget(Gizmo):
    bl_idname = "VIEW3D_GT_PURP"
    bl_target_properties = (
        {"id": "scale", "type": 'FLOAT', "array_length": 1},
    )

    __slots__ = (
        "custom_shape",
        "init_mouse_y",
        "init_value",
    )

    # def matrix_basis():

    def _update_offset_matrix(self):
        # offset behind the light
        # print("jaja")
        #self.matrix_offset.col[3][2] = context.object.matrix_world
        pass

    def draw(self, context):
        # self._update_offset_matrix()
        self.draw_custom_shape(self.custom_shape)

    def draw_select(self, context, select_id):
        # self._update_offset_matrix()
        self.draw_custom_shape(self.custom_shape, select_id=select_id)

    def setup(self):
        if not hasattr(self, "custom_shape"):
            self.custom_shape = self.new_custom_shape(
                'TRIS', custom_shape_verts)

    def invoke(self, context, event):
        self.init_mouse_y = event.mouse_y
        # self.init_value = self.target_get_value("offset")
        return {'RUNNING_MODAL'}

    def exit(self, context, cancel):
        context.area.header_text_set(None)
        # if cancel:
        #    self.target_set_value("offset", self.init_value)

    def modal(self, context, event, tweak):
        delta = (event.mouse_y - self.init_mouse_y) / 10.0
        # if 'SNAP' in tweak:
        #    delta = round(delta)
        # if 'PRECISE' in tweak:
        #    delta /= 10.0
        # value = self.init_value - delta
        # self.target_set_value("offset", value)
        # context.area.header_text_set("My Gizmo: %.4f" % value)
        return {'RUNNING_MODAL'}


'''


class MyCustomShapeWidgetGroup(GizmoGroup):
    bl_idname = "OBJECT_GGT_light_test"
    bl_label = "Test Light Widget"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT'}

    @classmethod
    def poll(cls, context):
        ob = context.object
        return (ob and ob.type == 'LIGHT')

    def setup(self, context):
        # Assign the 'offset' target property to the light energy.
        ob = context.object
        self.custom_shape = self.new_custom_shape('TRIS', custom_shape_verts)
        mpr = self.gizmos.new(MyCustomShapeWidget.bl_idname)
        # mpr.target_set_prop("offset", ob.data, "energy")

        mpr.color = 1.0, 0.5, 1.0
        mpr.alpha = 0.5

        mpr.color_highlight = 1.0, 1.0, 1.0
        mpr.alpha_highlight = 0.5

        # units are large, so shrink to something more reasonable.
        mpr.scale_basis = 0.1
        mpr.use_draw_modal = True

        self.energy_widget = mpr

    def refresh(self, context):
        ob = context.object
        mpr = self.energy_widget
        mpr.matrix_basis = ob.matrix_world.normalized()'''

'''


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
            # if ("PUrP" in ob.name) and ("diff" and "fix" and "union" not in ob.name):
            #    if len(ob.children) > 1:  # flatcut has zero or
            # 1 (order) child... excluded from gizmos
            # if len(ob.children) != 1 and isnt_order(ob):
            # print(f"isnt {isnt_order(ob)}")
            return True
        return False

    def setup(self, context):
        # Run an operator using the dial gizmo
        ob = context.object

        # matrixWorld = context.object[:]
        # elf.custom_shape = self.new_custom_shape('TRIS', custom_shape_verts)
        s

        # mpr = self.gizmos.new(MyCustomShapeWidget.bl_idname)

        mpr = self.gizmos.new("GIZMO_GT_dial_3d")
        props = mpr.target_set_operator("object.pp_ot_widgettest")
        # props.constraint_axis = True, True, True
        # props.orient_type = 'LOCAL'
        # props.release_confirm = True
        # print(
        #   f"Oversize matrix world object name{ob.name} {ob.matrix_world.normalized()}")
        mpr.matrix_basis = ob.matrix_world.normalized()

        mpr.line_width = 3

        mpr.color = 0.8, 0.2, 0.8
        mpr.alpha = 0.5

        mpr.color_highlight = 1.0, 0.5, 1.0
        mpr.alpha_highlight = 1.0

        self.roll_widget = mpr

    def refresh(self, context):
        ob = context.object
        mpr = self.roll_widget

        mpr.matrix_basis = ob.matrix_world.normalized()


'''

'''


class PP_OT_widgetTestOperator(bpy.types.Operator):

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
            # print(f"MouspositionX: {self.value}")
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


classes = (
    MyCustomShapeWidget,
    PUrP_OversizeGizmo,
    PP_OT_widgetTestOperator
)

for cls in classes:
    bpy.utils.register_class(cls)
'''
