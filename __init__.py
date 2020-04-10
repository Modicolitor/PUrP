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
    "version" : (0,6),
    "blender" : (2, 82, 0),
    "location" : "View3D > Tools",
    "description" : "Cut your Objects into pieces and get Connectors to fit parts after Printing",
    "category" : "Object"}



modules = addon_auto_imports.setup_addon_modules(
    __path__, __name__, ignore_packages=[], ignore_modules=[]
)



#from files.PUrP_a5 import classes
from .files import *
#from .operators import classes



    
#classes = (PP_PT_PuzzlePrintMenu,PP_OT_AddSingleCoupling,PP_OT_ApplyCoupling,PP_OT_DeleteCoupling) 
#classes = ()
register, unregister = bpy.utils.register_classes_factory(classes)
        



#if __name__ == "__main__":
#    register()            
            