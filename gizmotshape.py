#
# Copyright (C) 2020 by Modicolitor
#
# This file is part of PuzzleUrPrint.
#
# License Text
#
# You should have received a copy of the GNU General Public License along with PuzzleUrPrint. If
# not, see <https://www.gnu.org/licenses/>.

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


# vertices pfeil up
'''
p0 = Vector((-0.18262259662151337, 6.799549367997315e-08, -1.2501908540725708))
p1 = Vector((0.1815710812807083, 6.799549367997315e-08, -1.2501908540725708))
p2 = Vector((-0.18262259662151337, -1.9427282893502706e-08, 0.7498091459274292))
p3 = Vector((0.1815710812807083, -1.9427282893502706e-08, 0.7498091459274292))
p4 = Vector((-0.18262259662151337, -1.9427282893502706e-08, 1.1021496057510376))
p5 = Vector((0.1815710812807083, -1.9427282893502706e-08, 1.1021496057510376))
p6 = Vector((-0.45311158895492554, -1.9427282893502706e-08, 0.7498091459274292))
p7 = Vector((0.4567919075489044, -1.9427282893502706e-08, 0.7498091459274292))
p8 = Vector((-0.0005257626180537045, -1.9427282893502706e-08, 1.342955231666565))


arrowup_shape_verts = (
    p0, p1, p2,
    p1, p2, p3,
    p2, p3, p4,
    p3, p4, p5,
    p4, p5, p8,
    p6, p2, p4,
    p3, p7, p5

)
'''


p0 = Vector((-0.18262259662151337, 6.799549367997315e-08, -1.2501908540725708))
p1 = Vector((0.1815710812807083, 6.799549367997315e-08, -1.2501908540725708))
p2 = Vector((-0.18262259662151337, -1.9427282893502706e-08, 0.7498091459274292))
p3 = Vector((0.1815710812807083, -1.9427282893502706e-08, 0.7498091459274292))
p4 = Vector((-0.18262259662151337, -1.9427282893502706e-08, 1.1021496057510376))
p5 = Vector((0.1815710812807083, -1.9427282893502706e-08, 1.1021496057510376))
p6 = Vector((-0.45311158895492554, -1.9427282893502706e-08, 0.7498091459274292))
p7 = Vector((0.4567919075489044, -1.9427282893502706e-08, 0.7498091459274292))
p8 = Vector((-0.0005257626180537045, -1.9427282893502706e-08, 1.342955231666565))
p9 = Vector((-0.18262259662151337, 0.06851532310247421, -1.2501908540725708))
p10 = Vector((0.1815710812807083, 0.06851532310247421, -1.2501908540725708))
p11 = Vector((-0.18262259662151337, 0.06851523369550705, 0.7498091459274292))
p12 = Vector((0.1815710812807083, 0.06851523369550705, 0.7498091459274292))
p13 = Vector((-0.18262259662151337, 0.06851523369550705, 1.1021496057510376))
p14 = Vector((0.1815710812807083, 0.06851523369550705, 1.1021496057510376))
p15 = Vector((-0.45311158895492554, 0.06851523369550705, 0.7498091459274292))
p16 = Vector((0.4567919075489044, 0.06851523369550705, 0.7498091459274292))
p17 = Vector((-0.0005257626180537045, 0.06851523369550705, 1.342955231666565))

arrowup_shape_verts = (
    p2,
    p1,
    p0,
    p4,
    p3,
    p2,
    p2,
    p6,
    p4,
    p5,
    p7,
    p3,
    p4,
    p8,
    p5,
    p10,
    p11,
    p9,
    p12,
    p13,
    p11,
    p11,
    p13,
    p15,
    p14,
    p12,
    p16,
    p13,
    p14,
    p17,
    p1,
    p9,
    p0,
    p2,
    p15,
    p6,
    p8,
    p14,
    p5,
    p3,
    p10,
    p1,
    p6,
    p13,
    p4,
    p7,
    p12,
    p3,
    p0,
    p11,
    p2,
    p4,
    p17,
    p8,
    p5,
    p16,
    p7,
    p2,
    p3,
    p1,
    p4,
    p5,
    p3,
    p10,
    p12,
    p11,
    p12,
    p14,
    p13,
    p1,
    p10,
    p9,
    p2,
    p11,
    p15,
    p8,
    p17,
    p14,
    p3,
    p12,
    p10,
    p6,
    p15,
    p13,
    p7,
    p16,
    p12,
    p0,
    p9,
    p11,
    p4,
    p13,
    p17,
    p5,
    p14,
    p16,)


class PUrP_ArrowUpShapeWidget(Gizmo):
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
                'TRIS', arrowup_shape_verts)

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
linecount0 = Vector(
    (-0.47405409812927246, -0.3000001907348633, -0.27930986881256104))
linecount1 = Vector(
    (0.47405409812927246, -0.3000001907348633, -0.27930986881256104))
linecount2 = Vector(
    (-0.47405409812927246, -0.3000001907348633, 0.2793097496032715))
linecount3 = Vector(
    (0.47405409812927246, -0.3000001907348633, 0.2793097496032715))
linecount4 = Vector(
    (-0.47405409812927246, -2.384185791015625e-07, -0.27930986881256104))
linecount5 = Vector(
    (0.47405409812927246, -2.384185791015625e-07, -0.27930986881256104))
linecount6 = Vector(
    (-0.47405409812927246, -2.384185791015625e-07, 0.2793097496032715))
linecount7 = Vector(
    (0.47405409812927246, -2.384185791015625e-07, 0.2793097496032715))
linecount8 = Vector(
    (-0.47405409812927246, 0.2999997138977051, -0.27930986881256104))
linecount9 = Vector(
    (0.47405409812927246, 0.2999997138977051, -0.27930986881256104))
linecount10 = Vector(
    (-0.47405409812927246, 0.2999997138977051, 0.2793097496032715))
linecount11 = Vector(
    (0.47405409812927246, 0.2999997138977051, 0.2793097496032715))
linecount12 = Vector(
    (-0.47405409812927246, -0.26971444487571716, -0.27930986881256104))
linecount13 = Vector(
    (0.47405409812927246, -0.26971444487571716, -0.27930986881256104))
linecount14 = Vector(
    (-0.47405409812927246, -0.26971444487571716, 0.2793097496032715))
linecount15 = Vector(
    (0.47405409812927246, -0.26971444487571716, 0.2793097496032715))
linecount16 = Vector(
    (-0.47405409812927246, 0.030285514891147614, -0.27930986881256104))
linecount17 = Vector(
    (0.47405409812927246, 0.030285514891147614, -0.27930986881256104))
linecount18 = Vector(
    (-0.47405409812927246, 0.030285514891147614, 0.2793097496032715))
linecount19 = Vector(
    (0.47405409812927246, 0.030285514891147614, 0.2793097496032715))
linecount20 = Vector(
    (-0.47405409812927246, 0.3302854597568512, -0.27930986881256104))
linecount21 = Vector(
    (0.47405409812927246, 0.3302854597568512, -0.27930986881256104))
linecount22 = Vector(
    (-0.47405409812927246, 0.3302854597568512, 0.2793097496032715))
linecount23 = Vector(
    (0.47405409812927246, 0.3302854597568512, 0.2793097496032715))


linecount_shape_verts = (
    linecount1,
    linecount0,
    linecount2,
    linecount5,
    linecount4,
    linecount6,
    linecount9,
    linecount8,
    linecount10,
    linecount1,
    linecount2,
    linecount3,
    linecount5,
    linecount6,
    linecount7,
    linecount9,
    linecount10,
    linecount11,
    linecount13,
    linecount14,
    linecount12,
    linecount17,
    linecount18,
    linecount16,
    linecount21,
    linecount22,
    linecount20,
    linecount13,
    linecount15,
    linecount14,
    linecount17,
    linecount19,
    linecount18,
    linecount21,
    linecount23,
    linecount22,
    linecount3,
    linecount13,
    linecount1,
    linecount9,
    linecount20,
    linecount8,
    linecount7,
    linecount17,
    linecount5,
    linecount2,
    linecount15,
    linecount3,
    linecount11,
    linecount21,
    linecount9,
    linecount0,
    linecount14,
    linecount2,
    linecount6,
    linecount19,
    linecount7,
    linecount4,
    linecount18,
    linecount6,
    linecount10,
    linecount23,
    linecount11,
    linecount1,
    linecount12,
    linecount0,
    linecount8,
    linecount22,
    linecount10,
    linecount5,
    linecount16,
    linecount4,
    linecount3,
    linecount15,
    linecount13,
    linecount9,
    linecount21,
    linecount20,
    linecount7,
    linecount19,
    linecount17,
    linecount2,
    linecount14,
    linecount15,
    linecount11,
    linecount23,
    linecount21,
    linecount0,
    linecount12,
    linecount14,
    linecount6,
    linecount18,
    linecount19,
    linecount4,
    linecount16,
    linecount18,
    linecount10,
    linecount22,
    linecount23,
    linecount1,
    linecount13,
    linecount12,
    linecount8,
    linecount20,
    linecount22,
    linecount5,
    linecount17,
    linecount16,)


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

linelength0 = Vector(
    (-0.5301038026809692, -0.0629303902387619, -0.27930986881256104))
linelength1 = Vector(
    (0.5301038026809692, -0.0629303902387619, -0.27930986881256104))
linelength2 = Vector(
    (-0.5301038026809692, -0.0629303902387619, 0.27930986881256104))
linelength3 = Vector(
    (0.5301038026809692, -0.0629303902387619, 0.27930986881256104))
linelength4 = Vector(
    (-0.34048211574554443, -0.0629303902387619, 0.27930986881256104))
linelength5 = Vector(
    (-0.1508605033159256, -0.0629303902387619, 0.27930986881256104))
linelength6 = Vector(
    (0.1508604735136032, -0.0629303902387619, 0.27930986881256104))
linelength7 = Vector(
    (0.3404821455478668, -0.0629303902387619, 0.27930986881256104))
linelength8 = Vector(
    (0.3404821455478668, -0.0629303902387619, -0.27930986881256104))
linelength9 = Vector(
    (0.1508605033159256, -0.0629303902387619, -0.27930986881256104))
linelength10 = Vector(
    (-0.1508604735136032, -0.0629303902387619, -0.27930986881256104))
linelength11 = Vector(
    (-0.34048211574554443, -0.0629303902387619, -0.27930986881256104))
linelength12 = Vector(
    (-0.1508605033159256, 0.09439557790756226, 0.27930986881256104))
linelength13 = Vector(
    (-0.34048211574554443, 0.09439557790756226, 0.27930986881256104))
linelength14 = Vector(
    (0.3404821455478668, 0.09439557790756226, 0.27930986881256104))
linelength15 = Vector(
    (0.1508604735136032, 0.09439557790756226, 0.27930986881256104))
linelength16 = Vector(
    (0.1508605033159256, 0.09439557790756226, -0.27930986881256104))
linelength17 = Vector(
    (0.3404821455478668, 0.09439557790756226, -0.27930986881256104))
linelength18 = Vector(
    (-0.34048211574554443, 0.09439557790756226, -0.27930986881256104))
linelength19 = Vector(
    (-0.1508604735136032, 0.09439557790756226, -0.27930986881256104))
linelength20 = Vector(
    (-0.5301038026809692, -0.032930389046669006, -0.27930986881256104))
linelength21 = Vector(
    (0.5301038026809692, -0.03293130546808243, -0.27930986881256104))
linelength22 = Vector(
    (-0.5301038026809692, -0.032930389046669006, 0.27930986881256104))
linelength23 = Vector(
    (0.5301038026809692, -0.032930389046669006, 0.27930986881256104))
linelength24 = Vector(
    (-0.3616946041584015, -0.04171789065003395, 0.27930986881256104))
linelength25 = Vector(
    (-0.12964800000190735, -0.04171789065003395, 0.27930986881256104))
linelength26 = Vector(
    (0.12964797019958496, -0.04171789065003395, 0.27930986881256104))
linelength27 = Vector(
    (0.3616946339607239, -0.04171789065003395, 0.27930986881256104))
linelength28 = Vector(
    (0.3616946339607239, -0.04171789065003395, -0.27930986881256104))
linelength29 = Vector(
    (0.12964800000190735, -0.04171789065003395, -0.27930986881256104))
linelength30 = Vector(
    (-0.12964797019958496, -0.04171789065003395, -0.27930986881256104))
linelength31 = Vector(
    (-0.3616946041584015, -0.04171789065003395, -0.27930986881256104))
linelength32 = Vector(
    (-0.12964800000190735, 0.1156080812215805, 0.27930986881256104))
linelength33 = Vector(
    (-0.3616946041584015, 0.1156080812215805, 0.27930986881256104))
linelength34 = Vector(
    (0.3616946339607239, 0.1156080812215805, 0.27930986881256104))
linelength35 = Vector(
    (0.12964797019958496, 0.1156080812215805, 0.27930986881256104))
linelength36 = Vector(
    (0.12964800000190735, 0.1156080812215805, -0.27930986881256104))
linelength37 = Vector(
    (0.3616946339607239, 0.1156080812215805, -0.27930986881256104))
linelength38 = Vector(
    (-0.3616946041584015, 0.1156080812215805, -0.27930986881256104))
linelength39 = Vector(
    (-0.12964797019958496, 0.1156080812215805, -0.27930986881256104))

linelength_shape_verts = (
    linelength1,
    linelength7,
    linelength8,
    linelength11,
    linelength2,
    linelength0,
    linelength9,
    linelength5,
    linelength10,
    linelength18,
    linelength12,
    linelength13,
    linelength16,
    linelength14,
    linelength15,
    linelength7,
    linelength17,
    linelength8,
    linelength5,
    linelength19,
    linelength10,
    linelength9,
    linelength15,
    linelength6,
    linelength11,
    linelength13,
    linelength4,
    linelength1,
    linelength3,
    linelength7,
    linelength11,
    linelength4,
    linelength2,
    linelength9,
    linelength6,
    linelength5,
    linelength18,
    linelength19,
    linelength12,
    linelength16,
    linelength17,
    linelength14,
    linelength7,
    linelength14,
    linelength17,
    linelength5,
    linelength12,
    linelength19,
    linelength9,
    linelength16,
    linelength15,
    linelength11,
    linelength18,
    linelength13,
    linelength21,
    linelength28,
    linelength27,
    linelength31,
    linelength20,
    linelength22,
    linelength29,
    linelength30,
    linelength25,
    linelength38,
    linelength33,
    linelength32,
    linelength36,
    linelength35,
    linelength34,
    linelength27,
    linelength28,
    linelength37,
    linelength25,
    linelength30,
    linelength39,
    linelength29,
    linelength26,
    linelength35,
    linelength31,
    linelength24,
    linelength33,
    linelength21,
    linelength27,
    linelength23,
    linelength31,
    linelength22,
    linelength24,
    linelength29,
    linelength25,
    linelength26,
    linelength38,
    linelength32,
    linelength39,
    linelength36,
    linelength34,
    linelength37,
    linelength27,
    linelength37,
    linelength34,
    linelength25,
    linelength39,
    linelength32,
    linelength29,
    linelength35,
    linelength36,
    linelength31,
    linelength33,
    linelength38,
    linelength2,
    linelength20,
    linelength0,
    linelength1,
    linelength28,
    linelength21,
    linelength3,
    linelength21,
    linelength23,
    linelength2,
    linelength24,
    linelength22,
    linelength6,
    linelength25,
    linelength5,
    linelength3,
    linelength27,
    linelength7,
    linelength10,
    linelength29,
    linelength9,
    linelength0,
    linelength31,
    linelength11,
    linelength12,
    linelength33,
    linelength13,
    linelength14,
    linelength35,
    linelength15,
    linelength16,
    linelength37,
    linelength17,
    linelength18,
    linelength39,
    linelength19,
    linelength19,
    linelength30,
    linelength10,
    linelength18,
    linelength31,
    linelength38,
    linelength17,
    linelength28,
    linelength8,
    linelength16,
    linelength29,
    linelength36,
    linelength15,
    linelength26,
    linelength6,
    linelength14,
    linelength27,
    linelength34,
    linelength13,
    linelength24,
    linelength4,
    linelength12,
    linelength25,
    linelength32,
    linelength2,
    linelength22,
    linelength20,
    linelength1,
    linelength8,
    linelength28,
    linelength3,
    linelength1,
    linelength21,
    linelength2,
    linelength4,
    linelength24,
    linelength6,
    linelength26,
    linelength25,
    linelength3,
    linelength23,
    linelength27,
    linelength10,
    linelength30,
    linelength29,
    linelength0,
    linelength20,
    linelength31,
    linelength12,
    linelength32,
    linelength33,
    linelength14,
    linelength34,
    linelength35,
    linelength16,
    linelength36,
    linelength37,
    linelength18,
    linelength38,
    linelength39,
    linelength19,
    linelength39,
    linelength30,
    linelength18,
    linelength11,
    linelength31,
    linelength17,
    linelength37,
    linelength28,
    linelength16,
    linelength9,
    linelength29,
    linelength15,
    linelength35,
    linelength26,
    linelength14,
    linelength7,
    linelength27,
    linelength13,
    linelength33,
    linelength24,
    linelength12,
    linelength5,
    linelength25,
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

linedistance0 = Vector(
    (-0.47405412793159485, -0.015096773393452168, -0.27930986881256104))
linedistance1 = Vector(
    (0.47405412793159485, -0.015096773393452168, -0.27930986881256104))
linedistance2 = Vector(
    (-0.47405412793159485, -0.015096773393452168, 0.27930986881256104))
linedistance3 = Vector(
    (0.47405412793159485, -0.015096773393452168, 0.27930986881256104))
linedistance4 = Vector(
    (-0.47405412793159485, 0.28490322828292847, -0.27930986881256104))
linedistance5 = Vector(
    (0.47405412793159485, 0.28490322828292847, -0.27930986881256104))
linedistance6 = Vector(
    (-0.47405412793159485, 0.28490322828292847, 0.27930986881256104))
linedistance7 = Vector(
    (0.47405412793159485, 0.28490322828292847, 0.27930986881256104))
linedistance8 = Vector(
    (0.07070715725421906, 0.3107404410839081, 0.4522562026977539))
linedistance9 = Vector(
    (-0.19720323383808136, 0.3107404410839081, 0.4522562026977539))
linedistance10 = Vector(
    (0.07070715725421906, -0.010376221500337124, 0.4522562026977539))
linedistance11 = Vector(
    (-0.19720323383808136, -0.010376221500337124, 0.4522562026977539))
linedistance12 = Vector(
    (0.07070715725421906, 0.3151625394821167, 0.33240607380867004))
linedistance13 = Vector(
    (-0.19720323383808136, 0.3151625394821167, 0.33240607380867004))
linedistance14 = Vector(
    (0.07070715725421906, -0.014798318035900593, 0.33240607380867004))
linedistance15 = Vector(
    (-0.19720323383808136, -0.014798318035900593, 0.33240607380867004))
linedistance16 = Vector(
    (-0.47405412793159485, 0.014903225935995579, -0.27930986881256104))
linedistance17 = Vector(
    (0.47405412793159485, 0.014903225935995579, -0.27930986881256104))
linedistance18 = Vector(
    (-0.47405412793159485, 0.014903225935995579, 0.27930986881256104))
linedistance19 = Vector(
    (0.47405412793159485, 0.014903225935995579, 0.27930986881256104))
linedistance20 = Vector(
    (-0.47405412793159485, 0.31490322947502136, -0.27930986881256104))
linedistance21 = Vector(
    (0.47405412793159485, 0.31490322947502136, -0.27930986881256104))
linedistance22 = Vector(
    (-0.47405412793159485, 0.31490322947502136, 0.27930986881256104))
linedistance23 = Vector(
    (0.47405412793159485, 0.31490322947502136, 0.27930986881256104))
linedistance24 = Vector(
    (0.07070715725421906, 0.28952792286872864, 0.43104368448257446))
linedistance25 = Vector(
    (-0.19720323383808136, 0.28952792286872864, 0.43104368448257446))
linedistance26 = Vector(
    (0.07070715725421906, 0.010836278088390827, 0.43104368448257446))
linedistance27 = Vector(
    (-0.19720323383808136, 0.010836278088390827, 0.43104368448257446))
linedistance28 = Vector(
    (0.07070715725421906, 0.2851625382900238, 0.33240607380867004))
linedistance29 = Vector(
    (-0.19720323383808136, 0.2851625382900238, 0.33240607380867004))
linedistance30 = Vector(
    (0.07070715725421906, 0.015201681293547153, 0.33240607380867004))
linedistance31 = Vector(
    (-0.19720323383808136, 0.015201681293547153, 0.33240607380867004))

linedistant_shape_verts = (
    linedistance1,
    linedistance2,
    linedistance0,
    linedistance5,
    linedistance6,
    linedistance4,
    linedistance11,
    linedistance14,
    linedistance10,
    linedistance1,
    linedistance3,
    linedistance2,
    linedistance5,
    linedistance7,
    linedistance6,
    linedistance10,
    linedistance9,
    linedistance11,
    linedistance8,
    linedistance13,
    linedistance9,
    linedistance11,
    linedistance15,
    linedistance14,
    linedistance10,
    linedistance8,
    linedistance9,
    linedistance8,
    linedistance12,
    linedistance13,
    linedistance17,
    linedistance16,
    linedistance18,
    linedistance21,
    linedistance20,
    linedistance22,
    linedistance27,
    linedistance26,
    linedistance30,
    linedistance17,
    linedistance18,
    linedistance19,
    linedistance21,
    linedistance22,
    linedistance23,
    linedistance26,
    linedistance27,
    linedistance25,
    linedistance24,
    linedistance25,
    linedistance29,
    linedistance27,
    linedistance30,
    linedistance31,
    linedistance26,
    linedistance25,
    linedistance24,
    linedistance24,
    linedistance29,
    linedistance28,
    linedistance2,
    linedistance16,
    linedistance0,
    linedistance0,
    linedistance17,
    linedistance1,
    linedistance1,
    linedistance19,
    linedistance3,
    linedistance3,
    linedistance18,
    linedistance2,
    linedistance6,
    linedistance20,
    linedistance4,
    linedistance4,
    linedistance21,
    linedistance5,
    linedistance5,
    linedistance23,
    linedistance7,
    linedistance7,
    linedistance22,
    linedistance6,
    linedistance12,
    linedistance29,
    linedistance13,
    linedistance10,
    linedistance24,
    linedistance8,
    linedistance9,
    linedistance27,
    linedistance11,
    linedistance15,
    linedistance30,
    linedistance14,
    linedistance14,
    linedistance26,
    linedistance10,
    linedistance15,
    linedistance27,
    linedistance31,
    linedistance13,
    linedistance25,
    linedistance9,
    linedistance12,
    linedistance24,
    linedistance28,
    linedistance2,
    linedistance18,
    linedistance16,
    linedistance0,
    linedistance16,
    linedistance17,
    linedistance1,
    linedistance17,
    linedistance19,
    linedistance3,
    linedistance19,
    linedistance18,
    linedistance6,
    linedistance22,
    linedistance20,
    linedistance4,
    linedistance20,
    linedistance21,
    linedistance5,
    linedistance21,
    linedistance23,
    linedistance7,
    linedistance23,
    linedistance22,
    linedistance12,
    linedistance28,
    linedistance29,
    linedistance10,
    linedistance26,
    linedistance24,
    linedistance9,
    linedistance25,
    linedistance27,
    linedistance15,
    linedistance31,
    linedistance30,
    linedistance14,
    linedistance30,
    linedistance26,
    linedistance15,
    linedistance11,
    linedistance27,
    linedistance13,
    linedistance29,
    linedistance25,
    linedistance12,
    linedistance8,
    linedistance24,

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

# thickness widget


thickness0 = Vector((-0.25504493713378906, 0.0, -0.2793097496032715))
thickness1 = Vector((-0.30159735679626465, 0.0, -0.2793097496032715))
thickness2 = Vector((-0.25504493713378906, 0.0, 0.27930986881256104))
thickness3 = Vector((-0.30159735679626465, 0.0, 0.27930986881256104))
thickness4 = Vector((-0.1861875057220459, 0.0, 0.27930986881256104))
thickness5 = Vector((-0.3421952724456787, 0.0, 0.27930986881256104))
thickness6 = Vector((-0.3421952724456787, 0.0, -0.2793097496032715))
thickness7 = Vector((0.6702046394348145, 0.0, 0.27930986881256104))
thickness8 = Vector((0.28983044624328613, 0.0, 0.27930986881256104))
thickness9 = Vector((0.24941444396972656, 0.0, -0.2793097496032715))
thickness10 = Vector((0.28983044624328613, 0.0, -0.2793097496032715))
thickness11 = Vector((-0.1861875057220459, 0.0, -0.2793097496032715))
thickness12 = Vector((0.6702046394348145, 0.0, -0.2793097496032715))
thickness13 = Vector((0.02269768714904785, 0.0, -0.2793097496032715))
thickness14 = Vector((-0.007831096649169922, 0.0, -0.2793097496032715))
thickness15 = Vector((-0.007831096649169922, 0.0, 0.27930986881256104))
thickness16 = Vector((-0.13929295539855957, 0.0, 0.27930986881256104))
thickness17 = Vector((-0.13929295539855957, 0.0, -0.2793097496032715))
thickness18 = Vector((0.02269768714904785, 0.0, 0.27930986881256104))
thickness19 = Vector((0.24941444396972656, 0.0, 0.27930986881256104))
thickness20 = Vector(
    (-0.25504493713378906, 0.016856903210282326, -0.2793097496032715))
thickness21 = Vector(
    (-0.30159735679626465, 0.016856903210282326, -0.2793097496032715))
thickness22 = Vector(
    (-0.25504493713378906, 0.016856903210282326, 0.27930986881256104))
thickness23 = Vector(
    (-0.30159735679626465, 0.016856903210282326, 0.27930986881256104))
thickness24 = Vector(
    (-0.1861875057220459, 0.016856903210282326, 0.27930986881256104))
thickness25 = Vector(
    (-0.3421952724456787, 0.016856903210282326, 0.27930986881256104))
thickness26 = Vector(
    (-0.3421952724456787, 0.016856903210282326, -0.2793097496032715))
thickness27 = Vector(
    (0.6702046394348145, 0.016856903210282326, 0.27930986881256104))
thickness28 = Vector(
    (0.28983044624328613, 0.016856903210282326, 0.27930986881256104))
thickness29 = Vector(
    (0.24941444396972656, 0.016856903210282326, -0.2793097496032715))
thickness30 = Vector(
    (0.28983044624328613, 0.016856903210282326, -0.2793097496032715))
thickness31 = Vector(
    (-0.1861875057220459, 0.016856903210282326, -0.2793097496032715))
thickness32 = Vector(
    (0.6702046394348145, 0.016856903210282326, -0.2793097496032715))
thickness33 = Vector(
    (0.02269768714904785, 0.016856903210282326, -0.2793097496032715))
thickness34 = Vector(
    (-0.007831096649169922, 0.016856903210282326, -0.2793097496032715))
thickness35 = Vector(
    (-0.007831096649169922, 0.016856903210282326, 0.27930986881256104))
thickness36 = Vector(
    (-0.13929295539855957, 0.016856903210282326, 0.27930986881256104))
thickness37 = Vector(
    (-0.13929295539855957, 0.016856903210282326, -0.2793097496032715))
thickness38 = Vector(
    (0.02269768714904785, 0.016856903210282326, 0.27930986881256104))
thickness39 = Vector(
    (0.24941444396972656, 0.016856903210282326, 0.27930986881256104))


thickness_shape_verts = (
    thickness11,
    thickness0,
    thickness2,
    thickness9,
    thickness18,
    thickness19,
    thickness11,
    thickness2,
    thickness4,
    thickness1,
    thickness5,
    thickness3,
    thickness1,
    thickness6,
    thickness5,
    thickness14,
    thickness16,
    thickness15,
    thickness12,
    thickness10,
    thickness8,
    thickness12,
    thickness8,
    thickness7,
    thickness14,
    thickness17,
    thickness16,
    thickness9,
    thickness13,
    thickness18,
    thickness31,
    thickness22,
    thickness20,
    thickness29,
    thickness39,
    thickness38,
    thickness31,
    thickness24,
    thickness22,
    thickness21,
    thickness23,
    thickness25,
    thickness21,
    thickness25,
    thickness26,
    thickness34,
    thickness35,
    thickness36,
    thickness32,
    thickness28,
    thickness30,
    thickness32,
    thickness27,
    thickness28,
    thickness34,
    thickness36,
    thickness37,
    thickness29,
    thickness38,
    thickness33,
    thickness14,
    thickness37,
    thickness17,
    thickness19,
    thickness29,
    thickness9,
    thickness7,
    thickness32,
    thickness12,
    thickness5,
    thickness23,
    thickness3,
    thickness16,
    thickness35,
    thickness15,
    thickness6,
    thickness25,
    thickness5,
    thickness13,
    thickness38,
    thickness18,
    thickness12,
    thickness30,
    thickness10,
    thickness15,
    thickness34,
    thickness14,
    thickness18,
    thickness39,
    thickness19,
    thickness0,
    thickness22,
    thickness2,
    thickness8,
    thickness27,
    thickness7,
    thickness17,
    thickness36,
    thickness16,
    thickness2,
    thickness24,
    thickness4,
    thickness10,
    thickness28,
    thickness8,
    thickness3,
    thickness21,
    thickness1,
    thickness9,
    thickness33,
    thickness13,
    thickness11,
    thickness20,
    thickness0,
    thickness1,
    thickness26,
    thickness6,
    thickness4,
    thickness31,
    thickness11,
    thickness14,
    thickness34,
    thickness37,
    thickness19,
    thickness39,
    thickness29,
    thickness7,
    thickness27,
    thickness32,
    thickness5,
    thickness25,
    thickness23,
    thickness16,
    thickness36,
    thickness35,
    thickness6,
    thickness26,
    thickness25,
    thickness13,
    thickness33,
    thickness38,
    thickness12,
    thickness32,
    thickness30,
    thickness15,
    thickness35,
    thickness34,
    thickness18,
    thickness38,
    thickness39,
    thickness0,
    thickness20,
    thickness22,
    thickness8,
    thickness28,
    thickness27,
    thickness17,
    thickness37,
    thickness36,
    thickness2,
    thickness22,
    thickness24,
    thickness10,
    thickness30,
    thickness28,
    thickness3,
    thickness23,
    thickness21,
    thickness9,
    thickness29,
    thickness33,
    thickness11,
    thickness31,
    thickness20,
    thickness1,
    thickness21,
    thickness26,
    thickness4,
    thickness24,
    thickness31,
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


cube0 = Vector((-0.6875224113464355, -0.6875224113464355, -0.6875224113464355))
cube1 = Vector((-0.6875224113464355, -0.6875224113464355, 0.6875224113464355))
cube2 = Vector((-0.6875224113464355, 0.6875224113464355, -0.6875224113464355))
cube3 = Vector((-0.6875224113464355, 0.6875224113464355, 0.6875224113464355))
cube4 = Vector((0.6875224113464355, -0.6875224113464355, -0.6875224113464355))
cube5 = Vector((0.6875224113464355, -0.6875224113464355, 0.6875224113464355))
cube6 = Vector((0.6875224113464355, 0.6875224113464355, -0.6875224113464355))
cube7 = Vector((0.6875224113464355, 0.6875224113464355, 0.6875224113464355))


cube_shape_verts = (
    cube0, cube1, cube3,
    cube0, cube2, cube3,
    cube7, cube2, cube3,
    cube7, cube2, cube6,
    cube6, cube5, cube7,
    cube6, cube5, cube4,
    cube1, cube5, cube4,
    cube0, cube1, cube4,
    cube0, cube2, cube4,
    cube6, cube2, cube4,
    cube1, cube3, cube7,
    cube1, cube5, cube7,

)


class PUrP_CubeShapeWidget(Gizmo):
    bl_idname = "VIEW3D_GT_PURP_Cube"
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
                'TRIS', cube_shape_verts)

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


cone0 = Vector((-1.0058283805847168e-07, 1.0, -0.5))
cone1 = Vector((7.790674771968042e-08, 0.2513604164123535, 0.5))
cone2 = Vector((0.3826833665370941, 0.9238795042037964, -0.5))
cone3 = Vector((0.09619154036045074, 0.23222671449184418, 0.5))
cone4 = Vector((0.7071066498756409, 0.7071067690849304, -0.5))
cone5 = Vector((0.1777387410402298, 0.17773865163326263, 0.5))
cone6 = Vector((0.9238793849945068, 0.3826834261417389, -0.5))
cone7 = Vector((0.23222680389881134, 0.09619145840406418, 0.5))
cone8 = Vector((0.9999998807907104, -5.3024614032892714e-08, -0.5))
cone9 = Vector((0.2513605058193207, -2.030053991575187e-08, 0.5))
cone10 = Vector((0.9238793849945068, -0.38268351554870605, -0.5))
cone11 = Vector((0.23222680389881134, -0.09619150310754776, 0.5))
cone12 = Vector((0.7071066498756409, -0.7071067690849304, -0.5))
cone13 = Vector((0.1777387410402298, -0.17773868143558502, 0.5))
cone14 = Vector((0.3826833963394165, -0.9238795042037964, -0.5))
cone15 = Vector((0.09619157016277313, -0.23222674429416656, 0.5))
cone16 = Vector((5.041296446961496e-08, -1.0, -0.5))
cone17 = Vector((1.1586111270389665e-07, -0.2513604164123535, 0.5))
cone18 = Vector((-0.38268330693244934, -0.9238796234130859, -0.5))
cone19 = Vector((-0.09619133174419403, -0.23222680389881134, 0.5))
cone20 = Vector((-0.7071067094802856, -0.7071070075035095, -0.5))
cone21 = Vector((-0.17773853242397308, -0.1777387410402298, 0.5))
cone22 = Vector((-0.9238796234130859, -0.38268357515335083, -0.5))
cone23 = Vector((-0.2322266548871994, -0.09619150310754776, 0.5))
cone24 = Vector((-1.0000001192092896, 2.6116548923482696e-09, -0.5))
cone25 = Vector((-0.25136032700538635, -6.315782563603989e-09, 0.5))
cone26 = Vector((-0.9238795638084412, 0.3826836049556732, -0.5))
cone27 = Vector((-0.2322266548871994, 0.09619148820638657, 0.5))
cone28 = Vector((-0.7071066498756409, 0.7071070075035095, -0.5))
cone29 = Vector((-0.17773853242397308, 0.1777387112379074, 0.5))
cone30 = Vector((-0.38268306851387024, 0.9238797426223755, -0.5))
cone31 = Vector((-0.09619127213954926, 0.23222677409648895, 0.5))

cone_shape_verts = (
    cone1, cone2, cone0,
    cone3, cone4, cone2,
    cone5, cone6, cone4,
    cone7, cone8, cone6,
    cone9, cone10, cone8,
    cone11, cone12, cone10,
    cone13, cone14, cone12,
    cone15, cone16, cone14,
    cone17, cone18, cone16,
    cone19, cone20, cone18,
    cone21, cone22, cone20,
    cone23, cone24, cone22,
    cone25, cone26, cone24,
    cone27, cone28, cone26,
    cone17, cone13, cone5,
    cone29, cone30, cone28,
    cone31, cone0, cone30,
    cone6, cone14, cone22,
    cone1, cone3, cone2,
    cone3, cone5, cone4,
    cone5, cone7, cone6,
    cone7, cone9, cone8,
    cone9, cone11, cone10,
    cone11, cone13, cone12,
    cone13, cone15, cone14,
    cone15, cone17, cone16,
    cone17, cone19, cone18,
    cone19, cone21, cone20,
    cone21, cone23, cone22,
    cone23, cone25, cone24,
    cone25, cone27, cone26,
    cone27, cone29, cone28,
    cone5, cone3, cone29,
    cone3, cone1, cone29,
    cone1, cone31, cone29,
    cone29, cone27, cone25,
    cone25, cone23, cone21,
    cone21, cone19, cone17,
    cone17, cone15, cone13,
    cone13, cone11, cone5,
    cone11, cone9, cone5,
    cone9, cone7, cone5,
    cone29, cone25, cone5,
    cone25, cone21, cone5,
    cone21, cone17, cone5,
    cone29, cone31, cone30,
    cone31, cone1, cone0,
    cone30, cone0, cone6,
    cone0, cone2, cone6,
    cone2, cone4, cone6,
    cone6, cone8, cone10,
    cone10, cone12, cone6,
    cone12, cone14, cone6,
    cone14, cone16, cone22,
    cone16, cone18, cone22,
    cone18, cone20, cone22,
    cone22, cone24, cone30,
    cone24, cone26, cone30,
    cone26, cone28, cone30,
    cone30, cone6, cone22,
)


class PUrP_ConeShapeWidget(Gizmo):
    bl_idname = "VIEW3D_GT_PURP_Cone"
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
                'TRIS', cone_shape_verts)

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


cylinder0 = Vector((-1.6669440583427786e-07, 1.699167013168335, -0.5))
cylinder1 = Vector((0.0, 1.0, 0.5))
cylinder2 = Vector((0.6502429246902466, 1.569825530052185, -0.5))
cylinder3 = Vector((0.3826834559440613, 0.9238795042037964, 0.5))
cylinder4 = Vector((1.2014923095703125, 1.2014925479888916, -0.5))
cylinder5 = Vector((0.7071067690849304, 0.7071067690849304, 0.5))
cylinder6 = Vector((1.5698254108428955, 0.6502430438995361, -0.5))
cylinder7 = Vector((0.9238795042037964, 0.3826834261417389, 0.5))
cylinder8 = Vector((1.6991668939590454, -7.427294690387498e-08, -0.5))
cylinder9 = Vector((1.0, -4.371138828673793e-08, 0.5))
cylinder10 = Vector((1.5698254108428955, -0.6502432227134705, -0.5))
cylinder11 = Vector((0.9238795042037964, -0.38268351554870605, 0.5))
cylinder12 = Vector((1.2014923095703125, -1.2014925479888916, -0.5))
cylinder13 = Vector((0.7071067690849304, -0.7071067690849304, 0.5))
cylinder14 = Vector((0.6502429842948914, -1.569825530052185, -0.5))
cylinder15 = Vector((0.38268348574638367, -0.9238795042037964, 0.5))
cylinder16 = Vector((8.987268529381254e-08, -1.699167013168335, -0.5))
cylinder17 = Vector((1.5099580252808664e-07, -1.0, 0.5))
cylinder18 = Vector((-0.6502428650856018, -1.5698257684707642, -0.5))
cylinder19 = Vector((-0.3826832175254822, -0.9238796234130859, 0.5))
cylinder20 = Vector((-1.2014923095703125, -1.2014929056167603, -0.5))
cylinder21 = Vector((-0.7071065902709961, -0.7071070075035095, 0.5))
cylinder22 = Vector((-1.5698257684707642, -0.6502432823181152, -0.5))
cylinder23 = Vector((-0.9238795042037964, -0.38268357515335083, 0.5))
cylinder24 = Vector((-1.6991671323776245, 2.026236423091632e-08, -0.5))
cylinder25 = Vector((-1.0, 1.1924880638503055e-08, 0.5))
cylinder26 = Vector((-1.5698256492614746, 0.65024334192276, -0.5))
cylinder27 = Vector((-0.9238794445991516, 0.3826836049556732, 0.5))
cylinder28 = Vector((-1.2014923095703125, 1.2014929056167603, -0.5))
cylinder29 = Vector((-0.7071065306663513, 0.7071070075035095, 0.5))
cylinder30 = Vector((-0.6502424478530884, 1.5698260068893433, -0.5))
cylinder31 = Vector((-0.3826829791069031, 0.9238797426223755, 0.5))


cylinder_shape_verts = (
    cylinder1, cylinder2, cylinder0,
    cylinder3, cylinder4, cylinder2,
    cylinder5, cylinder6, cylinder4,
    cylinder7, cylinder8, cylinder6,
    cylinder9, cylinder10, cylinder8,
    cylinder11, cylinder12, cylinder10,
    cylinder13, cylinder14, cylinder12,
    cylinder15, cylinder16, cylinder14,
    cylinder17, cylinder18, cylinder16,
    cylinder19, cylinder20, cylinder18,
    cylinder21, cylinder22, cylinder20,
    cylinder23, cylinder24, cylinder22,
    cylinder25, cylinder26, cylinder24,
    cylinder27, cylinder28, cylinder26,
    cylinder5, cylinder29, cylinder21,
    cylinder29, cylinder30, cylinder28,
    cylinder31, cylinder0, cylinder30,
    cylinder6, cylinder14, cylinder22,
    cylinder1, cylinder3, cylinder2,
    cylinder3, cylinder5, cylinder4,
    cylinder5, cylinder7, cylinder6,
    cylinder7, cylinder9, cylinder8,
    cylinder9, cylinder11, cylinder10,
    cylinder11, cylinder13, cylinder12,
    cylinder13, cylinder15, cylinder14,
    cylinder15, cylinder17, cylinder16,
    cylinder17, cylinder19, cylinder18,
    cylinder19, cylinder21, cylinder20,
    cylinder21, cylinder23, cylinder22,
    cylinder23, cylinder25, cylinder24,
    cylinder25, cylinder27, cylinder26,
    cylinder27, cylinder29, cylinder28,
    cylinder5, cylinder3, cylinder1,
    cylinder1, cylinder31, cylinder29,
    cylinder29, cylinder27, cylinder25,
    cylinder25, cylinder23, cylinder21,
    cylinder21, cylinder19, cylinder17,
    cylinder17, cylinder15, cylinder13,
    cylinder13, cylinder11, cylinder9,
    cylinder9, cylinder7, cylinder13,
    cylinder7, cylinder5, cylinder13,
    cylinder5, cylinder1, cylinder29,
    cylinder29, cylinder25, cylinder21,
    cylinder21, cylinder17, cylinder5,
    cylinder17, cylinder13, cylinder5,
    cylinder29, cylinder31, cylinder30,
    cylinder31, cylinder1, cylinder0,
    cylinder30, cylinder0, cylinder2,
    cylinder2, cylinder4, cylinder30,
    cylinder4, cylinder6, cylinder30,
    cylinder6, cylinder8, cylinder10,
    cylinder10, cylinder12, cylinder6,
    cylinder12, cylinder14, cylinder6,
    cylinder14, cylinder16, cylinder22,
    cylinder16, cylinder18, cylinder22,
    cylinder18, cylinder20, cylinder22,
    cylinder22, cylinder24, cylinder26,
    cylinder26, cylinder28, cylinder30,
    cylinder22, cylinder26, cylinder30,
    cylinder30, cylinder6, cylinder22,)


class PUrP_CylinderShapeWidget(Gizmo):
    bl_idname = "VIEW3D_GT_PURP_Cylinder"
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
                'TRIS', cylinder_shape_verts)

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
