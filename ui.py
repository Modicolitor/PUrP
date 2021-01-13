import bpy
from .bun import is_coup, is_planar, is_single

'''UI -Elements'''


class PP_PT_PuzzlePrintAddMenu(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Add, Exchange, Apply"
    bl_category = "PuzzleUrPrint"

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

            subcol.operator("add.coup", text="Add Connector",
                            icon="PLUS")  # zeige button an
            subcol.operator("rem.coup", text="Delete Connector",
                            icon="CANCEL")  # zeige button an
            subcol.label(text="Adjust")
            subcol.operator("object.exchangecoup",
                            text="Exchange", icon="FILE_REFRESH")
            subcol.operator("object.activecoupdefault",
                            text='Active to Settings', icon="EXPORT")  # zeige button an

            subcol.prop(PUrP, "SingleCouplingModes",
                        expand=True, text='Connector Modes')
            if context.scene.PUrP.SingleCouplingModes != '4':
                subcol.prop(PUrP, "SingleMainTypes", text='Maincut Type')
                subcol.prop(PUrP, "SingleCouplingTypes", text='Inlay Type')

            else:
                subcol.prop(PUrP, "PlanarCouplingTypes", text='Connector Type')
            if context.scene.PUrP.ExactOptBool:
                subcol.prop(PUrP, "BoolModSettings", text='Solver')
            subcol.prop(PUrP, "GlobalScale", text='Global Scale')
            subcol.prop(PUrP, "CoupScale", text='Connector Scale')

            # for stick, mf, planecut
            if context.scene.PUrP.SingleCouplingModes == '1' or context.scene.PUrP.SingleCouplingModes == '2' or context.scene.PUrP.SingleCouplingModes == '3':
                subcol.prop(PUrP, "CoupSize", text='Inlay Size')
                subcol.prop(PUrP, "zScale", text='z-Scale')
                subcol.prop(PUrP, "Oversize", text='Oversize')
                subcol.prop(PUrP, "CutThickness", text='Cut Thickness')
                subcol.prop(PUrP, "BevelOffset", text='Bevel Offset')
                subcol.prop(PUrP, "BevelSegments", text='Bevel Segments')
            if context.scene.PUrP.SingleMainTypes == '2':
                subcol.prop(context.scene.PUrP, "MaincutVert",
                            text='Maincut Verts')
            if PUrP.SingleCouplingTypes == "2" or PUrP.SingleCouplingTypes == "3":  # cylinder cone
                subcol.prop(context.scene.PUrP, "CylVert",
                            text='Inlay Vertices')
                subcol.prop(context.scene.PUrP, "aRadius", text='Radius')
                # subcol.prop(PUrP, "aRadius", text='Radius 1')
            if PUrP.SingleCouplingTypes == "3":
                subcol.prop(PUrP, "bRadius", text='Radius Top')

            if context.scene.PUrP.SingleCouplingModes == '4':
                subcol.prop(PUrP, "Oversize", text='Oversize')
                # subcol.prop(PUrP, "CoupSize", text='Coup Scale')
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

            subcol.prop(PUrP, "ViewPortVisAdd",
                        text='Add with Viewport Visibility')
            subcol.prop(PUrP, "AddUnmapped",
                        text='Add Unmapped')
            subcol = col.box()
            subcol.operator("apl.coup", text="Apply Connector(s)",
                            icon="MOD_DYNAMICPAINT")  # zeige button an
            subcol.operator("apl.allcoup", text='Apply All',
                            icon="EXPERIMENTAL")  # zeige button an
            subcol.prop(PUrP, "KeepCoup", text="Keep Connector")
            # subcol.operator_menu_hold(
            #    "purp.zscalemenu", "ZScale", text="Zscale")

        else:
            col.operator("purp.init", icon="SHADERFX")
            col.operator("purp.window_draw_operator", icon="SHADERFX")


class PP_PT_PuzzlePrintSApplyMenu(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Special Apply"
    bl_category = "PuzzleUrPrint"
    bl_options = {'DEFAULT_CLOSED'}

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
            subcol = col.column()
            subcol.label(text="Special Apply Methods")
            subcol.operator("object.applyplanarmultiobj", text='Planar To Multiple Objects',
                            icon="PARTICLE_POINT")  # zeige button an
            subcol.operator("object.applymultipleplanartoobject", text='Multiple Planar to Object',
                            icon="MOD_INSTANCE")
            subcol.operator("object.applysingletoobjects", text='Single Connector To Multiple Objects',
                            icon="MOD_INSTANCE")
            subcol.prop(PUrP, "IgnoreMainCut", text="Ignore Main Cut")
            # subcol.operator("object.pp_ot_overlapcheck",
            # text = 'Check Overlap', icon = "HIDE_OFF")
            subcol.operator("object.pp_ot_testcorrectname", text='Test correct name',
                            icon="MOD_INSTANCE")


class PP_PT_PuzzlePrintOrderMenu(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Mapping, Order, Visibility"
    bl_category = "PuzzleUrPrint"
    bl_options = {'DEFAULT_CLOSED'}

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
            subcol = col.box()
            subcol.label(text="Mapping")
            subcol.operator("object.remapcoups",
                            text='Remap Connector To Active', icon="FILE_REFRESH")
            subcol.operator("object.pp_ot_unmapcoup",
                            text='Unmap Connector', icon="FILE_REFRESH")
            subcol = col.box()
            subcol.label(text="Order")
            subcol.operator("pup.couplingorder",
                            text='Toggle Order', icon="LINENUMBERS_ON")
            subcol.operator("pup.modup", text='Up in Order ',
                            icon="TRIA_UP")
            subcol.operator(
                "pup.moddown", text='Down in Order', icon="TRIA_DOWN")

            subcol = col.box()
            subcol.label(text="Connector Visibility Toggles")
            subcol.operator("purp.connectorhide",
                            text='Visibility Selected', icon="VIS_SEL_11")
            subcol.operator("purp.allconnectorhide",
                            text='Visibility All', icon="HIDE_OFF")
            subcol.label(text="Modifier Visibility Toggle")
            subcol.operator("object.togglecoupvisibility",
                            text='Toggle Modifier Visibility', icon="RESTRICT_VIEW_ON")
            subcol.prop(PUrP, "InlayToggleBool", text='Toggle Inlay')


class PP_PT_PuzzlePrintBuildVolumeMenu(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Build Volume"
    bl_category = "PuzzleUrPrint"
    bl_options = {'DEFAULT_CLOSED'}

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
            subcol = col.column()
            subcol.prop(PUrP, "BuildplateX", text='Buildplate X')
            subcol.prop(PUrP, "BuildplateY", text='Buildplate Y')
            subcol.prop(PUrP, "BuildplateZ", text='Buildplate Z')
            subcol.operator("object.makebuildvolume",
                            text='Generate Buildvolume', icon="MESH_CUBE")
            if context.object != None:
                if "BuildVolume" in context.object.name:
                    Vol = context.object
                    mods = Vol.modifiers
                    subcol.label(text="BuildVolume Arrays")
                    subcol.prop(mods["PUrP_BuildVol_ArrayX"],
                                "count", text='Build Volume X Repeat')
                    subcol.prop(mods["PUrP_BuildVol_ArrayY"],
                                "count", text='Build Volume Y Repeat')
                    subcol.prop(mods["PUrP_BuildVol_ArrayZ"],
                                "count", text='Build Volume Z Repeat')


class PP_PT_PuzzlePrintActiveObject(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Active Connector"
    bl_category = "PuzzleUrPrint"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        if (context.view_layer.objects.active != None) and context.mode == 'OBJECT':
            if is_coup(context, context.object):
                return True
        else:
            return False

    def draw(self, context):
        PUrP = context.scene.PUrP
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
            subcol = col.column()
            subcol.prop(PUrP, "BuildplateX", text='Buildplate X')

            subcol.operator("purp.zscalemenu",
                            text=str(PUrP.zScale)[:5], icon="MESH_CUBE")
            subcol.operator("purp.roffsetgiz",
                            text=str(PUrP.OffsetRight)[:5], icon="MESH_CUBE")


'''
class PP_PT_PuzzlePrintActive(bpy.types.Panel):
    bl_space_type="VIEW_3D"
    bl_region_type="UI"
    bl_label="Active Coupling"
    bl_category="PuzzleUrPrint"



    # schreibe auf den Bildschirm
    def draw(self, context):


        data = bpy.data

        layout = self.layout ;

        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        flow = layout.grid_flow(row_major=True, columns=0,
                                even_columns=False, even_rows=False, align=True)
        col = flow.column()
        row = layout.row()


        col.operator("pup.modup", text = 'Move Modifiers Up')
        col.operator("pup.moddown", text = 'Move Modifiers Down')

'''
