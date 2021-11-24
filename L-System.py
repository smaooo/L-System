import bpy
import bmesh
from math import radians, log, pow
import mathutils
from os.path import dirname
from random import randint, choice

# L-System Settings
ITERATIONS = 6



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

def replacer(word):
    rotators = ['/','\\','&','^']
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

def createSystem(iters, axiom):
  startString = axiom
  endString = ''
  
  for i in range(iters):
    endString = processString(startString)
    startString = endString
  return endString

def createTree(word, angle, distance):
    # Convert angle to radians
    angle = radians(angle)
    # Set center point location
    center = [0,0,0]
    # Create stack for push action
    stack = []
    # Set current heading
    heading = mathutils.Vector([0,0,distance])
    
    # Set rotation matrix
    rotationMat = mathutils.Matrix()

    # Make a new BMesh for the tree
    bm = bmesh.new()
    # Make a new BMesh for the leaves
    bmLeaf = bmesh.new()
    # Create first Vertex
    vertex = bmesh.ops.create_vert(bm, co = center)['vert'][0]
    # Create leaf list
    #leaf = []
    # Max of steps
    max = len(word)
    index = 0
    # Loop throught the L-System word
    for char in word:
        
  
        #Progress
        print(str(index) + '/' + str(max))
        index += 1
        # Move forward and create a mesh cell
        if char == 'F':   
            # Extrude the marked edges
            vertex = bmesh.ops.extrude_vert_indiv(bm, verts = [vertex])['verts'][0]
            # Move selecte vertices forward
            bmesh.ops.translate(bm, vec=heading, verts=[vertex])   
            # set current center
            center = vertex.co
      
        # Turn left
        elif char == '+':
            # Set the rotation matrix
            rotationMat = mathutils.Matrix.Rotation(angle, 3, 'Z')
            # Rotate heading vector
            heading.rotate(rotationMat)  
          
        # Turn right
        elif char == '-':
            # Set the rotation matrix
            rotationMat = mathutils.Matrix.Rotation(-angle, 3, 'Z')
            # Rotate heading vector
            heading.rotate(rotationMat)
            
        # Pitch down
        elif char == '&':
            # Set the rotation matrix
            rotationMat = mathutils.Matrix.Rotation(angle, 3, 'Y')
            # Rotate heading vector
            heading.rotate(rotationMat)
            
        # pitch up
        elif char == '^':
            # Set the rotation matrix
            rotationMat = mathutils.Matrix.Rotation(-angle, 3, 'Y')
            # Rotate heading vector
            heading.rotate(rotationMat)
           
        # Roll left (\)
        elif char == '\\':
            # Set the rotation matrix
            rotationMat = mathutils.Matrix.Rotation(angle, 3, 'X')
            # Rotate heading vector
            heading.rotate(rotationMat)
             
        # Roll right
        elif char == '/':
            # Set the rotation matrix
            rotationMat = mathutils.Matrix.Rotation(-angle, 3, 'X')
            # Rotate heading vector
            heading.rotate(rotationMat)
                   
        # Push
        elif char == '[': 
            # Append current vertex, heading vector, and center to the stack list as a new tuple
            stack.append((vertex, (heading.x, heading.y, heading.z), center))
        
        # Pop
        elif char == ']':
            leaf = bmesh.ops.create_vert(bmLeaf, co = center)['vert'][0]
            #l = bmesh.ops.create_vert(bm, co = center)
            #leaf.append(l)
            # Get the previous vertex, heading vector, and center from the stack list
            vertex, tmpheading, center = stack.pop()
            # Create the heading vector
            heading = mathutils.Vector(tmpheading)
           
    """ CONVERTING VERTICES TO MESHES """        
    # Remove doubles
    bmesh.ops.remove_doubles(bm, verts = bm.verts, dist = 0.0001)
    # Finish up, write the bmesh into a new mesh
    meshTree = bpy.data.meshes.new("TreeMesh")
    # Create a mesh from bmesh
    bm.to_mesh(meshTree)
    # Free memory allocated by bmesh
    bm.free()
    # Create an object of the mesh
    obj = bpy.data.objects.new("Tree", meshTree)
    # Add object to the scene collection
    bpy.context.collection.objects.link(obj)
    
    # write the leaves bmesh into a new mesh
    meshLeaf = bpy.data.meshes.new("LeavesMesh")
    # Create a mesh from bmesh
    bmLeaf.to_mesh(meshLeaf)
    # Free memory allocated by bmesh
    bmLeaf.free()
    # Create an object of the mesh
    objLeaf = bpy.data.objects.new("Leaves", meshLeaf)
    # Add object to the scene collection
    bpy.context.collection.objects.link(objLeaf)
    # Select and make active
    bpy.context.view_layer.objects.active = obj
    # Select leaves
    obj.select_set(True)
    
    """ MODIFYING AND OPTIMIZING TREE VERTICES """
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
    bpy.ops.transform.skin_resize(value=( log(ITERATIONS,3)*ITERATIONS /2, log(ITERATIONS,3)*ITERATIONS/2, log(ITERATIONS,3)*ITERATIONS/2), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=True, proportional_edit_falloff='ROOT', proportional_size=log(ITERATIONS,3)* log(ITERATIONS, 2) * ITERATIONS, use_proportional_connected=False, use_proportional_projected=False)
    # Go to object mode
    bpy.ops.object.mode_set(mode = 'OBJECT')
    # Deselct first vertex
    obj.data.vertices[0].select = False
    # Select last vertex
    obj.data.vertices[-1].select = True
    # Go to Edit mode
    bpy.ops.object.mode_set(mode = 'EDIT')
    # Scle skin size proportionally form top vertex
    bpy.ops.transform.skin_resize(value=(log(ITERATIONS,3) , log(ITERATIONS,3) , log(ITERATIONS,3) ), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=True, proportional_edit_falloff='ROOT', proportional_size=log(ITERATIONS,3)* 1000, use_proportional_connected=False, use_proportional_projected=False)
    
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
        filepath = dirname(bpy.data.filepath) + '\Materials\Materials.blend'
        # Set the directory
        directory = dirname(bpy.data.filepath) + '\\Materials'
        # Append the material to this file
        bpy.ops.wm.append(filepath=filepath, directory = directory, filename='Materials.blend\\Material\TreeBody')        
        # Append the material to the object
        obj.data.materials.append(bpy.data.materials['TreeBody'])
        
        
    """ PARTICLE SYSTEM """    
    # Select leaves
    objLeaf.select_set(True)
    # Set tree as parent 
    bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
    # Make leaves active selection
    bpy.context.view_layer.objects.active = objLeaf
    # Add particle System for leaves
    bpy.ops.object.particle_system_add()
    # Assign particle system to a variable
    particle = objLeaf.particle_systems.active
    # Set particle system to hair
    particle.settings.type = 'HAIR'
    # Set hairs to grow from vertices
    particle.settings.emit_from = 'VERT'
    # Set hairs render type to object
    particle.settings.render_type = 'OBJECT'
    if 'L' not in bpy.data.objects.keys():
        filepath = dirname(bpy.data.filepath) + '\Materials\Materials.blend'
        # Set the directory
        directory = dirname(bpy.data.filepath) + '\\Materials'
        # Append the material to this file
        bpy.ops.wm.append(filepath=filepath, directory = directory, filename='Materials.blend\\Collection\Leaf') 
    # Select leaf mesh
    particle.settings.instance_object = bpy.data.objects['L']
    particle.settings.use_emit_random = False
    particle.settings.use_advanced_hair = True
    particle.settings.use_rotations = True
    particle.settings.rotation_mode = 'NOR'
    particle.settings.rotation_factor_random = 1
    particle.settings.phase_factor_random = 0.690391
    particle.settings.particle_size = log(6 * ITERATIONS) / 10
    particle.settings.size_random = 1
    particle.settings.use_rotation_instance = True
    particle.settings.count = int(pow(1000, log(ITERATIONS,3)) / 10)
    bpy.context.scene.view_layers[0].layer_collection.children['Leaf'].exclude = True
def main():
    # Create L-system
    word = createSystem(ITERATIONS, 'X')
    # Clean up the word
    word = wordCleaner(word)
    # Add 3d rotations to the word
    word = replacer(word)
    
    angle = 25.7
    distance = 0.5
    createTree(word, angle, distance)
    
if __name__ == "__main__":
    main()