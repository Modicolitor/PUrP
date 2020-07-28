import bpy


def noCutthroughWarn(self, context):
    self.layout.label(
        text="This Coupling didn't cut through!! Is this really what you want?")


def coneTrouble(self, context):
    self.layout.label(
        text="Using a Cone in a Stick Connector will not work! But maybe you have a greater vision...")


#bpy.context.window_manager.popup_menu(noCutthroughWarn, title="Error", icon='ERROR')
