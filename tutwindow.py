import bpy

from bpy.types import Operator
import copy
from mathutils import Vector
from .bun import deselectall, is_coup, applyScale, applySingleCoup


from .tutwindowengine import *
# from .tutwindowengine import BL_UI_OT_draw_operator


class BE_OT_Draw_Operator(BL_UI_OT_draw_operator):
    '''Brings you to Tutorialland of PuzzleUrPrint. A distant world, one Blender Scene away, where you'll learn how to use the addon Puzzle your Print'''
    bl_idname = "purp.window_draw_operator"
    bl_label = "Start Tutorial"
    bl_description = "Brings you to Tutorialland. A distant World, one whole Blender Scene away, where you'll learn how to use the addon 'Puzzle your Print'"
    bl_options = {'REGISTER'}

    def __init__(self):

        super().__init__()
        self.TutorialCounter = 0
        self.panel = BL_UI_Drag_Panel(0, 0, 500, 600)  # 400 200
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

        self.slidenum = BL_UI_Label(200, 550, 100, 15)
        self.set_slidenum(99)
        self.slidenum.text_size = 20
        self.slidenum.text_color = (0.2, 0.9, 0.9, 1.0)

        self.button1 = BL_UI_Button(20, 550, 120, 30)
        self.button1.bg_color = (0.2, 0.8, 0.8, 0.8)
        self.button1.hover_bg_color = (0.2, 0.9, 0.9, 1.0)
        self.button1.text = "Back"
        self.button1.set_mouse_down(self.button1_press)

        self.button2 = BL_UI_Button(350, 550, 120, 30)
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
        print(
            f" width {context.area.width} height {context.area.height} event.mouse_x {event.mouse_x} event.mouse_y {event.mouse_y} ")
        self.panel.set_location(event.mouse_x - context.area.height/30,  # context.area.width -
                                -context.area.height/4)  # context.area.height - event.mouse_y
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

    def add_planar(self, context, loc, ConnectorScale, zScale, Oversize, ViewPortVis, PlanarCouplingTypes, OffsetRight, OffsetLeft, LineCount, LineLength, StopperHeight, StopperBool, KeepCoup, AddUnmapped):
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
        objs = bpy.data.scenes['PUrPTutorial'].objects
        bpy.ops.object.delete({"selected_objects": objs})

    def applycoup(self, context, coups):
        # deselectall(context)
        for coup in coups:
            applySingleCoup(context, coup, coup.parent, True)
            # coup.select_set(True)

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
        print(self.TutorialCounter)
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
        self.viewloc = (-5, 21, -2)
        self.viewrot = (0.75, 0.6565, 0.0325, 0.0262)
        self.viewdistance = 10
        self.set_view(context, self.viewloc, self.viewrot, self.viewdistance)
        self.set_slidenum(0)
        self.label.text = "Welcome to the Tutorial"
        self.headloc = Vector((0, 0, 5))
        self.headlinescale = Vector((3, 3, 3))
        self.linebreak(
            "This little tutorial is designed to get you started. If you need a more detailed description try the documentation under PUrP.modicolitor.com.%% BTW, If you think 'This guy just deleted my work.', don't worry. We are in a new scene, when you close the Tutorial you'll get back to your original scene.%% This interactive Tutorial will generate new objects to show you what the addon is capable off. Be encouraged to play with the objects and settings in the scene. However, don't be sad when you go to another slide or out of the Tutorial and everything is gone :-D.")
        headline = self.add_text(
            context, self.headloc, "Welcome to the Tutorial")
        headline.rotation_euler[0] = 1.507
        cubeloc = Vector((0, 0, 0))
        Cube = self.add_primitive(context, cubeloc, 'Cube')
        Cube.scale = Vector((4, 4, 4))
        con1 = self.add_single(context, cubeloc, 1, 1, '2', True,
                               '1',  16, '1', 1.5, 0.04, 16, 0, 0, 1, 1, False)

        self.focus(context, self.tutorialscene.objects)
        deselectall(context)

    def slide01(self, context):
        self.cleanscene(context)
        self.set_slidenum(1)
        self.label.text = "What does the addon do?"
        self.linebreak(
            "The addon helps to cut models in pieces and simutansouly add connectors for simple reassambling after 3D Printing. Here you see a Cube with a 'Single Connector' in male-female configuration with Cube as Inlay type.... Lets see how it looks after applying%%% Press Next")
        headline = self.add_text(
            context, self.headloc, "What does the addon do?")
        headline.rotation_euler[0] = 1.507
        cubeloc = Vector((0, 0, 0))
        Cube = self.add_primitive(context, cubeloc, 'Cube')
        Cube.scale = Vector((4, 4, 4))
        con1 = self.add_single(context, cubeloc, 1, 1, '2',  True,
                               '1',  16, '1', 1.5, 0.04, 16, 0, 0, 1, 1, False)
        # self.applyallscene(context)
        self.focus(context, self.tutorialscene.objects)
        deselectall(context)
        self.focus(context, self.tutorialscene.objects)

    def slide02(self, context):
        self.cleanscene(context)
        self.set_slidenum(2)
        self.label.text = "The Result"
        self.linebreak("This is the result you would when you apply the connector from the last slide to the cube. The cube is now cut in half. Moreover, the bottom part has a male connector attached while the top part has a hole in the shape of the connector. If you would print that you could put both parts together again easily. This can be helpful for many things.%% - Print large: 3D-Printers are typically very small. Desect large models into printable bits. Your lifesized Koro is only a few clicks and days of printing away (support cloud.blender.org!!) % - Add Functionality: Using cylinders as Inlays allows to turn parts against each other. A 'joint'-cut allows to make maken even more delicate joints.  Print your own actionfigure, monster, sculpture,... with movable parts.% -PUZZLES: Of course you can make puzzles with PuzzleyourPrint. Play with the thickness of the parts (for example sculpt a pictures). It'll change the whole experience. %- Wallholders and Fixation: You can add Dovetail and other shapes to make objects slie into each other and if you like stop at the right point. This is ideal for wall holders where you wanne hide the screws. ")

        headline = self.add_text(context, self.headloc, "The Result")
        headline.rotation_euler[0] = 1.507
        cubeloc = Vector((0, 0, 0))
        Cube = self.add_primitive(context, cubeloc, 'Cube')
        Cube.scale = Vector((4, 4, 4))
        Cube.name = 'PUrPCube'
        con1 = self.add_single(context, cubeloc, 1, 1, '2',  True,
                               '1',  16, '1', 1.5, 0.04, 16, 0, 0, 1, 1, False)

        self.applycoup(context, [con1])
        self.tutorialscene.objects['PUrPCube'].location[2] = -4

        # self.applyallscene(context)
        self.focus(context, self.tutorialscene.objects)
# diversity

    def slide03(self, context):
        self.cleanscene(context)
        self.set_slidenum(3)
        self.label.text = "Many Connectors shapes: Settings"
        self.linebreak("Here you see a couple of examples of connectors. They can have all kinds of shapes and produce different functionalities. Quiet divers, right.% You can produce all of these connectors by adjusting the settings in the 'Add, Exchange, Apply'-dropdown. With 'Add Connector' a new connector will be born using the current settings in the 'Add, Exchange, Apply'-dropdown. If you haven't specified another (mesh) object by selecting it or another connector is selected, the addon will try to map (something like parenting) the connector to the last known 'Center Object'. This is the object set in the top line in 'Add,Exhange,Apply'.%You can change the settings via the 'Add, Exchange, Apply'-dropdown or via the gizmos visible when a connector is selected. While changing settings via gizmot will take immediate effect on mesh and setting in the dropdown, changes in the 'Add, Exchange, Apply'-dropdown will only take effect after pressing the 'Exchange'-Button. %% If your are interested to know which settings produced a specific connector, select the connector of intrest and press 'Active to Settings' in the 'Add, Exchange, Apply'-dropdown. The dropdown now shows the settings of the active connector. You can 'past' these new settings onto an existing connector by selecting it and press 'Exchange'.%%Useful Detail: I just switched off 'Add with Viewport Visibility'. Althoug, it might be nice to see the preview of the bool modifier already cutting a part, it makes working extremly slow. You can also toggle the visibility on/off by pressing 'Toggle Modifier Visibility' in the 'Mapping Order,Visibility'-dropdown")

        self.viewloc = (-5, 21, -2)
        self.viewrot = (0.75, 0.6565, 0.0325, 0.0262)
        self.viewdistance = 20
        self.set_view(context, self.viewloc, self.viewrot, self.viewdistance)

        headline = self.add_text(
            context, self.headloc, "A Large Variety of Options")
        headline.rotation_euler[0] = 1.507
        headline.scale = (5, 5, 5)
        # singleconnectors
        singloc = Vector((-10, -10, 0))
        singletext = self.add_text(context, singloc, "Single Connectors")
        singletext.scale = Vector((2.3, 2.3, 2.3))
        # cube
        cube1loc = Vector((-5, 0, 0))
        Cube1 = self.add_primitive(context, cube1loc, 'Cube')
        Cube1.scale = Vector((3, 3, 3))
        con1 = self.add_single(context, cube1loc, 1, 1, '2', False,
                               '1',  16, '1', 1.5, 0.04, 16, 0, 0, False, False, False)
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

        # flat
        sphereloc = Vector((-20, 10, 0))
        self.add_primitive(context, sphereloc, 'Sphere')
        self.add_single(context, sphereloc, 1.5, 1, '3', False,
                        '1', 16, '1', 2, 0.4, 16, 0, 1, 1, 1, False)
        # cone
        coneloc = Vector((-5, 10, 0))
        cube = self.add_primitive(context, coneloc, 'Cube')
        cube.scale = Vector((3, 3, 3))
        self.add_single(context, coneloc, 1, 0.5, '2', False,
                        '2', 16, '2', 2, 0.4, 16, 0, 1, 1, 0.3, False)

        # triangle
        # flat
        sphereloc = Vector((-20, 20, 0))
        self.add_primitive(context, sphereloc, 'Sphere')
        self.add_single(context, sphereloc, 1.5, 1, '3', False,
                        '1', 16, '1', 2, 0.4, 16, 0, 1, 1, 1, False)
        # Triangle
        coneloc = Vector((-5, 20, 0))
        cube = self.add_primitive(context, coneloc, 'Cube')
        cube.scale = Vector((3, 3, 3))
        self.add_single(context, coneloc, 1, 1, '1', False,
                        '1', 3, '2', 0.5, 0.04, 5, 0, 1, 1, 0.5, False)
        # planar
        planaloc = Vector((20, -10, 0))
        planartext = self.add_text(context, planaloc, "Planar Connectors")
        planartext.scale = Vector((1.75, 1.75, 1.75))
        # puzzle
        largeplaneloc = Vector((10, 0, 0))
        largeplanep = self.add_primitive(context, largeplaneloc, 'Cube')
        largeplanep.scale = Vector((10, 10, 0.2))
        puzzle1 = self.add_planar(
            context, Vector((5, -5, 1)), 0.5, 1, 0.04, False, '4', 2, 2, 3, 3, 1, False, False, False)
        puzzle2 = self.add_planar(
            context, Vector((14, -5, 1)), 0.5, 1, 0.04,  False, '5', 2, 2, 3, 3, 5, False, False, False)
        puzzle2.rotation_euler[2] = 1.5708

        # cube with stopper
        cubestopperloc = Vector((27, 0, 0))
        cubestopper = self.add_primitive(context, cubestopperloc, 'Cube')
        cubestopper.scale = Vector((5, 3, 3))
        plancol = self.add_planar(
            context, Vector(
                (27, 0, 2)), 1, 3, 0.04,  False, '2', 1.2, 1.2, 1, 1, 3, True, False, False)

        # planar collection without stopper
        largeplaneloc = Vector((10, 32, 0))
        largeplane1 = self.add_primitive(context, largeplaneloc, 'Cube')
        largeplane1.scale = Vector((15, 48, 1))
        type = 1
        plancolloc = Vector((4, 10, 1))
        while type <= 16:

            plancol = self.add_planar(
                context, plancolloc, 1, 1, 0.04, False, str(type), 1.2, 1.2, 1, 3, 5, False, False, False)
            plancolloc += Vector((0, 3, 0))
            type += 1
        # planar collection with stopper
        largeplaneloc = Vector((30, 32, 0))
        largeplane1 = self.add_primitive(context, largeplaneloc, 'Cube')
        largeplane1.scale = Vector((15, 48, 1))
        type = 1
        plancolloc = Vector((24.5, 10, 1))
        while type <= 16:
            plancol = self.add_planar(
                context, plancolloc, 1, 1, 0.04, False, str(type), 1.2, 1.2, 1, 3, 5, True, False, False)
            plancolloc += Vector((0, 3, 0))
            type += 1
        self.focus(context, self.tutorialscene.objects)
        deselectall(context)
# connector modes

    def slide04(self, context):
        self.cleanscene(context)
        self.set_slidenum(4)
        self.label.text = "Connector Modes"
        self.linebreak("There are 4 types of connector modes. %- Stick, %- Male-Female (mf)  %- Flat %- Planar %%We saw a mf-connector in the first example. After applying, one of the resulting objects will be male and one will be female (if you know what I mean...).%Stick mode will generate two female daughter objects and an additional 'Stick'-Object to connect both (if you know what I mean...). Having the stick as an additional part can be beneficial. You need to reprint less, when your oversize value is off. We'll talk about oversize later.%Flat is actually just a stupid plane. It cuts two things in half without any connector. Still can be useful if you want to glue stuff together anyway.%Plane is compared to the other modes a whole new world. Mathematically speaking (or was it geographically) the functionallity is here parallel to the maincut and not perpendicular like in the first two cases. Moreover, a planar can generate a large number of couplings with one object while the first two only produce one coupling. That's why I'll call the first 3 modes Stick, MF and Flat  (yeah, I know flat doesn't...bla) Single Connector Modes and the other is planar .... for consistency ... you'll get it... later... maybe.")
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
                               '1',  16, '1', 1.5, 0.04, 16, 0, 0, False, False, False)
        # Male-Female
        singloc = Vector((-5, -10, 0))
        singletext = self.add_text(context, singloc, "Male-Female")
        singletext.scale = Vector((2.3, 2.3, 2.3))
        # cube
        cube1loc = Vector((-5, 0, 0))
        Cube1 = self.add_primitive(context, cube1loc, 'Cube')
        Cube1.scale = Vector((3, 3, 3))
        con1 = self.add_single(context, cube1loc, 1, 1, '2', False,
                               '1',  16, '1', 1.5, 0.04, 16, 0, 0, False, False, False)

        # Flat
        singloc = Vector((5, -10, 0))
        singletext = self.add_text(context, singloc, "Flat")
        singletext.scale = Vector((2.3, 2.3, 2.3))
        # cube
        cube1loc = Vector((5, 0, 0))
        Cube1 = self.add_primitive(context, cube1loc, 'Cube')
        Cube1.scale = Vector((3, 3, 3))
        con1 = self.add_single(context, cube1loc, 1, 1, '3', False,
                               '1',  16, '1', 1.5, 0.04, 16, 0, 0, False, False, False)

        # planar
        singloc = Vector((15, -10, 0))
        singletext = self.add_text(context, singloc, "Planar")
        singletext.scale = Vector((2.3, 2.3, 2.3))
        # cube
        cube1loc = Vector((15, 0, 0))
        Cube1 = self.add_primitive(context, cube1loc, 'Cube')
        Cube1.scale = Vector((3, 3, 3))
        planar = self.add_planar(
            context, Vector((15, 0, 2)), 0.5, 4, 0.04, False, '4', 2, 2, 1, 1, 1, False, False, False)
# Single Connectors

    def slide05(self, context):
        self.cleanscene(context)
        self.set_slidenum(5)
        self.label.text = "Single Connectors"
        self.linebreak(
            "Single Connectors consist of one maincut and two inlay objects.%%The maincut causes the initial seperation of the object in two parts. You can choose the maincut type to be Flat or Joint. The Flat type is only a plane with a solidify modifier. It creates a flat base cut. However, the Joint type produces a circular ... joint cut (Please mail better terms) useful for example for ellbows of your actionfigure. It is not forbiden to enter edit mode and change the shape to your liking. In most cases also 'Exchange' will not replace your adjusted maincut. %%The inlay shapes can be either cube, cylinder or cone. I forbit selecting them. Believe me, you'll mess it up. Use the panel or the Gizmos to change them. It's better for all of us. They are parented to the maincut anyway. So only use them to transform the connector. Depending on the chosen Inlay Type additional settings might become available. For example cylinders have additional settings to adjust the vertcount and radius, for cone you can set the upper and lower radius individually. However, also consider that some configuration will not make sense. For example a cone in stick configuration will not be  However, they also have a lot of parameters in comon. Lets talk about them in the next part together with the gizmos system.%%%Useful Detail: You might get the error 'This connector didn't cut through'! Is this really what you want?'. Then you might Undo and check which coupling might needs repositioning. ")
        headline = self.add_text(context, self.headloc, "Single Connectors")
        headline.rotation_euler[0] = 1.507
        headline.scale = (5, 5, 5)
        # [[flat [as text], joint [as text],] [flat mf (cube) (cylinder) (Cone)]

    def slide06(self, context):
        self.cleanscene(context)
        self.set_slidenum(6)
        self.label.text = "Single Connector Gizmos"
        self.linebreak(
            "When you select an object some colorful symbols appear around the connecotor (only avaiable when the addon is installed and initalized). These are controls to change several settings and, hence, the appearance of the connector.%% From bottom to top:%- The two at the bottom control the maincut: the ring for the Connector Scale, the other for the Maincut Thickness (should be in the range of the oversize).%- The big blue cube controlls the Inlay Size%-the light blue controlls the oversize (see later!!)%- The Corner shapes represent controls over the Beveling, the large one is the Beveloffset and the small one the Bevelsegments (only visible when Beveloffset is not zero).%-The Red UP Arrow represents the zScale with which you can stretch the inlay along (local) z-axis.%-Cone type has additional two controls for upper and lower radius (import cone with radius top higher then 0 too have control over the top via gizmos)%%In addition, using any Gizmos will also change the settings in the panel too. This can also allow to figure out, what (the heck) 'this' gizmo does.%%%Useful detail: If muscle memory made you scale the connector with the blender typical 's'-shortcut, its' not a big deal. However, just click shortly green ring at the bottom (connector scale) to have the scale of all object back to (1,1,1) (important for Oversize calculations, see later)")
        headline = self.add_text(
            context, self.headloc, "Single Connector Gizmos")
        headline.rotation_euler[0] = 1.507
        # [[flat [as text], joint [as text],] [flat mf (cube) (cylinder) (Cone)]

    def slide07(self, context):
        self.cleanscene(context)
        self.set_slidenum(7)
        self.label.text = "Planar Connectors "
        self.linebreak(
            "Planar connectors are essentially a plane with a coupling element and two array modifiers two duplicate it. In this version 16 different connector types (shapes) are avaiable: cubic, dovetail, different puzzle shapes, arrow, t-shape,... . Try out what fits for your project (recommendations for additional shapes welcome)   One Array duplicates allong the line, called Linelength. The other Array generates copies of the original lines with Linecount beeing the number of lines and the Linedistance between those lines. Together with the Oversize, these 4 settings can be also changed via the 4 Gizmos in the corners of a plane. BTW: You can keep the mouse on the gizmos to get small definition what it does. Additionally you'll find 3 Arrow shaped gizmos: the left and right arrows control the Right- and Left Offset. This is the distance between the coupling element and the end of a repeating unit. Maybe reduce the 'Linelength' to 1 to get a clearer understand of what they do.%%A Subclass of Planar are called Planar with Stopper ...if you like. In this configuration the coupling parts ends somewhere in the middle of the plane and the rest is only a flat cut. Get one by activating the 'Stopper' checkbox and add or Exchange a connector. Models printed with this will not fall through like a puzzle piece but will be stopped at the right height when putting together. This is ideal for example to make wallholders with replaceable parts, canvases, guitars,.... where ever you need the pieces slide into each other and stay where they are supposed to. When you have Stopper activated, you'll see the setting Stopper Height and when its in the connector also in the Gizmos as a down arrow.")
        headline = self.add_text(context, self.headloc, "Planar Connectors")
        headline.rotation_euler[0] = 1.507
        # [center planar, planar with stopper je mit text (im Hintergrund overview von seite 3)]

    def slide08(self, context):
        self.cleanscene(context)
        self.set_slidenum(8)
        self.label.text = "Positioning and Scaling"
        self.linebreak(
            "You can move and rotate the connectors as you like to find the right position using for example the typical Blender shortcuts 'r' and 'g'. Scaling with shortcut 's' is critical because you change the scaling of the object. Better use the Connectorscale Gizmo (green large ring) to scale. If it is more convenient for you to use 's' at least click the 'Connector Scale' - Gizmo once. It will correct the scaling and will make the Oversize be consistent over all connectors. Again this oversize term. Next we'll get to it.%%%Useful Detail: All values in the addon are multiplied by the GlobalScale. The size of connectors, the oversize, the build volume, even the sensitivity of the gizmos. Typically, exporting formats like *.stl interpret size different to blender resulting in a need to scale up the models in the slicing software. Naturally, we start working in larger dimensions in Blender. Adjust the Globalscale to compensate. For example, a Globalscale of 10 allows to work nicely when blender meter translate to mm in reality (without scaling in the slicer or during blender export), which is the normal behavior of an stl beeing imported into Cura.")
        headline = self.add_text(
            context, self.headloc, "Positioning and Scaling")
        headline.rotation_euler[0] = 1.507
        # [figure + one connector, and half done puzzle (make a Puzzle)]

    def slide09(self, context):
        self.cleanscene(context)
        self.set_slidenum(9)
        self.label.text = "Oversize"
        self.linebreak(
            "The oversize setting allows to compensate for printing inaccuracies.%We all know it: 3D printing is a wonderful thing but not really exact. Typically, a 3D printed part is a bit larger than you actually tell it to be. For FDM (fuse depositon molding) printers, this comes for example from smearing material a bit over the side while following printing path. Also the shape of an object and as a result the path the printer takes, will have an influence on the oversize. Try printing two walls connected in a 90° angle. Especially, with high printing velocities you'll see thickening add the outside of the corner. Of course, also nozzle size, problems with overhanging parts, brim, orientation of the part... the number of influencing parameters is large why it is unfortunately hard to give a perfect recommendation for all cases. However, the oversize is the option to compensate for all those parameters. Keep in mind, that the oversize is an absolut value. When the printers oversize 0.4 mm for a small object, your print has the same oversize for a bigger object. On the one hand this means the connector can have the same oversize despite their size. On the other hand your PUrP Oversize might get wrong when scalling object later (e.g. in the slicer software).%% Useful Detail: Here are typicall parameter:% Nozzle 0.8 mm blender meter to cm, oversize 0.03.%% But I really recommand to print small test pieces with different oversize values until you figure out the best values for your 3D Printer.")
        headline = self.add_text(context, self.headloc, "Oversize")
        headline.rotation_euler[0] = 1.507
        # [Cube, Cylinder, joint, planar mit objecten, text (play with the oversize) ]

    def slide10(self, context):
        self.cleanscene(context)
        self.set_slidenum(10)
        self.label.text = "Mapping"
        self.linebreak(
            "Mapping is the way a connector are bound to the object they are supposed to cut (Centerobject). It includes parenting. When you move the object in the viewport the connectors will follow. Moreover, mapping also includes having the boolean modifiers of a connectors already on the Centerobj allowing to preview the result (when you can work with a slow blender). The addon will check for these attributes during applying.% However, you can change the mapping of a connector by using the 'Remap Connector to Active'-Button. Select the connector you wane remap and then the new Centerobject it should be mapped to and press the 'Remap Connector to Active'-Button. Now the parenting and the modifiers exist on the other object.%Moreover, if you don't wanne have a connector mapped to any object, you can either add them with the checkbox 'Add Unmapped' in the 'Add, Exchange,...'- dropdown enabled or you select an existing connector and press 'Unmap Connector' in the 'Mapping, Order, Visibility' -dropdown.%%Useful Detail: If a mapped connector doesn't touch/cut any part of a Centerobject during applying (for example Apply All). It will remain in the scene and will be labeled unmapped.")
        headline = self.add_text(context, self.headloc, "Mapping")
        headline.rotation_euler[0] = 1.507
        # [high cube 3 connectors, apply the one in the middle, check the mapping of the new objects, remap one connector]

    def slide11(self, context):
        self.cleanscene(context)
        self.set_slidenum(11)
        self.label.text = "Applying and Order"
        self.linebreak(
            "By Applying a Connector you finalize the editing process, cut the model in pieces and add the connectors. You can choose to select one or several connectors and Press 'Apply Connectors(s)' to have only specific connectors applied or you press 'Apply All' (both in 'Add,Exchange,Apply'-dropdown) to apply all connectors mapped to a Centerobject (or the Centerobj the selected Connector is mapped to).%The order in which the Connectors are applied can be displayed as little numbers above the Connectors by  Toggling on/off with 'Toggle Order' in the 'Mapping,Order,Visibility'-dropdown. The order can be changed by selecting a connector and pressing either 'Up in Order' or 'Down in Order'. The order rarely is necessary but in an example like here on the right it can be important.%%Useful Detail: By default the connectors are getting deleted after applying. If they are precious to you check the checkbox 'Keep Connector' before applying and they will be kept unmapped.")
        headline = self.add_text(context, self.headloc, "Applying and Order")
        headline.rotation_euler[0] = 1.507
        # 3x[one cube with two planar and a single] with different order

    def slide12(self, context):
        self.cleanscene(context)
        self.set_slidenum(12)
        self.label.text = "Special Apply Menu"
        self.linebreak(
            "The 'Special Apply'-dropdown has some extra operations that might get helpful:%- 'Planar To Multiple Objects' allows you to decide which objects are also should be cut through in addition to the Centerobject the planar is mapped to. For example (left) you make a puzzle and applied only the first planar, the second will be only applied to the one row its mapped to. Select all rows first and select the remaining planar last. Then Press  Planar To Multiple Objects'. BTW: 'Apply All' will do this automatically. %- 'Multiple Planar to Object' does it the other way around. Select several Planar Connector, select the Centerobj of choice last and press the button. This is a bit of a relict from where 'Apply All' was'nt smart enough, but it might become helpful in some configurations. %- 'Single To Multiple Objects' This allows to connect one Single Connector beeing applied to several Objects. Imagine your character needs a new hat. Select the hat and the charakter and the Single Connector last and press 'Single To Multiple Objects'. You can also enable 'Ignore Main Cut' to do exactly that during applying.")
        headline = self.add_text(context, self.headloc, "Special Apply Menu")
        headline.rotation_euler[0] = 1.507
        # [Puzzle with one applied(Cube with planar and single, single applied)[text: Planar to Multiple Objects], PUzzle both unapplied,  figure + Head ]

    def slide13(self, context):
        self.cleanscene(context)
        self.set_slidenum(13)
        self.label.text = "BuildVolume"
        self.linebreak(
            "Especially when you desect large objects to fit in your 3D printer, you always need to know how big your print real estate is at all times. In the 'Build Volume'-Dropdown, you can set the size of your 3D printer in cm (probably if you haven't changed it globaly to freedom units) and press 'Generate Buildvolume' to get cube (set to wireframe). When added you can adjust also its repeation in x,y and z. You can at as many as you like. The settings will only be avaiable for the last selected Build Volume. The BuildVolumes are nothing more than simple objects to get a feel for the avaiable space. Otherwise they do nothing.")
        headline = self.add_text(context, self.headloc, "BuildVolume")
        headline.rotation_euler[0] = 1.507
        # [Figure with connector, Buildvolume with 2x2x4 ]

    def slide14(self, context):
        self.cleanscene(context)
        self.set_slidenum(14)
        self.label.text = "Typical Process"
        self.linebreak(
            "Here is a typical workflow too work with the addon:%1. Import/append model (keep backup)%2. Select the model%3. Set the 3d cursor to a point where you want to add a connector. Press Add Connector,%4. Adjust settings, exchange, position with 's' and 'r'-shortcuts, fine tune with the gizmos...%5. Repeat to add more connectors as you like, use 'Active to Setting' and 'Exchange' as copy and paste of connector settings.%[6-53]. ...%54. Maybe print a few test cuts to figure out the best oversize value and adjust the connectors accordingly.%55. Adjust all Oversize values according to you test results%56. Apply All Connectors or do it manually one by one%57. 3D Print %58. PUZZLE THEM TOGHETHER  %%Let Blender be your canvas and make cool stuff. Please send me pics, models and suggestions to info@modicolitor.com")
        headline = self.add_text(context, self.headloc, "Typical Process")
        headline.rotation_euler[0] = 1.507
        #[Figure + Buildvolume]

    def slide15(self, context):
        self.cleanscene(context)
        self.set_slidenum(15)
        self.label.text = "Last thoughts "
        self.linebreak(
            "Before I let you go explore more on your own here are somethings to keep in mind to have everything working nicely as intended:%- The objects you are using must be manifold (water tight). A single plane will not work. It needs thickness. Also enable the 3D Printing addon shiped with blender it allows to check 'how manifold' (and pregnant) your object is and often repairs it. %- The addon is strongly reliant (abh) on blenders boolean modifier. With the 2.91 update the exact solver arrived and the number of fails drastically decreased. However, sometimes the boolean modifier just produce s***. In these cases increasing or reducing resolution and repositioning might help. %- All other modifiers must be applied before starting to apply the Connector. Keep in mind the Addon ignores all modifiers not created by itself. When you have a large stack of modifiers before (or just one) before you start cutting, the preview before and the result after applying the connector will look not as expected. %- Always also consider the orientation during printing. Overhangs are always a problem in fdm printing. In addition, also the x-y-resolution is different than in z-direction. Good cut design can lead to less overhangs and better results. However, the oversize might change when the orientation during printing changes (seen in rare cases where it needs to be really precise).% I guess it's obvious, but let me make sure everyone understands: we are cuttings things in pieces with this addon. When this model is the only version you have and you save the cutted model over the only original, that's it! The model is gone. The addon does not make any safety copies. Please keep your heads together. :-) %%Useful Detail: Have Fun!!!")
        headline = self.add_text(context, self.headloc, "Last thoughts ")
        headline.rotation_euler[0] = 1.507
        # [page3?]
