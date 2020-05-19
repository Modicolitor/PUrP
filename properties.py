import bpy 
from bpy.types import Scene, Image, Object


class PUrPropertyGroup(bpy.types.PropertyGroup):
    CenterObj = bpy.props.PointerProperty(name="Object", type=Object)
    
    PUrP_name = bpy.props.StringProperty(name="PUrPname", default="PUrP_")
    CutThickness = bpy.props.FloatProperty(name="Size", default = 0.04)
    CoupSize = bpy.props.FloatProperty(name="Size", default = 1.0)
    Oversize = bpy.props.FloatProperty(name="DynamicOversize", default = 0.04)
    zScale = bpy.props.FloatProperty(name="zScale", default = 1.0)
    OffsetLeft = bpy.props.FloatProperty(name="OffsetLeft", default = 1.0)
    OffsetRight = bpy.props.FloatProperty(name="OffsetRight", default = 1.0)
    GlobalScale = bpy.props.FloatProperty(name="Globalscale ", default = 1.0)
    LineDistance = bpy.props.FloatProperty(name="Linedistance", default = 5.0)
    LineCount = bpy.props.IntProperty(name="Linecount", default = 1)
    LineLength = bpy.props.IntProperty(name="Linelength", default = 5)
    BevelSegments = bpy.props.IntProperty(name="Bevelsegements", default = 1)
    BevelOffset = bpy.props.FloatProperty(name="Beveloffset", default = 0.0)
    StopperHeight = bpy.props.FloatProperty(name="Beveloffset", default = 0.2)
    StopperBool = bpy.props.BoolProperty(name="Beveloffset", default = False)

    CylVert = bpy.props.IntProperty(
        name='Vertexcount',
        description='Set the resolution of the cylic objects',
        default=16,
     )


    SingleCouplingTypes = bpy.props.EnumProperty(
        name='',  #SingleCoupltypes
        description='List of forms avaiable in single connector mode',
        default='1',
        items=[ ('1','Cube',''),
                ('2','Cylinder', ''),
                ('3','Cone',''),
                ]
        )
    
    PlanarCouplingTypes = bpy.props.EnumProperty(
        name='',  #PlanarCoupltypes
        description='List of forms avaiable in planar connector mode',
        default='1',
        items=[ ('1','Cubic',' '),
                ('2','Dovetail', ''),
                ('3','Puzzle',''),
                ]
        )
    
    SingleCouplingModes = bpy.props.EnumProperty(
        name='SingleCouplModes',
        description='List of forms avaiable in single connector mode',
        items=[ ('1','Stick',''),
                ('2','Male-Female', ''),
                ('3','FlatCut',''),
                ('4','Planar',''),
                ]
        )