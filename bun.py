#
# Copyright (C) 2020 by Modicolitor
#
# This file is part of PuzzleUrPrint.
#
# License Text
#
# You should have received a copy of the GNU General Public License along with PuzzleUrPrint. If
# not, see <https://www.gnu.org/licenses/>.

from re import A
import bmesh
import bpy
import mathutils
from math import radians, sqrt
import numpy as np
from bpy.types import Scene, Image, Object
import random
import os
# from .intersect import bmesh_check_intersect_objects
from .bvh_overlap import bvhOverlap
from .warning import noCutthroughWarn, coneTrouble, noVertsWarn
from . gen_mesh import gen_figure, gen_hat, gen_arrow
import copy


# from .properties import PUrPropertyGroup

'''Operator in Blender'''


class PP_OT_AddSingleCoupling(bpy.types.Operator):
    '''Add a new Connector to the scene at the position of the 3D cursor. It will be mapped to the selected or the last center object and  the shape will be defined by the current settings in this panel.'''

    bl_label = "Add Single Couplings"
    bl_idname = "add.coup"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        # PUrP = context.scene.PUrP
        if context.mode == 'OBJECT' and context.area.type == 'VIEW_3D':
            if (context.view_layer.objects.active != None) and context.view_layer.objects.active.select_get():
                if context.object.type == 'MESH':
                    if not is_coup(context, context.object) or context.scene.PUrP.CenterObj != None:
                        return True

            elif context.scene.PUrP.CenterObj != None:
                return True
            if context.scene.PUrP.AddUnmapped:
                return True
        return False

    def execute(self, context):
        # createSingleCoupling()
        context = bpy.context
        data = bpy.data
        active = context.view_layer.objects.active
        PUrP = context.scene.PUrP
        CenterObj = PUrP.CenterObj
        PUrP_name = PUrP.PUrP_name
        CutThickness = PUrP.CutThickness
        # Oversize = PUrP.Oversize
        GlobalScale = PUrP.GlobalScale
        cursorloc = context.scene.cursor.location
        cursorlocori = context.scene.cursor.location
        add_unmap = PUrP.AddUnmapped

        # Prim = self.PrimTypes

        deselectall(context)

        # handling CenterObj ###############
        # try to test if the object is not deleted

        # find CenterObj
        if not add_unmap:
            if active != None:
                if active.type == "MESH":
                    if is_coup(context, active) or is_buildvolume(context, active):
                        CenterObj = PUrP.CenterObj
                    else:
                        CenterObj = active
                        PUrP.CenterObj = CenterObj
            # else:
            if PUrP.CenterObj != None:
                if not is_coup(context, PUrP.CenterObj):
                    if not in_view_layer(context, PUrP.CenterObj):
                        print(
                            f"evaluation {in_view_layer(context, PUrP.CenterObj)}")
                        self.report(
                            {'WARNING'}, "Set Centerobject doesn't exist anymore. Please select a mesh object")
                        return{"FINISHED"}
                    else:

                        active = PUrP.CenterObj
                        active.select_set(True)
                else:
                    self.report(
                        {'WARNING'}, "A connector cannot be a Centerobj. Please select another mesh object")
                    return{"FINISHED"}
            else:
                if not add_unmap:
                    self.report(
                        {'WARNING'}, "No, centerobject selected or set. Please select a mesh object")
                    return{"FINISHED"}

            # apply scale to CenterObj
            # bpy.ops.object.transform_apply(
            #    location=False, rotation=False, scale=True)  # changed rotation to False is, that a problem for planar and stuff? But actually should

            CenterObj_name = CenterObj.name
            CenterObj.PUrPCobj = True
            Centerloc = CenterObj.location
            ensurenoscaling(context, CenterObj)
        # make main cut plane when not planar
        if PUrP.SingleCouplingModes != "4":

            newmain = genSinglemain(
                context, CenterObj, PUrP.SingleMainTypes, add_unmap)
            newname_mainplane = newmain.name
            # context.object.scale *= PUrP.GlobalScale * PUrP.CoupScale
            # bpy.ops.object.transform_apply(
            #    location=False, rotation=False, scale=True)

            if not add_unmap:
                context.object.parent = data.objects[CenterObj_name]
                # set boolean for the slice plane
                mod = data.objects[CenterObj_name].modifiers.new(
                    name=context.object.name, type="BOOLEAN")
                mod.show_viewport = False
                if PUrP.ViewPortVisAdd:
                    mod.show_viewport = True
                mod.object = newmain
                mod.operation = 'DIFFERENCE'
                set_BoolSolver(context, mod)

        else:
            newname_mainplane = "Null"  # for planar

        newMain = coupModeDivision(context, CenterObj, newname_mainplane,
                                   add_unmap, PUrP.ViewPortVisAdd)

        # compensate Cobjs rotation, setting world_matrix to scale and rot 1
        newMain.matrix_world = ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1,
                                                             0), (cursorloc[0], cursorloc[1], cursorloc[2], 1))

        # order refreshing
        if not add_unmap:
            if PUrP.OrderBool:
                update_order(context, CenterObj)
        else:
            unmapped_signal(context, newMain)

        newMain.select_set(True)
        return{"FINISHED"}


def deselectall(context):
    selected = context.selected_objects[:]
    for ob in selected:
        ob.select_set(False)


def in_view_layer(context, ob):
    tester = False
    for obj in context.view_layer.objects:
        if ob == obj:
            return True

    return False


def coupModeDivision(context, CenterObj, newname_mainplane, is_unmapped, visibility):
    data = bpy.data

    PUrP = bpy.context.scene.PUrP
    # Oversize = PUrP.Oversize
    # zScale = PUrP.zScale
    GlobalScale = PUrP.GlobalScale
    print(f"CenterObj in coupmode division {CenterObj}")
    if PUrP.SingleCouplingModes == "3":                     # flatCut
        bpy.data.objects[newname_mainplane].scale = mathutils.Vector((1, 1, 1))
        newMain = data.objects[newname_mainplane]

    elif PUrP.SingleCouplingModes == "2":  # Male - female
        bpy.data.objects[newname_mainplane].scale = mathutils.Vector((1, 1, 1))
        # add negativ object
        # loc.z += 0.45
        ob0 = genPrimitive(CenterObj, newname_mainplane, '_diff', is_unmapped)
        ob0.hide_select = True

        # add positiv object
        ob1 = genPrimitive(CenterObj, newname_mainplane, '_union', is_unmapped)
        oversizeToPrim(context, singcoupmode(context, "2", None), ob0, ob1)
        ob1.hide_select = True
        newMain = data.objects[newname_mainplane]

    elif PUrP.SingleCouplingModes == "1":  # stick
        bpy.data.objects[newname_mainplane].scale = mathutils.Vector((1, 1, 1))
        ob0 = genPrimitive(CenterObj, newname_mainplane,
                           '_stick_diff', is_unmapped)
        ob0.hide_select = True
        ob1 = genPrimitive(CenterObj, newname_mainplane,
                           '_stick_fix', is_unmapped)
        ob1.hide_select = True
        oversizeToPrim(context, singcoupmode(context, "1", None), ob0, ob1)

        newMain = data.objects[newname_mainplane]

    elif PUrP.SingleCouplingModes == "4":
        newMain = genPlanar(context, CenterObj, visibility, is_unmapped)
    # Adjustment for globalscale
    # newMain.scale = mathutils.Vector((GlobalScale, GlobalScale, GlobalScale))

    for ob in context.selected_objects:
        ob.select_set(False)

    context.view_layer.objects.active = newMain
    newMain.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return newMain


def singcoupmode(context, Number, coup):
    if Number != None:
        if Number == "1":
            return "STICK"
        elif Number == "2":
            return "MF"
        elif Number == "3":
            return "FLAT"

    if coup != None:
        children = coup.children
        if len(children) == 0 or len(children) == 1:
            return "FLAT"
        elif len(children) == 2 or len(children) == 3:
            for child in children:
                if "diff" in child.name:
                    obout = child
                # elif "fix" in child.name or "union" in child.name:
                #    obin = child
            if zSym(obout):
                return "STICK"
            else:
                return "MF"


def oversizeToPrim(context, mode, ob0, ob1):
    '''applies the oversize to the primitves; ob0 is the bigger object (diff) ob1 the smaller (fix, union), mode can be "STICK" "MF" "'''
    PUrP = context.scene.PUrP
    Oversize = PUrP.Oversize * PUrP.GlobalScale

    upperverts = []
    lowerverts = []
    for v in ob0.data.vertices:
        if v.co[2] > 0:
            upperverts.append(v.index)
        else:
            lowerverts.append(v.index)

    shift = Oversize  # * sqrt(2)

    # cube is spezial case but why

    if "Cube" not in ob0.data.name:
        for v in ob1.data.vertices:
            Pur = ob0.data.vertices[v.index].co

            # P1 = Pur.normalized()
            P2Dim = mathutils.Vector((Pur[0], Pur[1]))

            P2Norm = P2Dim.normalized()
            # print(f"P2Dim {P2Dim} Pur {P2Norm}")

            v.co.x = Pur[0] - shift * P2Norm[0]
            v.co.y = Pur[1] - shift * P2Norm[1]

            if v.index in upperverts:
                v.co.z = Pur[2] - Oversize
            elif v.index in lowerverts and mode != "MF":
                v.co.z = Pur[2] + Oversize
    else:
        v = ob1.data.vertices
        w = ob0.data.vertices

        v[1].co = w[1].co + \
            mathutils.Vector((Oversize, Oversize, -Oversize))
        v[3].co = w[3].co + \
            mathutils.Vector((Oversize, -Oversize, -Oversize))
        v[5].co = w[5].co + \
            mathutils.Vector((-Oversize, Oversize, -Oversize))
        v[7].co = w[7].co + \
            mathutils.Vector((-Oversize, -Oversize, -Oversize))

        if mode != "MF":
            v[0].co = w[0].co + \
                mathutils.Vector((Oversize, Oversize, Oversize))
            v[2].co = w[2].co + \
                mathutils.Vector((Oversize, -Oversize, Oversize))
            v[4].co = w[4].co + \
                mathutils.Vector((-Oversize, Oversize, Oversize))
            v[6].co = w[6].co + \
                mathutils.Vector((-Oversize, -Oversize, Oversize))
        else:
            v[0].co = w[0].co + \
                mathutils.Vector((Oversize, Oversize, 0))
            v[2].co = w[2].co + \
                mathutils.Vector((Oversize, -Oversize, 0))
            v[4].co = w[4].co + \
                mathutils.Vector((-Oversize, Oversize, 0))
            v[6].co = w[6].co + \
                mathutils.Vector((-Oversize, -Oversize, 0))


def applyScalRot(obj):
    mat = obj.matrix_world
    # translation/ location vector
    Vector = mathutils.Vector
    trans = mathutils.Matrix.Translation(Vector(
        (obj.matrix_world[0][3], obj.matrix_world[1][3], obj.matrix_world[2][3])))

    # ob data
    me = obj.data
    for v in me.vertices:
        v.co = v.co@mat
    mat.identity()
    mat @= trans

    # obj.rotation_euler = Vector((0, 0, 0))
    # obj.rotation_euler = obj.parent.rotation_euler


def applyScale(obj):
    verts = obj.data.vertices
    scale = obj.scale

    for vert in verts:
        vert.co[0] *= scale[0]
        vert.co[1] *= scale[1]
        vert.co[2] *= scale[2]

    obj.scale[0] = 1
    obj.scale[1] = 1
    obj.scale[2] = 1


def genPrimitive(CenterObj, newname_mainplane, nameadd, is_unmapped):
    context = bpy.context
    PUrP = bpy.context.scene.PUrP
    size = 1  # PUrP.CoupSize
    PrimTypes = context.scene.PUrP.SingleCouplingTypes
    CylVert = PUrP.CylVert
    aRadius = PUrP.aRadius
    bRadius = PUrP.bRadius
    data = bpy.data

    # print(f"CenterObj in gen primitive {CenterObj}")
    loc = mathutils.Vector((0, 0, 0))
    if PrimTypes == "1":
        bpy.ops.mesh.primitive_cube_add(size=size, location=loc)

    elif PrimTypes == "2":
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=CylVert, radius=aRadius, depth=1, enter_editmode=False, location=loc)

    elif PrimTypes == "3":
        bpy.ops.mesh.primitive_cone_add(
            vertices=CylVert, radius1=aRadius, radius2=bRadius, depth=1, enter_editmode=False, location=loc)
        if PUrP.SingleCouplingModes == "1":
            bpy.context.window_manager.popup_menu(
                coneTrouble, title="Warning", icon='ERROR')  # raise error message
        elif PUrP.SingleCouplingModes == "2" and aRadius < bRadius:
            bpy.context.window_manager.popup_menu(
                coneTrouble, title="Warning", icon='ERROR')  # raise error message

    # correct geometry location for Male Female
    if PUrP.SingleCouplingModes == "2":  # Male - female
        import bmesh

        # Get the active mesh
        me = bpy.context.object.data

        # Get a BMesh representation
        bm = bmesh.new()   # create an empty BMesh
        bm.from_mesh(me)   # fill it in from a Mesh

        # moves cube up that it still intersects with male merge partner
        for v in bm.verts:
            if nameadd == "_diff":
                v.co.z += 0.4999999
            elif nameadd == "_union":
                v.co.z += 0.4999

        if PrimTypes == "3":  # cone must be higher
            for v in bm.verts:
                if nameadd == "_diff":
                    v.co.z += 0.0  # 5
                elif nameadd == "_union":
                    v.co.z += 0.0  # 5

        # Finish up, write the bmesh back to the mesh
        bm.to_mesh(me)
        bm.free()  # free and prevent further access

    # bevel for mode 2 - male-female
    obj = context.object
    # bevel weights need to enabled explizitly
    #context.object.data.use_customdata_edge_bevel = True
    upverz = 0
    downverz = 0

    # bevelweights
    #mesh = bpy.context.object.data
    bevel_weight_attr = obj.data.attributes.new("bevel_weight_edge", "FLOAT", "EDGE")
    for idx, e in enumerate(obj.data.edges):
        bevel_weight_attr.data[idx].value = 0.0 #if e.select else 1.0
    

    for vert in obj.data.vertices:
        if upverz < vert.co.z:
            upverz = vert.co.z
        if downverz > vert.co.z:
            downverz = vert.co.z
    if PUrP.SingleCouplingModes == "2":  # Male - female
        for id, edge in enumerate(context.object.data.edges):
            if context.object.data.vertices[edge.vertices[0]].co.z == upverz and context.object.data.vertices[edge.vertices[1]].co.z == upverz:
                # print(f"setting weight for edge {edge}")
                bevel_weight_attr.data[id].value = 1  #edge.bevel_weight = 1
    elif PUrP.SingleCouplingModes == "1":  # stick --> upper and lower edge bevelt
        for id, edge in enumerate(context.object.data.edges):
            if context.object.data.vertices[edge.vertices[0]].co.z == upverz and context.object.data.vertices[edge.vertices[1]].co.z == upverz:
                # print(f"setting weight for edge {edge}")
                bevel_weight_attr.data[id].value = 1
                #edge.bevel_weight = 1
            if context.object.data.vertices[edge.vertices[0]].co.z == downverz and context.object.data.vertices[edge.vertices[1]].co.z == downverz:
                # print(f"setting weight for edge {edge}")
                bevel_weight_attr.data[id].value = 1
                #edge.bevel_weight = 1

    scalefactor = PUrP.GlobalScale * PUrP.CoupScale * PUrP.CoupSize
    obj.scale *= scalefactor
    context.object.scale.z *= PUrP.zScale

    context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # make name relative to the Couplingmainplain
    context.object.name = str(newname_mainplane) + str(nameadd)
    context.object.parent = bpy.data.objects[newname_mainplane]

    # print(f"zscale should affect obj {context.object.name}")
    #

    mod = context.object.modifiers.new(
        name=context.object.name + "Bevel", type="BEVEL")  # bevelOption to the Subcoupling
    mod.width = PUrP.BevelOffset
    mod.segments = PUrP.BevelSegments
    mod.limit_method = 'WEIGHT'
    context.object.display_type = 'WIRE'
    context.object.show_in_front = True
    context.object.hide_select = True
    if not is_unmapped:
        if ("_diff" in bpy.context.object.name) or ("_union" in bpy.context.object.name):
            mod = CenterObj.modifiers.new(
                name=context.object.name, type="BOOLEAN")
            mod.object = context.object
            mod.show_viewport = False
            set_BoolSolver(context, mod)
            if nameadd == "_diff":
                mod.operation = 'DIFFERENCE'
            elif nameadd == '_union':
                mod.operation = 'UNION'
        else:
            pass

    return context.object


def genPlanar(context, CenterObj, visibility, is_unmapped):
    # context = bpy.context
    PUrP = bpy.context.scene.PUrP
    PUrP_name = PUrP.PUrP_name
    LineLength = PUrP.LineLength
    LineCount = PUrP.LineCount
    LineDistance = PUrP.LineDistance
    Oversize = PUrP.Oversize
    # CenterObj = PUrP.CenterObj
    GlobalScale = PUrP.GlobalScale
    CoupSize = PUrP.CoupSize
    CutThickness = PUrP.CutThickness
    OffsetRight = PUrP.OffsetRight
    OffsetLeft = PUrP.OffsetLeft
    StopperHeight = PUrP.StopperHeight
    StopperBool = PUrP.StopperBool
    Oversize = PUrP.Oversize
    height = PUrP.zScale
    CoupScale = PUrP.CoupScale
    type = PUrP.PlanarCouplingTypes

    # I don't know how to get the name from the enum property might be simpler
    if type == "1":
        objectname = "Cubic"
    elif type == "2":
        objectname = "Dovetail"
    elif type == "3":
        objectname = "Puzzle1"
    elif type == "4":
        objectname = "Puzzle2"
    elif type == "5":
        objectname = "Puzzle3"
    elif type == "6":
        objectname = "Puzzle4"
    elif type == "7":
        objectname = "Puzzle5"
    elif type == "8":
        objectname = "Arrow1"
    elif type == "9":
        objectname = "Arrow2"
    elif type == "10":
        objectname = "Arrow3"
    elif type == "11":
        objectname = "Pentagon"
    elif type == "12":
        objectname = "Hexagon"
    elif type == "13":
        objectname = "T-RoundedAll"
    elif type == "14":
        objectname = "T-RoundedTop"
    elif type == "15":
        objectname = "T-Straight"
    elif type == "16":
        objectname = "Flat"
        PUrP.StopperBool = False
        StopperBool = False
    else:
        objectname = "Cubic"

    newname = str(PUrP_name) + "PlanarConnector_" + str(random.randint(1, 999))
    nameadd = "_diff"

    appendCoupling(context, "planar.blend", objectname)
    #print(
    #    f'nache append active {context.object.name}, CenterObj {CenterObj.name}')
    context.object.name = str(newname) + str(nameadd)

    #print(f'active {context.object.name}, CenterObj {CenterObj.name}')
    if not is_unmapped:
        context.object.parent = CenterObj
    context.object.display_type = 'WIRE'
    context.object.show_in_front = True

    # deselect all
    selected = context.selected_objects[:]
    for ob in selected:
        ob.select_set(False)

    obj = bpy.data.objects[context.object.name]

    # scale it a bit smaller than in the file
    adjustScale = PUrP.PlanarCorScale
    obj.scale.x *= adjustScale * GlobalScale * CoupScale
    obj.scale.y *= adjustScale * GlobalScale * CoupScale

    # apply scale to get scale to one

    obj.select_set(True)
    context.view_layer.objects.active = obj
    print(f"obj before apply scale {obj.name}")
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    import bmesh
    # planar side offset
    me = bpy.context.object.data

    # Get a BMesh representation
    bm = bmesh.new()   # create an empty BMesh
    bm.from_mesh(me)   # fill it in from a Mesh

    bm.verts.ensure_lookup_table()
    # bm.edges.ensure_lookup_table()

    # prepare values for  offsets
    right = OffsetRight
    left = OffsetLeft

    bm.verts[0].co.x += right
    bm.verts[1].co.x -= left

    # collect data for later
    Oriy = bm.verts[0].co.y

    # check if its true for all models  #############may delete later
    mergecoright = bm.verts[3].co.x
    mergecoleft = bm.verts[2].co.x

    # check if its true for all models  #############may delete later
    middlerightcox = bm.verts[3].co.x
    middleleftcox = bm.verts[2].co.x

    if StopperBool != True:
        ret = bmesh.ops.extrude_edge_only(
            bm,
            edges=bm.edges)

        geom_extrude_mid = ret['geom']

        verts_extrude_a = [ele for ele in geom_extrude_mid
                           if isinstance(ele, bmesh.types.BMVert)]

        edges_extrude_a = [ele for ele in geom_extrude_mid
                           if isinstance(ele, bmesh.types.BMEdge) and ele.is_boundary]

        bmesh.ops.translate(
            bm,
            verts=verts_extrude_a,
            vec=(0.0, 0.0, -height))
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    else:
        # extrude
        # lowestverts = bm.verts[:]
        ret = bmesh.ops.extrude_edge_only(  # first extrude
            bm,
            edges=bm.edges)

        geom_extrude_start = ret['geom']

        verts_extrude_a = [ele for ele in geom_extrude_start
                           if isinstance(ele, bmesh.types.BMVert)]

        bmesh.ops.translate(  # first translate
            bm,
            verts=verts_extrude_a,
            vec=(0.0, 0.0, -height))  # zScale as height for the couple part

        # second extrude
        # lowestverts = bm.verts[:]
        edges_extrude_a = [ele for ele in geom_extrude_start  # collectect edges on cut
                           if isinstance(ele, bmesh.types.BMEdge) and ele.is_boundary and ele.verts[0].co.y == Oriy and ele.verts[1].co.y == Oriy]

        ret = bmesh.ops.extrude_edge_only(  # extrude only the edges on cut
            bm,
            edges=edges_extrude_a)

        geom_extrude_mid = ret['geom']

        verts_extrude_b = [ele for ele in geom_extrude_mid
                           if isinstance(ele, bmesh.types.BMVert)]

        # translate to stopper height
        bmesh.ops.translate(
            bm,
            verts=verts_extrude_b,
            vec=(0.0, 0.0, -StopperHeight))

        # make missing faces
        # Cutfaces
        Cutfaceverts_start = [ele for ele in geom_extrude_start
                              if isinstance(ele, bmesh.types.BMVert) and ele.co.y == Oriy
                              if ele.co.x == middlerightcox or ele.co.x == middleleftcox]

        Cutfaceverts_mid = [ele for ele in geom_extrude_mid
                            if isinstance(ele, bmesh.types.BMVert) and ele.co.y == Oriy
                            if ele.co.x == middlerightcox or ele.co.x == middleleftcox]

        Cutfaceverts = Cutfaceverts_start + Cutfaceverts_mid

        # test content of list
        for ele in Cutfaceverts:
            print(f"Cutfaceverts co x {ele.co.x} co y {ele.co.y} ")

        edges_frontface = bmesh.ops.contextual_create(
            bm,
            geom=Cutfaceverts,
            # mat_nr,
            # use_smooth
        )

        # vertversion
        Sitfaceverts_start = [ele for ele in geom_extrude_start
                              if isinstance(ele, bmesh.types.BMVert) and ele.co.y != Oriy]

        Sitfaceverts = Cutfaceverts_start + Sitfaceverts_start

        ####
        Sitfaceedges = [ele for ele in bm.edges
                        if ele.verts[0] in Sitfaceverts and ele.verts[1] in Sitfaceverts]

        # alternative with edges

        # Sitfaceedges = Sitfaceedges_sit + Sitfaceedges_front #+ Sitfaceedges_frontalt
        # Sitfaceedges =  Cutfaceverts_start + Sitfaceverts_start ###actually verts

        # test sitedges
        print(f" Sit edges all {Sitfaceedges}")

        bmesh.ops.contextual_create(
            bm,
            geom=Sitfaceedges,
            # mat_nr,
            # use_smooth
        )

        # bmesh.ops.weld_verts(bm, bm.verts)

        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

    # Finish up, write the bmesh back to the mesh
    bm.to_mesh(me)
    bm.free()  # free

    # obj.scale *= CoupSize
    # print(f"obj {obj.name} coupSize {CoupSize} obj.scale {obj.scale} ")

    # array 1 und 2
    mod = obj.modifiers.new(name="PUrP_Array_1", type="ARRAY")
    mod.use_merge_vertices = True
    mod.count = LineLength

    mod = obj.modifiers.new(name="PUrP_Array_2", type="ARRAY")
    mod.use_relative_offset = False
    mod.use_constant_offset = True
    mod.constant_offset_displace[0] = 0
    mod.constant_offset_displace[1] = LineDistance

    mod.count = LineCount
    mod.use_merge_vertices = True

    # Solidify
    mod = obj.modifiers.new(name="PUrP_Solidify", type="SOLIDIFY")

    mod.thickness = Oversize * PUrP.GlobalScale
    mod.offset = -1.0
    mod.solidify_mode = "NON_MANIFOLD"
    mod.nonmanifold_thickness_mode = 'CONSTRAINTS'

   # mod.use_even_offset = True
    mod.use_rim = True

    # boolean _diff at parent object
    if not is_unmapped:
        mod = obj.parent.modifiers.new(name=obj.name, type="BOOLEAN")
        mod.show_viewport = visibility
        mod.operation = 'DIFFERENCE'
        mod.object = obj
        set_BoolSolver(context, mod)
    # print(f"Active after planar generation {context.object}, obj is {obj}")

    return obj


def appendCoupling(context, filename, objectname):

    script_path = os.path.dirname(os.path.realpath(__file__))
    subpath = "blend" + os.sep + filename
    cp = os.path.join(script_path, subpath)

    # filepath = "//2.82\scripts\addons\purp\blend\new_library.blend"
    with bpy.data.libraries.load(cp) as (data_from, data_to):
        print('I am in')
        data_to.objects = [
            name for name in data_from.objects if name == objectname]

    for obj in data_to.objects:
        context.collection.objects.link(obj)
        obj.location = mathutils.Vector((0, 0, 0))
        context.view_layer.objects.active = obj


def newmainPlane(context, CenterObj, unmapped):
    data = bpy.data
    PUrP = context.scene.PUrP
    PUrP_name = PUrP.PUrP_name
    CutThickness = PUrP.CutThickness

    bpy.ops.mesh.primitive_plane_add(
        size=2, enter_editmode=False, location=(0, 0, 0))
    context.object.name = str(
        PUrP_name) + "SingleConnector_" + str(random.randint(1, 999))

    while '.' in context.object.name:
        context.object.name = str(
            PUrP_name) + "SingleConnector_" + str(random.randint(1, 999))

    newname_mainplane = context.object.name

    # bpy.ops.object.modifier_add(type='SOLIDIFY')
    mod = context.object.modifiers.new(
        name="PUrP_Solidify", type="SOLIDIFY")
    mod.thickness = CutThickness * PUrP.GlobalScale
    mod.offset = 1.0
    context.object.display_type = 'WIRE'
    # context.object.show_in_front = True
    if not unmapped:
        context.object.parent = CenterObj

    return context.object


def newmainJoint(context, CenterObj, unmapped):

    PUrP = context.scene.PUrP
    PUrP_name = PUrP.PUrP_name
    CutThickness = PUrP.CutThickness

    bpy.ops.mesh.primitive_circle_add(vertices=PUrP.MaincutVert, radius=1, fill_type='TRIFAN',
                                      enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

    # planar side offset
    me = bpy.context.object.data

    # Get a BMesh representation
    bm = bmesh.new()   # create an empty BMesh
    bm.from_mesh(me)   # fill it in from a Mesh

    bm.verts.ensure_lookup_table()
    # bm.edges.ensure_lookup_table()

    # in der mitte 0 dann
    edges_up = [ele for n, ele in enumerate(bm.edges[:])
                if isinstance(ele, bmesh.types.BMEdge) and ele.is_boundary and bm.verts[0] not in ele.verts and bm.verts[1] not in ele.verts and n < ((len(bm.edges)-1)/2)-1]
    edges_down = [ele for n, ele in enumerate(bm.edges[:])
                  if isinstance(ele, bmesh.types.BMEdge) and ele.is_boundary and bm.verts[0] not in ele.verts and n > ((len(bm.edges)-1)/2)+1]

    ret = bmesh.ops.extrude_edge_only(bm, edges=edges_up)
    geom_extrude_mid = ret['geom']
    verts_extrude_a = [ele for ele in geom_extrude_mid
                       if isinstance(ele, bmesh.types.BMVert)]
    # edges_extrude_a = [ele for ele in geom_extrude_mid
    #                   if isinstance(ele, bmesh.types.BMEdge) and ele.is_boundary]

    bmesh.ops.translate(
        bm,
        verts=verts_extrude_a,
        vec=(0.0, 0.0, 1))

    ret = bmesh.ops.extrude_edge_only(bm, edges=edges_down)
    geom_extrude_mid = ret['geom']
    verts_extrude_b = [ele for ele in geom_extrude_mid
                       if isinstance(ele, bmesh.types.BMVert)]
    # edges_extrude_b = [ele for ele in geom_extrude_mid
    #                  if isinstance(ele, bmesh.types.BMEdge) and ele.is_boundary]

    bmesh.ops.translate(
        bm,
        verts=verts_extrude_b,
        vec=(0.0, 0.0, -1))

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

    bm.to_mesh(me)
    bm.free()

    context.object.data.name = "Joint"
    context.object.name = str(
        PUrP_name) + "SingleConnector_" + str(random.randint(1, 999))
    newname_mainplane = context.object.name

    # bpy.ops.object.modifier_add(type='SOLIDIFY')
    mod = context.object.modifiers.new(
        name="PUrP_Solidify", type="SOLIDIFY")
    mod.thickness = CutThickness * PUrP.GlobalScale
    mod.offset = 1.0
    mod.solidify_mode = 'NON_MANIFOLD'
    mod.nonmanifold_thickness_mode = 'EVEN'

    context.object.display_type = 'WIRE'

    # context.object.show_in_front = True
    if not unmapped:
        context.object.parent = CenterObj

    return context.object


def genSinglemain(context, CenterObj, type, unmapped):
    if type == '1':
        newmain = newmainPlane(context, CenterObj, unmapped)
    elif type == '2':
        newmain = newmainJoint(context, CenterObj, unmapped)
    else:
        print("Maincut type must be '1' oder '2'")
    PUrP = context.scene.PUrP
    scalefactor = PUrP.GlobalScale * PUrP.CoupScale
    for vert in newmain.data.vertices:
        vert.co *= 3 * scalefactor
    applyScale(newmain)
    return newmain


def ReplaceOrNotMain(context, coup):
    name = coup.data.name
    PUrP = context.scene.PUrP
    if 'Plane' in name and PUrP.SingleMainTypes == '1':
        if coup.data.vertices[1].co.x / (3 * PUrP.GlobalScale) != PUrP.CoupScale:
            print("Exchanged MainCut")
            return True
        else:
            return False

    elif is_joint(context, coup) and PUrP.SingleMainTypes == '2':
        if amount_jointverts(context, coup) != PUrP.MaincutVert:
            return True
        elif coup.data.vertices[1].co.y / (3 * PUrP.GlobalScale) != PUrP.CoupScale:
            print("Exchanged MainCut")
            return True
        else:
            return False

    # print("Exchanged MainCut")
    return True


def is_joint(context, coup):
    if 'Joint' in coup.data.name:
        return True
    return False


def amount_jointverts(context, coup):

    if is_joint(context, coup):
        allverts = len(coup.data.vertices)
        #  substract the center vert and remove the half from the extrusion
        return int((allverts)/2)


class PP_OT_ExChangeCoup(bpy.types.Operator):
    '''Exchanges the selected couplings against a new connector defined by the setting in the panel. It can be use as the past part of copy and paste (with copy is "Active to settings")'''
    bl_idname = "object.exchangecoup"
    bl_label = "ExChangeCoupling"
    bl_options = {'REGISTER', "UNDO"}

    @ classmethod
    def poll(cls, context):
        if (context.view_layer.objects.active != None) and context.mode == 'OBJECT':
            if ("SingleConnector" in context.view_layer.objects.active.name) or ("PlanarConnector" in context.view_layer.objects.active.name):
                return True
        else:
            return False

    def execute(self, context):

        context = bpy.context
        data = bpy.data
        PUrP = context.scene.PUrP
        CutThickness = PUrP.CutThickness
        GlobalScale = PUrP.GlobalScale
        zScale = PUrP.zScale
        PUrP_name = PUrP.PUrP_name
        CouplingModes = context.scene.PUrP.SingleCouplingModes
        selected = context.selected_objects[:]

        for obj in selected:  # für die selektierten
            # deselct all

            if is_coup(context, obj):  # eines meiner coupling

                for ob in context.selected_objects:
                    ob.select_set(False)

                correctname(context, obj)
                if not is_unmapped(context, obj):
                    CenterObj = obj.parent
                    print("Parent to CenterObj Exchange")
                else:
                    CenterObj = PUrP.CenterObj
                    print("OldData to CenterObj Exchange")

                is_unmap = False
                if is_unmapped(context, obj) or PUrP.AddUnmapped:
                    is_unmap = True

                viewportvis = True
                if not is_unmap:
                    for mod in obj.parent.modifiers:  # lösche alle modifier im centerobj
                        if obj.name == mod.name:
                            print(
                                f"viewportvis for {mod.name} is {mod.show_viewport}")
                            viewportvis = mod.show_viewport
                        if obj.name in mod.name:
                            obj.parent.modifiers.remove(mod)

                for child in obj.children:  # lösche alle kinder
                    child.hide_select = False
                    child.select_set(True)
                    obj.select_set(False)
                    bpy.ops.object.delete(use_global=False)

                loc = mathutils.Vector((0, 0, 0))
                # when  new object planar types oder das ursprüngliche object planar ist
                if CouplingModes == "4":

                    # print(f"obj.data.name {obj.data.name}")
                    loc = obj.location.copy()
                    trans = obj.matrix_world.copy()
                    oldname = obj.name

                    for ob in context.selected_objects:  # deselte all
                        ob.select_set(False)
                    obj.select_set(True)
                    bpy.ops.object.delete(use_global=False)

                    # report stupidity
                    if PUrP.SingleCouplingModes == "1" and context.scene.PUrP.SingleCouplingTypes == "3":
                        self.report(
                            {'WARNING'}, "Using a Cone in a Stick Connector will not work! But maybe you have a greater vision...")

                    # generate new planar
                    newmain = coupModeDivision(context, CenterObj,
                                               oldname, is_unmap, viewportvis)
                    context.object.matrix_world = trans

                    if is_unmap:
                        unmapped_signal(context, newmain)

                else:  # when it was SingleCoupling, the mainplane is kept

                    if ReplaceOrNotMain(context, obj):
                        # print(f"2obj.data.name {obj.data.name}")
                        loc = obj.location.copy()
                        trans = obj.matrix_world.copy()
                        for ob in context.selected_objects:  # deselte all
                            ob.select_set(False)
                        obj.select_set(True)
                        # delete the old planar coupling
                        bpy.ops.object.delete(use_global=False)
                        # name for

                        newob = genSinglemain(
                            context, CenterObj, PUrP.SingleMainTypes, is_unmap)

                        # newname = newmainPlane(context, data.objects[parentname])
                        newname = newob.name
                        data.objects[newname].matrix_world = trans
                        obj = context.object

                    obj.modifiers["PUrP_Solidify"].thickness = CutThickness * GlobalScale
                    if not is_unmap:
                        mod = CenterObj.modifiers.new(
                            name=obj.name, type="BOOLEAN")
                        print(f"viewportvis applied {viewportvis}")
                        mod.show_viewport = viewportvis
                        mod.object = obj
                        mod.operation = 'DIFFERENCE'
                        set_BoolSolver(context, mod)
                        obj.scale = mathutils.Vector((1, 1, 1))

                    coupModeDivision(context, CenterObj,
                                     obj.name, is_unmap, viewportvis)

                    if is_unmap:
                        unmap_coup(context, obj)
                        # unmapped_signal(context, obj)

            # hideselectinlay(context, obj)

            if PUrP.OrderBool:
                update_order(context, CenterObj)

        return {'FINISHED'}


def otherparents(context, coup):
    parents = []
    for ob in context.view_layer.objects:
        if ob != coup.parent:
            if ob.PUrPCobj == True:
                if not is_coup(context, ob) and not is_inlay(context, ob):
                    for mod in ob.modifiers:
                        if coup.name in mod.name and "diff" not in mod.name and "union" not in mod.name:
                            parents.append(ob)
    return parents


def centerObjList(context, coup):
    parents = []
    for ob in context.view_layer.objects:
        for mod in ob.modifiers:
            if coup.name in mod.name:
                if ob not in parents:
                    parents.append(ob)
    return parents


# sort coups in order on the centerobjs to have the order reflected --> [coup1center1,coup2center1,...,coup1center2,coup2, center2 ]


def sort_coups(context, coups):
    # collect all Cobjs from coups
    CObjs = []
    coupnames = []
    sortedcoups = []
    for coup in coups:
        coupnames.append(coup.name)
        if coup.parent not in CObjs:
            CObjs.append(coup.parent)

    for Cobj in CObjs:
        for mod in Cobj.modifiers:
            if mod.name in coupnames:
                if mod.object not in sortedcoups:
                    sortedcoups.append(mod.object)

    print(f"End Sort coups return {sortedcoups} ")
    return sortedcoups

    # go through Cobj
    #   go through  modifiers und bei übereinstimmung in die sorted coups list


class PP_OT_ApplyCoupling(bpy.types.Operator):
    '''Applys selected Connectors. Finalizes the editing by cutting the model and adding the connectors. Behaviour changes relative to "Cut All" Checkbox'''
    bl_label = "ApplyCouplings"
    bl_idname = "apl.coup"
    bl_options = {'REGISTER', "UNDO"}

    @ classmethod
    def poll(cls, context):
        if (context.view_layer.objects.active != None) and context.mode == 'OBJECT':
            if context.mode == 'OBJECT' and context.area.type == 'VIEW_3D':
                if ("SingleConnector" in context.view_layer.objects.active.name) or ("PlanarConnector" in context.view_layer.objects.active.name):
                    return True
        else:
            return False

    def execute(self, context):

        data = bpy.data
        selected = context.selected_objects[:]
        PUrP = context.scene.PUrP
        PUrP_name = context.scene.PUrP.PUrP_name

        # if there is no Centerobj
        Centerobj = PUrP.CenterObj

        # [+]coups from selected, sort out unmapped
        selected = selectedtocouplist(context, selected)
        print(f"Selected {selected}")
        # sort out unmapped
        for coup in selected[:]:
            if is_unmapped(context, coup):
                selected.remove(coup)
                self.report({'WARNING'}, "Connector is unmapped!")

        # sort coups in order on the centerobjs to have the order reflected --> [coup1center1,coup2center1,...,coup1center2,coup2, center2 ]
        sortedCoups = sort_coups(context, selected)

        # Plan
        # [+]coups from selected, sort out unmapped
        ###

        # gehe durch die coups
        for coup in sortedCoups:
            if not PUrP.CutAll:
                #  apply to parent (klappt wenn applysingle sortiert alle richtig)
                # maybe unmapped in the process?
                if is_unmapped(context, coup):
                    unmap_coup(context, coup)
                    continue
                else:
                    Centerobj = coup.parent
                    if bvhOverlap(context, coup, Centerobj):
                        # hmm only enough for planar, other wise only diff and union not there, but whole line should be not necessary
                        ensure_allmods(context, coup, Centerobj)
                        applySingleCoup(context, coup, Centerobj, True)
                    else:
                        unmap_coup(context, coup)
            else:
                Centerobjs = context.view_layer.objects[:]
                # collecte all CObjs which are touching
                TouchedCobjs = []
                for Centerobj in Centerobjs:
                    if Centerobj.type == 'MESH':
                        print(f'Test now Cobj {Centerobj}')
                        if not is_coup(context, Centerobj) and not is_inlay(context, Centerobj) and not is_buildvolume(context, Centerobj):
                            if bvhOverlap(context, coup, Centerobj):
                                TouchedCobjs.append(Centerobj)
                print(f'Found Touched Cobjs {TouchedCobjs}')
                for n, Centerobj in enumerate(TouchedCobjs):
                    # ensure for planar and for single
                    # remap_coup(context, coup, Centerobj)
                    ensure_allmods(context, coup, Centerobj)
                    if not n == len(TouchedCobjs)-1:
                        applySingleCoup(context, coup, Centerobj, False)
                    else:
                        applySingleCoup(context, coup, Centerobj, True)

        PUrP = context.scene.PUrP
        if PUrP.OrderBool:
            update_order(context, Centerobj)
        return{"FINISHED"}


def applyRemoveCouplMods(daughter, connector, side):
    print(f"daughter: {daughter} connector: {connector}, side : {side}")
    context = bpy.context
    active = context.view_layer.objects.active
    active = daughter
    daughtermods = daughter.modifiers[:]

    if side == "NEGATIV":
        for mod in daughtermods:
            if str(connector.name) + '_stick_diff' == mod.name:
                print(
                    f"I apply now modifier: {mod.name} to Object {daughter.name}. Active obj: {active.name}")
                context.view_layer.objects.active = daughter
                print(f"active: {active}")
                # mod.show_viewport = True
                bpy.ops.object.modifier_apply(modifier=mod.name)

            elif str(connector.name) + '_diff' == mod.name:
                print(
                    f"I apply now modifier: {mod.name} to Object {daughter.name}")
                context.view_layer.objects.active = daughter
                print(f"active: {active}")
                # mod.show_viewport = True
                bpy.ops.object.modifier_apply(modifier=mod.name)
            elif str(connector.name) + '_union' == mod.name:
                print(
                    f'I delete now modifier {mod.name} from Object {daughter.name}')
                daughter.modifiers.remove(mod)
    elif side == "POSITIV":
        print('Positive Seite')
        for mod in daughtermods:
            print(f"modifiert nam: {mod.name}")
            if str(connector.name) + '_stick_diff' == mod.name:
                print(
                    f"I apply now modifier: {mod.name} to Object {daughter.name}")
                context.view_layer.objects.active = daughter
                print(f"active: {active}")
                mod.show_viewport = True
                bpy.ops.object.modifier_apply(modifier=mod.name)

            elif str(connector.name) + '_union' == mod.name:
                context.view_layer.objects.active = daughter
                print(f"active: {active}")
                print(
                    f"I apply now modifier: {mod.name} to Object {daughter.name}")
                mod.show_viewport = True
                bpy.ops.object.modifier_apply(modifier=mod.name)
            elif str(connector.name) + '_diff' == mod.name:
                print(
                    f'I delete now modifier {mod.name} from Object {daughter.name}')
                daughter.modifiers.remove(mod)
    else:
        print("Somethings Wrong with side determin")
    # if context.scene.PUrP.PUrP_name not in daughter.name:
    #    daughter.name = str(context.scene.PUrP.PUrP_name) + str(daughter.name)


def ensurenoscaling(context, Cobj):
    # deselectall(context)
    Cobj.select_set(True)
    if Cobj.scale[0] != 1 or Cobj.scale[1] != 1 or Cobj.scale[2] != 1:
        applyScale(Cobj)


def in_collection(context, ob):
    data = bpy.data
    collection = None
    for col in data.collections:
        for o in col.objects:
            if o == ob:
                collection = col
    return collection


def removeCoupling(context, Coupl):
    '''removes objects related to the coupling after apllying or when it is a fixed '''
    print(f"I'm in Delete now Coupling {Coupl.name}")

    data = context.view_layer  # bpy.data
    PUrP = context.scene.PUrP
    keep = PUrP.KeepCoup
    active = context.view_layer.objects.active

    Coupl_children = Coupl.children[:]
    ChildCopies = []
    ChildNames = []

    for child in Coupl_children:
        # make a copy of the inlays to reconnect and keep them later is Keep Bool is set
        if not is_order(context, child):
            if keep:
                # make a copy of the inlays
                matrix = child.matrix_world
                childtmpdata = child.data.copy()
                child_tmp = bpy.data.objects.new(
                    name="tmp", object_data=childtmpdata)

                col = in_collection(context, Coupl)
                if col == None:
                    if context.collection != None:
                        col = context.collection
                    else:
                        collection = bpy.data.collections.new(
                            name="PUrPNeededThat")  # makes collection
                        context.scene.collection.children.link(collection)

                col.objects.link(child_tmp)
                child_tmp.parent = Coupl
                child_tmp.matrix_world = matrix
                child_tmp.display_type = 'WIRE'
                print("remove coup keep mache Bevel mod ")
                mod = child_tmp.modifiers.new(
                    name=Coupl.name + "Bevel", type="BEVEL")
                mod.width = child.modifiers[child.name + "Bevel"].width
                mod.segments = child.modifiers[child.name + "Bevel"].segments
                mod.limit_method = 'WEIGHT'

                ChildCopies.append(child_tmp)
                ChildNames.append(child.name)

            if "fix" not in child.name:  # alle normalen couplings die applied sind
                child.hide_select = False
                for ob in context.selected_objects:
                    ob.select_set(False)
                child.select_set(True)

                bpy.ops.object.delete(use_global=False)
            elif 'fix' in child.name:
                child.hide_select = False
                # apply bevel and stuff
                for mod in child.modifiers:
                    print(f"fix stick active {active} mod {mod.name}")
                    context.view_layer.objects.active = child
                    # ensuremodvis(context, mod)
                    print(mod.name)
                    try:  # not used bevel cause runtime error when applying in 2.91, try as work arround
                        bpy.ops.object.modifier_apply(modifier=mod.name)
                    except:
                        bpy.ops.object.modifier_remove(modifier=mod.name)

                if Coupl.parent != None:
                    child.name = Coupl.parent.name
                child.display_type = 'SOLID'
                # child.location = mathutils.Vector((0,0,0))
                globloc = Coupl.matrix_world
                print(f" Matrix World  von Coupl {globloc}")

                child.parent = None
                child.matrix_world = globloc
                # child.parent = context.scene.PUrP.CenterObj
                # child.name = context.scene.PUrP.PUrP_name + "CoupleStick"

    for ob in data.objects:
        ob.select_set(False)  # for deleting after this modifier removal
        if ob not in ChildCopies:
            for mod in ob.modifiers:
                if Coupl.name in mod.name:
                    ob.modifiers.remove(mod)

    if keep:
        for num, coup in enumerate(ChildCopies):
            coup.name = ChildNames[num]
        unmap_coup(context, Coupl)
    else:
        remove_order_tag(context, Coupl)
        Coupl.select_set(True)
        bpy.ops.object.delete(use_global=False)

# excuting function of apply all
#  finds all coups connected to given Cobj and checks all objects in the scene if they overlap and need to be applied


def centerObjDecider(context, CenterObj):
    PUrP = context.scene.PUrP
    PUrP_name = PUrP.PUrP_name
    Objects = context.view_layer.objects

    # name, mods = couplingList(CenterObj)
    CoupName, ModList = couplingList(CenterObj)
    print(f"Modlist in beginning of decider {ModList}")
    # mods are actually coups
    for mod in CoupName[:]:
        Cobjlist = []
        if PUrP.CutAll:
            for pCobj in Objects[:]:
                if pCobj.type == 'MESH':
                    if not is_coup(context, pCobj) and not is_inlay(context, pCobj) and not is_buildvolume(context, pCobj):
                        Cobjlist.append(pCobj)
        else:
            Cobjlist = [Objects[mod].parent]

        is_sing = False
        is_plan = False
        PlanCobs = []
        SingCobs = []
        # go through the potential Cobjects and check if they overlap with the coup (identified in )
        for Cobj in Cobjlist[:]:
            CoupNameslist, Cobjmodslist = couplingList(Cobj)
            if is_single(context, Objects[mod]):
                is_sing = True
                print("is_sing")

                if mod in CoupNameslist:
                    print("mod in")
                    if bvhOverlap(context, Objects[mod], Cobj):
                        SingCobs.append(Cobj)
                    else:
                        unmap_coup(context, Objects[mod])
            elif is_planar(context, Objects[mod]):
                is_plan = True
                if bvhOverlap(context, Objects[mod], Cobj):
                    PlanCobs.append(Cobj)
                    print(
                        f"CObj {Cobj} appended to PlanCobs list in decider")
                else:
                    print(f"Cob {Cobj} is not overlapping with {mod}")

        # apply and deleting singles
        if is_sing:
            if len(SingCobs) == 0:
                unmap_coup(context, Objects[mod])
            else:
                # single should only have one but who knows, need to unmapp correctly when not overlapping
                print(f"CenterDecider single list {SingCobs} ")
                for n, Cobj in enumerate(SingCobs):
                    if n < len(PlanCobs)-1:
                        ensure_allmods(context, Objects[mod], Cobj)
                        applySingleCoup(
                            context, Cobj.modifiers[mod].object, Cobj, False)
                    else:
                        print("all ast zwei sing apply cobdecider")
                        ensure_mod(context, Objects[mod], Cobj, '')
                        applySingleCoup(
                            context, Cobj.modifiers[mod].object, Cobj, True)

            # if not is_unmapped(context, Objects[mod]):
            #    removeCoupling(context, Objects[mod])

        # extra apply round for all Cobj with this coup, necessary to delete planar in the end
        if is_plan:
            if len(PlanCobs) == 0:
                unmap_coup(context, Objects[mod])
            else:
                for n, Cobj in enumerate(PlanCobs):
                    if n < len(PlanCobs)-1:
                        ensure_mod(context, Objects[mod], Cobj, '')
                        applySingleCoup(
                            context, Cobj.modifiers[mod].object, Cobj, False)
                    else:
                        print("all ast zwei")
                        ensure_mod(context, Objects[mod], Cobj, '')
                        applySingleCoup(
                            context, Cobj.modifiers[mod].object, Cobj, True)

        # takes coup and CenterObj and returns the distance


def SideOfPlane(context, coup, CenterObj):

    matrix = coup.matrix_world
    couptmpdata = coup.data.copy()
    # generate copy at origin
    coup_tmp = bpy.data.objects.new(name="tmp", object_data=couptmpdata)
    coup_tmp.parent = CenterObj
    context.scene.collection.objects.link(coup_tmp)

    for ob in context.selected_objects:
        ob.select_set(False)

    coup_tmp.select_set(True)
    context.view_layer.objects.active = coup_tmp
    coup_tmp.matrix_world = matrix
    bpy.ops.object.transform_apply(
        location=True, rotation=True, scale=False)

    # cube verts gerade unten, ungerade oben
    # test = 0
    test = len(CenterObj.data.vertices)-1
    DirecDistance = 0
    if test >= 0:
        while DirecDistance == 0:

            # CouplingNormal = coup_tmp.data.vertices[0].normal
            CouplingNormal = mathutils.Vector((0, 0, 1))
            print(f"CouplingNormal {CouplingNormal}")

            direction = CouplingNormal.dot(
                CenterObj.data.vertices[test].co@CenterObj.matrix_world)
            # print(f"direction {direction} CenterObj.data.vertices[n].co {CenterObj.data.vertices[test].co}")

            planedistanceorigin = CouplingNormal.dot(
                coup_tmp.data.vertices[0].co@coup_tmp.matrix_world)
            # print(f"planedistance {planedistance} coup_tmp.data.vertices[0].co {coup_tmp.data.vertices[0].co} plane.data.vertices[0].co@plane.matrix_world {plane.data.vertices[0].co@plane.matrix_world}")

            DirecDistance = direction - planedistanceorigin
            # print(f"difference {difference}")
            test -= 1
    else:
        bpy.context.window_manager.popup_menu(
            noVertsWarn, title="Warning", icon='ERROR')
    bpy.data.objects.remove(coup_tmp)

    return DirecDistance


def unmapped_signal(context, coup):
    PUrP = context.scene.PUrP

    bpy.ops.object.text_add(
        enter_editmode=False, location=(0, 0, 0))
    SignalText = context.object
    SignalText.name = coup.name + "_Order"

    SignalText.location.z += 0.5 * PUrP.GlobalScale

    SignalText.data.body = "UNMAPPED"
    SignalText.data.extrude = 0.05
    SignalText.show_in_front = True
    SignalText.display_type = 'WIRE'
    SignalText.hide_select = True
    SignalText.parent = coup
    SignalText.matrix_world = coup.matrix_world
    SignalText.rotation_euler.x = 1.5708
    SignalText.location.x -= 0.3
    SignalText.scale = mathutils.Vector(
        (PUrP.GlobalScale, PUrP.GlobalScale, PUrP.GlobalScale))
    context.view_layer.objects.active = coup
    print(f"coup {coup.name} got the unmapped signal")


def applySingleCoup(context, coup, CenterObj, delete):

    obj = coup
    oriCoupname = coup.name[:]

    for sel in context.selected_objects:
        sel.select_set(False)

    # remeber which couplings are parented to (alternative via modifiers)
    oriCoupNames, oriCoupMods = couplingList(CenterObj)
    if len(oriCoupNames) == 0:
        return []

    print(
        f"oricoupnames for Cobj {CenterObj} beginning applysinglecoup {oriCoupNames}  ")

    # apply boolean to seperate Centralobj parts
    context.view_layer.objects.active = CenterObj

    bpy.ops.object.modifier_apply(modifier=obj.name)

    # seperate by loose parts

    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.editmode_toggle()

    # remember both objects

    CenterObjDaughters = context.selected_objects[:]
    if context.object not in CenterObjDaughters:
        CenterObjDaughters.append(context.object)

    print(f'CenterObjDaugters are {CenterObjDaughters}')
    if len(CenterObjDaughters) <= 2:
        # print(f'CenterObjDaugters are {CenterObjDaughters}')
        DaughterOne = context.active_object
        DaughterTwo = None
        for ob in CenterObjDaughters:  # setze das ob für zweite Tochter
            if ob != DaughterOne:
                DaughterTwo = ob

        # teste on which side a vertex of one object lays
        context.view_layer.objects.active = obj
        # apply rotation centerplane obj damit die vector rechnung funktioniert
        # bpy.ops.object.transform_apply(   ###########################################removed while searching for coup unparenting and single to multiple, coup verschieben problem
        #    location=False, rotation=True, scale=True)

        direction = SideOfPlane(context, obj, DaughterOne)

        if direction < 0:
            # print('Object auf der Positiven Seite')
            DaughterOne_side = "POSITIV"
            DaughterTwo_side = "NEGATIV"
            applyRemoveCouplMods(DaughterOne, obj, DaughterOne_side)
        elif direction > 0:
            # print('negativ seite')
            DaughterOne_side = "NEGATIV"
            DaughterTwo_side = "POSITIV"
            applyRemoveCouplMods(DaughterOne, obj, DaughterOne_side)

        else:
            print('Probleme with side detection')

        if DaughterTwo == None:
            bpy.context.window_manager.popup_menu(
                noCutthroughWarn, title="Error", icon='ERROR')  # raise error message
        else:
            applyRemoveCouplMods(DaughterTwo, obj, DaughterTwo_side)
        # deleConnector (later propably with checkbox)

        # sort the couplings to the new Daughters
        objects = bpy.data.objects
        DOneCoupList = []
        DTwoCoupList = []
        # sometimes its not in i'm not sure why
        if oriCoupname in oriCoupNames:
            oriCoupNames.remove(oriCoupname)
        print(
            f"oriCoupname list shouldnt have {oriCoupname} in it contains {oriCoupNames} ")

        for coupname in oriCoupNames:
            print(f"coupname {coupname} beim umsortieren in applysingle")
            coup = objects[coupname]
            mw = coup.matrix_world
            print(f"restliche Coup verteilen liste {coupname}")
            if bvhOverlap(context, coup, DaughterOne):
                # mw = coup.matrix_world
                remap_coup(context, coup, DaughterOne)
                # coup.parent = DaughterOne
                # coup.matrix_world = mw
                DOneCoupList.append(coup)
            if DaughterTwo != None:
                if bvhOverlap(context, coup, DaughterTwo):
                    remap_coup(context, coup, DaughterTwo)
                    # coup.parent = DaughterTwo
                    # coup.matrix_world = mw
                    DTwoCoupList.append(coup)

            if len(DTwoCoupList) == 0 and len(DOneCoupList) == 0:
                print(
                    f"after bvh false in applysingle {coup.name} and Daughter? ")
                unmap_coup(context, coup)
                # coup.parent = None
                # coup.matrix_world = mw
                # unmapped_signal(context, coup)

        # all modifiers of all couplings which are identified as overlapping
        DOneAllMods = AllCoupMods(context, DOneCoupList, DaughterOne)
        DTwoAllMods = AllCoupMods(context, DTwoCoupList, DaughterTwo)

        print(f"DoneAllMods {DOneAllMods}")
        print(f"DoneAllMods {DTwoAllMods}")

        for mod in DaughterOne.modifiers:
            if mod not in DOneAllMods:
                if "PUrP_" in mod.name:
                    print(f"ReMV {mod.name} from DaughterOne")
                    DaughterOne.modifiers.remove(mod)
                    # DORemovedMod = True
        if DaughterTwo != None:
            for mod in DaughterTwo.modifiers:
                if mod not in DTwoAllMods:
                    if "PUrP_" in mod.name:
                        print(f"ReMV {mod.name} from DaughterTwo")
                        DaughterTwo.modifiers.remove(mod)
                        # DTRemovedMod = True

        # delete Coupling

        context.view_layer.objects.active = obj

        if delete:
            removeCoupling(context, obj)
        Daughters = (DaughterOne, DaughterTwo)
        # print(f"coup parent after applysingle is {coup.parent}")
        # print(breapo)

        return Daughters

    elif len(CenterObjDaughters) > 2:  # branch where a planar cuts the Centerobj in many pieces
        print("more then 2 Daughters")

        # sort couplings by overlap

        objects = context.view_layer.objects  # bpy.data.objects
        DCoupList = []

        oriCoupNames.remove(oriCoupname)

        for Daughter in CenterObjDaughters:
            DCoupList = []
            print(f"Apply sortDaughter {Daughter.name}")
            for coupname in oriCoupNames:
                coup = objects[coupname]
                if bvhOverlap(context, coup, Daughter):
                    DCoupList.append(coup)

            if len(DCoupList) > 0:
                remap_coup(context, DCoupList[0], Daughter)
            # else:
            #    if not delete:
            #        unmap_coup(context, coup)

            # all modifiers of all couplings which are identified as overlapping
            DAllMods = AllCoupMods(context, DCoupList, Daughter)

            # remove all modifiers of Objects which are not intersecting anymore
            for mod in Daughter.modifiers:
                if mod not in DAllMods:
                    Daughter.modifiers.remove(mod)

        # if delete:
            # print(
            #    f" before remove multi daughters obj {obj.name} coup Coup.name")
        if delete:
            removeCoupling(context, obj)
        Daughters = CenterObjDaughters
        # print(f"blub blub remove coup mod {mod.fail} 2")
        return Daughters


class PP_OT_ApplyAllCouplings(bpy.types.Operator):
    '''Applies all Couplings of all selected Centerobjs. If a Coupling is selected, all Couplings connectected to the same Centerobject will be applied.'''
    bl_idname = "apl.allcoup"
    bl_label = "PP_OT_ApplyAllCouplings"
    bl_options = {'REGISTER', "UNDO"}

    @ classmethod
    def poll(cls, context):

        if (context.view_layer.objects.active != None):
            if context.mode == 'OBJECT' and context.area.type == 'VIEW_3D':
                if ("SingleConnector" in context.view_layer.objects.active.name) or ("PlanarConnector" in context.view_layer.objects.active.name):
                    return True
                for child in context.object.children:
                    if ("SingleConnector" in child.name) or ("PlanarConnector" in child.name):
                        return True
        else:
            return False

    def execute(self, context):
        PUrP = context.scene.PUrP
        PUrP_name = PUrP.PUrP_name
        # data = bpy.data
        # global Daughtercollection

        # wenn nichts selected, gehe durch alle objecte und schaue ob die bearbeitet wurden (müssen Couplings haben)
        if context.selected_objects == None:
            self.report(
                {'WARNING'}, "Please select a Centerobject or a connector!")

        elif context.selected_objects != None:
            Cobjlist = []
            selected = context.selected_objects[:]
            for obj in selected:
                # CenterBool = False
                # wenn couplin type selected , finde Papa und sende es
                if is_coup(context, obj):
                    # print("I am a selected Connector such meinen Papa")
                    if obj.parent not in Cobjlist:
                        Cobjlist.append(obj.parent)

                else:
                    for child in obj.children:  # gibt es kinder Coupling in diesem Object
                        if is_coup(context, child):
                            if obj not in Cobjlist:
                                Cobjlist.append(obj)

            print(
                f"List of Centerobj on the way to the Cobjdecider {Cobjlist}")
            for obj in Cobjlist:
                if obj != None:
                    centerObjDecider(context, obj)

        # wenn coupling selected, apply für alle

        return {'FINISHED'}


class PP_OT_DeleteCoupling(bpy.types.Operator):
    '''Deletes the selected Connectors (ignores everything else)'''
    bl_label = "DeleteCouplings"
    bl_idname = "rem.coup"
    bl_options = {'REGISTER', "UNDO"}

    @ classmethod
    def poll(cls, context):

        if (context.view_layer.objects.active != None):
            if context.mode == 'OBJECT' and context.area.type == 'VIEW_3D':
                if ("SingleConnector" in context.view_layer.objects.active.name) or ("PlanarConnector" in context.view_layer.objects.active.name):
                    return True
        else:
            return False

    def execute(self, context):
        PUrP = context.scene.PUrP
        # active = context.view_layer.objects.active
        # objects = bpy.data.objects
        selected = context.selected_objects[:]

        coups = []

        for obj in selected:
            # print("obj in delete schleife {obj}")
            if is_coup(context, obj):
                coups.append(obj)

        print(f"coups are {coups}")
        for obj in coups:
            # clean selection array
            print("OBj check when it crash {obj.name}")
            for ob in context.selected_objects:
                ob.select_set(False)

                # name_active = obj.name
            for child in obj.children:
                child.hide_select = False
                child.select_set(True)
                bpy.ops.object.delete(use_global=False)

            if not is_unmapped(context, obj):
                # entferne modifier und zwar immer auch wenn es schon zerlegt ist
                for mod in obj.parent.modifiers:
                    # !!!!!!!!!!Das wird ein BUG     weil auch die ohne nummer gelöscht werden siehe lange zeile unten
                    if (str(obj.name) + '_diff' == mod.name) or (str(obj.name) + '_union' == mod.name) or (str(obj.name) + '_stick_fix' == mod.name) or (str(obj.name) + '_stick_diff' == mod.name) or (str(obj.name) == mod.name):
                        print(f'I delete modifier {mod.name}')
                        obj.parent.modifiers.remove(mod)

                obj.select_set(True)
                # print(f'selected objects{context.selected_objects}')
                bpy.ops.object.delete(use_global=True)
            else:
                obj.select_set(True)
                bpy.ops.object.delete(use_global=True)
            # context.view_layer.objects.active = context.scene.PUrP.CenterObj
            # order part
            PUrP = context.scene.PUrP

        if PUrP.OrderBool:
            update_order(context, PUrP.CenterObj)

        return{"FINISHED"}


def moveModdown(Coup, CenterObj):
    CoupModcount = howManyModsCoup(Coup.name, CenterObj)

    # list of coupling names connected to the centerobj
    PUrP_Modsnames, mods = couplingList(CenterObj)
    CoupList, mods = couplingList(CenterObj)

    #####
    for ele in PUrP_Modsnames:
        print(f"all  element  {ele} with index {PUrP_Modsnames.index(ele)}")
        if ele == Coup.name:
            # index of Coup name in list of all PUrP Mods (inkl.)
            coupindex = PUrP_Modsnames.index(ele)
    for ele in CoupList:
        print(f"all  element  {ele} with index {PUrP_Modsnames.index(ele)}")
        if ele == Coup.name:
            # index of Coup name in list of all PUrP Mods (inkl.)
            orderindex = CoupList.index(ele)

    # when its already lowest:index lowest modifier index lowestCou mod
    # wenn couplist index + 1 >= lenCouplist
    if orderindex+1 >= len(CoupList):
        print(
            'It is already the lowest modifier, orderindex {orderindex}, len(Couplist){len(Couplist)}')

        return {'FINISHED'}
    else:
        LowerCoup_name = PUrP_Modsnames[coupindex + 1]
        LowerCoupcount = howManyModsCoup(LowerCoup_name, CenterObj)
        indexLowestLowerCoup = modindex(
            CenterObj.modifiers[LowerCoup_name], CenterObj.modifiers) + LowerCoupcount - 1
        nameLowestLowerCoup = CenterObj.modifiers[indexLowestLowerCoup].name
        # print(f"nameLowestLowerCoup {nameLowestLowerCoup}")
        # now move the modifiers starting with the lowest of the coup children for as often as we have modifiers of LowerCoup
        realcoupindex = modindex(
            CenterObj.modifiers[PUrP_Modsnames[coupindex]], CenterObj.modifiers)
        indexLowestToMove = realcoupindex + CoupModcount - 1
        moveIndex = indexLowestToMove
        bpy.context.view_layer.objects.active = CenterObj

        while moveIndex >= realcoupindex:  # to move coups from bottom to top

            modifier = CenterObj.modifiers[moveIndex]

            print(
                f"modifier to move  {modindex(modifier, CenterObj.modifiers)}")

            # indexToMove =

            # runter so oft bis es unter dem letzten modifiers des lowerCoups ist
            while modindex(modifier, CenterObj.modifiers) < indexLowestLowerCoup:
                print(
                    f'one down for {modifier.name} index {modindex(modifier, CenterObj.modifiers)} index lowest {indexLowestLowerCoup}')
                modifiername = modifier.name
                bpy.ops.object.modifier_move_down(modifier=modifiername)
            moveIndex -= 1
            indexLowestLowerCoup -= 1

        bpy.context.view_layer.objects.active = Coup


# takes a coupling name and the CenterObj and returns how many modifiers beelong to the coupling
def howManyModsCoup(Coup_name, CenterObj):
    count = 0
    for mod in CenterObj.modifiers:
        if Coup_name in mod.name:
            count += 1
    return count


# returns list of modifiers on CenterObj belonging to one coup inclusive main modifier
def CoupModifiers(context, coup, CenterObj):
    CoupModlist = []
    for mod in CenterObj.modifiers:
        if coup.name in mod.name:
            CoupModlist.append(mod)
    return CoupModlist


# takes list of Singcouplings and returns all modifiers in one list
def AllCoupMods(context, Couplist, CenterObj):
    AllMods = []
    for coup in Couplist:
        allmodsOcoup = CoupModifiers(context, coup, CenterObj)
        print(f"append coup {coup} mods {allmodsOcoup} ")
        AllMods.extend(allmodsOcoup)
    return AllMods


def listPUrPMods(CenterObj):  # returns list of mod names
    namelist = []
    mods = []
    for mod in CenterObj.modifiers:
        if ("PUrP" in mod.name):
            namelist.append(mod.name)
            mods.append(mod)
    return namelist, mods

# returns Connectors name- and modifierlists of  a CenterObj


def couplingList(CenterObj):

    name = []
    mods = []
    for mod in CenterObj.modifiers:
        if "PUrP" in mod.name:
            if "diff" not in mod.name and "union" not in mod.name and "BuildVolume" not in mod.name:
                name.append(mod.name)
                mods.append(mod)
            elif "PlanarConnector" in mod.name:
                name.append(mod.name)
                mods.append(mod)
    return name, mods


def modindex(modifier, modifiers):
    count = 0
    for mod in modifiers:
        if mod.name == modifier.name:
            return count
        else:
            count += 1
    return -1


class PP_OT_MoveModDown(bpy.types.Operator):
    '''Move the selected Connector down in order'''
    bl_idname = "pup.moddown"
    bl_label = "PP_OT_MoveModDown"
    bl_options = {'REGISTER', "UNDO"}

    @ classmethod
    def poll(cls, context):

        if (context.view_layer.objects.active != None):
            if context.mode == 'OBJECT' and context.area.type == 'VIEW_3D':
                if is_single(context, context.object) or is_planar(context, context.object):
                    return True
        else:
            return False

    def execute(self, context):
        PUrP = context.scene.PUrP
        Coup = bpy.data.objects[context.object.name]
        CenterObj = Coup.parent
        data = bpy.data
        initialActivename = context.object.name[:]

        moveModdown(Coup, CenterObj)
        PUrP = context.scene.PUrP
        if PUrP.OrderBool:
            update_order(context, CenterObj)
        deselectall(context)
        context.view_layer.objects.active = data.objects[initialActivename]
        context.view_layer.objects.active.select_set(True)
        return {'FINISHED'}


class PP_OT_MoveModUp(bpy.types.Operator):
    '''Move the selected Connector up in order'''
    bl_idname = "pup.modup"
    bl_label = "PP_OT_MoveModup"
    bl_options = {'REGISTER', "UNDO"}

    @ classmethod
    def poll(cls, context):

        if (context.view_layer.objects.active != None):
            if context.mode == 'OBJECT' and context.area.type == 'VIEW_3D':
                if is_single(context, context.object) or is_planar(context, context.object):
                    return True
        else:
            return False

    def execute(self, context):
        Coup = bpy.data.objects[context.object.name]
        data = bpy.data
        CenterObj = Coup.parent
        PUrP = context.scene.PUrP
        PUrP_Modsnames, mods = couplingList(CenterObj)
        active = context.object
        initialActivename = active.name[:]

        for ele in PUrP_Modsnames:
            print(
                f"all  element  {ele} with index {PUrP_Modsnames.index(ele)}")
            if ele == Coup.name:
                # index of Coup name in own list in the list
                coupindex = PUrP_Modsnames.index(ele)

        print(f"Couindex for move up {coupindex}")
        # up is the same as the upper one down
        if coupindex == 0:
            print("It already the top modifier")
        else:
            coupindex -= 1
            Coup = bpy.data.objects[PUrP_Modsnames[coupindex]]

            moveModdown(Coup, CenterObj)

        # data = bpy.data

        if PUrP.OrderBool:
            update_order(context, CenterObj)

        deselectall(context)
        data = bpy.data
        context.view_layer.objects.active = data.objects[initialActivename]
        context.view_layer.objects.active.select_set(True)
        return {'FINISHED'}


class PP_OT_Ini(bpy.types.Operator):
    '''Initialize all PuzzleUrPrint-Magic'''
    bl_label = "Initialize PuzzleUrPrint"
    bl_idname = "purp.init"
    bl_options = {'REGISTER', "UNDO"}

    @ classmethod
    def poll(cls, context):

        if context.mode == 'OBJECT' and context.area.type == 'VIEW_3D':
            return True
        else:
            return False

    def execute(self, context):
        from bpy.types import Scene, Image, Object
        from .properties import PUrPropertyGroup
        active = context.view_layer.objects.active
        objects = bpy.data.objects
        scene = context.scene

        #########

        bpy.types.Scene.PUrP = bpy.props.PointerProperty(type=PUrPropertyGroup)
        bpy.types.Object.PUrPCobj = bpy.props.BoolProperty(
            name="PUrPCenterObj",
            description="True if obj was used as CenterObj for PUrP",
            default=False,
        )
        bpy.types.Screen.PUrPTutcount = bpy.props.IntProperty(
            name="PUrPTutorialCounter",
            description="Counts tutorial Pages",
            default=0,
        )
        #########
        MColName = "PuzzleUrPrint"

        # collection should not be necessary anymore
        if bpy.data.collections.find(MColName) < 0:
            collection = bpy.data.collections.new(
                name=MColName)  # makes collection
            # scene.collection.children.link(collection) ###### when its not linked the user can not delete and break the ui, better solution for init behaviour necessary

        # Scene.PUrP.CenterObj = bpy.props.PointerProperty(name="Object", type=Object)

        CenterObj = bpy.context.scene.PUrP.CenterObj
        CenterObj = active

        # Puzzle Ur print Element Name
        # bpy.types.Scene.PUrP.PUrP_name = bpy.props.StringProperty()
        PUrP = bpy.context.scene.PUrP
        PUrP.PUrP_name = "PUrP_"

        #version = float(bpy.app.version_string[:4])
        #print(f"Blender version is {version} vergleich {version <= 2.90}")
        # if version <= 2.90:
        PUrP.ExactOptBool = True
        # PUrP.SingleCouplingtypes = ('Cube', 'Cylinder', 'Cone')
        # CylVert

        return{"FINISHED"}


class PP_OT_TutorialButton(bpy.types.Operator):
    '''Start the 10 min Tutorial to learn about most of the settings in the Addon'''
    bl_idname = "purp.tutorial"
    bl_label = "Start Tutorial"
    bl_options = {'REGISTER', "UNDO"}

    @ classmethod
    def poll(cls, context):

        return True

    def execute(self, context):

        bpy.ops.purp.init()
        bpy.ops.purp.tutorialwindow()
        # bpy.ops.purp.tutorialwindow()
        PUrP = context.scene.PUrP

        return {'FINISHED'}


class PP_OT_ToggleCoupVisibilityOperator(bpy.types.Operator):
    '''Toggle the boolean modifier visibility of the selected connectors. Will make stuff slow'''
    bl_idname = "object.togglecoupvisibility"
    bl_label = "PP_OT_ToggleCoupVisibility"
    bl_options = {'REGISTER', "UNDO"}

    @ classmethod
    def poll(cls, context):

        if (context.view_layer.objects.active != None):
            if context.mode == 'OBJECT' and context.area.type == 'VIEW_3D':
                if is_coup(context, context.object):
                    return True
        else:
            return False

    def execute(self, context):
        PUrP = context.scene.PUrP
        inlaytogglebool = PUrP.InlayToggleBool
        CenterObj = None

        selected = selectedtocouplist(context, context.selected_objects)
        for coup in selected:

            # "PUrP" in ele.name:  # for selected coupling of PUrP
            if is_unmapped(context, coup):
                continue
            else:
                CenterObj = coup.parent

            if inlaytogglebool:
                names, mods = listPUrPMods(CenterObj)
            else:
                names, mods = couplingList(CenterObj)

            for mod in mods:
                if coup.name in mod.name:
                    if "diff" not in mod.name and "union" not in mod.name or is_planar(context, coup):
                        if mod.show_viewport == True:
                            mod.show_viewport = False
                        elif mod.show_viewport == False:
                            mod.show_viewport = True
                    else:
                        mod.show_viewport = CenterObj.modifiers[coup.name].show_viewport

        return {'FINISHED'}


class PP_OT_ActiveCoupDefaultOperator(bpy.types.Operator):
    '''Load settings of the active connector into the panel settings. Can be used as copy settings, while "Exchange" acts as paste'''

    bl_idname = "object.activecoupdefault"
    bl_label = "PP_OT_ActiveCoupDefault"
    bl_options = {'REGISTER', "UNDO"}

    @ classmethod
    def poll(cls, context):
        if (context.view_layer.objects.active != None):
            if context.mode == 'OBJECT' and context.area.type == 'VIEW_3D':
                if is_single(context, context.object) or is_planar(context, context.object):
                    return True
        else:
            return False

    def execute(self, context):
        PUrP = context.scene.PUrP
        obj = context.object

        if is_single(context, obj):
            children = obj.children

            if 'Plane' in obj.data.name:
                PUrP.SingleMainTypes = '1'
            elif is_joint(context, obj):
                PUrP.SingleMainTypes = '2'
                PUrP.MaincutVert = amount_jointverts(context, obj)

            if PUrP.ExactOptBool:
                if is_unmapped(context, obj):
                    PUrP.BoolModSettings = '1'
                else:
                    if obj.parent.modifiers[obj.name].solver == 'EXACT':
                        PUrP.BoolModSettings = '1'
                    elif obj.parent.modifiers[obj.name].solver == 'FAST':
                        PUrP.BoolModSettings = '2'
            # order correction
            for child in children:
                if "diff" in child.name:
                    self.obout = child
                elif "fix" in child.name or "union" in child.name:
                    self.obin = child

            bpy.ops.object.transform_apply(
                location=False, rotation=False, scale=True)

            PUrP.CutThickness = obj.modifiers['PUrP_Solidify'].thickness / \
                PUrP.GlobalScale
            # CoupScale
            if is_joint(context, obj):
                PUrP.CoupScale = obj.data.vertices[1].co.y / \
                    (3 * PUrP.GlobalScale)
            else:
                PUrP.CoupScale = obj.data.vertices[1].co.x / \
                    (3 * PUrP.GlobalScale)

            # more code because of order
            if len(children) == 0 or len(children) == 1:
                PUrP.SingleCouplingModes = "3"
            elif len(children) == 2 or len(children) == 3:
                if zSym(self.obout):
                    PUrP.SingleCouplingModes = "1"
                else:
                    PUrP.SingleCouplingModes = "2"

            scalefactor = PUrP.GlobalScale * PUrP.CoupScale  # * PUrP.CoupSize
            if not is_flat(context, obj):
                yv0 = self.obout.data.vertices[0].co.y

            if len(children) != 0:  # nicht flatcut
                # print(f"meshadata name {obj.data.name}")
                if "Cube" in self.obout.data.name:
                    PUrP.SingleCouplingTypes = '1'

                    PUrP.CoupSize = 2 * abs(yv0) / scalefactor

                    scalefactor *= PUrP.CoupSize
                    zv1 = self.obout.data.vertices[1].co.z
                    if PUrP.SingleCouplingModes == "1":
                        PUrP.zScale = 2*zv1 / scalefactor
                    else:
                        PUrP.zScale = zv1 / scalefactor
                elif "Cylinder" in self.obout.data.name:
                    PUrP.SingleCouplingTypes = '2'
                    PUrP.CoupSize = abs(yv0) / (scalefactor)
                    scalefactor *= PUrP.CoupSize

                    # PUrP.CylVert = len(obj.data.vertices)/2
                    PUrP.CylVert, ARadius, brad, upverts = self.coneanalysizer(  # cylinder is a special case of cone
                        context, self.obout)

                    PUrP.aRadius = ARadius / scalefactor
                    if PUrP.SingleCouplingModes == "1":
                        PUrP.zScale = 2*upverts[0].co.z/scalefactor
                    else:
                        PUrP.zScale = upverts[0].co.z/(scalefactor)
                elif "Cone" in self.obout.data.name:
                    PUrP.SingleCouplingTypes = '3'
                    PUrP.CoupSize = abs(yv0) / (scalefactor)
                    scalefactor *= PUrP.CoupSize

                    PUrP.CylVert, ARadius, BRadius, upverts = self.coneanalysizer(
                        context, self.obout)

                    PUrP.aRadius = ARadius / scalefactor
                    PUrP.bRadius = BRadius / scalefactor
                    # 1 bei stick, 2 bei MF
                    if PUrP.SingleCouplingModes == "1":
                        PUrP.zScale = upverts[0].co.z/scalefactor
                    else:
                        PUrP.zScale = upverts[0].co.z/(2*scalefactor)

                # for child in obj.children:
                    # if "diff" in child.name:

                # PUrP.zScale = self.obout.scale.z / PUrP.CoupSize
                # double check
                PUrP.BevelSegments = self.obout.modifiers[0].segments
                PUrP.BevelOffset = self.obout.modifiers[0].width
                diffchild = child
                # elif "fix" in child.name or "union" in child.name:
                outpoint = self.obout.data.vertices[0].co.y
                inpoint = self.obin.data.vertices[0].co.y
                PUrP.Oversize = (abs(outpoint) - abs(inpoint)
                                 ) / PUrP.GlobalScale

        elif is_planar(context, obj):
            PUrP.SingleCouplingModes = "4"
            if "Cubic" in obj.data.name:
                PUrP.PlanarCouplingTypes = "1"
            elif "Dovetail" in obj.data.name:
                PUrP.PlanarCouplingTypes = "2"
            elif "Puzzle1" in obj.data.name:
                PUrP.PlanarCouplingTypes = "3"
            elif "Puzzle2" in obj.data.name:
                PUrP.PlanarCouplingTypes = "4"
            elif "Puzzle3" in obj.data.name:
                PUrP.PlanarCouplingTypes = "5"
            elif "Puzzle4" in obj.data.name:
                PUrP.PlanarCouplingTypes = "6"
            elif "Puzzle5" in obj.data.name:
                PUrP.PlanarCouplingTypes = "7"
            elif "Arrow1" in obj.data.name:
                PUrP.PlanarCouplingTypes = "8"
            elif "Arrow2" in obj.data.name:
                PUrP.PlanarCouplingTypes = "9"
            elif "Arrow3" in obj.data.name:
                PUrP.PlanarCouplingTypes = "10"
            elif "Pentagon" in obj.data.name:
                PUrP.PlanarCouplingTypes = "11"
            elif "Hexagon" in obj.data.name:
                PUrP.PlanarCouplingTypes = "12"
            elif "T-RoundedAll" in obj.data.name:
                PUrP.PlanarCouplingTypes = "13"
            elif "T-RoundedTop" in obj.data.name:
                PUrP.PlanarCouplingTypes = "14"
            elif "T-Straight" in obj.data.name:
                PUrP.PlanarCouplingTypes = "15"
            elif "T-Straight" in obj.data.name:
                PUrP.PlanarCouplingTypes = "16"

            if PUrP.ExactOptBool:
                if is_unmapped:
                    PUrP.BoolModSettings = '1'
                else:
                    if obj.parent.modifier[obj.name + "_diff"].solver == 'EXACT':
                        PUrP.BoolModSettings = '1'
                    elif obj.parent.modifier[obj.name + "_diff"].solver == 'FAST':
                        PUrP.BoolModSettings = '2'

            # Apply scale e.g. zscale determination
            bpy.ops.object.transform_apply(
                location=False, rotation=False, scale=True)

            PUrP.Oversize = obj.modifiers["PUrP_Solidify"].thickness / \
                PUrP.GlobalScale
            PUrP.LineDistance = obj.modifiers["PUrP_Array_2"].constant_offset_displace[1]
            PUrP.LineCount = obj.modifiers["PUrP_Array_2"].count
            PUrP.LineLength = obj.modifiers["PUrP_Array_1"].count

            #
            PUrP.OffsetRight, PUrP.OffsetLeft, PUrP.zScale, PUrP.StopperHeight = planaranalysizerLocal(
                context, obj)
            # Stopperbool test

        return {'FINISHED'}

    def coneanalysizer(self, context, obj):
        # Cyclvert, and the radius are extrakted; Coupling types
        PUrP = context.scene.PUrP

        upperverts = []
        lowerverts = []
        for vert in obj.data.vertices:

            if vert.co.z > 0:
                upperverts.append(vert)
            elif vert.co.z <= 0:
                lowerverts.append(vert)
        # upperverts information
        if len(upperverts) == 1:  # hard tip
            bRadius = 0.0
        else:  # soft tip
            bRadius = obj.data.vertices[1].co.y

        aRadius = obj.data.vertices[0].co.y
        Cyclvert = len(lowerverts)

        '''
            for v in upperverts:
                # vert on an axis has the radius as co.axis
                if v.co.x == 0:
                    bRadius = v.co.y
                    bRadius = bRadius / (PUrP.GlobalScale * PUrP.CoupScale)
                    break
                if v.co.y == 0:
                    bRadius = v.co.x
                    bRadius = bRadius / (PUrP.GlobalScale * PUrP.CoupScale)
                    break
        # lower radius

        for v in lowerverts:
            if v.co.x == 0:
                aRadius = v.co.y
                aRadius = aRadius/(PUrP.GlobalScale * PUrP.CoupScale)
                break
            if v.co.y == 0:
                aRadius = v.co.x
                aRadius = aRadius / (PUrP.GlobalScale * PUrP.CoupScale)
                break
            '''
        return Cyclvert, aRadius, bRadius, upperverts


class PP_OT_CouplingOrder(bpy.types.Operator):
    '''Show Connector order of the selected Centerobject'''
    bl_idname = "pup.couplingorder"
    bl_label = "PP_OT_CouplingOrder"
    bl_options = {'REGISTER', "UNDO"}

    @ classmethod
    def poll(cls, context):
        if (context.object != None):
            if context.mode == 'OBJECT' and context.area.type == 'VIEW_3D':
                # print(f"context.object != None {context.object != None}")
                if context.object.PUrPCobj:
                    return True
                elif context.object.parent != None:
                    if context.object.parent.PUrPCobj:
                        return True
                    else:
                        return False
                else:
                    return False
        else:
            return False

    def execute(self, context):
        active = context.object
        PUrP = context.scene.PUrP
        initialActivename = active.name[:]
        # determine CenterObj from active CenterObj or Coupling
        CenterObj = PUrP.CenterObj
        if active.PUrPCobj:
            PUrP.CenterObj = context.object
            CenterObj = PUrP.CenterObj
        elif active.parent != None:
            if active.parent.PUrPCobj:
                PUrP.CenterObj = context.object.parent
                CenterObj = PUrP.CenterObj

        # toggle mechanism
        OrderBool = PUrP.OrderBool
        if OrderBool:
            PUrP.OrderBool = False
        else:
            PUrP.OrderBool = True

       # for ob in data.objects:
       #     if "PUrP" in ob.name and "_Order" in ob.name:  # gibt es objecte mit order -- > dann lösche nur
       #         Orderbool = False
       #         break

        # update or delete order
        data = bpy.data
        deselectall(context)
        if PUrP.OrderBool:
            update_order(context, CenterObj)
        else:
            removePUrPOrder()
        context.view_layer.objects.active = data.objects[initialActivename]
        context.view_layer.objects.active.select_set(True)
        return {'FINISHED'}


def update_order(context, CenterObj):
    data = bpy.data
    active = context.object
    PUrP = context.scene.PUrP
    try:
        initialActivename = active.name[:]
    except:
        initialActivename = PUrP.CenterObj.name

    # garbage run
    removePUrPOrder()
    # new numbers
    PUrPlist, mods = couplingList(CenterObj)
    for num, modname in enumerate(PUrPlist):
        matrixWorld = data.objects[modname].matrix_world
        bpy.ops.object.text_add(
            enter_editmode=False, location=(0, 0, 0))
        obj = context.object
        obj.name = modname + "_Order"

        obj.location.z += 0.5 * PUrP.GlobalScale

        obj.data.body = str(num+1)
        obj.data.extrude = 0.05
        obj.show_in_front = True
        obj.display_type = 'WIRE'
        obj.hide_select = True
        obj.parent = data.objects[modname]
        obj.matrix_world = matrixWorld
        obj.rotation_euler.x = 1.5708
        obj.location.x -= 0.3
        obj.scale = mathutils.Vector(
            (PUrP.GlobalScale, PUrP.GlobalScale, PUrP.GlobalScale))
        bpy.ops.object.transform_apply(
            location=False, rotation=False, scale=True)

        # context.view_layer.objects.active = CenterObj

    context.view_layer.objects.active = data.objects[initialActivename]
    context.view_layer.objects.active.select_set(True)


class PP_OT_TestCorrectnameOperator(bpy.types.Operator):
    bl_idname = "object.pp_ot_testcorrectname"
    bl_label = "PP_OT_TestCorrectname"
    bl_options = {'REGISTER', "UNDO"}

    def execute(self, context):
        coup = context.object
        selected = context.selected_objects

        # for ob in selected:
        #    if ob != coup:
        #        Cob = ob
        # origin_in_bb(context, coup, Cob)

        # context.view_layer.objects.active = coup
        # Cob.select_set(True)
        gen_arrow(context, (0, 0, 0))
        # correctname(context, coup)
        return {'FINISHED'}


class PP_OT_ReMapCoups(bpy.types.Operator):
    '''Remap selected Connector to active object. First select Connector, then the object'''
    bl_idname = "object.remapcoups"
    bl_label = "PP_OT_ReMapCoups"
    bl_options = {'REGISTER', "UNDO"}

    @ classmethod
    def poll(cls, context):
        if (context.object != None):
            if context.mode == 'OBJECT' and context.area.type == 'VIEW_3D':
                # print(f"context.object != None {context.object != None}")
                if not is_coup(context, context.object):
                    if len(context.selected_objects) > 1:
                        return True

        return False

    def execute(self, context):
        
        selected = selectedtocouplist(context, context.selected_objects[:])
        active = context.object
        CenterObj = context.object
        applyScale(CenterObj)
        
        if is_coup(context, active) or is_buildvolume(context, active):
            self.report(
                {'WARNING'}, "Active object is a connector or BuildVolume!")
            return {'FINISHED'}
        elif not CenterObj.PUrPCobj:
            print('Active was never a Centerobject before')
        PUrP = context.scene.PUrP
        print(f'CenterObj {CenterObj}')
        CenterObj.PUrPCobj = True
        
        # remove from original parent
        for coup in selected:
            correctname(context, coup)
            remap_coup(context, coup, CenterObj)
        
        PUrP.CenterObj = CenterObj
        return {'FINISHED'}


def is_mapped_correct(context, coup, CObj):
    # defintion
    # parented to CenterObj
    # all bool mods on CenterObj
    print(f" coup parent in is mapped correct {coup.parent}")
    if coup.parent == CObj:
        modnames, mods = listPUrPMods(CObj)
        print(modnames)
        if len(modnames) != 0:
            if coup.name in modnames:
                print('coup name in modnames')
                if is_stick(context, coup):
                    print('coup name in modnames')
                    if coup.name + "_stick_diff" in modnames:
                        print('coup name in modnames')
                        return True
                elif is_mf(context, coup):
                    if coup.name + "_diff" in modnames:
                        if coup.name + "_union" in modnames:
                            return True
                elif is_planar(context, coup):
                    return True

    print(f"coup {coup.name} is not mapped correctly to CObj")
    return False


def remap_coup(context, coup, CenterObj):
    # applyScale(CenterObj)
    # check if already mapped correctly
    if is_mapped_correct(context, coup, CenterObj):
        return

    #
    if coup.parent != None:
        Couplist = [coup]

        AllCoupmods = AllCoupMods(context, Couplist, coup.parent)
        for mod in AllCoupmods:
            # remove in parent
            print(f"blieb remove coup mod {mod.name} from {CenterObj}")
            coup.parent.modifiers.remove(mod)

    if is_single(context, coup):

        ensure_mod(context, coup, CenterObj, '')
        '''mod = CenterObj.modifiers.new(
            name=coup.name, type="BOOLEAN")
        set_modvisbility(context, mod)
        mod.object = coup
        mod.operation = 'DIFFERENCE'
        set_BoolSolver(context, mod)
        '''
        # inlay modifiers
        for child in coup.children:
            if "Order" not in child.name and "fix" not in child.name:

                if is_mf(context, coup):
                    if "_diff" in child.name:
                        ensure_mod(context, child, CenterObj, 'diff')
                        # mod.operation = 'DIFFERENCE'
                    elif '_union' in child.name:
                        ensure_mod(context, child, CenterObj, 'union')
                        # mod.operation = 'UNION'
                elif is_stick(context, coup):
                    if "_stick_diff" in child.name:
                        ensure_mod(context, child, CenterObj, 'stick_diff')
                        # mod.operation = 'DIFFERENCE'
                    # elif '_union' in child.name:
                     #   ensure_mod(context, child, CenterObj, 'union')
                        # mod.operation = 'UNION'

    elif is_planar(context, coup):
        ensure_mod(context, coup, CenterObj, '')
        '''
        mod = CenterObj.modifiers.new(
            name=coup.name, type="BOOLEAN")
        set_modvisbility(context, mod)
        mod.object = coup
        mod.operation = 'DIFFERENCE'
        set_BoolSolver(context, mod)'''

    matrix_w = coup.matrix_world #.copy()
    print(matrix_w)

    coup.parent = CenterObj
    coup.matrix_world = matrix_w
    
    # remove remap sign
    remove_order_tag(context, coup)

    bpy.ops.object.delete(use_global=False)


def set_modvisbility(context, mod):
    PUrP = context.scene.PUrP
    mod.show_viewport = PUrP.ViewPortVisAdd


class PP_OT_UnmapCoup(bpy.types.Operator):
    bl_idname = "object.pp_ot_unmapcoup"
    bl_label = "PP_OT_UnmapCoup"
    bl_options = {'REGISTER', "UNDO"}

    @ classmethod
    def poll(cls, context):
        if (context.object != None):
            if context.mode == 'OBJECT' and context.area.type == 'VIEW_3D':
                # print(f"context.object != None {context.object != None}")
                if is_coup(context, context.object):
                    return True

        else:
            return False

    def execute(self, context):
        PUrP = context.scene.PUrP
        coups = selectedtocouplist(context, context.selected_objects)

        for coup in coups:
            correctname(context, coup)
            if not is_unmapped(context, coup):
                # if is_planar(context, coup) or is_single(context, coup):

                unmap_coup(context, coup)
                # mw = coup.matrix_world

                # change_parent(context, coup, None)
                # coup.parent = None
                # coup.matrix_world = mw
                # remove_coupmods(context, coup)
                # unmapped_signal(context, coup)

        return {'FINISHED'}


def unmap_coup(context, coup):
    if not is_unmapped(context, coup):
        # if is_planar(context, coup) or is_single(context, coup):
        mw = coup.matrix_world
        change_parent(context, coup, None)
        # coup.parent = None
        coup.matrix_world = mw
        remove_coupmods(context, coup)
        unmapped_signal(context, coup)


class PP_OT_MakeBuildVolume(bpy.types.Operator):
    '''Makes a wireframe cube in the size of the settings above. Nothing more than a scale landmark.'''
    bl_idname = "object.makebuildvolume"
    bl_label = "PP_OT_MakeBuildVolume"
    bl_options = {'REGISTER', "UNDO"}

    def execute(self, context):
        PUrP = context.scene.PUrP
        BuildplateX = PUrP.BuildplateX
        BuildplateY = PUrP.BuildplateY
        BuildplateZ = PUrP.BuildplateZ

        cursorloc = context.scene.cursor.location

        bpy.ops.mesh.primitive_cube_add(
            enter_editmode=False, align='WORLD', location=cursorloc)
        BuildVol = context.object
        BuildVol.name = "PUrP_BuildVolume"

        BuildVol.scale[0] = BuildplateX/2 * PUrP.GlobalScale  # cube is 2m
        BuildVol.scale[1] = BuildplateY/2 * PUrP.GlobalScale
        BuildVol.scale[2] = BuildplateZ/2 * PUrP.GlobalScale

        BuildVol.display_type = 'WIRE'
        bpy.ops.object.transform_apply(
            location=False, rotation=False, scale=True)

        mod1 = BuildVol.modifiers.new(
            name="PUrP_BuildVol_ArrayX", type='ARRAY')
        mod1.count = 1

        mod2 = BuildVol.modifiers.new(
            name="PUrP_BuildVol_ArrayY", type='ARRAY')
        mod2.relative_offset_displace[0] = 0
        mod2.relative_offset_displace[1] = 1
        mod2.count = 1

        mod3 = BuildVol.modifiers.new(
            name="PUrP_BuildVol_ArrayZ", type='ARRAY')
        mod3.relative_offset_displace[0] = 0
        mod3.relative_offset_displace[2] = 1
        mod3.count = 1
        return {'FINISHED'}


class PP_OT_ApplyPlanarMultiObj(bpy.types.Operator):
    '''Applys the active planar connector to all selected objects. First select all objects, then the planar connector last.'''
    bl_idname = "object.applyplanarmultiobj"
    bl_label = "PP_OT_ApplyPlanarMultiObj"
    bl_options = {'REGISTER', "UNDO"}

    @ classmethod
    def poll(cls, context):
        if (context.object != None):
            if context.mode == 'OBJECT' and context.area.type == 'VIEW_3D':
                if len(context.selected_objects) > 1:
                    if is_planar(context, context.object):
                        return True

        else:
            return False

    def execute(self, context):

        coup = bpy.data.objects[context.object.name]

        # Centerobjects sammeln
        CenterObjs = []
        for ob in context.selected_objects:
            if not is_coup(context, ob):  # fail selection
                CenterObjs.append(ob)

        # suchen nach dem Centerobj mit dem Planar?
        OriCenterObj = coup.parent

        # Generate Modifier on all CenterObj and apply
        for CenterObj in CenterObjs:

            # is there already a modifier for this coup
            BoolCool = False
            for mod in CenterObj.modifiers:
                if mod.name == coup.name:
                    BoolCool = True

            if not BoolCool:
                mod = CenterObj.modifiers.new(coup.name, 'BOOLEAN')
                mod.object = coup
                mod.operation = 'DIFFERENCE'
                set_BoolSolver(context, mod)

            context.view_layer.objects.active = CenterObj
            bpy.ops.object.modifier_apply(modifier=coup.name)

            # CenterObj.modifiers.new(coup.name, 'BOOLEAN')

            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.separate(type='LOOSE')
            bpy.ops.object.editmode_toggle()

        # delete planar coupling
        removeCoupling(context, coup)

        return {'FINISHED'}


def ensuremodvis(context, mod):

    if not mod.show_render:
        mod.show_render = True
    if not mod.show_viewport:
        mod.show_viewport = True

# apply multiple planar to  active object  ---- maybe alternative with the normal one


class PP_OT_ApplyMultiplePlanarToObject(bpy.types.Operator):
    '''Apply multiple planar connectors to the active object. First select all planar connectors and then the center obj last. Helpful when CenterObj will be cut in a lot of pieces'''
    bl_idname = "object.applymultipleplanartoobject"
    bl_label = "PP_OT_ApplyMultiplePlanarToObject"
    bl_options = {'REGISTER', "UNDO"}

    @ classmethod
    def poll(cls, context):
        if (context.object != None):
            if context.mode == 'OBJECT' and context.area.type == 'VIEW_3D':
                if not is_planar(context, context.object) and not is_single(context, context.object):
                    if len(context.selected_objects) > 1:
                        for ob in context.selected_objects:
                            if is_planar(context, ob):
                                return True

        return False

    def execute(self, context):
        selected = context.selected_objects[:]
        CenterObj = bpy.data.objects[context.object.name]
        PUrP = context.scene.PUrP

        coups = []
        # deselect all for the separate by selection
        for ob in selected:
            ob.select_set(False)
            if is_planar(context, ob):
                coups.append(ob)

        # check for modifier
        for coup in coups:
            # if "PlanarConnector" not in coup.name:
            #    continue
            
            ensure_mod(context, coup, CenterObj, "")


            ####should just apply all modifiers without Seperation!!!!!!!!!!
            #applySingleCoup(context, coup, CenterObj, not context.scene.PUrP.KeepCoup)

            ''' 
            is_coup = False
            for mod in CenterObj.modifiers:
                if mod.name == coup.name:
                    is_coup = True
                    break
            # make modifiers when there aren't the right ones
            if not is_coup:
                
                CenterObj.modifiers.new(coup.name, "BOOLEAN")
                mod.object = coup
                mod.operation = 'DIFFERENCE'
            '''
            # context.view_layer.objects.active = CenterObj
            #bpy.ops.object.modifier_apply(modifier=coup.name)
            #removeCoupling(context, coup)
        
        ###apply all purp mods
        

        for coup in coups[:]:
            #bpy.ops.object.mode_set(mode = 'OBJECT')
            deselectall(context)
            CenterObj.select_set(True)
            context.view_layer.objects.active = CenterObj
            bpy.ops.object.modifier_apply(modifier=coup.name)
            if PUrP.KeepCoup == False:
                removeCoupling(context, coup)
        


        CenterObj.select_set(True)
        context.view_layer.objects.active = CenterObj
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}


class PP_OT_ApplySingleToObjects(bpy.types.Operator):
    '''Applys the active Singleconnector to the selected objects. Select the objects first and the connector last.'''
    bl_idname = "object.applysingletoobjects"
    bl_label = "Apply Selected Single Connectors to active object"
    bl_options = {'REGISTER', "UNDO"}

    @ classmethod
    def poll(cls, context):
        if (context.object != None):
            if context.mode == 'OBJECT' and context.area.type == 'VIEW_3D':
                # print(f"context.object != None {context.object != None}")
                if is_coup(context, context.object):
                    if len(context.selected_objects) > 1:
                        for ob in context.selected_objects:
                            if is_single(context, ob):
                                return True

        return False

    def execute(self, context):
        data = bpy.data
        coup = bpy.data.objects[context.object.name]
        PUrP = context.scene.PUrP

        
        # stop when its the wrong active
        if not is_coup(context, coup) or is_planar(context, coup) or is_flat(context, coup):
            self.report({'WARNING'}, "Wrong active Object")
            return {'FINISHED'}

        # type of coup
        couptype = None
        if is_stick(context, coup):
            couptype = 'STICK'
        if is_mf(context, coup):
            couptype = 'MF'

        # Centerobjects sammeln
        CenterObjs = []
        for ob in context.selected_objects:
            if ob != coup:
                if not is_coup(context, ob):
                    CenterObjs.append(ob)
        # break when only coup was selected
        if len(CenterObjs) == 0:
            return{'FINISHED'}

        remove_order_tag(context, coup)
        # find the CenterObj with the closest distance to the mainplane
        # distancelist = []
        OverLapCenterObjs = []
        for Cob in CenterObjs:
            # distancelist.append(SideOfPlane(context, coup, Cob))
            if bvhOverlap(context, coup, Cob):
                # overlappcount += 1
                OverLapCenterObjs.append(Cob)

        # child zuordnung
        for child in coup.children:
            if coup.name + "_stick_fix" in child.name:
                fix = child
            elif coup.name + "_stick_diff" in child.name or coup.name + "_diff" in child.name:
                diff = child
            elif coup.name + "_union" in child.name:
                union = child

        # OverLapCenterObj = OverLapCenterObjs[0]  # not lösung erstmal

        # add inlay mods to CenterObjs
        print(CenterObjs)
        foundBase = None
        for num, Cob in enumerate(CenterObjs):

            print(f"Processing now Cob {Cob.name}")
            context.view_layer.objects.active = Cob
            Cob.select_set(True)
            if couptype == 'STICK':
                # stick case
                print("Stick")
                # mainplane
                if bvhOverlap(context, coup, Cob):
                    # ignore mainplane
                    remove_mod(context, coup, coup.parent, "")
                    remove_mod(context, diff, coup.parent, "stick_diff")
                    
                    mw = coup.matrix_world.copy()
                    coup.parent = Cob
                    coup.matrix_world = mw
                    if not PUrP.IgnoreMainCut:
                        # union + das Cobjs
                        # mit mainplane mach das ganze applyteil inkl. seperate by loose parts

                        ensure_mod(context, coup, Cob, "")

                        # ensure_mod(context, diff, Cob, "stick_diff")
                        daughters = cut_n_separate(context, coup, Cob)
                        print(f"Daughters {daughters} ")
                        for daughter in daughters:
                            print(f"taking care of daughter {daughter.name}")
                            context.view_layer.objects.active = daughter
                            ensure_mod(context, diff, daughter, "stick_diff")
                            bpy.ops.object.modifier_apply(
                                modifier=coup.name + "_stick_diff")
                        print(f"Daughters set {Cob.name}")
                        # applySingleCoup(context, coup, Cob, PUrP.KeepCoup)
                    else:
                        context.view_layer.objects.active = Cob
                        ensure_mod(context, diff, Cob, "stick_diff")
                        bpy.ops.object.modifier_apply(
                            modifier=coup.name + "_stick_diff")
                else:
                    # without overlap just add the inlay mod and apply
                    context.view_layer.objects.active = Cob
                    ensure_mod(context, diff, Cob, "stick_diff")
                    bpy.ops.object.modifier_apply(
                        modifier=coup.name + "_stick_diff")

                # letzte Runde, delete or dublicate
                # last in line
                if num == len(CenterObjs)-1:
                    if PUrP.KeepCoup:
                        newfix = copyobject(context, fix, Cob.name + "_stick")
                        print(f"made newfix {newfix.name}")
                        newfix.parent = None
                        newfix.display_type = 'SOLID'
                        newfix.show_in_front = True
                        newfix.hide_select = False
                        print(f"new fix is set to {newfix.hide_select}")

                        if not is_unmapped:
                            unmap_coup(context, coup)
                            # change_parent(context, coup, None)
                            # unmapped_signal(context, coup)

                    else:
                        data.objects.remove(
                            data.objects[coup.name + "_stick_diff"])
                        mw = fix.matrix_world.copy()
                        fix.parent = None
                        fix.matrix_world = mw
                        fix.display_type = 'SOLID'
                        fix.show_in_front = True
                        fix.hide_select = False
                        fix.name = Cob.name + "_stick"

                        # remove mainplane when not keep
                        print("remove coup {coup.name}")
                        data.objects.remove(coup)

            elif couptype == 'MF':
                foundCob = None
                # MF case
                print("MF")
                if origin_in_bb(context, coup, Cob):
                    print(f"Detected {Cob} as Base CenterObj")
                    # change_parent(context, coup, Cob)

                    if not PUrP.IgnoreMainCut:
                        # applying the base unmapps coup, better apply to base after the last Cob is processed
                        foundBase = Cob

                    else:
                        print(f"ignore mainplane --> apply {union.name} ")
                        foundBase = Cob
                        ensure_mod(context, union, Cob, "union")
                        # print(f"{union.fail}")
                        context.view_layer.objects.active = Cob
                        bpy.ops.object.modifier_apply(
                            modifier=coup.name + "_union")

                        # union + das Cobjs
                        # mit mainplane mach das ganze applyteil inkl. seperate by loose parts
                        # foundCob = Cob
                        # applySingleCoup(context, coup, Cob, PUrP.KeepCoup)
                else:  # wenn nicht zentraler CObj mach ein loch und zieh die mainplane ab
                    # erst diff
                    print(f"{Cob} is not foundBase  ")
                    context.view_layer.objects.active = Cob
                    if not PUrP.IgnoreMainCut:
                        ensure_mod(context, coup, Cob, "")

                        bpy.ops.object.modifier_apply(modifier=coup.name)

                    ensure_mod(context, diff, Cob, "diff")
                    Cob.select_set(True)
                    # apply modifier

                    bpy.ops.object.modifier_apply(modifier=coup.name + "_diff")

                    # the mainplane for MF when not the base Cob

                # after last Cobj
                if num == len(CenterObjs)-1:
                    print(
                        "Operation after last Cob Cycle Last, heres should apply and delete/unmapp ")
                    # wenn keep
                    if PUrP.KeepCoup:
                        # unmap coup
                        if PUrP.IgnoreMainCut:
                            if not is_unmapped:
                                unmap_coup(context, coup)
                            # change_parent(context, coup, None)
                            # unmapped_signal(context, coup)
                        else:
                            if foundBase != None:
                                # foundBase.PUrPCobj = True
                                # change_parent(context, coup, foundBase)
                                # ensure_mod(context, coup, foundBase, "")
                                # ensure_mod(context, union, foundBase, "union")
                                # ensure_mod(context, diff, foundBase, "diff")
                                remap_coup(context, coup, foundBase)
                                applySingleCoup(
                                    context, coup, foundBase, PUrP.KeepCoup)
                            if not is_unmapped(context, coup):
                                unmap_coup(context, coup)
                            # change_parent(context, coup, None)
                            # unmapped_signal(context, coup)
                    else:
                        # when everything is done apply or remove couple to found Cob
                        if PUrP.IgnoreMainCut:
                            removeCoupling(context, coup)
                        else:
                            if foundBase != None:

                                foundBase.PUrPCobj = True
                                # change_parent(context, coup, foundBase)
                                remap_coup(context, coup, foundBase)
                                # ensure_mod(context, coup, foundBase, "")
                                # ensure_mod(context, union, foundBase, "union")
                                # ensure_mod(context, diff, foundBase, "diff")
                                applySingleCoup(
                                    context, coup, foundBase, PUrP.KeepCoup)

                            removeCoupling(context, coup)

        return {'FINISHED'}


class PP_OT_ConnectorHide(bpy.types.Operator):
    '''Toggles the viewport visibility of the selected connectors'''
    bl_idname = "purp.connectorhide"
    bl_label = "Toggle Connector Visibility of Selected"
    bl_options = {'REGISTER', "UNDO"}

    @ classmethod
    def poll(cls, context):

        if context.mode == 'OBJECT' and context.area.type == 'VIEW_3D':
            if (context.object != None):
                if is_coup(context, context.object):
                    return True
        return False

    def execute(self, context):
        couplist = selectedtocouplist(context, context.selected_objects)
        hide = couplist[0].hide_viewport
        for coup in couplist:
            coupvisset(context, coup, not hide)
        return {'FINISHED'}


class PP_OT_AllConnectorHide(bpy.types.Operator):
    '''Toggle viewport visibility of all Connectors in the scene'''
    bl_idname = "purp.allconnectorhide"
    bl_label = "Toggle Connector Visibility of All"
    bl_options = {'REGISTER', "UNDO"}

    @ classmethod
    def poll(cls, context):
        if context.mode == 'OBJECT' and context.area.type == 'VIEW_3D':
            return True
        return False

    def execute(self, context):
        couplist = selectedtocouplist(context, bpy.data.objects)
        if len(couplist) > 0:
            hide = couplist[0].hide_viewport
            for coup in couplist:
                coupvisset(context, coup, not hide)

        return {'FINISHED'}


def planaranalysizerLocal(context, Coup):
    PUrP = context.scene.PUrP

    coupfaktor = PUrP.PlanarCorScale * PUrP.GlobalScale

    v3c = Coup.data.vertices[3].co  # @Coup.matrix_world
    print(f"Cubic {Coup.data.name}")

    # compensate for the 3 different position of vert3 in planar objects
    if "Cubic" in Coup.data.name or "Puzzle" in Coup.data.name:
        print("Cube ............................")
        PUrP.CoupScale = v3c[0] / coupfaktor
    elif "Dovetail" in Coup.data.name or "Arrow" in Coup.data.name or "Hexagon" in Coup.data.name or "Pentagon" in Coup.data.name:
        print("Dove")
        PUrP.CoupScale = v3c[0]*2 / coupfaktor
    elif "T" in Coup.data.name:
        print("T")
        PUrP.CoupScale = v3c[0]/0.4 / coupfaktor
    else:
        print("fail")

    print("fail..................................................")
    v0c = Coup.data.vertices[0].co  # @Coup.matrix_world
    OffsetRight = v0c[0] - 1.5*coupfaktor * PUrP.CoupScale

    v1c = Coup.data.vertices[1].co  # @Coup.matrix_world
    OffsetLeft = abs(v1c[0]) - 1.5*coupfaktor * PUrP.CoupScale

    # zscale and StopperHeight
    lowestvert = 0
    for vert in Coup.data.vertices:  # find lowest z coordinate
        vco = vert.co  # @Coup.matrix_world
        if vco[2] <= lowestvert:
            lowestvert = vco[2]

    lowestlist = []
    lowestexample = Coup.data.vertices[0]
    for vert in Coup.data.vertices:  # collect all verts with lowest co.z values
        vco = vert.co  # @Coup.matrix_world
        if vco[2] == lowestvert:
            lowestlist.append(vco[2])
            lowestexample = vert  # example for stopperheight evaluation

    lowestexampleco = lowestexample.co  # @Coup.matrix_world
    PUrP.StopperBool = False
    if len(lowestlist) == 4:  # with 4 verts its a stopper
        PUrP.StopperBool = True

    # for stopper height such den kürzesten abstand bei gleichen x
    # smallestdistance = 50
    distance = []

    for vert in Coup.data.vertices:
        vco = vert.co  # @Coup.matrix_world
        if vco[0] == lowestexampleco[0]:
            if vco[1] == lowestexampleco[1]:
                if vco[2] != lowestexampleco[2]:
                    # collect distances to vert
                    distance.append(
                        vco[2] - lowestexampleco[2])
                    # print(f"distance {vert.co.z - lowestexample.co.z}")
    distance.sort()
    StopperHeight = distance[0]

    # zscale top vert at co.z = 0
    if PUrP.StopperBool == True:
        zScale = -lowestexampleco[2] - distance[0]
    else:
        zScale = distance[0]

    return OffsetRight, OffsetLeft, zScale, StopperHeight


def planaranalysizerGlobal(context, Coup):
    PUrP = context.scene.PUrP

    coupfaktor = PUrP.PlanarCorScale * PUrP.GlobalScale
    v3c = Coup.data.vertices[3].co@Coup.matrix_world

    # compensate for the 3 different position of vert3 in planar objects
    if "Cubic" in Coup.data.name or "Puzzle" in Coup.data.name:
        print("Cube ............................")
        PUrP.CoupScale = v3c[0] / coupfaktor
    elif "Dovetail" in Coup.data.name or "Arrow" in Coup.data.name or "Hexagon" in Coup.data.name or "Pentagon" in Coup.data.name:
        print("Dove")
        PUrP.CoupScale = v3c[0]*2 / coupfaktor
    elif "T" in Coup.data.name:
        print("T")
        PUrP.CoupScale = v3c[0]/0.4 / coupfaktor
    else:
        print("fail")

    v0c = Coup.data.vertices[0].co  # @Coup.matrix_world
    OffsetRight = v0c[0] - 1.5*coupfaktor * PUrP.CoupScale

    v1c = Coup.data.vertices[1].co  # @Coup.matrix_world
    OffsetLeft = v1c[0] - 1.5*coupfaktor * PUrP.CoupScale

    # zscale and StopperHeight
    lowestvert = 0
    for vert in Coup.data.vertices:  # find lowest z coordinate
        vco = vert.co  # @Coup.matrix_world
        if vco[2] <= lowestvert:
            lowestvert = vco[2]

    lowestlist = []
    lowestexample = Coup.data.vertices[0]
    for vert in Coup.data.vertices:  # collect all verts with lowest co.z values
        vco = vert.co  # @Coup.matrix_world
        if vco[2] == lowestvert:
            lowestlist.append(vco[2])
            lowestexample = vert  # example for stopperheight evaluation

    lowestexampleco = lowestexample.co  # @Coup.matrix_world
    PUrP.StopperBool = False
    if len(lowestlist) == 4:  # with 4 verts its a stopper
        PUrP.StopperBool = True

    # for stopper height such den kürzesten abstand bei gleichen x
    # smallestdistance = 50
    distance = []

    for vert in Coup.data.vertices:
        vco = vert.co  # @Coup.matrix_world
        if vco[0] == lowestexampleco[0]:
            if vco[1] == lowestexampleco[1]:
                if vco[2] != lowestexampleco[2]:
                    # collect distances to vert
                    distance.append(
                        vco[2] - lowestexampleco[2])
                    # print(f"distance {vert.co.z - lowestexample.co.z}")
    distance.sort()
    StopperHeight = distance[0]

    # zscale top vert at co.z = 0
    if PUrP.StopperBool == True:
        zScale = -lowestexampleco[2] - distance[0]
    else:
        zScale = distance[0]

    return abs(OffsetRight), abs(OffsetLeft), zScale, StopperHeight


def zSym(obj):
    '''Test whether the obj is symmetrical relative to the object origin'''

    z = obj.data.vertices[0].co.z

    for v in obj.data.vertices:
        if v.co.z == -z:
            return True

    return False

    ###removes only the text fragement when its called order
def remove_order_tag(context, coup):
    if coup == None:
        return

    if context.object != None:
        activename = context.object.name

    deselectall(context)
    print('Welcome to order tag search of ' + coup.name)
    print(coup.children)
    for child in coup.children:
        print(child.name)
        if "Order" in child.name:
            print('found child ' + child.name)
            child.hide_select = False
            child.select_set(True)
            context.view_layer.objects.active = child
            bpy.ops.object.delete(use_global=False)
            
    if context.object != None:
        context.view_layer.objects.active = bpy.data.objects[activename] 

def removePUrPOrder():
    data = bpy.data
    # garbage run
    for ob in data.objects:
        ob.select_set(False)
        ob.hide_select = False
        if "PUrP" in ob.name:
            if "_Order" in ob.name:
                ob.select_set(True)
    bpy.ops.object.delete(use_global=False)


def copyobject(context, ob, newname):
    print(f"copy i make a copy of {ob} with the name {newname} ")
    ob_dat = ob.data.copy()
    newob = bpy.data.objects.new(name=newname, object_data=ob_dat)
    matrix = ob.matrix_world
    newob.parent = ob.parent
    col = in_collection(context, ob)
    if col == None:
        if context.collection != None:
            col = context.collection
        else:
            collection = bpy.data.collections.new(
                name="PUrPNeededThat")  # makes collection
            context.scene.collection.children.link(collection)
    col.objects.link(newob)

    for ob in context.selected_objects:
        ob.select_set(False)

    newob.select_set(True)
    context.view_layer.objects.active = newob
    newob.matrix_world = matrix
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    return newob


# changes name of object (planar and flat cut) and adjust name of related modifiers (the other aren't easily duplicateable)
def correctname(context, coup):
    data = bpy.data
    oriname = coup.name[:]
    if not "." in oriname:
        pass
    else:
        check = False
        while check == False:
            if "Single" in coup.name:
                newname = coup.name[:len(coup.name)-6] + \
                    str(random.randint(1, 999))
            elif "Planar" in coup.name:
                newname = coup.name[:len(coup.name)-12] + \
                    str(random.randint(1, 999)) + "_diff"
            # str(PUrP_name) + "SingleConnector_" + str(random.randint(1, 999))
            if newname not in data.objects:
                check = True

        coup.name = newname
        # when Cobj and Connector duplicated together, the bool mod is using the copied connector, change its name too
        for ob in data.objects:
            for mod in ob.modifiers:
                if "PUrP" in mod.name:
                    if mod.type == 'BOOLEAN':
                        if mod.object.name == newname:
                            mod.name = newname

        if is_unmapped(context, coup):
            if is_planar(context, coup) or is_single(context, coup):
                if coup.parent != None:
                    CObCo = coup.parent.location
                else:
                    CObCo = mathutils.Vector((0, 0, 0))

                CoupCo = coup.location
                Globalloc = CoupCo + CObCo
                # matrix_world = coup.matrix_world
                coup.parent = None
                remove_coupmods(context, coup)
                unmapped_signal(context, coup)
                # coup.matrix_world = matrix_world
                coup.location = Globalloc

    # return True


def set_BoolSolver(context, mod):
    PUrP = context.scene.PUrP
    if PUrP.ExactOptBool:
        if PUrP.BoolModSettings == '1':
            mod.solver = 'EXACT'
        elif PUrP.BoolModSettings == '2':
            mod.solver = 'FAST'

# doppelt


def remove_coupmods(context, coup):
    data = bpy.data
    print(f"remove coup mods of {coup.name} from all objects")
    for ob in data.objects:
        if not is_inlay(context, ob):
            for mod in ob.modifiers:
                if coup.name in mod.name:
                    print(
                        f"blub blub remove coup mod {mod.name} from {ob.name}")
                    ob.modifiers.remove(mod)


def is_coup(context, coup):
    if "PUrP" in coup.name:
        if is_single(context, coup) or is_planar(context, coup):

            return True
    return False


def is_planar(context, coup):
    return "Planar" in coup.name


def is_single(context, coup):
    if "Single" in coup.name:
        if not is_inlay(context, coup):
            # print(f"Coup positiv in Single {coup.name}")
            return True
    return False


def is_mf(context, coup):
    back = False
    for child in coup.children:
        if "union" in child.name:
            back = True
    return back


def is_stick(context, coup):
    back = False
    for child in coup.children:
        if "fix" in child.name:
            back = True
    return back


def is_flat(context, coup):
    if "Single" in coup.name:
        if len(coup.children) == 1 or len(coup.children) == 0:
            return True
    return False


def is_unmapped(context, coup):
    # check for unmapped signal
    if len(coup.children) != 0:
        for c in coup.children:
            if "Order" in c.name:
                if "UNMAPPED" in c.data.body:
                    return True

    elif coup.parent == None:
        return True
    elif coup.name not in coup.parent.modifiers:
        return True
    return False


def is_order(context, coup):
    if "Order" in coup.name:
        return True
    else:
        return False


def is_buildvolume(context, obj):
    return "BuildVolume" in obj.name


def is_inlay(context, coup):
    if "diff" in coup.name or "union" in coup.name or "fix" in coup.name:
        return True
    return False


def copy_obj(context, child, newname):
    matrix = child.matrix_world
    childtmpdata = child.data.copy()
    child_new = bpy.data.objects.new(
        name=newname, object_data=childtmpdata)

    col = in_collection(context, child)
    col.objects.link(child_new)
    child_new.parent = child.parent
    child_new.matrix_world = matrix
    child_new.display_type = 'WIRE'

    return child_new


def change_parent(context, obj, parent):
    # print(f"I change the parent of {obj.name} in {parent}")
    mw = obj.matrix_world
    # print(f"mw in Change Parent {mw}")
    obj.parent = parent
    obj.matrix_world = mw
    # print(f"obj mw after Parent change {obj.matrix_world}")


def cut_n_separate(context, coup, Cobj):
    context.view_layer.objects.active = Cobj
    bpy.ops.object.modifier_apply(modifier=coup.name)

    # seperate by loose parts
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.editmode_toggle()

    # remember objects
    CenterObjDaughters = context.selected_objects[:]
    if context.object not in CenterObjDaughters:
        CenterObjDaughters.append(context.object)

    return CenterObjDaughters


def remove_mod(context, ele, CObj, nameadd):
    data = bpy.data
    check = False
    if nameadd == "":   # coup and not an inlay
        coup = ele
        modname = coup.name
    else:
        coup = ele.parent
        modname = coup.name + "_" + nameadd
    if CObj != None:
        if modname in CObj.modifiers:
            CObj.modifiers.remove(CObj.modifiers[modname])
            return True


def ensure_allmods(context, coup, CObj):
    if is_planar(context, coup):
        ensure_mod(context, coup, CObj, '')
    elif is_single(context, coup):
        ensure_mod(context, coup, CObj, '')

        for child in coup.children:
            if coup.name + "_stick_fix" in child.name:
                fix = child
            elif coup.name + "_stick_diff" in child.name or coup.name + "_diff" in child.name:
                diff = child
            elif coup.name + "_union" in child.name:
                union = child

        if is_stick(context, coup):
            ensure_mod(context, fix, CObj, 'stick_diff')
        elif is_mf(context, coup):
            ensure_mod(context, diff, CObj, 'diff')
            ensure_mod(context, union, CObj, 'union')
        else:
            print("seems to be flat")


def ensure_mod(context, ele, CObj, nameadd):
    PUrP = context.scene.PUrP

    data = bpy.data
    check = False
    if nameadd == "":   # coup and not an inlay
        coup = ele
        modname = coup.name
    else:
        coup = ele.parent
        modname = coup.name + "_" + nameadd

    if modname in CObj.modifiers:
        print(f"{modname} found in {CObj.name}")
        return True

    print(f"{modname} not found in {CObj.name}, add modifier")

    mod = CObj.modifiers.new(
        type='BOOLEAN', name=modname)

    set_BoolSolver(context, mod)
    if "diff" in nameadd:
        mod.operation = "DIFFERENCE"
    elif "union" in nameadd:
        mod.operation = "UNION"
    elif "" == nameadd:
        mod.operation = "DIFFERENCE"

    mod.show_viewport = False

    if nameadd == '':
        mod.show_viewport = PUrP.ViewPortVisAdd

    mod.object = data.objects[modname]


def lowest_value(vectorlist, dim):
    initvector = vectorlist[1]
    lowest = initvector[dim]
    for v in vectorlist:
        if lowest > v[dim]:
            lowest = v[dim]
    return lowest


def highest_value(vectorlist, dim):
    initvector = vectorlist[1]
    highest = initvector[dim]
    for v in vectorlist:
        if highest < v[dim]:
            highest = v[dim]
    return highest


def origin_in_bb(context, union, CObj):
    tmp = copyobject(context, CObj, "tmp")

    bbox_corners = [tmp.matrix_world @
                    mathutils.Vector(corner) for corner in tmp.bound_box]

    xhighest = highest_value(bbox_corners, 0)
    xlowest = lowest_value(bbox_corners, 0)
    yhighest = highest_value(bbox_corners, 1)
    ylowest = lowest_value(bbox_corners, 1)
    zhighest = highest_value(bbox_corners, 2)
    zlowest = lowest_value(bbox_corners, 2)

    # print(f"xhighest {xhighest} yhighest {yhighest} zhighest {zhighest} xlowest {xlowest} ylowest {ylowest} zlowest {zlowest}")

    answer = False
    # union.location@union.matrix_world
    unionloc = mathutils.Vector(
        (union.matrix_world[0][3], union.matrix_world[1][3], union.matrix_world[2][3]))
    print(f"unionloc {unionloc}")
    if xhighest > unionloc[0]:
        # print("01")
        if xlowest < unionloc[0]:
            # print("02")
            if yhighest > unionloc[1]:
                # print("11")
                if ylowest < unionloc[1]:
                    # print("12")
                    if zhighest > unionloc[2]:
                        # print("21")
                        if zlowest < unionloc[2]:
                            # print("22")
                            answer = True

    bpy.data.objects.remove(tmp)
    print(f"origin in bb answer {answer} for {union.name} and {CObj.name}")
    return answer


def coupvisset(context, coup, hide):
    # if is_planar(context, coup):
    coup.hide_viewport = hide
    if is_single(context, coup):
        for child in coup.children:
            child.hide_viewport = hide

# takes obj list and returns list of coups


def selectedtocouplist(context, selected):
    couplist = []
    for obj in selected:
        if is_coup(context, obj):
            couplist.append(obj)
    return couplist
