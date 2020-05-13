import bpy

'''UI -Elements''' 

class PP_PT_PuzzlePrintMenu(bpy.types.Panel):
    bl_space_type="VIEW_3D"
    bl_region_type="UI"
    bl_label="New Coupling"
    bl_category="PuzzleUrPrint"
    
    
    
    #schreibe auf den Bildschirm
    def draw(self, context):
        

        data = bpy.data 
        
        layout = self.layout 
        
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        flow = layout.grid_flow(row_major=True, columns=0, even_columns=False, even_rows=False, align=True)
        col = flow.column()
        row = layout.row()
        
       
            
        if "PuzzleUrPrint" in data.collections: 
            PUrP = context.scene.PUrP
            try:
                col.template_ID(PUrP, "CenterObj", filter='AVAILABLE')
            except:
                pass    
                    
            subcol = col.column()
            subcol.label(text="Coupling Mode")
            subcol.prop(PUrP, "SingleCouplingModes", expand=True)
            if context.scene.PUrP.SingleCouplingModes != '4':
                subcol.prop(PUrP, "SingleCouplingTypes", text = 'Coupling Type')
            else:
                subcol.prop(PUrP, "PlanarCouplingTypes", text = 'Coupling Type')

            subcol.operator("add.coup", icon="MOD_OCEAN") ### zeige button an
            
            

            
            subcol.label(text="AddingCouplings")
            
            if PUrP.SingleCouplingTypes == "2" or PUrP.SingleCouplingTypes == "3":
                subcol.prop(context.scene.PUrP, "CylVert", text = 'Vertices')
            
            subcol.prop(PUrP, "GlobalScale", text = 'Globalscalefaktor')
            subcol.prop(PUrP, "CoupSize", text = 'Coupling Size')    
            subcol.prop(PUrP, "zScale", text = 'z-Scale')
            subcol.prop(PUrP, "Oversize", text = 'Oversize')
            subcol.prop(PUrP, "CutThickness", text = 'Cut Thickness')    
            subcol.prop(PUrP, "BevelOffset", text = 'Bevel Offset')
            subcol.prop(PUrP, "BevelSegments", text = 'Bevel Segments')

            if context.scene.PUrP.SingleCouplingModes == '4':
                subcol.prop(PUrP, "LineLength", text = 'LineLength')
                subcol.prop(PUrP, "LineCount", text = 'Linecount')
                subcol.prop(PUrP, "LineDistance", text = 'Linedistance')
                subcol.prop(PUrP, "OffsetRight", text = 'Right Offset')
                subcol.prop(PUrP, "OffsetLeft", text = 'Left Offset')
                subcol.prop(PUrP, "StopperBool", text = 'Stopper')
                if PUrP.StopperBool:
                    subcol.prop(PUrP, "StopperHeight", text = 'Stopper Height')

            subcol.operator("object.exchangecoup", text="Apply New Settings")
            subcol = col.column()
            subcol.operator("rem.coup", icon="MOD_OCEAN") ### zeige button an
            subcol.operator("apl.coup", icon="MOD_OCEAN") ### zeige button an
            subcol.operator("apl.allcoup", text='Apply All', icon="MOD_OCEAN") ### zeige button an

            
            
            
            

            for ob in context.selected_objects:
                if "Connector" in context.object.name: 
                    subcol.prop(context.object, "rotation_euler", text = "Rotation")    

        else: 
            col.operator("pup.init", icon="MOD_OCEAN")        


'''
class PP_PT_PuzzlePrintActive(bpy.types.Panel):
    bl_space_type="VIEW_3D"
    bl_region_type="UI"
    bl_label="Active Coupling"
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
        

        col.operator("pup.modup", text = 'Move Modifiers Up')
        col.operator("pup.moddown", text = 'Move Modifiers Down')

'''