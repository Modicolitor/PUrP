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
#from bpy.ops.object import subdivision_set
import mathutils
#from .bun import is_planar, applyScalRot


def bvhOverlap(context, coup, CenterObj):
    #print(f"in BVHanfang coup.location {coup.location}")
    # making a copy of the coup plane
    matrix = coup.matrix_world
    couptmpdata = coup.data.copy()
    # generate copy at origin
    coup_tmp = bpy.data.objects.new(name="tmp", object_data=couptmpdata)
    coup_tmp.parent = CenterObj

    context.scene.collection.objects.link(coup_tmp)

    for ob in context.selected_objects:
        ob.select_set(False)

    # coup_tmp.select_set(True)
    #context.view_layer.objects.active = coup_tmp
    coup_tmp.matrix_world = matrix
    # if "Planar" in coup.name:
    #    print("Planar)
    #    bvhapplyScalRot(coup_tmp)
    # else:
    #

    # make Solidify to the mainplane, but also more stuff for planar
    context.view_layer.objects.active = coup_tmp

    for mod in coup.modifiers:
        mod = coup_tmp.modifiers.new(name=mod.name, type=mod.type)
        if "PUrP_Solidify" == mod.name:
            #mod = coup.modifiers["PUrP_Solidify"]
            mod.thickness = coup.modifiers["PUrP_Solidify"].thickness
            mod.offset = coup.modifiers["PUrP_Solidify"].offset
            mod.solidify_mode = coup.modifiers["PUrP_Solidify"].solidify_mode
            mod.nonmanifold_thickness_mode = coup.modifiers["PUrP_Solidify"].nonmanifold_thickness_mode
        elif "PUrP_Array_1" == mod.name:
            mod.count = coup.modifiers["PUrP_Array_1"].count
            mod.relative_offset_displace = coup.modifiers["PUrP_Array_1"].relative_offset_displace
            mod.use_merge_vertices = coup.modifiers["PUrP_Array_2"].use_merge_vertices
        elif "PUrP_Array_2" == mod.name:
            mod.count = coup.modifiers["PUrP_Array_2"].count
            mod.use_relative_offset = False
            mod.use_constant_offset = True
            mod.constant_offset_displace = coup.modifiers["PUrP_Array_2"].constant_offset_displace
            mod.use_merge_vertices = coup.modifiers["PUrP_Array_2"].use_merge_vertices
        try:
            bpy.ops.object.modifier_apply(modifier=mod.name)
        except:
            print('Problem in Applying the Modifier')

    '''mod = coup_tmp.modifiers.new(name='PUrP_Helpsubsurf', type='SUBSURF')
    mod.levels = 2
    mod.subdivision_type = 'SIMPLE'
    bpy.ops.object.modifier_apply(modifier=mod.name)'''

    coup_tmp.select_set(True)
    coup_tmp.matrix_world = matrix

    # coup.select_set(False)
    context.view_layer.objects.active = coup_tmp
    # bvhapplyScalRot(coup_tmp)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # BVH Tree creation
    depsgraph = context.evaluated_depsgraph_get()
    BVHTree = mathutils.bvhtree.BVHTree
    BVHTreeCoup = BVHTree.FromObject(
        coup_tmp, depsgraph, deform=True)

    BVHTreeCenterObj = BVHTree.FromObject(
        CenterObj, depsgraph, deform=True)  # render=False, cage=False, epsilon=0.0

    overlaplist = BVHTreeCoup.overlap(BVHTreeCenterObj)
    print("###########################")
    # remove coup tmp
    bpy.data.objects.remove(coup_tmp)

    if len(overlaplist) > 0:
        print(
            f"BVH Overlap True for coup {coup.name}  Cob {CenterObj.name}")
        return True
    else:
        print(
            f"BVH Overlap False for coup {coup.name}  Cob {CenterObj.name}")
        return False


class PP_OT_OverlapcheckOperator(bpy.types.Operator):
    bl_idname = "object.pp_ot_overlapcheck"
    bl_label = "PP_OT_Overlapchecl"
    bl_options = {'REGISTER', "UNDO"}

    def execute(self, context):
        coup = context.object
        for ob in context.selected_objects:
            if ob != coup:
                CenterObj = ob
        bvhOverlap(context, coup, CenterObj)

        return {'FINISHED'}


def bvhapplyScalRot(obj):
    mat = obj.matrix_world
    # translation/ location vector
    trans = mathutils.Matrix.Translation(mathutils.Vector(
        (obj.matrix_world[0][3], obj.matrix_world[1][3], obj.matrix_world[2][3])))

    # ob data
    me = obj.data
    for v in me.vertices:
        v.co = v.co@mat
    mat.identity()
    mat @= trans
