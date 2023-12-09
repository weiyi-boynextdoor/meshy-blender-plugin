import json
import bpy
import tempfile
from bpy.types import Context
import requests

# Web url for text to texture
tttUrl = "https://api.meshy.ai/v1/text-to-texture"
taskList = []

# Get local api key
def get_api_key():
    user_preferences = bpy.context.preferences
    addon_preferences = user_preferences.addons["meshy-for-blender"].preferences
    return addon_preferences.api_key


# Submit task
class SendSubmitRequest(bpy.types.Operator):
    bl_label = "Submit Task"
    bl_idname = "send.submit_request"

    def execute(self, context):
        if bpy.context.selected_objects.__len__()==0:
            self.report(type={'ERROR'},message = "No selected objects!")
            return {"FINISHED"}
        
        if context.scene.ttt_object_prompt == "" or context.scene.ttt_object_prompt== None:
            self.report(type={'ERROR'},message = "Object prompt can not be empty!")
            return {"FINISHED"}
        
        if context.scene.ttt_style_prompt == "" or context.scene.ttt_object_prompt== None:
            self.report(type={'ERROR'},message = "Style prompt can not be empty!")
            return {"FINISHED"}
        
        fp = tempfile.NamedTemporaryFile(suffix=".glb")
        bpy.ops.export_scene.gltf(filepath=fp.name, use_selection=True)

        postData = {
            "object_prompt": context.scene.ttt_object_prompt,
            "style_prompt": context.scene.ttt_style_prompt,
            "enable_original_uv": context.scene.ttt_enable_original_UV,
            "enable_pbr": context.scene.ttt_enable_PBR,
            "negative_prompt": context.scene.ttt_negative_prompt,
            "art_style": context.scene.ttt_art_syle,
            "name": context.scene.ttt_task_name,
        }

        headers = {"Authorization": f"Bearer {get_api_key()}"}

        response = requests.post(
            tttUrl,
            files={
                "model_file": (
                    context.scene.ttt_task_name + ".glb",
                    open(fp.name, "rb"),
                )
            },
            headers=headers,
            data=postData,
        )
        fp.close()
        
        response.raise_for_status()
        self.report({'INFO'},response.text)
        json_res = response.json()
        print(json_res)
        return {"FINISHED"}


# Refresh task list
class RefreshTaskList(bpy.types.Operator):
    bl_label = "Refresh Task List"
    bl_idname = "send.refresh_task_list"

    def refreshOnePage(self, context):
        headers = {"Authorization": f"Bearer {get_api_key()}"}

        response = requests.get(tttUrl + "?sortBy=-created_at", headers=headers)

        response.raise_for_status()

        if response.text != "[]":
            taskList.append(json.loads(response.text))
            self.report(type={'INFO'},message="Refreshing completed.")

    def execute(self, context):
        taskList.clear()
        self.refreshOnePage(context)
        return {"FINISHED"}


# Download the model
class DownloadModel(bpy.types.Operator):
    bl_label = "Download Model"
    bl_idname = "send.download_model"
    downloadPath: bpy.props.StringProperty(name="download path", default="")

    def execute(self, context):
        req = requests.get(self.downloadPath)
        fp = tempfile.NamedTemporaryFile(suffix=".glb")
        fp.write(req.content)
        bpy.ops.import_scene.gltf(filepath=fp.name)
        fp.close()
        bpy.context.active_object.scale = (1,1,1)
        bpy.context.active_object.location = (0,0,0)
        bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY")
        return {"FINISHED"}


# Create text to texture GUI
class MeshyTextToTexture(bpy.types.Panel):
    bl_idname = "MESHY_TEXT_TO_TEXTURE"
    bl_label = "Text To Texture"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Meshy"

    # Draw the panel UI
    def draw(self, context):
        layout = self.layout
        column = layout.column()
        column.label(text="Object Prompt:")
        column.prop(context.scene, "ttt_object_prompt", text="")
        column.label(text="Style Prompt:")
        column.prop(context.scene, "ttt_style_prompt", text="")
        column.prop(context.scene, "ttt_enable_original_UV", text="Enable Orginal UV")
        column.prop(context.scene, "ttt_enable_PBR", text="Enable PBR")
        column.label(text="Negative Prompt:")
        column.prop(context.scene, "ttt_negative_prompt", text="")
        column.label(text="Task Name:")
        column.prop(context.scene, "ttt_task_name", text="")
        column.label(text="Art Style:")
        column.prop(context.scene, "ttt_art_syle", text="")
        column.operator(SendSubmitRequest.bl_idname, text="Submit Task")
        column.operator(RefreshTaskList.bl_idname, text="Refresh Task List")
        split = layout.split()
        col = split.column()
        col.label(text="Download")
        for indexA in taskList:
            for indexB in indexA:
                if indexB["status"] == "SUCCEEDED":
                    downloadButton = col.operator(
                        DownloadModel.bl_idname, text="Download"
                    )
                    downloadButton.downloadPath = indexB["model_url"]
                else:
                    col.label(text=" ")
        col = split.column()
        col.label(text="Task Name")
        for indexA in taskList:
            for indexB in indexA:
                if (
                    indexB["status"] == "SUCCEEDED"
                    or indexB["status"] == "FAILED"
                    or indexB["status"] == "PENDING"
                    or indexB["status"] == "IN_PROGRESS"
                ):
                    col.label(text=indexB["name"])
        col = split.column()
        col.label(text="Progress")
        for indexA in taskList:
            for indexB in indexA:
                if (
                    indexB["status"] == "SUCCEEDED"
                    or indexB["status"] == "FAILED"
                    or indexB["status"] == "PENDING"
                    or indexB["status"] == "IN_PROGRESS"
                ):
                    col.label(text=str(indexB["progress"]))
        col = split.column()
        col.label(text="Art Style")
        for indexA in taskList:
            for indexB in indexA:
                if (
                    indexB["status"] == "SUCCEEDED"
                    or indexB["status"] == "FAILED"
                    or indexB["status"] == "PENDING"
                    or indexB["status"] == "IN_PROGRESS"
                ):
                    col.label(text=indexB["art_style"])
        col = split.column()
        col.label(text="Status")
        for indexA in taskList:
            for indexB in indexA:
                if (
                    indexB["status"] == "SUCCEEDED"
                    or indexB["status"] == "FAILED"
                    or indexB["status"] == "PENDING"
                    or indexB["status"] == "IN_PROGRESS"
                ):
                    col.label(text=indexB["status"])
