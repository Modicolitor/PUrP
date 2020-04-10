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
        #row.template_ID(context.view_layer.objects, "active", filter='AVAILABLE')
        col.template_ID(context.scene, "PUrP_CenterObj", filter='AVAILABLE')
        
        subcol = col.column()
        subcol.operator("add.coup", icon="MOD_OCEAN") ### zeige button an
        subcol.operator("apl.coup", icon="MOD_OCEAN") ### zeige button an
        subcol.operator("rem.coup", icon="MOD_OCEAN") ### zeige button an
        if "Connector" in context.object.name: 
            subcol.prop(context.object.rotation_euler, 'x', text = "x-rotation")    
       

        
   # col = layout.column(align=True)  ### col befehl packt die werte in einen kasten
#    row = layout.row(align=True)
    
    