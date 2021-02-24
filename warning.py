#
# Copyright (C) 2020 by Modicolitor
#
# This file is part of PuzzleUrPrint.
#
# License Text
#
# You should have received a copy of the GNU General Public License along with PuzzleUrPrint. If
# not, see <https://www.gnu.org/licenses/>.

import bpy


def noCutthroughWarn(self, context):
    self.layout.label(
        text="This Coupling didn't cut through!! Is this really what you want?")


def coneTrouble(self, context):
    self.layout.label(
        text="Using a Cone in a Stick Connector will not work! But maybe you have a greater vision...")


#bpy.context.window_manager.popup_menu(noCutthroughWarn, title="Error", icon='ERROR')
