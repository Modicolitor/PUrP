import bpy
from bpy.types import Scene, Image, Object


class PUrPropertyGroup(bpy.types.PropertyGroup):
    CenterObj = bpy.props.PointerProperty(name="Object", type=Object)

    PUrP_name = bpy.props.StringProperty(
        name="PUrPname", default="PUrP_")
    CutThickness = bpy.props.FloatProperty(
        name="Size", default=0.04, min=0.0)
    CoupSize = bpy.props.FloatProperty(
        name="Size", default=1.0, min=0.0)
    Oversize = bpy.props.FloatProperty(
        name="DynamicOversize", default=0.04)
    zScale = bpy.props.FloatProperty(
        name="zScale", default=1.0, min=0.0001)
    aRadius = bpy.props.FloatProperty(
        name="Radius 1", default=1.0, min=0.0)
    bRadius = bpy.props.FloatProperty(
        name="Radius 2", default=0.0, min=0.0)
    OffsetLeft = bpy.props.FloatProperty(
        name="OffsetLeft", default=1.0, min=0.0)
    OffsetRight = bpy.props.FloatProperty(
        name="OffsetRight", default=1.0, min=0.0)
    GlobalScale = bpy.props.FloatProperty(
        name="Globalscale ", default=1.0, min=0.0)
    LineDistance = bpy.props.FloatProperty(
        name="Linedistance", default=5.0, min=0.0)
    LineCount = bpy.props.IntProperty(
        name="Linecount", default=1, min=0)
    LineLength = bpy.props.IntProperty(
        name="Linelength", default=5, min=0)
    BevelSegments = bpy.props.IntProperty(
        name="Bevelsegements", default=1, min=0)
    BevelOffset = bpy.props.FloatProperty(
        name="Beveloffset", default=0.0, min=0.0)
    StopperHeight = bpy.props.FloatProperty(
        name="Beveloffset", default=0.2, min=0.0)
    StopperBool = bpy.props.BoolProperty(
        name="Beveloffset", default=False)
    BuildplateX = bpy.props.FloatProperty(
        name="Buildplate X-Dimensions", default=19, min=0.0)
    BuildplateY = bpy.props.FloatProperty(
        name="Buildplate Y-Dimensions", default=19, min=0.0)
    BuildplateZ = bpy.props.FloatProperty(
        name="Buildplate Z-Dimensions", default=19, min=0.0)
    CoupScale = bpy.props.FloatProperty(
        name="Connector Scale", default=1)
    PlanarCorScale = bpy.props.FloatProperty(
        name="PlanarKorrekturBG", default=1)

    CylVert = bpy.props.IntProperty(
        name='Vertexcount',
        description='Set the resolution of the cylic objects',
        default=16,
        min=0,
    )

    SingleCouplingTypes = bpy.props.EnumProperty(
        name='',  # SingleCoupltypes
        description='List of forms avaiable in single connector mode',
        default='1',
        items=[('1', 'Cube', ''),
               ('2', 'Cylinder', ''),
               ('3', 'Cone', ''),
               ]
    )

    PlanarCouplingTypes = bpy.props.EnumProperty(
        name='',  # PlanarCoupltypes
        description='List of forms avaiable in planar connector mode',
        default='1',
        items=[('1', 'Cubic', ' '),
               ('2', 'Dovetail', ''),
               ('3', 'Puzzle1', ''),
               ('4', 'Puzzle2', ''),
               ('5', 'Puzzle3', ''),
               ('6', 'Puzzle4', ''),
               ('7', 'Puzzle5', ''),
               ('8', 'Arrow1', ''),
               ('9', 'Arrow2', ''),
               ('10', 'Arrow3', ''),
               ('11', 'Pentagon', ''),
               ('12', 'Hexagon', ''),
               ('13', 'T-RoundedAll', ''),
               ('14', 'T-RoundedTop', ''),
               ('15', 'T-Straight', ''),
               ('16', 'Flat', ''),

               ]
    )

    SingleCouplingModes = bpy.props.EnumProperty(
        name='SingleCouplModes',
        description='List of forms avaiable in single connector mode',
        items=[('1', 'Stick', ''),
               ('2', 'Male-Female', ''),
               ('3', 'FlatCut', ''),
               ('4', 'Planar', ''),
               ]
    )
