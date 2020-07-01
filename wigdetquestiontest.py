bl_info = {  # für export als addon
    "name": "WidgetTester",
    "author": "Modicolitor",
    "version": (0, 1),
    "blender": (2, 83, 0),
    "location": "View3D > Tools",
    "description": "Test your widget shapes",
    "category": "Object"}

import bpy 
from bpy.types import (
    Gizmo,
    GizmoGroup,
)
from mathutils import Vector

#####centered 
centered0 = Vector((0.0, 1.0, -1.0))
centered1 = Vector((0.866, -0.50, -1.0))
centered2 = Vector((-0.866, -0.50, -1.0))
centered3 = Vector((0.0, 0.0, 1.0))

center_shape = (
    centered0,centered1,centered2,
    centered0,centered1,centered3,
    centered2,centered1,centered3,
    centered0,centered2,centered3,
)

#####corner R 
cornerR0 = Vector((-2.0, 3.0, 1.0))
cornerR1 = Vector((-1.13, 1.5, 1.0))
cornerR2 = Vector((-2.866, 1.50, 1.0))
cornerR3 = Vector((-2.0, 2.0, 3.0))
cornerR_shape = (
    cornerR0,cornerR1,cornerR2,
    cornerR0,cornerR1,cornerR3,
    cornerR2,cornerR1,cornerR3,
    cornerR0,cornerR2,cornerR3,
)

######corner L
cornerL0 = Vector((-2.0, 3.0, 1.0))
cornerL1 = Vector((-1.134, 1.5, 1.0))
cornerL2 = Vector((-2.866, 1.50, 1.0))
cornerL3 = Vector((-2.0, 2.0, 3.0))

cornerR_shape = (
    cornerL0,cornerL1,cornerL2,
    cornerL0,cornerL1,cornerL3,
    cornerL2,cornerL1,cornerL3,
    cornerL0,cornerL2,cornerL3,
)



class CenterShapeWidget(Gizmo):
    bl_idname = "VIEW3D_GT_Centershape"
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
                'TRIS', center_shape)

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


class PUrP_PlanarGizmo(GizmoGroup):
    bl_idname = "OBJECT_GGT_PLANARCONNECTOR"
    bl_label = "Positioning GizmoGroup"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT'}

    @classmethod
    def poll(cls, context):
        ob = context.object
        return ob != None
          

    def setup(self, context):
        ob = context.object

        print("setup Gizmo")
        ####Center Version start 
        centerR = self.gizmos.new(CenterShapeWidget.bl_idname)
        props = centerR.target_set_prop("offset", ob.scale, "x")
        centerR.matrix_basis = ob.matrix_world.normalized()
        centerR.matrix_basis[0][3] += 2

        #centerR.line_width = 3
        centerR.color = 0.05, 0.2, 0.8
        #centerR.alpha = 0.5
        #centerR.color_highlight = 0.03, 0.05, 1.0
        #centerR.alpha_highlight = 1.0
        self.WidCR = centerR 

    def refresh(self):
        ###center start
        centerR = self.WidCR 
        centerR.matrix_basis = ob.matrix_world.normalized()
        centerR.matrix_basis[0][3] += 2
        
        
        

classes = (
    PUrP_PlanarGizmo,
    CenterShapeWidget,
)

register, unregister = bpy.utils.register_classes_factory(classes)