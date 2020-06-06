import bpy
import mathutils


def bvhOverlap():
    context = bpy.context

    obj = context.object
    for e in context.selected_objects:
        if e != obj:
            obj2 = e

    # mathutils.bvhtree.BVHTree(bmesh, epsilon=0.0) BVH tree based on BMesh data.
    depsgraph = context.evaluated_depsgraph_get()
    BVHTree = mathutils.bvhtree.BVHTree
    BVHTree1 = BVHTree.FromObject(
        obj, depsgraph, deform=True)

    BVHTree2 = BVHTree.FromObject(
        obj2, depsgraph, deform=True)  # render=False, cage=False, epsilon=0.0

    overlaplist = BVHTree1.overlap(BVHTree2)
    print("###########################")
    for num, el in enumerate(overlaplist):
        print(str(num) + str(el))


bvhOverlap()
