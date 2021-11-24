
import bpy
import bmesh
from math import radians, log, pow
import mathutils
from os.path import dirname
from random import randint, choice




class LSystem:
    # Initialize L-System Class
    def __init__(self, system, generation, size):
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
        # Generate the word
        self.word = self.initSystem()
        
        print(self.word)
    # Initialize system
    def initSystem(self):
        # Set the axiom as the first character of the L-System word
        startString = self.selSystem['axiom']
        endString = ''
        # For number of generations that user has chosen, generate the process the word
        for gen in range(self.generation):
            endString = self.processString(startString)
            startString = endString
        return self.wordCleaner(self.rotationReplacer(endString))

    # Generate the L-System word 
    def processString(self, word):
        newstr = ''
        # Go through each character of the word and apply the rules on it
        for character in word:
            newstr = newstr + self.generateWord(character)
    
        return newstr

    # Apply the production rule(s) on the given character
    def generateWord(self, character):
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

    def rotationReplacer(self, word):
        rotators = ['/','\\','&','^']
        newstr = ''
        
        for i in range(0, len(word)):
            if word[i] == '+' or word[i] ==  '-':
               
                c = choice(rotators)
                newstr += c
               
            else:
                newstr += word[i]

        return newstr

    def wordCleaner(self, word):
        word = word.replace('X', '')
        word = word.replace('[+]', '')
        word = word.replace('[-]', '')
        return word

def register():
    bpy.utils.register_class(LSystem)
def unregister():
    bpy.utils.unregister_class(LSystem)
    

l = LSystem('system5', 7, 0.5)