import bpy

from bpy.types import Operator
import copy
import mathutils
from .bun import deselectall, is_coup


from .tutwindowengine import *
# from .tutwindowengine import BL_UI_OT_draw_operator


class BE_OT_Draw_Operator(BL_UI_OT_draw_operator):
    '''Brings you to Tutorialland of PuzzleUrPrint. A distant world, one Blender Scene away, where you'll learn how to use the addon Puzzle your Print'''
    bl_idname = "purp.window_draw_operator"
    bl_label = "Start Tutorial"
    bl_description = "Brings you to Tutorialland. A distant World one Blender Scene away, where you'll learn how to use the addon 'Puzzle your Print'"
    bl_options = {'REGISTER'}

    def __init__(self):

        super().__init__()
        self.TutorialCounter = 0
        self.panel = BL_UI_Drag_Panel(400, 300, 500, 600)
        self.panel.bg_color = (0.2, 0.2, 0.2, 0.9)
        # self.panel.mouse_move(-30, -100)

        self.label = BL_UI_Label(20, 20, 100, 15)
        self.label.text = "Welcome"
        self.label.text_size = 20
        self.label.text_color = (0.2, 0.9, 0.9, 1.0)

        self.closebutton = BL_UI_Button(460, 20, 30, 30)
        self.closebutton.bg_color = (0.2, 0.8, 0.8, 0.8)
        self.closebutton.hover_bg_color = (0.2, 0.9, 0.9, 1.0)
        self.closebutton.text = "X"
        self.closebutton.set_mouse_down(self.closebutton_press)

        lineamount = 25
        self.lines = []
        x = 20
        y = 50
        y_offset = 17
        height = 40
        width = 15
        count = 0
        while count <= lineamount:
            count += 1
            line = BL_UI_Label(x, y, height, width)
            line.text_size = 14
            self.lines.append(line)
            y += y_offset

        #self.label = BL_UI_Label(400, 450, 100, 15)
        #self.label.text = "Please Click Next"
        #self.label.text_size = 20
        #self.label.text_color = (0.2, 0.9, 0.9, 1.0)

        self.button1 = BL_UI_Button(20, 500, 120, 30)
        self.button1.bg_color = (0.2, 0.8, 0.8, 0.8)
        self.button1.hover_bg_color = (0.2, 0.9, 0.9, 1.0)
        self.button1.text = "Back"
        self.button1.set_mouse_down(self.button1_press)

        self.button2 = BL_UI_Button(350, 500, 120, 30)
        self.button2.bg_color = (0.2, 0.8, 0.8, 0.8)
        self.button2.hover_bg_color = (0.2, 0.9, 0.9, 1.0)
        self.button2.text = "Next"
        self.button2.set_mouse_down(self.button2_press)

    def on_invoke(self, context, event):

        self.initialzeviaTutorial(context)
        # Add new widgets here (TODO: perhaps a better, more automated solution?)
        widgets_panel = []
        widgets_panel.append(self.label)
        widgets_panel.append(self.closebutton)
        for line in self.lines:
            widgets_panel.append(line)
        widgets_panel.append(self.button1)
        widgets_panel.append(self.button2)
        # widgets_panel = [self.label, self.line1, self.line2, self.line3, self.line4, self.line5,
        #                 self.line6, self.line7, self.line8, self.line9, self.line10, self.button1, self.button2]
        widgets = [self.panel]

        widgets += widgets_panel

        self.init_widgets(context, widgets)

        self.panel.add_widgets(widgets_panel)

        # Open the panel at the mouse location
        self.panel.set_location(event.mouse_x,
                                context.area.height - event.mouse_y + 20)
        self.context = context
        self.slide00(context)

    def on_chb_visibility_state_change(self, checkbox, state):
        active_obj = bpy.context.view_layer.objects.active
        if active_obj is not None:
            active_obj.hide_viewport = not state

    def on_up_down_value_change(self, up_down, value):
        active_obj = bpy.context.view_layer.objects.active
        if active_obj is not None:
            active_obj.scale = (1, 1, value)

    def on_slider_value_change(self, slider, value):
        active_obj = bpy.context.view_layer.objects.active
        if active_obj is not None:
            active_obj.scale = (1, 1, value)

    # Button press handlers
    def button1_press(self, widget):
        context = self.context
        self.TutorialCounter -= 1
        self.pageturner(context)

    def button2_press(self, widget):
        context = self.context
        self.TutorialCounter += 1
        self.pageturner(context)

    def closebutton_press(self, widget):
        bpy.data.scenes.remove(self.tutorialscene)
        self.finish()

    def initialzeviaTutorial(self, context):
        self.tutorialscene = bpy.data.scenes.new("PUrPTutorial")
        context.window.scene = self.tutorialscene

        if "PuzzleUrPrint" not in bpy.data.collections:
            bpy.ops.purp.init()

    def linebreak(self, text):
        #maxCharnum = len(text)
        linelength = 70
        linebreaksymbol = "%"

        pos = 0
        for n, line in enumerate(self.lines):
            linebreak = False
            initalpos = copy.copy(pos)

            # check for linebreak
            while pos < (initalpos + linelength):
                #print(f"pos {initalpos} {linelength}")
                if pos == len(text):
                    break
                else:
                    if text[pos] == linebreaksymbol:
                        linebreak = True
                        linebreakpos = copy.copy(pos)
                        break

                pos += 1

            pos = initalpos
            # check if reaching the end of the text
            if linebreak:
                listart = pos
                liend = linebreakpos
            else:
                if pos + linelength > (len(text) - 1):
                    listart = pos
                    liend = len(text)
                else:
                    listart = pos
                    liend = pos + linelength
                    # check for last complete word
                    while text[liend] != " ":
                        liend -= 1

            line.text = text[listart:liend]
            if linebreak:
                pos = liend + 1
            else:
                pos = liend

    def add_single(self, context, x, y, z, mode, ViewPortVis, MaincutType,  MaincutVert, inlaytype, zScale, Oversize, BevOff, BevSeg, IgnoreMain, KeepCoup, AddUnmapped):
        PUrP = context.scene.PUrP
        PUrP.GlobalScale = 1
        PUrP.CoupScale = 1
        PUrP.CoupSize = 1  # inlaysize
        PUrP.SingleCouplingModes = mode
        PUrP.SingleMainTypes = MaincutType
        PUrP.SingleCouplingTypes = inlaytype
        PUrP.zScale = zScale
        PUrP.Oversize = Oversize
        PUrP.BevelSegments = BevSeg
        PUrP.BevelOffset = BevOff
        PUrP.KeepCoup = KeepCoup
        PUrP.MaincutVert = MaincutVert
        PUrP.ViewPortVisAdd = ViewPortVis
        PUrP.IgnoreMainCut = IgnoreMain
        PUrP.AddUnmapped = AddUnmapped

        context.scene.cursor.location = mathutils.Vector((x, y, z))
        bpy.ops.add.coup()

        return context.object

    def add_planar(self, context, x, y, z, ViewPortVis, PlanarCouplingTypes, OffsetRight, OffsetLeft, LineCount, LineLength, StopperHeight, StopperBool, KeepCoup, AddUnmapped):
        PUrP = context.scene.PUrP
        PUrP.GlobalScale = 1
        PUrP.CoupScale = 1
        PUrP.CoupSize = 1  # inlaysize
        PUrP.SingleCouplingModes = '4'
        PUrP.PlanarCouplingTypes = PlanarCouplingTypes
        #PUrP.SingleMainTypes = MaincutType
        #PUrP.SingleCouplingTypes = inlaytype

        PUrP.KeepCoup = KeepCoup
        PUrP.ViewPortVisAdd = ViewPortVis
        #PUrP.IgnoreMainCut = IgnoreMain
        PUrP.OffsetRight = OffsetRight
        PUrP.OffsetLeft = OffsetLeft
        PUrP.LineCount = LineCount
        PUrP.LineLength = LineLength
        PUrP.StopperHeight = StopperHeight
        PUrP.StopperBool = StopperBool
        PUrP.AddUnmapped = AddUnmapped
        context.scene.cursor.location = mathutils.Vector((x, y, z))
        bpy.ops.add.coup()
        return context.object

    def add_text(self, context, x, y, z, text):
        bpy.ops.object.text_add(
            enter_editmode=False, align='WORLD', location=(x, y, z), scale=(1, 1, 1))
        context.object.body = text
        return context.object

    def add_primitive(self, context, x, y, z, Key):
        if key == "Cube":
            print('CUbe')
            bpy.ops.mesh.primitive_cube_add(
                size=1, enter_editmode=False, align='WORLD', location=(x, y, z), scale=(1, 1, 1))
        elif key == "Cylinder":
            bpy.ops.mesh.primitive_cylinder_add(
                radius=1, depth=2, enter_editmode=False, align='WORLD', location=(x, y, z), scale=(1, 1, 1))
        elif key == "Sphere":
            bpy.ops.mesh.primitive_ico_sphere_add(
                radius=1, enter_editmode=False, align='WORLD', location=(x, y, z), scale=(1, 1, 1))
        else:
            print("Key not in the list")
        return context.object

    def cleanscene(self, context):
        deselectall(context)
        objs = bpy.data.scenes['PUrPTutorial'].objects
        bpy.ops.object.delete({"selected_objects": objs})

    def applycoup(self, context, coups):
        deselectall(context)
        for coup in coups:
            coup.select_set(True)
        bpy.ops.apl.coup()

    def applyallscene(self, context):
        deselectall(context)
        for ob in bpy.data.scene['PUrPTutorial'].objects:
            if is_coup(context, ob):
                ob.select_set(True)
                bpy.ops.apl.coup()

    def focus(self, context, objs):
        deselectall(context)
        for ob in obs:
            ob.select_set(True)
        bpy.ops.view3d.view_selected

    def pageturner(self, context):
        if self.TutorialCounter == 0:
            self.slide00(context)
        elif self.TutorialCounter == 1:
            self.slide01(context)
        elif self.TutorialCounter == 2:
            self.slide02(context)
        else:
            self.TutorialCounter = 0

    def slide00(self, context):
        self.cleanscene(context)

        self.label = "Welcome to the Tutorial"
        self.linebreak(
            "This little tutorial is designed to get you started. If you need a more detailed description try the documentation under PUrP.modicolitor.com.%% BTW, If you think 'This guy just deleted my work.', don't worry. We are in a new scene, when you close the Tutorial you'll get back to your original scene.%% This interactive Tutorial will generate new objects to show you what the addon is capable off. Be encouraged to play the objects and settings. However, don't be sad when you go to another slide or out of the Tutorial and everything is gone :-D.")

        bpy.ops.view3d.localview(frame_selected=True)
        bpy.ops.view3d.localview(frame_selected=True)

    def slide01(self, context):
        self.cleanscene(context)
        print('Learn what')
        self.label.text = "What does the addon do?"
        self.linebreak(
            "It helps to cut models in pieces and simutansouly add conntectors for simple reassambling after 3D Printing.")

        bpy.ops.mesh.primitive_cube_add(
            size=5, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 3))
        self.addsingle(context, 0, 0, 0, '2', True, '1',  16,
                       '1', 1.5, 0.04, 0, 0, False, False, False)

        bpy.ops.view3d.localview(frame_selected=True)
        bpy.ops.view3d.localview(frame_selected=True)

    def slide02(self, context):
        self.cleanscene(context)
        print('Learn what')
        self.label.text = "First Contact"
        self.linebreak("This is one example of a connector.")

        bpy.ops.mesh.primitive_cube_add(
            size=5, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

        self.addsingle(context, 0, 0, 0, '1', True, '1',  16,
                       '1', 1.5, 0.04, 0, 0, False, False, False)
        self.addplanar(context, 5, 5, 6, True, '5', 1,
                       1, 3, 3, 5, False, False, False)
        bpy.ops.view3d.localview(frame_selected=True)
        bpy.ops.view3d.localview(frame_selected=True)

    def slide03(self, context):
        self.cleanscene(context)
        print('Learn what')
        self.label.text = "First Contact"
        self.linebreak("This is one example of a connector.")

        bpy.ops.mesh.primitive_cube_add(
            size=5, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

        self.addsingle(context, 0, 0, 0, '1', True, '1',  16,
                       '1', 1.5, 0.04, 0, 0, False, False, False)
        self.addplanar(context, 5, 5, 6, True, '5', 1,
                       1, 3, 3, 5, False, False, False)
        bpy.ops.view3d.localview(frame_selected=True)
        bpy.ops.view3d.localview(frame_selected=True)

    def slide04(self, context):
        self.cleanscene(context)
        print('Learn what')
        self.label.text = "First Contact"
        self.linebreak("This is one example of a connector.")

        bpy.ops.mesh.primitive_cube_add(
            size=5, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

        self.addsingle(context, 0, 0, 0, '1', True, '1',  16,
                       '1', 1.5, 0.04, 0, 0, False, False, False)
        self.addplanar(context, 5, 5, 6, True, '5', 1,
                       1, 3, 3, 5, False, False, False)

        bpy.ops.view3d.localview(frame_selected=True)
        bpy.ops.view3d.localview(frame_selected=True)
