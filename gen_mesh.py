#
# Copyright (C) 2020 by Modicolitor
#
# This file is part of PuzzleUrPrint.
#
# License Text
#
# You should have received a copy of the GNU General Public License along with PuzzleUrPrint. If
# not, see <https://www.gnu.org/licenses/>.

import bpy
import bmesh


import bmesh
from mathutils import Vector


def bm_extruder(type, vector,  bm, verts, edges):
    if type == 'Vert':
        geo = bmesh.ops.extrude_vert_indiv(bm, verts=verts)

        verts = geo['verts']  # for vert in geo]  # ['verts']
        edges = geo['edges']  # [edge for edge in geo]  # edges

        print('####################')
        print(edges)
        print('####################')
        print(verts)

        bmesh.ops.translate(bm, vec=vector, verts=verts)

        return bm, verts, edges
    elif type == 'Edge':
        ret = bmesh.ops.extrude_edge_only(
            bm,
            edges=edges)

        geom = ret['geom']

        verts = [ele for ele in geom
                 if isinstance(ele, bmesh.types.BMVert)]
        print(f"wieviele vert {len(verts)}")
        edges = [ele for ele in geom
                 if isinstance(ele, bmesh.types.BMEdge)]  # and ele.is_boundary]
        print(f"wieviele edges {len(edges)}")

        bmesh.ops.translate(bm, vec=vector, verts=verts)

        return bm, verts, edges, geom
    else:
        print('wrong type')
        # return bm, verts, edges


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
        vert.co = (0.5, -0.5, 0)

    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)

    bm, verts, edges = bm_extruder(
        'Vert', (0, 0.5, 0),  bm, bm.verts, bm.edges)  # Fuß
    bm, verts, edges = bm_extruder('Vert', (-0.15, -0.1, 1),  bm, verts, edges)
    bm, verts, edges = bm_extruder('Vert', (-0.15, 0.1, 1),  bm, verts, edges)
    bm, verts, edges = bm_extruder('Vert', (-0.2, 0.0, 0),  bm, verts, edges)
    # bm, verts, edges = bm_extruder('Vert', (0.0, 0.0, 1s),  bm, verts, edges)
    bm, vertsneck, edges = bm_extruder('Vert', (0, 0, 1),  bm, verts, edges)
    bm, vertsshoulder, edges = bm_extruder(
        'Vert', (0.5, 0, -0.1),  bm, vertsneck, edges)
    bm, vertsuparm, edges = bm_extruder(
        'Vert', (0.2, 0, -0.7),  bm, vertsshoulder, edges)
    bm, vertlowarm, edges = bm_extruder(
        'Vert', (0.2, -0.3, -0.6),  bm, vertsuparm, edges)

    bm, vertsneckup, edges = bm_extruder(
        'Vert', (0.0, 0, 0.1),  bm, vertsneck, edges)
    bm, vertsheaddown, edges = bm_extruder(
        'Vert', (0.0, 0, 0.2),  bm, vertsneckup, edges)
    bm, vertsheadup, edges = bm_extruder(
        'Vert', (0.0, 0, 0.1),  bm, vertsheaddown, edges)
    bm, vertsheadup, edges = bm_extruder(
        'Vert', (0.0, 0, 0.2),  bm, vertsheadup, edges)
    bm, vertsheadup, edges = bm_extruder(
        'Vert', (0.0, 0, 0.2),  bm, vertsheadup, edges)

    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)

    # delete back half because I don't know to extrude a single verts:-(
    # for vert in bm.verts:
    #    backhalf_verts if vert.co[1] > 0]s
    # Finish up, write the bmesh back to the mesh
    bm.verts.ensure_lookup_table()
    bm.verts[8].select_set(True)
    bm.to_mesh(me)
    bm.free()  # free

    mod = ob.modifiers.new(name="PUrP_Skin", type="SKIN")
    mod = ob.modifiers.new(name="PUrP_Sub", type="SUBSURF")
    mod.levels = 3
    # beispiel code from internet change skin vert data

    # obj = bpy.data.objects['Plane']
    # for v in obj.data.skin_vertices[0].data:
    #    v.radius = 0.2, 1.2

    obj = context.object
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    obj.data.vertices[1].select = True
    obj.data.vertices[6].select = True
    obj.data.vertices[7].select = True
    obj.data.vertices[8].select = True
    obj.data.vertices[9].select = True
    obj.data.vertices[10].select = True
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.transform.skin_resize(value=(0.6, 0.6, 0.6), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True,
                                  use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    obj.data.vertices[3].select = True
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.object.skin_root_mark()
    bpy.ops.object.mode_set(mode='OBJECT')
    # #bpy.data.meshes['Plane'].skin_vertices[""].data

    bpy.ops.object.modifier_apply(modifier='PUrP_Mirror')
    bpy.ops.object.modifier_apply(modifier='PUrP_Skin')
    bpy.ops.object.modifier_apply(modifier='PUrP_Sub')
    bpy.ops.object.shade_smooth()

    return context.object


def gen_hat(context, loc):

    bpy.ops.mesh.primitive_circle_add(
        radius=0.1, fill_type='NGON', enter_editmode=False, align='WORLD', location=loc, scale=(1, 1, 1))
    ob = context.object
    # mod = ob.modifiers.new(name="PUrP_Mirror", type="MIRROR")

    # planar side offset
    me = context.object.data

    # Get a BMesh representation
    bm = bmesh.new()   # create an empty BMesh
    bm.from_mesh(me)   # fill it in from a Mesh

    bm.verts.ensure_lookup_table()
    bm, verts, edges, geom = bm_extruder(
        'Edge', (0, 0, 0.0),  bm, bm.verts, bm.edges)
    bmesh.ops.scale(bm, vec=(8, 8, 1), space=ob.matrix_local, verts=verts)
    bm, verts, edges, geom = bm_extruder(
        'Edge', (0, 0, 0.0),  bm, verts, edges)
    bmesh.ops.scale(bm, vec=(1.1, 1.1, 1), space=ob.matrix_local, verts=verts)
    bm, verts, edges, geom = bm_extruder(
        'Edge', (0, 0, 0.5),  bm, verts, edges)
    bmesh.ops.scale(bm, vec=(1.1, 1.1, 1), space=ob.matrix_local, verts=verts)
    bm, verts, edges, geom = bm_extruder(
        'Edge', (0, 0, 0),  bm, verts, edges)
    bmesh.ops.scale(bm, vec=(0.9, 0.9, 1), space=ob.matrix_local, verts=verts)
    bm, verts, edges, geom = bm_extruder(
        'Edge', (0, 0, -0.3),  bm, verts, edges)

    bmesh.ops.scale(bm, vec=(0.8, 0.8, 1), space=ob.matrix_local, verts=verts)

    bm, verts, edges, geom = bm_extruder(
        'Edge', (0, 0, 0),  bm, verts, edges)
    bmesh.ops.scale(bm, vec=(0.8, 0.8, 1), space=ob.matrix_local, verts=verts)

    bm, verts, edges, geom = bm_extruder(
        'Edge', (0, 0, 0),  bm, verts, edges)
    bmesh.ops.scale(bm, vec=(0.8, 0.8, 1), space=ob.matrix_local, verts=verts)

    bm, verts, edges, geom = bm_extruder(
        'Edge', (0, 0, 0.5),  bm, verts, edges)
    bm, verts, edges, geom = bm_extruder(
        'Edge', (0.0, 0.0, 0.0),  bm, verts, edges)
    bmesh.ops.scale(bm, vec=(0.5, 0.5, 1.2),
                    space=ob.matrix_local, verts=verts)
    bm, verts, edges, geom = bm_extruder(
        'Edge', (0.0, 0.0, 0.02),  bm, verts, edges)
    bmesh.ops.scale(bm, vec=(0.3, 0.3, 1.05),
                    space=ob.matrix_local, verts=verts)

    # faces = bmesh.ops.grid_fill(bm, edges=edges, mat_nr=0,
    #                            use_smooth=False, use_interp_simple=True)
    bmesh.ops.edgenet_fill(bm, edges=edges, mat_nr=0,
                           use_smooth=False, sides=4)
    # bm, verts, edges, geom = bm_extruder(
    #    'Edge', (0.0, 0.0, 0.05),  bm, verts, edges)
    # bmesh.ops.scale(bm, vec=(0, 0, 1),
    #                space = ob.matrix_local, verts = verts)

    # bmesh.ops.remove_doubles(bm, verts = bm.verts, dist = 0.0001)

    # res = bmesh.ops.contextual_create(
    #    bm, geom=geom, mat_nr=0, use_smooth=False)

    bm.to_mesh(me)
    bm.free()  # free

    mod = ob.modifiers.new(name="PUrP_Sub", type="SUBSURF")
    mod.levels = 3
    # bpy.ops.object.modifier_apply(modifier='PUrP_Sub')
    bpy.ops.object.shade_smooth()
    return context.object


def gen_arrow(context, loc):
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

    bm, verts, edges = bm_extruder(
        'Vert', (0, 0, 4),  bm, bm.verts, bm.edges)
    bm, verts, edges, = bm_extruder(
        'Vert', (1, 0, 0),  bm, verts, edges)

    bm, verts, edges, = bm_extruder(
        'Vert', (-2, 0, 1.5),  bm, verts, edges)

    # nach innen extrodieren
    bm, verts, edges, geo = bm_extruder(
        'Edge', (0, 0, 0),  bm, bm.verts, bm.edges)

    for v in verts:
        v.co = (0, 0, v.co[2])

    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)

    bm.to_mesh(me)
    bm.free()  # free
    bpy.ops.object.modifier_apply(modifier='PUrP_Mirror')
    return context.object
