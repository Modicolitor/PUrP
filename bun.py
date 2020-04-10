import bpy
import mathutils
from math import radians

'''Operator in Blender'''            

class PP_OT_AddSingleCoupling(bpy.types.Operator):
    bl_label="Add Single Couplings"
    bl_idname="add.coup"
    
    @classmethod 
    def poll(cls,context):
      #  if context.area.type == 'VIEW_3D':
         return True 
       # return False
        
    def execute(self, context):
        #createSingleCoupling()
        #def createSingleCoupling():
        context = bpy.context
        data = bpy.data
        PUrP_CenterObj = context.scene.PUrP_CenterObj
        
        ####apply scale 
        
        
        PUrP_name  = context.scene.PUrP_name
        
        
        if PUrP_CenterObj.type == 'MESH':
            CenterObj_name = context.scene.PUrP_CenterObj.name
            bpy.ops.mesh.primitive_plane_add(size=6, enter_editmode=False, location=(0, 0, 0))
            context.object.name = str(PUrP_name) + "SingleConnector"
            newname_mainplane = context.object.name  
            
            bpy.ops.object.modifier_add(type='SOLIDIFY')
            context.object.display_type = 'WIRE'
            context.object.parent = data.objects[CenterObj_name]
        # bpy.types.Object.connector_children = bpy.props.CollectionProperty()
            
            ###set boolean for the slice plane
            mod = data.objects[CenterObj_name].modifiers.new(name = context.object.name, type = "BOOLEAN")
            mod.object = data.objects[newname_mainplane]
            mod.operation = 'DIFFERENCE'

            
            
        
            
            #add negativ object 
            bpy.ops.mesh.primitive_cube_add(size=1,location=(0,0,0.45))
            context.object.name = str(newname_mainplane)+"_diff"
            context.object.parent = data.objects[newname_mainplane]
            context.object.display_type = 'WIRE'    
            context.object.hide_select = True
            
            mod = data.objects[CenterObj_name].modifiers.new(name = context.object.name, type = "BOOLEAN")
            mod.object = context.object
            mod.operation = 'DIFFERENCE'

            #add positiv object 

            bpy.ops.mesh.primitive_cube_add(size=0.95,location=(0,0,0.45))
            context.object.name = str(newname_mainplane)+"_union"
            context.object.parent = data.objects[newname_mainplane]
            context.object.display_type = 'WIRE'
            context.object.hide_select = True
            
            mod = data.objects[CenterObj_name].modifiers.new(name = context.object.name, type = "BOOLEAN")
            mod.object = context.object
            mod.operation = 'UNION'
            
            
            context.view_layer.objects.active =  data.objects[newname_mainplane]
            

            return{"FINISHED"}     




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
        CenterObj = context.scene.PUrP_CenterObj
        PUrP_name = bpy.context.scene.PUrP_name
        
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

def modifier_sucher(name):
    name
  
class PP_OT_DeleteCoupling(bpy.types.Operator):
    bl_label="DeleteCouplings"
    bl_idname="rem.coup"
    
    def execute(self, context):
        
        active = context.view_layer.objects.active
        objects = bpy.data.objects
        
        
        if "SingleConnector" in active.name:
            name_active = str(active.name)
            for obj in objects:                          #####schau in allen Objekten
                if name_active in obj.name:              #####wenn der name des aktiven obj im namen des objects passt dann
                    
                    
                    ###delete centerobj modifiers
                    Centerobj = context.scene.PUrP_CenterObj
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
             
        else:
            print("No connectorselected")

        return{"FINISHED"} 
     
     