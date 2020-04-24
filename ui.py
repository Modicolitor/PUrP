import bpy

'''UI -Elements''' 

class PP_PT_PuzzlePrintMenu(bpy.types.Panel):
    bl_space_type="VIEW_3D"
    bl_region_type="UI"
    bl_label="PuzzleUrPrint"
    bl_category="PuzzleUrPrint"
    
    
    
    #schreibe auf den Bildschirm
    def draw(self, context):
        data = bpy.data 
        
        layout = self.layout ;
        
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        flow = layout.grid_flow(row_major=True, columns=0, even_columns=False, even_rows=False, align=True)
        col = flow.column()
        row = layout.row()
        
       
            
        if "PuzzleUrPrint" in data.collections: 
            try:
                col.template_ID(context.scene.PUrP, "CenterObj", filter='AVAILABLE')
            except:
                pass    
                    
            subcol = col.column()
            subcol.label(text="Coupling Mode")
            subcol.prop(context.scene.PUrP, "SingleCouplingModes", expand=True)
            if context.scene.PUrP.SingleCouplingModes != '4':
                subcol.prop(context.scene.PUrP, "SingleCouplingTypes", text = 'Coupling Type')
            else:
                subcol.prop(context.scene.PUrP, "PlanarCouplingTypes", text = 'Coupling Type')

            props = subcol.operator("add.coup", icon="MOD_OCEAN") ### zeige button an
            props.PrimTypes = context.scene.PUrP.SingleCouplingTypes
            props.CylVert = context.scene.PUrP.CylVert

            PUrP = context.scene.PUrP
            subcol.label(text="AddingCouplings")
            subcol.prop(context.scene.PUrP, "CutThickness", text = 'Cut Thickness')    
            if PUrP.SingleCouplingTypes == "2" or PUrP.SingleCouplingTypes == "3":
                subcol.prop(context.scene.PUrP, "CylVert", text = 'Vertices')
            
            subcol.prop(context.scene.PUrP, "GlobalScale", text = 'Globalscalefaktor')
            subcol.prop(context.scene.PUrP, "CoupSize", text = 'Size')    
            subcol.prop(context.scene.PUrP, "zScale", text = 'z-scale')
            subcol.prop(context.scene.PUrP, "Oversize", text = 'oversize')
            if context.scene.PUrP.SingleCouplingModes == '4':
                subcol.prop(context.scene.PUrP, "LineLength", text = 'LineLength')
                subcol.prop(context.scene.PUrP, "LineCount", text = 'Linecount')
                subcol.prop(context.scene.PUrP, "LineDistance", text = 'Linedistance')

            subcol.operator("object.exchangecoup", text="Apply New Settings")
            subcol = col.column()
            subcol.operator("rem.coup", icon="MOD_OCEAN") ### zeige button an
            subcol.operator("apl.coup", icon="MOD_OCEAN") ### zeige button an
            
            subcol = col.column()
            subcol.label(text ='Test Button für Appends')
            subcol.operator("object.appendfromfile")
            
            

            for ob in context.selected_objects:
                if "Connector" in context.object.name: 
                    subcol.prop(context.object, "rotation_euler", text = "Rotation")    

        else: 
            col.operator("pup.init", icon="MOD_OCEAN")        

from bpy.types import (
    GizmoGroup,
)




class PUrP_RotationGizmo(GizmoGroup):
    bl_idname = "OBJECT_GGT_test_camera"
    bl_label = "Object Camera Test Widget"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT'}

    @classmethod
    def poll(cls, context):
        ob = context.object
        return (ob and ob.type == 'MESH' and "SingleConnector" in context.view_layer.objects.active.name)

    def setup(self, context):
        # Run an operator using the dial gizmo
        ob = context.object
        mpr = self.gizmos.new("GIZMO_GT_dial_3d")
        props = mpr.target_set_operator("object.oversize")
        #props.constraint_axis = True, True, True
        #props.orient_type = 'LOCAL'
        #props.release_confirm = True

        mpr.matrix_basis = ob.matrix_world.normalized()
        mpr.line_width = 3

        mpr.color = 0.8, 0.2, 0.8
        mpr.alpha = 0.5

        mpr.color_highlight = 1.0, 0.5, 1.0
        mpr.alpha_highlight = 1.0

        self.roll_widget = mpr

    def refresh(self, context):
        ob = context.object
        mpr = self.roll_widget
        mpr.matrix_basis = ob.matrix_world.normalized()     
    