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

    coup_tmp.select_set(True)
    context.view_layer.objects.active = coup_tmp
    coup_tmp.matrix_world = matrix
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # make Solidify to the mainplane, but also more stuff for planar

    for mod in coup.modifiers:
        mod = coup_tmp.modifiers.new(name=mod.name, type=mod.type)
        if "PUrP_Solidify" == mod.name:
            mod.thickness = coup.modifiers["PUrP_Solidify"].thickness
            mod.offset = coup.modifiers["PUrP_Solidify"].offset
            mod.solidify_mode = coup.modifiers["PUrP_Solidify"].solidify_mode
            mod.nonmanifold_thickness_mode = coup.modifiers["PUrP_Solidify"].nonmanifold_thickness_mode
        elif "PUrP_Array_1" == mod.name:
            mod.count = coup.modifiers["PUrP_Array_1"].count
            mod.relative_offset_displace = coup.modifiers["PUrP_Array_1"].relative_offset_displace
        elif "PUrP_Array_2" == mod.name:
            mod.count = coup.modifiers["PUrP_Array_2"].count
            mod.relative_offset_displace = coup.modifiers["PUrP_Array_2"].constant_offset_displace
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


'''coup active, CenterObj selected'''


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
