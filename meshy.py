import bpy

# Web url for text to texture
ttt_url = "https://api.meshy.ai/v1/text-to-texture"

# Web url for text to model
ttm_url = "https://api.meshy.ai/v1/text-to-3d"


# Get local api key
def get_api_key():
    user_preferences = bpy.context.preferences
    addon_preferences = user_preferences.addons["meshy-for-blender"].preferences
    return addon_preferences.api_key
