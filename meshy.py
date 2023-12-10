import bpy

# Web url for text to texture
tttUrl = "https://api.meshy.ai/v1/text-to-texture"
taskList = []

# Get local api key
def get_api_key():
    user_preferences = bpy.context.preferences
    addon_preferences = user_preferences.addons["meshy-for-blender"].preferences
    return addon_preferences.api_key