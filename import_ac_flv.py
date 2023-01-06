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

    armature = ob.data
    armature.name = str(filename)

    mesh_index = 0

    bone_mapping = []


    for flver_bone in data.bones:

        bone_mapping.append(flver_bone.name)

        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bone = armature.edit_bones.new(flver_bone.name)

        bone.head = (0, 0, 0)
        bone.tail = (0, 0, 1)
        
        bone.matrix = flver_bone.computeWorldTransform()

        if flver_bone.parent_index != -1:

            parent = data.bones[flver_bone.parent_index]

            bone.parent = armature.edit_bones[parent.name]
            bone.matrix = armature.edit_bones[parent.name].matrix @ bone.matrix

    bones = armature.edit_bones
    for flver_bone in data.bones:

        bone = bones[flver_bone.name]

        if flver_bone.parent_index != -1:

            parent = data.bones[flver_bone.parent_index]
            
            bone.tail = bones[parent.name].head

    bpy.ops.object.mode_set(mode='OBJECT')

    for flv_mesh in data.meshes:

        mesh = bpy.data.meshes.new(str(mesh_index))
        obj = bpy.data.objects.new(str(mesh_index), mesh)

        bpy.context.collection.objects.link(obj)

        modifier = obj.modifiers.new(armature.name, type="ARMATURE")
        modifier.object = ob

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

                bone = data.bones[bone_indice]
                if not bone.name in obj.vertex_groups:
                     obj.vertex_groups.new(name=bone.name)

                bone_matrix = Matrix.Identity(4)
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

        for i in range(len(flv_mesh.vertices.positions)):
            if flv_mesh.vertices.bone_indices != []:
                vg_name = bone_mapping[flv_mesh.bone_indices[flv_mesh.vertices.bone_indices[i]]]
                group = obj.vertex_groups[vg_name]
                weight = 1.0
                if weight > 0.0:
                    group.add([i], weight, 'REPLACE')



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


def build_ani(data, filename):

    bpy.ops.object.add(type="ARMATURE")
    ob = bpy.context.object
    ob.name = str(filename)

    armature = ob.data
    armature.name = str(filename)

    mesh_index = 0

    bone_mapping = []


    for flver_bone in data.bones:

        bone_mapping.append(flver_bone.name)

        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bone = armature.edit_bones.new(flver_bone.name)

        bone.head = (0, 0, 0)
        bone.tail = (0, 0, 1)
        
        bone.matrix = flver_bone.computeWorldTransform()

        if flver_bone.parent_index != -1:

            parent = data.bones[flver_bone.parent_index]

            bone.parent = armature.edit_bones[parent.name]
            bone.matrix = armature.edit_bones[parent.name].matrix @ bone.matrix

    bones = armature.edit_bones
    for flver_bone in data.bones:

        bone = bones[flver_bone.name]

        if flver_bone.parent_index != -1:

            parent = data.bones[flver_bone.parent_index]
            
            bone.tail = bones[parent.name].head

    bpy.ops.object.mode_set(mode='OBJECT')

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

        elif file_extension == ".ani":

            ani = ANI_CLASS()
            br.endian = ">"
            ani.read(br)

            file.close()

            build_ani(ani, filename)
        
                

    