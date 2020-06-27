

import bpy
import mathutils
from math import radians
from bpy.types import Scene, Image, Object
import random
import os
# from .intersect import bmesh_check_intersect_objects
from .bvh_overlap import bvhOverlap
from .warning import noCutthroughWarn, coneTrouble


# from .properties import PUrPropertyGroup

'''Operator in Blender'''


class PP_OT_AddSingleCoupling(bpy.types.Operator):
    bl_label = "Add Single Couplings"
    bl_idname = "add.coup"

    @classmethod
    def poll(cls, context):
        # PUrP = context.scene.PUrP
        if context.mode == 'OBJECT' and context.area.type == 'VIEW_3D':
            if (context.view_layer.objects.active != None):
                return True
            elif context.scene.PUrP.CenterObj != None:
                return True
        return False

    def execute(self, context):
        # createSingleCoupling()
        # def createSingleCoupling():
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
        # Prim = self.PrimTypes

        # handling CenterObj
        if active != None:

            if active.type == "MESH":
                if PUrP_name in active.name:
                    CenterObj = context.scene.PUrP.CenterObj
                else:
                    CenterObj = active
                    context.scene.PUrP.CenterObj = CenterObj
        else:
            active = context.scene.PUrP.CenterObj
            active.select_set(True)

        # apply scale to CenterObj
        bpy.ops.object.transform_apply(
            location=False, rotation=True, scale=True)
        CenterObj_name = CenterObj.name
        CenterObj.PUrPCobj = True
        Centerloc = CenterObj.location

        # make slice plane when not planar
        if PUrP.SingleCouplingModes != "4":
            bpy.ops.mesh.primitive_plane_add(
                size=6, enter_editmode=False, location=(0, 0, 0))
            context.object.name = str(
                PUrP_name) + "SingleConnector_" + str(random.randint(1, 999))
            newname_mainplane = context.object.name

            # bpy.ops.object.modifier_add(type='SOLIDIFY')
            mod = context.object.modifiers.new(
                name="PUrP_Solidify", type="SOLIDIFY")
            mod.thickness = CutThickness
            mod.offset = 1.0
            context.object.display_type = 'WIRE'
            # context.object.show_in_front = True

            context.object.parent = data.objects[CenterObj_name]

            # set boolean for the slice plane
            mod = data.objects[CenterObj_name].modifiers.new(
                name=context.object.name, type="BOOLEAN")
            mod.object = data.objects[newname_mainplane]
            mod.operation = 'DIFFERENCE'

        else:
            newname_mainplane = "Null"  # for planar

        # loc = mathutils.Vector((0,0,0))
        # print(f'CenterObj {CenterObj.name} vor Divisioncall. Active {active.name} ')
        coupModeDivision(CenterObj, newname_mainplane)

        # CenterObj.scale *= GlobalScale
        cursorloc.x -= CenterObj.location.x
        cursorloc.y -= CenterObj.location.y
        cursorloc.z -= CenterObj.location.z
        # context.scene.objects.link(unioncopy)

        if PUrP.SingleCouplingModes != "4":
            data.objects[newname_mainplane].location += cursorloc
            data.objects[newname_mainplane].select_set(True)
        elif PUrP.SingleCouplingModes == "4":
            context.object.location += cursorloc
            # context.object.select_set(True)

        context.scene.cursor.location = cursorlocori
        # for ob in context.selected_objects:
        #    ob.select_set(False)
        # context.object.select_set(True)

        # order refreshing
        data = bpy.data
        Orderbool = False
        for ob in data.objects:
            if "PUrP" in ob.name and "_Order" in ob.name:
                Orderbool = True
                bpy.ops.pup.couplingorder()
                bpy.ops.pup.couplingorder()
                break

        return{"FINISHED"}


def coupModeDivision(CenterObj, newname_mainplane):
    data = bpy.data
    context = bpy.context
    PUrP = bpy.context.scene.PUrP
    # Oversize = PUrP.Oversize
    # zScale = PUrP.zScale
    GlobalScale = PUrP.GlobalScale
    if PUrP.SingleCouplingModes == "3":                     # flatCut
        bpy.data.objects[newname_mainplane].scale = mathutils.Vector((1, 1, 1))
        newMain = data.objects[newname_mainplane]

    elif PUrP.SingleCouplingModes == "2":  # Male - female
        bpy.data.objects[newname_mainplane].scale = mathutils.Vector((1, 1, 1))
        # add negativ object
        # loc.z += 0.45
        ob0 = genPrimitive(CenterObj, newname_mainplane, '_diff')

        # add positiv object
        ob1 = genPrimitive(CenterObj, newname_mainplane, '_union')
        oversizeToPrim(ob0, ob1)
        newMain = data.objects[newname_mainplane]

    elif PUrP.SingleCouplingModes == "1":  # stick
        bpy.data.objects[newname_mainplane].scale = mathutils.Vector((1, 1, 1))
        ob0 = genPrimitive(CenterObj, newname_mainplane, '_stick_diff')

        ob1 = genPrimitive(CenterObj, newname_mainplane, '_stick_fix')

        oversizeToPrim(ob0, ob1)

        newMain = data.objects[newname_mainplane]

    elif PUrP.SingleCouplingModes == "4":
        newMain = genPlanar()
    # Adjustment for globalscale
    newMain.scale = mathutils.Vector((GlobalScale, GlobalScale, GlobalScale))

    for ob in context.selected_objects:
        ob.select_set(False)

    context.view_layer.objects.active = newMain
    newMain.select_set(True)


def oversizeToPrim(ob0, ob1):
    '''applies the oversize to the primitves ob0 is the bigger object (diff) ob1 the smaller'''
    PUrP = bpy.context.scene.PUrP
    Oversize = PUrP.Oversize
    zScale = PUrP.zScale
    size = PUrP.CoupSize

    ob0.scale = mathutils.Vector((size, size, size))
    ob1.scale = mathutils.Vector((size, size, size))

    # ob1.scale.z *= zScale
    ob0.scale.z *= zScale

    print(f"ob0 {ob0.name} dimensions z {ob0.dimensions.z}")

    oversizeDim = (ob0.scale.x - 2 * Oversize)
    if "fix" in ob0.name or "fix" in ob1.name:
        oversizeDimz = (ob0.scale.z - 2 * Oversize)  # mf
    else:
        oversizeDimz = (ob0.scale.z - Oversize)  # stick

    # should be ob1.dimensions but somehow don't work
    print(f"ob0 {ob0} ob1 {ob1} dimension z {ob0.dimensions.z} oversize {Oversize} gleichung{(ob0.dimensions.z - 2 * Oversize)}")

    # should be ob1.dimensions but somehow don't work
    print(f"ob0 {ob0} ob1 {ob1} dimension x {ob0.dimensions.x} oversize {Oversize} gleichung{(ob0.dimensions.x - 2 * Oversize)}")

    ob1.scale.x = oversizeDim
    print(f"dimensions x {ob1.scale.x}")
    ob1.scale.y = oversizeDim
    print(f"dimensions y {ob1.scale.y}")
    ob1.scale.z = oversizeDimz
    print(f"dimensions z {ob1.scale.z}")
    # ob1.scale.z *= zScale
    # ob0.scale.z *= zScale - oversizeDim


def genPrimitive(CenterObj, newname_mainplane, nameadd):
    context = bpy.context
    PUrP = bpy.context.scene.PUrP
    size = 1  # PUrP.CoupSize
    PrimTypes = context.scene.PUrP.SingleCouplingTypes
    CylVert = PUrP.CylVert
    aRadius = PUrP.aRadius
    bRadius = PUrP.bRadius
    data = bpy.data

    loc = mathutils.Vector((0, 0, 0))
    if PrimTypes == "1":
        bpy.ops.mesh.primitive_cube_add(size=size, location=loc)

    elif PrimTypes == "2":
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=CylVert, radius=aRadius, depth=1, enter_editmode=False, location=loc)

    elif PrimTypes == "3":
        bpy.ops.mesh.primitive_cone_add(
            vertices=CylVert, radius1=aRadius, radius2=bRadius, depth=2, enter_editmode=False, location=loc)
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
                    v.co.z += 0.5
                elif nameadd == "_union":
                    v.co.z += 0.5

        # Finish up, write the bmesh back to the mesh
        bm.to_mesh(me)
        bm.free()  # free and prevent further access

    # bevel for mode 2 - male-female
    obj = context.object
    # bevel weights need to enabled explizitly
    context.object.data.use_customdata_edge_bevel = True
    upverz = 0
    downverz = 0

    # bevelweights

    for vert in obj.data.vertices:
        if upverz < vert.co.z:
            upverz = vert.co.z
        if downverz > vert.co.z:
            downverz = vert.co.z
    if PUrP.SingleCouplingModes == "2":  # Male - female
        for edge in context.object.data.edges:
            if context.object.data.vertices[edge.vertices[0]].co.z == upverz and context.object.data.vertices[edge.vertices[1]].co.z == upverz:
                print(f"setting weight for edge {edge}")
                edge.bevel_weight = 1
    elif PUrP.SingleCouplingModes == "1":  # stick --> upper and lower edge bevelt
        for edge in context.object.data.edges:
            if context.object.data.vertices[edge.vertices[0]].co.z == upverz and context.object.data.vertices[edge.vertices[1]].co.z == upverz:
                print(f"setting weight for edge {edge}")
                edge.bevel_weight = 1
            if context.object.data.vertices[edge.vertices[0]].co.z == downverz and context.object.data.vertices[edge.vertices[1]].co.z == downverz:
                print(f"setting weight for edge {edge}")
                edge.bevel_weight = 1

    # apply oversize
    if nameadd == "_diff":
        context.object.scale.x += PUrP.Oversize
        context.object.scale.y += PUrP.Oversize
        context.object.scale.z += PUrP.Oversize

    # make name relative to the Couplingmainplain
    context.object.name = str(newname_mainplane) + str(nameadd)
    context.object.parent = bpy.data.objects[newname_mainplane]

    # print(f"zscale should affect obj {context.object.name}")
    # context.object.scale.z *= PUrP.zScale
    mod = context.object.modifiers.new(
        name=context.object.name + "Bevel", type="BEVEL")  # bevelOption to the Subcoupling
    mod.width = PUrP.BevelOffset
    mod.segments = PUrP.BevelSegments
    mod.limit_method = 'WEIGHT'
    context.object.display_type = 'WIRE'
    context.object.show_in_front = True
    context.object.hide_select = True

    if ("_diff" in bpy.context.object.name) or ("_union" in bpy.context.object.name):
        mod = CenterObj.modifiers.new(name=context.object.name, type="BOOLEAN")
        mod.object = context.object
        if nameadd == "_diff":
            mod.operation = 'DIFFERENCE'
        elif nameadd == '_union':
            mod.operation = 'UNION'
    else:
        pass

    return context.object


def genPlanar():
    context = bpy.context
    PUrP = bpy.context.scene.PUrP
    PUrP_name = PUrP.PUrP_name
    LineLength = PUrP.LineLength
    LineCount = PUrP.LineCount
    LineDistance = PUrP.LineDistance
    Oversize = PUrP.Oversize
    CenterObj = PUrP.CenterObj
    GlobalScale = PUrP.GlobalScale
    CoupSize = PUrP.CoupSize
    CutThickness = PUrP.CutThickness
    OffsetRight = PUrP.OffsetRight
    OffsetLeft = PUrP.OffsetLeft
    StopperHeight = PUrP.StopperHeight
    StopperBool = PUrP.StopperBool
    Oversize = PUrP.Oversize
    height = PUrP.zScale
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
    else:
        objectname = "Cubic"

    newname = str(PUrP_name) + "PlanarConnector_" + str(random.randint(1, 999))
    nameadd = "_diff"

    appendCoupling("planar.blend", objectname)
    print(
        f'nache append active {context.object.name}, CenterObj {CenterObj.name}')
    context.object.name = str(newname) + str(nameadd)

    print(f'active {context.object.name}, CenterObj {CenterObj.name}')

    context.object.parent = CenterObj
    context.object.display_type = 'WIRE'
    context.object.show_in_front = True

    # deselect all
    selected = context.selected_objects[:]
    for ob in selected:
        ob.select_set(False)

    obj = bpy.data.objects[context.object.name]
    # scale it a bit smaller than in the file
    adjustScale = 0.25
    obj.scale.x *= adjustScale
    obj.scale.y *= adjustScale

    '''# but then also have a global scale
    obj.scale *= GlobalScale

    # apply scale to get scale to one #####################################might need coupsize, too?
    obj.select_set(True)
    # bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    obj.scale *=  CoupSize
    print(f"obj {obj.name} coupSize {CoupSize} obj.scale {obj.scale} ")
    '''
    import bmesh
    # planar side offset
    me = bpy.context.object.data

    # Get a BMesh representation
    bm = bmesh.new()   # create an empty BMesh
    bm.from_mesh(me)   # fill it in from a Mesh

    bm.verts.ensure_lookup_table()
    # bm.edges.ensure_lookup_table()

    # prepare values for  offsets
    right = OffsetRight * GlobalScale
    left = OffsetLeft * GlobalScale

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

    # but then also have a global scale
    obj.scale *= GlobalScale

    # apply scale to get scale to one #####################################might need coupsize, too?
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    obj.scale *= CoupSize
    print(f"obj {obj.name} coupSize {CoupSize} obj.scale {obj.scale} ")

    # array 1 und 2
    mod = obj.modifiers.new(name="PUrP_Array_1", type="ARRAY")
    mod.use_merge_vertices = True
    mod.count = LineLength

    mod = obj.modifiers.new(name="PUrP_Array_2", type="ARRAY")

    mod.relative_offset_displace[0] = 0
    mod.relative_offset_displace[1] = LineDistance
    mod.count = LineCount
    mod.use_merge_vertices = True

    # Solidify
    mod = obj.modifiers.new(name="PUrP_Solidify", type="SOLIDIFY")

    mod.thickness = Oversize
    mod.offset = -1.0
    mod.solidify_mode = "NON_MANIFOLD"
    mod.nonmanifold_thickness_mode = 'FIXED'

    mod.use_even_offset = True
    mod.use_rim = True

    # boolean _diff at parent object
    mod = obj.parent.modifiers.new(name=obj.name, type="BOOLEAN")
    mod.operation = 'DIFFERENCE'
    mod.object = obj
    print(f"Active after planar generation {context.object}, obj is {obj}")

    return obj


def appendCoupling(filename, objectname):

    script_path = os.path.dirname(os.path.realpath(__file__))
    subpath = "blend" + os.sep + filename
    cp = os.path.join(script_path, subpath)

    # filepath = "//2.82\scripts\addons\purp\blend\new_library.blend"
    with bpy.data.libraries.load(cp) as (data_from, data_to):
        print('I am in')
        data_to.objects = [
            name for name in data_from.objects if name == objectname]

    for obj in data_to.objects:
        bpy.context.collection.objects.link(obj)
        obj.location = mathutils.Vector((0, 0, 0))
        bpy.context.view_layer.objects.active = obj


def newmainPlane(context, CenterObj):
    data = bpy.data
    PUrP = context.scene.PUrP
    PUrP_name = PUrP.PUrP_name
    CutThickness = PUrP.CutThickness

    bpy.ops.mesh.primitive_plane_add(
        size=6, enter_editmode=False, location=(0, 0, 0))
    context.object.name = str(
        PUrP_name) + "SingleConnector_" + str(random.randint(1, 999))
    newname_mainplane = context.object.name

    # bpy.ops.object.modifier_add(type='SOLIDIFY')
    mod = context.object.modifiers.new(
        name="PUrP_Solidify", type="SOLIDIFY")
    mod.thickness = CutThickness
    mod.offset = 1.0
    context.object.display_type = 'WIRE'
    # context.object.show_in_front = True

    context.object.parent = CenterObj

    # set boolean for the slice plane
    '''
    mod = data.objects[CenterObj.name].modifiers.new(
        name=context.object.name, type="BOOLEAN")
    mod.object = data.objects[newname_mainplane]
    mod.operation = 'DIFFERENCE'
    return newname_mainplane'''


class PP_OT_ExChangeCoup(bpy.types.Operator):
    '''Exchange selected couplings'''
    bl_idname = "object.exchangecoup"
    bl_label = "ExChangeCoupling"

    @classmethod
    def poll(cls, context):
        if (context.view_layer.objects.active != None) and context.mode == 'OBJECT':
            if ("SingleConnector" in context.view_layer.objects.active.name) or ("PlanarConnector" in context.view_layer.objects.active.name):
                return True
        else:
            return False

    def execute(self, context):

        context = bpy.context
        data = bpy.data
        CenterObj = context.scene.PUrP.CenterObj
        PUrP = bpy.context.scene.PUrP
        CutThickness = PUrP.CutThickness
        GlobalScale = PUrP.GlobalScale
        zScale = PUrP.zScale
        PUrP_name = PUrP.PUrP_name
        CouplingModes = bpy.context.scene.PUrP.SingleCouplingModes
        selected = context.selected_objects[:]

        for obj in selected:  # für die selektierten
            if PUrP_name in obj.name:  # eines meiner coupling

                for mod in obj.parent.modifiers:  # lösche alle modifier im centerobj
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

                    print(f"obj.data.name {obj.data.name}")
                    loc = obj.location.copy()
                    trans = obj.matrix_world.copy()
                    oldname = obj.name

                    for ob in context.selected_objects:  # deselte all
                        ob.select_set(False)
                    obj.select_set(True)
                    # delete the old planar coupling
                    bpy.ops.object.delete(use_global=False)

                    coupModeDivision(CenterObj, oldname)  # generate new planar
                    context.object.matrix_world = trans
                    # context.object.location = loc
                    #  ##planarversion
                else:  # when it was SingleCoupling, the mainplane is kept
                    if "Plane" not in obj.data.name:
                        print(f"2obj.data.name {obj.data.name}")
                        loc = obj.location.copy()
                        trans = obj.matrix_world.copy()
                        # oldname = obj.name
                        parentname = obj.parent.name[:]

                        for ob in context.selected_objects:  # deselte all
                            ob.select_set(False)
                        obj.select_set(True)
                        # delete the old planar coupling
                        bpy.ops.object.delete(use_global=False)
                        # name for
                        newname = newmainPlane(
                            context, data.objects[parentname])
                        obj = context.object

                    # obj.modifiers["PUrP_Solidify"].thickness = CutThickness

                    mod = CenterObj.modifiers.new(
                        name=obj.name, type="BOOLEAN")
                    mod.object = obj
                    mod.operation = 'DIFFERENCE'
                    # obj.scale = mathutils.Vector((1, 1, 1))
                    coupModeDivision(CenterObj, obj.name)
                    # print(f"obj at rescale {obj}")
                    obj.scale.x = GlobalScale
                    obj.scale.y = GlobalScale
                    obj.scale.z = GlobalScale

        Orderbool = False
        for ob in data.objects:
            if "PUrP" in ob.name and "_Order":
                Orderbool = True
                bpy.ops.pup.couplingorder()
                bpy.ops.pup.couplingorder()
                break

        return {'FINISHED'}


class PP_OT_ApplyCoupling(bpy.types.Operator):
    bl_label = "ApplyCouplings"
    bl_idname = "apl.coup"

    @classmethod
    def poll(cls, context):
        if (context.view_layer.objects.active != None) and context.mode == 'OBJECT':
            if context.mode == 'OBJECT' and context.area.type == 'VIEW_3D':
                if ("SingleConnector" in context.view_layer.objects.active.name) or ("PlanarConnector" in context.view_layer.objects.active.name):
                    return True
        else:
            return False

    def execute(self, context):
        #    applyCouplings()
        # def applyCouplings():
        context = bpy.context
        data = bpy.data
        selected = context.selected_objects[:]
        # CenterObj = context.scene.PUrP.CenterObj
        PUrP_name = bpy.context.scene.PUrP.PUrP_name

        # start conditions: seperators selected

        for obj in selected:
            if PUrP_name in obj.name:
                CenterObj = obj.parent
                applySingleCoup(context, obj, CenterObj)

        data = bpy.data
        Orderbool = False
        for ob in data.objects:
            if "PUrP" in ob.name and "_Order" in ob.name:
                Orderbool = True
                ob.select_set(True)
                # bpy.ops.pup.couplingorder()
                # bpy.ops.pup.couplingorder()
                break
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
                bpy.ops.object.modifier_apply(
                    apply_as='DATA', modifier=mod.name)

            elif str(connector.name) + '_diff' == mod.name:
                print(
                    f"I apply now modifier: {mod.name} to Object {daughter.name}")
                context.view_layer.objects.active = daughter
                print(f"active: {active}")
                bpy.ops.object.modifier_apply(
                    apply_as='DATA', modifier=mod.name)
            elif str(connector.name) + '_union' == mod.name:
                print(f'I delete now  {mod.name} from Object {daughter.name}')
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
                bpy.ops.object.modifier_apply(
                    apply_as='DATA', modifier=mod.name)

            elif str(connector.name) + '_union' == mod.name:
                context.view_layer.objects.active = daughter
                print(f"active: {active}")
                print(
                    f"I apply now modifier: {mod.name} to Object {daughter.name}")
                bpy.ops.object.modifier_apply(
                    apply_as='DATA', modifier=mod.name)
            elif str(connector.name) + '_diff' == mod.name:
                print(f'I delete now  {mod.name} from Object {daughter.name}')
                daughter.modifiers.remove(mod)
    else:
        print("Somethings Wrong with side determin")
    # if context.scene.PUrP.PUrP_name not in daughter.name:
    #    daughter.name = str(context.scene.PUrP.PUrP_name) + str(daughter.name)


def removeCoupling(Coupl):
    '''removes objects related to the coupling after apllying or when it is a fixed '''
    data = bpy.data
    context = bpy.context
    active = context.view_layer.objects.active
    Coupl_children = Coupl.children[:]
    for child in Coupl_children:
        if "fix" not in child.name:  # alle normalen couplings die applied sind
            child.hide_select = False

            for ob in context.selected_objects:
                ob.select_set(False)
            child.select_set(True)

            bpy.ops.object.delete(use_global=False)
        elif 'fix' in child.name:
            child.hide_select = False
            active = child
            for mod in child.modifiers:
                print(f"fix stick active {active} mod {mod.name}")
                bpy.ops.object.modifier_apply(
                    apply_as='DATA', modifier=mod.name)

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
        for mod in ob.modifiers:
            if Coupl.name in mod.name:
                ob.modifiers.remove(mod)
    Coupl.select_set(True)
    bpy.ops.object.delete(use_global=False)


'''
Daughtercollection = []

def CenterObjCollector():
    data = bpy.data
    global Daughtercollection
    list(set(Daughtercollection))
    PUrP = bpy.context.scene.PUrP
    PUrP_name = PUrP.PUrP_name

    # if len(Daughtercollection) == 0:
    test = False
    print (f"DaughterCollection content {Daughtercollection}")
    for Daughter in Daughtercollection:
        for mod in Daughter.modifiers:
            if (PUrP_name in mod.name) and ("diff" not in mod.name) and ("union" not in mod.name):
                if bmesh_check_intersect_objects(data.objects[mod.name], Daughter):
                    print(
                        f"intersect in Collector True for {mod.name} and {Daughter}")

                    test = True
                    continue

        if test:
            print(f"Test is for {Daughter}")
            applyCenterObj(Daughter)
        else:
            Daughtercollection.remove(Daughter)


    if len(Daughtercollection) != 0:
        CenterObjCollector()


def applyCenterObj(CenterObj):
    global Daughtercollection
    context = bpy.context
    data = bpy.data
    PUrP = context.scene.PUrP
    PUrP_name = PUrP.PUrP_name

    print('frisch in appyl centerObj {CenterObj}')

    # n = 0
    # test = True
    modifiers = CenterObj.modifiers[:]

    for mod in modifiers:
    # while test == True:
        print(f'nächste Runde für mod {mod.name} in CenterObj {CenterObj}')
        # if (len(CenterObj.modifiers) != 0) and (len(CenterObj.modifiers)-1 >= n):
        if (PUrP_name in mod.name) and ("diff" not in mod.name) and ("union" not in mod.name):
            print('nächste Runde')
            # try:
            # if PUrP_name in CenterObj.modifiers[n].name:
            # mod_name = CenterObj.modifiers[n].name
            if bmesh_check_intersect_objects(data.objects[mod.name], CenterObj):
                print("Intersection test is positiv")
                Daughters = applySingleCoup(
                    context, data.objects[mod.name], CenterObj)
                print(f"Daughters send to collection {Daughters}")
                Daughtercollection.append(Daughters)

 '''


def centerObjDecider(context, CenterObj):
    PUrP = context.scene.PUrP
    PUrP_name = PUrP.PUrP_name
    Objects = bpy.data.objects

    CenterMods = CenterObj.modifiers[:]
    ModList = []
    for PriMod in CenterMods:  # look through the modifers of the centerObj and make a list of the Couplings that need to be applied
        if ("PUrP_" in PriMod.name) and ("diff" not in PriMod.name) and ("union" not in PriMod.name):
            primodname = PriMod.name[:]
            print(f"primodname {primodname}")
            ModList.append(primodname)
        elif "PUrP_Planar" in PriMod.name:
            primodname = PriMod.name[:]
            print(f"primodname {primodname}")
            ModList.append(primodname)
    # name, ModList = couplingList(CenterObj)

    for mod in ModList:
        print(f"centerObjdecider mod name {mod}")
        if PUrP_name in mod:
            if "PUrP_Planar" in mod or ("diff" not in mod) and ("union" not in mod):

                # potential Cobj list (checking the Object bool),otherwise when I loo through all objects and delete objects during the round, the Objects change adress
                Cobjlist = []
                for pCobj in Objects:
                    if pCobj.PUrPCobj == True:
                        Cobjlist.append(pCobj)

                for Cobj in Cobjlist:
                    print(f"centerObjdecider Cobj {Cobj}")

                    # now collect all the modifiers that belong to a single coupling (not diff and union), and nothing from user
                    Cobjmodslist = []
                    for ele in Cobj.modifiers:
                        if ("PUrP_" in ele.name) and ("diff" not in ele.name) and ("union" not in ele.name):
                            Cobjmodslist.append(ele)
                        elif "PUrP_Planar" in ele.name:
                            print("decider Planar to list")
                            Cobjmodslist.append(ele)

                    for Cmod in Cobjmodslist:  # look through addon own modifier liste and
                        print(f"centerObjdecider Cmod name {Cmod.name}")
                        if Cmod.name == mod:

                            if bvhOverlap(context, Objects[mod], Cobj):
                                print(
                                    f"centerObjdecider send applySingleCoup mod.name {mod} and CObj {Cobj}")
                                applySingleCoup(context, Objects[mod], Cobj)
                            else:
                                print(
                                    f"centerObjdecider remove now mod {mod} of Cobj {Cobj}")
                                # mid = Cobj.modifiers[mod]
                                # Cobj.modifiers.remove(mid)


def applySingleCoup(context, Coup, CenterObj):
    # context = bpy.context
    data = bpy.data
    PUrP_name = bpy.context.scene.PUrP.PUrP_name

    obj = Coup

    for sel in context.selected_objects:
        sel.select_set(False)

    # remeber which couplings are parented to (alternative via modifiers)
    oriCoupNames, oriCoupMods = couplingList(CenterObj)

    # apply boolean to seperate Centralobj parts
    context.view_layer.objects.active = CenterObj
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier=obj.name)

    # seperate by loose parts

    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.editmode_toggle()

    # remember both objects
    CenterObjDaughters = context.selected_objects[:]
    print(f'CenterObjDaugters are {CenterObjDaughters}')
    DaughterOne = context.active_object
    DaughterTwo = None
    for ob in CenterObjDaughters:  # setze das ob für zweite Tochter
        if ob != DaughterOne:
            DaughterTwo = ob

    # teste on which side a vertex of one object lays
    context.view_layer.objects.active = obj
    # apply rotation centerplane obj damit die vector rechnung funktioniert
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

    CouplingNormal = obj.data.vertices[0].normal
    ctl = False
    n = 0
    Daughtertwo_side = "NULL"
    while ctl == False:

        # geo = mathutils.geometry.distance_point_to_plane(pt, plane_co, plane_no)
        geo = mathutils.geometry

        direction = CouplingNormal.dot(
            DaughterOne.data.vertices[n].co) - CouplingNormal.dot(obj.data.vertices[0].co)
        print(f"that's the direction value {direction}")
        if direction == 0:  # actual vector geometry part
            n += 1
            print("vertice number" + str(n))

        elif direction < 0:

            ctl = True
            print('Object auf der Positiven Seite')
            DaughterOne_side = "POSITIV"
            DaughterTwo_side = "NEGATIV"
            applyRemoveCouplMods(DaughterOne, obj, DaughterOne_side)
        elif direction > 0:
            ctl = True
            print('negativ seite')
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
    for coupname in oriCoupNames:
        coup = objects[coupname]
        if bvhOverlap(context, coup, DaughterOne):
            coup.parent = DaughterOne
            DOneCoupList.append(coup)

        elif bvhOverlap(context, coup, DaughterTwo):
            coup.parent = DaughterTwo
            DTwoCoupList.append(coup)
        else:
            print(f"coup {coup.name} was false with both daughters")

    DOneAllMods = AllCoupMods(context, DOneCoupList, DaughterOne)
    DTwoAllMods = AllCoupMods(context, DTwoCoupList, DaughterTwo)

    print(f"DoneAllMods {DOneAllMods}")
    print(f"DoneAllMods {DTwoAllMods}")

    for mod in DaughterOne.modifiers:

        if mod not in DOneAllMods:
            DaughterOne.modifiers.remove(mod)

    for mod in DaughterTwo.modifiers:
        if mod not in DTwoAllMods:
            DaughterTwo.modifiers.remove(mod)

    context.view_layer.objects.active = obj
    removeCoupling(obj)
    Daughters = (DaughterOne, DaughterTwo)
    return Daughters

    # SingleConnectorNormal = objects.data.meshes['Cube.013'].vertices[1].normal


class PP_OT_ApplyAllCouplings(bpy.types.Operator):
    '''Applies all Couplings. If nothing is selected it applies the Couplings to all modified objects. If an Centerobject is selected, it only applies the all Coupling for this Object. If a Coupling is selected, all Couplings connectected to the same Centerobject will be applied'''
    bl_idname = "apl.allcoup"
    bl_label = "PP_OT_ApplyAllCouplings"

    @classmethod
    def poll(cls, context):

        if (context.view_layer.objects.active != None):
            if context.mode == 'OBJECT' and context.area.type == 'VIEW_3D':
                if ("SingleConnector" in context.view_layer.objects.active.name) or ("PlanarConnector" in context.view_layer.objects.active.name):
                    return True

        else:
            return False

    def execute(self, context):
        PUrP = context.scene.PUrP
        PUrP_name = PUrP.PUrP_name
        data = bpy.data
        global Daughtercollection

        # wenn nichts selected, gehe durch alle objecte und schaue ob die bearbeitet wurden (müssen Couplings haben)
        if context.selected_objects == None:
            print('Its None und nicht "None"')
            for obj in data.objects:
                for child in obj.child:  # gibt es kinder Coupling in diesem Object
                    if PUrP_name in child:
                        CenterBool = True
                        pass
                if CenterBool:
                    # Daughtercollection = []
                    # Daughtercollection.append(obj)
                    centerObjDecider(context, obj)

                    # CenterObjCollector()

        elif context.selected_objects != None:

            selected = context.selected_objects[:]
            for obj in selected:
                CenterBool = False
                # wenn couplin type selected , finde Papa und sende es
                if PUrP_name in obj.name:
                    print("I am a selected Connector such meinen Papa")
                    # applyCenterObj(obj.parent)
                    # Daughtercollection = []
                    # Daughtercollection.append(obj.parent)
                    # CenterObjCollector()
                    centerObjDecider(context, obj.parent)
                else:
                    for child in obj.child:  # gibt es kinder Coupling in diesem Object
                        if PUrP_name in child:
                            CenterBool = True
                            pass
                if CenterBool:
                    # Daughtercollection = []
                    # Daughtercollection.append(obj)
                    # CenterObjCollector()
                    centerObjDecider(context, obj)
                    # applyCenterObj(obj)

        # wenn coupling selected, apply für alle

        return {'FINISHED'}


class PP_OT_DeleteCoupling(bpy.types.Operator):
    bl_label = "DeleteCouplings"
    bl_idname = "rem.coup"

    @classmethod
    def poll(cls, context):

        if (context.view_layer.objects.active != None):
            if context.mode == 'OBJECT' and context.area.type == 'VIEW_3D':
                if ("SingleConnector" in context.view_layer.objects.active.name) or ("PlanarConnector" in context.view_layer.objects.active.name):
                    return True
        else:
            return False

    def execute(self, context):

        active = context.view_layer.objects.active
        objects = bpy.data.objects
        selected = context.selected_objects[:]

        for obj in selected:
            if ("SingleConnector" in obj.name) or ("PlanarConnector" in obj.name):
                # clean selection array
                for ob in context.selected_objects:
                    ob.select_set(False)

                    # name_active = obj.name
                for child in obj.children:
                    child.hide_select = False
                    child.select_set(True)
                    bpy.ops.object.delete(use_global=False)

                # entferne modifier und zwar immer auch wenn es schon zerlegt ist
                for mod in obj.parent.modifiers:
                    # !!!!!!!!!!Das wird ein BUG     weil auch die ohne nummer gelöscht werden siehe lange zeile unten
                    if (str(obj.name) + '_diff' == mod.name) or (str(obj.name) + '_union' == mod.name) or (str(obj.name) + '_stick_fix' == mod.name) or (str(obj.name) + '_stick_diff' == mod.name) or (str(obj.name) == mod.name):
                        print(f'I delete modifier {mod.name}')
                        obj.parent.modifiers.remove(mod)

                obj.select_set(True)
                print(f'selected objects{context.selected_objects}')
                bpy.ops.object.delete(use_global=False)

            context.view_layer.objects.active = context.scene.PUrP.CenterObj
            # order part
            data = bpy.data
            Orderbool = False
            for ob in data.objects:
                if "PUrP" in ob.name and "_Order":
                    Orderbool = True
                    bpy.ops.pup.couplingorder()
                    bpy.ops.pup.couplingorder()
                    break

        return{"FINISHED"}


def moveModdown(Coup, CenterObj):
    CoupModcount = howManyModsCoup(Coup.name, CenterObj)

    # list of coupling names connected to the centerobj
    PUrP_Modsnames = listPUrPMods(CenterObj)
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


# takes a coupling name and the CenterObj and returns how modifiers beelong to the coupling
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
        AllMods.extend(allmodsOcoup)
    return AllMods


def listPUrPMods(CenterObj):  # returns list of mod names
    namelist = []
    for mod in CenterObj.modifiers:
        if ("PUrP" in mod.name):
            if ("diff" not in mod.name) and ("union" not in mod.name):
                namelist.append(mod.name)
            elif ("Planar" in mod.name):
                namelist.append(mod.name)
    return namelist


def couplingList(CenterObj):

    name = []
    mods = []
    for mod in CenterObj.modifiers:
        if "PUrP" in mod.name:
            if "diff" not in mod.name and "union" not in mod.name:
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
    bl_idname = "pup.moddown"
    bl_label = "PP_OT_MoveModDown"

    @classmethod
    def poll(cls, context):

        if (context.view_layer.objects.active != None):
            if context.mode == 'OBJECT' and context.area.type == 'VIEW_3D':
                if ("SingleConnector" in context.view_layer.objects.active.name) or ("PlanarConnector" in context.view_layer.objects.active.name):
                    return True
        else:
            return False

    def execute(self, context):

        Coup = bpy.data.objects[context.object.name]
        CenterObj = Coup.parent

        moveModdown(Coup, CenterObj)

        data = bpy.data
        Orderbool = False
        for ob in data.objects:
            if "PUrP" in ob.name and "_Order":
                Orderbool = True
                bpy.ops.pup.couplingorder()
                bpy.ops.pup.couplingorder()
                break

        return {'FINISHED'}


class PP_OT_MoveModUp(bpy.types.Operator):
    bl_idname = "pup.modup"
    bl_label = "PP_OT_MoveModup"

    @classmethod
    def poll(cls, context):

        if (context.view_layer.objects.active != None):
            if context.mode == 'OBJECT' and context.area.type == 'VIEW_3D':
                if ("SingleConnector" in context.view_layer.objects.active.name) or ("PlanarConnector" in context.view_layer.objects.active.name):
                    return True
        else:
            return False

    def execute(self, context):
        Coup = bpy.data.objects[context.object.name]
        CenterObj = Coup.parent
        PUrP_Modsnames = listPUrPMods(CenterObj)
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

        data = bpy.data
        Orderbool = False
        for ob in data.objects:
            if "PUrP" in ob.name and "_Order":
                Orderbool = True
                bpy.ops.pup.couplingorder()
                bpy.ops.pup.couplingorder()
                break

        for ob in data.objects:
            ob.select_set(False)

        context.view_layer.objects.active = data.objects[initialActivename]
        context.view_layer.objects.active.select_set(True)
        return {'FINISHED'}


class PP_OT_Ini(bpy.types.Operator):

    bl_label = "Initialize PuzzleUrPrint"
    bl_idname = "pup.init"

    @classmethod
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
        #########
        MColName = "PuzzleUrPrint"

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
        # PUrP.SingleCouplingtypes = ('Cube', 'Cylinder', 'Cone')
        # CylVert

        return{"FINISHED"}


class PP_OT_ToggleCoupVisibilityOperator(bpy.types.Operator):
    bl_idname = "object.togglecoupvisibility"
    bl_label = "PP_OT_ToggleCoupVisibility"

    @classmethod
    def poll(cls, context):

        if (context.view_layer.objects.active != None):
            if context.mode == 'OBJECT' and context.area.type == 'VIEW_3D':
                if ("SingleConnector" in context.view_layer.objects.active.name) or ("PlanarConnector" in context.view_layer.objects.active.name):
                    return True
        else:
            return False

    def execute(self, context):

        for ele in context.selected_objects:
            if "PUrP" in ele.name:  # for selected coupling of PUrP
                CenterObj = ele.parent
                for mod in CenterObj.modifiers:
                    if ele.name in mod.name:
                        if CenterObj.modifiers[mod.name].show_viewport == True:
                            CenterObj.modifiers[mod.name].show_viewport = False
                        elif CenterObj.modifiers[mod.name].show_viewport == False:
                            CenterObj.modifiers[mod.name].show_viewport = True
                        else:
                            print('Something Wrong in Visibility Toggle')
        return {'FINISHED'}


class PP_OT_ActiveCoupDefaultOperator(bpy.types.Operator):
    '''Use the settings of the active coupling as Default values. Helps to transfer settings from Connector to Connector or duplicate a Connector.'''

    bl_idname = "object.activecoupdefault"
    bl_label = "PP_OT_ActiveCoupDefault"

    @classmethod
    def poll(cls, context):
        if (context.view_layer.objects.active != None):
            if context.mode == 'OBJECT' and context.area.type == 'VIEW_3D':
                if ("SingleConnector" in context.view_layer.objects.active.name) or ("PlanarConnector" in context.view_layer.objects.active.name):
                    return True
        else:
            return False

    def execute(self, context):
        PUrP = context.scene.PUrP
        obj = context.object

        if "SingleConnector" in obj.name:
            PUrP.CutThickness = obj.modifiers['PUrP_Solidify'].thickness

            if len(obj.children) == 0:
                PUrP.SingleCouplingModes = "3"
            elif zSym(obj.children[0]):
                PUrP.SingleCouplingModes = "1"
            else:
                PUrP.SingleCouplingModes = "2"

            if len(obj.children) != 0:
                # print(f"meshadata name {obj.data.name}")
                if "Cube" in obj.children[0].data.name:
                    PUrP.SingleCouplingTypes = '1'
                elif "Cylinder" in obj.children[0].data.name:
                    PUrP.SingleCouplingTypes = '2'
                    # PUrP.CylVert = len(obj.data.vertices)/2
                    PUrP.CylVert, PUrP.aRadius, PUrP.bRadius = self.coneanalysizer(  # cylinder is a special case of cone
                        context, obj.children[0])
                elif "Cone" in obj.children[0].data.name:
                    PUrP.SingleCouplingTypes = '3'
                    # PUrP.CylVert = len(obj.data.vertices) - 1
                    PUrP.CylVert, PUrP.aRadius, PUrP.bRadius = self.coneanalysizer(
                        context, obj.children[0])
                for child in obj.children:
                    if "diff" in child.name:
                        PUrP.CoupSize = child.scale.x
                        PUrP.zScale = child.scale.z
                        # double check
                        PUrP.BevelSegments = child.modifiers[0].segments
                        PUrP.BevelOffset = child.modifiers[0].width
                        diffchild = child
                    elif "fix" in child.name or "union" in child.name:
                        PUrP.Oversize = (diffchild.scale.x -
                                         child.scale.x)/2  # double check

                '''('1','Stick',''),
                    ('2','Male-Female', ''),
                #    ('3','FlatCut',''),
                #    ('4','Planar',''),'''

        elif "PlanarConnector" in obj.name:
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

            PUrP.CoupSize = obj.scale.x
            # Apply scale e.g. zscale determination
            bpy.ops.object.transform_apply(
                location=False, rotation=False, scale=True)

            PUrP.Oversize = obj.modifiers["PUrP_Solidify"].thickness
            PUrP.LineDistance = obj.modifiers["PUrP_Array_2"].relative_offset_displace[1]
            PUrP.LineCount = obj.modifiers["PUrP_Array_2"].count
            PUrP.LineLength = obj.modifiers["PUrP_Array_1"].count
            # double checl
            PUrP.OffsetRight = obj.data.vertices[0].co.x*4 - 1.5
            PUrP.OffsetLeft = - obj.data.vertices[1].co.x*4 - 1.5

            #

            # Stopperbool test
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

            PUrP.StopperBool = False
            if len(lowestlist) == 4:  # with 4 verts its a stopper
                PUrP.StopperBool = True

            # for stopper height such den kürzesten abstand bei gleichen x
            smallestdistance = 50
            distance = []
            for vert in obj.data.vertices:
                if vert.co.x == lowestexample.co.x:
                    if vert.co.y == lowestexample.co.y:
                        if vert.co.z != lowestexample.co.z:
                            # collect distances to vert
                            distance.append(vert.co.z - lowestexample.co.z)
                            print(f"distance {vert.co.z - lowestexample.co.z}")
            distance.sort()
            PUrP.StopperHeight = distance[0]

            # zscale top vert at co.z = 0
            if PUrP.StopperBool == True:
                PUrP.zScale = -lowestexample.co.z - distance[0]
            else:
                PUrP.zScale = distance[0]

        return {'FINISHED'}

    def coneanalysizer(self, context, obj):
        # Cyclvert, and the radius are extrakted; Coupling types

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
            for v in upperverts:
                # vert on an axis has the radius as co.axis
                if v.co.x == 0:
                    bRadius = v.co.y
                    break
                if v.co.y == 0:
                    bRadius = v.co.x
                    break
        # lower radius
        Cyclvert = len(upperverts)
        for v in lowerverts:
            if v.co.x == 0:
                aRadius = v.co.y
                break
            if v.co.y == 0:
                aRadius = v.co.x
                break

        return Cyclvert, aRadius, bRadius


def zSym(obj):
    '''Test whether the obj is symmetrical relative to the object origin'''

    z = obj.data.vertices[0].co.z

    for v in obj.data.vertices:
        if v.co.z == -z:
            return True

    return False


class PP_OT_CouplingOrder(bpy.types.Operator):
    bl_idname = "pup.couplingorder"
    bl_label = "PP_OT_CouplingOrder"

    @classmethod
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

        data = bpy.data
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
        Orderbool = True
        for ob in data.objects:
            if "PUrP" in ob.name and "_Order" in ob.name:  # gibt es objecte mit order -- > dann lösche nur
                Orderbool = False

                # bpy.ops.pup.couplingorder()
                # bpy.ops.pup.couplingorder()
                break

        if Orderbool:

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
        else:
            removePUrPOrder()
        context.view_layer.objects.active = data.objects[initialActivename]
        context.view_layer.objects.active.select_set(True)
        return {'FINISHED'}


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


class PP_OT_ReMapCoupsOperator(bpy.types.Operator):
    '''Remap selected couplings to active centerobject'''
    bl_idname = "object.remapcoups"
    bl_label = "PP_OT_ReMapCoups"

    def execute(self, context):
        print("remap")
        selected = context.selected_objects[:]
        active = context.object
        CenterObj = active
        if "SingleConnector" in active.name or "Planar" in active.name:
            print("finish remap")
            return {'FINISHED'}
        elif not CenterObj.PUrPCobj:
            self.report({'WARNING'}, 'Active was never a Centerobject before')

        PUrP = context.scene.PUrP

        CenterObj.PUrPCobj = True

        # reparent

        for coup in selected:
            if coup != CenterObj:
                print(f"coup {coup.name}")
                Couplist = []
                Couplist.append(coup)  # only the one in the list in this case
                print(f"parent {coup.parent}")
                AllCoupmods = AllCoupMods(context, Couplist, coup.parent)
                print(f"a allcoupsmods remap {AllCoupmods}")
                for mod in AllCoupmods:

                    # make new in CenterObj
                    newmod = CenterObj.modifiers.new(mod.name, mod.type)
                    newmod.operation = mod.operation
                    newmod.object = mod.object

                    # remove in parent

                    coup.parent.modifiers.remove(mod)

                coup.parent = CenterObj

        PUrP.CenterObj = CenterObj
        return {'FINISHED'}
