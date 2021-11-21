 # This script uses bmesh operators to make 2 links of a chain.

import bpy
import bmesh
import numpy as np
from bmesh.types import BMVert, BMEdge
import math
import mathutils
from multiprocessing import Process, Manager
import os
from random import randint, choice

# L-System Settings
ITERATIONS = 3

def processString(word):
  newstr = ''
  for character in word:
    newstr = newstr + applyRules(character)
    
  return newstr
  
def applyRules(character):

    newstr = ''
    
    if character == 'F':
        newstr = 'FF'
      #newstr = 'F[+FL]F[-FL]F'
    elif character == 'X':
        #rand = randint(0,1)
        #if rand == 0:
        #    newstr = 'F-[[X]+X]+F[+FX]-X'
        #elif rand == 1:
        #    newstr = 'F+[[X]-X]-F[-FX]+X'
        newstr = 'F[+X][-X]FX'
    else:
      newstr = character
    
    return newstr
 
 
def wordCleaner(word):
    word = word.replace('X', '')
    word = word.replace('[+]', '')
    word = word.replace('[-]', '')
    return word
"""
def replacer(word):
    rotators = ['/','\\','&','^', '+', '-']
    newstr = ''
    
    for i in range(0, len(word)):
        if word[i] == '+' or word[i] ==  '-':
            #rand = randint(0,3)
            #if rand == 1 or rand == 2:
            
            c = choice(rotators)
            newstr += c
            #else:
                #print(word[i])
            #    newstr += word[i]
        else:
            newstr += word[i]

    return newstr
"""
def replacer(word):
    rotators = ['/','\\','&','^']
    newstr = ''
    
    for i in range(0, len(word)):
        if word[i] == '+' or word[i] ==  '-':
             c = rotators[randint(0, 3)]
             newstr += c
        else:
            #print(word[i])
            newstr += word[i]
#   print(newstr)
    return newstr

def createSystem(iters, axiom):
  startString = axiom
  endString = ''
  
  for i in range(iters):
    endString = processString(startString)
    startString = endString
  return endString

def createTree(word, angle, distance):
    # Convert angle to radians
    angle = math.radians(angle)
    # Set center point location
    center = [0,0,0]
    # Create stack for push action
    stack = []
    # Set current heading
    heading = mathutils.Vector([0,0,distance]).normalized()
    
    # Set rotation matrix
    rotationMat = mathutils.Matrix()

    # Make a new BMesh
    bm = bmesh.new()
    # Create first Vertex
    vertex = bmesh.ops.create_vert(bm, co = center)['vert'][0]
    # Create leaf list
    #leaf = []
    # is in stack
    inStack = False
    # Max of steps
    max = len(word)
    index = 0
    # Loop throught the L-System word
    for char in word:
        print(char)
  
        #Progress
        print(str(index) + '/' + str(max))
        index += 1
        # Move forward and create a mesh cell
        if char == 'F':   
            # Extrude the marked edges
            vertex = bmesh.ops.extrude_vert_indiv(bm, verts = [vertex])
            edge = vertex['edges']
            vertex = vertex['verts'][0]
            # Move selecte vertices forward
            bmesh.ops.translate(bm, vec=heading, verts=[vertex])   
            # set current center
            center = vertex.co
            
      
        # Turn left
        elif char == '+':
            #rotationMat = [[math.cos(angle), -math.sin(angle), 0],
            #                [math.sin(angle), math.cos(angle), 0],
            #                [0, 0, 1]]
            # Set the rotation matrix
            rotationMat = mathutils.Matrix.Rotation(angle, 3, 'Z')
            # Duplicate and rotate selected edges
            tmpRotation = rotateEdges(bm, heading, rotationMat, vertex, edge, inStack)
            # Update selected edges and their center
            vertex, center, heading, inStack = tmpRotation[0], tmpRotation[1], tmpRotation[2], tmpRotation[3]
            
          
        # Turn right
        elif char == '-':
            #rotationMat = [[-math.cos(angle), math.sin(angle), 0],
            #                [-math.sin(angle), -math.cos(angle), 0],
            #                [0, 0, 1]]
            rotationMat = mathutils.Matrix.Rotation(-angle, 3, 'Z')
            # Duplicate and rotate selected edges
            tmpRotation = rotateEdges(bm, heading, rotationMat, vertex, edge, inStack)
            # Update selected edges and their center
            vertex, center, heading, inStack = tmpRotation[0], tmpRotation[1], tmpRotation[2], tmpRotation[3]
            
        # Pitch down
        elif char == '&':
           
            
            rotationMat = mathutils.Matrix.Rotation(angle, 3, 'Y')
            # Duplicate and rotate selected edges
            tmpRotation = rotateEdges(bm, heading, rotationMat, vertex, edge, inStack)
            # Update selected edges and their center
            vertex, center, heading, inStack = tmpRotation[0], tmpRotation[1], tmpRotation[2], tmpRotation[3]
            
        # pitch up
        elif char == '^':
            #rotationMat = [[-math.cos(angle), 0, -math.sin(angle)],
            #                [0, 1, 0],
            #                [math.sin(angle), 0, -math.cos(angle)]]
            rotationMat = mathutils.Matrix.Rotation(-angle, 3, 'Y')
            # Duplicate and rotate selected edges
            tmpRotation = rotateEdges(bm, heading, rotationMat, vertex, edge, inStack)
            # Update selected edges and their center
            vertex, center, heading, inStack = tmpRotation[0], tmpRotation[1], tmpRotation[2], tmpRotation[3]
                
        # Roll left (\)
        elif char == '\\':
            #rotationMat = [[1, 0, 0],
            #                [0, math.cos(angle), math.sin(angle)],
            #                [0, -math.sin(angle), math.cos(angle)]]
            rotationMat = mathutils.Matrix.Rotation(angle, 3, 'X')
            # Duplicate and rotate selected edges
            tmpRotation = rotateEdges(bm, heading, rotationMat, vertex, edge, inStack)
            # Update selected edges and their center
            vertex, center, heading, inStack = tmpRotation[0], tmpRotation[1], tmpRotation[2], tmpRotation[3]
            
        # Roll right
        elif char == '/':
            #rotationMat = [[1, 0, 0],
            #                [0, -math.cos(angle), -math.sin(angle)],
            #                [0, math.sin(angle), -math.cos(angle)]]
            rotationMat = mathutils.Matrix.Rotation(-angle, 3, 'X')
            # Duplicate and rotate selected edges
            tmpRotation = rotateEdges(bm, heading, rotationMat, vertex, edge, inStack)
            # Update selected edges and their center
            vertex, center, heading, inStack = tmpRotation[0], tmpRotation[1], tmpRotation[2], tmpRotation[3]
            
                   
        # Push
        elif char == '[': 
            stack.append((vertex, (heading.x, heading.y, heading.z), center))
            inStack = True
        # Pop
        elif char == ']':
            #l = bmesh.ops.create_vert(bm, co = center)
            #leaf.append(l)
            vertex, tmpheading, center = stack.pop()
            inStack = False
    
    # Remove doubles
    bmesh.ops.remove_doubles(bm, verts = bm.verts, dist = 0.0001)
    # Finish up, write the bmesh into a new mesh
    me = bpy.data.meshes.new("Mesh")
    # Create a mesh from bmesh
    bm.to_mesh(me)
    # Free memory allocated by bmesh
    bm.free()

    # Create an object of the mesh
    obj = bpy.data.objects.new("Object", me)
    
    # Add object to the scene collection
    bpy.context.collection.objects.link(obj)

    # Select and make active
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    
    # Add skin modifier
    skin = obj.modifiers.new(name='Skin', type='SKIN')
    skin.branch_smoothing = 1
    skin.use_x_symmetry = False
    # Go to edit mode
    bpy.ops.object.editmode_toggle()
    # Select all vertices
    bpy.ops.mesh.select_all(action='SELECT')
  
    # Deselect all vertices
    bpy.ops.mesh.select_all(action='DESELECT')
    # Go to object  mode
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    
    # Select the first vertex (bottom one)
    obj.data.vertices[0].select = True
    # Go to edit mode
    bpy.ops.object.mode_set(mode = 'EDIT')
    # Scle skin size proportionally form bottom vertex
    bpy.ops.transform.skin_resize(value=( ITERATIONS, ITERATIONS, ITERATIONS), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=True, proportional_edit_falloff='ROOT', proportional_size=2 * ITERATIONS, use_proportional_connected=False, use_proportional_projected=False)
    # Go to object mode
    bpy.ops.object.mode_set(mode = 'OBJECT')
    # Deselct first vertex
    obj.data.vertices[0].select = False
    # Select last vertex
    obj.data.vertices[-1].select = True
    # Go to Edit mode
    bpy.ops.object.mode_set(mode = 'EDIT')
    # Scle skin size proportionally form top vertex
    bpy.ops.transform.skin_resize(value=(0.09 * ITERATIONS, 0.09 * ITERATIONS, 0.09 * ITERATIONS), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=True, proportional_edit_falloff='ROOT', proportional_size=2 *  ITERATIONS, use_proportional_connected=False, use_proportional_projected=False)
    
    # Add Bevel modifier
    bevel = obj.modifiers.new(name='Bevel', type='BEVEL')
    # Set bevel effect on vertices
    bevel.affect = 'VERTICES'
    # Increase bevel segments
    bevel.segments = 2
    # Add subdivision surface modifier
    subdivision = obj.modifiers.new(name='Subdivision', type='SUBSURF')
    # Set subdivision type to simple
    subdivision.subdivision_type = 'SIMPLE'

    
    # Add smooth corrective modifier
    smoothcor = obj.modifiers.new(name='CorrectiveSmooth', type='CORRECTIVE_SMOOTH')
    # Set smooth modifier to use only smooth
    smoothcor.use_only_smooth = True
    # Set smooth modifier to use pin boundaries
    smoothcor.use_pin_boundary = True
    # Go to object mode
    bpy.ops.object.mode_set(mode = 'OBJECT')
    # Add Material to object
    # Check if the material is in the file
    if 'TreeBody' in bpy.data.materials.keys():
        # If so append it to the object
        obj.data.materials.append(bpy.data.materials['TreeBody'])
    else:
        # if not append it from materials file to this file
        # Set the filepath
        filepath = os.path.dirname(bpy.data.filepath) + '\Materials\Materials.blend'
        # Set the directory
        directory = os.path.dirname(bpy.data.filepath) + '\\Materials'
        # Append the material to this file
        bpy.ops.wm.append(filepath=filepath, directory = directory, filename='Materials.blend\\Material\TreeBody')        
        # Append the material to the object
        obj.data.materials.append(bpy.data.materials['TreeBody'])
        
def rotateEdges(bm, heading, rotationMat, vertex, edge, inStack):
    
    
    if inStack:
        
        #Duplicate selected edges
        #vertex = bmesh.ops.duplicate(bm, geom = [vertex])['geom'][0]
        vertex = bmesh.ops.extrude_vert_indiv(bm, verts = [vertex])
        edge = vertex['edges']
        vertex = vertex['verts'][0]
        inStack = False
    if vertex == None:
        center = [0,0,0]
    else:
        # Calculate current center
        center = vertex.co
    # Rotate the edge      
    print(edge[0].verts) 
    bmesh.ops.rotate(bm, cent = edge[0].verts[0].co, matrix = rotationMat, verts = edge[0].verts)
    
    # Update heading vector
   
    heading.rotate(rotationMat)
    vertex.normal_update()
    return vertex, center, heading.normalized(), inStack

def main():
    # Create L-system
    word = createSystem(ITERATIONS, 'X')
    # Clean up the word
    word = wordCleaner(word)
    # Add 3d rotations to the word
    word = replacer(word)
    print(word)
    angle = 25.7
    distance = 0.5
    createTree(word, angle, distance)
    
if __name__ == "__main__":
    main()