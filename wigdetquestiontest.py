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



class BE_GizmoGroup(GizmoGroup):
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

        #'''
        ####Center Version start 
        centerR = self.gizmos.new(CenterShapeWidget.bl_idname)
        props = centerR.target_set_operator("object.ot_scalemini")
        centerR.matrix_basis = ob.matrix_world.normalized()
        centerR.use_draw_offset_scale = True 
        centerR.matrix_offset[0][3] = -2
        centerR.matrix_offset[1][3] = 2
        centerR.matrix_offset[2][3] = 2
        
        #centerR.matrix_basis[0][3] -= 2  ## moving the centered Gizmoshape 
        #centerR.matrix_basis[1][3] += 2
        #centerR.matrix_basis[2][3] += 2
        #centerR.color = 0.05, 0.2, 0.8
        self.WidCR = centerR 

        centerL = self.gizmos.new(CenterShapeWidget.bl_idname)
        props = centerL.target_set_operator("object.ot_scalemini")
        
        centerL.use_draw_offset_scale = True 
        centerL.matrix_basis = ob.matrix_world.normalized()
        centerL.matrix_offset[0][3] = -2  ## moving the centered Gizmoshape 
        centerL.matrix_offset[1][3] = -2
        centerL.matrix_offset[2][3] = 2
        centerL.color = 0.05, 0.2, 0.8
        self.WidCL = centerL 

        '''
        ####cornered start 
        cornerR = self.gizmos.new(CornerRShapeWidget.bl_idname)
        props = cornerR.target_set_operator("object.ot_scalemini")
        cornerR.matrix_basis = ob.matrix_world.normalized()
        cornerR.color = 0.05, 0.2, 0.8
        self.CornR = cornerR 

        cornerL = self.gizmos.new(CornerLShapeWidget.bl_idname)
        props = cornerL.target_set_operator("object.ot_scalemini")
        cornerL.matrix_basis = ob.matrix_world.normalized()
        cornerL.color = 0.05, 0.2, 0.8
        self.CornL = cornerL 
        ###cornered end 
        '''

    def refresh(self, context):
        ob = context.object
        #'''
        ###centered start
        centerR = self.WidCR 
        centerR.matrix_basis = ob.matrix_world.normalized()
        centerR.matrix_offset[0][3] = -2
        centerR.matrix_offset[1][3] = 2
        centerR.matrix_offset[2][3] = 2

        centerL = self.WidCL 
        centerL.matrix_basis = ob.matrix_world.normalized()
        centerL.matrix_offset[0][3] = -2
        centerL.matrix_offset[1][3] = -2
        centerL.matrix_offset[2][3] = 2
        ###centered end 
        '''
        #####cornered start 
        cornerL = self.CornL
        cornerL.matrix_basis = ob.matrix_world.normalized()
        cornerR = self.CornR
        cornerR.matrix_basis = ob.matrix_world.normalized()
        #####cornered end
        #'''  



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
cornerR2 = Vector((-2.87, 1.50, 1.0))
cornerR3 = Vector((-2.0, 2.0, 3.0))
cornerR_shape = (
    cornerR0,cornerR1,cornerR2,
    cornerR0,cornerR1,cornerR3,
    cornerR2,cornerR1,cornerR3,
    cornerR0,cornerR2,cornerR3,
)

######corner L
cornerL0 = Vector((-2.0, -1.0, 1.0))
cornerL1 = Vector((-1.13, -2.5, 1.0))
cornerL2 = Vector((-2.87, -2.5, 1.0))
cornerL3 = Vector((-2.0, -2.0, 3.0))

cornerL_shape = (
    cornerL0,cornerL1,cornerL2,
    cornerL0,cornerL1,cornerL3,
    cornerL2,cornerL1,cornerL3,
    cornerL0,cornerL2,cornerL3,
)

class CenterShapeWidget(Gizmo):
    bl_idname = "VIEW3D_GT_CENTERSHAPE"
    
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
    
class CornerLShapeWidget(Gizmo):
    bl_idname = "VIEW3D_GT_CORNERL"
    
    def draw(self, context):
        # self._update_offset_matrix()
        self.draw_custom_shape(self.custom_shape)

    def draw_select(self, context, select_id):
        # self._update_offset_matrix()
        self.draw_custom_shape(self.custom_shape, select_id=select_id)

    def setup(self):
        if not hasattr(self, "custom_shape"):
            self.custom_shape = self.new_custom_shape(
                'TRIS', cornerL_shape)

class CornerRShapeWidget(Gizmo):
    bl_idname = "VIEW3D_GT_CORNERR"
    
    def draw(self, context):
        # self._update_offset_matrix()
        self.draw_custom_shape(self.custom_shape)

    def draw_select(self, context, select_id):
        # self._update_offset_matrix()
        self.draw_custom_shape(self.custom_shape, select_id=select_id)

    def setup(self):
        if not hasattr(self, "custom_shape"):
            self.custom_shape = self.new_custom_shape(
                'TRIS', cornerR_shape)   

class BE_OT_scale(bpy.types.Operator):
    bl_idname = "object.ot_scalemini"
    bl_label = "BE_PP_scalemini"

    @classmethod
    def poll(cls, context):
        ob = context.object
        return ob !=None

    def execute(self, context):
        ob = context.object
        ob.scale.x = self.value
        return {'FINISHED'}

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':  # Apply
            self.delta = event.mouse_x - self.init_value
            self.value = self.init_position + self.delta / 1000
            self.execute(context)
        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            ob.scale.x = self.init_value 
            return {'CANCELLED'}
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        ob = context.object
        self.init_position = ob.scale.x
        self.init_value = event.mouse_x
        self.value = ob.scale.x
        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


classes = (
    BE_GizmoGroup,
    CenterShapeWidget,
    CornerLShapeWidget,
    CornerRShapeWidget,
    BE_OT_scale,
)

register, unregister = bpy.utils.register_classes_factory(classes)