

import bpy
import mathutils


def bvhOverlap(coup, CenterObj):

    couptmpdata = coup.data.copy()
    # generate copy at origin
    coup_tmp = bpy.data.objects.new(name="tmp", object_data=couptmpdata)
    # context.scene.collection.objects.link(coup_tmp)

    # move in edit mode,.... to lazy for bmesh
    # +++the location of the Centerobj (parent) + the location of the original mainplane
    for v in coup_tmp.data.vertices:
        # v.co += coup.parent.location  #### moving for parent not necessary because child already in centerobj space
        v.co += coup.location

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


context = bpy.context
coup = context.object
CenterObj = context.object.parent

bvhOverlap(coup, CenterObj)
