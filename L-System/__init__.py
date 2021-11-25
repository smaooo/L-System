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
    "doc_url": "",
    "category": "Add Mesh",
}


from collections import defaultdict
import bpy
from os.path import dirname, abspath, join
from bpy.types import Operator
import bpy.props as prop
from bpy_extras.object_utils import AddObjectHelper
system = None


def initiateLSystem(self, context):
    global system
    system = LSystem.LSystem(self.rule, self.genNum, self.size, self.style, self.seed, self.angle, self.thickness, self.leafSize, self.showShape, self.showLeaf, self.leafCount)


def updateAngle(self,context):
    print(self.rule)    
    ruleDet = {'system1': {'angle': 25.7, 'thickness': 0.6, 'leafSize': 0.6},
                'system2': {'angle': 20, 'thickness': 0.4, 'leafSize': 0.35},
                'system3': {'angle': 22.5, 'thickness': 1, 'leafSize': 2},
                'system4': {'angle': 20, 'thickness': 0.8, 'leafSize': 0.62},
                'system5': {'angle': 25.7, 'thickness': 0.8, 'leafSize': 0.9},
                'system6': {'angle': 22.5, 'thickness': 0.8, 'leafSize': 1},
                'system7': {'angle': 22.5, 'thickness': 0.1, 'leafSize': 0.46},
                'system8': {'angle': 22.5, 'thickness': 1.4, 'leafSize': 1}}
    self.angle = ruleDet[self.rule]['angle']
    self.thickness = ruleDet[self.rule]['thickness']
    self.leafSize = ruleDet[self.rule]['leafSize']

class OBJECT_OT_add_object(Operator, AddObjectHelper):
    
    #pcoll = bpy.utils.previews.new()
    #iconPath = '\Materials\Icon.png'
    #pcoll.load("tree_icon", iconPath, 'IMAGE')
    #icon = pcoll['tree_icon']
    """Create a new Tree"""
    bl_idname = "mesh.add_tree"
    bl_label = "Create Tree"
    bl_options = {'REGISTER', 'UNDO'}
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

    ruleItems = [('system1', 'System 1', "System 1", pcoll['System1'].icon_id, 1),
                ('system2', 'System 2', 'System 2',pcoll['System2'].icon_id, 2),
                ('system3', 'System 3', 'System 3',pcoll['System3'].icon_id, 3),
                ('system4', 'System 4', 'System 4',pcoll['System4'].icon_id, 4),
                ('system5', 'System 5', 'System 5',pcoll['System5'].icon_id, 5),
                ('system6', 'System 6', 'System 6',pcoll['System6'].icon_id, 6),
                ('system7', 'System 7', 'System 7',pcoll['System7'].icon_id, 7),
                ('system8', 'System 8', 'System 8',pcoll['System8'].icon_id, 8)]

    
    iconPath = []
    for i in range(1,3):
        partPath = 'Materials\Style{}.png'.format(i)
        iconPath.append(join(installationPath, partPath))
    for icon in iconPath:
        pcoll.load("Style{}".format(iconPath.index(icon)+1), icon, 'IMAGE')

    styles = [('STYLE1', 'Jagged', 'Jagged Mesh', pcoll['Style1'].icon_id, 1),
            ('STYLE2', 'Smooth', 'Smooth and organic', pcoll['Style2'].icon_id, 2)]

    rule: prop.EnumProperty(
        items = ruleItems,
        name = 'System', update = updateAngle
    )

    genNum: prop.IntProperty(
        name='Generations',
        description = 'Number of Generations',
        default = 3,
        min = 1, max = 10
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

    leafCount: prop.IntProperty(
        name = 'Leaves Count',
        description = 'Leaves Count Multiplication',
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
    def draw(self, context):
        #self.angle = self.ruleAngle[self.rule]
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        box = layout.box()
        box.label(text='L-System', icon_value = self.pcoll['tree_icon'].icon_id)
        box.prop(self, 'rule')
        box.prop(self, 'genNum')
        box.prop (self, 'angle')
        box.prop(self, 'seed')
        box.prop(self, 'size')
        box = layout.box()
        box.label(text = 'Mesh', icon = 'MESH_DATA')
        box.prop(self, 'showShape')
        if self.showShape:
            box.prop(self, 'thickness')
            box.prop(self, 'style')
        box = layout.box()
        box.label(text = 'Leaves', icon_value = self.pcoll['LeafIcon'].icon_id)
        box.prop(self, 'showLeaf')
        if self.showLeaf:
            box.prop(self, 'leafCount')
            box.prop(self, 'leafSize')
        #layout.operator(MESH_OT_tree_structure.bl_idname, text='Shape', icon='NODE')

    
    
    def execute(self, context):        
        initiateLSystem(self,context)
        
        return {'FINISHED'}

def add_object_button(self, context):
    pcoll = bpy.utils.previews.new()
    installationPath = dirname(abspath(__file__))
    iconPath = join(installationPath, 'Materials\Icon.png')
    pcoll.load("tree_icon", iconPath, 'IMAGE')
    icon = pcoll['tree_icon']
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="Tree",
        icon_value = icon.icon_id)
    

preview_collections = {}
def register():
    
    bpy.utils.register_class(OBJECT_OT_add_object)  
    bpy.types.VIEW3D_MT_add.append(add_object_button)
    #LSystem.register()

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_object)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_object_button)

    #LSystem.unregister()
if __name__ == "__main__":
    register()
