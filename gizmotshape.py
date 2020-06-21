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


# vertices pfeil
p0 = Vector((-0.487274706363678, -1.0, 0.0))
p1 = Vector((0.487274706363678, -1.0, 0.0))
p2 = Vector((-0.487274706363678, 1.0, 0.0))
p3 = Vector((0.487274706363678, 1.0, 0.0))
p4 = Vector((-0.487274706363678, 1.2692807912826538, 0.0))
p5 = Vector((0.487274706363678, 1.2692807912826538, 0.0))
p6 = Vector((-1.2957993745803833, 1.0, 0.0))
p7 = Vector((1.2957993745803833, 1.0, 0.0))
p8 = Vector((0.0, 1.4367600679397583, 0.0))


arrow_shape_verts = (
    p0, p1, p2,
    p1, p2, p3,
    p2, p3, p4,
    p3, p4, p5,
    p4, p5, p8,
    p6, p2, p4,
    p3, p7, p5

)


class PUrP_ArrowShapeWidget(Gizmo):
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
                'TRIS', arrow_shape_verts)

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
