import json
import bpy
import tempfile
from bpy.types import Context
import requests
import os
from . import Operators
from .. import meshy

# Create text to texture GUI
class MeshyTextToTexture(bpy.types.Panel):
    bl_idname = "MESHY_PT_TEXT_TO_TEXTURE"
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
        column.operator(Operators.TTTSendSubmitRequest.bl_idname, text="Submit Task")
        column.operator(Operators.TTTRefreshTaskList.bl_idname, text="Refresh Task List")
        split = layout.split()
        col = split.column()
        col.label(text="Download")
        for indexA in bpy.types.Scene.task_list:
            for indexB in indexA:
                if indexB["status"] == "SUCCEEDED":
                    downloadButton = col.operator(
                        Operators.DownloadModel.bl_idname, text="Download"
                    )
                    downloadButton.downloadPath = indexB["model_url"]
                else:
                    col.label(text=" ")
        col = split.column()
        col.label(text="Task Name")
        for indexA in bpy.types.Scene.task_list:
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
        for indexA in bpy.types.Scene.task_list:
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
        for indexA in bpy.types.Scene.task_list:
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
        for indexA in bpy.types.Scene.task_list:
            for indexB in indexA:
                if (
                    indexB["status"] == "SUCCEEDED"
                    or indexB["status"] == "FAILED"
                    or indexB["status"] == "PENDING"
                    or indexB["status"] == "IN_PROGRESS"
                ):
                    col.label(text=indexB["status"])

class MeshyTextToModel(bpy.types.Panel):
    bl_idname = "MESHY_PT_TEXT_TO_MODEL"
    bl_label = "Text To Model"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Meshy"

    # Draw the panel UI
    def draw(self, context):
        layout = self.layout
        column = layout.column()
        column.label(text="Object Prompt:")
        column.prop(context.scene, "ttm_object_prompt", text="")
        column.label(text="Style Prompt:")
        column.prop(context.scene, "ttm_style_prompt", text="")
        column.prop(context.scene, "ttm_enable_PBR", text="Enable PBR")
        column.prop(context.scene, "ttm_resolution", text="Resolution")
        column.label(text="Negative Prompt:")
        column.prop(context.scene, "ttm_negative_prompt", text="")
        column.label(text="Task Name:")
        column.prop(context.scene, "ttm_task_name", text="")
        column.label(text="Art Style:")
        column.prop(context.scene, "ttm_art_syle", text="")
        column.operator(Operators.TTMSendSubmitRequest.bl_idname, text="Submit Task")
        column.operator(Operators.TTMRefreshTaskList.bl_idname, text="Refresh Task List")
        split = layout.split()
        col = split.column()
        col.label(text="Download")
        for indexA in bpy.types.Scene.task_list:
            for indexB in indexA:
                if indexB["status"] == "SUCCEEDED":
                    downloadButton = col.operator(
                        Operators.DownloadModel.bl_idname, text="Download"
                    )
                    downloadButton.downloadPath = indexB["model_url"]
                else:
                    col.label(text=" ")
        col = split.column()
        col.label(text="Task Name")
        for indexA in bpy.types.Scene.task_list:
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
        for indexA in bpy.types.Scene.task_list:
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
        for indexA in bpy.types.Scene.task_list:
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
        for indexA in bpy.types.Scene.task_list:
            for indexB in indexA:
                if (
                    indexB["status"] == "SUCCEEDED"
                    or indexB["status"] == "FAILED"
                    or indexB["status"] == "PENDING"
                    or indexB["status"] == "IN_PROGRESS"
                ):
                    col.label(text=indexB["status"])
