# Example of a custom widget that defines it's own geometry.
#
# Usage: Select a light in the 3D view and drag the arrow at it's rear
# to change it's energy value.
#
import bpy
from bpy.types import (
    Gizmo,
    GizmoGroup,
)

# Coordinates (each one is a triangle).
custom_shape_verts = (
    (3.0, 1.0, -1.0), (2.0, 2.0, -1.0), (3.0, 3.0, -1.0),
    (1.0, 3.0, 1.0), (3.0, 3.0, -1.0), (1.0, 3.0, -1.0),
    (3.0, 3.0, 1.0), (3.0, 1.0, -1.0), (3.0, 3.0, -1.0),
    (2.0, 0.0, 1.0), (3.0, 1.0, -1.0), (3.0, 1.0, 1.0),
    (2.0, 0.0, -1.0), (2.0, 2.0, 1.0), (2.0, 2.0, -1.0),
    (2.0, 2.0, -1.0), (0.0, 2.0, 1.0), (0.0, 2.0, -1.0),
    (1.0, 3.0, 1.0), (2.0, 2.0, 1.0), (3.0, 3.0, 1.0),
    (0.0, 2.0, -1.0), (1.0, 3.0, 1.0), (1.0, 3.0, -1.0),
    (2.0, 2.0, 1.0), (3.0, 1.0, 1.0), (3.0, 3.0, 1.0),
    (2.0, 2.0, -1.0), (1.0, 3.0, -1.0), (3.0, 3.0, -1.0),
    (-3.0, -1.0, -1.0), (-2.0, -2.0, -1.0), (-3.0, -3.0, -1.0),
    (-1.0, -3.0, 1.0), (-3.0, -3.0, -1.0), (-1.0, -3.0, -1.0),
    (-3.0, -3.0, 1.0), (-3.0, -1.0, -1.0), (-3.0, -3.0, -1.0),
    (-2.0, 0.0, 1.0), (-3.0, -1.0, -1.0), (-3.0, -1.0, 1.0),
    (-2.0, 0.0, -1.0), (-2.0, -2.0, 1.0), (-2.0, -2.0, -1.0),
    (-2.0, -2.0, -1.0), (0.0, -2.0, 1.0), (0.0, -2.0, -1.0),
    (-1.0, -3.0, 1.0), (-2.0, -2.0, 1.0), (-3.0, -3.0, 1.0),
    (0.0, -2.0, -1.0), (-1.0, -3.0, 1.0), (-1.0, -3.0, -1.0),
    (-2.0, -2.0, 1.0), (-3.0, -1.0, 1.0), (-3.0, -3.0, 1.0),
    (-2.0, -2.0, -1.0), (-1.0, -3.0, -1.0), (-3.0, -3.0, -1.0),
    (1.0, -1.0, 0.0), (-1.0, -1.0, 0.0), (0.0, 0.0, -5.0),
    (-1.0, -1.0, 0.0), (1.0, -1.0, 0.0), (0.0, 0.0, 5.0),
    (1.0, -1.0, 0.0), (1.0, 1.0, 0.0), (0.0, 0.0, 5.0),
    (1.0, 1.0, 0.0), (-1.0, 1.0, 0.0), (0.0, 0.0, 5.0),
    (-1.0, 1.0, 0.0), (-1.0, -1.0, 0.0), (0.0, 0.0, 5.0),
    (-1.0, -1.0, 0.0), (-1.0, 1.0, 0.0), (0.0, 0.0, -5.0),
    (-1.0, 1.0, 0.0), (1.0, 1.0, 0.0), (0.0, 0.0, -5.0),
    (1.0, 1.0, 0.0), (1.0, -1.0, 0.0), (0.0, 0.0, -5.0),
    (3.0, 1.0, -1.0), (2.0, 0.0, -1.0), (2.0, 2.0, -1.0),
    (1.0, 3.0, 1.0), (3.0, 3.0, 1.0), (3.0, 3.0, -1.0),
    (3.0, 3.0, 1.0), (3.0, 1.0, 1.0), (3.0, 1.0, -1.0),
    (2.0, 0.0, 1.0), (2.0, 0.0, -1.0), (3.0, 1.0, -1.0),
    (2.0, 0.0, -1.0), (2.0, 0.0, 1.0), (2.0, 2.0, 1.0),
    (2.0, 2.0, -1.0), (2.0, 2.0, 1.0), (0.0, 2.0, 1.0),
    (1.0, 3.0, 1.0), (0.0, 2.0, 1.0), (2.0, 2.0, 1.0),
    (0.0, 2.0, -1.0), (0.0, 2.0, 1.0), (1.0, 3.0, 1.0),
    (2.0, 2.0, 1.0), (2.0, 0.0, 1.0), (3.0, 1.0, 1.0),
    (2.0, 2.0, -1.0), (0.0, 2.0, -1.0), (1.0, 3.0, -1.0),
    (-3.0, -1.0, -1.0), (-2.0, 0.0, -1.0), (-2.0, -2.0, -1.0),
    (-1.0, -3.0, 1.0), (-3.0, -3.0, 1.0), (-3.0, -3.0, -1.0),
    (-3.0, -3.0, 1.0), (-3.0, -1.0, 1.0), (-3.0, -1.0, -1.0),
    (-2.0, 0.0, 1.0), (-2.0, 0.0, -1.0), (-3.0, -1.0, -1.0),
    (-2.0, 0.0, -1.0), (-2.0, 0.0, 1.0), (-2.0, -2.0, 1.0),
    (-2.0, -2.0, -1.0), (-2.0, -2.0, 1.0), (0.0, -2.0, 1.0),
    (-1.0, -3.0, 1.0), (0.0, -2.0, 1.0), (-2.0, -2.0, 1.0),
    (0.0, -2.0, -1.0), (0.0, -2.0, 1.0), (-1.0, -3.0, 1.0),
    (-2.0, -2.0, 1.0), (-2.0, 0.0, 1.0), (-3.0, -1.0, 1.0),
    (-2.0, -2.0, -1.0), (0.0, -2.0, -1.0), (-1.0, -3.0, -1.0),
)


class MyCustomShapeWidget(Gizmo):
    bl_idname = "VIEW3D_GT_auto_facemap"
    bl_target_properties = (
        {"id": "scale", "type": 'FLOAT', "array_length": 1},
    )

    __slots__ = (
        "custom_shape",
        "init_mouse_y",
        "init_value",
    )

    def _update_offset_matrix(self):
        # offset behind the light
        self.matrix_offset.col[3][2] = self.target_get_value("offset") / -10.0

    def draw(self, context):
        self._update_offset_matrix()
        self.draw_custom_shape(self.custom_shape)

    def draw_select(self, context, select_id):
        self._update_offset_matrix()
        self.draw_custom_shape(self.custom_shape, select_id=select_id)

    def setup(self):
        if not hasattr(self, "custom_shape"):
            self.custom_shape = self.new_custom_shape(
                'TRIS', custom_shape_verts)

    def invoke(self, context, event):
        self.init_mouse_y = event.mouse_y
        #self.init_value = self.target_get_value("offset")
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
        #value = self.init_value - delta
        #self.target_set_value("offset", value)
        #context.area.header_text_set("My Gizmo: %.4f" % value)
        return {'RUNNING_MODAL'}


'''class MyCustomShapeWidgetGroup(GizmoGroup):
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
        #mpr.target_set_prop("offset", ob.data, "energy")

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
            #print(f"isnt {isnt_order(ob)}")
            return True
        return False

    def setup(self, context):
        # Run an operator using the dial gizmo
        ob = context.object

        #matrixWorld = context.object[:]
        mpr = self.gizmos.new("GIZMO_GT_dial_3d")
        props = mpr.target_set_operator("object.pp_ot_widgettest")
        #props.constraint_axis = True, True, True
        #props.orient_type = 'LOCAL'
        #props.release_confirm = True
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


class PP_OT_widgetTestOperator(bpy.types.Operator):
    bl_idname = "object.pp_ot_widgettest"
    bl_label = "PP_OT_widgetTest"

    def execute(self, context):
        print('ALARM')

        return {'FINISHED'}


classes = (
    MyCustomShapeWidget,
    PUrP_OversizeGizmo,
)

for cls in classes:
    bpy.utils.register_class(cls)
