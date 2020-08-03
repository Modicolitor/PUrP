import bpy

'''UI -Elements'''


class PP_PT_PuzzlePrintMenu(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "New Coupling"
    bl_category = "PuzzleUrPrint"

    # schreibe auf den Bildschirm

    def draw(self, context):

        data = bpy.data

        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        flow = layout.grid_flow(row_major=True, columns=0,
                                even_columns=False, even_rows=False, align=True)
        col = flow.column()
        row = layout.row()

        if "PuzzleUrPrint" in data.collections:
            PUrP = context.scene.PUrP
            try:
                col.template_ID(PUrP, "CenterObj", filter='AVAILABLE')
            except:
                pass

            subcol = col.column()
            #subcol.label(text="Coupling Mode")
            # subcol.label(text="AddingCouplings")

            subcol.operator("add.coup", text="Add Coupling",
                            icon="PLUS")  # zeige button an
            subcol.label(text="Adjust")
            subcol.operator("object.exchangecoup",
                            text="Exchange", icon="FILE_REFRESH")
            subcol.operator("object.activecoupdefault",
                            text='Active to Settings', icon="EXPORT")  # zeige button an

            subcol.prop(PUrP, "SingleCouplingModes", expand=True)
            if context.scene.PUrP.SingleCouplingModes != '4':
                subcol.prop(PUrP, "SingleCouplingTypes", text='Coupling Type')
            else:
                subcol.prop(PUrP, "PlanarCouplingTypes", text='Coupling Type')
            subcol.prop(PUrP, "GlobalScale", text='Global Scale')
            subcol.prop(PUrP, "CoupScale", text='Connector Scale')

            if PUrP.SingleCouplingTypes == "2" or PUrP.SingleCouplingTypes == "3":  # cylinder cone
                subcol.prop(context.scene.PUrP, "CylVert", text='Vertices')
                subcol.prop(context.scene.PUrP, "aRadius", text='Radius')
                #subcol.prop(PUrP, "aRadius", text='Radius 1')
                if PUrP.SingleCouplingTypes == "3":
                    subcol.prop(PUrP, "bRadius", text='Radius Top')

            # for stick, mf, planecut
            if context.scene.PUrP.SingleCouplingModes == '1' or context.scene.PUrP.SingleCouplingModes == '2' or context.scene.PUrP.SingleCouplingModes == '3':

                subcol.prop(PUrP, "Oversize", text='Oversize')
                subcol.prop(PUrP, "CoupSize", text='Inlay Size')
                subcol.prop(PUrP, "zScale", text='z-Scale')
                subcol.prop(PUrP, "CutThickness", text='Cut Thickness')
                subcol.prop(PUrP, "BevelOffset", text='Bevel Offset')
                subcol.prop(PUrP, "BevelSegments", text='Bevel Segments')

            if context.scene.PUrP.SingleCouplingModes == '4':
                subcol.prop(PUrP, "Oversize", text='Oversize')
                subcol.prop(PUrP, "CoupSize", text='Coup Scale')
                subcol.prop(PUrP, "zScale", text='z-Scale')
                subcol.prop(PUrP, "LineLength", text='LineLength')
                subcol.prop(PUrP, "LineCount", text='Linecount')
                subcol.prop(PUrP, "LineDistance", text='Linedistance')
                subcol.prop(PUrP, "OffsetRight", text='Right Offset')
                subcol.prop(PUrP, "OffsetLeft", text='Left Offset')

                subcol = col.column()
                subcol.prop(PUrP, "StopperBool", text='Stopper')
                if PUrP.PlanarCouplingTypes == "16":
                    subcol.enabled = False
                else:
                    subcol.enabled = True
                if PUrP.StopperBool:
                    subcol.prop(PUrP, "StopperHeight", text='Stopper Height')

            subcol = col.column()
            subcol.operator("rem.coup", text="Delete Coupling",
                            icon="CANCEL")  # zeige button an
            subcol.operator("apl.coup", text="Apply Coupling",
                            icon="MOD_DYNAMICPAINT")  # zeige button an
            subcol.operator("apl.allcoup", text='Apply All',
                            icon="EXPERIMENTAL")  # zeige button an
            subcol.prop(PUrP, "KeepCoup", text="Keep Connector")
            subcol.label(text="Special Apply Methods")
            subcol.operator("object.applyplanarmultiobj", text='Planar To Multiple Objects',
                            icon="PARTICLE_POINT")  # zeige button an
            #subcol.operator("object.applymultipleplanartoobject", text='Multiple Planar to Object',
            #                icon="MOD_INSTANCE")
            subcol.operator("object.applysingletoobjects", text='Single Connector To Multiple Objects',
                            icon="MOD_INSTANCE")
            subcol.prop(PUrP, "IgnoreMainCut", text = "Ignore Main Cut")

            
            subcol.label(text="Coupling Order")
            subcol.operator("pup.couplingorder",
                            text='Toggle Order', icon="LINENUMBERS_ON")
            subcol.operator("pup.modup", text='Up in Order ', icon="TRIA_UP")
            subcol.operator(
                "pup.moddown", text='Down in Couplingorder', icon="TRIA_DOWN")
            subcol.operator("object.remapcoups",
                        text='Remap To Active', icon="FILE_REFRESH")
            subcol.label(text="Modifier Visibility")
            subcol.operator("object.togglecoupvisibility",
                            text='Toggle Modifier Visibility', icon="HIDE_OFF")
            subcol.prop(PUrP, "InlayToggleBool", text='Toggle Inlay')
            subcol.operator("object.pp_ot_overlapcheck",
                            text='Check Overlap', icon="HIDE_OFF")

            subcol.label(text="Modifier Visibility")
            subcol.prop(PUrP, "BuildplateX", text='Buildplate X')
            subcol.prop(PUrP, "BuildplateY", text='Buildplate Y')
            subcol.prop(PUrP, "BuildplateZ", text='Buildplate Z')
            subcol.operator("object.makebuildvolume",
                            text='Generate Buildvolume', icon="MESH_CUBE")

        else:
            col.operator("pup.init", icon="SHADERFX")


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
