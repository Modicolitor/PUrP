#import Blender
import bpy
import bmesh
import mathutils


def bmesh_copy_from_object(obj, transform=False, triangulate=True, apply_modifiers=False):
    """
    Returns a transformed, triangulated copy of the mesh
    """

    assert(obj.type == 'MESH')

    if apply_modifiers and obj.modifiers:
        me = obj.to_mesh(bpy.context.scene, True,
                         'PREVIEW', calc_tessface=False)
        bm = bmesh.new()
        bm.from_mesh(me)
        bpy.data.meshes.remove(me)
    else:
        me = obj.data
        if obj.mode == 'EDIT':
            bm_orig = bmesh.from_edit_mesh(me)
            bm = bm_orig.copy()
        else:
            bm = bmesh.new()
            bm.from_mesh(me)

    # Remove custom data layers to save memory
    for elem in (bm.faces, bm.edges, bm.verts, bm.loops):
        for layers_name in dir(elem.layers):
            if not layers_name.startswith("_"):
                layers = getattr(elem.layers, layers_name)
                for layer_name, layer in layers.items():
                    layers.remove(layer)

    if transform:
        bm.transform(obj.matrix_world)

    if triangulate:
        bmesh.ops.triangulate(bm, faces=bm.faces)

    return bm


def bmesh_check_intersect_objects(obj, obj2):
    """
    Check if any faces intersect with the other object

    returns a boolean
    """
    assert(obj != obj2)

    # Triangulate
    bm = bmesh_copy_from_object(obj, transform=True, triangulate=True)
    obj_matrixworld = obj.matrix_world
    bm2 = bmesh_copy_from_object(obj2, transform=True, triangulate=True)
    obj2_matrixworld = obj2.matrix_world
    # If bm has more edges, use bm2 instead for looping over its edges
    # (so we cast less rays from the simpler object to the more complex object)

    if len(bm.edges) > len(bm2.edges):
        bm2, bm = bm, bm2
        obj2_matrixworld, obj_matrixworld = obj_matrixworld, obj2_matrixworld

    # Create a real mesh (lame!)
    scene = bpy.context.scene
    me_tmp = bpy.data.meshes.new(name="~temp~")
    bm2.to_mesh(me_tmp)
    bm2.free()
    obj_tmp = bpy.data.objects.new(name=me_tmp.name, object_data=me_tmp)
    scene.collection.objects.link(obj_tmp)

    # scene.update()
    ray_cast = obj_tmp.ray_cast

    intersect = False

    EPS_NORMAL = 0.000001
    EPS_CENTER = 0.01  # should always be bigger

    # for ed in me_tmp.edges:
    for ed in bm.edges:
        v1, v2 = ed.verts

        # setup the edge with an offset
        co_1 = v1.co.copy()
        co_2 = v2.co.copy()
        print(
            f"before co_1 {co_1} Matrixworld {obj.name} 0 : {obj_matrixworld[0][3]} 1 : {obj_matrixworld[1][3]} 2: {obj_matrixworld[2][3]}")
        co_1[0] = obj2_matrixworld[0][3] + co_1[0]
        co_1[1] = obj2_matrixworld[1][3] + co_1[1]
        co_1[2] = obj2_matrixworld[2][3] + co_1[2]

        co_2[0] = obj2_matrixworld[0][3] + co_2[0]
        co_2[1] = obj2_matrixworld[1][3] + co_2[1]
        co_2[2] = obj2_matrixworld[2][3] + co_2[2]
        print(f"after changes co_1 {co_1}")

        co_mid = (co_1 + co_2) * 0.5
        no_mid = (v1.normal + v2.normal).normalized() * EPS_NORMAL
        co_1 = co_1.lerp(co_mid, EPS_CENTER) + no_mid
        co_2 = co_2.lerp(co_mid, EPS_CENTER) + no_mid

        extra_var, co, no, index = ray_cast(co_1, co_2)

        if index != -1:
            intersect = True
            break

    scene.collection.objects.unlink(obj_tmp)
    bpy.data.objects.remove(obj_tmp)
    bpy.data.meshes.remove(me_tmp)

    return intersect


#obj = bpy.context.object
#obj2 = (ob for ob in bpy.context.selected_objects if ob != obj).__next__()
# intersect = bmesh_check_intersect_objects(obj, obj2)   ### returns True if...


"""
# ------------ intersect boundingboxes


class BoundingEdge:
    def __init__(self, v0, v1):
        self.vertex = (v0, v1)
        self.vector = v1 - v0


class BoundingFace:
    def __init__(self, v0, v1, v2):
        self.vertex = (v0, v1, v2)
        self.normal = Blender.Mathutils.TriangleNormal(v0, v1, v2)


class BoundingBox:
    def __init__(self, ob):
        self.vertex = ob.getBoundBox()
        if self.vertex != None:
            self.edge = [BoundingEdge(self.vertex[0], self.vertex[1]),
                         BoundingEdge(self.vertex[1], self.vertex[2]),
                         BoundingEdge(self.vertex[2], self.vertex[3]),
                         BoundingEdge(self.vertex[3], self.vertex[0]),
                         BoundingEdge(self.vertex[4], self.vertex[5]),
                         BoundingEdge(self.vertex[5], self.vertex[6]),
                         BoundingEdge(self.vertex[6], self.vertex[7]),
                         BoundingEdge(self.vertex[7], self.vertex[4]),
                         BoundingEdge(self.vertex[0], self.vertex[4]),
                         BoundingEdge(self.vertex[1], self.vertex[5]),
                         BoundingEdge(self.vertex[2], self.vertex[6]),
                         BoundingEdge(self.vertex[3], self.vertex[7])]
            self.face = [BoundingFace(self.vertex[0], self.vertex[1], self.vertex[3]),
                         BoundingFace(
                             self.vertex[0], self.vertex[4], self.vertex[1]),
                         BoundingFace(
                             self.vertex[0], self.vertex[3], self.vertex[4]),
                         BoundingFace(
                             self.vertex[6], self.vertex[5], self.vertex[7]),
                         BoundingFace(
                             self.vertex[6], self.vertex[7], self.vertex[2]),
                         BoundingFace(self.vertex[6], self.vertex[2], self.vertex[5])]

    def whichSide(self, vtxs, normal, faceVtx):
        retVal = 0
        positive = 0
        negative = 0
        for v in vtxs:
            t = normal.dot(v - faceVtx)
            if t & gt; 0:
                positive = positive + 1
            elif t & lt; 0:
                negative = negative + 1

            if positive != 0 and negative != 0:
                return 0

        if positive != 0:
            retVal = 1
        else:
            retVal = -1
        return retVal

    # Taken from: http://www.geometrictools.com/Documentation/MethodOfSeparatingAxes.pdf

    def intersect(self, bb):
        retVal = False
        if self.vertex != None and bb.vertex != None:
            # check all the faces of this object for a seperation axis
            for i, f in enumerate(self.face):
                d = f.normal
                if self.whichSide(bb.vertex, d, f.vertex[0]) & gt; 0:
                    return False  # all the vertexes are on the +ve side of the face

            # now do it again for the other objects faces
            for i, f in enumerate(bb.face):
                d = f.normal
                if self.whichSide(self.vertex, d, f.vertex[0]) & gt; 0:
                    return False  # all the vertexes are on the +ve side of the face

            # do edge checks
            for e1 in self.edge:
                for e2 in bb.edge:
                    d = e1.vector.cross(e2.vector)
                    side0 = self.whichSide(self.vertex, d, e1.vertex[0])
                    if side0 == 0:
                        continue
                    side1 = self.whichSide(bb.vertex, d, e1.vertex[0])
                    if side1 == 0:
                        continue

                    if (side0 * side1) & lt; 0:
                        return False

            retVal = True
        return retVal


sce = bpy.data.scenes.active

tOb = sce.objects.active
tObBb = BoundingBox(tOb)
for ob in sce.objects:
    if ob != tOb:
        print "intersects: %u" % tObBb.intersect(BoundingBox(ob))
"""
