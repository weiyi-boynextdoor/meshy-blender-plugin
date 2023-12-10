import bpy
import tempfile
import requests
import os
import json
from .. import meshy

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

        temp_dir = tempfile.TemporaryDirectory()
        temp_file_path = os.path.join(temp_dir.name, "temp.glb")
        bpy.ops.export_scene.gltf(filepath=temp_file_path, use_selection=True)

        postData = {
            "object_prompt": context.scene.ttt_object_prompt,
            "style_prompt": context.scene.ttt_style_prompt,
            "enable_original_uv": context.scene.ttt_enable_original_UV,
            "enable_pbr": context.scene.ttt_enable_PBR,
            "negative_prompt": context.scene.ttt_negative_prompt,
            "art_style": context.scene.ttt_art_syle,
            "name": context.scene.ttt_task_name,
        }

        headers = {"Authorization": f"Bearer {meshy.get_api_key()}"}

        response = requests.post(
            meshy.tttUrl,
            files={
                "model_file": (
                    context.scene.ttt_task_name + ".glb",
                    open(temp_file_path, "rb"),
                )
            },
            headers=headers,
            data=postData,
        )

        temp_dir.cleanup()

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
        headers = {"Authorization": f"Bearer {meshy.get_api_key()}"}

        response = requests.get(meshy.tttUrl + "?sortBy=-created_at", headers=headers)

        response.raise_for_status()

        if response.text != "[]":
            meshy.taskList.append(json.loads(response.text))
            self.report(type={'INFO'},message="Refreshing completed.")

    def execute(self, context):
        meshy.taskList.clear()
        self.refreshOnePage(context)
        return {"FINISHED"}

# Download the model
class DownloadModel(bpy.types.Operator):
    bl_label = "Download Model"
    bl_idname = "send.download_model"
    downloadPath: bpy.props.StringProperty(name="download path", default="")

    def execute(self, context):
        req = requests.get(self.downloadPath)
        temp_dir = tempfile.TemporaryDirectory()
        temp_file_path = os.path.join(temp_dir.name, "temp.glb")
        with open(temp_file_path, "wb") as f:
            f.write(req.content)
        bpy.ops.import_scene.gltf(filepath=temp_file_path)
        temp_dir.cleanup()
        bpy.context.active_object.scale = (1,1,1)
        bpy.context.active_object.location = (0,0,0)
        bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY")
        return {"FINISHED"}