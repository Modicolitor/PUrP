import bpy
import bmesh


import bmesh


def gen_figure(context, loc):

    bpy.ops.mesh.primitive_plane_add(
        size=2, enter_editmode=False, align='WORLD', location=loc, scale=(1, 1, 1))

    ob = context.object
    mod = ob.modifiers.new(name="PUrP_Mirror", type="MIRROR")

    # planar side offset
    me = context.object.data

    # Get a BMesh representation
    bm = bmesh.new()   # create an empty BMesh
    bm.from_mesh(me)   # fill it in from a Mesh

    bm.verts.ensure_lookup_table()
    # bm.edges.ensure_lookup_table()
    for vert in bm.verts:
        vert.co = (1, 0, 0)

    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)
    # ==> one vert left
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
    return context.object
