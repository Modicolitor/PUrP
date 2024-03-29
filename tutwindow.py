#
# Copyright (C) 2020 by Modicolitor
#
# This file is part of PuzzleUrPrint.
#
# License Text
#
# You should have received a copy of the GNU General Public License along with PuzzleUrPrint. If
# not, see <https://www.gnu.org/licenses/>.


from .gen_mesh import gen_arrow, gen_figure, gen_hat
import bpy

from bpy.types import Operator
import copy
from mathutils import Vector
from .bun import deselectall, is_coup, applyScale, applySingleCoup
from math import pi

from .tutwindowengine import *
# from .tutwindowengine import BL_UI_OT_draw_operator


class BE_OT_Draw_Operator(BL_UI_OT_draw_operator):
    '''Brings you to Tutorialland of PuzzleUrPrint. A distant world, one Blender Scene away, where you'll learn how to use the addon Puzzle your Print'''
    bl_idname = "purp.window_draw_operator"
    bl_label = "Start Tutorial"
    bl_description = "Brings you to Tutorialland. A distant World, one whole Blender Scene away, where you'll learn how to use the addon 'Puzzle your Print'"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self):

        super().__init__()
        self.TutorialCounter = 0
        self.panel = BL_UI_Drag_Panel(0, 0, 500, 600)  # 400 200
        self.panel.bg_color = (0.2, 0.2, 0.2, 0.9)
        # self.panel.mouse_move(-30, -100)

        self.label = BL_UI_Label(20, 20, 100, 15)
        self.label.text = "Welcome"
        self.label.text_size = 20
        self.label.text_color = (0.80, 0.2, 0.2, 0.8)

        self.closebutton = BL_UI_Button(460, 20, 30, 30)
        self.closebutton.bg_color = (0.80, 0.2, 0.2, 0.8)
        self.closebutton.hover_bg_color = (0.80, 0.2, 0.2, 0.8)
        self.closebutton.text = "X"
        self.closebutton.text_color = (0.8, 0.9, 0.9, 1.0)
        self.closebutton.set_mouse_down(self.closebutton_press)

        lineamount = 27
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

        self.slidenum = BL_UI_Label(200, 550, 100, 15)
        self.set_slidenum(99)
        self.slidenum.text_size = 20
        self.slidenum.text_color = (0.8, 0.9, 0.9, 1.0)

        self.button1 = BL_UI_Button(20, 550, 120, 30)
        self.button1.bg_color = (0.80, 0.2, 0.2, 0.8)
        self.button1.hover_bg_color = (0.80, 0.2, 0.2, 0.8)
        self.button1.text = "Back"
        self.button1.text_color = (0.8, 0.9, 0.9, 1.0)
        self.button1.set_mouse_down(self.button1_press)

        self.button2 = BL_UI_Button(350, 550, 120, 30)
        self.button2.bg_color = (0.80, 0.2, 0.2, 0.8)
        self.button2.hover_bg_color = (0.80, 0.2, 0.2, 0.8)
        self.button2.text = "Next"
        self.button2. text_color = (0.8, 0.9, 0.9, 1.0)
        self.button2.set_mouse_down(self.button2_press)

    def on_invoke(self, context, event):

        self.initialzeviaTutorial(context)
        # Add new widgets here (TODO: perhaps a better, more automated solution?)
        widgets_panel = []
        widgets_panel.append(self.label)
        widgets_panel.append(self.closebutton)
        widgets_panel.append(self.slidenum)
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
        # print(
        #    f" width {context.area.width} height {context.area.height} event.mouse_x {event.mouse_x} event.mouse_y {event.mouse_y} ")
        self.panel.set_location(event.mouse_x - context.area.height/30,  # context.area.width -
                                -context.area.height/4)  # context.area.height - event.mouse_y

        self.viewloc = (-0, -21, 2)
        self.viewrot = (0.75, 0.6565, 0.0325, 0.0262)
        self.viewdistance = 20
        self.headloc = Vector((0, 0, 5))
        self.headlinescale = Vector((3, 3, 3))

        self.context = context
        self.pageturner(context)
        # self.slide00(context)
    '''
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
    '''
    # Button press handlers

    def button1_press(self, widget):
        context = self.context
        # self.TutorialCounter -= 1
        context.screen.PUrPTutcount -= 1
        self.pageturner(context)

    def button2_press(self, widget):
        context = self.context
        # self.TutorialCounter += 1
        context.screen.PUrPTutcount += 1
        self.pageturner(context)

    def closebutton_press(self, widget):
        bpy.data.scenes.remove(self.tutorialscene)
        self.finish()

    def refresh_widget(self, widget):
        bpy.ops.purp.window_draw_operator()
        bpy.data.scenes.remove(self.tutorialscene)
        self.finish()

    def initialzeviaTutorial(self, context):
        if not "PUrPTutorial" in context.scene.name:
            self.tutorialscene = bpy.data.scenes.new("PUrPTutorial")
        else:
            self.tutorialscene = context.scene

        context.window.scene = self.tutorialscene

        if not hasattr(context.scene, "PUrP"):
            bpy.ops.purp.init()

    def set_slidenum(self, num):
        self.slidenum.text = str(num)+"/15"

    def linebreak(self, text):
        # maxCharnum = len(text)
        linelength = 70
        linebreaksymbol = "%"

        pos = 0
        for n, line in enumerate(self.lines):
            linebreak = False
            initalpos = copy.copy(pos)

            # check for linebreak
            while pos < (initalpos + linelength):
                # print(f"pos {initalpos} {linelength}")
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

    def add_single(self, context, loc, ConnectorScale, InlayScale, mode, ViewPortVis, MaincutType,  MaincutVert, inlaytype, zScale, Oversize, CylVert, BevOff, BevSeg, aRadius, bRadius, AddUnmapped):
        PUrP = context.scene.PUrP
        PUrP.GlobalScale = 1
        PUrP.CoupScale = ConnectorScale
        PUrP.CoupSize = InlayScale
        PUrP.SingleCouplingModes = mode
        PUrP.SingleMainTypes = MaincutType
        PUrP.SingleCouplingTypes = inlaytype
        PUrP.CylVert = CylVert
        PUrP.zScale = zScale
        PUrP.Oversize = Oversize
        PUrP.BevelSegments = BevSeg
        PUrP.BevelOffset = BevOff
        PUrP.aRadius = aRadius
        PUrP.bRadius = bRadius
        # PUrP.KeepCoup = KeepCoup
        PUrP.MaincutVert = MaincutVert
        PUrP.ViewPortVisAdd = ViewPortVis
        # PUrP.IgnoreMainCut = IgnoreMain
        PUrP.AddUnmapped = AddUnmapped

        context.scene.cursor.location = loc
        bpy.ops.add.coup()

        return context.object

    def add_planar(self, context, loc, ConnectorScale, zScale, Oversize, ViewPortVis, PlanarCouplingTypes, OffsetRight, OffsetLeft, LineCount, LineLength, StopperHeight, StopperBool, KeepCoup, AddUnmapped, Linedistance):
        PUrP = context.scene.PUrP
        PUrP.GlobalScale = 1
        PUrP.CoupScale = ConnectorScale
        PUrP.CoupSize = 1  # inlaysize
        PUrP.Oversize = Oversize
        PUrP.SingleCouplingModes = '4'
        PUrP.PlanarCouplingTypes = PlanarCouplingTypes
        # PUrP.SingleMainTypes = MaincutType
        # PUrP.SingleCouplingTypes = inlaytype
        PUrP.zScale = zScale
        PUrP.KeepCoup = KeepCoup
        PUrP.ViewPortVisAdd = ViewPortVis
        # PUrP.IgnoreMainCut = IgnoreMain
        PUrP.OffsetRight = OffsetRight
        PUrP.OffsetLeft = OffsetLeft
        PUrP.LineCount = LineCount
        PUrP.LineDistance = Linedistance
        PUrP.LineLength = LineLength
        PUrP.StopperHeight = StopperHeight
        PUrP.StopperBool = StopperBool
        PUrP.AddUnmapped = AddUnmapped
        context.scene.cursor.location = loc
        bpy.ops.add.coup()
        return context.object

    def add_text(self, context, loc, text):
        bpy.ops.object.text_add(
            enter_editmode=False, align='WORLD', location=loc, scale=(1, 1, 1))
        context.object.data.body = text
        context.object.data.align_x = 'CENTER'

        return context.object

    def add_primitive(self, context, loc, key):
        if key == "Cube":
            print('CUbe')
            bpy.ops.mesh.primitive_cube_add(
                size=1, enter_editmode=False, align='WORLD', location=loc, scale=(1, 1, 1))
        elif key == "Cylinder":
            bpy.ops.mesh.primitive_cylinder_add(
                radius=1, depth=2, enter_editmode=False, align='WORLD', location=loc, scale=(1, 1, 1))
        elif key == "Sphere":
            bpy.ops.mesh.primitive_ico_sphere_add(
                radius=1, enter_editmode=False, align='WORLD', location=loc, scale=(1, 1, 1))
        else:
            print("Key not in the list")
        return context.object

    def cleanscene(self, context):
        deselectall(context)
        objs = self.tutorialscene.objects
        bpy.ops.object.delete({"selected_objects": objs})

    def applycoup(self, context, coups):
        # deselectall(context)
        alldaughters = []
        for coup in coups:
            daughters = applySingleCoup(context, coup, coup.parent, True)
            for d in daughters:
                alldaughters.append(d)  # coup.select_set(True)

        return alldaughters
        # bpy.ops.apl.coup()

    def applyallscene(self, context):
        deselectall(context)
        for ob in self.tutorialscene.objects:
            if is_coup(context, ob):
                ob.select_set(True)
                bpy.ops.apl.coup()

    def set_view(self, context, loc, rot, distance):

        for area in bpy.context.screen.areas:
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    s = space

        s.lens = 50
        r = s.region_3d
        # print(r.view_location)
        # print(r.view_rotation)
        r.view_location = loc
        r.view_rotation = rot
        r.view_distance = distance

    def focus(self, context, objs):
        deselectall(context)
        for ob in objs:
            ob.select_set(True)
        bpy.ops.view3d.view_selected()

    def pageturner(self, context):

        for n, hand in enumerate(bpy.app.handlers):
            print(bpy.app.handlers[n])

        self.TutorialCounter = context.screen.PUrPTutcount
        print(self.TutorialCounter)
        print(self.lines[0].text)

        if self.TutorialCounter == 0:
            self.slide00(context)
        elif self.TutorialCounter == 1:
            self.slide01(context)
        elif self.TutorialCounter == 2:
            self.slide02(context)
        elif self.TutorialCounter == 3:
            self.slide03(context)
        elif self.TutorialCounter == 4:
            self.slide04(context)
        elif self.TutorialCounter == 5:
            self.slide05(context)
        elif self.TutorialCounter == 6:
            self.slide06(context)
        elif self.TutorialCounter == 7:
            self.slide07(context)
        elif self.TutorialCounter == 8:
            self.slide08(context)
        elif self.TutorialCounter == 9:
            self.slide09(context)
        elif self.TutorialCounter == 10:
            self.slide10(context)
        elif self.TutorialCounter == 11:
            self.slide11(context)
        elif self.TutorialCounter == 12:
            self.slide12(context)
        elif self.TutorialCounter == 13:
            self.slide13(context)
        elif self.TutorialCounter == 14:
            self.slide14(context)
        elif self.TutorialCounter == 15:
            self.slide15(context)
        else:
            self.TutorialCounter = 0

    def slide00(self, context):
        self.cleanscene(context)
        self.viewloc = (-0, -21, 2)
        self.viewrot = (0.75, 0.6565, 0.0325, 0.0262)
        self.viewdistance = 20
        self.set_view(context, self.viewloc, self.viewrot, self.viewdistance)
        self.set_slidenum(0)
        self.label.text = "Welcome to the Tutorial"
        self.headloc = Vector((0, 0, 5))
        self.headlinescale = Vector((3, 3, 3))
        self.linebreak(
            "This little tutorial is designed to get you started. If you need a more detailed description try the documentation under PUrP.modicolitor.com or the Modicolitor Youtube channel.%% This interactive tutorial will generate new objects to show you what the addon is capable of. Be encouraged to play with the objects and settings in the scene. However, don't be sad when you go to another slide or out of the Tutorial and everything is gone :-D. %% BTW, If you think 'This guy just deleted my work.', don't worry. We are in a new scene, when you close the tutorial you'll get back to your original scene. Moreover, sorry this tutorial window is not very stable. I'm working on it. If it stops reacting just close it and start a new tutorial session. You'll continue on the slide you left. The actual addon functionalities are super reliable!")
        headline = self.add_text(
            context, self.headloc, "Welcome to the Tutorial")
        headline.rotation_euler[0] = 1.507
        cubeloc = Vector((0, 0, 0))
        Cube = self.add_primitive(context, cubeloc, 'Cube')
        Cube.scale = Vector((4, 4, 4))
        con1 = self.add_single(context, cubeloc, 1, 1, '2', True,
                               '1',  16, '1', 1.5, 0.04, 16, 0, 0, 1, 1, False)
        daughters = self.applycoup(context, [con1])
        daughters[0].location[2] -= 1
        daughters[1].location[2] += 1
        # self.focus(context, self.tutorialscene.objects)
        deselectall(context)
        context.view_layer.objects.active = headline
        # arrow = gen_arrow(context, (-12, 0, 0))
        # arrow.rotation_euler[1] = 1.5078
        # hat = gen_hat(context, (0, 0, 0))
        # hat.location = (9.99, 0, 3.739)
        # hat.scale = (0.45, 0.45, 0.45)

    def slide01(self, context):
        self.cleanscene(context)

        self.viewloc = (0, -21, 2)
        self.viewrot = (0.75, 0.6565, 0.0325, 0.0262)
        self.viewdistance = 20
        self.set_view(context, self.viewloc, self.viewrot, self.viewdistance)

        self.set_slidenum(1)
        self.label.text = "What does the addon do?"
        self.linebreak(
            "The addon helps to cut models in pieces and simultansouly add connectors for simple reassambling after 3D Printing. The PuzzleUrPrint-addon can produce a broad variety of these Connectors called objects (or combination of objects), which are internally used in boolean operation to eventually generate the transformation intended. Here you see a cube with a 'Single Connector' in male-female configuration with cube as Inlay type.... Lets see how it looks after applying.")
        headline = self.add_text(
            context, self.headloc, "What does the addon do?")
        headline.rotation_euler[0] = 1.507
        headline.scale = (3, 3, 3)
        cubeloc = Vector((0, 0, 0))
        Cube = self.add_primitive(context, cubeloc, 'Cube')
        Cube.scale = Vector((4, 4, 4))
        con1 = self.add_single(context, cubeloc, 1, 1, '2',  True,
                               '1',  16, '1', 1.5, 0.04, 16, 0, 0, 1, 1, False)
        # self.applyallscene(context)
        # self.focus(context, self.tutorialscene.objects)

        arrow = gen_arrow(context, (-6.5, 0, 0))
        arrow.rotation_euler[1] = pi/2
        arrow.scale = (0.5, 0.5, 0.5)
        text = self.add_text(context, (-11, 0, 0), 'This is a Connector')
        text.rotation_euler[0] = pi/2

        deselectall(context)
        # self.focus(context, self.tutorialscene.objects)
        context.view_layer.objects.active = headline

    def slide02(self, context):
        self.cleanscene(context)
        self.viewloc = (0, -21, 2)
        self.viewrot = (0.75, 0.6565, 0.0325, 0.0262)
        self.viewdistance = 20
        self.set_view(context, self.viewloc, self.viewrot, self.viewdistance)
        self.set_slidenum(2)
        self.label.text = "The Result"
        self.linebreak("This is the result you would get when you apply the connector from the last slide to the cube. The cube is now cut in half. Moreover, the bottom part has a male connector attached while the top part has a hole in the shape of the connector. If you would print that you could put both parts together again easily. This can be helpful for many things.%% - Print large: 3D-printers are typically very small. Use the addon to desect large models into printable bits. Your lifesized Koro is only a few clicks and days of printing away (support cloud.blender.org!!)%- Add Functionality: Using cylinders as Inlays allows you to twist two parts adjoined. A 'joint'-cut allows you to make even more delicate joints.  Print your own actionfigures, monsters, sculptures,... with movable parts.% -Puzzles: Of course you can make puzzles with PuzzleUrPrint. Whether you deform a plane (with some thickness of course) and make a more traditional 2D puzzle, you can also make 3D Puzzles by dissecting larger objects for a new generation of challenging puzzles. It'll change the whole experience. %- Wallmounts and fasteners: You can add dovetail and other shapes to make objects slide into each other and, if you like, stop at the right point. This is ideal for wallholders and nice to hide the screws. ")
        headline = self.add_text(context, self.headloc, "The Result")
        headline.rotation_euler[0] = 1.507
        headline.scale = (3, 3, 3)
        cubeloc = Vector((0, 0, 0))
        Cube = self.add_primitive(context, cubeloc, 'Cube')
        Cube.scale = Vector((4, 4, 4))
        Cube.name = 'PUrPCube'
        con1 = self.add_single(context, cubeloc, 1, 1, '2',  True,
                               '1',  16, '1', 1.5, 0.04, 16, 0, 0, 1, 1, False)

        daughters = self.applycoup(context, [con1])
        daughters[0].location[2] = -3
        daughters[1].location[2] = 1

        arrow = gen_arrow(context, (-6.5, 0, 2))
        arrow.rotation_euler[1] = pi/2
        arrow.scale = (0.5, 0.5, 0.5)
        text = self.add_text(context, (-10, 0, 1.76), 'Female Part')
        text.rotation_euler[0] = pi/2

        arrow = gen_arrow(context, (-6.5, 0, -4))
        arrow.rotation_euler[1] = pi/2
        arrow.scale = (0.5, 0.5, 0.5)
        text = self.add_text(context, (-10, 0, -4.23), 'Male Part')
        text.rotation_euler[0] = pi/2
        # self.applyallscene(context)
        # self.focus(context, self.tutorialscene.objects)
        headline.select_set(True)
    # diversity

    def slide03(self, context):
        self.cleanscene(context)
        self.set_slidenum(3)
        self.label.text = "Many Connectors shapes: Settings"
        self.linebreak("Here you see a couple of examples of connectors. They can have all kinds of shapes and produce different functionalities. Quite diverse, right?% You can produce all of these connectors by adjusting the settings in the 'Add, Exchange, Apply'-dropdown. With 'Add Connector' a new connector will be born using the current settings in the 'Add, Exchange, Apply'-dropdown. If you haven't specified another (mesh) object by selecting it or another connector is selected, the addon will try to map (something like parenting) the connector to the last known 'Center Object'. This is the object set in the top line in 'Add,Exhange,Apply'.%You can change the settings via the 'Add, Exchange, Apply'-dropdown or via the gizmos visible when a connector is selected. While changing settings via gizmos will take immediate effect on the mesh or the settings in the dropdown, changes in the 'Add, Exchange, Apply'-dropdown will only take effect after pressing the 'Exchange'-Button. % If you are interested to know which settings produced a specific connector, select the connector of interest and press 'Active to Settings' in the 'Add, Exchange, Apply'-dropdown. The dropdown now shows the settings of the active connector. You can 'paste' these new settings onto an existing connector by selecting it and pressing 'Exchange'.%Useful Detail: I just switched off 'Add with Viewport Visibility'. Showing the boolean result makes working extremly slow. You can toggle the visibility on/off for selected connectors by pressing 'Toggle Modifier Visibility' in the 'Mapping, Order, Visibility'- dropdown")

        self.viewloc = (1, -58, 40)
        self.viewrot = (0.881, 0.474, 0.005, 0.0004)
        self.viewdistance = 40
        self.set_view(context, self.viewloc, self.viewrot, self.viewdistance)

        headline = self.add_text(
            context, (self.headloc[0], self.headloc[1], self.headloc[0] + 5), "A Large Variety of Options")
        headline.rotation_euler[0] = 1.507
        headline.scale = (5, 5, 5)
        # singleconnectors
        singloc = Vector((-20, -10, 0))
        singletext = self.add_text(context, singloc, "Single Connectors")
        singletext.scale = Vector((2.3, 2.3, 2.3))
        # cube mf
        cube1loc = Vector((-5, 0, 0))
        Cube1 = self.add_primitive(context, cube1loc, 'Cube')
        Cube1.scale = Vector((3, 3, 3))
        con1 = self.add_single(context, cube1loc, 1, 1, '2', False,
                               '1',  16, '1', 1.2, 0.04, 16, 0, 0, 1, 1, False)

        cube1loc = Vector((-5, 10, 0))
        Cube1 = self.add_primitive(context, cube1loc, 'Cube')
        Cube1.scale = Vector((3, 3, 3))
        con1 = self.add_single(context, cube1loc, 1, 1, '1', False,
                               '1',  16, '1', 1.2, 0.04, 16, 0, 0, 1, 1, False)

        cube1loc = Vector((-5, 20, 0))
        Cube1 = self.add_primitive(context, cube1loc, 'Cube')
        Cube1.scale = Vector((3, 3, 3))
        con1 = self.add_single(context, cube1loc, 1, 1, '3', False,
                               '1',  16, '1', 1.2, 0.04, 16, 0, 0, 1, 1, False)
        # joint
        jointloc = Vector((-20, 0, 0))
        Cylinder1 = self.add_primitive(context, jointloc, 'Cylinder')
        Cylinder1.scale = Vector((2, 2, 5))
        joint1 = self.add_single(context, jointloc, 1, 1, '1', False,
                                 '2',  16, '2', 1.5, 0.04, 16, 0.2, 3, 1, 1, False)
        joint1.rotation_euler[1] = 1.1
        for vert in joint1.data.vertices:
            vert.co[2] *= 1.5
        # joint1.scale[2] = 1.5
        # applyScale(joint1)

        # cone
        coneloc = Vector((-20, 10, 0))
        cube = self.add_primitive(context, coneloc, 'Cube')
        cube.scale = Vector((3, 3, 3))
        self.add_single(context, coneloc, 1, 0.5, '2', False,
                        '1', 16, '3', 0.8, 0.04, 16, 0, 1, 1, 0, False)

        # cone variation
        coneloc = Vector((-20, 20, 0))
        self.add_primitive(context, coneloc, 'Sphere')
        self.add_single(context, coneloc, 1, 0.5, '2', False,
                        '1', 16, '3', 0.7, 0.04, 16, 0, 1, 1, 0.3, False)

        # flat
        sphereloc = Vector((-35, 0, 0))
        Cube1 = self.add_primitive(context, sphereloc, 'Sphere')
        Cube1.scale = Vector((2, 2, 2))
        self.add_single(context, sphereloc, 1.5, 1, '3', False,
                        '1', 16, '1', 2, 0.04, 16, 0, 1, 1, 1, False)

        cube1loc = Vector((-35, 10, 0))
        Cube1 = self.add_primitive(context, cube1loc, 'Sphere')
        Cube1.scale = Vector((2, 2, 2))
        con1 = self.add_single(context, cube1loc, 1, 1, '1', False,
                               '1',  16, '2', 1.5, 0.04, 16, 0.4, 3, 1, 1, False)

        cube1loc = Vector((-35, 20, 0))
        Cube1 = self.add_primitive(context, cube1loc, 'Sphere')
        Cube1.scale = Vector((2, 2, 2))
        con1 = self.add_single(context, cube1loc, 1, 1, '1', False,
                               '1',  16, '2', 1.5, 0.04, 3, 0.4, 3, 1, 1, False)

        # planar
        planaloc = Vector((20, -10, 0))
        planartext = self.add_text(context, planaloc, "Planar Connectors")
        planartext.scale = Vector((1.75, 1.75, 1.75))
        # puzzle
        largeplaneloc = Vector((10, 0, 0))
        largeplanep = self.add_primitive(context, largeplaneloc, 'Cube')
        largeplanep.scale = Vector((10, 10, 0.2))
        puzzle1 = self.add_planar(
            context, Vector((6.6674, -1.7019, 0.26765)), 0.30, 1, 0.04, False, '4', 1.22, 1.22, 2, 3, 1.0, False, False, False, 3.32)
        puzzle2 = self.add_planar(
            context, Vector((11.391, -3.3397, 0.36302)), 0.30, 1, 0.04, False, '5', 1.22, 1.22, 2, 3, 1.0, False, False, False, 3.34)
        puzzle2.rotation_euler[2] = 1.5708

        # cube with stopper
        cubestopperloc = Vector((27, 0, 0))
        cubestopper = self.add_primitive(context, cubestopperloc, 'Cube')
        cubestopper.scale = Vector((5, 3, 3))
        plancol = self.add_planar(
            context, Vector(
                (27, 0, 2)), 1, 3, 0.04,  False, '2', 1.2, 1.2, 1, 1, 3, True, False, False, 3.2)

        # planar collection without stopper
        largeplaneloc = Vector((10, 32, 0))
        largeplane1 = self.add_primitive(context, largeplaneloc, 'Cube')
        largeplane1.scale = Vector((15, 48, 1))
        type = 1
        plancolloc = Vector((4.6, 10, 1))
        while type <= 16:

            plancol = self.add_planar(
                context, plancolloc, 1, 3, 0.04, False, str(type), 1.2, 1.2, 1, 3, 5, False, False, False, 3.2)
            plancolloc += Vector((0, 3, 0))
            type += 1
        # planar collection with stopper
        largeplaneloc = Vector((30, 32, 0))
        largeplane1 = self.add_primitive(context, largeplaneloc, 'Cube')
        largeplane1.scale = Vector((15, 48, 1))
        type = 1
        plancolloc = Vector((24.5, 10, 1))
        while type <= 15:
            plancol = self.add_planar(
                context, plancolloc, 1, 1, 0.04, False, str(type), 1.2, 1.2, 1, 3, 5, True, False, False, 3.2)
            plancolloc += Vector((0, 3, 0))
            type += 1
        # self.focus(context, self.tutorialscene.objects)
        deselectall(context)
        # headline.select_set(True)
        context.view_layer.objects.active = headline
    # connector modes

    def slide04(self, context):
        self.cleanscene(context)
        self.viewloc = (5, -21, 8)
        self.viewrot = (0.75, 0.6565, 0.0325, 0.0262)
        self.viewdistance = 20
        self.set_view(context, self.viewloc, self.viewrot, self.viewdistance)

        self.set_slidenum(4)
        self.label.text = "Connector Modes"
        self.linebreak("There are 4 types of connector modes. %- Stick, %- Male-Female (mf)  %- Flat %- Planar %%We saw a mf-connector in the first example. After applying, one of the resulting objects will be male and one will be female.%Stick mode will generate two female daughter objects and an additional 'Stick'-Object to connect both. Having the stick as an additional part can be beneficial. For example, you need to reprint less (only the stick), if your oversize value is off. We'll talk about oversize later.%Flat is actually just a stupid plane. It cuts two things in half without any connector. Still can be useful if you want to glue stuff together anyway.%Planar is a whole new world, compared to the other modes. Mathematically speaking (or was it topologically, geographically) the functionallity is here parallel to the maincut and not perpendicular like in the first two cases. Moreover, a planar can generate a large number of couplings with one object while the first two only produce one coupling. That's why I'll call the first 3 modes Stick, MF and Flat  (yeah, I know flat doesn't...bla) Single Connector Modes and the other is multiconnectors... ok they are called  planar  .... for consistency ... you'll get it... later... maybe.")
        headline = self.add_text(context, self.headloc, "Connector Modes")
        headline.scale = self.headlinescale
        headline.rotation_euler[0] = 1.507

        # Stick
        singloc = Vector((-15, -10, 0))
        singletext = self.add_text(context, singloc, "Stick")
        singletext.scale = Vector((2.3, 2.3, 2.3))
        # cube
        cube1loc = Vector((-15, 0, 0))
        Cube1 = self.add_primitive(context, cube1loc, 'Cube')
        Cube1.scale = Vector((3, 3, 3))
        con1 = self.add_single(context, cube1loc, 1, 1, '1', False,
                               '1',  16, '1', 1.5, 0.04, 16, 0, 0, 1.0, 0.0, False)
        # cube applied
        cube1loc = Vector((-15, 10, 0))
        Cube1 = self.add_primitive(context, cube1loc, 'Cube')
        Cube1.scale = Vector((3, 3, 3))
        con1 = self.add_single(context, cube1loc, 1, 1, '1', False,
                               '1',  16, '1', 1.5, 0.04, 16, 0, 0, 1.0, 0.0, False)

        daughters = self.applycoup(context, [con1])
        daughters[0].location[2] -= 2
        daughters[1].location[2] += 2
        # Male-Female
        singloc = Vector((-5, -10, 0))
        singletext = self.add_text(context, singloc, "Male-Female")
        singletext.scale = Vector((2.3, 2.3, 2.3))
        # cube
        cube1loc = Vector((-5, 0, 0))
        Cube1 = self.add_primitive(context, cube1loc, 'Cube')
        Cube1.scale = Vector((3, 3, 3))
        con1 = self.add_single(context, cube1loc, 1, 1, '2', False,
                               '1',  16, '1', 1.5, 0.04, 16, 0, 0, 1.0, 0.0, False)

        cube1loc = Vector((-5, 10, 0))
        Cube1 = self.add_primitive(context, cube1loc, 'Cube')
        Cube1.scale = Vector((3, 3, 3))
        con1 = self.add_single(context, cube1loc, 1, 1, '2', False,
                               '1',  16, '1', 1.5, 0.04, 16, 0, 0, 1.0, 0.0, False)

        daughters = self.applycoup(context, [con1])
        daughters[0].location[2] -= 2
        daughters[1].location[2] += 2
        # Flat
        singloc = Vector((5, -10, 0))
        singletext = self.add_text(context, singloc, "Flat")
        singletext.scale = Vector((2.3, 2.3, 2.3))
        # cube
        cube1loc = Vector((5, 0, 0))
        Cube1 = self.add_primitive(context, cube1loc, 'Cube')
        Cube1.scale = Vector((3, 3, 3))
        con1 = self.add_single(context, cube1loc, 1, 1, '3', False,
                               '1',  16, '1', 1.5, 0.04, 16, 0, 0, 1, 0, False)
        # applied
        cube1loc = Vector((5, 10, 0))
        Cube1 = self.add_primitive(context, cube1loc, 'Cube')
        Cube1.scale = Vector((3, 3, 3))
        con1 = self.add_single(context, cube1loc, 1, 1, '3', False,
                               '1',  16, '1', 1.5, 0.04, 16, 0, 0, 1.0, 0.0, False)
        daughters = self.applycoup(context, [con1])
        daughters[0].location[2] -= 2
        daughters[1].location[2] += 2
        # planar
        singloc = Vector((15, -10, 0))
        singletext = self.add_text(context, singloc, "Planar")
        singletext.scale = Vector((2.3, 2.3, 2.3))
        # cube
        cube1loc = Vector((15, 0, 0))
        Cube1 = self.add_primitive(context, cube1loc, 'Cube')
        Cube1.scale = Vector((3, 3, 3))
        planar = self.add_planar(
            context, Vector((15, 0, 2)), 0.5, 4, 0.04, False, '4', 2, 2, 1, 1, 1, False, False, False, 3.2)
        # applied
        cube1loc = Vector((15, 10, 0))
        Cube1 = self.add_primitive(context, cube1loc, 'Cube')
        Cube1.scale = Vector((3, 3, 3))
        planar = self.add_planar(
            context, Vector((15, 10, 2)), 0.5, 4, 0.04, False, '4', 2, 2, 1, 1, 1, False, False, False, 3.2)
        daug = self.applycoup(context, [planar])
        daug[1].location[1] += 2
        # headline.select_set(True)
        context.view_layer.objects.active = headline

    # Single Connectors

    def slide05(self, context):
        self.cleanscene(context)
        self.viewloc = (5, -21, 8)
        self.viewrot = (0.75, 0.6565, 0.0325, 0.0262)
        self.viewdistance = 20
        self.set_view(context, self.viewloc, self.viewrot, self.viewdistance)

        self.set_slidenum(5)
        self.label.text = "Single Connectors"
        self.linebreak(
            "Single Connectors consist of one maincut and two inlay objects.%%The maincut causes the initial seperation of the object in two parts. You can choose the maincut type to be Flat or Joint. The Flat type is only a plane with a solidify modifier. It creates a flat base cut. However, the Joint type produces a circular ... joint cut (Please email me better terms) useful for example for elbows of your actionfigure. It is not forbiden to enter edit mode and change the shape to your liking. In most cases also 'Exchange' will not replace your adjusted maincut. %%The inlay shapes can be either cube, cylinder or cone. I forbid selecting them. Believe me, you'll mess it up. It's better for all of us. They are parented to the maincut anyway. Use the panel or the Gizmos to change them. Depending on the chosen Inlay Type additional settings might become available in the panel and gizmos. For example cylinders have additional settings to adjust the vertcount and radius, for cone you can set the upper and lower radius individually. However, also consider that some configuration will not make sense. For example a cone in stick configuration doesn't make much sense.  However, all single connectors have a lot of parameters in common. Lets talk about them in the next part together with the gizmos system.%%%Useful Detail: You might get the error 'This connector didn't cut through'! Is this really what you want?'. Then you might Undo and check which Connector might need repositioning. ")
        headline = self.add_text(context, self.headloc, "Single Connectors")
        headline.rotation_euler[0] = 1.507
        headline.scale = (5, 5, 5)
        # [[flat [as text], joint [as text],] [flat mf (cube) (cylinder) (Cone)]

        text = self.add_text(context, (-10, -10, 0), "Maincut Types")
        text.scale = (3, 3, 3)
        self.add_text(context, (-15, -5, 0), "Flat")
        self.add_text(context, (-5, -5, 0), "Joint")
        # self.add_text(context, (2.5, -5, 0), "Cube")

        # self.add_text(context, (12.5, -5, 0), "Cone")

        cube1loc = Vector((-15, 0, 0))
        Cube1 = self.add_primitive(context, cube1loc, 'Cube')
        Cube1.scale = Vector((3, 3, 3))
        con1 = self.add_single(context, cube1loc, 1, 1, '2', False,
                               '1',  16, '1', 1.0, 0.04, 16, 0, 0, 1, 0, False)
        # joint
        jointloc = Vector((-5, 0, 0))
        Cylinder1 = self.add_primitive(context, jointloc, 'Cylinder')
        Cylinder1.scale = Vector((1, 1, 2.5))
        joint1 = self.add_single(context, jointloc, 0.5, 1, '1', False,
                                 '2',  16, '2', 1.5, 0.04, 16, 0.2, 3, 1, 1, False)
        joint1.rotation_euler[1] = 1.1
        for vert in joint1.data.vertices:
            vert.co[2] *= 1.5

        text = self.add_text(context, (10, -10, 0), "Inlay Type")
        text.scale = (3, 3, 3)
        self.add_text(context, (2.5, -5, 0), "Cube")
        self.add_text(context, (10, -5, 0), "Cylinder")
        self.add_text(context, (17.5, -5, 0), "Cone")

        cube1loc = Vector((2.5, 0, 0))
        Cube1 = self.add_primitive(context, cube1loc, 'Cube')
        Cube1.scale = Vector((3, 3, 3))
        con1 = self.add_single(context, cube1loc, 1, 1, '2', False,
                               '1',  16, '1', 1.0, 0.04, 16, 0, 0, 1, 0, False)

        cube1loc = Vector((10, 0, 0))
        Cube1 = self.add_primitive(context, cube1loc, 'Cube')
        Cube1.scale = Vector((3, 3, 3))
        con1 = self.add_single(context, cube1loc, 1, 1, '2', False,
                               '1',  16, '2', 1.0, 0.04, 16, 0, 0, 1, 0, False)
        cube1loc = Vector((17.5, 0, 0))
        Cube1 = self.add_primitive(context, cube1loc, 'Cube')
        Cube1.scale = Vector((3, 3, 3))
        con1 = self.add_single(context, cube1loc, 1, 0.5, '2', False,
                               '1',  16, '3', 1.0, 0.04, 16, 0, 0, 1, 0, False)
        # headline.select_set(True)
        context.view_layer.objects.active = headline

    def slide06(self, context):
        self.cleanscene(context)
        self.viewloc = (5, -21, 8)
        self.viewrot = (0.75, 0.6565, 0.0325, 0.0262)
        self.viewdistance = 20
        self.set_view(context, self.viewloc, self.viewrot, self.viewdistance)

        self.set_slidenum(6)
        self.label.text = "Single Connector Gizmos"

        self.linebreak(
            "When you select a Connector several colorful symbols appear around the connecotor's origin (only avaiable when the addon is installed and initalized). These are controls to change several settings and, hence, the appearance of the connector.%% From bottom to top:%- The two gizmos at the bottom control the maincut: the ring for the Connector Scale, the other for the Maincut Thickness (should be in the range of the oversize).%- The big blue cube controls the Inlay Size%-The light blue controls the Oversize (see later!!)%- The corner shapes represent controls over the beveling of the inlay shapes, the large one is the Beveloffset and the small one the Bevelsegments (only visible when Beveloffset is not zero).%-The red up arrow represents the zScale with which you can stretch the inlay along (local) z-axis.%-Cone type has additional two controls for upper and lower radius (exchange cone with radius top higher than 0 to have control over the top via gizmos)%In addition, using any Gizmos will also change the settings in the panel too. You can also keep your mouse hovering over a gizmo to get a tooltip about what it does.%%Useful detail: If muscle memory made you scale the connector with the blender typical 's'-shortcut, it's not a big deal. However, just click the green ring at the bottom (connector scale) to have the scale of all objects back to (1,1,1) (important for Oversize calculations, see later).")
        headline = self.add_text(
            context, self.headloc, "Single Connector Gizmos")
        headline.scale = (5, 5, 5)
        headline.rotation_euler[0] = 1.507
        # [flat mf (cube) (cylinder) (Cone)] für single gizmos, nix applied

        text = self.add_text(context, (0, -10, 0), "Try Out the Gizmos")
        text.scale = (3, 3, 3)
        self.add_text(context, (-7.5, -5, 0), "Cube")
        self.add_text(context, (0, -5, 0), "Cylinder")
        self.add_text(context, (7.5, -5, 0), "Cone")

        cube1loc = Vector((-7.5, 0, 0))
        Cube1 = self.add_primitive(context, cube1loc, 'Cube')
        Cube1.scale = Vector((3, 3, 3))
        con1 = self.add_single(context, cube1loc, 1, 1, '2', False,
                               '1',  16, '1', 1.0, 0.04, 16, 0, 0, 1, 0, False)

        cube1loc = Vector((0, 0, 0))
        Cube1 = self.add_primitive(context, cube1loc, 'Cube')
        Cube1.scale = Vector((3, 3, 3))
        con2 = self.add_single(context, cube1loc, 1, 1, '2', False,
                               '1',  16, '2', 1.0, 0.04, 16, 0, 0, 1, 0, False)
        cube1loc = Vector((7.5, 0, 0))
        Cube1 = self.add_primitive(context, cube1loc, 'Cube')
        Cube1.scale = Vector((3, 3, 3))
        con3 = self.add_single(context, cube1loc, 1, 0.5, '2', False,
                               '1',  16, '3', 1.0, 0.04, 16, 0, 0, 1, 0, False)
        deselectall(context)
        # con1.select_set(True)
        context.view_layer.objects.active = headline

    def slide07(self, context):
        self.cleanscene(context)
        self.viewloc = (5, -21, 8)
        self.viewrot = (0.75, 0.6565, 0.0325, 0.0262)
        self.viewdistance = 20
        self.set_view(context, self.viewloc, self.viewrot, self.viewdistance)

        self.set_slidenum(7)
        self.label.text = "Planar Connectors "
        self.linebreak(
            "Planar connectors are essentially a plane with a coupling element and two array modifiers  to duplicate it. In this version 16 different connector types (shapes) are avaiable: cubic, dovetail, different puzzle shapes, arrow, t-shape,... . Try out what fits for your project (recommendations for additional shapes welcome)   One array duplicates allong the line, called Linelength. The other array generates copies of the original lines with Linecount being the number of lines and the Linedistance between those lines. Together with the Oversize, these 4 settings can be also changed via the 4 upper gizmos. You can keep the mouse on the gizmos to get small definition what it does. Additionally you'll find 3 Arrow shaped gizmos: the upwards arrow changes the zScale (height),  the left and right arrows control the Left- and Right-Offset. This is the distance between the coupling element and the end of a repeating unit. Maybe reduce the 'Linelength' to 1 to get a clearer understanding of what they do.%%A Subclass of Planar is called Planar with Stopper. In this configuration the Connector part ends somewhere in the middle of the plane and the rest is only a flat cut. Get one by activating the 'Stopper' checkbox and add or Exchange a connector. Models printed with this will not fall through like a puzzle piece but will be stopped at the right height when putting together. This is ideal for example to make wallmounts with replaceable parts, canvases, guitars,.... where ever you need the pieces slide into each other and stay where they are supposed to. When you have Stopper activated, you'll see the setting Stopper Height in the dropdown as well as in the connector's gizmos as a down arrow.")
        headline = self.add_text(context, self.headloc, "Planar Connectors")
        headline.rotation_euler[0] = 1.507
        headline.scale = (5, 5, 5)
        # [center planar, planar with stopper je mit text (im Hintergrund overview von seite 3)]
        text = self.add_text(context, (-13, -5, 0), "Without Stopper")
        text.scale = (3, 3, 3)
        # cube without stopper
        cubestopperloc = Vector((-5, 0, 0))
        cubestopper = self.add_primitive(context, cubestopperloc, 'Cube')
        cubestopper.scale = Vector((5, 3, 3))
        plancol = self.add_planar(context, (-5, 0, 2), 1, 5.0, 0.04,
                                  False, '2', 1.2, 1.2, 1, 1, 3, False, False, False, 3.2)

        text = self.add_text(context, (13, -5, 0), "With Stopper")
        text.scale = (3, 3, 3)
        # cube with stopper
        cubestopperloc = (5, 0, 0)
        cubestopper = self.add_primitive(context, cubestopperloc, 'Cube')
        cubestopper.scale = Vector((5, 3, 3))
        plancol = self.add_planar(
            context, (5, 0, 2), 1, 3, 0.04,  False, '2', 1.2, 1.2, 1, 1, 2, True, False, False, 3.2)

        # cube without stopper applied
        cubestopperloc = Vector((-5, 5, 0))
        cubestopper = self.add_primitive(context, cubestopperloc, 'Cube')
        cubestopper.scale = Vector((5, 3, 3))
        plancol = self.add_planar(context,
                                  (-5, 5, 2), 1, 5.0, 0.04,  False, '2', 1.2, 1.2, 1, 1, 3, False, False, False, 3.2)
        daughters = self.applycoup(context, [plancol])
        daughters[0].location[1] -= 1.3
        daughters[1].location[1] += 1.3

        # cube with stopper applied
        cubestopperloc = Vector((5, 5, 0))
        cubestopper = self.add_primitive(context, cubestopperloc, 'Cube')
        cubestopper.scale = Vector((5, 3, 3))
        plancol = self.add_planar(context, (5, 5, 2), 1, 3, 0.04,
                                  False, '2', 1.2, 1.2, 1, 1, 2, True, False, False, 3.2)
        daughters = self.applycoup(context, [plancol])
        daughters[0].location[1] -= 1.3
        daughters[1].location[1] += 1.3

        # planar collection without stopper
        largeplaneloc = Vector((-14.8, 32, 0))
        largeplane1 = self.add_primitive(context, largeplaneloc, 'Cube')
        largeplane1.scale = Vector((15, 48, 1))
        type = 1
        plancolloc = Vector((-20.5, 10, 1))
        while type <= 16:
            plancol = self.add_planar(
                context, plancolloc, 1, 3, 0.04, False, str(type), 1.2, 1.2, 1, 3, 5, False, False, False, 3.2)
            plancolloc += Vector((0, 3, 0))
            type += 1
        # planar collection with stopper
        largeplaneloc = Vector((20, 32, 0))
        largeplane1 = self.add_primitive(context, largeplaneloc, 'Cube')
        largeplane1.scale = Vector((15, 48, 1))
        type = 1
        plancolloc = Vector((14.5, 10, 1))
        while type <= 15:
            plancol = self.add_planar(
                context, plancolloc, 1, 1, 0.04, False, str(type), 1.2, 1.2, 1, 3, 1.0, True, False, False, 3.2)
            plancolloc += Vector((0, 3, 0))
            type += 1
        # self.focus(context, self.tutorialscene.objects)
        deselectall(context)
        # headline.select_set(True)
        context.view_layer.objects.active = headline

    def slide08(self, context):
        self.cleanscene(context)
        self.viewloc = (5, -21, 8)
        self.viewrot = (0.75, 0.6565, 0.0325, 0.0262)
        self.viewdistance = 20
        self.set_view(context, self.viewloc, self.viewrot, self.viewdistance)

        self.set_slidenum(8)
        self.label.text = "Positioning and Scaling"
        self.linebreak(
            "You can move and rotate the connectors as you like to find the right position using for example the typical Blender shortcuts 'r' and 'g'. Scaling with shortcut 's' is inadvisable because you change the scaling of the object. Better use the Connectorscale Gizmo (green large ring) for scaling. If it is more convenient for you to use 's' at least click the 'Connector Scale' - Gizmo once shortly after you are done. It will correct the scaling and will make the Oversize be consistent over all connectors. Again this oversize term. Next we'll get to it.%%%Useful Detail: All values in the addon are multiplied by the GlobalScale. The size of connectors, the oversize, the build volume, even the sensitivity of the gizmos. Typically, exporting formats like *.stl interpret size different to blender resulting in a need to scale up the models while exporting or in the slicing software. Naturally, we start working in larger dimensions in Blender. Adjust the Globalscale to compensate. For example, a Globalscale of 10 allows you to work nicely when blender meter translates to one mm in reality (without scaling in the slicer or during blender export), which is the normal behavior of an stl being imported into Cura.")
        headloc = (self.headloc[0], self.headloc[1], self.headloc[0] + 8)
        headline = self.add_text(context, headloc,
                                 "Positioning and Scaling")
        headline.rotation_euler[0] = 1.507
        headline.scale = (5, 5, 5)
        # [figure + one connector, and half done puzzle (make a Puzzle)]

        # figure
        figure = gen_figure(context, (-10, 0, 0))
        figure.scale = (2, 2, 2)
        # hals
        conloc = (-10, 0, 6.4)
        con1 = self.add_single(context, conloc, 0.18, 1, '1', False,
                               '1',  16, '2', 2.5, 0.04, 32, 0.02, 3, 1, 1,  False)

        # Arm 1 set
        conloc = (-10.74, 0.024, 5.87)
        con1 = self.add_single(context, conloc, 0.18, 1, '1', False,
                               '1',  16, '2', 1.8, 0.04, 32, 0.02, 3, 1, 1,  False)
        con1.rotation_euler[1] = 1.57079632679489
        # Arm2
        conloc = (-8, 0, 5.87)
        con1 = self.add_single(context, conloc,  0.18, 1, '1', False,
                               '1',  16, '2', 1.8, 0.04, 32, 0.02, 3, 1, 1,  False)
        # Schenkel 1
        conloc = (-8, 0, 3.768)
        con1 = self.add_single(context, conloc, 0.15, 1, '1', False,
                               '2',  32, '2', 2.68, 0.04, 16, 0.02, 3, 1, 1, False)

        # Schenkel 2 set
        conloc = (-10.453, -0.042, 3.768)
        con1 = self.add_single(context, conloc, 0.15, 1, '1', False,
                               '2',  32, '2', 2.68, 0.04, 16, 0.02, 3, 1, 1, False)
        con1.rotation_euler[1] = -1.57079632679489
        con1.rotation_euler[0] = 1.57079632679489*2

        # anweisung
        text = self.add_text(context, (0, 0, 5.5),
                             "You can practice\n by positioning these")
        text.rotation_euler[0] = 1.57079632679489
        # up arrow
        arrow = gen_arrow(context, (-5.938, 0, 5.89))
        arrow.scale = (0.25, 0.25, 0.25)
        arrow.rotation_euler[1] = -1.57079632679489

        # down arrow
        arrow = gen_arrow(context, (-5.938, 0, 3.6))
        arrow.scale = (0.25, 0.25, 0.25)
        arrow.rotation_euler[1] = -1.57079632679489

        # down arrow
        arrow = gen_arrow(context, (+4.5, 0, 2.5))
        arrow.scale = (0.25, 0.25, 0.25)
        arrow.rotation_euler[1] = 2.5

        # puzzle
        largeplaneloc = Vector((10, 0, 0))
        largeplanep = self.add_primitive(context, largeplaneloc, 'Cube')
        largeplanep.scale = Vector((10, 10, 0.2))
        puzzle1 = self.add_planar(
            context, Vector((6.6674, -1.7019, 0.26765)), 0.30, 1, 0.04, False, '4', 1.22, 1.22, 2, 3, 1.0, False, False, False, 3.32)
        puzzle2 = self.add_planar(
            context, Vector((20, 0, 0.36302)), 0.30, 1, 0.04, False, '5', 1.22, 1.22, 2, 3, 1.0, False, False, False, 3.34)
        # puzzle2.rotation_euler[2] = 1.5708
        # headline.select_set(True)
        context.view_layer.objects.active = headline

    def slide09(self, context):
        self.cleanscene(context)
        self.viewloc = (5, -21, 8)
        self.viewrot = (0.75, 0.6565, 0.0325, 0.0262)
        self.viewdistance = 20
        self.set_view(context, self.viewloc, self.viewrot, self.viewdistance)

        self.set_slidenum(9)
        self.label.text = "Oversize"
        self.linebreak(
            "The oversize setting allows you to compensate for printing inaccuracies.%We all know it: 3D printing is a wonderful thing but not really exact. Typically, a 3D printed part is a bit larger than it's supposed to be. For FDM (fuse depositon molding) printers, this comes for example from smearing material a bit over the side while following printing path. Also the shape of an object and as a result the path the printer takes, will have an influence on the oversize. Try printing two walls connected in a 90° angle. Especially, with high printing velocities you'll see thickening at the outside of the corner. Of course, also nozzle size, problems with overhanging parts, brim, orientation of the part... the number of influencing parameters is large, so it is unfortunately hard to give a perfect recommendation for all cases. However, the oversize is the option to compensate for all those parameters. Keep in mind, that the oversize is an absolute value. If the printer's oversize 0.4 mm for a small object, your print has the same oversize for a bigger object. On the one hand this means the connector can have the same oversize despite their size. On the other hand your PUrP Oversize might get wrong when scaling object later (e.g. in the slicer software).%% Useful Detail: My Oversize Values - Fortunately, I found a very consistent picture for my system (Cura+Ultimaker3) where I can use an Oversize of 0.02 for all round shapes (cylinder, cone, puzzles,...) for a tight fit even independent of the nozzle size. Only cube inlays need 0.03 for a nice fit. But I really recommend printing small test pieces with different oversize values until you figure out the best values for your 3D Printer.")
        headline = self.add_text(context, self.headloc, "Oversize")
        headline.rotation_euler[0] = 1.507
        headline.scale = (5, 5, 5)
        # [Cube, Cylinder, planar mit objecten, text (play with the oversize) ]

        self.add_text(context, (0, -10, 0), "Play with the Oversize")
        cube1loc = Vector((-7.5, 0, 0))
        Cube1 = self.add_primitive(context, cube1loc, 'Cube')
        Cube1.scale = Vector((3, 3, 3))
        con1 = self.add_single(context, cube1loc, 1, 1, '2', False,
                               '1',  16, '1', 1.0, 0.04, 16, 0, 0, 1, 0, False)

        cube1loc = Vector((0, 0, 0))
        Cube1 = self.add_primitive(context, cube1loc, 'Cube')
        Cube1.scale = Vector((3, 3, 3))
        con2 = self.add_single(context, cube1loc, 1, 1, '2', False,
                               '1',  16, '2', 1.0, 0.04, 16, 0, 0, 1, 0, False)

        cubestopperloc = Vector((7.5, 0, 0))
        cubestopper = self.add_primitive(context, cubestopperloc, 'Cube')
        cubestopper.scale = Vector((5, 3, 3))
        plancol = self.add_planar(
            context, Vector(
                (7.5, 0, 2)), 1, 4, 0.04,  False, '2', 1.2, 1.2, 1, 1, 3, False, False, False, 3.2)
        # headline.select_set(True)
        context.view_layer.objects.active = headline

    def slide10(self, context):
        self.cleanscene(context)
        self.viewloc = (5, -21, 8)
        self.viewrot = (0.75, 0.6565, 0.0325, 0.0262)
        self.viewdistance = 20
        self.set_view(context, self.viewloc, self.viewrot, self.viewdistance)

        self.set_slidenum(10)
        self.label.text = "Mapping"
        self.linebreak(
            "Mapping is the way connectors are bound to the object they are supposed to cut (Centerobject). It includes parenting. When you move the object in the viewport the connectors will follow. Moreover, mapping also includes having the boolean modifiers of a connector already on the Centerobject allowing you to preview the result (if you can work with a slow blender). The addon will check for these attributes during applying. A Connector can only be mapped to one Centerobject% However, you can change the mapping of a connector by using the 'Remap Connector to Active'-Button. Select the connector you want to remap and then the new Centerobject it should be mapped to and press the 'Remap Connector to Active'-Button. Now the parenting and the modifiers exist on the other object.%Moreover, if you don't want to have a connector mapped to any object, you can either add them with the checkbox 'Add Unmapped' in the 'Add, Exchange,...'- dropdown enabled or you select an existing connector and press 'Unmap Connector' in the 'Mapping, Order, Visibility' -dropdown.%%Useful Detail: If a mapped connector doesn't touch/cut any part of a Centerobject during applying (for example Apply All), it will remain in the scene and will be labeled unmapped. If you get this during applying when you don't expect it, check if your connector is not secretly touching another object (maybe an object that will exist after cutting everything in pieces).")

        headloc = (self.headloc[0], self.headloc[1], self.headloc[2]+7)
        headline = self.add_text(context, headloc, "Mapping")
        headline.rotation_euler[0] = 1.507
        headline.scale = (5, 5, 5)
        # [high cube 3 connectors, apply the one in the middle, check the mapping of the new objects, remap one connector]

        cube1loc = Vector((0, 0, 0))
        Cube1 = self.add_primitive(context, cube1loc, 'Cube')
        Cube1.scale = Vector((3, 3, 20))
        con2 = self.add_single(context, cube1loc, 1, 1, '1', False,
                               '1',  16, '2', 1.0, 0.04, 16, 0, 0, 1, 0, False)
        con2 = self.add_single(context, (0, 0, -5), 1, 1, '2', False,
                               '1',  16, '2', 1.0, 0.04, 16, 0, 0, 1, 0, False)
        con2 = self.add_single(context, (0, 0, 5), 1, 1, '3', False,
                               '1',  16, '2', 1.0, 0.04, 16, 0, 0, 1, 0, False)
        arrow = gen_arrow(context, (-10, 0, 0))
        arrow.rotation_euler[1] = 1.57079632679489
        hinweis = self.add_text(context, (-18.5, 0, 1.27),
                                "Apply this one and check \nthe mapping of the remaining couples. \nThen change the mapping of\none of them to the other Centerobject.")
        hinweis.rotation_euler[0] = 1.57079632679489

        # headline.select_set(True)
        context.view_layer.objects.active = headline

    def slide11(self, context):
        self.cleanscene(context)
        self.viewloc = (5, -21, 8)
        self.viewrot = (0.75, 0.6565, 0.0325, 0.0262)
        self.viewdistance = 20
        self.set_view(context, self.viewloc, self.viewrot, self.viewdistance)

        self.set_slidenum(11)
        self.label.text = "Applying and Order"
        self.linebreak(
            "By Applying a Connector you finalize the editing process, cut the model in pieces and add the connectors. You can choose to select one or several connectors and Press 'Apply Connector(s)' to have only specific connectors applied or you press 'Apply All' (both in 'Add,Exchange,Apply'-dropdown) to apply all Connectors mapped to a Centerobject (or the Centerobj the selected Connector is mapped to). When the checkbox 'Cut Everything' is disabled, the connectors will only cut the objects they are mapped to. For several planar connectors this will mean that not all resulting objects get cut by the following connector. Enable 'Cut Everything' to have the connecotrs cut everything they touch.%The order in which the Connectors are applied can be displayed as little numbers above the Connectors by toggling on/off with 'Toggle Order' in the 'Mapping,Order,Visibility'-dropdown. The order can be changed by selecting a connector and pressing either 'Up in Order' or 'Down in Order'. Monitoring the order is rarely necessary but in an example like this it can be important.%%Useful Detail: By default the connectors get deleted after applying. If they are precious to you check the checkbox 'Keep Connector' before applying and they will be kept unmapped.")
        headline = self.add_text(
            context, (self.headloc[0], self.headloc[1], self.headloc[2]+10), "Applying and Order")
        headline.rotation_euler[0] = 1.507
        headline.scale = (5, 5, 5)
        # 3x[one cube with two planar and a single] with different order

        # Version links
        largeplaneloc = Vector((-10, 0, 0))
        largeplanep = self.add_primitive(context, largeplaneloc, 'Cube')
        largeplanep.scale = Vector((7, 7, 7))

        puz1loc = (largeplaneloc[0]-2, largeplaneloc[1]-0, largeplaneloc[2]+4)
        puzzle1 = self.add_planar(
            context, puz1loc, 0.30, 8.5, 0.04, False, '10', 1.5, 1.5, 1, 2, 1.0, False, False, False, 3.32)

        puz2loc = (largeplaneloc[0]-0.33,
                   largeplaneloc[1]-2, largeplaneloc[2]+4)
        puzzle2 = self.add_planar(
            context, puz2loc, 0.30, 8.5, 0.04, False, '13', 1.5, 1.5, 1, 2, 1.0, False, False, False, 3.34)
        puzzle2.rotation_euler[2] = 1.57079632679489

        con2 = self.add_single(context, largeplaneloc, 1.44, 1, '2', False,
                               '1',  16, '1', 1.0, 0.04, 16, 0, 0, 1, 0, False)

        # Version Mitte
        largeplaneloc = Vector((0, 0, 0))
        largeplanep = self.add_primitive(context, largeplaneloc, 'Cube')
        largeplanep.scale = Vector((7, 7, 7))

        puz1loc = (largeplaneloc[0]-2, largeplaneloc[1]-0, largeplaneloc[2]+4)
        puzzle1 = self.add_planar(
            context, puz1loc, 0.30, 8.5, 0.04, False, '10', 1.5, 1.5, 1, 2, 1.0, False, False, False, 3.32)
        con2 = self.add_single(context, largeplaneloc, 1.44, 1, '2', False,
                               '1',  16, '1', 1.0, 0.04, 16, 0, 0, 1, 0, False)

        puz2loc = (largeplaneloc[0]-0.33,
                   largeplaneloc[1]-2, largeplaneloc[2]+4)
        puzzle2 = self.add_planar(
            context, puz2loc, 0.30, 8.5, 0.04, False, '13', 1.5, 1.5, 1, 2, 1.0, False, False, False, 3.34)
        puzzle2.rotation_euler[2] = 1.57079632679489

        # Version rechts
        largeplaneloc = Vector((10, 0, 0))
        largeplanep = self.add_primitive(context, largeplaneloc, 'Cube')
        largeplanep.scale = Vector((7, 7, 7))

        con2 = self.add_single(context, largeplaneloc, 1.44, 1, '2', False,
                               '1',  16, '1', 1.0, 0.04, 16, 0, 0, 1, 0, False)

        puz1loc = (largeplaneloc[0]-2, largeplaneloc[1]-0, largeplaneloc[2]+4)
        puzzle1 = self.add_planar(
            context, puz1loc, 0.30, 8.5, 0.04, False, '10', 1.5, 1.5, 1, 2, 1.0, False, False, False, 3.32)

        puz2loc = (largeplaneloc[0]-0.33,
                   largeplaneloc[1]-2, largeplaneloc[2]+4)
        puzzle2 = self.add_planar(
            context, puz2loc, 0.30, 8.5, 0.04, False, '13', 1.5, 1.5, 1, 2, 1.0, False, False, False, 3.34)
        puzzle2.rotation_euler[2] = 1.57079632679489

        context.scene.PUrP.CutAll = True

        self.add_text(context, (0, -10, 0),
                      "All 3 Cubes have the same Connectors \napplied, but in different orders.\nThe order of the one on the right might be helpful for very large prints (use 'Cut Everything')")

        hinweis = self.add_text(context, (-20, 0, 10),
                                "Select one or several connectors and press 'Apply Connector(s)'.\n")
        hinweis.rotation_euler[0] = 1.57079632679489
        hinweis = self.add_text(context, (20, 0, 10),
                                "Select one Centerobject and press 'Toggle Order'\nto get the order displayed.\nTry 'Apply All' to see the results.")
        hinweis.rotation_euler[0] = 1.57079632679489

        # headline.select_set(True)
        context.view_layer.objects.active = headline

    def slide12(self, context):
        self.cleanscene(context)
        self.viewloc = (5, -21, 8)
        self.viewrot = (0.75, 0.6565, 0.0325, 0.0262)
        self.viewdistance = 20
        self.set_view(context, self.viewloc, self.viewrot, self.viewdistance)

        self.set_slidenum(12)
        self.label.text = "Special Apply Menu"
        self.linebreak(
            "The 'Special Apply'-dropdown has some extra operations that might get helpful:%- 'Planar To Multiple Objects' allows you to decide which objects also should be cut through in addition to the Centerobject the planar is mapped to. For example (left) you make a puzzle and applied only the first planar, the second will be only applied to the one row its mapped to. Select all rows first and select the remaining planar last. Then Press  Planar To Multiple Objects'. BTW: 'Apply All' will do this automatically. %- 'Multiple Planar to Object' does it the other way around. Select several Planar Connectors, select the Centerobj of choice last and press the button. Typically 'Apply All' handles these cases reliably. However, this can become useful if you can't use 'Apply All'.%- 'Single To Multiple Objects' This allows you to connect one Single Connector being applied to several Objects. Imagine your character needs a new hat. Select the hat and the character and the Single Connector last and press 'Single To Multiple Objects'. You can also enable 'Ignore Main Cut' to do exactly that during applying.")
        headline = self.add_text(context, self.headloc, "Special Apply Menu")
        headline.rotation_euler[0] = 1.507
        headline.scale = (5, 5, 5)
        # [Puzzle with one applied(Cube with planar and single, single applied)[text: Planar to Multiple Objects], PUzzle both unapplied,  figure + Head ]

        # puzzle1
        self.add_text(context, (-15, -10, 0),
                      "Select all Puzzlestripes, \n select Connector last  and \npress 'Planar to Multiple Objects'")
        largeplaneloc = Vector((-12, 0, 0))
        largeplanep = self.add_primitive(context, largeplaneloc, 'Cube')
        largeplanep.scale = Vector((10, 10, 0.2))
        puzzle1 = self.add_planar(
            context, Vector((-15.34, -1.35, 0.26765)), 0.30, 1, 0.04, False, '4', 1.22, 1.22, 2, 3, 1.0, False, False, False, 3.32)
        puzzle2 = self.add_planar(
            context, Vector((-10.58, -3.39, 0.36302)), 0.30, 1, 0.04, False, '5', 1.22, 1.22, 2, 3, 1.0, False, False, False, 3.34)
        puzzle2.rotation_euler[2] = 1.5708
        self.applycoup(context, [puzzle1])

        self.add_text(context, (15, -10, 0),
                      "Select both Connectors and \nthen plane last and press \n'Multiple Connectors to Object'.")
        # puzzle2
        largeplaneloc = Vector((0, 0, 0))
        largeplanep = self.add_primitive(context, largeplaneloc, 'Cube')
        largeplanep.scale = Vector((10, 10, 0.2))
        puzzle1 = self.add_planar(
            context, Vector((-3.340, -1.3582, 0.26765)), 0.30, 1, 0.04, False, '4', 1.22, 1.22, 2, 3, 1.0, False, False, False, 3.32)
        puzzle2 = self.add_planar(
            context, Vector((+1.425, -3.3397, 0.36302)), 0.30, 1, 0.04, False, '5', 1.22, 1.22, 2, 3, 1.0, False, False, False, 3.34)
        puzzle2.rotation_euler[2] = 1.5708

        # figure + hat

        hat = gen_hat(context, (0, 0, 0))
        hat.location = (15, 0, 3.739)
        hat.scale = (0.45, 0.45, 0.45)
        gen_figure(context, (15, 0, 0))
        con2 = self.add_single(context, (15, 0, 3.72), 0.16, 0.65, '2', False,
                               '1',  16, '2', 2.76, 0.04, 16, 0, 0, 1, 0, False)
        self.add_text(context, (0, -10, 0),
                      "Select both Connectors and \nthen plane last and press \n'Multiple Connectors to Object'.")
        # headline.select_set(True)
        context.view_layer.objects.active = headline

    def slide13(self, context):
        self.cleanscene(context)

        self.viewloc = (19, -191, 29)
        self.viewrot = (0.703, 0.7081, 0.0483, 0.0379)
        self.viewdistance = 20
        self.set_view(context, self.viewloc, self.viewrot, self.viewdistance)

        self.set_slidenum(13)
        self.label.text = "BuildVolume"
        self.linebreak(
            "Especially when you dissect large objects to fit in your 3D printer, you always need to know how big your print real estate is at all times. In the 'Build Volume'-Dropdown, you can set the size of your 3D printer in cm (probably if you haven't changed it globally to freedom units) and press 'Generate Buildvolume' to get this cube (set to wireframe). When added you can adjust also its repetition in x,y and z. You can add as many as you like. The settings will only be available for the last selected Build Volume. The BuildVolumes are nothing more than simple objects to get a feel for the available space. Otherwise they do nothing.")
        headline = self.add_text(
            context, (self.headloc[0], self.headloc[1], self.headloc[2]+55), "BuildVolume")
        headline.rotation_euler[0] = 1.507
        headline.scale = (5, 5, 5)
        # [Figure with connector, Buildvolume with 2x2x4 ]
        fig = gen_figure(context, (0, 0, 0))
        fig.scale = (14, 14, 14)
        context.scene.cursor.location = (-18.7, -21.5, 6.5)
        bpy.ops.object.makebuildvolume()
        context.object.modifiers['PUrP_BuildVol_ArrayX'].count = 3
        context.object.modifiers['PUrP_BuildVol_ArrayY'].count = 3
        context.object.modifiers['PUrP_BuildVol_ArrayZ'].count = 3

        # headline.select_set(True)
        context.view_layer.objects.active = headline

    def slide14(self, context):
        self.cleanscene(context)
        self.viewloc = (19, -191, 29)
        self.viewrot = (0.703, 0.7081, 0.0483, 0.0379)
        self.viewdistance = 20
        self.set_view(context, self.viewloc, self.viewrot, self.viewdistance)

        self.set_slidenum(14)
        self.label.text = "Typical Process"
        self.linebreak(
            "Here is a typical workflow to work with the addon:%1. Import/append model, apply all modifiers (keep backup)%2. Select the model%3. Set the 3d cursor to a point where you want to add a connector. Press Add Connector,%4. Adjust settings, exchange, position with 's' and 'r'-shortcuts, fine tune with the gizmos...%5. Repeat to add more connectors as you like, use 'Active to Setting' and 'Exchange' as copy and paste of connector settings.%[6-53]. ...%54. Maybe print a few test cuts to figure out the best oversize value and adjust the connectors accordingly.%55. Adjust all Oversize values according to your test results%56. Apply All Connectors or do it manually one by one%57. 3D Print %58. PUZZLE THEM TOGETHER  %%Let Blender be your canvas and make cool stuff. Please send me pics, models and suggestions to info@modicolitor.com")
        headline = self.add_text(
            context, (self.headloc[0], self.headloc[1], self.headloc[2]+55), "Typical Process")
        headline.rotation_euler[0] = 1.507
        headline.scale = (5, 5, 5)
        # [Figure + Buildvolume]

        fig = gen_figure(context, (0, 0, 0))
        fig.scale = (14, 14, 14)
        context.scene.cursor.location = (-18.7, -21.5, 6.5)
        bpy.ops.object.makebuildvolume()
        context.object.modifiers['PUrP_BuildVol_ArrayX'].count = 3
        context.object.modifiers['PUrP_BuildVol_ArrayY'].count = 3
        context.object.modifiers['PUrP_BuildVol_ArrayZ'].count = 3

        # headline.select_set(True)
        context.view_layer.objects.active = headline

    def slide15(self, context):
        self.cleanscene(context)
        self.viewloc = (5, -21, 8)
        self.viewrot = (0.75, 0.6565, 0.0325, 0.0262)
        self.viewdistance = 20
        self.set_view(context, self.viewloc, self.viewrot, self.viewdistance)

        self.set_slidenum(15)
        self.label.text = "Last thoughts"
        self.linebreak(
            "Before I let you go explore more on your own here are some things to keep in mind to have everything working nicely as intended:%- The objects you are using must be manifold (water tight). A single plane will not work. It needs thickness. Also enable the 3D Printing addon shipped with blender. It allows to check 'how manifold' (and pregnant) your object is and often repairs it (not the pregnancy).%-Some Planar types produce problems with too large oversize values due to self intersection. The 'Exact' solver will often completly delete the object during applying. Changing the solver to 'Fast' will maybe solve this problem. However,the bad geometrie will still be transfered to your model during applying and may cause problmes during printing %- The addon is strongly reliant on blender's boolean modifier. With the 2.91 update the exact solver arrived and the number of fails drastically decreased. However, sometimes the boolean modifier just produce s***. In these cases increasing or reducing resolution and repositioning might help. %- All other modifiers must be applied before starting to apply the Connector. Keep in mind the addon ignores all modifiers that it hasn't created itself. When you have a large stack of modifiers before (or just one) before you start cutting, the preview before and the result after applying the connector will look not as expected. %- Always also consider the orientation during printing. Overhangs are always a problem in fdm printing. In addition, also the x-y-resolution is different than in z-direction. Good cut design can lead to less overhangs and better results. However, the oversize might change when the orientation during printing changes (seen in rare cases where it needs to be really precise).% I guess it's obvious, but let me make sure everyone understands: we are cuttings things in pieces with this addon. If this model is the only version you have and you save the cut model over the only original, that's it! The model is gone. The addon does not make any safety copies. Please keep your head together. :-)%Useful Detail: Have Fun and create great things!!!")
        headline = self.add_text(
            context, (self.headloc[0], self.headloc[1], self.headloc[2]+12), "Last thoughts\n\nHave Fun and \nCreate Great Things")
        headline.rotation_euler[0] = 1.507
        headline.scale = (5, 5, 5)

        # [page3?]
        # headline.select_set(True)
        context.view_layer.objects.active = headline
