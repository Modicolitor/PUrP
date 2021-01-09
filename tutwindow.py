import bpy

from bpy.types import Operator


from .tutwindowengine import *
# from .tutwindowengine import BL_UI_OT_draw_operator


class BE_OT_Draw_Operator(BL_UI_OT_draw_operator):

    bl_idname = "purp.window_draw_operator"
    bl_label = "bl ui widgets custom operator"
    bl_description = "Demo operator for bl ui widgets"
    bl_options = {'REGISTER'}

    def __init__(self):

        super().__init__()
        self.TutorialCounter = 0
        self.panel = BL_UI_Drag_Panel(400, 300, 500, 600)
        self.panel.bg_color = (0.2, 0.2, 0.2, 0.9)
        # self.panel.mouse_move(-30, -100)

        self.label = BL_UI_Label(20, 10, 100, 15)
        self.label.text = "Welcome"
        self.label.text_size = 20
        self.label.text_color = (0.2, 0.9, 0.9, 1.0)

        '''
        self.slider = BL_UI_Slider(20, 50, 260, 30)
        self.slider.color = (0.2, 0.8, 0.8, 0.8)
        self.slider.hover_color = (0.2, 0.9, 0.9, 1.0)
        self.slider.min = 1.0
        self.slider.max = 5.0
        self.slider.set_value(2.0)
        self.slider.decimals = 1
        self.slider.show_min_max = True
        self.slider.set_value_change(self.on_slider_value_change)
        '''
        self.main_text = BL_UI_Label(20, 162, 40, 15)
        self.main_text.text = "This little tutorial is designed to get you started. If you need a more detailed description try the documentation under PUrP.modicolitor.com"
        self.main_text.text_size = 14

        self.button1 = BL_UI_Button(20, 500, 120, 30)
        self.button1.bg_color = (0.2, 0.8, 0.8, 0.8)
        self.button1.hover_bg_color = (0.2, 0.9, 0.9, 1.0)
        self.button1.text = "Back"
        # self.button1.set_image("//img/scale_24.png")
        # self.button1.set_image_size((24,24))
        # self.button1.set_image_position((4, 2))
        self.button1.set_mouse_down(self.button1_press)

        self.button2 = BL_UI_Button(350, 500, 120, 30)
        self.button2.bg_color = (0.2, 0.8, 0.8, 0.8)
        self.button2.hover_bg_color = (0.2, 0.9, 0.9, 1.0)
        self.button2.text = "Next"
        # self.button2.set_image("//img/rotate.png")
        # self.button2.set_image_size((24, 24))
        # elf.button2.set_image_position((4, 2))
        self.button2.set_mouse_down(self.button2_press)
        '''
        self.up_down = BL_UI_Up_Down(120, 165)
        self.up_down.color = (0.2, 0.8, 0.8, 0.8)
        self.up_down.hover_color = (0.2, 0.9, 0.9, 1.0)
        self.up_down.min = 1.0
        self.up_down.max = 5.0
        self.up_down.decimals = 0

        self.up_down.set_value(3.0)
        self.up_down.set_value_change(self.on_up_down_value_change)

        self.chb_visibility = BL_UI_Checkbox(20, 210, 100, 15)
        self.chb_visibility.text = "Active visible"
        self.chb_visibility.text_size = 14
        self.chb_visibility.text_color = (0.2, 0.9, 0.9, 1.0)
        self.chb_visibility.is_checked = True
        self.chb_visibility.set_state_changed(
            self.on_chb_visibility_state_change)

        self.chb_1 = BL_UI_Checkbox(20, 235, 100, 15)
        self.chb_1.text = "Checkbox 2"
        self.chb_1.text_size = 14
        self.chb_1.text_color = (0.2, 0.9, 0.9, 1.0)

        self.chb_2 = BL_UI_Checkbox(20, 260, 100, 15)
        self.chb_2.text = "Checkbox 3"
        self.chb_2.text_size = 14
        self.chb_2.text_color = (0.2, 0.9, 0.9, 1.0)
        '''

    def on_invoke(self, context, event):
        if "PuzzleUrPrint" not in bpy.data.collections:
            bpy.ops.purp.init()
        # self.initialzeviaTutorial(context)
        # Add new widgets here (TODO: perhaps a better, more automated solution?)
        widgets_panel = [self.label, self.main_text,
                         self.button1, self.button2]
        widgets = [self.panel]

        widgets += widgets_panel

        self.init_widgets(context, widgets)

        self.panel.add_widgets(widgets_panel)

        # Open the panel at the mouse location
        self.panel.set_location(event.mouse_x,
                                context.area.height - event.mouse_y + 20)
        self.context = context

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

    def initialzeviaTutorial(self, context):
        if "PuzzleUrPrint" in data.collections:
            pass

    def pageturner(self, context):
        if self.TutorialCounter == 1:
            self.slide01(context)
        elif self.TutorialCounter == 2:
            self.slide02(context)
        else:
            self.TutorialCounter = 0

    def slide01(self, context):
        print('Learn what')
        self.label.text = "What does the addon do?"
        self.main_text.text = "It helps to cut models in pieces and simutansouly add conntectors for simple reassambling after 3D Printing."

    def slide02(self, context):
        print('Learn what')
        self.label.text = "First Contact"
        self.main_text.text = "This is one example of a connector. "

        bpy.ops.mesh.primitive_cube_add(
            size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

        PUrP = context.scene.PUrP
        PUrP.CoupScale = 1
        PUrP.SingleCouplingModes = '1'
        PUrP.SingleMainTypes = '1'
        PUrP.SingleCouplingTypes = '1'

        bpy.ops.add.coup()
