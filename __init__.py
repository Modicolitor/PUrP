#
# Copyright (C) 2020 by Modicolitor
#
# This file is part of PuzzleUrPrint.
#
# License Text
#
# You should have received a copy of the GNU General Public License along with Power Sequencer. If
# not, see <https://www.gnu.org/licenses/>.

#from .gizmos import PP_OT_PlanarRoffsetGizmo
from .gizmos import PP_OT_BevelSegmentGizmo
from .gizmos import PP_OT_BevelOffsetGizmo
from .gizmos import PP_OT_zScaleGizmo
from .gizmos import PP_OT_PlanarRoffsetGizmo
from .gizmos import PP_OT_PlanarLoffsetGizmo
from .gizmos import PP_OT_PlanarzScaleGizmo
from .gizmos import PP_OT_PlanarStopperHeightGizmo
from .gizmos import PP_OT_CouplSizeGizmo
from .gizmos import PUrP_PlanarGizmo
from .gizmos import PUrP_SinglCoupGizmo
from .gizmos import PP_OT_OversizeGizmo
from .gizmos import PP_OT_PlanarLineCountGizmo
from .gizmos import PP_OT_PlanarLineLengthGizmo
from .gizmos import PP_OT_PlanarLineDistanceGizmo

from .gizmotshape import PUrP_CornerShapeWidget
from .gizmotshape import PUrP_ArrowShapeWidget
from .gizmotshape import PUrP_linecountShapeWidget
from .gizmotshape import PUrP_LineLengthShapeWidget
from .gizmotshape import PUrP_LineDistanceShapeWidget


from .ui import PP_PT_PuzzlePrintMenu
from .properties import PUrPropertyGroup
from .bun import PP_OT_ApplyAllCouplings

from .bun import PP_OT_CouplingOrder
from .bun import PP_OT_ActiveCoupDefaultOperator
from .bun import PP_OT_ToggleCoupVisibilityOperator
from .bun import PP_OT_MoveModUp
from .bun import PP_OT_MoveModDown
from .bun import PP_OT_Ini
from .bun import PP_OT_DeleteCoupling
from .bun import PP_OT_ApplyCoupling
from .bun import PP_OT_ExChangeCoup
from .bun import PP_OT_AddSingleCoupling
from .bun import PP_OT_ReMapCoups
from .bun import PP_OT_MakeBuildVolume
from .bun import PP_OT_ApplyPlanarMultiObj
from .bun import PP_OT_ApplyMultiplePlanarToObject
from .bvh_overlap import PP_OT_OverlapcheckOperator
from bpy.types import Scene, Image, Object
import bpy


from .utils import addon_auto_imports

bl_info = {  # für export als addon
    "name": "PuzzleUrPrint",
    "author": "Modicolitor",
    "version": (0, 7),
    "blender": (2, 82, 0),
    "location": "View3D > Tools",
    "description": "Cut your Objects into pieces and get Connectors to fit parts after Printing",
    "category": "Object"}

# modules = addon_auto_imports.setup_addon_modules(
#    __path__, __name__, ignore_packages=[], ignore_modules=[]
# )


#from .ui import PP_PT_PuzzlePrintActive
#from.gizmos import PUrP_CouplSizeGizmo


'''define the Centerobject and make it globally avaiable'''

# Centerobj Pointer


classes = (PP_PT_PuzzlePrintMenu,
           PP_OT_AddSingleCoupling,
           PP_OT_ExChangeCoup,
           PP_OT_ApplyCoupling,
           PP_OT_DeleteCoupling,
           PP_OT_Ini,
           PP_OT_MoveModDown,
           PP_OT_MoveModUp,
           PP_OT_ToggleCoupVisibilityOperator,
           PP_OT_ActiveCoupDefaultOperator,
           PP_OT_CouplingOrder,
           PP_OT_ReMapCoups,
           PP_OT_MakeBuildVolume,
           PP_OT_ApplyPlanarMultiObj,
           PP_OT_ApplyMultiplePlanarToObject,
           PP_OT_OversizeGizmo,
           PUrP_SinglCoupGizmo,
           PUrP_PlanarGizmo,
           PP_OT_CouplSizeGizmo,
           PP_OT_PlanarRoffsetGizmo,
           PP_OT_PlanarLoffsetGizmo,
           PP_OT_PlanarzScaleGizmo,
           PP_OT_PlanarStopperHeightGizmo,
           PP_OT_BevelOffsetGizmo,
           PP_OT_BevelSegmentGizmo,
           PP_OT_zScaleGizmo,
           PP_OT_PlanarLineLengthGizmo,
           PP_OT_PlanarLineDistanceGizmo,
           PUrP_CornerShapeWidget,
           PUrP_ArrowShapeWidget,
           PUrP_linecountShapeWidget,
           PUrP_LineLengthShapeWidget,
           PUrP_LineDistanceShapeWidget,
           PP_OT_PlanarLineCountGizmo,
           PP_OT_ApplyAllCouplings,
           PP_OT_OverlapcheckOperator,
           PUrPropertyGroup
           )
#classes = ()
register, unregister = bpy.utils.register_classes_factory(classes)

# if __name__ == "__main__":
#    register()
