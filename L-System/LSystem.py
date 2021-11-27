import bpy
from bpy.types import Object
import bmesh
from bmesh.types import BMesh
from math import radians, log, pow
from mathutils import Matrix, Vector
from os.path import dirname, abspath, join
from random import choice, seed, shuffle, choices


class LSystem:
    bl_idname = "mesh.l_system"
    bl_label = "l_system"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Initialize L-System Class
    def __init__(self, system: str, generation: int, size: float, style: str,
                randSeed: int, angle: float, thickness: float, leafSize: float,
                showShape: bool, showLeaf: bool, leafCount: int, random: bool,
                flat: bool):
        self.generation = generation
        self.system = system
        self.size = size
        self.style = style
        self.randSeed = randSeed
        self.thickness = thickness
        self.leafSize = leafSize
        self.angle = radians(angle)
        self.showShape = showShape
        self.showLeaf = showLeaf
        self.leafCount = leafCount
        self.random = random
        self.flat = flat
        # Set preset rules
        self.systems = {'system1': {'axiom': 'F', 'angle': 25.7, 'rule':{'F':'F[&F]F[^F]F[\F]F[/F]F'}, 'random':{'F':'F[+F]F[-F]F'},'stochastic': False},
            'system2': {'axiom': 'F', 'angle': 20, 'rule': {'F':'F[&F]F[^F]F[\F]F[/F][F]'}, 'random': {'F':'F[+F]F[-F][F]'}, 'stochastic': False},
            'system3': {'axiom': 'F', 'angle': 22.5, 'rule': {'F': 'FF^[^F&F&F]&[&F^F^F]/[/F\F\F]\[\F/F/F]'}, 'random':{'F': 'FF-[-F+F+F]+[+F-F-F]'}, 'stochastic': False},
            'system4': {'axiom': 'X', 'angle': 20, 'rule': {'F': 'FF', 'X': 'F[&X]F[^X]F[\X]F[/X]&X'}, 'random': {'F': 'FF', 'X': 'F[+X]F[-X]+X'},'stochastic': False},
            'system5': {'axiom': 'X', 'angle': 25.7, 'rule': {'F': 'FF', 'X': 'F[&X][^X][\X][/F]FX'}, 'random': {'F': 'FF', 'X': 'F[+X][-X]FX'}, 'stochastic': False},
            'system6': {'axiom': 'X', 'angle': 22.5, 'rule': {'F': 'FF', 'X': 'F^[[X]\+X]&&[[X]/-X]^F[/+FX]^X'}, 'random': {'F': 'FF', 'X': 'F-[[X]+X]+F[+FX]-X'}, 'stochastic': False},
            'system7': {'axiom': 'F', 'angle': 22.5, 'rule': {'F': {33:'F[+F][-F]F', 33: 'F[-F]F', 34:'F[+F]F'}}, 'stochastic': True},
            'system8': {'axiom': 'X', 'angle': 22.5, 'rule': {'F': 'FF', 'X': {33: 'F[+X]F[-X]+X', 33: 'F[-X]F[-X]+X', 34: 'F[-X]F+X'}}, 'stochastic': True}}
        # Deselect every selected object in the scene
        bpy.ops.object.select_all(action='DESELECT')
        # Set user's system of choice 
        self.selSystem = self.systems[system]
        # Set angle
        # Generate the word
        self.word = self.initSystem()
        # Create tree Structure
        self.tree, self.leaves = self.createTree()
        # Create tree skin and mesh
        # Convert tree bmesh to mesh and add it as a object to the scene
        self.treeObj = self.convertToMesh('Tree', self.tree)
        self.shapeTree()
        # Add leaves to the tree
        if self.showLeaf:
            self.addLeaves()
        
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
        # If system is not stochastic
        if self.selSystem['stochastic'] is not True:
            # Get the variables and production rules dictionary
            if self.random or self.flat:
                rules = self.selSystem['random']
            else:
                rules = self.selSystem['rule']
            
            # Variables are the keys of the dictionary
            variables = list(rules.keys())
            # For the number of production rules
            for i in range(len(variables)):
                # if current character is one of the rules
                if character in variables:
                    # if current character is the rule character
                    if character == variables[i]:
                        # Change character using the production rule
                        newstr = rules[variables[i]]
                else:
                        newstr = character
        # If system is stochastic
        else:
            # Get Variables of the system
            if self.random or self.flat:
                system = self.selSystem['random']
            else:
                system = self.selSystem['rule']
            variables = list(system.keys())
            stoVar = ''
            for var in variables:
                if len(system[var]) > 1:
                    stoVar = var
                    rules = system[var]
            # Get production rules of the system
            #rules = self.selSystem['rule'][list(self.selSystem['rule'])[0]]
            # Create a list for distributing the rules based on the given chances
            stoRules = []
            # Create the distributed list
            for key in list(rules.keys()):
                tmpList = [rules[key] for i in range(key)]
                stoRules += tmpList
            
            for i in range(len(variables)):
                    
                # if current character is one of the rules
                if character in variables:
                    # if current character is the rule character
                    if character == variables[i]:
                        if variables[i] == stoVar:
                            # Change character using the production rule
                            newstr = choice(stoRules)
                        else:
                            newstr = system[variables[i]]
                else:
                    newstr = character

        return newstr

    def rotationReplacer(self, word: str) -> str:
        if self.random:
            rotators = ['/','\\','&','^']
            posRots = ['\\', '&']
            negRots = ['/', '^']

            #shuffle(rotators)
            seed(self.randSeed)
            newstr = ''
            for i in range(0, len(word)):
               
                if word[i] == '+':
                    c = choice(posRots)
                    newstr += c
                elif word[i] == '-':
                    c = choice(negRots)
                    newstr += c   
                else:
                    newstr += word[i]

            return newstr
        elif self.flat:
            newstr = ''
            for i in range(0, len(word)):
                if word[i] == '+':
                    newstr += '&'
                elif word[i] == '-':
                    newstr += '^'
                else:
                    newstr += word[i]
            return newstr
        else:
            return word

    def wordCleaner(self, word: str) -> str:
        word = word.replace('X', '')
        word = word.replace('[+]', '')
        word = word.replace('[-]', '')
        return word

    def createTree(self) -> BMesh:
        
        # Set center point position based on the 3D cursor location
        center = bpy.context.scene.cursor.location
        # Create stack for pushing / pulling
        stack = []
        # Create heading vector
        heading = Vector([0, 0, self.size])
        # Create rotation matrix
        rotationMat = Matrix()
        # Is in Stack
        inStack = False
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
                # if in stack add a leaf vertex
                if inStack:
                    leaf = bmesh.ops.create_vert(bmLeaf, co = center)['vert'][0]

            # Turn Left
            elif char == '+':
                # Rotate heading Vector (angle) radians around Z and update it
                heading = self.rotateHeading(heading, -1, 'Z')
            
            # Turn Right
            elif char == '-':
                # Rotate heading Vector (-angle) radians around Z and update it
                heading = self.rotateHeading(heading, 1, 'Z')

            # Pitch Down
            elif char == '&':
                # Rotate heading Vector (angle) radians around Y and update it
                heading = self.rotateHeading(heading, -1, 'Y')

            # Pitch Up
            elif char == '^':
                # Rotate heading Vector (-angle) radians around Y and update it
                heading = self.rotateHeading(heading, 1, 'Y')
            
            # Roll Left (\)
            elif char == '\\':
                # Rotate heading Vector (angle) radians around X and update it
                heading = self.rotateHeading(heading, -1, 'X')
            
            # Roll Right
            elif char == '/':
                # Rotate heading Vector (-angle) radians around X and update it
                heading = self.rotateHeading(heading, 1, 'X')

            # Push current settings to stack
            elif char == '[':
                # Set inStack True
                inStack = True
                # Push current vertex, heading vector, and center point to the stack
                stack.append((vertex, (heading.x, heading.y, heading.z), center, inStack))
            
            # Pull previous settings from stack
            elif char == ']':
                inStack = False
                # create a vertex and the last vertex of the branch for leaf
                #leaf = bmesh.ops.create_vert(bmLeaf, co = center)['vert'][0]

                # Pull the previous vertex, heading vector, and center from the stack
                vertex, tmpHeading, center, inStack = stack.pop()

                # Update heading vector and create and new vector from pulled heading vector
                heading = Vector(tmpHeading)
       
        # Remove double vertices from tree structure
        bmesh.ops.remove_doubles(bmTree, verts = bmTree.verts, dist = 0.0001)

        return bmTree, bmLeaf


    def rotateHeading(self, heading: Vector, angleNegation: int, rotationAxis: str) -> Vector:
        # Rotate heading based on the rotation matrix
        heading.rotate(Matrix.Rotation(self.angle * angleNegation, 3, rotationAxis))
        return heading

    
    # Create skin around tree and clean up the tree structure
    def shapeTree(self) -> None:
        treeObj = self.treeObj
        # Select and make active
        bpy.context.view_layer.objects.active = treeObj
        # Select tree object
        treeObj.select_set(True)
        if self.showShape:
           
            """ SKIN MODIFIER"""
            # Add skin modifier to tree object
            skin = treeObj.modifiers.new(name='Skin', type='SKIN')
            # Set skin Modifier settings
            skin.branch_smoothing = 1 # Branch smoothing
            skin.use_x_symmetry = False # Disabling active symmetry
            if self.style == 'STYLE2':
                skin.use_smooth_shade = True
            # Activate auto smoothing for normals
            treeObj.data.use_auto_smooth = True
            # Go to edit mode for modifying skin size around the tree
            bpy.ops.object.mode_set(mode = 'EDIT')
            # Deselect all vertices
            bpy.ops.mesh.select_all(action = 'DESELECT')
            # Select the firts and bottom vertex of tree object
            self.selSingleVert(treeObj, 0)
            # Scale skin size proportionally from bottom vertex
            bpy.ops.transform.skin_resize(value = [(log(self.generation  * self.thickness,3) * self.generation * self.size) for i in range(3)],
                                        orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
                                        mirror=True,
                                        use_proportional_edit=True, proportional_edit_falloff='ROOT',
                                        proportional_size=log(self.generation,3)* log(self.generation, 2) * self.generation * self.size * 2,
                                        use_proportional_connected=False, use_proportional_projected=False)
            # Select the top last vertex
            self.selSingleVert(treeObj, -1)
            # Scale skin size proportionally from top vertex
            bpy.ops.transform.skin_resize(value = [(log(self.generation * self.thickness,3)* self.size ) for i in range(3)],
                                        orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', 
                                        mirror=True, 
                                        use_proportional_edit=True, proportional_edit_falloff='ROOT', 
                                        proportional_size=log(self.generation,3)* log(self.generation, 2) * self.generation * self.size * 2,
                                        use_proportional_connected=False, use_proportional_projected=False)

            """BEVEL MODIFIER (only for STYLE1)"""
            if self.style == 'STYLE1':
                # Add Bevel modifier
                bevel = treeObj.modifiers.new(name = 'Bevel', type = 'BEVEL')
                # Set bevel modifier settings
                bevel.affect = 'VERTICES' # Bevel only affect of vertices and not edges
                bevel.segments = 2 # Number of bevel segments

            """SUBDIVISION MODIFIER"""
            subdivision = treeObj.modifiers.new(name='Subdivision', type='SUBSURF')
            # Subdivision settings
            if self.style == 'STYLE1':
                subdivision.subdivision_type = 'SIMPLE' # Subdivision type
            else: 
                subdivision.subdivision_type = 'CATMULL_CLARK' # Subdivision type
            subdivision.levels = 1 # levels of viewport display

            """SMOOTH CORRECTIVE MODIFIER"""
            # Add smooth corrective modifier
            smoothCor = treeObj.modifiers.new(name = 'CorrectiveSmooth', type = 'CORRECTIVE_SMOOTH')
            # Smooth corrective modifier settings
            smoothCor.use_only_smooth = True # Use Only Smooth
            smoothCor.use_pin_boundary = True # Use Pin Boundaries

            """WEIGHTED NORMAL MODIFIER"""
            weighted = treeObj.modifiers.new(name = 'Weighted Normal', type= 'WEIGHTED_NORMAL')
            # Go to the object mode
            bpy.ops.object.mode_set(mode = 'OBJECT')


        """ASSIGNING MATERIAL TO THE TREE OBJECT"""
        # If TreeBody material is not in the blend file
        if 'TreeBody' not in bpy.data.materials.keys():
            # Set the filepath for material
            installationPath = dirname(abspath(__file__))
            filepath = join(installationPath, 'Materials\Materials.blend')
            # Set the directory path
            directory = join(installationPath, 'Materials')
            # Append TreeBody material from materials blend file
            bpy.ops.wm.append(filepath=filepath, directory=directory, filename='Materials.blend\Material\TreeBody')
        # Assign material to the tree object
        treeObj.data.materials.append(bpy.data.materials['TreeBody'])
        self.treeObj = treeObj
        #return treeObj

    def selSingleVert(self, object: Object, vertIndex: int) -> None:
        # Go to the object mode to select the given vertex
        bpy.ops.object.mode_set(mode = 'OBJECT')
        # Make sure none of the vertices are selected
        for i in range(len(object.data.vertices)):
            object.data.vertices[i].select = False 
        # Select the first and bottom vertex of the tree structure
        object.data.vertices[vertIndex].select = True
        # Go to edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')

    def addLeaves(self) -> None:
        # Set leaves bmesh
        bmLeaf = self.leaves
        # Convert leaves vertices to mesh and add it as a object to the scen
        leavesObj = self.convertToMesh('Leaves', bmLeaf)
        # Select leaves
        leavesObj.select_set(True)
        # Make leaves object child of tree object
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
        # Make leaves active sleection
        bpy.context.view_layer.objects.active = leavesObj

        """ SHRINKWRAP MODIFIER"""
        # Add Shrinkwrap modifier
        shrink = leavesObj.modifiers.new(name='Shrinkwrap', type='SHRINKWRAP')
        # Set the target object
        shrink.target = self.treeObj

        """PARTICLE SYSTEM"""
        # If leaf object is not in the blend file
        if 'L' not in bpy.data.objects.keys() or 'L2D' not in bpy.data.objects.keys():
            # Set filepath for leaf object blend file
            installationPath = dirname(abspath(__file__))
            filepath = join(installationPath, 'Materials\Materials.blend')
            # Set directory for leaf object blend file
            directory = join(installationPath, 'Materials')
            # Append leaf object to the blend file
            bpy.ops.wm.append(filepath=filepath, directory=directory, filename='Materials.blend\\Collection\Leaf', active_collection = False)
        # Add particle system to leaves object
        bpy.ops.object.particle_system_add()
        # Assign particle system to a variable
        particle = leavesObj.particle_systems.active
        # Particle system settings
        particle.settings.type = 'HAIR' # Set particle system to hair
        particle.settings.use_advanced_hair = True # Use advanced settings for the particle system
        particle.settings.count = int(pow(1000, log(self.generation,3)) / 10 * self.size * 2) * self.leafCount # Set the number of hairs base on the number of generations
        particle.settings.emit_from = 'VERT' # Set vertices as hair emit location
        particle.settings.render_type = 'OBJECT' # Set particle system to render hairs as a specific object
        particle.settings.use_emit_random = False # Don't use random order for instance object
        particle.settings.use_rotations = True # Use Rotation for instance objects
        particle.settings.rotation_mode = 'NOR' # Set vertices normals as rotation mode for instance objects 
        if self.flat:
            particle.settings.instance_object = bpy.data.objects['L2D'] # Set hair intance object to leaf 2d
            particle.settings.rotation_factor_random = 0 # Set rotaiton randomness to 0
            particle.settings.phase_factor = -0.246575 # Set rotation phase factor
            particle.settings.phase_factor_random = 0 # Set rotation randomness phase factor to 0
        else:
            particle.settings.instance_object = bpy.data.objects['L'] # Set hair instance object to leaf object 
            particle.settings.rotation_factor_random = 1 # Set rotation randomization to maximum
            particle.settings.phase_factor_random = 0.690391 # Set rotation randomization phase
        particle.settings.particle_size = log(6 * self.generation) / 10 * self.leafSize # Set instance object scale based on the number of generations
        particle.settings.size_random = 1 # Set scale size randomization to maximum
        particle.settings.use_rotation_instance = True # Use instance object rotation
        
        # Deactive leaf object collection and exclude it from the scene
        bpy.context.scene.view_layers[0].layer_collection.children['Leaf'].exclude = True

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
