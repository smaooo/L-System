if "bpy" in locals():
    import importlib as imp
    imp.reload(LSystem)
else:
    from . import LSystem



bl_info = {
    "name": "L-System Tree",
    "author": "Soroush Mohammadzadeh Azari",
    "version": (1, 0),
    "blender": (2, 93, 0),
    "location": "View3D > Add",
    "description": "Creates a tree based on L-System",
    "warning": "",
    "doc_url": "https://github.com/smaooo/L-System/blob/main/README.md",
    "category": "Add Mesh",
}


from collections import defaultdict
import bpy
from os.path import dirname, abspath, join
from bpy.types import Operator, PropertyGroup
import bpy.props as prop
from bpy_extras.object_utils import AddObjectHelper
import textwrap

system = None
warningMessage = ''
#treeSelf = None

# Call LSystem module
def initiateLSystem(self, context):
    global system
    system = LSystem.LSystem(self.rule, self.genNum, self.size, self.style,
                            self.seed, self.angle, self.thickness, self.leafSize,
                            self.showShape, self.showLeaf, self.leafCount, self.randomRotation,
                            self.flat)

# Update Variables after the system change
def updateVariables(self,context):
    
    # Defined variables for each system
    ruleDet = {'system1': {'angle': 25.7, 'thickness': 0.6, 'leafSize': 0.6, 'leafCount': 5},
                'system2': {'angle': 20, 'thickness': 0.4, 'leafSize': 0.35, 'leafCount': 5},
                'system3': {'angle': 22.5, 'thickness': 0.1, 'leafSize': 0.3, 'leafCount': 200},
                'system4': {'angle': 20, 'thickness': 0.8, 'leafSize': 0.62, 'leafCount': 5}, 
                'system5': {'angle': 25.7, 'thickness': 0.8, 'leafSize': 0.5, 'leafCount': 5},
                'system6': {'angle': 22.5, 'thickness': 0.7, 'leafSize': 0.43, 'leafCount': 3},
                'system7': {'angle': 22.5, 'thickness': 0.1, 'leafSize': 0.15, 'leafCount': 2},
                'system8': {'angle': 22.5, 'thickness': 0.5, 'leafSize': 0.26, 'leafCount': 5}}
    
    # Updates
    self.angle = ruleDet[self.rule]['angle']
    self.thickness = ruleDet[self.rule]['thickness']
    self.leafSize = ruleDet[self.rule]['leafSize']
    self.leafCount = ruleDet[self.rule]['leafCount']
    self.size = 0.5
    self.flat = True
    self.showShape = False
    self.showLeaf = False
    self.genNum = 3

# Change random rotation option based on the 2D/3D context
def changeRotation(self, context):
    if self.flat:
        self.randomRotation = False
        
    else:
        self.randomRotation = True

# Update draw length based on the random rotation option
def updateLen(self, context):

    if self.randomRotation:
        self.size = 0.5
    else: 
        self.size = 0.25

# UI Panel
class OBJECT_OT_add_object(Operator, AddObjectHelper):
    
    """Create a new Tree"""
    bl_idname = "mesh.add_tree"
    bl_label = "Create Tree"
    bl_options = {'REGISTER', 'UNDO'}

    # Check rule and give warning to the user
    def checkRule(self, context):
        global warningMessage

        rules = {'system1': [5,5,4],
                'system2': [5,5,4],
                'system3': [4,4,3],
                'system4': [7,7,5],
                'system5': [8,7,5],
                'system6': [6,6,6],
                'system7': [8,8,7],
                'system8': [8,8,6]}

        genRules = rules[self.rule]
        ruleIndex = list(rules.keys()).index(self.rule) + 1

        # Produce warning message
        warning = '''System {} will process the tree generation really slowly after the {}th generation. Therefore, it is possible that Blender stall for a long time based on your device specification.'''
        
        # Check states
        if self.flat:
            if self.genNum > genRules[0]:
                warningMessage =  warning.format(str(ruleIndex), str(genRules[0]))
                return bpy.ops.wm.warning("INVOKE_DEFAULT")
    
        else:
            if self.randomRotation:
                if self.genNum > genRules[1]:
                    warningMessage = warning.format(str(ruleIndex), str(genRules[1]))
                    return bpy.ops.wm.warning("INVOKE_DEFAULT")
          
            else:
                if self.genNum > genRules[2]:
                    warningMessage = warning.format(str(ruleIndex), str(genRules[2]))
                    return bpy.ops.wm.warning("INVOKE_DEFAULT")

    """ADD ICONS""" 
    pcoll = bpy.utils.previews.new()
    installationPath = dirname(abspath(__file__))
    iconPath = []

    for i in range(1,9):
        partPath = 'Materials\System{}.png'.format(i)
        iconPath.append(join(installationPath, partPath))
   
    for icon in iconPath:
        pcoll.load("System{}".format(iconPath.index(icon)+1), icon, 'IMAGE')
    tmpPath = 'Materials\LeafIcon.png'
    leafIcon = join(installationPath, tmpPath)
    pcoll.load("LeafIcon", leafIcon, 'IMAGE')

    tmpPath = join(installationPath, 'Materials\Icon.png')
    pcoll.load("tree_icon", tmpPath, 'IMAGE')

    
    iconPath = []
    for i in range(1,3):
        partPath = 'Materials\Style{}.png'.format(i)
        iconPath.append(join(installationPath, partPath))
    for icon in iconPath:
        pcoll.load("Style{}".format(iconPath.index(icon)+1), icon, 'IMAGE')

    tmpPath = join(installationPath, 'Materials\DD.png')
    pcoll.load("DD", tmpPath, 'IMAGE')

    tmpPath = join(installationPath, 'Materials\DDD.png')
    pcoll.load("DDD", tmpPath, 'IMAGE')

    """CLASS ATTRIBUTES"""
    ruleItems = [('system1', 'System 1', "System 1", pcoll['System1'].icon_id, 1),
                ('system2', 'System 2', 'System 2',pcoll['System2'].icon_id, 2),
                ('system3', 'System 3', 'System 3',pcoll['System3'].icon_id, 3),
                ('system4', 'System 4', 'System 4',pcoll['System4'].icon_id, 4),
                ('system5', 'System 5', 'System 5',pcoll['System5'].icon_id, 5),
                ('system6', 'System 6', 'System 6',pcoll['System6'].icon_id, 6),
                ('system7', 'System 7', 'System 7',pcoll['System7'].icon_id, 7),
                ('system8', 'System 8', 'System 8',pcoll['System8'].icon_id, 8)]

    styles = [('STYLE1', 'Jagged', 'Jagged Mesh', pcoll['Style1'].icon_id, 1),
            ('STYLE2', 'Smooth', 'Smooth and organic', pcoll['Style2'].icon_id, 2)]

    
    rule: prop.EnumProperty(
        items = ruleItems,
        name = 'System', update = updateVariables
    )

    genNum: prop.IntProperty(
        name='Generations',
        description = 'Number of Generations',
        default = 3,
        min = 1, max = 10,
        update = checkRule
    )
    
    size: prop.FloatProperty(
        name = 'Draw Length',
        description = 'Distance between each vertex', 
        min = 0.1, 
        default = 0.5
    )
    
    
    style: prop.EnumProperty(
        items = styles,
        name = 'Style',
        default = 'STYLE2'
    )
    
    seed: prop.IntProperty(
        name = 'Rotation Seed',
        description = 'Branches Rotation Seed',
        default = 0,
        min = 0
    )
    
    angle: prop.FloatProperty(
        name = 'Angle',
        description = 'Branch Rotation Angle',
        min = -360, max = 360, default = 25.7
    )


    thickness: prop.FloatProperty(
        name = 'Branch Thickness',
        description = 'Branch Thickness',
        default = 0.6,
        min = 0.1
    )
    leafSize: prop.FloatProperty(
        name = 'Leaf Size',
        description = 'Leaves General Size',
        min = 0,
        default = 0.63
    )

    leafCount: prop.FloatProperty(
        name = 'Leaf Count',
        description = 'Leaf Count Multiplication',
        default = 1,
        min = 0
    )

    showShape: prop.BoolProperty(
        name = 'Show Mesh',
        description = 'Toggle between the structure and the mesh',
        default = False
    )
    showLeaf: prop.BoolProperty(
        name= 'Show Leaves',
        description = 'Show Leaves',
        default = False
    )

    randomRotation: prop.BoolProperty(
        name = 'Random Rotation',
        description = 'Use random rotation for branches',
        default = False,
        update = updateLen
    )

    flat: prop.BoolProperty(
        name = '2D / 3D', 
        description = 'Toggle between 2D (Flat) mode and 3D mode.',
        default = True,
        update = changeRotation
    )
    
    generate: prop.BoolProperty(
        name = 'Generate',
        description = "Generate Tree",
        default = False
    )

    realTime: prop.BoolProperty(
        name= 'Real-time',
        description = 'Update L-System constantly with every change.',
        default = False,
    )
  
    regenerate: prop.BoolProperty(
        name = 'Regenerate',
        description = 'Regenrate stochastic system',
        default = False
    )

    # UI Panel draw Function
    def draw(self, context):

        layout = self.layout
        layout.use_property_split = True
        box = layout.box()
        box.label(text='L-System', icon_value = self.pcoll['tree_icon'].icon_id)
        row = box.row(heading = 'Real-time')
        row.prop(self, 'realTime', text = '')
        box.prop(self, 'rule')
        if self.flat:
            box.prop(self, 'flat', icon_value = self.pcoll['DDD'].icon_id, invert_checkbox = True)
        else:
            box.prop(self, 'flat', icon_value = self.pcoll['DD'].icon_id)
        box.prop(self, 'genNum')
        box.prop (self, 'angle')
        if self.flat == False:
            box.prop(self, 'randomRotation')
            if self.randomRotation:
                box.prop(self, 'seed')
        box.prop(self, 'size')
        if self.rule == 'system7' or self.rule == 'system8':
            if self.realTime:
                box.prop(self, 'regenerate', icon= 'MOD_BUILD', expand = True)
        box = layout.box()
        box.label(text = 'Mesh', icon = 'MESH_DATA')
        row = box.row(heading='Show Mesh')
        row.prop(self, 'showShape', text = '')
        if self.showShape:
            box.prop(self, 'thickness')
            box.prop(self, 'style')
        box = layout.box()
        box.label(text = 'Leaves', icon_value = self.pcoll['LeafIcon'].icon_id)
        row = box.row(heading = 'Show Leaves')
        row.prop(self, 'showLeaf', text='')
        if self.showLeaf:
            box.prop(self, 'leafCount')
            box.prop(self, 'leafSize')
        if self.realTime == False:
            row = layout.row(align=True)
            row.prop(self, 'generate', icon = 'MOD_REMESH', expand = True)

    # Execute LSYSTEMS after changes in panel
    def execute(self, context):  

        if self.realTime or self.generate or self.regenerate:
            self.regenerate = False
            self.generate = False
            initiateLSystem(self,context)
        
        return {"FINISHED"}
    
# Add warning message to pop-up panel
def printText(context, parent):
    global warningMessage
    wrapper = textwrap.wrap(text = warningMessage, width = context.region.width / 6)
    #lines = wrapper.wrap(text=warningMessage)
    for line in wrapper:
        parent.label(text = line)

# Warning message pop-up class
class WM_OT_warning(Operator):
    bl_idname = 'wm.warning'
    bl_label = "WARNING"

    # Draw warning panel
    def draw(self, context):
        layout = self.layout
        box = layout.box()
        printText(context, box)
        
    def execute(self, context):
    
        return {"FINISHED"}
    
    def invoke(self,context,event):

        return context.window_manager.invoke_props_dialog(self)

# Add Tree button to the add menu
def add_object_button(self, context):
    # Add Icon
    pcoll = bpy.utils.previews.new()
    installationPath = dirname(abspath(__file__))
    iconPath = join(installationPath, 'Materials\Icon.png')
    pcoll.load("tree_icon", iconPath, 'IMAGE')
    icon = pcoll['tree_icon']
    # Add button operator
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="Tree",
        icon_value = icon.icon_id)
    

def register():
    
    bpy.utils.register_class(OBJECT_OT_add_object)  
    bpy.utils.register_class(WM_OT_warning)
    bpy.types.VIEW3D_MT_add.append(add_object_button)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_object)
    bpy.utils.unregister_class(WM_OT_warning)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_object_button)

if __name__ == "__main__":
    register()
