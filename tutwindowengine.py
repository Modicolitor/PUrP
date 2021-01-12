from bpy.types import Operator
#from . bl_ui_widget import *

import blf
import bpy
import gpu
import bgl

from gpu_extras.batch import batch_for_shader


class BL_UI_Widget:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.x_screen = x
        self.y_screen = y
        self.width = width
        self.height = height
        self._bg_color = (0.8, 0.8, 0.8, 1.0)
        self._tag = None
        self.context = None
        self.__inrect = False
        self._mouse_down = False
        self._is_visible = True

    def set_location(self, x, y):
        self.x = x
        self.y = y
        self.x_screen = x
        self.y_screen = y
        self.update(x, y)

    @property
    def bg_color(self):
        return self._bg_color

    @bg_color.setter
    def bg_color(self, value):
        self._bg_color = value

    @property
    def visible(self):
        return self._is_visible

    @visible.setter
    def visible(self, value):
        self._is_visible = value

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, value):
        self._tag = value

    def draw(self):
        if not self.visible:
            return

        self.shader.bind()
        self.shader.uniform_float("color", self._bg_color)

        bgl.glEnable(bgl.GL_BLEND)
        self.batch_panel.draw(self.shader)
        bgl.glDisable(bgl.GL_BLEND)

    def init(self, context):
        self.context = context
        self.update(self.x, self.y)

    def update(self, x, y):

        area_height = self.get_area_height()

        self.x_screen = x
        self.y_screen = y

        indices = ((0, 1, 2), (0, 2, 3))

        y_screen_flip = area_height - self.y_screen

        # bottom left, top left, top right, bottom right
        vertices = (
            (self.x_screen, y_screen_flip),
            (self.x_screen, y_screen_flip - self.height),
            (self.x_screen + self.width, y_screen_flip - self.height),
            (self.x_screen + self.width, y_screen_flip))

        self.shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
        self.batch_panel = batch_for_shader(
            self.shader, 'TRIS', {"pos": vertices}, indices=indices)

    def handle_event(self, event):
        x = event.mouse_region_x
        y = event.mouse_region_y

        if(event.type == 'LEFTMOUSE'):
            if(event.value == 'PRESS'):
                self._mouse_down = True
                return self.mouse_down(x, y)
            else:
                self._mouse_down = False
                self.mouse_up(x, y)

        elif(event.type == 'MOUSEMOVE'):
            self.mouse_move(x, y)

            inrect = self.is_in_rect(x, y)

            # we enter the rect
            if not self.__inrect and inrect:
                self.__inrect = True
                self.mouse_enter(event, x, y)

            # we are leaving the rect
            elif self.__inrect and not inrect:
                self.__inrect = False
                self.mouse_exit(event, x, y)

            return False

        elif event.value == 'PRESS' and (event.ascii != '' or event.type in self.get_input_keys()):
            return self.text_input(event)

        return False

    def get_input_keys(self):
        return []

    def get_area_height(self):
        return self.context.area.height

    def is_in_rect(self, x, y):
        area_height = self.get_area_height()

        widget_y = area_height - self.y_screen
        if (
            (self.x_screen <= x <= (self.x_screen + self.width)) and
            (widget_y >= y >= (widget_y - self.height))
        ):
            return True

        return False

    def text_input(self, event):
        return False

    def mouse_down(self, x, y):
        return self.is_in_rect(x, y)

    def mouse_up(self, x, y):
        pass

    def set_mouse_enter(self, mouse_enter_func):
        self.mouse_enter_func = mouse_enter_func

    def call_mouse_enter(self):
        try:
            if self.mouse_enter_func:
                self.mouse_enter_func(self)
        except:
            pass

    def mouse_enter(self, event, x, y):
        self.call_mouse_enter()

    def set_mouse_exit(self, mouse_exit_func):
        self.mouse_exit_func = mouse_exit_func

    def call_mouse_exit(self):
        try:
            if self.mouse_exit_func:
                self.mouse_exit_func(self)
        except:
            pass

    def mouse_exit(self, event, x, y):
        self.call_mouse_exit()

    def mouse_move(self, x, y):
        pass


class BL_UI_Button(BL_UI_Widget):

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self._text_color = (1.0, 1.0, 1.0, 1.0)
        self._hover_bg_color = (0.5, 0.5, 0.5, 1.0)
        self._select_bg_color = (0.7, 0.7, 0.7, 1.0)

        self._text = "Button"
        self._text_size = 16
        self._textpos = (x, y)

        self.__state = 0
        self.__image = None
        self.__image_size = (24, 24)
        self.__image_position = (4, 2)

    @property
    def text_color(self):
        return self._text_color

    @text_color.setter
    def text_color(self, value):
        self._text_color = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def text_size(self):
        return self._text_size

    @text_size.setter
    def text_size(self, value):
        self._text_size = value

    @property
    def hover_bg_color(self):
        return self._hover_bg_color

    @hover_bg_color.setter
    def hover_bg_color(self, value):
        self._hover_bg_color = value

    @property
    def select_bg_color(self):
        return self._select_bg_color

    @select_bg_color.setter
    def select_bg_color(self, value):
        self._select_bg_color = value

    def set_image_size(self, imgage_size):
        self.__image_size = imgage_size

    def set_image_position(self, image_position):
        self.__image_position = image_position

    def set_image(self, rel_filepath):
        try:
            self.__image = bpy.data.images.load(
                rel_filepath, check_existing=True)
            self.__image.gl_load()
        except:
            pass

    def update(self, x, y):
        super().update(x, y)
        self._textpos = [x, y]

    def draw(self):
        if not self.visible:
            return

        area_height = self.get_area_height()

        self.shader.bind()

        self.set_colors()

        bgl.glEnable(bgl.GL_BLEND)

        self.batch_panel.draw(self.shader)

        self.draw_image()

        bgl.glDisable(bgl.GL_BLEND)

        # Draw text
        self.draw_text(area_height)

    def set_colors(self):
        color = self._bg_color
        text_color = self._text_color

        # pressed
        if self.__state == 1:
            color = self._select_bg_color

        # hover
        elif self.__state == 2:
            color = self._hover_bg_color

        self.shader.uniform_float("color", color)

    def draw_text(self, area_height):
        blf.size(0, self._text_size, 72)
        size = blf.dimensions(0, self._text)

        textpos_y = area_height - \
            self._textpos[1] - (self.height + size[1]) / 2.0
        blf.position(
            0, self._textpos[0] + (self.width - size[0]) / 2.0, textpos_y + 1, 0)

        r, g, b, a = self._text_color
        blf.color(0, r, g, b, a)

        blf.draw(0, self._text)

    def draw_image(self):
        if self.__image is not None:
            try:
                y_screen_flip = self.get_area_height() - self.y_screen

                off_x, off_y = self.__image_position
                sx, sy = self.__image_size

                # bottom left, top left, top right, bottom right
                vertices = (
                    (self.x_screen + off_x, y_screen_flip - off_y),
                    (self.x_screen + off_x, y_screen_flip - sy - off_y),
                    (self.x_screen + off_x + sx,
                     y_screen_flip - sy - off_y),
                    (self.x_screen + off_x + sx, y_screen_flip - off_y))

                self.shader_img = gpu.shader.from_builtin('2D_IMAGE')
                self.batch_img = batch_for_shader(self.shader_img, 'TRI_FAN',
                                                  {"pos": vertices,
                                                   "texCoord": ((0, 1), (0, 0), (1, 0), (1, 1))
                                                   },)

                bgl.glActiveTexture(bgl.GL_TEXTURE0)
                bgl.glBindTexture(bgl.GL_TEXTURE_2D, self.__image.bindcode)

                self.shader_img.bind()
                self.shader_img.uniform_int("image", 0)
                self.batch_img.draw(self.shader_img)
                return True
            except:
                pass

        return False

    def set_mouse_down(self, mouse_down_func):
        self.mouse_down_func = mouse_down_func

    def mouse_down(self, x, y):
        if self.is_in_rect(x, y):
            self.__state = 1
            try:
                self.mouse_down_func(self)
            except:
                pass

            return True

        return False

    def mouse_move(self, x, y):
        if self.is_in_rect(x, y):
            if(self.__state != 1):

                # hover state
                self.__state = 2
        else:
            self.__state = 0

    def mouse_up(self, x, y):
        if self.is_in_rect(x, y):
            self.__state = 2
        else:
            self.__state = 0


#from . bl_ui_widget import *

#import blf
#import bpy

class BL_UI_Checkbox(BL_UI_Widget):

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self._text_color = (1.0, 1.0, 1.0, 1.0)
        self._box_color = (1.0, 1.0, 1.0, 1.0)
        self._cross_color = (0.2, 0.9, 0.9, 1.0)

        self._text = "Checkbox"
        self._text_size = 16
        self._textpos = [x, y]
        self.__boxsize = (16, 16)

        self.__state = False

    @property
    def text_color(self):
        return self._text_color

    @text_color.setter
    def text_color(self, value):
        self._text_color = value

    @property
    def cross_color(self):
        return self._cross_color

    @cross_color.setter
    def cross_color(self, value):
        self._cross_color = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def text_size(self):
        return self._text_size

    @text_size.setter
    def text_size(self, value):
        self._text_size = value

    @property
    def is_checked(self):
        return self.__state

    @is_checked.setter
    def is_checked(self, value):
        if value != self.__state:
            self.__state = value

            self.call_state_changed()

    def update(self, x, y):
        super().update(x, y)

        self._textpos = [x + 26, y]

        area_height = self.get_area_height()

        y_screen_flip = area_height - self.y_screen

        off_x = 0
        off_y = 0
        sx, sy = self.__boxsize

        self.shader_chb = gpu.shader.from_builtin('2D_UNIFORM_COLOR')

        # top left, top right, ...
        vertices_box = (
            (self.x_screen + off_x,      y_screen_flip - off_y - sy),
            (self.x_screen + off_x + sx, y_screen_flip - off_y - sy),
            (self.x_screen + off_x + sx, y_screen_flip - off_y),
            (self.x_screen + off_x,      y_screen_flip - off_y))

        self.batch_box = batch_for_shader(
            self.shader_chb, 'LINE_LOOP', {"pos": vertices_box})

        inset = 4

        # cross top-left, bottom-right | top-right, bottom-left
        vertices_cross = (
            (self.x_screen + off_x + inset,      y_screen_flip - off_y - inset),
            (self.x_screen + off_x + sx - inset,
             y_screen_flip - off_y - sy + inset),
            (self.x_screen + off_x + sx - inset, y_screen_flip - off_y - inset),
            (self.x_screen + off_x + inset, y_screen_flip - off_y - sy + inset))

        self.batch_cross = batch_for_shader(
            self.shader_chb, 'LINES', {"pos": vertices_cross})

    def draw(self):
        if not self.visible:
            return

        area_height = self.get_area_height()
        self.shader_chb.bind()

        if self.is_checked:
            bgl.glLineWidth(3)
            self.shader_chb.uniform_float("color", self._cross_color)

            self.batch_cross.draw(self.shader_chb)

        bgl.glLineWidth(2)
        self.shader_chb.uniform_float("color", self._box_color)

        self.batch_box.draw(self.shader_chb)

        # Draw text
        self.draw_text(area_height)

    def draw_text(self, area_height):
        blf.size(0, self._text_size, 72)
        size = blf.dimensions(0, self._text)

        textpos_y = area_height - \
            self._textpos[1] - (self.height + size[1]) / 2.0
        blf.position(0, self._textpos[0], textpos_y + 1, 0)

        r, g, b, a = self._text_color
        blf.color(0, r, g, b, a)

        blf.draw(0, self._text)

    def is_in_rect(self, x, y):
        area_height = self.get_area_height()

        widget_y = area_height - self.y_screen
        if (
            (self.x_screen <= x <= (self.x_screen + self.__boxsize[0])) and
            (widget_y >= y >= (widget_y - self.__boxsize[1]))
        ):
            return True

        return False

    def set_state_changed(self, state_changed_func):
        self.state_changed_func = state_changed_func

    def call_state_changed(self):
        try:
            self.state_changed_func(self, self.__state)
        except:
            pass

    def toggle_state(self):
        self.__state = not self.__state

    def mouse_enter(self, event, x, y):
        super().mouse_enter(event, x, y)
        if self._mouse_down:
            self.toggle_state()
            self.call_state_changed()

    def mouse_down(self, x, y):
        if self.is_in_rect(x, y):
            self.toggle_state()

            self.call_state_changed()

            return True

        return False

#from . bl_ui_widget import *


class BL_UI_Drag_Panel(BL_UI_Widget):

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.drag_offset_x = 600
        self.drag_offset_y = 500
        self.is_drag = False
        self.widgets = []

    def set_location(self, x, y):
        super().set_location(x, y)
        self.layout_widgets()

    def add_widget(self, widget):
        self.widgets.append(widget)

    def add_widgets(self, widgets):
        self.widgets = widgets
        self.layout_widgets()

    def layout_widgets(self):
        for widget in self.widgets:
            widget.update(self.x_screen + widget.x, self.y_screen + widget.y)

    def update(self, x, y):
        super().update(x - self.drag_offset_x, y + self.drag_offset_y)

    def child_widget_focused(self, x, y):
        for widget in self.widgets:
            if widget.is_in_rect(x, y):
                return True
        return False

    def mouse_down(self, x, y):
        if self.child_widget_focused(x, y):
            return False

        if self.is_in_rect(x, y):
            height = self.get_area_height()
            self.is_drag = True
            self.drag_offset_x = x - self.x_screen
            self.drag_offset_y = y - (height - self.y_screen)
            return True

        return False

    def mouse_move(self, x, y):
        if self.is_drag:
            height = self.get_area_height()
            self.update(x, height - y)
            self.layout_widgets()

    def mouse_up(self, x, y):
        self.is_drag = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0


#import bpy


class BL_UI_OT_draw_operator(Operator):
    bl_idname = "object.bl_ui_ot_draw_operator"
    bl_label = "bl ui widgets operator"
    bl_description = "Operator for bl ui widgets"
    bl_options = {'REGISTER'}

    def __init__(self):
        self.draw_handle = None
        self.draw_event = None
        self._finished = False

        self.widgets = []

    def init_widgets(self, context, widgets):
        self.widgets = widgets
        for widget in self.widgets:
            widget.init(context)

    def on_invoke(self, context, event):
        pass

    def on_finish(self, context):
        self._finished = True

    def invoke(self, context, event):

        self.on_invoke(context, event)

        args = (self, context)

        self.register_handlers(args, context)

        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def register_handlers(self, args, context):
        self.draw_handle = bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback_px, args, "WINDOW", "POST_PIXEL")
        self.draw_event = context.window_manager.event_timer_add(
            0.1, window=context.window)

    def unregister_handlers(self, context):

        context.window_manager.event_timer_remove(self.draw_event)

        bpy.types.SpaceView3D.draw_handler_remove(self.draw_handle, "WINDOW")

        self.draw_handle = None
        self.draw_event = None

    def handle_widget_events(self, event):
        result = False
        for widget in self.widgets:
            if widget.handle_event(event):
                result = True
        return result

    def modal(self, context, event):

        if self._finished:
            return {'FINISHED'}

        if context.area:
            context.area.tag_redraw()

        if self.handle_widget_events(event):
            return {'RUNNING_MODAL'}

        if event.type in {"ESC"}:
            bpy.data.scenes.remove(self.tutorialscene)
            self.finish()

        return {"PASS_THROUGH"}

    def finish(self):
        self.unregister_handlers(bpy.context)
        self.on_finish(bpy.context)

        # Draw handler to paint onto the screen
    def draw_callback_px(self, op, context):
        for widget in self.widgets:
            widget.draw()


#from . bl_ui_widget import *

#import blf

class BL_UI_Label(BL_UI_Widget):

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

        self._text_color = (1.0, 1.0, 1.0, 1.0)
        self._text = "Label"
        self._text_size = 16

    @property
    def text_color(self):
        return self._text_color

    @text_color.setter
    def text_color(self, value):
        self._text_color = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def text_size(self):
        return self._text_size

    @text_size.setter
    def text_size(self, value):
        self._text_size = value

    def is_in_rect(self, x, y):
        return False

    def draw(self):
        if not self.visible:
            return

        area_height = self.get_area_height()

        blf.size(0, self._text_size, 72)
        size = blf.dimensions(0, self._text)

        textpos_y = area_height - self.y_screen - self.height
        blf.position(0, self.x_screen, textpos_y, 0)

        r, g, b, a = self._text_color

        blf.color(0, r, g, b, a)

        blf.draw(0, self._text)


#from . bl_ui_widget import *

#import blf

class BL_UI_Slider(BL_UI_Widget):

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self._text_color = (1.0, 1.0, 1.0, 1.0)
        self._color = (0.5, 0.5, 0.7, 1.0)
        self._hover_color = (0.5, 0.5, 0.8, 1.0)
        self._select_color = (0.7, 0.7, 0.7, 1.0)
        self._bg_color = (0.8, 0.8, 0.8, 0.6)

        self._min = 0
        self._max = 100

        self.x_screen = x
        self.y_screen = y

        self._text_size = 14
        self._decimals = 2

        self._show_min_max = True

        self.__state = 0
        self.__is_drag = False
        self.__slider_pos = 0
        self.__slider_value = round(0, self._decimals)
        self.__slider_width = 5
        self.__slider_height = 13
        self.__slider_offset_y = 3

    @property
    def text_color(self):
        return self._text_color

    @text_color.setter
    def text_color(self, value):
        self._text_color = value

    @property
    def text_size(self):
        return self._text_size

    @text_size.setter
    def text_size(self, value):
        self._text_size = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    @property
    def hover_color(self):
        return self._hover_color

    @hover_color.setter
    def hover_color(self, value):
        self._hover_color = value

    @property
    def select_color(self):
        return self._select_color

    @select_color.setter
    def select_color(self, value):
        self._select_color = value

    @property
    def min(self):
        return self._min

    @min.setter
    def min(self, value):
        self._min = value

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, value):
        self._max = value

    @property
    def decimals(self):
        return self._decimals

    @decimals.setter
    def decimals(self, value):
        self._decimals = value

    @property
    def show_min_max(self):
        return self._show_min_max

    @show_min_max.setter
    def show_min_max(self, value):
        self._show_min_max = value

    def draw(self):
        if not self.visible:
            return

        area_height = self.get_area_height()

        self.shader.bind()

        color = self._color
        text_color = self._text_color

        # pressed
        if self.__state == 1:
            color = self._select_color

        # hover
        elif self.__state == 2:
            color = self._hover_color

        # Draw background
        self.shader.uniform_float("color", self._bg_color)
        bgl.glEnable(bgl.GL_BLEND)
        self.batch_bg.draw(self.shader)

        # Draw slider
        self.shader.uniform_float("color", color)

        self.batch_slider.draw(self.shader)
        bgl.glDisable(bgl.GL_BLEND)

        # Draw value text
        sFormat = "{:0." + str(self._decimals) + "f}"
        blf.size(0, self._text_size, 72)

        sValue = sFormat.format(self.__slider_value)
        size = blf.dimensions(0, sValue)

        blf.position(0, self.__slider_pos + 1 + self.x_screen - size[0] / 2.0,
                     area_height - self.y_screen + self.__slider_offset_y, 0)

        blf.draw(0, sValue)

        # Draw min and max
        if self._show_min_max:
            sMin = sFormat.format(self._min)

            size = blf.dimensions(0, sMin)

            blf.position(0, self.x_screen - size[0] / 2.0,
                         area_height - self.height - self.y_screen, 0)
            blf.draw(0, sMin)

            sMax = sFormat.format(self._max)

            size = blf.dimensions(0, sMax)

            r, g, b, a = self._text_color
            blf.color(0, r, g, b, a)

            blf.position(0, self.x_screen + self.width - size[0] / 2.0,
                         area_height - self.height - self.y_screen, 0)
            blf.draw(0, sMax)

    def update_slider(self):
        # Slider triangles
        #
        #        0
        #     1 /\ 2
        #      |  |
        #     3---- 4

        # batch for slider
        area_height = self.get_area_height()

        h = self.__slider_height
        w = self.__slider_width
        pos_y = area_height - self.y_screen - self.height / 2.0 + \
            self.__slider_height / 2.0 + self.__slider_offset_y
        pos_x = self.x_screen + self.__slider_pos

        indices = ((0, 1, 2), (1, 2, 3), (3, 2, 4))

        vertices = (
            (pos_x, pos_y),
            (pos_x - w, pos_y - w),
            (pos_x + w, pos_y - w),
            (pos_x - w, pos_y - h),
            (pos_x + w, pos_y - h)
        )

        self.shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
        self.batch_slider = batch_for_shader(self.shader, 'TRIS',
                                             {"pos": vertices}, indices=indices)

    def update(self, x, y):

        area_height = self.get_area_height()

        # Min                      Max
        #  |---------V--------------|

        self.x_screen = x
        self.y_screen = y

        self.update_slider()

        # batch for background
        pos_y = area_height - self.y_screen - self.height / 2.0
        pos_x = self.x_screen

        indices = ((0, 1, 2), (0, 2, 3))

        # bottom left, top left, top right, bottom right
        vertices = (
            (pos_x, pos_y),
            (pos_x, pos_y + 4),
            (pos_x + self.width, pos_y + 4),
            (pos_x + self.width, pos_y)
        )

        self.batch_bg = batch_for_shader(
            self.shader, 'TRIS', {"pos": vertices}, indices=indices)

    def set_value_change(self, value_change_func):
        self.value_change_func = value_change_func

    def is_in_rect(self, x, y):
        area_height = self.get_area_height()
        slider_y = area_height - self.y_screen - self.height / \
            2.0 + self.__slider_height / 2.0 + self.__slider_offset_y

        if (
            (self.x_screen + self.__slider_pos - self.__slider_width <= x <=
             (self.x_screen + self.__slider_pos + self.__slider_width)) and
            (slider_y >= y >= slider_y - self.__slider_height)
        ):
            return True

        return False

    def __value_to_pos(self, value):
        return self.width * (value - self._min) / (self._max - self._min)

    def __pos_to_value(self, pos):
        return self._min + round(((self._max - self._min) * self.__slider_pos / self.width), self._decimals)

    def get_value(self):
        return self.__slider_value

    def set_value(self, value):
        if value < self._min:
            value = self._min
        if value > self._max:
            value = self._max

        if value != self.__slider_value:
            self.__slider_value = round(value, self._decimals)

            try:
                self.value_change_func(self, self.__slider_value)
            except:
                pass

            self.__slider_pos = self.__value_to_pos(self.__slider_value)

            if self.context is not None:
                self.update_slider()

    def __set_slider_pos(self, x):
        if x <= self.x_screen:
            self.__slider_pos = 0
        elif x >= self.x_screen + self.width:
            self.__slider_pos = self.width
        else:
            self.__slider_pos = x - self.x_screen

        newValue = self.__pos_to_value(self.__slider_pos)

        if newValue != self.__slider_value:
            self.__slider_value = newValue

            try:
                self.value_change_func(self, self.__slider_value)
            except:
                pass

    def mouse_down(self, x, y):
        if self.is_in_rect(x, y):
            self.__state = 1
            self.__is_drag = True

            return True

        return False

    def mouse_move(self, x, y):
        if self.is_in_rect(x, y):
            if(self.__state != 1):

                # hover state
                self.__state = 2
        else:
            self.__state = 0

        if self.__is_drag:
            self.__set_slider_pos(x)
            self.update(self.x_screen, self.y_screen)

    def mouse_up(self, x, y):
        self.__state = 0
        self.__is_drag = False


class BL_UI_Textbox(BL_UI_Widget):

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self._text_color = (1.0, 1.0, 1.0, 1.0)

        self._label_color = (1.0, 1.0, 1.0, 1.0)

        self._label_text_color = (0.1, 0.1, 0.1, 1.0)

        self._bg_color = (0.2, 0.2, 0.2, 1.0)

        self._carret_color = (0.0, 0.2, 1.0, 1.0)

        self._offset_letters = 0

        self._carret_pos = 0

        self._input_keys = ['ESC', 'RET', 'BACK_SPACE',
                            'HOME', 'END', 'LEFT_ARROW', 'RIGHT_ARROW', 'DEL']

        self.text = ""
        self._label = ""
        self._text_size = 12
        self._textpos = [x, y]
        self._max_input_chars = 100
        self._label_width = 0
        self._is_numeric = False

    @property
    def carret_color(self):
        return self._carret_color

    @carret_color.setter
    def carret_color(self, value):
        self._carret_color = value

    @property
    def text_color(self):
        return self._text_color

    @text_color.setter
    def text_color(self, value):
        self._text_color = value

    @property
    def max_input_chars(self):
        return self._max_input_chars

    @max_input_chars.setter
    def max_input_chars(self, value):
        self._max_input_chars = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self._carret_pos = len(value)

        if self.context is not None:
            self.update_carret()

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value
        if self.context is not None:
            self.update_label()

    @property
    def text_size(self):
        return self._text_size

    @text_size.setter
    def text_size(self, value):
        self._text_size = value

    @property
    def has_label(self):
        return self._label != ""

    @property
    def is_numeric(self):
        return self._is_numeric

    @is_numeric.setter
    def is_numeric(self, value):
        self._is_numeric = value

    def update(self, x, y):
        super().update(x, y)

        if self.has_label:
            self.update_label()

        self._textpos = [x, y]
        self.update_carret()

    def update_label(self):
        y_screen_flip = self.get_area_height() - self.y_screen

        size = blf.dimensions(0, self._label)

        self._label_width = size[0] + 12

        # bottom left, top left, top right, bottom right
        vertices_outline = (
            (self.x_screen, y_screen_flip),
            (self.x_screen + self.width + self._label_width, y_screen_flip),
            (self.x_screen + self.width + self._label_width,
             y_screen_flip - self.height),
            (self.x_screen, y_screen_flip - self.height))

        self.batch_outline = batch_for_shader(
            self.shader, 'LINE_LOOP', {"pos": vertices_outline})

        indices = ((0, 1, 2), (2, 3, 1))

        lb_x = self.x_screen + self.width

        # bottom left, top left, top right, bottom right
        vertices_label_bg = (
            (lb_x, y_screen_flip),
            (lb_x + self._label_width, y_screen_flip),
            (lb_x, y_screen_flip - self.height),
            (lb_x + self._label_width, y_screen_flip - self.height))

        self.batch_label_bg = batch_for_shader(
            self.shader, 'TRIS', {"pos": vertices_label_bg}, indices=indices)

    def get_carret_pos_px(self):
        size_all = blf.dimensions(0, self._text)
        size_to_carret = blf.dimensions(0, self._text[:self._carret_pos])
        return self.x_screen + (self.width / 2.0) - (size_all[0] / 2.0) + size_to_carret[0]

    def update_carret(self):

        y_screen_flip = self.get_area_height() - self.y_screen

        x = self.get_carret_pos_px()

        # bottom left, top left, top right, bottom right
        vertices = (
            (x, y_screen_flip - 6),
            (x, y_screen_flip - self.height + 6)
        )

        self.batch_carret = batch_for_shader(
            self.shader, 'LINES', {"pos": vertices})

    def draw(self):

        if not self.visible:
            return

        super().draw()

        area_height = self.get_area_height()

        # Draw text
        self.draw_text(area_height)

        self.shader.bind()
        self.shader.uniform_float("color", self._carret_color)
        bgl.glEnable(bgl.GL_LINE_SMOOTH)
        bgl.glLineWidth(2)
        self.batch_carret.draw(self.shader)

        if self.has_label:
            self.shader.uniform_float("color", self._label_color)
            bgl.glLineWidth(1)
            self.batch_outline.draw(self.shader)

            self.batch_label_bg.draw(self.shader)

            size = blf.dimensions(0, self._label)

            textpos_y = area_height - self.y_screen - \
                (self.height + size[1]) / 2.0
            blf.position(0, self.x_screen + self.width +
                         (self._label_width / 2.0) - (size[0] / 2.0), textpos_y + 1, 0)

            r, g, b, a = self._label_text_color
            blf.color(0, r, g, b, a)

            blf.draw(0, self._label)

    def set_colors(self):
        color = self._bg_color
        text_color = self._text_color

        self.shader.uniform_float("color", color)

    def draw_text(self, area_height):
        blf.size(0, self._text_size, 72)
        size = blf.dimensions(0, self._text)

        textpos_y = area_height - \
            self._textpos[1] - (self.height + size[1]) / 2.0
        blf.position(
            0, self._textpos[0] + (self.width - size[0]) / 2.0, textpos_y + 1, 0)

        r, g, b, a = self._text_color
        blf.color(0, r, g, b, a)

        blf.draw(0, self._text)

    def get_input_keys(self):
        return self._input_keys

    def text_input(self, event):

        index = self._carret_pos

        if event.ascii != '' and len(self._text) < self.max_input_chars:
            value = self._text[:index] + event.ascii + self._text[index:]
            if self._is_numeric and not (event.ascii.isnumeric() or event.ascii in ['.', ',', '-']):
                return False

            self._text = value
            self._carret_pos += 1
        elif event.type == 'BACK_SPACE':
            if event.ctrl:
                self._text = ""
                self._carret_pos = 0
            elif self._carret_pos > 0:
                self._text = self._text[:index-1] + self._text[index:]
                self._carret_pos -= 1

        elif event.type == 'DEL':
            if self._carret_pos < len(self._text):
                self._text = self._text[:index] + self._text[index+1:]

        elif event.type == 'LEFT_ARROW':
            if self._carret_pos > 0:
                self._carret_pos -= 1

        elif event.type == 'RIGHT_ARROW':
            if self._carret_pos < len(self._text):
                self._carret_pos += 1

        elif event.type == 'HOME':
            self._carret_pos = 0

        elif event.type == 'END':
            self._carret_pos = len(self._text)

        self.update_carret()
        try:
            self.text_changed_func(self, self.context, event)
        except:
            pass

        return True

    def set_text_changed(self, text_changed_func):
        self.text_changed_func = text_changed_func

    def mouse_down(self, x, y):
        if self.is_in_rect(x, y):
            return True

        return False

    def mouse_move(self, x, y):
        pass

    def mouse_up(self, x, y):
        pass


class BL_UI_Up_Down(BL_UI_Widget):

    def __init__(self, x, y):

        self.__up_down_width = 16
        self.__up_down_height = 16

        super().__init__(x, y, self.__up_down_width * 2, self.__up_down_height)

        # Text of the numbers
        self._text_color = (1.0, 1.0, 1.0, 1.0)

        # Color of the up/down graphics
        self._color = (0.5, 0.5, 0.7, 1.0)

        # Hover % select colors of the up/down graphics
        self._hover_color = (0.5, 0.5, 0.8, 1.0)
        self._select_color = (0.7, 0.7, 0.7, 1.0)

        self._min = 0
        self._max = 100

        self.x_screen = x
        self.y_screen = y

        self._text_size = 14
        self._decimals = 2

        self.__state = 0
        self.__up_down_value = round(0, self._decimals)

    @property
    def text_color(self):
        return self._text_color

    @text_color.setter
    def text_color(self, value):
        self._text_color = value

    @property
    def text_size(self):
        return self._text_size

    @text_size.setter
    def text_size(self, value):
        self._text_size = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    @property
    def hover_color(self):
        return self._hover_color

    @hover_color.setter
    def hover_color(self, value):
        self._hover_color = value

    @property
    def select_color(self):
        return self._select_color

    @select_color.setter
    def select_color(self, value):
        self._select_color = value

    @property
    def min(self):
        return self._min

    @min.setter
    def min(self, value):
        self._min = value

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, value):
        self._max = value

    @property
    def decimals(self):
        return self._decimals

    @decimals.setter
    def decimals(self, value):
        self._decimals = value

    def draw(self):

        if not self.visible:
            return

        area_height = self.get_area_height()

        self.shader.bind()

        color = self._color
        text_color = self._text_color

        # pressed
        if self.__state == 1:
            color = self._select_color

        # hover
        elif self.__state == 2:
            color = self._hover_color

        self.shader.uniform_float("color", color)

        self.batch_up.draw(self.shader)

        color = self._color

        # pressed (down button)
        if self.__state == 3:
            color = self._select_color

        # hover (down button)
        elif self.__state == 4:
            color = self._hover_color

        self.shader.uniform_float("color", color)
        self.batch_down.draw(self.shader)

        # Draw value text
        sFormat = "{:0." + str(self._decimals) + "f}"
        blf.size(0, self._text_size, 72)

        sValue = sFormat.format(self.__up_down_value)
        size = blf.dimensions(0, sValue)

        y_pos = area_height - self.y_screen - size[1] - 2
        x_pos = self.x_screen + 2 * self.__up_down_width + 10

        blf.position(0, x_pos, y_pos, 0)

        r, g, b, a = self._text_color
        blf.color(0, r, g, b, a)

        blf.draw(0, sValue)

    def create_up_down_buttons(self):
        # Up / down triangle
        #
        #        0
        #     1 /\ 2
        #       --

        area_height = self.get_area_height()

        h = self.__up_down_height
        w = self.__up_down_width / 2.0

        pos_y = area_height - self.y_screen
        pos_x = self.x_screen

        vertices_up = (
            (pos_x + w, pos_y),
            (pos_x, pos_y - h),
            (pos_x + 2*w, pos_y - h)
        )

        pos_x += 18

        vertices_down = (
            (pos_x, pos_y),
            (pos_x + w, pos_y - h),
            (pos_x + 2*w, pos_y)

        )

        self.shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
        self.batch_up = batch_for_shader(
            self.shader, 'TRIS', {"pos": vertices_up})
        self.batch_down = batch_for_shader(
            self.shader, 'TRIS', {"pos": vertices_down})

    def update(self, x, y):

        self.x_screen = x
        self.y_screen = y

        self.create_up_down_buttons()

    def set_value_change(self, value_change_func):
        self.value_change_func = value_change_func

    def is_in_up(self, x, y):

        area_height = self.get_area_height()
        pos_y = area_height - self.y_screen

        if (
            (self.x_screen <= x <= self.x_screen + self.__up_down_width) and
            (pos_y >= y >= pos_y - self.__up_down_height)
        ):
            return True

        return False

    def is_in_down(self, x, y):

        area_height = self.get_area_height()
        pos_y = area_height - self.y_screen
        pos_x = self.x_screen + self.__up_down_width + 2

        if (
            (pos_x <= x <= pos_x + self.__up_down_width) and
            (pos_y >= y >= pos_y - self.__up_down_height)
        ):
            return True

        return False

    def is_in_rect(self, x, y):
        return self.is_in_up(x, y) or self.is_in_down(x, y)

    def set_value(self, value):
        if value < self._min:
            value = self._min
        if value > self._max:
            value = self._max

        if value != self.__up_down_value:
            self.__up_down_value = round(value, self._decimals)

            try:
                self.value_change_func(self, self.__up_down_value)
            except:
                pass

    def mouse_down(self, x, y):
        if self.is_in_up(x, y):
            self.__state = 1
            self.inc_value()
            return True

        if self.is_in_down(x, y):
            self.__state = 3
            self.dec_value()
            return True

        return False

    def inc_value(self):
        self.set_value(self.__up_down_value + 1)

    def dec_value(self):
        self.set_value(self.__up_down_value - 1)

    def mouse_move(self, x, y):
        if self.is_in_up(x, y):
            if(self.__state != 1):

                # hover state
                self.__state = 2

        elif self.is_in_down(x, y):
            if(self.__state != 3):

                # hover state
                self.__state = 4

        else:
            self.__state = 0

    def mouse_up(self, x, y):
        self.__state = 0
