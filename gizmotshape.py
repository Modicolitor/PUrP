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
p9 = Vector((-0.18262259662151337, -4.856819835197257e-09, 0.4164758026599884))
p10 = Vector((-0.18262259662151337, 9.713643223108193e-09, 0.08314245939254761))
p11 = Vector(
    (-0.18262259662151337, 2.4284105393235222e-08, -0.2501908540725708))
p12 = Vector((-0.18262259662151337, 3.885456933971909e-08, -0.583524227142334))
p13 = Vector((-0.18262259662151337, 5.342503328620296e-08, -0.9168575406074524))
p14 = Vector((0.1815710812807083, 5.342502973348928e-08, -0.9168574810028076))
p15 = Vector((0.1815710812807083, 3.885456578700541e-08, -0.5835241079330444))
p16 = Vector((0.1815710812807083, 2.4284103616878383e-08, -0.250190794467926))
p17 = Vector((0.1815710812807083, 9.713640558572934e-09, 0.08314251899719238))
p18 = Vector((0.1815710812807083, -4.856821611554096e-09, 0.4164758324623108))
p19 = Vector((-0.18262259662151337, 5.82818522332218e-08, -1.0279686450958252))
p20 = Vector((-0.18262259662151337, 6.313867118024064e-08, -1.1390798091888428))
p21 = Vector((-0.06122469902038574, 6.799549367997315e-08, -1.2501908540725708))
p22 = Vector((0.060173191130161285, 6.799549367997315e-08, -1.2501908540725708))
p23 = Vector((0.1815710812807083, -9.713642334929773e-09, 0.5275869369506836))
p24 = Vector((0.1815710812807083, -1.457046217012703e-08, 0.6386980414390564))
p25 = Vector((0.06017318367958069, -1.9427282893502706e-08, 0.7498091459274292))
p26 = Vector(
    (-0.06122470647096634, -1.9427282893502706e-08, 0.7498091459274292))
p27 = Vector((0.06017318367958069, -1.9427282893502706e-08, 1.1021496057510376))
p28 = Vector(
    (-0.06122470647096634, -1.9427282893502706e-08, 1.1021496057510376))
p29 = Vector(
    (-0.18262259662151337, -1.9427282893502706e-08, 0.9847027659416199))
p30 = Vector(
    (-0.18262259662151337, -1.9427282893502706e-08, 0.8672559261322021))
p31 = Vector((0.1815710812807083, -1.9427282893502706e-08, 0.8672559857368469))
p32 = Vector((0.1815710812807083, -1.9427282893502706e-08, 0.9847028255462646))
p33 = Vector(
    (-0.06122471019625664, -1.9427282893502706e-08, 1.2626867294311523))
p34 = Vector(
    (-0.12192365527153015, -1.9427282893502706e-08, 1.1824181079864502))
p35 = Vector(
    (-0.36294859647750854, -1.9427282893502706e-08, 0.7498091459274292))
p36 = Vector(
    (-0.27278560400009155, -1.9427282893502706e-08, 0.7498091459274292))
p37 = Vector(
    (-0.27278560400009155, -1.9427282893502706e-08, 0.9847027659416199))
p38 = Vector(
    (-0.36294859647750854, -1.9427282893502706e-08, 0.8672559261322021))
p39 = Vector((0.2733113467693329, -1.9427282893502706e-08, 0.7498091459274292))
p40 = Vector((0.36505162715911865, -1.9427282893502706e-08, 0.7498091459274292))
p41 = Vector((0.36505162715911865, -1.9427282893502706e-08, 0.8672559857368469))
p42 = Vector((0.2733113467693329, -1.9427282893502706e-08, 0.9847028255462646))
p43 = Vector((0.1208721324801445, -1.9427282893502706e-08, 1.1824181079864502))
p44 = Vector((0.06017318367958069, -1.9427282893502706e-08, 1.2626867294311523))
p45 = Vector((-0.18262259662151337, -1.457046217012703e-08, 0.6386980414390564))
p46 = Vector((-0.18262259662151337, -9.713641446751353e-09, 0.5275869369506836))
p47 = Vector((-0.18262259662151337, 1.3322676295501878e-15, 0.3053646683692932))
p48 = Vector((-0.18262259662151337, 4.856822055643306e-09, 0.1942535638809204))
p49 = Vector(
    (-0.18262259662151337, 1.457046394648387e-08, -0.027968645095825195))
p50 = Vector((-0.18262259662151337, 1.9427284669859546e-08, -0.139079749584198))
p51 = Vector((-0.18262259662151337, 2.914092789296774e-08, -0.361301988363266))
p52 = Vector(
    (-0.18262259662151337, 3.3997750392700254e-08, -0.4724131226539612))
p53 = Vector((-0.18262259662151337, 4.371139183945161e-08, -0.6946353316307068))
p54 = Vector(
    (-0.18262259662151337, 4.8568210786470445e-08, -0.8057464361190796))
p55 = Vector((0.1815710812807083, 6.313867118024064e-08, -1.1390796899795532))
p56 = Vector((0.1815710812807083, 5.828184868050812e-08, -1.0279686450958252))
p57 = Vector((0.1815710812807083, 4.8568207233756766e-08, -0.8057463765144348))
p58 = Vector((0.1815710812807083, 4.371138828673793e-08, -0.694635272026062))
p59 = Vector((0.1815710812807083, 3.39977432872729e-08, -0.47241300344467163))
p60 = Vector((0.1815710812807083, 2.914092434025406e-08, -0.36130189895629883))
p61 = Vector((0.1815710812807083, 1.9427282893502706e-08, -0.13907968997955322))
p62 = Vector((0.1815710812807083, 1.457046217012703e-08, -0.02796858549118042))
p63 = Vector((0.1815710812807083, 4.856819835197257e-09, 0.19425362348556519))
p64 = Vector((0.1815710812807083, -8.881784197001252e-16, 0.305364727973938))
p65 = Vector((0.06017318367958069, 5.342502973348928e-08, -0.9168574810028076))
p66 = Vector((-0.06122470647096634, 5.342503328620296e-08, -0.9168574810028076))
p67 = Vector((0.06017318367958069, 3.885456578700541e-08, -0.5835241675376892))
p68 = Vector((-0.06122470647096634, 3.885456578700541e-08, -0.583524227142334))
p69 = Vector((0.06017318367958069, 2.4284103616878383e-08, -0.2501908242702484))
p70 = Vector(
    (-0.06122470647096634, 2.4284105393235222e-08, -0.2501908540725708))
p71 = Vector((0.06017318367958069, 9.713641446751353e-09, 0.08314249664545059))
p72 = Vector((-0.06122470647096634, 9.713642334929773e-09, 0.0831424742937088))
p73 = Vector((0.06017318367958069, -4.8568211674648865e-09, 0.4164758324623108))
p74 = Vector((-0.06122470647096634, -4.856820723375677e-09, 0.4164758324623108))
p75 = Vector((-0.06122470647096634, 4.8568211674648865e-09, 0.1942535936832428))
p76 = Vector((-0.06122470647096634, 4.440892098500626e-16, 0.305364727973938))
p77 = Vector((0.06017318367958069, 4.856820723375677e-09, 0.19425362348556519))
p78 = Vector((0.06017318367958069, 0.0, 0.305364727973938))
p79 = Vector((-0.06122470647096634, 1.9427284669859546e-08, -0.139079749584198))
p80 = Vector((-0.06122470647096634, 1.457046394648387e-08, -0.0279686376452446))
p81 = Vector((0.06017318367958069, 1.9427282893502706e-08, -0.1390797197818756))
p82 = Vector(
    (0.06017318367958069, 1.457046217012703e-08, -0.027968615293502808))
p83 = Vector(
    (-0.06122470647096634, 3.3997746839986576e-08, -0.4724130928516388))
p84 = Vector((-0.06122470647096634, 2.91409261166109e-08, -0.3613019585609436))
p85 = Vector((0.06017318367958069, 3.39977432872729e-08, -0.4724130630493164))
p86 = Vector((0.06017318367958069, 2.914092434025406e-08, -0.3613019585609436))
p87 = Vector(
    (-0.06122470647096634, 4.8568210786470445e-08, -0.8057463765144348))
p88 = Vector((-0.06122470647096634, 4.371138828673793e-08, -0.694635272026062))
p89 = Vector((0.06017318367958069, 4.8568207233756766e-08, -0.8057463765144348))
p90 = Vector((0.06017318367958069, 4.371138828673793e-08, -0.694635272026062))
p91 = Vector((-0.06122470274567604, 6.313867118024064e-08, -1.1390796899795532))
p92 = Vector((-0.06122470647096634, 5.82818522332218e-08, -1.0279686450958252))
p93 = Vector((0.06017318740487099, 6.313867118024064e-08, -1.1390796899795532))
p94 = Vector((0.06017318367958069, 5.828184868050812e-08, -1.0279686450958252))
p95 = Vector((-0.0005257576704025269, -
              1.9427282893502706e-08, 1.1824181079864502))
p96 = Vector((0.2733113467693329, -1.9427282893502706e-08, 0.8672559857368469))
p97 = Vector(
    (-0.27278560400009155, -1.9427282893502706e-08, 0.8672559261322021))
p98 = Vector(
    (-0.06122470647096634, -1.9427282893502706e-08, 0.8672559857368469))
p99 = Vector(
    (-0.06122470647096634, -1.9427282893502706e-08, 0.9847028255462646))
p100 = Vector(
    (0.06017318367958069, -1.9427282893502706e-08, 0.8672559857368469))
p101 = Vector(
    (0.06017318367958069, -1.9427282893502706e-08, 0.9847028255462646))
p102 = Vector(
    (-0.06122470647096634, -9.713641446751353e-09, 0.5275869369506836))
p103 = Vector(
    (-0.06122470647096634, -1.457046217012703e-08, 0.6386980414390564))
p104 = Vector(
    (0.06017318367958069, -9.713641446751353e-09, 0.5275869369506836))
p105 = Vector(
    (0.06017318367958069, -1.457046217012703e-08, 0.6386980414390564))

arrowup_shape_verts = (
    p24, p25, p105,
    p32, p27, p101,
    p2, p30, p36,
    p5, p32, p42,
    p4, p28, p34,
    p56, p65, p94,
    p58, p67, p90,
    p60, p69, p86,
    p62, p71, p82,
    p64, p73, p78,
    p76, p9, p47,
    p78, p74, p76,
    p72, p48, p10,
    p75, p47, p48,
    p71, p75, p72,
    p77, p76, p75,
    p17, p77, p71,
    p63, p78, p77,
    p80, p10, p49,
    p82, p72, p80,
    p70, p50, p11,
    p79, p49, p50,
    p69, p79, p70,
    p81, p80, p79,
    p16, p81, p69, p61, p82, p81, p84, p11, p51, p86, p70, p84,    p68,    p52,    p12,    p83,    p51,    p52,    p67,    p83,    p68,    p85,    p84,    p83,    p15,    p85,    p67,    p59,
    p86, p85, p88, p12, p53, p90, p68,  p88, p66, p54, p13, p87, p53, p54, p65, p87, p66, p89, p88, p87, p14, p89, p65, p57, p90, p89, p92, p13, p19, p94,    p66, p92, p21, p20, p0,  p91, p19,
    p20,
    p22,
    p91,
    p21,
    p93,
    p92,
    p91,
    p1,
    p93,
    p22,
    p55,
    p94,
    p93,
    p33,
    p44,
    p8,
    p34,
    p95,
    p33,
    p33,
    p95,
    p44,
    p95,
    p43,
    p44,
    p34,
    p28,
    p95,
    p28,
    p27,
    p95,
    p95,
    p27,
    p43,
    p27,
    p5,
    p43,
    p41,
    p40,
    p7,
    p42,
    p96,
    p41,
    p41,
    p96,
    p40,
    p96,
    p39,
    p40,
    p42,
    p32,
    p96,
    p32,
    p31,
    p96,
    p96,
    p31,
    p39,
    p31,
    p3,
    p39,
    p35,
    p38,
    p6,
    p36,
    p97,
    p35,
    p35,
    p97,
    p38,
    p97,
    p37,
    p38,
    p36,
    p30,
    p97,
    p30,
    p29,
    p97,
    p97,
    p29,
    p37,
    p29,
    p4,
    p37,
    p99,
    p4,
    p29,
    p101,
    p28,
    p99,
    p26,
    p30,
    p2,
    p98,
    p29,
    p30,
    p25,
    p98,
    p26,
    p100,
    p99,
    p98,
    p3,
    p100,
    p25,
    p31,
    p101,
    p100,
    p103,
    p2,
    p45,
    p105,
    p26,
    p103,
    p74,
    p46,
    p9,
    p102,
    p45,
    p46,
    p73,
    p102,
    p74,
    p104,
    p103,
    p102,
    p18,
    p104,
    p73,
    p23,
    p105,
    p104,
    p24,
    p3,
    p25,
    p32,
    p5,
    p27,
    p56,
    p14,
    p65,
    p58,
    p15,
    p67,
    p60,
    p16,
    p69,
    p62,
    p17,
    p71,
    p64,
    p18,
    p73,
    p76,
    p74,
    p9,
    p78,
    p73,
    p74,
    p72,
    p75,
    p48,
    p75,
    p76,
    p47,
    p71,
    p77,
    p75,
    p77,
    p78,
    p76,
    p17,
    p63,
    p77,
    p63,
    p64,
    p78,
    p80,
    p72,
    p10,
    p82,
    p71,
    p72,
    p70,
    p79,
    p50,
    p79,
    p80,
    p49,
    p69,
    p81,
    p79,
    p81,
    p82,
    p80,
    p16,
    p61,
    p81,
    p61,
    p62,
    p82,
    p84,
    p70,
    p11,
    p86,
    p69,
    p70,
    p68,
    p83,
    p52,
    p83,
    p84,
    p51,
    p67,
    p85,
    p83,
    p85,
    p86,
    p84,
    p15,
    p59,
    p85,
    p59,
    p60,
    p86,
    p88,
    p68,
    p12,
    p90,
    p67,
    p68,
    p66,
    p87,
    p54,
    p87,
    p88,
    p53,
    p65,
    p89,
    p87,
    p89,
    p90,
    p88,
    p14,
    p57,
    p89,
    p57,
    p58,
    p90,
    p92,
    p66,
    p13,
    p94,
    p65,
    p66,
    p21,
    p91,
    p20,
    p91,
    p92,
    p19,
    p22,
    p93,
    p91,
    p93,
    p94,
    p92,
    p1,
    p55,
    p93,
    p55,
    p56,
    p94,
    p99,
    p28,
    p4,
    p101,
    p27,
    p28,
    p26,
    p98,
    p30,
    p98,
    p99,
    p29,
    p25,
    p100,
    p98,
    p100,
    p101,
    p99,
    p3,
    p31,
    p100,
    p31,
    p32,
    p101,
    p103,
    p26,
    p2,
    p105,
    p25,
    p26,
    p74,
    p102,
    p46,
    p102,
    p103,
    p45,
    p73,
    p104,
    p102,
    p104,
    p105,
    p103,
    p18,
    p23,
    p104,
    p23,
    p24,
    p105)


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


linecount_shape_verts = (
    linecount0, linecount1, linecount2,
    linecount1, linecount2, linecount3,
    linecount6, linecount4, linecount5,
    linecount6, linecount7, linecount5,
    linecount9, linecount8, linecount10,
    linecount9, linecount11, linecount10,
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

linedistance0 = Vector((-0.47405412793159485, 0.0, -0.27930986881256104))
linedistance1 = Vector((0.47405412793159485, 0.0, -0.27930986881256104))
linedistance2 = Vector((-0.47405412793159485, 0.0, 0.27930986881256104))
linedistance3 = Vector((0.47405412793159485, 0.0, 0.27930986881256104))
linedistance4 = Vector(
    (-0.47405412793159485, 0.30000001192092896, -0.27930986881256104))
linedistance5 = Vector(
    (0.47405412793159485, 0.30000001192092896, -0.27930986881256104))
linedistance6 = Vector(
    (-0.47405412793159485, 0.30000001192092896, 0.27930986881256104))
linedistance7 = Vector(
    (0.47405412793159485, 0.30000001192092896, 0.27930986881256104))
linedistance8 = Vector(
    (0.07070715725421906, 0.3000657558441162, 0.44158151745796204))
linedistance9 = Vector(
    (-0.19720323383808136, 0.3000657558441162, 0.44158151745796204))
linedistance10 = Vector(
    (0.07070715725421906, 0.0002984553575515747, 0.44158151745796204))
linedistance11 = Vector(
    (-0.19720323383808136, 0.0002984553575515747, 0.44158151745796204))
linedistance12 = Vector(
    (0.07070715725421906, 0.3000657558441162, 0.33240607380867004))
linedistance13 = Vector(
    (-0.19720323383808136, 0.3000657558441162, 0.33240607380867004))
linedistance14 = Vector(
    (0.07070715725421906, 0.0002984553575515747, 0.33240607380867004))
linedistance15 = Vector(
    (-0.19720323383808136, 0.0002984553575515747, 0.33240607380867004))

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


thickness_shape_verts = (
    thickness1, thickness5, thickness6,
    thickness1, thickness5, thickness3,
    thickness0, thickness2, thickness11,
    thickness4, thickness2, thickness11,
    thickness16, thickness17, thickness14,
    thickness16, thickness15, thickness14,
    thickness13, thickness18, thickness9,
    thickness19, thickness18, thickness9,
    thickness8, thickness10, thickness12,
    thickness8, thickness7, thickness12,
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


cylinder0 = Vector((0.0, 1.0, -0.5))
cylinder1 = Vector((0.0, 1.0, 0.5))
cylinder2 = Vector((0.3826834559440613, 0.9238795042037964, -0.5))
cylinder3 = Vector((0.3826834559440613, 0.9238795042037964, 0.5))
cylinder4 = Vector((0.7071067690849304, 0.7071067690849304, -0.5))
cylinder5 = Vector((0.7071067690849304, 0.7071067690849304, 0.5))
cylinder6 = Vector((0.9238795042037964, 0.3826834261417389, -0.5))
cylinder7 = Vector((0.9238795042037964, 0.3826834261417389, 0.5))
cylinder8 = Vector((1.0, -4.371138828673793e-08, -0.5))
cylinder9 = Vector((1.0, -4.371138828673793e-08, 0.5))
cylinder10 = Vector((0.9238795042037964, -0.38268351554870605, -0.5))
cylinder11 = Vector((0.9238795042037964, -0.38268351554870605, 0.5))
cylinder12 = Vector((0.7071067690849304, -0.7071067690849304, -0.5))
cylinder13 = Vector((0.7071067690849304, -0.7071067690849304, 0.5))
cylinder14 = Vector((0.38268348574638367, -0.9238795042037964, -0.5))
cylinder15 = Vector((0.38268348574638367, -0.9238795042037964, 0.5))
cylinder16 = Vector((1.5099580252808664e-07, -1.0, -0.5))
cylinder17 = Vector((1.5099580252808664e-07, -1.0, 0.5))
cylinder18 = Vector((-0.3826832175254822, -0.9238796234130859, -0.5))
cylinder19 = Vector((-0.3826832175254822, -0.9238796234130859, 0.5))
cylinder20 = Vector((-0.7071065902709961, -0.7071070075035095, -0.5))
cylinder21 = Vector((-0.7071065902709961, -0.7071070075035095, 0.5))
cylinder22 = Vector((-0.9238795042037964, -0.38268357515335083, -0.5))
cylinder23 = Vector((-0.9238795042037964, -0.38268357515335083, 0.5))
cylinder24 = Vector((-1.0, 1.1924880638503055e-08, -0.5))
cylinder25 = Vector((-1.0, 1.1924880638503055e-08, 0.5))
cylinder26 = Vector((-0.9238794445991516, 0.3826836049556732, -0.5))
cylinder27 = Vector((-0.9238794445991516, 0.3826836049556732, 0.5))
cylinder28 = Vector((-0.7071065306663513, 0.7071070075035095, -0.5))
cylinder29 = Vector((-0.7071065306663513, 0.7071070075035095, 0.5))
cylinder30 = Vector((-0.3826829791069031, 0.9238797426223755, -0.5))
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
