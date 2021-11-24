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


import bpy
from os.path import dirname, abspath, join
from bpy.types import Operator
import bpy.props as prop
from bpy_extras.object_utils import AddObjectHelper



def initiateLSystem(self, context):
   
    system = LSystem.LSystem(self.rule, self.genNum, self.size, self.style, self.seed)

class OBJECT_OT_add_object(Operator, AddObjectHelper):
    
    #pcoll = bpy.utils.previews.new()
    #iconPath = '\Materials\Icon.png'
    #pcoll.load("tree_icon", iconPath, 'IMAGE')
    #icon = pcoll['tree_icon']
    """Create a new Tree"""
    bl_idname = "mesh.add_tree"
    bl_label = "Create Tree"
    bl_options = {'REGISTER', 'UNDO'}

    ruleItems = [('system1', 'System 1', "System 1", 1),
                ('system2', 'System 2', 'System 2', 2),
                ('system3', 'System 3', 'System 3', 3),
                ('system4', 'System 2', 'System 4', 4),
                ('system5', 'System 5', 'System 5', 5),
                ('system6', 'System 6', 'System 6', 6),
                ('system7', 'System 7', 'System 7', 7),
                ('system8', 'System 8', 'System 8', 8)]

    styles = [('STYLE1', 'Style 1', 'Style 1'),
            ('STYLE2', 'Style 2', 'Style 2')]

    rule: prop.EnumProperty(
        items = ruleItems,
        name = 'Rule')


    genNum: prop.IntProperty(
        name='Generations',
        description = 'Number of Generations',
        default = 5,
        min = 1, max = 10)
    
    size: prop.FloatProperty(
        name = 'Size',
        description = 'Size of the tree', 
        min = 0.1, 
        default = 0.5)
    
    
    style: prop.EnumProperty(
        items = styles,
        name = 'Style'
    )
    
    seed: prop.IntProperty(
        name = 'Rotation Seed',
        description = 'Branches Rotation Seed',
        default = 0,
        min = 0
    )
    

    def draw(self, context):
        
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        layout.prop(self, 'rule')
        layout.prop(self, 'genNum')
        layout.prop(self, 'size')
        layout.prop(self, 'style')
        layout.prop(self, 'seed')
        

            
    
    def execute(self, context):
        
        initiateLSystem(self,context)
        return {'FINISHED'}

def add_object_button(self, context):
    pcoll = bpy.utils.previews.new()
    installationPath = dirname(abspath(__file__))
    iconPath = join(installationPath, 'Materials\Icon.png')
    print(iconPath)
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