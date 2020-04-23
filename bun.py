import bpy
import mathutils
from math import radians
from bpy.types import Scene, Image, Object
import random
import os

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

        ####apply scale 
            
        CenterObj_name = CenterObj.name
        Centerloc = CenterObj.location
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
        
        loc = mathutils.Vector((0,0,0))
        coupModeDivision(CenterObj, newname_mainplane, loc)

        
        cursorloc.x -= CenterObj.location.x  
        cursorloc.y -= CenterObj.location.y
        cursorloc.z -= CenterObj.location.z
        #context.scene.objects.link(unioncopy)

        data.objects[newname_mainplane].location += cursorloc
        context.scene.cursor.location = cursorlocori  
        
        return{"FINISHED"} 
        
    
def coupModeDivision(CenterObj, newname_mainplane,loc):
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
        appendPlanar()

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

        #### scale die sticks
    context.object.scale.z *= PUrP.zScale

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


def appendPlanar(newname_mainplane, nameadd):
    PUrP = bpy.context.scene.PUrP
    
    appendCoupling(planar, objectname)

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



class PP_OT_ExChangeCoup(bpy.types.Operator):
    bl_idname = "object.exchangecoup"
    bl_label = "ExChangeCoupling"

    @classmethod
    def poll(self, context):
        
        return (context.object != None) and (context.scene.PUrP.PUrP_name in context.object.name)


    def execute(self, context):
        
        context = bpy.context 
        data = bpy.data
        CenterObj = context.scene.PUrP.CenterObj
        PUrP_name = bpy.context.scene.PUrP.PUrP_name
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
                coupModeDivision(CenterObj, obj.name, loc)
                
        
        
        return {'FINISHED'}
 
class PP_OT_ApplyCoupling(bpy.types.Operator):
    bl_label="ApplyCouplings"
    bl_idname="apl.coup"
    
    def execute(self, context):
    #    applyCouplings()
    #def applyCouplings():
        context = bpy.context 
        data = bpy.data
        selected = context.selected_objects[:]
        CenterObj = context.scene.PUrP.CenterObj
        PUrP_name = bpy.context.scene.PUrP.PUrP_name
        
        #### start conditions: seperators selected 
        
        for obj in selected: 
            if PUrP_name in obj.name:
                
                ###apply boolean to seperate Centralobj parts
                context.view_layer.objects.active = CenterObj
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier=obj.name)
                
        
        ###seperate by loose parts 
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier="PUrP_SingleConnector")
                bpy.ops.object.editmode_toggle()
                bpy.ops.mesh.separate(type='LOOSE')
                bpy.ops.object.editmode_toggle()
                

        
        ####remember both objects 
                CenterObjDaughters = context.selected_objects[:]
                
                DaughterOne = context.active_object
                
                for ob in CenterObjDaughters:           ###setze das ob für zweite Tochter 
                    if ob != DaughterOne:
                        DaughterTwo = ob
                
        
        
        ####teste on which side a vertex of one object lays 
                context.view_layer.objects.active = obj
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)    #### apply rotation centerplane obj damit die vector rechnung funktioniert

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
                        self.applyRemoveCouplMods(context, DaughterOne, obj, DaughterOne_side)
                    elif direction > 0: 
                        ctl = True
                        print('negativ seite')
                        DaughterOne_side = "NEGATIV"
                        DaughterTwo_side = "POSITIV" 
                        self.applyRemoveCouplMods(context, DaughterOne, obj, DaughterOne_side)
                               
                    else:
                        print('Probleme with side detection') 
  
                self.applyRemoveCouplMods(context, DaughterTwo, obj, DaughterTwo_side)
                #deleConnector (later propably with checkbox)
                context.view_layer.objects.active = obj   
                self.removeCoupling(context, obj)
        
        
        
        #SingleConnectorNormal = objects.data.meshes['Cube.013'].vertices[1].normal

        return{"FINISHED"} 
    
    def applyRemoveCouplMods(self, context, daughter, connector, side):
        print(f"daughter: {daughter} connector: {connector}, side : {side}")
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

    def removeCoupling(self, context, Coupl):
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
                child.display_type = 'SOLID'
                child.location = mathutils.Vector((0,0,0))

                child.parent = context.scene.PUrP.CenterObj
                child.name = context.scene.PUrP.PUrP_name + "CoupleStick"
                child.hide_select = False
        Coupl.select_set(True)
        bpy.ops.object.delete(use_global=False)

class PP_OT_DeleteCoupling(bpy.types.Operator):
    bl_label="DeleteCouplings"
    bl_idname="rem.coup"
    
    @classmethod
    def poll(cls, context):
        
        if (context.view_layer.objects.active != None) and ("SingleConnector" in context.view_layer.objects.active.name):
            return True
        else:
            return False


    def execute(self, context):
        
        active = context.view_layer.objects.active
        objects = bpy.data.objects
        selected = context.selected_objects[:]


        for obj in selected:
            if "SingleConnector" in obj.name:
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



class AppendFromFileOperator(bpy.types.Operator):
    bl_idname = "object.appendfromfile"
    bl_label = "appendFromFile"

    def execute(self, context):
        
        self.appendCoupling("Cubic")
        self.appendCoupling("Puzzle")
        self.appendCoupling("Dovetail")
        
        
        return {'FINISHED'}

    def appendCoupling(self, objectname):
        
        script_path = os.path.dirname(os.path.realpath(__file__))
        subpath = "blend" + os.sep + "planar.blend"
        cp = os.path.join(script_path, subpath)
    
        
        #filepath = "//2.82\scripts\addons\purp\blend\new_library.blend"
        with bpy.data.libraries.load(cp) as (data_from, data_to):
            print('I am in')
            data_to.objects = [name for name in data_from.objects if name == objectname]
        
        for obj in data_to.objects:
            bpy.context.collection.objects.link(obj)
            obj.location = mathutils.Vector((0,0,0))

        

        # write selected objects and their data to a blend file
        #data_blocks = set(bpy.context.selected_objects)
        #bpy.data.libraries.write(filepath, data_blocks)



        '''https://devtalk.blender.org/t/append-entire-scene-python-to-current-scene/280/8
        FILEPATH = '/home/januz/tmp/appen_test.blend'
        with bpy.data.libraries.load(FILEPATH) as (data_from, data_to):
            data_to.objects = [name for name in data_from.objects]
            print('These are the objs: ', data_to.objects)

        # Objects have to be linked to show up in a scene
        for obj in data_to.objects:
            bpy.context.scene.objects.link(obj)'''

        ##https://stackoverflow.com/questions/33447680/blender-open-and-parse-a-blend-file-from-python-script

        #https://docs.blender.org/api/current/bpy.path.html    