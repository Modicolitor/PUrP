import bpy
import mathutils
from math import radians
from bpy.types import Scene, Image, Object
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
        items=[ ('1','Cube',''),
                ('2','Cylinder', ''),
                ('3','Cone',''),
                ]
        #default= ''
        )
    
    @classmethod 
    def poll(cls,context):
        if context.view_layer.objects.active != None:                 #context.area.type == 'VIEW_3D':
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
        #Prim = self.PrimTypes
       

        print(f'Cyclverts has the value{self.CylVert}')

        if active.type == "MESH":
            if PUrP_name in active.name:
                CenterObj = context.scene.PUrP.CenterObj
            else: 
                CenterObj = active
                context.scene.PUrP.CenterObj = CenterObj
        ####apply scale 
            
        CenterObj_name = CenterObj.name
        bpy.ops.mesh.primitive_plane_add(size=6, enter_editmode=False, location=(0, 0, 0))
        context.object.name = str(PUrP_name) + "SingleConnector"
        newname_mainplane = context.object.name  
        
        bpy.ops.object.modifier_add(type='SOLIDIFY')
        context.object.display_type = 'WIRE'
        #context.object.show_in_front = True

        context.object.parent = data.objects[CenterObj_name]

        
        ###set boolean for the slice plane
        mod = data.objects[CenterObj_name].modifiers.new(name = context.object.name, type = "BOOLEAN")
        mod.object = data.objects[newname_mainplane]
        mod.operation = 'DIFFERENCE'

        loc = context.scene.cursor.location

        print(f'Mode aktivated: {PUrP.SingleCouplingModes}')   
        if PUrP.SingleCouplingModes == "3":                     # flatCut
            active =  data.objects[newname_mainplane]
              
        elif PUrP.SingleCouplingModes == "2": ####Male - female 
            #add negativ object 
            loc.z += 0.45
            self.genPrimitive(context, CenterObj, newname_mainplane, '_diff' , loc)

            #add positiv object 
            self.genPrimitive(context, CenterObj, newname_mainplane, '_union', loc)
            

        elif PUrP.SingleCouplingModes == "1":       #stick 
            self.genPrimitive(context, CenterObj, newname_mainplane, '_diff', loc)
            self.genPrimitive(context, CenterObj, newname_mainplane, '_fix', loc)          

            
            #context.scene.objects.link(unioncopy)
            
        return{"FINISHED"} 
    
    def genPrimitive(self, context, CenterObj, newname_mainplane, nameadd, loc):
        PUrP = bpy.context.scene.PUrP
        size = PUrP.CoupSize
        if nameadd == "_diff":
            size *= PUrP.Oversize

        if self.PrimTypes == "1":
            print("I'm in...")
            bpy.ops.mesh.primitive_cube_add(size=size,location=loc)
        elif self.PrimTypes == "2":
            bpy.ops.mesh.primitive_cylinder_add(vertices=self.CylVert, radius=size, depth=1, enter_editmode=False, location=loc)

        elif self.PrimTypes == "3":
            bpy.ops.mesh.primitive_cone_add(vertices=self.CylVert, radius1=size, radius2=0, depth=2, enter_editmode=False, location=loc)

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

        

       

class PP_OT_ExChangeCoupOperator(bpy.types.Operator):
    bl_idname = "object.pp_ot_exchangecoup"
    bl_label = "ExChangeCoup"
    bl

    @classmethod
    def poll(self, context):
        return True


    def execute(self, context):
        
        print("here I'am an")
        
        return {'FINISHED'}
       



def applyRemoveCouplMods(context, daughter, connector, side):
    if side == "NEGATIV":
        for mod in daughter.modifiers:
            print(mod.name)
            
            if str(connector.name) + '_diff' == mod.name:
                print(f"I apply now modifier: {mod.name} to Object {daughter.name}")
                context.view_layer.objects.active = daughter
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier=str(connector.name) + '_diff')
            elif str(connector.name) + '_union' == mod.name:
                print(f'I delete now  {mod.name} from Object {daughter.name}')
                context.view_layer.objects.active = daughter
                daughter.modifiers.remove(mod)
    elif side == "POSITIV":
        for mod in daughter.modifiers:
            print(mod.name)
            
            if str(connector.name) + '_union' == mod.name:
                print(f"I apply now modifier: {mod.name} to Object {daughter.name}")
                context.view_layer.objects.active = daughter
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier=str(connector.name) + '_union')
            elif str(connector.name) + '_diff' == mod.name:
                print(f'I delete now  {mod.name} from Object {daughter.name}')
                context.view_layer.objects.active = daughter
                daughter.modifiers.remove(mod)
    else:
        print("Somethings Wrong with side determin" )



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
                print('ich bin das Zentrale object ' + str(CenterObj.name)) 
                
                
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
                #DaughterMesh = DaughterOne.meshes.name
                for ob in CenterObjDaughters:
                    if ob != DaughterOne:
                        DaughterTwo = ob
                
        
        
        ####teste on which side a vertex of one object lays 
                context.view_layer.objects.active = obj
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

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
                        applyRemoveCouplMods(context, DaughterOne, obj, DaughterOne_side)
                        
                        
                    elif direction > 0: 
                        
                        ctl = True
                        print('negativ seite')
                        DaughterOne_side = "NEGATIV"
                        DaughterTwo_side = "POSITIV" 
                        applyRemoveCouplMods(context, DaughterOne, obj, DaughterOne_side)
                                
                                #bpy.ops.object.modifier_remove(mod.name)
                                #C.object.modifiers.remove(C.object.modifiers['PUrP_SingleConnector_diff']
                    else:
                        print('Probleme with side detection') 
                    
        ### apply right bool and discard second bool 
        
        
        ####do the opposite for the 
                
                
                applyRemoveCouplMods(context, DaughterTwo, obj, DaughterTwo_side)
            
            
        
        #deleConnector (later propably with checkbox)
                context.view_layer.objects.active = obj   
                bpy.ops.rem.coup()
        
        #SingleConnectorNormal = objects.data.meshes['Cube.013'].vertices[1].normal

        return{"FINISHED"} 


  
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
        
        
        if "SingleConnector" in active.name:
            name_active = active.name
            for obj in objects:                          #####schau in allen Objekten
                if (str(name_active) + '_diff' == obj.name) or (str(name_active) + '_union' == obj.name) or (str(name_active) + '_fix' == obj.name) or (str(name_active) == obj.name):              #####wenn der name des aktiven obj im namen des objects passt dann
                    
                    
                    ###delete centerobj modifiers
                    Centerobj = context.scene.PUrP.CenterObj
                    print('Centerobj is called '+str(Centerobj.name))
                    for mod in Centerobj.modifiers:
                        if mod.name == obj.name:
                            Centerobj.modifiers.remove(mod)
                    
                    
                    obj.hide_select = False    ###  selectierbar machen 
                    #active = obj
                    
                    for ob in context.selected_objects:
                        ob.select_set(False)
                    
                    obj.select_set(True)
                    bpy.ops.object.delete(use_global=False)
                    
                    ###delete centerobj modifiers
                    
                    
                    
                    
            print('connector')
            active = context.scene.PUrP.CenterObj 
        else:
            print("No connectorselected")

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



