import turtle
import keyboard
from random import randint

def processString(word):
  newstr = ''
  for character in word:
    newstr = newstr + applyRules(character)
    
  return newstr
  
  
def applyRules(character):
   
    
    newstr = ''
    #if character == 'A':
    #    newstr = 'B-F+CFC+F-D&F∧D-F+&&CFC+F+B//'
    #elif character == 'B':
    #    newstr = 'A&F∧CFB∧F∧D∧∧-F-D∧|F∧B|FC∧F∧A//'
    #elif character == 'C':
    #    newstr = '|D∧|F∧B-F+C∧F∧A&&FA&F∧C+F+B∧F∧D//'
    #elif character == 'D':
    #    newstr = '|CFB-F+B|FA&F∧A&&FB-F+B|FC//'
    #else:
    #    newstr = ''
    #return newstr
    #if character == 'X':
    #    newstr = 'F[+X]F[-X]+X'
    #elif character == 'F':
    #    newstr = 'FF'
    #else:
    #    newstr = ''
    #return newstr
    #newstr = ''
    #if character == 'F':
    #    newstr = 'S/////F'
    #elif character == 'A':
    #    newstr = '[&FL!A]/////;[&FL!A]???????;[&FL!A]'
    #elif character == 'S':
    #    newstr = 'FL'
    #else:
    #    newstr = character
    #return newstr

  #newstr = ''
    
    #if character == 'F':
      #newstr = 'FF'
    #    newstr = 'F[+F]F[-F]F'
    #elif character == 'X':
    #  rand = randint(0,1)
    #  if rand == 0:
    #    newstr = 'F-[[X]+X]+F[+FX]-X'
    #  elif rand == 1:
    #    newstr = 'F+[[X]-X]-F[-FX]+X'
    #else:
    #  newstr = character
    #return newstr
  
      
    if character == 'F':
        newstr = 'FF'
      #newstr = 'F[+FL]F[-FL]F'
    elif character == 'X':
        #rand = randint(0,1)
        #if rand == 0:
        #    newstr = 'F-[[XL]+X]+F[+FXL]-XL'
        #elif rand == 1:
        #    newstr = 'F+[[XL]-X]-F[-FXL]+XL'
        newstr = 'F[+XL][-XL]FX'
    else:
      newstr = character
    return newstr
def createSystem(iters, axiom):
  startString = axiom
  endString = ''
  
  for i in range(iters):
    endString = processString(startString)
    startString = endString
  return endString
     
def drawLsystem(t, word, angle, distance):
  stack = []
  heading = t.heading()
    
  for character in word:
    print(stack)
    #print(character)
    t.pd()
    if character == 'F':
      t.forward(distance)
    elif character == '+':
      t.left(angle)
      
    elif character == '-':
      t.right(angle)
      
    elif character == '[':   
      stack.append((t.position(), t.heading()))
      
    elif character == ']':
      colors = ['#b9c21d', '#90a900', '#547b01', '#304c02', 'green', '#f4d200', '#e68828']

      t.fillcolor(colors[randint(0,len(colors) -1)])
      t.begin_fill()
      t.forward(distance) # draw base

      t.left(90)
      t.forward(distance)
 
      t.left(135)
      t.forward(distance)
      t.end_fill()
      t.pu()
      position, heading = stack.pop()
      t.goto(position[0], position[1])
      t.setheading(heading)
      
    
      
def main():
  
  word = createSystem(7, 'X')
  print(word)
  
  angle = 25.7
  distance = 5
  turtle.hideturtle()
  t = turtle
  wn = turtle.Screen()
  #t.hideturtle()
  #t.clear()
  #t.up()
  t.pu()
  wn.screensize(1280,720)
  wn.setup(width=1.0,height=1.0,startx=None, starty=None)
  #t.screensize(1280,720)
  t.goto(0,-t.screensize()[1]/2)
  t.setheading(90)
  print(t.screensize())
  #t.down()
  t.speed('fastest  ')
  #t.heading(0)
  drawLsystem(t, word, angle, distance)
  #while (True):
  #  if keyboard.is_pressed('q'):
  #    break
if __name__ == "__main__":
  main()