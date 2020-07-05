import bpy
import mathutils


def bvhOverlap(context, coup, CenterObj):
    print(f"in BVHanfang coup.location {coup.location}")
    # making a copy of the coup plane
    matrix = coup.matrix_world
    couptmpdata = coup.data.copy()
    # generate copy at origin
    coup_tmp = bpy.data.objects.new(name="tmp", object_data=couptmpdata)
    coup_tmp.parent = CenterObj

    context.scene.collection.objects.link(coup_tmp)

    for ob in context.selected_objects:
        ob.select_set(False)
    # coup.select_set(False)
    # CenterObj.select_set(False)
    coup_tmp.select_set(True)
    context.view_layer.objects.active = coup_tmp
    coup_tmp.matrix_world = matrix
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=False)

    # make Solidify to the mainplane, but also more stuff for planar

    for mod in coup.modifiers:
        mod = coup_tmp.modifiers.new(name=mod.name, type=mod.type)
        if "PUrP_Solidify" == mod.name:
            mod.thickness = coup.modifiers["PUrP_Solidify"].thickness
            mod.offset = -1.0
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod.name)

    # coup_tmp.select_set(True)
    # coup.select_set(False)
    # bpy.ops.object.transform_apply(location=True, rotation=True, scale=False)

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
        for ob in context.selected_objects:
            if ob != coup:
                CenterObj = ob
        bvhOverlap(context, coup, CenterObj)

        return {'FINISHED'}
