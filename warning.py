import bpy

def noCutthroughWarn(self, context):
    self.layout.label(text="This Coupling didn't cut through!! Is this really what you want?")

#bpy.context.window_manager.popup_menu(noCutthroughWarn, title="Error", icon='ERROR')