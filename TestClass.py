import bpy



class printer():
    def printTest():
        print(45)




def register():
    bpy.utils.register_class(printer)

def unregister():
    bpy.utils.unregister_class(printer)


