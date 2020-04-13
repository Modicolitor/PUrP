import bpy 
from bpy.types import Scene, Image, Object


class PUrPropertyGroup(bpy.types.PropertyGroup):
    CenterObj = bpy.props.PointerProperty(name="Object", type=Object)
    PUrP_name = bpy.props.StringProperty(name="My Int")




