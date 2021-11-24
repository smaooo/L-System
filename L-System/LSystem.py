
import bpy
from bpy.types import Object
import bmesh
from bmesh.types import BMesh
from math import radians, log, pow
import mathutils
from mathutils import Matrix
from mathutils.Matrix import Vector, Rotation
from os.path import dirname
from random import randint, choice




class LSystem:
    # Initialize L-System Class
    def __init__(self, system: str, generation: int, size: float):
        self.generation = generation
        self.system = system
        self.size = size
        # Set preset rules
        self.systems = {'system1': {'axiom': 'F', 'angle': 25.7, 'rule':{'F':'F[+F]F[-F]F'}},
            'system2': {'axiom': 'F', 'angle': 20, 'rule': {'F':'F[+F]F[-F][F]'}},
            'system3': {'axiom': 'F', 'angle': 22.5, 'rule': {'F': 'FF-[-F+F+F]+[+F-F-F]'}},
            'system4': {'axiom': 'X', 'angle': 20, 'rule': {'F': 'FF', 'X': 'F[+X]F[-X]+X'}},
            'system5': {'axiom': 'X', 'angle': 25.7, 'rule': {'F': 'FF', 'X': 'F[+X][-X]FX'}},
            'system6': {'axiom': 'X', 'angle': 22.5, 'rule': {'F': 'FF', 'X': 'F-[[X]+X]+F[+FX]-X'}},
            'system7': {},
            'system8': {}}
        # Set user's system of choice
        self.selSystem = self.systems[system]
        # Set angle
        self.angle = radians(self.selSystem['angle'])
        # Generate the word
        self.word = self.initSystem()
        # Create tree Structure
        self.tree, self.leaves = self.createTree()
        
    # Initialize system
    def initSystem(self) -> str:
        # Set the axiom as the first character of the L-System word
        startString = self.selSystem['axiom']
        endString = ''
        # For number of generations that user has chosen, generate the process the word
        for gen in range(self.generation):
            endString = self.processString(startString)
            startString = endString
        return self.wordCleaner(self.rotationReplacer(endString))

    # Generate the L-System word 
    def processString(self, word: str) -> str: 
        newstr = ''
        # Go through each character of the word and apply the rules on it
        for character in word:
            newstr = newstr + self.generateWord(character)
    
        return newstr

    # Apply the production rule(s) on the given character
    def generateWord(self, character: str) -> str:
        newstr = ''
        
        # Get the variables and production rules dictionary
        rules = self.selSystem['rule']
        # Variables are the keys of the dictionary
        variables = list(rules.keys())
        for i in range(len(variables)):
            if character in variables:
                if character == variables[i]:
                    newstr = rules[variables[i]]
            else:
                    newstr = character
        return newstr

    def rotationReplacer(self, word: str) -> str:
        rotators = ['/','\\','&','^']
        newstr = ''
        
        for i in range(0, len(word)):
            if word[i] == '+' or word[i] ==  '-':
               
                c = choice(rotators)
                newstr += c
               
            else:
                newstr += word[i]

        return newstr

    def wordCleaner(self, word: str) -> str:
        word = word.replace('X', '')
        word = word.replace('[+]', '')
        word = word.replace('[-]', '')
        return word

    def createTree(self) -> BMesh:
        
        # Set center point position
        center = [0,0,0]
        # Create stack for pushing / pulling
        stack = []
        # Create heading vector
        heading = Vector([0, 0, self.size])
        # Create rotation matrix
        rotationMat = Matrix()

        # Create a new bmesh for the tree structure
        bmTree = bmesh.new()
        # Create a new bmesh for leaf vertices
        bmLeaf = bmesh.new()
        
        # Create the first and bottom vertex of the tree
        vertex = bmesh.ops.create_vert(bmTree, co = center)['vert'][0]

        for char in self.word:
            # Extrude and move current vertex in heading vector direction
            if char == 'F':
                # Extrude the vertex
                vertex = bmesh.ops.extrude_vert_indiv(bmTree, verts = [vertex])['verts'][0]
                # Move extruded vertex according to the heading vector
                bmesh.ops.translate(bmTree, vec = heading, verts = [vertex])
                # Update center point to the latest vertex coordination
                center = vertex.co

            # Turn Left
            elif char == '+':
                # Rotate heading Vector (angle) radians around Z and update it
                heading = self.rotateHeading(heading, 1, 'Z')
            
            # Turn Right
            elif char == '-':
                # Rotate heading Vector (-angle) radians around Z and update it
                heading = self.rotateHeading(heading, -1, 'Z')

            # Pitch Down
            elif char == '&':
                # Rotate heading Vector (angle) radians around Y and update it
                heading = self.rotateHeading(heading, 1, 'Y')

            # Pitch Up
            elif char == '^':
                # Rotate heading Vector (-angle) radians around Y and update it
                heading = self.rotateHeading(heading, -1, 'Y')
            
            # Roll Left (\)
            elif char == '\\':
                # Rotate heading Vector (angle) radians around X and update it
                heading = self.rotateHeading(heading, 1, 'X')
            
            # Roll Right
            elif char == '/':
                # Rotate heading Vector (-angle) radians around X and update it
                heading = self.rotateHeading(heading, -1, 'X')

            # Push current settings to stack
            elif char == '[':
                # Push current vertex, heading vector, and center point to the stack
                stack.append((vertex, (heading.x, heading.y, heading.z), center))
            
            # Pull previous settings from stack
            elif char == ']':
                # create a vertex and the last vertex of the branch for leaf
                leaf = bmesh.ops.create_vert(bmLeaf, co = center)['vert'][0]

                # Pull the previous vertex, heading vector, and center from the stack
                vertex, tmpHeading, center = stack.pop()

                # Update heading vector and create and new vector from pulled heading vector
                heading = Vector(tmpHeading)

        return bmTree, bmLeaf


    def rotateHeading(self, heading: Vector, angleNegation: int, rotationAxis: str) -> Vector:
        # Rotate heading based on the rotation matrix
        heading.rotate(Rotation(self.angle * angleNegation, 3, rotationAxis))
        return heading

    # Create skin around tree and clean up the tree structure
    def shapeTree(self):
        # Set tree bmesh
        bmTree = self.tree
        # Remove double vertices from tree structure
        bmesh.ops.remove_doubles(bmTree, verts = bmTree.verts, dist = 0.0001)
        # Convert tree bmesh to mesh and add it as a object to the scene
        treeObj = self.convertToMesh('Tree', bmTree)
        
        """ SKIN MODIFIER"""
        # Add skin modifier to tree object
        skin = treeObj.modifiers.new(name='Skin', type='SKIN')
        # Set skin Modifier settings
        skin.branch_smoothing = 1 # Branch smoothing
        skin.use_x_symmetry = False # Disabling active symmetry

        # Go to edit mode for modifying skin size around the tree
        bpy.ops.object.mode_set(mode = 'EDIT')
        # Deselect all vertices
        bpy.ops.mesh.select_all(action = 'DESELECT')
        # Go back to the object mode to select the first and bottom vertex of the tree
        bpy.ops.object.mode_set(mode = 'OBJECT')
        # Select the first and bottom vertex of the tree structure
        treeObj.data.vertices[0].select = True
        # Go to edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')
        # Scale skin size proportionally from bottom vertex
        bpy.ops.transform.skin_resize(value = [log(self.generation,3) * self.generation / 2 for i in range(3)],
                                    orient_type='GLOBAL',
                                    orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                                    orient_matrix_type='GLOBAL',
                                    mirror=True,
                                    use_proportional_edit=True, proportional_edit_falloff='ROOT',
                                    proportional_size=log(self.generation,3)* log(self.generation, 2) * self.generation,
                                    use_proportional_connected=False, use_proportional_projected=False)


    def addLeaves(self):
        # Set leaves bmesh
        bmLeaf = self.leaves
        # Convert leaves vertices to mesh and add it as a object to the scen
        leavesObj = self.convertToMesh('Leaves', bmLeaf)
        # Select the leaves object and set it to active object 
        bpy.context.view_layer.objects.active = leavesObj
        # Select leaves
        leavesObj.select_set(True)

    # Convert BMesh to Mesh
    def convertToMesh(self, objectName: str, bm: BMesh) -> Object:
        # Create a new empty mesh
        mesh = bpy.data.meshes.new(objectName + 'Mesh')
        # Convert given bmesh to mesh
        bm.to_mesh(mesh)
        # Free memory allocated by bmesh
        bm.free()
        # Create an object in the scene with the given mesh
        obj = bpy.data.objects.new(objectName, mesh)
        # Add object to the scene collection
        bpy.context.collection.objects.link(obj)

        return obj

def register():
    bpy.utils.register_class(LSystem)
def unregister():
    bpy.utils.unregister_class(LSystem)
    

l = LSystem('system5', 7, 0.5)