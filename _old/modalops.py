import bpy

from bpy.types import (
    Operator,
    GizmoGroup,
)

from .gizmos import has_stopper

#from bpy.types import Scene, Image, Object


class PP_OT_PlanarZScaleMenu(bpy.types.Operator):
    '''Change the Zscale of the coupling'''
    bl_idname = "purp.zscalemenu"
    bl_label = "zscalemenu"
    bl_options = {'REGISTER', "UNDO"}

    ZScale: bpy.props.FloatProperty(
        name="Zscale",
        description="Sets the Zscale",
        default=3,
        min=0,
    )

    @classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):
        PUrP = context.scene.PUrP
        if self.has_stopper:
            if self.valuemiddle >= 0:  # upper limiter
                for v in self.middleV:
                    v.co.z = -0.01
                for v in self.lowestV:
                    v.co.z = -0.01 - context.scene.PUrP.StopperHeight
                context.scene.PUrP.zScale = 0.01
            else:  # positioning

                for v in self.middleV:
                    v.co.z = self.valuemiddle

                for v in self.lowestV:
                    v.co.z = self.valuelow

                context.scene.PUrP.zScale = -self.valuemiddle
        else:  # no stopper
            if self.valuelow >= 0:
                for v in self.lowestV:
                    v.co.z = -0.01
                context.scene.PUrP.zScale = 0.01
            else:
                for v in self.lowestV:
                    v.co.z = self.valuelow
                context.scene.PUrP.zScale = -self.valuelow

                # if self.has_stopper:
                #    for v in self.middleV:
                #        v.co.z = self.valuemiddle

        return {'FINISHED'}

    def modal(self, context, event):
        PUrP = context.scene.PUrP
        if event.type == 'MOUSEMOVE':  # Apply
            sensi = 100 if not event.type == 'SHIFT' else 1000
            self.delta = event.mouse_y - self.init_value
            self.valuelow = self.lowestz + self.delta * PUrP.GlobalScale / sensi
            # if self.has_stopper:
            self.valuemiddle = self.middlez + self.delta / 100

            self.execute(context)

        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            for v in self.lowestV:
                v.co.z = self.lowestz
            if self.has_stopper:
                for v in self.middleV:
                    v.co.z = self.middlez
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        ob = context.object
        self.middleV = []
        self.lowestV = []
        self.lowestz = 0
        self.middlez = 0
        for v in ob.data.vertices:
            if v.co.z < self.lowestz:
                self.lowestz = v.co.z

        self.has_stopper = has_stopper(ob)

        if self.has_stopper:  # zscale with stopper is like moving all below the top line

            for v in ob.data.vertices:
                if v.co.z != 0 and v.co.z != self.lowestz:
                    self.middlez = v.co.z
                    self.middleV.append(v)

            for v in ob.data.vertices:
                if v.co.z == self.lowestz:
                    self.lowestV.append(v)

            # for v in ob.data.vertices:
            #    if v.co.z == self.middlez:
            #        self.middleV.append(v)

        else:
            self.lowestz = 0
            for v in ob.data.vertices:
                if v.co.z < self.lowestz:
                    self.lowestz = v.co.z
            # self.lowestV = []
            for v in ob.data.vertices:
                if v.co.z == self.lowestz:
                    self.lowestV.append(v)
            # coordinaten aller

        # self.init_position1 = lowestz
        # self.init_position2 = self.middlez

        self.init_value = event.mouse_y

        # event.mouse_x #- self.window_width/21   ################mach mal start value einfach 00
        self.valuelow = self.lowestz
        if self.has_stopper:
            self.valuemiddle = self.middlez

        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
