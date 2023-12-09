import bpy
from . import MeshyTextToTexture

# The classes while will be registered
classes = (
    MeshyTextToTexture.MeshyTextToTexture,
    MeshyTextToTexture.SendSubmitRequest,
    MeshyTextToTexture.RefreshTaskList,
    MeshyTextToTexture.DownloadModel,
)

# The options of art style for text to texture 
ttt_artStyle = [
    ("realistic", "Realistic", ""),
    ("fake-3d-cartoon", "2.5D Cartoon", ""),
    ("cartoon-line-art", "Cartoon Line Art", ""),
    ("fake-3d-hand-drawn", "2.5D Hand-drawn", ""),
    ("japanese-anime", "Japanese Anime", ""),
    ("realistic-hand-drawn", "Realistic Hand-drawn", ""),
    ("oriental-comic-ink", "Oriental Comic Lnk", ""),
]


# Create value we will use in all of the windows
def CreateValue():

    # The value we will use in text to texture
    ############################################
    bpy.types.Scene.ttt_object_prompt = bpy.props.StringProperty(
        name="ttt_object_prompt",
        description="text_to_texture_object_prompt",
        default="",
    )

    bpy.types.Scene.ttt_style_prompt = bpy.props.StringProperty(
        name="ttt_style_prompt", description="text_to_texture_style_prompt", default=""
    )

    bpy.types.Scene.ttt_enable_original_UV = bpy.props.BoolProperty(
        name="ttt_enable_original_UV",
        description="text_to_texture_enable_original_UV",
        default=False,
    )

    bpy.types.Scene.ttt_enable_PBR = bpy.props.BoolProperty(
        name="ttt_enable_PBR", description="text_to_texture_enable_PBR", default=False
    )

    bpy.types.Scene.ttt_negative_prompt = bpy.props.StringProperty(
        name="ttt_negative_prompt",
        description="text_to_texture_negative_prompt",
        default="",
    )

    bpy.types.Scene.ttt_art_syle = bpy.props.EnumProperty(
        items=ttt_artStyle,
    )

    bpy.types.Scene.ttt_task_name = bpy.props.StringProperty(
        name="ttt_task_name",
        description="text_to_texture_task_name",
        default="Meshy_model",
    )
    ############################################


# Set the api key
class APIKeySetting(bpy.types.AddonPreferences):
    bl_idname = "meshy-for-blender"

    api_key: bpy.props.StringProperty(
        name="API Key", description="Enter your API key", default="", subtype="NONE"
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "api_key", full_event=True)


# Delete the value we have created
def DeleteValue():
    del bpy.types.Scene.ttt_object_prompt
    del bpy.types.Scene.ttt_style_prompt
    del bpy.types.Scene.ttt_enable_original_UV
    del bpy.types.Scene.ttt_enable_PBR
    del bpy.types.Scene.ttt_negative_prompt
    del bpy.types.Scene.ttt_art_syle
    del bpy.types.Scene.ttt_task_name


# This function will work while we star the plugin
def register():
    bpy.utils.register_class(APIKeySetting)
    for cls in classes:
        bpy.utils.register_class(cls)
    CreateValue()


# This function will work while we ban the plugin
def unregister():
    DeleteValue()
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    bpy.utils.unregister_class(APIKeySetting)
