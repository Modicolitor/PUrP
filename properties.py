import bpy 
from bpy.types import Scene, Image, Object


class PUrPropertyGroup(bpy.types.PropertyGroup):
    CenterObj = bpy.props.PointerProperty(name="Object", type=Object)
    PUrP_name = bpy.props.StringProperty(name="My Int")
    Oversize = bpy.props.FloatProperty(name="DynamicOversize", default = 1.0)
    SingleCouplingTypes = bpy.props.EnumProperty(
        name='',  #SingleCoupltypes
        description='List of forms avaiable in single connector mode',
        items=[ ('1','Cube',''),
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