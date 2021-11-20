# This script uses bmesh operators to make 2 links of a chain.

import bpy
import bmesh
import numpy as np
from bmesh.types import BMVert, BMEdge
import math
import mathutils
from multiprocessing import Process, Manager
import os
from random import randint

def processString(word):
  newstr = ''
  for character in word:
    newstr = newstr + applyRules(character)
    
  return newstr
  
def applyRules(character):

    #newstr = ''
    #if character == 'A':
    #    newstr = 'B-F+CFC+F-D&F∧D-F+&&CFC+F+B//'
    #elif character == 'B':
    #    newstr = 'A&F∧CFB∧F∧D∧∧-F-D∧|F∧B|FC∧F∧A//'
    #elif character == 'C':
    #    newstr = '|D∧|F∧B-F+C∧F∧A&&FA&F∧C+F+B∧F∧D//'
    #elif character == 'D':
    #    newstr = '|CFB-F+B|FA&F∧A&&FB-F+B|FC//'
    #else:
    #    newstr = ''
    #return newstr
    newstr = ''
    #if character == 'F':
    #    newstr = 'S/////F'
    #elif character == 'A':
    #    newstr = '[&FL!A]/////’[&FL!A]///////’[&FL!A]'
    #elif character == 'S':
    #    newstr = 'FL'
    #else:
    newstr = character
    
    if character == 'F':
        newstr = 'FF'
      #newstr = 'F[+FL]F[-FL]F'
    elif character == 'X':
        rand = randint(0,1)
        if rand == 0:
            newstr = 'F-[[X]+X]+F[+FX]-X'
        elif rand == 1:
            newstr = 'F+[[X]-X]-F[-FX]+X'
        #newstr = 'F[+X][-X]FX'
    else:
      newstr = character
    
    return newstr
 
 
def wordCleaner(word):
    word = word.replace('X', '')
    word = word.replace('[+]', '')
    word = word.replace('[-]', '')
    return word
 
def replacer(word):
    rotators = ['/','\\','&','^']
    newstr = ''
    
    for i in range(0, len(word)):
        rand = randint(0,2)
        if rand == 1 or rand == 2:
            if word[i] == '+' or word[i] ==  '-':
                 c = rotators[randint(0, 3)]
                 newstr += c
            else:
                #print(word[i])
                newstr += word[i]
        else:
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
    heading = mathutils.Vector([0,0,distance])
    
    # Set rotation matrix
    rotationMat = mathutils.Matrix()

    # Make a new BMesh
    bm = bmesh.new()
    
    vertex = bmesh.ops.create_vert(bm, co = center)['vert'][0]
    # Select current edges 
    

    # is in stack
    inStack = False
    
    max = len(word)
    index = 0
    # Loop throught the L-System word
    for char in word:
        print(str(index) + '/' + str(max))
        #print(len(stack))
        index += 1
        #print(leafRot)
        # Move forward and create a mesh cell
        if char == 'F':   
            # Extrude the marked edges
            vertex = bmesh.ops.extrude_vert_indiv(bm, verts = [vertex])['verts'][0]
            
            
            
           
            
            # Move selecte vertices forward
            bmesh.ops.translate(bm, vec=heading, verts=[vertex])
          
           
            # Create the scale vector based on the heading vector
            #scaleVec = [diameter / prevDiameter for i in range(0,3)]
            # Scale the edge loop
            #bmesh.ops.scale(bm, vec = scaleVec, verts = tmpVerts)
            # Update previous diameter
            #prevDiameter = diameter
            # Get raw vertices
            #rawVerts = [v.co for v in tmpVerts]
             # Calculate current center
            center = vertex.co
            

            
        # Turn left
        elif char == '+':
            #rotationMat = [[math.cos(angle), -math.sin(angle), 0],
            #                [math.sin(angle), math.cos(angle), 0],
            #                [0, 0, 1]]
            # Set the rotation matrix
            rotationMat = mathutils.Matrix.Rotation(angle, 3, 'Z')
            
            #print(mathutils.Matrix.Rotation(angle, 3, 'Z'))
            #print(mathutils.Matrix.Rotation(angle, 3, 'X') @ mathutils.Matrix.Rotation(angle, 3, 'Y')) 
            # Duplicate and rotate selected edges
            tmpRotation = rotateEdges(bm, heading, rotationMat, vertex, inStack)
            # Update selected edges and their center
            vertex, center, heading, inStack = tmpRotation[0], tmpRotation[1], tmpRotation[2], tmpRotation[3]
            
          
        # Turn right
        elif char == '-':
            #rotationMat = [[-math.cos(angle), math.sin(angle), 0],
            #                [-math.sin(angle), -math.cos(angle), 0],
            #                [0, 0, 1]]
            rotationMat = mathutils.Matrix.Rotation(-angle, 3, 'Z')
            #leafRot.rotate_axis('Y', -angle)
            
            # Duplicate and rotate selected edges
            tmpRotation = rotateEdges(bm, heading, rotationMat, vertex, inStack)
            # Update selected edges and their center
            vertex, center, heading, inStack = tmpRotation[0], tmpRotation[1], tmpRotation[2], tmpRotation[3]
            
        # Pitch down
        elif char == '&':
           
            
            rotationMat = mathutils.Matrix.Rotation(angle, 3, 'Y')
            
            #leafRot.rotate_axis('Z', -angle)
            # Duplicate and rotate selected edges
            tmpRotation = rotateEdges(bm, heading, rotationMat, vertex, inStack)
            # Update selected edges and their center
            vertex, center, heading, inStack = tmpRotation[0], tmpRotation[1], tmpRotation[2], tmpRotation[3]
            
        # pitch up
        elif char == '^':
            #rotationMat = [[-math.cos(angle), 0, -math.sin(angle)],
            #                [0, 1, 0],
            #                [math.sin(angle), 0, -math.cos(angle)]]
            rotationMat = mathutils.Matrix.Rotation(-angle, 3, 'Y')
            
            #leafRot.rotate_axis('Z', angle)
            # Duplicate and rotate selected edges
            tmpRotation = rotateEdges(bm, heading, rotationMat, vertex, inStack)
            # Update selected edges and their center
            vertex, center, heading, inStack = tmpRotation[0], tmpRotation[1], tmpRotation[2], tmpRotation[3]
                
        # Roll left (\)
        elif char == '\\':
            #rotationMat = [[1, 0, 0],
            #                [0, math.cos(angle), math.sin(angle)],
            #                [0, -math.sin(angle), math.cos(angle)]]
            rotationMat = mathutils.Matrix.Rotation(angle, 3, 'X')
            
            #leafRot.rotate_axis('X', angle)
            # Duplicate and rotate selected edges
            tmpRotation = rotateEdges(bm, heading, rotationMat, vertex, inStack)
            # Update selected edges and their center
            vertex, center, heading, inStack = tmpRotation[0], tmpRotation[1], tmpRotation[2], tmpRotation[3]
            
        # Roll right
        elif char == '/':
            #rotationMat = [[1, 0, 0],
            #                [0, -math.cos(angle), -math.sin(angle)],
            #                [0, math.sin(angle), -math.cos(angle)]]
            rotationMat = mathutils.Matrix.Rotation(-angle, 3, 'X')
            
            #leafRot = leafRot @ rotationMat
            #leafRot.rotate_axis('X', -angle)
            # Duplicate and rotate selected edges
            tmpRotation = rotateEdges(bm, heading, rotationMat, vertex, inStack)
            # Update selected edges and their center
            vertex, center, heading, inStack = tmpRotation[0], tmpRotation[1], tmpRotation[2], tmpRotation[3]
            
                
        # Turn around (angle: 180)
        elif char == '|':
            #rotationMat = [[math.cos(math.radians(180)), -math.sin(math.radians(180)), 0],
            #                [math.sin(math.radians(180)), math.cos(math.radians(180)), 0],
            #                [0, 0, 1]]
            rotationMat = mathutils.Matrix.Rotation(math.radians(180), 3, 'Z')              
            # Duplicate and rotate selected edges
            tmpRotation = rotateEdges(bm, heading, rotationMat, vertex, inStack)
            # Update selected edges and their center
            vertex, center, heading, inStack = tmpRotation[0], tmpRotation[1], tmpRotation[2], tmpRotation[3]
            
        # Push
        elif char == '[': 
            stack.append((vertex, (heading.x, heading.y, heading.z), center))
            inStack = True
        # Pop
        elif char == ']':
            vertex, tmpheading, center = stack.pop()
            heading = mathutils.Vector(tmpheading)
            #markedEdges = stack[0]
            #heading = mathutils.Vector(stack[1])
            #center = stack[2]
            inStack = False
        
        
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

def rotateEdges(bm, heading, rotationMat, vertex, inStack):
    
    
    if inStack:
        #Duplicate selected edges
        vertex = bmesh.ops.duplicate(bm, geom = [vertex])['geom'][0]
        
    
    
    if vertex == None:
        center = [0,0,0]
    else:
        # Calculate current center
        center = vertex.co
    # Rotate the edge       
    bmesh.ops.rotate(bm, cent = center, matrix = rotationMat, verts = [vertex])
  
    # Update heading vector
    heading.rotate(rotationMat)

    if inStack:
        inStack = False
    return vertex, center, heading, inStack

def main():
    word = createSystem(7, 'X')
    word = wordCleaner(word)
    word = replacer(word)
    print(word)
    
   
    angle = 22.5
    distance = 0.5
    #F[+F]F[-F]F[+F[+F]F[-F]F]F[+F]F[-F]F[-F[+F]F[-F]F]F[+F]F[-F]F[+F[+F]F[-F]F[+F[+F]F[-F]F]F[+F]F[-F]F[-F[+F]F[-F]F]F[+F]
    createTree(word, angle, distance)
    
if __name__ == "__main__":
    main()