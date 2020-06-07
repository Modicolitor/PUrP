import bpy
import mathutils


def bvhOverlap(context, coup, CenterObj):
    matrix = coup.matrix_local
    couptmpdata = coup.data.copy()
    # generate copy at origin
    coup_tmp = bpy.data.objects.new(name="tmp", object_data=couptmpdata)
    coup_tmp.parent = CenterObj

    context.scene.collection.objects.link(coup_tmp)

    context.view_layer.objects.active = coup_tmp
    coup_tmp.select_set(True)
    coup.select_set(False)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=False)

    for mod in coup.modifiers:
        mod = coup_tmp.modifiers.new(name=mod.name, type=mod.type)
        if "PUrP_Solidify" == mod.name:
            mod.thickness = coup.modifiers["PUrP_Solidify"].thickness
            mod.offset = -1.0
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod.name)

    coup_tmp.matrix_local = matrix
    coup_tmp.select_set(True)
    coup.select_set(False)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=False)
    # move in edit mode,.... to lazy for bmesh
    # +++the location of the Centerobj (parent) + the location of the original mainplane
    # for v in coup_tmp.data.vertices:
    #v.co += coup.parent.location
    #    v.co += coup.location

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
        print("BVH Overlap True")
        return True
    else:
        print("BVH Overlap False")
        return False


class PP_OT_OverlapcheckOperator(bpy.types.Operator):
    bl_idname = "object.pp_ot_overlapcheck"
    bl_label = "PP_OT_Overlapchecl"

    def execute(self, context):
        coup = context.object
        bvhOverlap(context, coup, coup.parent)

        return {'FINISHED'}
