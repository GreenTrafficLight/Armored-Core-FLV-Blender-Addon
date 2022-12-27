import bpy
import bmesh

import os

from math import *
from mathutils import *
from bpy_extras import image_utils

from .Utilities import *
from .Blender import*
from .Resources import *

def build_msb(data, filename):

    bpy.ops.object.add(type="ARMATURE")
    ob = bpy.context.object
    ob.name = str(filename)
    ob.rotation_euler = ( radians(90), 0, 0 )

    part_map_pieces_empty = add_empty("part_map_pieces", ob)

    for part_map_piece in data.parts.map_pieces:

        add_empty(part_map_piece.Name, part_map_pieces_empty, part_map_piece.Position, part_map_piece.Rotation, part_map_piece.Scale)

    part_objects_empty = add_empty("part_objects", ob)

    for part_object in data.parts.objects:

        add_empty(part_object.Name, part_objects_empty, part_object.Position, part_object.Rotation, part_object.Scale)

    part_enemies_empty = add_empty("part_enemies", ob)

    for part_enemy in data.parts.enemies:

        add_empty(part_enemy.Name, part_enemies_empty, part_enemy.Position, part_enemy.Rotation, part_enemy.Scale)



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
                    bone_matrix = bone.computeWorldTransform() @ bone_matrix
                    if bone.parent_index == -1:
                        matrices.append(bone_matrix)
                        break
                    bone = data.bones[bone.parent_index]

        # Set vertices
        for j in range(len(flv_mesh.vertices.positions)):

                if flv_mesh.vertices.bone_indices != []:
                    transformation =  matrices[flv_mesh.vertices.bone_indices[j]] @ Matrix.Translation(flv_mesh.vertices.positions[j])
                    vertex = bm.verts.new(transformation.translation)
                else:
                    vertex = bm.verts.new(flv_mesh.vertices.positions[j])

                if flv_mesh.vertices.normals != []:
                    vertex.normal = flv_mesh.vertices.normals[j]
                    normals.append(flv_mesh.vertices.normals[j])
                
                vertex.index = last_vertex_count + j

                vertexList[last_vertex_count + j] = vertex

        faces = StripToTriangle(flv_mesh.vertex_indices, True)
        #faces = StripToTriangle2(flv_mesh.vertex_indices, vertexList)

        # Set faces
        for j in range(0, len(flv_mesh.vertex_indices)):
            try:
                face = bm.faces.new([vertexList[faces[j][0] + last_vertex_count], vertexList[faces[j][1] + last_vertex_count], vertexList[faces[j][2] + last_vertex_count]])
                face.smooth = True
                facesList.append([face, [vertexList[faces[j][0] + last_vertex_count], vertexList[faces[j][1] + last_vertex_count], vertexList[faces[j][2]] + last_vertex_count]])
            except:
                pass

        if flv_mesh.vertices.uvs != []:

            uv_name = "UV1Map"
            uv_layer1 = bm.loops.layers.uv.get(uv_name) or bm.loops.layers.uv.new(uv_name)

            for f in bm.faces:
                for l in f.loops:
                    if l.vert.index >= last_vertex_count:
                        l[uv_layer1].uv = [flv_mesh.vertices.uvs[l.vert.index - last_vertex_count][0], 1 - flv_mesh.vertices.uvs[l.vert.index - last_vertex_count][1]]

        if flv_mesh.vertices.colors != []:

            color_name = "Color1Map"
            color_layer = bm.loops.layers.color.get(color_name) or bm.loops.layers.color.new(color_name)
            for f in bm.faces:
                for l in f.loops:
                    l[color_layer] = flv_mesh.vertices.colors[l.vert.index - last_vertex_count]


        bm.to_mesh(mesh)
        bm.free()

        # Set normals
        mesh.use_auto_smooth = True

        if normals != []:
            try:
                mesh.normals_split_custom_set_from_vertices(normals)
            except:
                pass

        # Set material
        flv_material = data.materials[flv_mesh.material_index]
        material = bpy.data.materials.get(flv_material.name)
        if not material:
            material = bpy.data.materials.new(flv_material.name)

        mesh.materials.append(material)

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
        
        elif file_extension == ".msb":

            msb = MSB1()
            br.endian = ">"
            msb.read(br)

            file.close()

            build_msb(msb, filename)
        
                

    