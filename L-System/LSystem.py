import bpy
import bmesh
from math import radians, log, pow
import mathutils
from os.path import dirname
from random import randint, choice

class LSystem:
    def __init__(self, rule, generation, size):
        self.rule = rule
        self.generation = generation
        self.size = size

def register():
    bpy.utils.register_class(LSystem)
def unregister():
    bpy.utils.unregister_class(LSystem)
    