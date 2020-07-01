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
corner_shape_verts = (
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


class PUrP_CornerShapeWidget(Gizmo):
    bl_idname = "VIEW3D_GT_PURPCORNERSHAPE"
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
                'TRIS', corner_shape_verts)

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
p0 = Vector((-0.18209683895111084, 4.371138828673793e-08, 0.10484981536865234))
p1 = Vector((0.18209683895111084, 4.371138828673793e-08, 0.10484981536865234))
p2 = Vector((-0.18209683895111084, -4.371138828673793e-08, 2.1048498153686523))
p3 = Vector((0.18209683895111084, -4.371138828673793e-08, 2.1048498153686523))
p4 = Vector((-0.18209683895111084, -4.371138828673793e-08, 2.4571902751922607))
p5 = Vector((0.18209683895111084, -4.371138828673793e-08, 2.4571902751922607))
p6 = Vector((-0.4525858163833618, -4.371138828673793e-08, 2.1048498153686523))
p7 = Vector((0.45731768012046814, -4.371138828673793e-08, 2.1048498153686523))
p8 = Vector((0.0, -4.371138828673793e-08, 2.697995901107788))


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


# linecount custom
linecountv0 = Vector((1.5259459018707275, 2.0, 1.720690131187439))
linecountv1 = Vector((2.4740540981292725, 2.0, 1.720690131187439))
linecountv2 = Vector((1.5259459018707275, 2.0, 2.2793097496032715))
linecountv3 = Vector((2.4740540981292725, 2.0, 2.2793097496032715))
linecountv4 = Vector(
    (1.5259459018707275, 2.299999952316284, 1.720690131187439))
linecountv5 = Vector(
    (2.4740540981292725, 2.299999952316284, 1.720690131187439))
linecountv6 = Vector(
    (1.5259459018707275, 2.299999952316284, 2.2793097496032715))
linecountv7 = Vector(
    (2.4740540981292725, 2.299999952316284, 2.2793097496032715))
linecountv8 = Vector(
    (1.5259459018707275, 2.5999999046325684, 1.720690131187439))
linecountv9 = Vector(
    (2.4740540981292725, 2.5999999046325684, 1.720690131187439))
linecountv10 = Vector(
    (1.5259459018707275, 2.5999999046325684, 2.2793097496032715))
linecountv11 = Vector(
    (2.4740540981292725, 2.5999999046325684, 2.2793097496032715))


linecount_shape_verts = (
    linecountv0, linecountv1, linecountv2,
    linecountv1, linecountv2, linecountv3,
    linecountv6, linecountv4, linecountv5,
    linecountv6, linecountv7, linecountv5,
    linecountv9, linecountv8, linecountv10,
    linecountv9, linecountv11, linecountv10,
)


class PUrP_linecountShapeWidget(Gizmo):
    bl_idname = "VIEW3D_GT_PURP_LINECOUNT"
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
                'TRIS', linecount_shape_verts)

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


# line lengtth

linelength0 = Vector((-2.586153507232666, 2.0, 1.720690131187439))
linelength1 = Vector((-1.5259459018707275, 2.0, 1.720690131187439))
linelength2 = Vector((-2.586153507232666, 2.0, 2.2793097496032715))
linelength3 = Vector((-1.5259459018707275, 2.0, 2.2793097496032715))
linelength4 = Vector((-2.396531820297241, 2.0, 2.2793097496032715))
linelength5 = Vector((-2.2069101333618164, 2.0, 2.2793097496032715))
linelength6 = Vector((-1.9051891565322876, 2.0, 2.2793097496032715))
linelength7 = Vector((-1.7155675888061523, 2.0, 2.2793097496032715))
linelength8 = Vector((-1.7155675888061523, 2.0, 1.720690131187439))
linelength9 = Vector((-1.9051891565322876, 2.0, 1.720690131187439))
linelength10 = Vector((-2.2069101333618164, 2.0, 1.720690131187439))
linelength11 = Vector((-2.396531820297241, 2.0, 1.720690131187439))
linelength12 = Vector(
    (-2.2069101333618164, 2.1573259830474854, 2.2793097496032715))
linelength13 = Vector(
    (-2.396531820297241, 2.1573259830474854, 2.2793097496032715))
linelength14 = Vector(
    (-1.7155675888061523, 2.1573259830474854, 2.2793097496032715))
linelength15 = Vector(
    (-1.9051891565322876, 2.1573259830474854, 2.2793097496032715))
linelength16 = Vector(
    (-1.9051891565322876, 2.1573259830474854, 1.720690131187439))
linelength17 = Vector(
    (-1.7155675888061523, 2.1573259830474854, 1.720690131187439))
linelength18 = Vector(
    (-2.396531820297241, 2.1573259830474854, 1.720690131187439))
linelength19 = Vector(
    (-2.2069101333618164, 2.1573259830474854, 1.720690131187439))

linelength_shape_verts = (
    linelength0, linelength2, linelength11,
    linelength4, linelength2, linelength11,
    linelength13, linelength4, linelength11,
    linelength13, linelength11, linelength18,
    linelength12, linelength13, linelength18,
    linelength12, linelength19, linelength18,
    linelength12, linelength19, linelength5,
    linelength19, linelength5, linelength10,
    linelength9, linelength5, linelength10,
    linelength9, linelength5, linelength6,
    linelength9, linelength15, linelength6,
    linelength9, linelength16, linelength15,
    linelength14, linelength15, linelength16,
    linelength14, linelength17, linelength16,
    linelength14, linelength17, linelength7,
    linelength8, linelength17, linelength7,
    linelength8, linelength1, linelength7,
    linelength3, linelength1, linelength7,
)


class PUrP_LineLengthShapeWidget(Gizmo):
    bl_idname = "VIEW3D_GT_PURP_LINELENGTH"
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
                'TRIS', linelength_shape_verts)

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


# linedistance

linedistance0 = Vector((1.5259459018707275, -2.0, 1.720690131187439))
linedistance1 = Vector((2.4740540981292725, -2.0, 1.720690131187439))
linedistance2 = Vector((1.5259459018707275, -2.0, 2.2793097496032715))
linedistance3 = Vector((2.4740540981292725, -2.0, 2.2793097496032715))
linedistance4 = Vector(
    (1.5259459018707275, -1.7000000476837158, 1.720690131187439))
linedistance5 = Vector(
    (2.4740540981292725, -1.7000000476837158, 1.720690131187439))
linedistance6 = Vector(
    (1.5259459018707275, -1.7000000476837158, 2.2793097496032715))
linedistance7 = Vector(
    (2.4740540981292725, -1.7000000476837158, 2.2793097496032715))
linedistance8 = Vector(
    (2.070707082748413, -1.6999342441558838, 2.4415814876556396))
linedistance9 = Vector(
    (1.802796721458435, -1.6999342441558838, 2.4415814876556396))
linedistance10 = Vector(
    (2.070707082748413, -1.9997014999389648, 2.4415814876556396))
linedistance11 = Vector(
    (1.802796721458435, -1.9997014999389648, 2.4415814876556396))
linedistance12 = Vector(
    (2.070707082748413, -1.6999342441558838, 2.3324060440063477))
linedistance13 = Vector(
    (1.802796721458435, -1.6999342441558838, 2.3324060440063477))
linedistance14 = Vector(
    (2.070707082748413, -1.9997014999389648, 2.3324060440063477))
linedistance15 = Vector(
    (1.802796721458435, -1.9997014999389648, 2.3324060440063477))

linedistant_shape_verts = (
    linedistance0, linedistance1, linedistance2,
    linedistance3, linedistance1, linedistance2,
    linedistance4, linedistance6, linedistance5,
    linedistance7, linedistance6, linedistance5,
    linedistance11, linedistance14, linedistance15,
    linedistance11, linedistance14, linedistance10,
    linedistance11, linedistance9, linedistance10,
    linedistance8, linedistance9, linedistance10,
    linedistance8, linedistance9, linedistance12,
    linedistance13, linedistance9, linedistance12,

)


class PUrP_LineDistanceShapeWidget(Gizmo):
    bl_idname = "VIEW3D_GT_PURP_LINEDISTANCE"
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
                'TRIS', linedistant_shape_verts)

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

##thickness widget

thickness0 = Vector((-2.4682538509368896, -2.0, 1.720690131187439))
thickness1 = Vector((-2.5148062705993652, -2.0, 1.720690131187439))
thickness2 = Vector((-2.4682538509368896, -2.0, 2.2793097496032715))
thickness3 = Vector((-2.5148062705993652, -2.0, 2.2793097496032715))
thickness4 = Vector((-2.3993964195251465, -2.0, 2.2793097496032715))
thickness5 = Vector((-2.5554041862487793, -2.0, 2.2793097496032715))
thickness6 = Vector((-2.5554041862487793, -2.0, 1.720690131187439))
thickness7 = Vector((-1.5430042743682861, -2.0, 2.2793097496032715))
thickness8 = Vector((-1.9233784675598145, -2.0, 2.2793097496032715))
thickness9 = Vector((-1.963794469833374, -2.0, 1.720690131187439))
thickness10 = Vector((-1.9233784675598145, -2.0, 1.720690131187439))
thickness11 = Vector((-2.3993964195251465, -2.0, 1.720690131187439))
thickness12 = Vector((-1.5430042743682861, -2.0, 1.720690131187439))
thickness13 = Vector((-2.1905112266540527, -2.0, 1.720690131187439))
thickness14 = Vector((-2.2210400104522705, -2.0, 1.720690131187439))
thickness15 = Vector((-2.2210400104522705, -2.0, 2.2793097496032715))
thickness16 = Vector((-2.35250186920166, -2.0, 2.2793097496032715))
thickness17 = Vector((-2.35250186920166, -2.0, 1.720690131187439))
thickness18 = Vector((-2.1905112266540527, -2.0, 2.2793097496032715))
thickness19 = Vector((-1.963794469833374, -2.0, 2.2793097496032715))



thickness_shape_verts = (
    thickness1,thickness5,thickness6,
    thickness1,thickness5,thickness3,
    thickness0,thickness2,thickness11,
    thickness4,thickness2,thickness11,
    thickness16,thickness17,thickness14,
    thickness16,thickness15,thickness14,
    thickness13,thickness18,thickness9,
    thickness19,thickness18,thickness9,
    thickness8,thickness10,thickness12,
    thickness8,thickness7,thickness12,
)



class PUrP_ThicknessShapeWidget(Gizmo):
    bl_idname = "VIEW3D_GT_PURP_THICKNESS"
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
                'TRIS', thickness_shape_verts)

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
