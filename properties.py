import bpy 
from bpy.types import Scene, Image, Object


class PUrPropertyGroup(bpy.types.PropertyGroup):
    CenterObj = bpy.props.PointerProperty(name="Object", type=Object)
    PUrP_name = bpy.props.StringProperty(name="PUrPname", default="PUrP_")
    CutThickness = bpy.props.FloatProperty(name="Size", default = 0.1)
    CoupSize = bpy.props.FloatProperty(name="Size", default = 1.0)
    Oversize = bpy.props.FloatProperty(name="DynamicOversize", default = 1.0)
    zScale = bpy.props.FloatProperty(name="zScale", default = 1.0)
    CylVert = bpy.props.IntProperty(
        name='Vertexcount',
        description='Set the resolution of the cylic objects',
        default=32,
     )


    SingleCouplingTypes = bpy.props.EnumProperty(
        name='',  #SingleCoupltypes
        description='List of forms avaiable in single connector mode',
        default='1',
        items=[ ('0', '',''),
                ('1','Cube',''),
                ('2','Cylinder', ''),
                ('3','Cone',''),
                ]
        )
    SingleCouplingModes = bpy.props.EnumProperty(
        name='SingleCouplModes',
        description='List of forms avaiable in single connector mode',
        items=[ ('1','Stick',''),
                ('2','Male-Female', ''),
                ('3','FlatCut',''),
                ]
        )