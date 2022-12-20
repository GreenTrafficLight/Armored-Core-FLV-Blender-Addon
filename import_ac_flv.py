import bpy
import bmesh

import os

from math import *
from mathutils import *
from bpy_extras import image_utils

from .Utilities import *
from .Blender import*
from .Resources import *

def build_flv(data, filename):

    bpy.ops.object.add(type="ARMATURE")
    ob = bpy.context.object
    ob.name = str(filename)

    amt = ob.data
    amt.name = str(filename)

    empty_list = []

    mesh_index = 0

    for bone in data.bones:

        empty = add_empty(bone.name, ob, bone.translation, bone.rotation, bone.scale)

        #empty.matrix_world = bone.computeWorldTransform()

        if bone.parent_index != -1:

            empty.parent = empty_list[bone.parent_index]

        empty_list.append(empty)

    for flv_mesh in data.meshes:

        mesh = bpy.data.meshes.new(str(mesh_index))
        obj = bpy.data.objects.new(str(mesh_index), mesh)

        bpy.context.collection.objects.link(obj)

        obj.parent = ob

        vertexList = {}
        facesList = []
        normals = []

        last_vertex_count = 0

        bm = bmesh.new()
        bm.from_mesh(mesh)

        matrices = []
        for bone_indice in flv_mesh.bone_indices:

            if bone_indice != 65535:

                bone_matrix = Matrix.Identity(4)
                bone = data.bones[bone_indice]
                while True:
                    bone_matrix @= Matrix.Scale(1, 4, bone.scale) @ Matrix.Translation(bone.translation)
                    if bone.parent_index == -1:
                        matrices.append(bone_matrix)
                        break
                    bone = data.bones[bone.parent_index]

        # Set vertices
        for j in range(len(flv_mesh.vertices.positions)):

                transformation =  matrices[flv_mesh.vertices.bone_indices[j]] @ Matrix.Translation(flv_mesh.vertices.positions[j])
                vertex = bm.verts.new(transformation.translation)

                if flv_mesh.vertices.normals != []:
                    vertex.normal = flv_mesh.vertices.normals[j]
                    normals.append(flv_mesh.vertices.normals[j])
                
                vertex.index = last_vertex_count + j

                vertexList[last_vertex_count + j] = vertex

        faces = StripToTriangle(flv_mesh.vertex_indices)

        # Set faces
        for j in range(0, len(flv_mesh.vertex_indices)):
            try:
                face = bm.faces.new([vertexList[faces[j][0] + last_vertex_count], vertexList[faces[j][1] + last_vertex_count], vertexList[faces[j][2] + last_vertex_count]])
                face.smooth = True
                facesList.append([face, [vertexList[faces[j][0] + last_vertex_count], vertexList[faces[j][1] + last_vertex_count], vertexList[faces[j][2]] + last_vertex_count]])
            except:
                pass

        bm.to_mesh(mesh)
        bm.free()

        # Set normals
        mesh.use_auto_smooth = True

        """
        if normals != []:
            try:
                mesh.normals_split_custom_set_from_vertices(normals)
            except:
                pass
        """
        last_vertex_count += len(flv_mesh.vertices.positions)

        mesh_index += 1

    ob.rotation_euler = ( radians(90), 0, 0 )


def main(filepath, files, clear_scene):
    if clear_scene:
        clearScene()

    folder = (os.path.dirname(filepath))

    for i, j in enumerate(files):

        path_to_file = (os.path.join(folder, j.name))

        file = open(path_to_file, 'rb')
        filename =  path_to_file.split("\\")[-1]
        file_extension =  os.path.splitext(path_to_file)[1]
        file_size = os.path.getsize(path_to_file)

        br = BinaryReader(file, "<")
        if file_extension == ".flv":

            flver0 = FLVER0_CLASS()
            flver0.read(br)

            file.close()

            build_flv(flver0, filename)
        
                

    