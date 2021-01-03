import bpy
from .gizmotshape import PUrP_CornerShapeWidget
from .gizmotshape import PUrP_ArrowUpShapeWidget
from .gizmotshape import PUrP_linecountShapeWidget
from .gizmotshape import PUrP_LineLengthShapeWidget
from .gizmotshape import PUrP_LineDistanceShapeWidget
from .gizmotshape import PUrP_ThicknessShapeWidget
from .gizmotshape import PUrP_CubeShapeWidget
from .gizmotshape import PUrP_ConeShapeWidget
from .gizmotshape import PUrP_CylinderShapeWidget


from .bun import oversizeToPrim
from .bun import applyScalRot
from .bun import singcoupmode
from .bun import planaranalysizerGlobal
from .bun import planaranalysizerLocal

from bpy.types import (
    Operator,
    GizmoGroup,
)
import mathutils
from math import radians
import copy


class PP_OT_OversizeGizmo(bpy.types.Operator):
    '''Change the Oversize of the coupling'''
    bl_idname = "object.oversize"
    bl_label = "oversize"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):
        children = context.object.children
        PUrP = context.scene.PUrP

        if self.valueos > 0:
            PUrP.Oversize = self.valueos
            # applyScalRot(self.obin)
            oversizeToPrim(context, singcoupmode(
                context, None, context.object), self.obout, self.obin)

        else:
            PUrP.Oversize = 0
            # applyScalRot(self.obin)
            oversizeToPrim(context, singcoupmode(
                context, None, context.object), self.obout, self.obin)
        return {'FINISHED'}

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':  # Apply
            sensi = 1000 if not event.shift else 10000
            #sensi = 1000
            self.delta = event.mouse_y - self.init_value
            self.valueos = self.init_oversize + self.delta/sensi

            self.execute(context)

        elif event.type == 'LEFTMOUSE':  # Confirm
            # applyScalRot(self.obin)
            oversizeToPrim(context, singcoupmode(
                context, None, context.object), self.obout, self.obin)
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            PUrP.Oversize = self.init_oversize
            # applyScalRot(self.obin)
            oversizeToPrim(context, singcoupmode(
                context, None, context.object), self.obout, self.obin)
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        PUrP = context.scene.PUrP
        children = context.object.children
        # order correction
        for child in children:
            if "diff" in child.name:
                self.obout = child
            elif "fix" in child.name or "union" in child.name:
                self.obin = child

        self.valueos = PUrP.Oversize
        self.init_oversize = copy.copy(PUrP.Oversize)
        self.init_value = event.mouse_y

        # event.mouse_x #- self.window_width/21   ################mach mal start value einfach 00

        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class PP_OT_CouplSizeGizmo(bpy.types.Operator):
    '''Change the scale of the coupling'''
    bl_idname = "object.couplesize"
    bl_label = "couplsize"
    bl_options = {'REGISTER', "UNDO"}

    @ classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):
        PUrP = context.scene.PUrP
        ob = context.object

        self.obout.scale.x = self.valuex0
        self.obout.scale.y = self.valuex0
        self.obout.scale.z = self.valuex0

        self.obin.scale.x = self.valuex0
        self.obin.scale.y = self.valuex0
        self.obin.scale.z = self.valuex0

        # applyScalRot(self.obout)
        singcoupmod = singcoupmode(context, None, context.object)
        # oversizeToPrim(context, singcoupmode, self.obout, self.obin)

        scalefactor = PUrP.GlobalScale * PUrP.CoupScale
        if "Cube" in self.obout.data.name:
            vert = self.obout.data.vertices[0].co@self.obout.matrix_world
            PUrP.CoupSize = 2 * abs(vert[1])/scalefactor
        else:
            vert = self.obout.data.vertices[0].co@self.obout.matrix_world
            # print(vert)
            # inter = 2 * abs(vert[1])/scalefactor
            # print(inter)
            PUrP.CoupSize = abs(vert[1])/scalefactor

        return {'FINISHED'}

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':  # Apply
            # if context.object.children[0].scale.x <= context.object.children[1].scale.x:  ####not bigger than the outer object
            sensi = 1000 if not event.shift else 10000
            self.delta = event.mouse_x - self.init_value
            # else:
            #    self.delta =  self.init_value

            # self.valuex1 = self.init_scale_x1 + self.delta / \
            #    1000  # - self.window_width/2 #(HD Screen 800)
            # self.valuey1 = self.init_scale_y1 + self.delta/1000
            # self.valuez1 = self.init_scale_z1 + self.delta/1000

            self.valuex0 = self.init_scale_x0 + self.delta/sensi
            # self.valuey0 = self.init_scale_y0 + self.delta/1000
            # self.valuez0 = self.init_scale_z0 + self.delta/1000

            # print(f"MouspositionX: {self.value}")
            self.execute(context)
        elif event.type == 'LEFTMOUSE':  # Confirm
            # applyScalRot(self.obout)
            # applyScalRot(self.obin)

            oversizeToPrim(context, singcoupmode(
                context, None, context.object), self.obout, self.obin)
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            self.obout.scale.x = self.init_scale_x0
            self.obout.scale.y = self.init_scale_x0
            self.obout.scale.z = self.init_scale_x0
            # applyScalRot(self.obout)
            # applyScalRot(self.obin)

            oversizeToPrim(context, singcoupmode(
                context, None, context.object), self.obout, self.obin)
            # self.obin.scale.x = self.init_scale_x1
            # self.obin.scale.y = self.init_scale_y1
            # self.obin.scale.z = self.init_scale_z1
            return {'CANCELLED'}
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        ob = context.object
        PUrP = context.scene.PUrP
        PUrP.Coupscale = ob.data.vertices[1].co.x / (3 * PUrP.GlobalScale)
        children = context.object.children
        # order correction
        for child in children:
            if "diff" in child.name:
                self.obout = child
            elif "fix" in child.name or "union" in child.name:
                self.obin = child

        self.init_scale_x0 = self.obout.scale.x
        # self.init_scale_y0 = self.obout.scale.y
        # self.init_scale_z0 = self.obout.scale.z

        self.valuex0 = self.obout.scale.x
        # self.valuey0 = self.obout.scale.y
        # self.valuez0 = self.obout.scale.z

        self.init_value = event.mouse_x

        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class PP_OT_zScaleGizmo(bpy.types.Operator):
    '''Change the z-scale of the coupling'''
    bl_idname = "object.zscale"
    bl_label = "couplsize"
    bl_options = {'REGISTER', "UNDO"}

    @ classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):

        self.obout.scale.z = self.value
        self.obin.scale.z = self.value

        PUrP = context.scene.PUrP
        PUrP.zScale = self.value / PUrP.CoupSize
        return {'FINISHED'}

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':  # Apply
            sensi = 1000 if not event.shift else 10000
            self.delta = event.mouse_y - self.init_value
            self.value = self.init_scale_z + self.delta/sensi

            self.execute(context)
        elif event.type == 'LEFTMOUSE':  # Confirm
            applyScalRot(self.obout)
            applyScalRot(self.obin)

            oversizeToPrim(context, singcoupmode(
                context, None, context.object), self.obout, self.obin)
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            self.obout.location.z = self.init_scale_z
            self.obin.location.z = self.init_scale_z
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        children = context.object.children
        # order correction
        for child in children:
            if "diff" in child.name:
                self.obout = child
            elif "fix" in child.name or "union" in child.name:
                self.obin = child

        self.init_scale_z = self.obout.scale.z
        self.init_value = event.mouse_y
        self.value = self.obout.scale.z

        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class PP_OT_BevelOffsetGizmo(bpy.types.Operator):
    '''Change the beveloffset of the coupling'''
    bl_idname = "purp.bevoffset"
    bl_label = "couplsize"
    bl_options = {'REGISTER', "UNDO"}

    @ classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):

        self.obin.modifiers[0].width = self.value
        self.obout.modifiers[0].width = self.value
        context.scene.PUrP.BevelOffset = self.value
        return {'FINISHED'}

    def modal(self, context, event):
        children = context.object.children
        if event.type == 'MOUSEMOVE':  # Apply
            sensi = 1000 if not event.shift else 10000
            self.delta = event.mouse_y - self.init_value
            self.value = self.init_width + self.delta / sensi

            self.execute(context)
        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            self.obout.modifiers[0].width = self.init_width
            self.obin.modifiers[0].width = self.init_width
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        children = context.object.children
        # order correction
        for child in children:
            if "diff" in child.name:
                self.obout = child
            elif "fix" in child.name or "union" in child.name:
                self.obin = child

        self.init_width = self.obout.modifiers[0].width
        self.init_value = event.mouse_y
        self.value = self.obout.modifiers[0].width

        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class PP_OT_BevelSegmentGizmo(bpy.types.Operator):
    '''Change the beveloffset of the coupling'''
    bl_idname = "purp.bevseggiz"
    bl_label = "couplsize"
    bl_options = {'REGISTER', "UNDO"}

    @ classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):
        self.obin.modifiers[0].segments = int(self.value)
        self.obout.modifiers[0].segments = int(self.value)
        context.scene.PUrP.BevelSegments = int(self.value)
        return {'FINISHED'}

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':  # Apply
            sensi = 10 if not event.shift else 100
            self.delta = event.mouse_y - self.init_value
            self.value = self.init_segments + self.delta / sensi

            self.execute(context)
        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            self.obout.modifiers[0].segments = self.init_segments
            self.obin.modifiers[0].segments = self.init_segments
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        children = context.object.children
        # order correction
        for child in children:
            if "diff" in child.name:
                self.obout = child
            elif "fix" in child.name or "union" in child.name:
                self.obin = child

        self.init_segments = self.obout.modifiers[0].segments
        self.init_value = event.mouse_y
        self.value = self.obout.modifiers[0].segments

        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class PP_OT_CoupScaleGizmo(bpy.types.Operator):
    '''Change the Size of the Connector'''
    bl_idname = "purp.coupscalegizmo"
    bl_label = "couplsize"
    bl_options = {'REGISTER', "UNDO"}

    @ classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):
        PUrP = context.scene.PUrP
        ob = context.object

        ob.scale = self.value
        # bpy.ops.object.transform_apply(
        #    location=False, rotation=False, scale=True)

        # applyScalRot(self.obout)
        # applyScalRot(self.obin)

        oversizeToPrim(context, singcoupmode(
            context, None, context.object), self.obout, self.obin)
        print(f" obname {ob.name}")
        if "Planar" in ob.name:
            print(1)
            coupfaktor = PUrP.PlanarCorScale * PUrP.GlobalScale
            PUrP.CoupScale = abs(ob.data.vertices[3].co.x) / coupfaktor

        else:
            print(2)
            PUrP.CoupScale = ob.data.vertices[1].co.x * \
                self.value[0] / (3 * PUrP.GlobalScale)
        # print(self.value)
        return {'FINISHED'}

    def modal(self, context, event):
        ob = context.object
        if event.type == 'MOUSEMOVE':  # Apply
            sensi = 1000 if not event.shift else 10000
            self.delta = event.mouse_x - self.init_value
            print(
                f"mouse x {event.mouse_x} self.init_value {self.init_value} self.delta {self.delta} self.value {self.value} ")
            self.value = self.init_scale + mathutils.Vector(
                (self.delta / sensi, self.delta / sensi, self.delta / sensi))

            self.execute(context)
        elif event.type == 'LEFTMOUSE':  # Confirm
            bpy.ops.object.transform_apply(
                location=False, rotation=False, scale=True)
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            ob.scale = self.init_scale
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        children = context.object.children
        # order correction
        for child in children:
            if "diff" in child.name:
                self.obout = child
            elif "fix" in child.name or "union" in child.name:
                self.obin = child

        ob = context.object
        self.init_scale = ob.scale.copy()
        self.init_value = event.mouse_x
        # event.mouse_x #- self.window_width/21   ################mach mal start value einfach 00
        self.value = ob.scale
        self.execute(context)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class PP_OT_LowerRadiusGizmo(bpy.types.Operator):
    '''Change the cylinder Radius or the lower radius of the cone'''
    bl_idname = "purp.lowerradiusgizmo"
    bl_label = "couplsize"
    bl_options = {'REGISTER', "UNDO"}

    @ classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):
        PUrP = context.scene.PUrP

        for num, v in enumerate(self.lowerverts):
            v.co.x = self.init_posx[num] * self.value
            v.co.y = self.init_posy[num] * self.value

        oversizeToPrim(context, singcoupmode(
            context, None, context.object), self.obout, self.obin)

        a, b, PUrP.aRadius, PUrP.bRadius = self.coneanalysizer(
            context, self.obout)
        return {'FINISHED'}

    def modal(self, context, event):
        # ob = context.object
        if event.type == 'MOUSEMOVE':  # Apply
            sensi = 1000 if not event.shift else 10000
            self.delta = event.mouse_x - self.init_mouse
            self.value = 1.0 + self.delta / sensi

            self.execute(context)

        elif event.type == 'LEFTMOUSE':  # Confirm
            # bpy.ops.object.transform_apply(
            #    location=False, rotation=False, scale=True)
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            for num, v in enumerate(self.lowerverts):
                v.co.x = self.init_posx[num]
                v.co.y = self.init_posy[num]

            for num, v in enumerate(self.INlowerverts):
                v.co.x = self.init_INposx[num]
                v.co.y = self.init_INposy[num]
                v.co.z = self.init_INposz[num]
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        children = context.object.children
        # order correction
        for child in children:
            if "diff" in child.name:
                self.obout = child
            elif "fix" in child.name or "union" in child.name:
                self.obin = child

        PUrP = context.scene.PUrP

        self.upperverts, self.lowerverts, PUrP.aRadius, PUrP.bRadius = self.coneanalysizer(
            context, self.obout)

        self.INupperverts, self.INlowerverts, PUrP.aRadius, PUrP.bRadius = self.coneanalysizer(
            context, self.obin)

        if "Cylinder" in self.obout.data.name:
            self.lowerverts += self.upperverts
            self.INlowerverts += self.INupperverts

        self.init_posx = []
        self.init_posy = []
        for v in self.lowerverts:
            self.init_posx.append(v.co.x)
            self.init_posy.append(v.co.y)

        self.init_INposx = []
        self.init_INposy = []
        self.init_INposz = []
        for v in self.lowerverts:
            self.init_INposx.append(v.co.x)
            self.init_INposy.append(v.co.y)
            self.init_INposz.append(v.co.z)

        self.init_mouse = event.mouse_x
        self.value = 1.0

        self.execute(context)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def coneanalysizer(self, context, ob):
        # Cyclvert, and the radius are extrakted; Coupling types
        PUrP = context.scene.PUrP

        upperverts = []
        lowerverts = []
        for vert in ob.data.vertices:
            if vert.co.z > 0:
                upperverts.append(vert)
            elif vert.co.z <= 0:
                lowerverts.append(vert)
        # upperverts information
        if len(upperverts) == 1:  # hard tip
            bRadius = 0.0
        else:  # soft tip
            bRadius = abs(ob.data.vertices[1].co.y)
            bRadius = bRadius / (PUrP.GlobalScale * PUrP.CoupScale)
        # lower radius

        aRadius = abs(ob.data.vertices[0].co.y)
        aRadius = aRadius/(PUrP.GlobalScale * PUrP.CoupScale)

        return upperverts, lowerverts, aRadius, bRadius


class PP_OT_UpperRadiusGizmo(bpy.types.Operator):
    '''Change the cylinder Radius or the lower radius of the cone'''
    bl_idname = "purp.upperradiusgizmo"
    bl_label = "couplsize"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):
        PUrP = context.scene.PUrP

        for num, v in enumerate(self.upperverts):
            v.co.x = self.init_posx[num] * self.value
            v.co.y = self.init_posy[num] * self.value

        oversizeToPrim(context, singcoupmode(
            context, None, context.object), self.obout, self.obin)

        a, b, PUrP.aRadius, PUrP.bRadius = self.coneanalysizer(
            context, self.obout)
        return {'FINISHED'}

    def modal(self, context, event):
        # ob = context.object
        if event.type == 'MOUSEMOVE':  # Apply
            sensi = 1000 if not event.shift else 10000
            self.delta = event.mouse_x - self.init_mouse
            self.value = 1.0 + self.delta / sensi
            self.execute(context)

        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            for num, v in enumerate(self.upperverts):
                v.co.x = self.init_posx[num]
                v.co.y = self.init_posy[num]

            oversizeToPrim(context, singcoupmode(
                context, None, context.object), self.obout, self.obin)

            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        children = context.object.children
        # order correction
        for child in children:
            if "diff" in child.name:
                self.obout = child
            elif "fix" in child.name or "union" in child.name:
                self.obin = child

        PUrP = context.scene.PUrP

        self.upperverts, self.lowerverts, PUrP.aRadius, PUrP.bRadius = self.coneanalysizer(
            context, self.obout)

        if "Cylinder" in self.obout.data.name:
            self.upperverts += self.lowerverts

        self.init_posx = []
        self.init_posy = []
        for v in self.upperverts:
            self.init_posx.append(v.co.x)
            self.init_posy.append(v.co.y)

        self.init_mouse = event.mouse_x
        self.value = 1.0

        self.execute(context)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def coneanalysizer(self, context, ob):
        # Cyclvert, and the radius are extrakted; Coupling types
        PUrP = context.scene.PUrP

        upperverts = []
        lowerverts = []
        for vert in ob.data.vertices:
            if vert.co.z > 0:
                upperverts.append(vert)
            elif vert.co.z <= 0:
                lowerverts.append(vert)
        # upperverts information
        if len(upperverts) == 1:  # hard tip
            bRadius = 0.0
        else:  # soft tip
            bRadius = abs(ob.data.vertices[1].co.y)
            bRadius = bRadius / (PUrP.GlobalScale * PUrP.CoupScale)
        # lower radius

        aRadius = abs(ob.data.vertices[0].co.y)
        aRadius = aRadius/(PUrP.GlobalScale * PUrP.CoupScale)

        return upperverts, lowerverts, aRadius, bRadius


class PP_OT_SingleThicknessGizmo(bpy.types.Operator):
    '''Change the Oversize (Thickness) of the planar connector'''
    bl_idname = "purp.singthicknessgiz"
    bl_label = "couplsize"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):
        ob = context.object

        if self.value <= 0:
            ob.modifiers["PUrP_Solidify"].thickness = 0
            # context.scene.PUrP.Oversize = 0
        else:
            ob.modifiers["PUrP_Solidify"].thickness = self.value * \
                self.GlobalScale
            context.scene.PUrP.CutThickness = self.value
        return {'FINISHED'}

    def modal(self, context, event):

        if event.type == 'MOUSEMOVE':  # Apply
            sensi = 1000 if not event.shift else 10000
            self.delta = event.mouse_y - self.init_value
            self.value = self.init_count + self.delta / sensi
            print(
                f"self.value {self.value}   self.delta {self.delta}  self.init_value {self.init_value} ")
            self.execute(context)

        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            ob.modifiers["PUrP_Solidify"].thickness = self.init_count * \
                self.GlobalScale

            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        ob = context.object
        PUrP = context.scene.PUrP
        self.GlobalScale = PUrP.GlobalScale
        self.init_value = event.mouse_y
        self.value = ob.modifiers["PUrP_Solidify"].thickness / self.GlobalScale
        self.init_count = ob.modifiers["PUrP_Solidify"].thickness / \
            self.GlobalScale

        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class PUrP_SinglCoupGizmo(GizmoGroup):
    bl_idname = "OBJECT_GGT_test_camera"
    bl_label = "Object Camera Test Widget"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT'}

    @classmethod
    def poll(cls, context):

        ob = context.object

        if ob != None:
            if ("PUrP" in ob.name) and ("diff" and "fix" and "union" not in ob.name):
                if len(ob.children) > 1:  # flatcut has zero or
                    try:
                        test = context.scene.PUrP.GlobalScale
                        return True
                    except:
                        return False
                return False

            return False

    def setup(self, context):
        # Run an operator using the dial gizmo
        ob = context.object

        # matrixWorld = context.object[:]
        mpr = self.gizmos.new(PUrP_CubeShapeWidget.bl_idname)
        props = mpr.target_set_operator("object.oversize")
        # props.constraint_axis = True, True, True
        # props.orient_type = 'LOCAL'
        # props.release_confirm = True

        mpr.matrix_basis = ob.matrix_world.normalized()
        mpr.use_draw_offset_scale = True
        mpr.line_width = 3

        mpr.color = 0.03, 0.8, 0.8
        mpr.alpha = 0.5

        mpr.color_highlight = 0.03, 1.0, 1.0
        mpr.alpha_highlight = 1.0

        mpr.scale_basis = 0.3
        # mpr.matrix_offset[2][3] = 1

        self.roll_widget = mpr

        # couple size gizmot
        mpa = self.gizmos.new(PUrP_CubeShapeWidget.bl_idname)
        props = mpa.target_set_operator("object.couplesize")
        mpa.use_draw_offset_scale = True
        # props.constraint_axis = True, True, True
        # props.orient_type = 'LOCAL'
        # props.release_confirm = True

        mpa.matrix_basis = ob.matrix_world.normalized()

        mpa.line_width = 3

        mpa.color = 0.2, 0.2, 0.8
        mpa.alpha = 0.5

        mpa.color_highlight = 0.2, 0.03, 0.9
        mpa.alpha_highlight = 1.0
        mpa.scale_basis = 0.5
        self.roll_widge = mpa

        # zscale gizmot
        mph = self.gizmos.new(PUrP_ArrowUpShapeWidget.bl_idname)
        mph.target_set_operator("object.zscale")

        mph.use_draw_offset_scale = True
        mph.matrix_basis = ob.matrix_world.normalized()
        mph.color = 0.8, 0.03, 0.03
        mph.alpha = 0.5
        mph.color_highlight = 1.0, 0.05, 0.05
        mph.alpha_highlight = 1
        self.roll_widg = mph

        # Bevel offset gizmot
        mpo = self.gizmos.new(PUrP_CornerShapeWidget.bl_idname)
        # mpo = self.gizmos.new("GIZMO_GT_dial_3d")
        mpo.target_set_operator("purp.bevoffset")
        mpo.use_draw_offset_scale = True
        mpo.matrix_basis = ob.matrix_world.normalized()
        # mpo.matrix_offset[2][0] = 0.5  # [3] - location, 0 -x
        # mpo.matrix_basis[2][3] += 8
        # mpo.matrix_basis[0][3] += 3
        mpo.line_width = 10

        mpo.color = 0.05, 0.9, 0.05
        mpo.alpha = 0.5

        mpo.color_highlight = 0.03, 1.0, 0.03
        mpo.alpha_highlight = 1.0
        mpo.scale_basis = 0.5

        # mpo.use_draw_value

        self.roll_wid = mpo

        # Bevel segments gizmot
        mps = self.gizmos.new(PUrP_CornerShapeWidget.bl_idname)
        # mps = self.gizmos.new("GIZMO_GT_dial_3d")
        mps.target_set_operator("purp.bevseggiz")

        mps.use_draw_offset_scale = True
        mps.matrix_basis = ob.matrix_world.normalized()
        # mps.matrix_offset[2][0] = 0.2
        # mps.matrix_offset[2][2] = 0.5
        # mps.matrix_basis[2][3] += 0.8
        # mps.matrix_basis[0][3] += 0.5
        mps.line_width = 10

        mps.color = 0.03, 0.8, 0.03
        mps.alpha = 0.5

        mps.color_highlight = 0.01, 1.0, 0.01
        mps.alpha_highlight = 1.0
        mps.scale_basis = 0.2
        # mps.use_draw_value

        self.bevseggizm = mps

        # connectorsize
        mcsize = self.gizmos.new("GIZMO_GT_dial_3d")
        mcsize.target_set_operator("purp.coupscalegizmo")
        mcsize.use_draw_offset_scale = True
        mcsize.matrix_basis = ob.matrix_world.normalized()
        mcsize.use_draw_value = True
        # mps.matrix_offset[2][0] = 0.2
        # mps.matrix_offset[2][2] = 0.5
        # mps.matrix_basis[2][3] += 0.8
        # mps.matrix_basis[0][3] += 0.5
        mcsize.line_width = 3

        mcsize.color = 0.03, 0.8, 0.03
        mcsize.alpha = 0.5

        mcsize.color_highlight = 0.01, 1.0, 0.01
        mcsize.alpha_highlight = 1.0
        mcsize.scale_basis = 2

        self.couplingScale = mcsize

        # for cylinder or cone when lowradius adjustment
        lowradius = self.gizmos.new(PUrP_CylinderShapeWidget.bl_idname)
        lowradius.target_set_operator("purp.lowerradiusgizmo")
        lowradius.use_draw_offset_scale = True
        lowradius.matrix_basis = ob.matrix_world.normalized()
        lowradius.use_draw_value = True

        lowradius.matrix_offset[0][3] -= 3
        lowradius.matrix_offset[2][3] += 1.6
        # mps.matrix_basis[0][3] += 0.5
        lowradius.line_width = 3

        lowradius.color = 0.4, 0.8, 0.03
        lowradius.alpha = 0.5

        lowradius.color_highlight = 0.01, 1.0, 0.01
        lowradius.alpha_highlight = 1.0
        lowradius.scale_basis = 0.4

        self.lowRadius = lowradius

        # for cone when upperradius adjustment
        upradius = self.gizmos.new(PUrP_ConeShapeWidget.bl_idname)
        upradius.target_set_operator("purp.upperradiusgizmo")
        upradius.use_draw_offset_scale = True
        upradius.matrix_basis = ob.matrix_world.normalized()
        upradius.use_draw_value = True

        upradius.matrix_offset[0][3] -= 3
        upradius.matrix_offset[2][3] += 3
        # mps.matrix_basis[0][3] += 0.5
        upradius.line_width = 3

        upradius.color = 0.4, 0.8, 0.03
        upradius.alpha = 0.5

        upradius.color_highlight = 0.5, 1.0, 0.04
        upradius.alpha_highlight = 1.0
        upradius.scale_basis = 0.4

        self.upRadius = upradius

        mpthickness = self.gizmos.new(PUrP_ThicknessShapeWidget.bl_idname)
        props = mpthickness.target_set_operator("purp.singthicknessgiz")
        mpthickness.use_draw_offset_scale = True
        mpthickness.matrix_basis = ob.matrix_world.normalized()
        mpthickness.use_draw_value = True
        mat_rot1 = mathutils.Matrix.Rotation(radians(90.0), 4, 'X')  # rotate
        mat_trans = mathutils.Matrix.Translation(mathutils.Vector((0, 0, 0)))
        mat = mat_trans @ mat_rot1
        mpthickness.matrix_offset = mat

        # mps.matrix_offset[2][0] = 0.2
        # mps.matrix_offset[2][2] = 0.5
        mpthickness.matrix_offset[2][3] -= 0.5
        # mps.matrix_basis[0][3] += 0.5
        mpthickness.line_width = 3

        mpthickness.color = 0.03, 0.8, 0.03
        mpthickness.alpha = 0.5

        mpthickness.color_highlight = 0.01, 1.0, 0.01
        mpthickness.alpha_highlight = 1.0
        mpthickness.scale_basis = 2

        self.thickness = mpthickness

    def refresh(self, context):
        ob = context.object
        children = context.object.children
        # order correction
        for child in children:
            if "diff" in child.name:
                self.obout = child
            elif "fix" in child.name or "union" in child.name:
                self.obin = child

        # oversize
        mpr = self.roll_widget
        mpr.matrix_basis = ob.matrix_world.normalized()
        mpr.matrix_offset[2][3] = 2

        # couplesize
        mpa = self.roll_widge
        mpa.matrix_basis = ob.matrix_world.normalized()
        mpa.matrix_offset[2][3] = 0

        # zScale
        mph = self.roll_widg
        mph.matrix_basis = ob.matrix_world.normalized()
        mph.scale_basis = 0.5
        mph.matrix_offset[2][3] = 3

        # bev offset
        mpo = self.roll_wid
        mpo.matrix_basis = ob.matrix_world.normalized()
        mpo.matrix_offset[0][3] = 2
        mpo.matrix_offset[2][3] = 2

        mps = self.bevseggizm
        if context.scene.PUrP.BevelOffset > 0:
            # bev segment
            mps.matrix_basis = ob.matrix_world.normalized()
            mps.matrix_offset[0][3] = 3
            mps.matrix_offset[2][3] = 3
            mps.scale_basis = 0.2
        else:
            mps.scale_basis = 0.0001

        mcsize = self.couplingScale
        mcsize.matrix_basis = ob.matrix_world.normalized()
        mcsize.matrix_offset[2][3] = -0.5

        lowradius = self.lowRadius
        lowradius.matrix_basis = ob.matrix_world.normalized()
        upradius = self.upRadius
        upradius.matrix_basis = ob.matrix_world.normalized()
        if "Cone" in self.obout.data.name:

            lowradius.scale_basis = 0.4
            upradius.scale_basis = 0.4
        else:
            lowradius.scale_basis = 0.0
            upradius.scale_basis = 0.0

        if len(children) == 0:
            mpr.scale_basis = 0.0
            mpa.scale_basis = 0.0
            mph.scale_basis = 0.0
            mpo.scale_basis = 0.0
            mps.scale_basis = 0.0
            # mcsize.scale_basis = 0.0
            lowradius.scale_basis = 0.0
            upradius.scale_basis = 0.0

        mpthickness = self.thickness
        mpthickness.matrix_basis = ob.matrix_world

# flatcut gizmot


class PUrP_FlatCoupGizmo(GizmoGroup):
    bl_idname = "OBJECT_FLAT_coup_camera"
    bl_label = "Object Camera Test Widget"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT'}

    @classmethod
    def poll(cls, context):

        ob = context.object

        if ob != None:
            if ("PUrP" in ob.name) and ("diff" and "fix" and "union" and "Planar" not in ob.name):
                if len(ob.children) == 0 or len(ob.children) == 1:  # flatcut has zero or
                    try:
                        test = context.scene.PUrP.GlobalScale
                        return True
                    except:
                        return False
                return False

            return False

    def setup(self, context):
        ob = context.object

        mcsize = self.gizmos.new("GIZMO_GT_dial_3d")
        mcsize.target_set_operator("purp.flatcoupscalegizmo")  # needs operator
        mcsize.use_draw_offset_scale = True
        mcsize.matrix_basis = ob.matrix_world.normalized()
        mcsize.use_draw_value = True
        mcsize.line_width = 3
        mcsize.matrix_offset[2][3] = -0.5

        mcsize.color = 0.03, 0.8, 0.03
        mcsize.alpha = 0.5

        mcsize.color_highlight = 0.01, 1.0, 0.01
        mcsize.alpha_highlight = 1.0
        mcsize.scale_basis = 2

        self.couplingScale = mcsize

        mpthickness = self.gizmos.new(PUrP_ThicknessShapeWidget.bl_idname)
        props = mpthickness.target_set_operator("purp.singthicknessgiz")
        mpthickness.use_draw_offset_scale = True
        mpthickness.matrix_basis = ob.matrix_world.normalized()
        mpthickness.use_draw_value = True
        mat_rot1 = mathutils.Matrix.Rotation(radians(90.0), 4, 'X')  # rotate
        mat_trans = mathutils.Matrix.Translation(mathutils.Vector((0, 0, 0)))
        mat = mat_trans @ mat_rot1
        mpthickness.matrix_offset = mat

        # mps.matrix_offset[2][0] = 0.2
        # mps.matrix_offset[2][2] = 0.5
        mpthickness.matrix_offset[2][3] -= 0.5
        # mps.matrix_basis[0][3] += 0.5
        mpthickness.line_width = 3

        mpthickness.color = 0.03, 0.8, 0.03
        mpthickness.alpha = 0.5

        mpthickness.color_highlight = 0.01, 1.0, 0.01
        mpthickness.alpha_highlight = 1.0
        mpthickness.scale_basis = 2

        self.thickness = mpthickness

    def refresh(self, context):
        ob = context.object
        mcsize = self.couplingScale
        mcsize.matrix_basis = ob.matrix_world

        mpthickness = self.thickness
        mpthickness.matrix_basis = ob.matrix_world
        # planar connector gizmos


class PP_OT_FlatCoupScaleGizmo(bpy.types.Operator):
    '''Change Connector Size'''
    bl_idname = "purp.flatcoupscalegizmo"
    bl_label = "couplsize"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):
        PUrP = context.scene.PUrP
        ob = context.object

        ob.scale = self.value
        # bpy.ops.object.transform_apply(
        #    location=False, rotation=False, scale=True)

        # applyScalRot(self.obout)
        # applyScalRot(self.obin)

        # oversizeToPrim(context, singcoupmode(
        #    context, None, context.object), self.obout, self.obin)

        PUrP.CoupScale = ob.data.vertices[1].co.x * \
            self.value[0] / (3 * PUrP.GlobalScale)
        # print(self.value)
        return {'FINISHED'}

    def modal(self, context, event):
        ob = context.object
        if event.type == 'MOUSEMOVE':  # Apply
            sensi = 1000 if not event.shift else 10000
            self.delta = event.mouse_x - self.init_value
            self.value = self.init_scale + \
                mathutils.Vector(
                    (self.delta / sensi, self.delta / sensi, self.delta / sensi))

            self.execute(context)
        elif event.type == 'LEFTMOUSE':  # Confirm
            bpy.ops.object.transform_apply(
                location=False, rotation=False, scale=True)
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            ob.scale = self.init_scale
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        '''
        children = context.object.children
        # order correction
        for child in children:
            if "diff" in child.name:
                self.obout = child
            elif "fix" in child.name or "union" in child.name:
                self.obin = child
        '''
        ob = context.object
        self.init_scale = ob.scale.copy()
        self.init_value = event.mouse_x
        # event.mouse_x #- self.window_width/21   ################mach mal start value einfach 00
        self.value = ob.scale
        self.execute(context)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


def has_stopper(obj):
    lowestvert = 0
    for vert in obj.data.vertices:  # find lowest z coordinate
        if vert.co.z <= lowestvert:
            lowestvert = vert.co.z

    lowestlist = []
    lowestexample = obj.data.vertices[0]
    for vert in obj.data.vertices:  # collect all verts with lowest co.z values
        if vert.co.z == lowestvert:
            lowestlist.append(vert.co.z)
            lowestexample = vert  # example for stopperheight evaluation

    # PUrP.StopperBool = False
    if len(lowestlist) == 4:  # with 4 verts its a stopper
        return True
    return False


class PUrP_PlanarGizmo(GizmoGroup):
    bl_idname = "OBJECT_GGT_PLANARCONNECTOR"
    bl_label = "Object Camera Test Widget"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT'}

    @classmethod
    def poll(cls, context):
        ob = context.object

        if ob != None:
            if ("PUrP" in ob.name) and ("Planar" in ob.name):
                try:
                    test = context.scene.PUrP.GlobalScale
                    return True
                except:
                    return False
            return False

    def setup(self, context):
        # Run an operator using the dial gizmo
        ob = context.object

        mpr = self.gizmos.new(PUrP_ArrowUpShapeWidget.bl_idname)
        props = mpr.target_set_operator("purp.roffsetgiz")

        mpr.matrix_basis = ob.matrix_world.normalized()
        mpr.use_draw_offset_scale = True
        mat_rot1 = mathutils.Matrix.Rotation(radians(90.0), 4, 'Y')  # rotate
        # mat_rot2 = mathutils.Matrix.Rotation(radians(90.0), 4, 'Y')  # rotate

        # mat_rot = mat_rot1 @ mat_rot2
        # mat_trans = mathutils.Matrix.Translation(ob.location)
        mat_trans = mathutils.Matrix.Translation(mathutils.Vector((0, 0, 0)))
        mat = mat_trans @ mat_rot1
        mpr.matrix_offset = mat
        mpr.matrix_offset[0][3] = 1.5
        # mpr.matrix_offset[0][3] = 1
        mpr.select_bias = 5
        # mpr.scale_basis = 0.5
        mpr.line_width = 50
        mpr.color = 0.05, 0.2, 0.8
        mpr.alpha = 0.5
        mpr.color_highlight = 0.03, 0.05, 1.0
        mpr.alpha_highlight = 1.0

        self.Roffset = mpr

        # left offset
        mpl = self.gizmos.new(PUrP_ArrowUpShapeWidget.bl_idname)
        props = mpl.target_set_operator("purp.loffsetgiz")
        mpl.use_draw_offset_scale = True
        # props.constraint_axis = True, True, True
        # props.orient_type = 'LOCAL'
        # props.release_confirm = True

        mpl.matrix_basis = ob.matrix_world.normalized()

        # mat_rot1 = mathutils.Matrix.Rotation(radians(90.0), 4, 'Z')  # rotate
        mat_rot2 = mathutils.Matrix.Rotation(radians(-90.0), 4, 'Y')  # rotate

        # mat_rot = mat_rot1 @ mat_rot2
        mat_trans = mathutils.Matrix.Translation(mathutils.Vector((0, 0, 0)))
        mat = mat_trans @ mat_rot2
        mpl.matrix_offset = mat
        # mpl.matrix_basis[0][3] += 0.4

        # mpl.scale_basis = 0.5
        mpl.line_width = 3
        mpl.color = 0.05, 0.2, 0.8
        mpl.alpha = 0.5
        mpl.color_highlight = 0.03, 0.05, 1.0
        mpl.alpha_highlight = 1.0

        self.Loffset = mpl

        # zscale
        mpz = self.gizmos.new(PUrP_ArrowUpShapeWidget.bl_idname)
        props = mpz.target_set_operator("purp.planzscalegiz")
        # props.constraint_axis = True, True, True
        # props.orient_type = 'LOCAL'
        # props.release_confirm = True

        mpz.matrix_basis = ob.matrix_world.normalized()
        mpz.use_draw_offset_scale = True
        mpz.matrix_offset[2][3] = 1.5

        mpz.scale_basis = 1
        mpz.line_width = 3
        mpz.color = 0.8, 0.05, 0.05
        mpz.alpha = 0.5
        mpz.color_highlight = 1.0, 0.05, 0.05
        mpz.alpha_highlight = 1.0

        self.zScale = mpz

        # stopper scale

        # if has_stopper():
        mps = self.gizmos.new(PUrP_ArrowUpShapeWidget.bl_idname)
        props = mps.target_set_operator("purp.stopperheightgiz")
        mps.use_draw_offset_scale = True
        # props.constraint_axis = True, True, True
        # props.orient_type = 'LOCAL'
        # props.release_confirm = True

        mps.matrix_basis = ob.matrix_world.normalized()

        #
        # mat_rot1 = mathutils.Matrix.Rotation(radians(90.0), 4, 'Z')  # rotate
        mat_rot2 = mathutils.Matrix.Rotation(
            radians(180.0), 4, 'Y')  # rotate

        # mat_rot = mat_rot1 @ mat_rot2
        mat_trans = mathutils.Matrix.Translation(ob.location)
        mat = mat_trans @ mat_rot2
        mps.matrix_basis = mat

        mps.line_width = 3
        mps.color = 0.8, 0.05, 0.05
        mps.alpha = 0.5
        mps.color_highlight = 1.0, 0.05, 0.05
        mps.alpha_highlight = 1.0

        self.stopper = mps

        # lineCount

        mpcount = self.gizmos.new(PUrP_linecountShapeWidget.bl_idname)
        props = mpcount.target_set_operator("purp.linecountgiz")

        mpcount.matrix_basis = ob.matrix_world.normalized()
        mpcount.use_draw_offset_scale = True
        mpcount.matrix_offset[2][3] = 1
        mpcount.matrix_offset[0][3] = 1
        mpcount.matrix_offset[1][3] = 1

        mpcount.scale_basis = 1
        mpcount.line_width = 3
        mpcount.color = 0.8, 0.4, 0.1
        mpcount.alpha = 0.5
        mpcount.color_highlight = 1, 0.5, 0.1
        mpcount.alpha_highlight = 1.0

        self.linecount = mpcount

        # linelength

        mplength = self.gizmos.new(PUrP_LineLengthShapeWidget.bl_idname)
        props = mplength.target_set_operator("purp.linelengthgiz")

        mplength.matrix_basis = ob.matrix_world.normalized()
        mplength.use_draw_offset_scale = True
        mplength.matrix_offset[2][3] = 1
        mplength.matrix_offset[1][3] = 1
        mplength.matrix_offset[2][3] = -1

        mplength.scale_basis = 1
        mplength.line_width = 3
        mplength.color = 0.8, 0.4, 0.1
        mplength.alpha = 0.5
        mplength.color_highlight = 1.0, 0.5, 0.3
        mplength.alpha_highlight = 1.0

        self.linelength = mplength

        # linedistance

        mpdistance = self.gizmos.new(PUrP_LineDistanceShapeWidget.bl_idname)
        # mpcount.target_set_prop("offset", context.scene.PUrP, "LineCount")
        props = mpdistance.target_set_operator("purp.linedistancegiz")
        # props.constraint_axis = True, True, True
        # props.orient_type = 'LOCAL'
        # props.release_confirm = True

        mpdistance.matrix_basis = ob.matrix_world.normalized()
        mpdistance.use_draw_offset_scale = True
        mpdistance.matrix_offset[2][3] = 1
        mpdistance.matrix_offset[0][3] = -1
        mpdistance.matrix_offset[1][3] = -1
        mpdistance.scale_basis = 1

        mpdistance.line_width = 3
        mpdistance.color = 0.8, 0.4, 0.05
        mpdistance.alpha = 0.5
        mpdistance.color_highlight = 1.0, 0.5, 0.05
        mpdistance.alpha_highlight = 1.0

        self.linedistance = mpdistance

        # thickness

        mpthickness = self.gizmos.new(PUrP_ThicknessShapeWidget.bl_idname)
        props = mpthickness.target_set_operator("purp.thicknessgiz")

        mpthickness.matrix_basis = ob.matrix_world.normalized()
        mpthickness.use_draw_offset_scale = True
        mpthickness.matrix_offset[2][3] = 1
        mpthickness.matrix_offset[1][3] = -1
        mpthickness.matrix_offset[0][3] = 1

        mpthickness.scale_basis = 1
        mpthickness.line_width = 20
        mpthickness.color = 0.05, 0.8, 0.8
        mpthickness.alpha = 0.5
        mpthickness.color_highlight = 0.03, 1.0, 1.0
        mpthickness.alpha_highlight = 1.0

        self.thickness = mpthickness

        # connectorsize
        mcsize = self.gizmos.new("GIZMO_GT_dial_3d")
        mcsize.target_set_operator("purp.planarcoupscalegizmo")

        mcsize.use_draw_offset_scale = True
        mcsize.matrix_basis = ob.matrix_world.normalized()
        mcsize.use_draw_value = True
        # mps.matrix_offset[2][0] = 0.2
        # mps.matrix_offset[2][2] = 0.5
        # mps.matrix_basis[2][3] += 0.8
        # mps.matrix_basis[0][3] += 0.5
        mcsize.line_width = 3

        mcsize.color = 0.03, 0.8, 0.03
        mcsize.alpha = 0.5

        mcsize.color_highlight = 0.01, 1.0, 0.01
        mcsize.alpha_highlight = 1.0
        mcsize.scale_basis = 2

        self.couplingScale = mcsize

    def refresh(self, context):
        ob = context.object
        # if has_stopper(ob):
        mpr = self.Roffset
        mpr.matrix_basis = ob.matrix_world.normalized()
        # mpr.matrix_offset[0][3] = 1.5

        mpl = self.Loffset
        mpl.matrix_basis = ob.matrix_world.normalized()
        mpl.matrix_offset[0][3] = -1.5

        mpz = self.zScale
        mpz.matrix_basis = ob.matrix_world.normalized()
        mpz.matrix_offset[2][3] = 1.5

        if has_stopper(ob):
            mps = self.stopper

            mat_rot2 = mathutils.Matrix.Rotation(
                radians(180.0), 4, 'Y')  # rotate
            mat_trans = mathutils.Matrix.Translation(ob.location)
            mat = mat_trans @ mat_rot2
            mps.matrix_basis = ob.matrix_world.normalized()
            mps.matrix_offset = mat_rot2
            mps.matrix_offset[2][3] = -1.5
            mps.scale_basis = 1
        else:

            mps = self.stopper
            mps.matrix_basis = ob.matrix_world.normalized()
            mps.matrix_basis[2][3] = +1.5
            mps.scale_basis = 0.0001

        mpcount = self.linecount
        mpcount.matrix_basis = ob.matrix_world.normalized()
        mpcount.matrix_offset[2][3] = 1
        mpcount.matrix_offset[0][3] = 1
        mpcount.matrix_offset[1][3] = 1
        mpcount.scale_basis = 1

        mplength = self.linelength
        mplength.matrix_basis = ob.matrix_world.normalized()
        mplength.matrix_offset[2][3] = 1
        mplength.matrix_offset[0][3] = -1
        mplength.matrix_offset[1][3] = 1
        mplength.scale_basis = 1

        mpdistance = self.linedistance
        if context.scene.PUrP.LineCount > 1:  # disable when there is only one line
            mpdistance.matrix_basis = ob.matrix_world.normalized()
            mpdistance.matrix_offset[2][3] = 1
            mpdistance.matrix_offset[0][3] = -1
            mpdistance.matrix_offset[1][3] = -1
            mpdistance.scale_basis = 1
        else:
            mpdistance.scale_basis = 0.0001

        mpthickness = self.thickness
        mpthickness.matrix_basis = ob.matrix_world.normalized()
        mpthickness.matrix_offset[2][3] = +1
        mpthickness.matrix_offset[0][3] = +1
        mpthickness.matrix_offset[1][3] = -1
        mpthickness.scale_basis = 1

        mcsize = self.couplingScale
        mcsize.matrix_basis = ob.matrix_world.normalized()
        mcsize.matrix_offset[2][3] = -0.5


class PP_OT_PlanarRoffsetGizmo(bpy.types.Operator):
    '''Change the right offset of the coupling'''
    bl_idname = "purp.roffsetgiz"
    bl_label = "couplsize"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):
        ob = context.object
        PUrP = context.scene.PUrP
        korrvalue = self.value - 1.5*self.coupfaktor * PUrP.CoupScale
        PUrP.OffsetRight = korrvalue
        print(self.value)
        if korrvalue >= 0:
            for v in self.rightestV:
                v.co.x = self.value
            else:
                pass

        # context.scene.PUrP.OffsetRight = ob.data.vertices[0].co.x - \
        #    1.5*self.coupfaktor * PUrP.CoupScale
        return {'FINISHED'}

    def modal(self, context, event):
        PUrP = context.scene.PUrP
        # * PUrP.GlobalScale
        if event.type == 'MOUSEMOVE':  # Apply
            sensi = 100 if not event.shift else 1000
            self.delta = event.mouse_x - self.init_value
            self.value = self.init_position + self.delta * PUrP.GlobalScale / sensi

            self.execute(context)
        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            for v in self.rightestV:
                v.co.x = self.init_position

            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        ob = context.object
        #
        rightestx = 0
        for v in ob.data.vertices:
            if v.co.x > rightestx:
                rightestx = v.co.x
        # rightestx is now
        self.rightestV = []
        for v in ob.data.vertices:
            if rightestx == v.co.x:
                self.rightestV.append(v)
        self.init_position = rightestx
        self.init_value = event.mouse_x

        # event.mouse_x #- self.window_width/21   ################mach mal start value einfach 00
        self.value = rightestx  # ???

        PUrP = context.scene.PUrP
        self.coupfaktor = PUrP.PlanarCorScale * PUrP.GlobalScale
        PUrP.CoupScale = ob.data.vertices[3].co.x / self.coupfaktor

        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class PP_OT_PlanarLoffsetGizmo(bpy.types.Operator):
    '''Change the left offset of the coupling'''
    bl_idname = "purp.loffsetgiz"
    bl_label = "couplsize"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):
        ob = context.object
        PUrP = context.scene.PUrP
        korrvalue = -self.value - 1.5*self.coupfaktor * PUrP.CoupScale
        PUrP.OffsetLeft = korrvalue
        print(self.value)
        if korrvalue >= 0:
            for v in self.leftestV:
                v.co.x = self.value
            else:
                pass

        # PUrP.OffsetLeft = - \
        #    ob.data.vertices[1].co.x - 1.5*self.coupfaktor * PUrP.CoupScale
        return {'FINISHED'}

    def modal(self, context, event):
        PUrP = context.scene.PUrP

        if event.type == 'MOUSEMOVE':  # Apply
            sensi = 100 if not event.shift else 1000
            self.delta = event.mouse_x - self.init_value
            self.value = self.init_position + self.delta * PUrP.GlobalScale / sensi

            self.execute(context)
        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            for v in self.leftestV:
                v.co.x = self.init_position

            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        ob = context.object
        #
        leftestx = 0
        for v in ob.data.vertices:
            if v.co.x < leftestx:
                leftestx = v.co.x
        # rightestx is now
        self.leftestV = []
        for v in ob.data.vertices:
            if leftestx == v.co.x:
                self.leftestV.append(v)
        self.init_position = leftestx
        self.init_value = event.mouse_x

        # event.mouse_x #- self.window_width/21   ################mach mal start value einfach 00
        self.value = leftestx  # ???

        PUrP = context.scene.PUrP
        self.coupfaktor = PUrP.PlanarCorScale * PUrP.GlobalScale
        PUrP.CoupScale = ob.data.vertices[3].co.x / self.coupfaktor

        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class PP_OT_PlanarzScaleGizmo(bpy.types.Operator):
    '''Change the Zscale of the coupling'''
    bl_idname = "purp.planzscalegiz"
    bl_label = "couplsize"
    bl_options = {'REGISTER', "UNDO"}

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
            sensi = 100 if not event.shift else 1000
            self.delta = event.mouse_y - self.init_value
            self.valuelow = self.lowestz + self.delta * PUrP.GlobalScale / sensi
            # if self.has_stopper:
            self.valuemiddle = self.middlez + self.delta / sensi

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


class PP_OT_PlanarStopperHeightGizmo(bpy.types.Operator):
    '''Change the Zscale of the coupling'''
    bl_idname = "purp.stopperheightgiz"
    bl_label = "couplsize"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):
        zscale = -context.scene.PUrP.zScale
        if self.value - zscale >= 0:
            for v in self.lowestV:
                v.co.z = zscale - 0.01
            context.scene.PUrP.StopperHeight = 0.01
        else:
            for v in self.lowestV:
                v.co.z = self.value
            context.scene.PUrP.StopperHeight = -self.value + zscale
        return {'FINISHED'}

    def modal(self, context, event):
        PUrP = context.scene.PUrP
        if event.type == 'MOUSEMOVE':  # Apply
            sensi = 100 if not event.shift else 1000
            self.delta = event.mouse_y - self.init_value
            self.value = self.lowestz + self.delta * PUrP.GlobalScale / 1000

            self.execute(context)

        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            for v in self.lowestV:
                v.co.z = self.lowestz

            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        ob = context.object
        self.lowestV = []
        self.lowestz = 0
        for v in ob.data.vertices:
            if v.co.z < self.lowestz:
                self.lowestz = v.co.z

        for v in ob.data.vertices:
            if v.co.z == self.lowestz:
                self.lowestV.append(v)
            # coordinaten aller

        # self.init_position1 = lowestz
        # self.init_position2 = self.middlez

        self.init_value = event.mouse_y

        # event.mouse_x #- self.window_width/21   ################mach mal start value einfach 00
        self.value = self.lowestz

        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class PP_OT_PlanarLineCountGizmo(bpy.types.Operator):
    '''Change the Zscale of the coupling'''
    bl_idname = "purp.linecountgiz"
    bl_label = "couplsize"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):
        ob = context.object
        ob.modifiers["PUrP_Array_2"].count = int(self.value)

        context.scene.PUrP.LineCount = int(self.value)
        return {'FINISHED'}

    def modal(self, context, event):

        if event.type == 'MOUSEMOVE':  # Apply
            sensi = 100 if not event.shift else 1000
            self.delta = event.mouse_y - self.init_value
            self.value = self.init_count + self.delta / sensi

            self.execute(context)

        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            ob.modifiers["PUrP_Array_2"].count = self.init_count

            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        ob = context.object

        self.init_value = event.mouse_y

        # event.mouse_x #- self.window_width/21   ################mach mal start value einfach 00
        self.value = ob.modifiers["PUrP_Array_2"].count

        self.init_count = ob.modifiers["PUrP_Array_2"].count

        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class PP_OT_PlanarLineLengthGizmo(bpy.types.Operator):
    '''Change the Zscale of the coupling'''
    bl_idname = "purp.linelengthgiz"
    bl_label = "couplsize"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):
        ob = context.object
        ob.modifiers["PUrP_Array_1"].count = int(self.value)

        context.scene.PUrP.LineLength = int(self.value)
        return {'FINISHED'}

    def modal(self, context, event):

        if event.type == 'MOUSEMOVE':  # Apply
            sensi = 100 if not event.shift else 1000
            self.delta = event.mouse_y - self.init_value
            self.value = self.init_count + self.delta / sensi

            self.execute(context)

        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            ob.modifiers["PUrP_Array_1"].count = self.init_count

            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        ob = context.object

        self.init_value = event.mouse_y

        # event.mouse_x #- self.window_width/21   ################mach mal start value einfach 00
        self.value = ob.modifiers["PUrP_Array_1"].count

        self.init_count = ob.modifiers["PUrP_Array_1"].count

        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class PP_OT_PlanarLineDistanceGizmo(bpy.types.Operator):
    '''Change the Zscale of the coupling'''
    bl_idname = "purp.linedistancegiz"
    bl_label = "couplsize"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):
        ob = context.object

        ob.modifiers["PUrP_Array_2"].constant_offset_displace[1] = self.value

        context.scene.PUrP.LineDistance = self.value
        return {'FINISHED'}

    def modal(self, context, event):

        if event.type == 'MOUSEMOVE':  # Apply
            sensi = 100 if not event.shift else 1000
            self.delta = event.mouse_y - self.init_value
            self.value = self.init_count + self.delta * self.GlobalScale / sensi

            self.execute(context)

        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            ob.modifiers["PUrP_Array_2"].relative_offset_displace[1] = self.init_count

            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        ob = context.object
        self.GlobalScale = context.scene.PUrP.GlobalScale
        self.init_value = event.mouse_y

        # event.mouse_x #- self.window_width/21   ################mach mal start value einfach 00
        self.value = ob.modifiers["PUrP_Array_2"].constant_offset_displace[1]

        self.init_count = ob.modifiers["PUrP_Array_2"].constant_offset_displace[1]

        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class PP_OT_PlanarThicknessGizmo(bpy.types.Operator):
    '''Change the Oversize (Thickness) of the planar connector'''
    bl_idname = "purp.thicknessgiz"
    bl_label = "couplsize"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):
        ob = context.object

        if self.value <= 0:
            ob.modifiers["PUrP_Solidify"].thickness = 0
            context.scene.PUrP.Oversize = 0
        else:
            ob.modifiers["PUrP_Solidify"].thickness = self.value * \
                self.GlobalScale
            context.scene.PUrP.Oversize = self.value
        return {'FINISHED'}

    def modal(self, context, event):
        ob = context.object
        if event.type == 'MOUSEMOVE':  # Apply
            sensi = 1000 if not event.shift else 10000
            self.delta = event.mouse_y - self.init_value
            self.value = self.init_count + self.delta / sensi
            print(
                f"self.value {self.value}   self.delta {self.delta}  self.init_value {self.init_value} ")
            self.execute(context)

        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            ob.modifiers["PUrP_Solidify"].thickness = self.init_count * \
                self.GlobalScale
            self.GlobalScale

            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        ob = context.object
        PUrP = context.scene.PUrP
        self.GlobalScale = PUrP.GlobalScale
        self.init_value = event.mouse_y

        # event.mouse_x #- self.window_width/21   ################mach mal start value einfach 00
        self.value = ob.modifiers["PUrP_Solidify"].thickness / self.GlobalScale

        # helpi = [str(ob.modifiers["PUrP_Solidify"].thickness)]

        # float(helpi[0])
        self.init_count = ob.modifiers["PUrP_Solidify"].thickness / \
            self.GlobalScale

        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class PP_OT_PlanarCoupScaleGizmo(bpy.types.Operator):
    '''Change the Connector Scale '''
    bl_idname = "purp.planarcoupscalegizmo"
    bl_label = "couplscale"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        if ("PUrP" in context.object.name) and ("diff" and "fix" and "union" and "Single" not in context.object.name):
            return True
        else:
            return False

    def execute(self, context):
        PUrP = context.scene.PUrP
        ob = context.object

        ob.scale = self.value
        print(self.value)

        coupfaktor = PUrP.PlanarCorScale * PUrP.GlobalScale
        vx3 = ob.data.vertices[3].co.x*ob.scale.x
        print(
            f"vx3 co{ob.data.vertices[3].co} scale{ob.scale[0]} vx3 {vx3} coupscale {abs(vx3) / coupfaktor}  ")
        PUrP.CoupScale = abs(vx3) / coupfaktor
        PUrP.OffsetRight, PUrP.OffsetLeft, PUrP.zScale, PUrP.StopperHeight = planaranalysizerGlobal(
            context, ob)

        return {'FINISHED'}

    def modal(self, context, event):
        ob = context.object

        if event.type == 'MOUSEMOVE':  # Apply
            sensi = 1000 if not event.shift else 10000
            self.delta = event.mouse_x - self.init_value
            print(
                f"mouse x {event.mouse_x} self.init_value {self.init_value} self.delta {self.delta} self.value {self.value} ")
            self.value = self.init_scale + \
                mathutils.Vector(
                    (self.delta / sensi, self.delta / sensi, self.delta / sensi))

            self.execute(context)
        elif event.type == 'LEFTMOUSE':  # Confirm
            PUrP = context.scene.PUrP
            bpy.ops.object.transform_apply(
                location=False, rotation=False, scale=True)
            coupfaktor = PUrP.PlanarCorScale * PUrP.GlobalScale
            vx3 = ob.data.vertices[3].co.x*ob.scale.x
            PUrP.CoupScale = abs(vx3) / coupfaktor
            PUrP.OffsetRight, PUrP.OffsetLeft, PUrP.zScale, PUrP.StopperHeight = planaranalysizerLocal(
                context, ob)
            # applyScalRot(self.obout)
            # applyScalRot(self.obin)
            # oversizeToPrim(context, singcoupmode(
            #    context, None, context.object), self.obout, self.obin)
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            ob.scale = self.init_scale
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        print("Hallo invoke")
        ob = context.object
        self.init_scale = ob.scale.copy()
        self.init_value = event.mouse_x
        # event.mouse_x #- self.window_width/21   ################mach mal start value einfach 00
        self.value = ob.scale
        self.execute(context)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
