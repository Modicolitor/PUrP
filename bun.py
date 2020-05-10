
       
import bpy
import mathutils
from math import radians
from bpy.types import Scene, Image, Object
import random
import os
from .intersect import bmesh_check_intersect_objects


#from .properties import PUrPropertyGroup

'''Operator in Blender'''            

class PP_OT_AddSingleCoupling(bpy.types.Operator):
    bl_label="Add Single Couplings"
    bl_idname="add.coup"
    
    CylVert: bpy.props.IntProperty(
        name='Vertexcount',
        description='Set the resolution of the cylic objects',
        default=32,
    )
    PrimTypes: bpy.props.EnumProperty(
        name='SingleCoupltypes',  
        description='List of forms avaiable in single connector mode',
        items=[ ('0', '', ''),
                ('1','Cube',''),
                ('2','Cylinder', ''),
                ('3','Cone',''),
                ]
        #default= ''
        )
    
    @classmethod 
    def poll(cls,context):
        PUrP = context.scene.PUrP
        if (context.view_layer.objects.active != None) or (PUrP.CenterObj != None):                 #context.area.type == 'VIEW_3D':
            return True 
        return False
        
    def execute(self, context):
        #createSingleCoupling()
        #def createSingleCoupling():
        context = bpy.context
        data = bpy.data
        active = context.view_layer.objects.active
        PUrP = context.scene.PUrP
        CenterObj = PUrP.CenterObj
        PUrP_name  = PUrP.PUrP_name
        cursorloc = context.scene.cursor.location
        cursorlocori = context.scene.cursor.location
        #Prim = self.PrimTypes
       

        
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

        ####apply scale 
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        CenterObj_name = CenterObj.name
        CenterObj.PUrPCobj = True
        Centerloc = CenterObj.location
        
        
        #####make slice plane when not planar
        if PUrP.SingleCouplingModes != "4":
            bpy.ops.mesh.primitive_plane_add(size=6, enter_editmode=False, location=(0,0,0))
            context.object.name = str(PUrP_name) + "SingleConnector_" + str(random.randint(1, 999))
            newname_mainplane = context.object.name  
            
            bpy.ops.object.modifier_add(type='SOLIDIFY')
            context.object.display_type = 'WIRE'
            #context.object.show_in_front = True
            
            context.object.parent = data.objects[CenterObj_name]

            
            ###set boolean for the slice plane
            mod = data.objects[CenterObj_name].modifiers.new(name = context.object.name, type = "BOOLEAN")
            mod.object = data.objects[newname_mainplane]
            mod.operation = 'DIFFERENCE'
        else:
            newname_mainplane = "Null"   ### for planar


        loc = mathutils.Vector((0,0,0))
        print(f'CenterObj {CenterObj.name} vor Divisioncall. Active {active.name} ')
        coupModeDivision(CenterObj, newname_mainplane, loc)

    
        cursorloc.x -= CenterObj.location.x  
        cursorloc.y -= CenterObj.location.y
        cursorloc.z -= CenterObj.location.z
        #context.scene.objects.link(unioncopy)

        if PUrP.SingleCouplingModes != "4":
            data.objects[newname_mainplane].location += cursorloc
            data.objects[newname_mainplane].select_set(True)
        elif PUrP.SingleCouplingModes == "4":
            context.object.location += cursorloc
            context.object.select_set(True)

        context.scene.cursor.location = cursorlocori  
        context.object.select_set(True)
        
        return{"FINISHED"} 
        
    
def coupModeDivision(CenterObj, newname_mainplane,loc):
    data = bpy.data
    context = bpy.context
    PUrP = bpy.context.scene.PUrP
    
    
    if PUrP.SingleCouplingModes == "3":                     # flatCut
        active =  data.objects[newname_mainplane]
            
    elif PUrP.SingleCouplingModes == "2": ####Male - female 
        #add negativ object 
        loc.z += 0.45
        genPrimitive(CenterObj, newname_mainplane, '_diff', loc)

        #add positiv object 
        genPrimitive(CenterObj, newname_mainplane, '_union', loc)
        

    elif PUrP.SingleCouplingModes == "1":       #stick 
        genPrimitive(CenterObj, newname_mainplane, '_stick_diff', loc )
        genPrimitive(CenterObj, newname_mainplane, '_stick_fix', loc)          
    elif PUrP.SingleCouplingModes == "4":
        genPlanar()

def genPrimitive(CenterObj, newname_mainplane, nameadd, loc):
    context = bpy.context
    PUrP = bpy.context.scene.PUrP
    size = PUrP.CoupSize
    PrimTypes = context.scene.PUrP.SingleCouplingTypes
    CylVert = PUrP.CylVert

    if nameadd == "_diff":
        size *= PUrP.Oversize

    if PrimTypes == "1":
        bpy.ops.mesh.primitive_cube_add(size=size,location=loc)
    elif PrimTypes == "2":
        bpy.ops.mesh.primitive_cylinder_add(vertices=CylVert, radius=size, depth=1, enter_editmode=False, location=loc)

    elif PrimTypes == "3":
        bpy.ops.mesh.primitive_cone_add(vertices=CylVert, radius1=size, radius2=0, depth=2, enter_editmode=False, location=loc)

        #### z-scale die sticks 
    context.object.scale.z *= PUrP.zScale
    
    #### make name relative to the Couplingmainplain
    context.object.name = str(newname_mainplane)+ str(nameadd)
    context.object.parent = bpy.data.objects[newname_mainplane]
    context.object.display_type = 'WIRE'    
    context.object.show_in_front = True
    context.object.hide_select = True

    if ("_diff" in bpy.context.object.name) or ("_union" in bpy.context.object.name):
        mod = CenterObj.modifiers.new(name = context.object.name, type = "BOOLEAN")
        mod.object = context.object
        if nameadd == "_diff":
            mod.operation = 'DIFFERENCE'
        elif nameadd == '_union':
            mod.operation = 'UNION'
    else:
        pass


def genPlanar():
    context = bpy.context
    PUrP = bpy.context.scene.PUrP
    PUrP_name = PUrP.PUrP_name
    LineLength = PUrP.LineLength
    LineCount = PUrP.LineCount
    LineDistance = PUrP.LineDistance
    CenterObj = PUrP.CenterObj
    GlobalScale = PUrP.GlobalScale 
    CutThickness = PUrP.CutThickness
    OffsetRight = PUrP.OffsetRight
    OffsetLeft = PUrP.OffsetLeft
    height = 3
    type = PUrP.PlanarCouplingTypes

    
    ### I don't know how to get the name from the enum property might be simpler 
    if type == "1":      
        objectname = "Cubic"
    elif type == "2":      
        objectname = "Dovetail"
    elif type == "3":      
        objectname = "Puzzle"
    else: 
        objectname = "Cubic"
    
    newname = str(PUrP_name) + "PlanarConnector_" + str(random.randint(1, 999))
    nameadd = "_diff"

    appendCoupling("planar.blend", objectname)
    print(f'nache append active {context.object.name}, CenterObj {CenterObj.name}')
    context.object.name = str(newname)+ str(nameadd)

    print(f'active {context.object.name}, CenterObj {CenterObj.name}')

    context.object.parent = CenterObj
    context.object.display_type = 'WIRE'    
    context.object.show_in_front = True
    
    selected = context.selected_objects[:]
    for ob in selected:
        ob.select_set(False)
    
    import bmesh
    ##planar side offset 
    me = bpy.context.object.data

    # Get a BMesh representation
    bm = bmesh.new()   # create an empty BMesh
    bm.from_mesh(me)   # fill it in from a Mesh

    bm.verts.ensure_lookup_table()

    # Modify the BMesh, can do anything here...
    right = OffsetRight * GlobalScale
    left = OffsetLeft * GlobalScale

    bm.verts[0].co.x += right
    bm.verts[1].co.x -= left

    # Finish up, write the bmesh back to the mesh
    bm.to_mesh(me)
    bm.free()  # free 



    #extrude
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, height)})
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    #"mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False}
    bpy.ops.object.editmode_toggle()


    obj = context.object
    ###scale it a bit smaller than in the file 
    adjustScale = 0.25
    obj.scale.x *= adjustScale 
    obj.scale.y *= adjustScale 

    # but then also have a global scale 
    obj.scale *= GlobalScale 
    
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)


    

    ## array 1 und 2 
    mod = obj.modifiers.new(name="PUrP_Array_1", type="ARRAY")
    mod.use_merge_vertices = True
    mod.count = LineLength
    

    mod = obj.modifiers.new(name="PUrP_Array_2", type="ARRAY")
    mod.relative_offset_displace[0] = 0
    mod.relative_offset_displace[1] = LineDistance
    mod.count = LineCount
    mod.use_merge_vertices = True
    
    ## Solidify
    mod = obj.modifiers.new(name="Thickness", type="SOLIDIFY")
    mod.thickness = PUrP.CutThickness
    mod.use_even_offset = True

    
    
    ##boolean _diff at parent object
    mod = obj.parent.modifiers.new(name=obj.name, type = "BOOLEAN")
    mod.operation =  'DIFFERENCE'
    mod.object = obj
    print(f"Active after planar generation {context.object}, obj is {obj}")


def appendCoupling(filename, objectname):
        
        script_path = os.path.dirname(os.path.realpath(__file__))
        subpath = "blend" + os.sep + filename
        cp = os.path.join(script_path, subpath)
    
        
        #filepath = "//2.82\scripts\addons\purp\blend\new_library.blend"
        with bpy.data.libraries.load(cp) as (data_from, data_to):
            print('I am in')
            data_to.objects = [name for name in data_from.objects if name == objectname]
        
        for obj in data_to.objects:
            bpy.context.collection.objects.link(obj)
            obj.location = mathutils.Vector((0,0,0))
            bpy.context.view_layer.objects.active = obj



class PP_OT_ExChangeCoup(bpy.types.Operator):
    bl_idname = "object.exchangecoup"
    bl_label = "ExChangeCoupling"

    @classmethod
    def poll(cls, context):
        if (context.view_layer.objects.active != None):
            if ("SingleConnector" in context.view_layer.objects.active.name) or ("PlanarConnector" in context.view_layer.objects.active.name): 
                return True
        else: 
            return False


    def execute(self, context):
        
        context = bpy.context 
        data = bpy.data
        CenterObj = context.scene.PUrP.CenterObj
        PUrP = bpy.context.scene.PUrP
        PUrP_name = PUrP.PUrP_name
        CouplingModes = bpy.context.scene.PUrP.SingleCouplingModes 
        selected = context.selected_objects[:]

        for obj in selected: 
            if PUrP_name in obj.name:
                
                for mod in obj.parent.modifiers:
                    if obj.name in mod.name:
                        obj.parent.modifiers.remove(mod)

                for child in obj.children:
                    child.hide_select = False
                    child.select_set(True)
                    obj.select_set(False)
                    bpy.ops.object.delete(use_global=False)

                loc = mathutils.Vector((0,0,0))
                if CouplingModes == "4":     #  when planar
                    loc = obj.location.copy()
                    trans = obj.matrix_world.copy()
                    oldname = obj.name
                    for ob in context.selected_objects:             ## deselte all
                        ob.select_set(False)
                    obj.select_set(True)                          ## 
                    bpy.ops.object.delete(use_global=False)         ## delete the old planar coupling
                    coupModeDivision(CenterObj, oldname, loc)
                    context.object.matrix_world = trans
                    #context.object.location = loc                                                ##planarversion 
                else:
                    coupModeDivision(CenterObj, obj.name, loc)          
                
        
        
        return {'FINISHED'}
 
class PP_OT_ApplyCoupling(bpy.types.Operator):
    bl_label="ApplyCouplings"
    bl_idname="apl.coup"
    
    @classmethod
    def poll(cls, context):
        if (context.view_layer.objects.active != None):
            if ("SingleConnector" in context.view_layer.objects.active.name) or ("PlanarConnector" in context.view_layer.objects.active.name): 
                return True
        else: 
            return False
        

    def execute(self, context):
        #    applyCouplings()
        #def applyCouplings():
        context = bpy.context 
        data = bpy.data
        selected = context.selected_objects[:]
        #CenterObj = context.scene.PUrP.CenterObj
        PUrP_name = bpy.context.scene.PUrP.PUrP_name
        
        #### start conditions: seperators selected 
        
        for obj in selected:
            if PUrP_name in obj.name:
                CenterObj = obj.parent
                applySingleCoup(obj, CenterObj)
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
                print(f"I apply now modifier: {mod.name} to Object {daughter.name}. Active obj: {active.name}")
                context.view_layer.objects.active = daughter
                print(f"active: {active}")
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod.name)
                
                
            elif str(connector.name) + '_diff' == mod.name:
                print(f"I apply now modifier: {mod.name} to Object {daughter.name}")
                context.view_layer.objects.active = daughter
                print(f"active: {active}")
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod.name)
            elif str(connector.name) + '_union' == mod.name:
                print(f'I delete now  {mod.name} from Object {daughter.name}')
                daughter.modifiers.remove(mod)
    elif side == "POSITIV":
        print('Positive Seite')
        for mod in daughtermods:
            print(f"modifiert nam: {mod.name}")
            if str(connector.name) + '_stick_diff' == mod.name:
                print(f"I apply now modifier: {mod.name} to Object {daughter.name}")
                context.view_layer.objects.active = daughter
                print(f"active: {active}")
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod.name)

            elif str(connector.name) + '_union' == mod.name:
                context.view_layer.objects.active = daughter
                print(f"active: {active}")
                print(f"I apply now modifier: {mod.name} to Object {daughter.name}")
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod.name)
            elif str(connector.name) + '_diff' == mod.name:
                print(f'I delete now  {mod.name} from Object {daughter.name}')
                daughter.modifiers.remove(mod)
    else:
        print("Somethings Wrong with side determin" )
    #if context.scene.PUrP.PUrP_name not in daughter.name:
    #    daughter.name = str(context.scene.PUrP.PUrP_name) + str(daughter.name)

def removeCoupling(Coupl):
    '''removes objects related to the coupling after apllying or when it is a fixed '''
    data = bpy.data
    context = bpy.context
    active = context.view_layer.objects.active
    Coupl_children = Coupl.children[:]
    for child in Coupl_children:
        if "fix" not in child.name:             ####alle normalen couplings die applied sind
            child.hide_select = False
            
            for ob in context.selected_objects:
                ob.select_set(False)
            child.select_set(True)
            
            bpy.ops.object.delete(use_global=False)
        elif 'fix' in child.name:
            child.hide_select = False
            child.display_type = 'SOLID'
            #child.location = mathutils.Vector((0,0,0))
            globloc = Coupl.matrix_world
            print(f" Matrix World  von Coupl {globloc}")
            
            
            child.parent = None
            child.matrix_world = globloc
            #child.parent = context.scene.PUrP.CenterObj
            #child.name = context.scene.PUrP.PUrP_name + "CoupleStick"
            
    
    for ob in data.objects:
        ob.select_set(False) ## for deleting after this modifier removal
        for mod in ob.modifiers: 
            if Coupl.name in mod.name:
                ob.modifiers.remove(mod)


    
    Coupl.select_set(True)
    bpy.ops.object.delete(use_global=False)
   
Daughtercollection = []

def CenterObjCollector():
    data = bpy.data
    global Daughtercollection
    list(set(Daughtercollection))
    PUrP = bpy.context.scene.PUrP
    PUrP_name = PUrP.PUrP_name

    #if len(Daughtercollection) == 0:
    test = False
    print (f"DaughterCollection content {Daughtercollection}")
    for Daughter in Daughtercollection:
        for mod in Daughter.modifiers:
            if (PUrP_name in mod.name) and ("diff" not in mod.name) and ("union" not in mod.name):                 
                if bmesh_check_intersect_objects(data.objects[mod.name], Daughter):
                    print(f"intersect in Collector True for {mod.name} and {Daughter}")
                
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
    
    #n = 0
    #test = True 
    modifiers = CenterObj.modifiers[:] 

    for mod in modifiers: 
    #while test == True:
        print(f'nächste Runde für mod {mod.name} in CenterObj {CenterObj}')
        #if (len(CenterObj.modifiers) != 0) and (len(CenterObj.modifiers)-1 >= n):
        if (PUrP_name in mod.name) and ("diff" not in mod.name) and ("union" not in mod.name):  
            print('nächste Runde')
            #try: 
            #if PUrP_name in CenterObj.modifiers[n].name:
            #mod_name = CenterObj.modifiers[n].name
            if bmesh_check_intersect_objects(data.objects[mod.name], CenterObj):
                print("Intersection test is positiv")
                Daughters = applySingleCoup(data.objects[mod.name], CenterObj)
                print(f"Daughters send to collection {Daughters}")
                Daughtercollection.append(Daughters)
            
        
    #CenterObjCollector()
        #CenterObjCollector(Daughters)    
        
        #in reinfolge alle Modier des CenterObj durch schauen 
        #wenn der Modifier zu mir gehört 
        #nimm den Namen des modifiers 
    
'''test if the coupling plane intersects with the Obje'''
#def intersectCoup(Coup, CenterObj)
    
#    return True

def centerObjDecider(CenterObj):
    PUrP = bpy.context.scene.PUrP
    PUrP_name = PUrP.PUrP_name
    Objects = bpy.data.objects





    CouplingsMods = CenterObj.modifiers[:]
    ModList = []
    for PriMod in CouplingsMods:   #################look through the modifers of the centerObj and make a list of the Couplings that need to be applied
        if ("PUrP_" in PriMod.name) and ("diff" not in PriMod.name) and ("union" not in PriMod.name):
            primodname = PriMod.name[:]
            print(f"primodname {primodname}")
            ModList.append(primodname)




    for mod in ModList:
        print(f"centerObjdecider mod name {mod}")
        if PUrP_name in mod: 
            if ("diff" not in mod) and ("union" not in mod): 

                ####potential Cobj list (checking the Object bool),otherwise when I loo through all objects and delete objects during the round, the Objects change adress
                Cobjlist = []
                for pCobj in Objects: 
                    if pCobj.PUrPCobj == True:
                        Cobjlist.append(pCobj)                   

                for Cobj in Cobjlist:
                    print(f"centerObjdecider Cobj {Cobj}")

                    Cobjmodslist = [] ### now collect all the modifiers that belong to a single coupling (not diff and union), and nothing from user
                    for ele in Cobj.modifiers:
                        if ("PUrP_" in ele.name) and ("diff" not in ele.name) and ("union" not in ele.name):
                            Cobjmodslist.append(ele)

                    
                    
                    for Cmod in Cobjmodslist:  ##### look through addon own modifier liste and 
                        print(f"centerObjdecider Cmod name {Cmod.name}")
                        if Cmod.name == mod:

                            print(f"Intersect test: Connector {Objects[mod]} and Center obj {Cobj} {bmesh_check_intersect_objects(Objects[mod], Cobj)}")
                            if bmesh_check_intersect_objects(Objects[mod], Cobj):
                                print(f"centerObjdecider send applySingleCoup mod.name {mod} and CObj {Cobj}")
                                applySingleCoup(Objects[mod],Cobj)
                            else:
                                print(f"centerObjdecider remove now mod {mod} of Cobj {Cobj}")
                                #mid = Cobj.modifiers[mod]
                                #Cobj.modifiers.remove(mid)
         
 


def applySingleCoup(Coup, CenterObj):    
    context = bpy.context 
    data = bpy.data
    PUrP_name = bpy.context.scene.PUrP.PUrP_name
    
    obj = Coup
    
    for sel in context.selected_objects:
        sel.select_set(False)
        
    ###apply boolean to seperate Centralobj parts
    context.view_layer.objects.active = CenterObj
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier=obj.name)
    

    ###seperate by loose parts 
    
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.editmode_toggle()
    


    ####remember both objects 
    CenterObjDaughters = context.selected_objects[:]
    print(f'CenterObjDaugters are {CenterObjDaughters}')
    DaughterOne = context.active_object
    
    for ob in CenterObjDaughters:           ###setze das ob für zweite Tochter 
        if ob != DaughterOne:
            DaughterTwo = ob
    


    ####teste on which side a vertex of one object lays 
    context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)    #### apply rotation centerplane obj damit die vector rechnung funktioniert

    CouplingNormal = obj.data.vertices[0].normal
    ctl = False
    n= 0
    Daughtertwo_side = "NULL" 
    while ctl == False:
        
        #geo = mathutils.geometry.distance_point_to_plane(pt, plane_co, plane_no)
        geo = mathutils.geometry
        
        direction  = CouplingNormal.dot(DaughterOne.data.vertices[n].co) - CouplingNormal.dot(obj.data.vertices[0].co)
        print(f"that's the direction value {direction}")
        if direction == 0:   ####actual vector geometry part 
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

    applyRemoveCouplMods(DaughterTwo, obj, DaughterTwo_side)
    #deleConnector (later propably with checkbox)
    context.view_layer.objects.active = obj   
    removeCoupling(obj)
    Daughters = (DaughterOne, DaughterTwo)
    return Daughters
    
    
    #SingleConnectorNormal = objects.data.meshes['Cube.013'].vertices[1].normal


class PP_OT_ApplyAllCouplings(bpy.types.Operator):
    '''Applies all Couplings. If nothing is selected it applies the Couplings to all modified objects. If an Centerobject is selected, it only applies the all Coupling for this Object. If a Coupling is selected, all Couplings connectected to the same Centerobject will be applied'''
    bl_idname = "apl.allcoup"
    bl_label = "PP_OT_ApplyAllCouplings"

    @classmethod
    def poll(cls, context):
        
        if (context.view_layer.objects.active != None):
            if ("SingleConnector" in context.view_layer.objects.active.name) or ("PlanarConnector" in context.view_layer.objects.active.name): 
                return True
            
        else:
            return False

    def execute(self, context):
        PUrP = context.scene.PUrP
        PUrP_name = PUrP.PUrP_name
        data = bpy.data
        global Daughtercollection
        
        #wenn nichts selected, gehe durch alle objecte und schaue ob die bearbeitet wurden (müssen Couplings haben)
        if context.selected_objects == None:
            print('Its None und nicht "None"')
            for obj in data.objects:
                for child in obj.child:         ###gibt es kinder Coupling in diesem Object
                    if PUrP_name in child:
                        CenterBool = True
                        pass
                if CenterBool:
                    #Daughtercollection = [] 
                    #Daughtercollection.append(obj)
                    centerObjDecider(obj)
                    
                    #CenterObjCollector()
        
        elif context.selected_objects != None:
        
            selected = context.selected_objects[:]
            for obj in selected: 
                CenterBool = False
                #wenn couplin type selected , finde Papa und sende es  
                if PUrP_name in obj.name:
                    print("I am a selected Connector such meinen Papa")
                    #applyCenterObj(obj.parent)
                    #Daughtercollection = [] 
                    #Daughtercollection.append(obj.parent)
                    #CenterObjCollector()
                    centerObjDecider(obj.parent)
                else:
                    for child in obj.child:         ###gibt es kinder Coupling in diesem Object
                        if PUrP_name in child:
                            CenterBool = True
                            pass
                if CenterBool:
                    #Daughtercollection = [] 
                    #Daughtercollection.append(obj)
                    #CenterObjCollector()
                    centerObjDecider(obj)
                    #applyCenterObj(obj)

        #wenn coupling selected, apply für alle  
        
        
        return {'FINISHED'}

    
    

class PP_OT_DeleteCoupling(bpy.types.Operator):
    bl_label="DeleteCouplings"
    bl_idname="rem.coup"
    
    @classmethod
    def poll(cls, context):
        
        if (context.view_layer.objects.active != None):
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
                ####clean selection array
                for ob in context.selected_objects:
                    ob.select_set(False)
                    
                    #name_active = obj.name
                for child in obj.children:
                    child.hide_select = False
                    child.select_set(True)
                    bpy.ops.object.delete(use_global=False)
                
                ######entferne modifier und zwar immer auch wenn es schon zerlegt ist
                for mod in obj.parent.modifiers:
                    if (str(obj.name) + '_diff' == mod.name) or (str(obj.name) + '_union' == mod.name) or (str(obj.name) + '_stick_fix' == mod.name) or (str(obj.name) + '_stick_diff' == mod.name) or (str(obj.name) == mod.name):                 #######!!!!!!!!!!Das wird ein BUG     weil auch die ohne nummer gelöscht werden siehe lange zeile unten
                        print(f'I delete modifier {mod.name}')
                        obj.parent.modifiers.remove(mod)

                obj.select_set(True)
                print(f'selected objects{context.selected_objects}')
                bpy.ops.object.delete(use_global=False)

            context.view_layer.objects.active = context.scene.PUrP.CenterObj 
           
        return{"FINISHED"} 
     
class PP_OT_Ini(bpy.types.Operator):

    bl_label="Initialize PuzzleUrPrint"
    bl_idname="pup.init"
    
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
            collection = bpy.data.collections.new(name=MColName) # makes collection
            #scene.collection.children.link(collection) ###### when its not linked the user can not delete and break the ui, better solution for init behaviour necessary



        #Scene.PUrP.CenterObj = bpy.props.PointerProperty(name="Object", type=Object)


        CenterObj = bpy.context.scene.PUrP.CenterObj
        CenterObj = active

        ###Puzzle Ur print Element Name  
        #bpy.types.Scene.PUrP.PUrP_name = bpy.props.StringProperty()
        PUrP = bpy.context.scene.PUrP
        PUrP.PUrP_name = "PUrP_"
        #PUrP.SingleCouplingtypes = ('Cube', 'Cylinder', 'Cone')
        #CylVert 
                
        

        return{"FINISHED"} 


class PP_OT_OversizeOperator(bpy.types.Operator):
    bl_idname = "object.oversize"
    bl_label = "oversize"
    bl_options = {'REGISTER',"UNDO"}
    def execute(self, context):
        context.object.scale.x = self.value 
        context.object.scale.y = self.value 
        context.object.scale.z = self.value 
        return {'FINISHED'}

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':  # Apply
            self.delta = event.mouse_x - self.init_value
            self.value = self.init_scale_x + self.delta/1000  #- self.window_width/2 #(HD Screen 800)
            #print(f"MouspositionX: {self.value}")
            self.execute(context)
        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancels
            context.object.location.x = self.init_scale_x
            context.object.location.y = self.init_scale_y
            context.object.location.z = self.init_scale_z
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
       # self.window_width = context.window.width 
        self.init_scale_x = context.object.scale.x 
        self.init_scale_y = context.object.scale.y 
        self.init_scale_z = context.object.scale.z
        self.init_value = event.mouse_x

        self.value = context.object.scale.x           ##event.mouse_x #- self.window_width/21   ################mach mal start value einfach 00
        
        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


##


       