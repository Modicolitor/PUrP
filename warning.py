import bpy


def noCutthroughWarn(self, context):
    self.layout.label(
        text="This Coupling didn't cut through!! Is this really what you want?")


def coneTrouble(self, context):
    self.layout.label(
        text="This seems to be impractical, but if you have a greater vision I won't stop you")


#bpy.context.window_manager.popup_menu(noCutthroughWarn, title="Error", icon='ERROR')
