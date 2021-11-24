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
    "location": "View3D > Add > Mesh > New Object",
    "description": "Creates a tree based on L-System",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}


import bpy
from os.path import dirname
from bpy.types import Operator
import bpy.props as prop
from bpy_extras.object_utils import AddObjectHelper



def initiateLSystem(self, context):
    rules = {'rule1': {'axiom': 'F', 'angle': 25.7, 'rule':{'F':'F[+F]F[-F]F'}},
            'rule2': {'axiom': 'F', 'angle': 20, 'rule': {'F':'F[+F]F[-F][F]'}},
            'rule3': {'axiom': 'F', 'angle': 22.5, 'rule': {'F': 'FF-[-F+F+F]+[+F-F-F]'}},
            'rule4': {'axiom': 'X', 'angle': 20, 'rule': {'F': 'FF', 'X': 'F[+X]F[-X]+X'}},
            'rule5': {'axiom': 'X', 'angle': 25.7, 'rule': {'F': 'FF', 'X': 'F[+X][-X]FX'}},
            'rule6': {'axiom': 'X', 'angle': 22.5, 'rule': {'F': 'FF', 'X': 'F-[[X]+X]+F[+FX]-X'}}}
    

class OBJECT_OT_add_object(Operator, AddObjectHelper):
    
    def __init__(self):
        
    
        self.numCusRules = 1
    pcoll = bpy.utils.previews.new()
    iconPath = dirname(bpy.data.filepath) + '\Materials\Icon.png'
    pcoll.load("tree_icon", iconPath, 'IMAGE')
    icon = pcoll['tree_icon']
    """Create a new Tree"""
    bl_idname = "mesh.add_tree"
    bl_label = "Create Tree"
    bl_options = {'REGISTER', 'UNDO'}
    ruleItems = [('rule1', 'Rule 1', "Rule 1", icon.icon_id, 1),
                ('rule2', 'Rule 2', 'Rule 2', icon.icon_id, 2),
                ('rule3', 'Rule 3', 'Rule 3', icon.icon_id, 3),
                ('rule2', 'Rule 2', 'Rule 4', icon.icon_id, 4),
                ('rule5', 'Rule 5', 'Rule 5', icon.icon_id, 5),
                ('rule6', 'Rule 6', 'Rule 6', icon.icon_id, 6),
                ('custom', 'Custom', 'Custom Rule', icon.icon_id, 7)]
    
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
        min = 0.1)
    
    axiom: prop.StringProperty(
            name = 'Axiom',
            description = 'Axiom of the tree',
            default = 'F',
            maxlen = 1)
    angle: prop.FloatProperty(
        name = 'Angle',
        description = 'Rotation Angle',
        default = 0)
    customVariable1: prop.StringProperty(
        name = 'Variable',
        description = 'Variable')   
    customRule1: prop.StringProperty(
        name = 'Production Rule',
        description = 'Producion Rule')
    customVariable2: prop.StringProperty(
        name = 'Variable',
        description = 'Variable')   
    customRule2: prop.StringProperty(
        name = 'Production Rule',
        description = 'Producion Rule')
    customVariable3: prop.StringProperty(
        name = 'Variable',
        description = 'Variable')   
    customRule3: prop.StringProperty(
        name = 'Production Rule',
        description = 'Producion Rule')
    customVariable3: prop.StringProperty(
        name = 'Variable',
        description = 'Variable')   
    customRule3: prop.StringProperty(
        name = 'Production Rule',
        description = 'Producion Rule')
    numCusRules: prop.IntProperty(name='Number of Rules',
        description = 'Number of Custom Rules',
        default = 1,
        min = 1, max = 3)
    def add_rule(self):
        self.numCusRules += 1

    def draw(self, context):
        
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        layout.prop(self, 'rule')
        layout.prop(self, 'genNum')
        layout.prop(self, 'size')
        if self.rule == 'custom':
            
            row = layout.row()
            row.prop(self, 'axiom')
            row.prop(self, 'angle')
            box = layout.box()
            
            for num in range(1,self.numCusRules+1):
                row = box.row()
                a = ('customVariable' + str(num), 'customRule' + str(num))
                row.prop(self, a[0]) 
                row.prop(self, a[1])
            row = box.row()
            
            row.prop(self, 'numCusRules')

            
    
    def execute(self, context):
        
        initiateLSystem(self,context)
        return {'FINISHED'}

def add_object_button(self, context):
    pcoll = preview_collections["main"]
    icon = pcoll['tree_icon']
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="Tree",
        icon_value = icon.icon_id)
    

preview_collections = {}
def register():
    pcoll = bpy.utils.previews.new()
    iconPath = dirname(bpy.data.filepath) + '\Materials\Icon.png'
    pcoll.load("tree_icon", iconPath, 'IMAGE')
    preview_collections['main'] = pcoll
    bpy.utils.register_class(OBJECT_OT_add_object)
    bpy.utils.register_class(ADD_TREE_OT_add_rule)
    bpy.utils.register_class(ADD_TREE_OT_remove_rule)    
    bpy.types.VIEW3D_MT_add.append(add_object_button)
    LSystem.register()

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_object)
    bpy.utils.unregister_class(ADD_TREE_OT_add_rule)
    bpy.utils.unregister_class(ADD_TREE_OT_remove_rule)    
    bpy.types.VIEW3D_MT_mesh_add.remove(add_object_button)

    LSystem.unregister()
if __name__ == "__main__":
    register()
