#
# Copyright (C) 2020 by Modicolitor
#
# This file is part of PuzzleUrPrint.
#
# License Text
#
# You should have received a copy of the GNU General Public License along with Power Sequencer. If
# not, see <https://www.gnu.org/licenses/>.

import bpy 


from .utils import addon_auto_imports

bl_info = {   ###für export als addon
    "name" : "PuzzleUrPrint",
    "author" : "Modicolitor",
    "version" : (0,7),
    "blender" : (2, 82, 0),
    "location" : "View3D > Tools",
    "description" : "Cut your Objects into pieces and get Connectors to fit parts after Printing",
    "category" : "Object"}



#modules = addon_auto_imports.setup_addon_modules(
#    __path__, __name__, ignore_packages=[], ignore_modules=[]
#)


from bpy.types import Scene, Image, Object
from .ui import PP_PT_PuzzlePrintMenu 
#from .ui import PP_PT_PuzzlePrintActive
from .bun import PP_OT_AddSingleCoupling
from .bun import PP_OT_ExChangeCoup
from .bun import PP_OT_ApplyCoupling
from .bun import PP_OT_DeleteCoupling
from .bun import PP_OT_Ini
from .bun import PP_OT_MoveModDown
#from .bun import PP_OT_MoveModUp
from .gizmos import PP_OT_OversizeGizmo
from.gizmos import PUrP_OversizeGizmo
from.gizmos import PP_OT_CouplSizeGizmo
#from.gizmos import PUrP_CouplSizeGizmo

from .bun import PP_OT_ApplyAllCouplings
from .properties import PUrPropertyGroup



'''define the Centerobject and make it globally avaiable'''

#####Centerobj Pointer






    
classes = (PP_PT_PuzzlePrintMenu, 
            PP_OT_AddSingleCoupling,
            PP_OT_ExChangeCoup, 
            PP_OT_ApplyCoupling, 
            PP_OT_DeleteCoupling,
            PP_OT_Ini, 
            PP_OT_MoveModDown, 
           # PP_OT_MoveModUp, 
            PP_OT_OversizeGizmo, 
            PUrP_OversizeGizmo, 
            PP_OT_CouplSizeGizmo, 
            PP_OT_ApplyAllCouplings, 
            PUrPropertyGroup
            ) 
#classes = ()
register, unregister = bpy.utils.register_classes_factory(classes)
        



#if __name__ == "__main__":
#    register()            
            