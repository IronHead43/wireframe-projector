#libraries
import turtle
import numpy as np

#functions

#Function that peforms linear transformations on given object
#takes input xyz, which if is a rotation represents the boolean value of which axis the object is being rotated parallel to
#if transformation is a dilation the x value will be whether it is enlarged (1) or shrunk (-1)
#if its a translation, it is the translation vector
#theta is only use if a rotation, it is the radians the object is being transformed by
#transformType represents whether a translation, rotation or dilation

def transformObject(x,y,z,theta,transformType):

    #access the vertices, object type (eg cube,cuboid) and size/scale of object
    global vertices, objectType, scale

    #check type of transformation
    if transformType=="rotate":

        #if rotate then check if parallel to xyz axis

        if x==True:
            transform=np.array([
                [1, 0, 0],
                [0, np.cos(theta), -np.sin(theta)],
                [0, np.sin(theta), np.cos(theta)]
            ])

        if y==True:
            transform=np.array([
            [np.cos(theta), 0, np.sin(theta)],
            [0, 1, 0],
            [-np.sin(theta), 0, np.cos(theta)]
        ])
            
        if z==True:
            transform=np.array([
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta), np.cos(theta), 0],
            [0, 0, 1]
        ])
    
        #apply transformation to vertices
        vertices=np.dot(vertices,transform.T)

    #if translation, add translation vector to vertices

    if transformType=="translate":
        transform=np.array([x,y,z
        ])
        vertices=vertices+transform
    
    #if dilate then scale object back to unit object, then dilate it by scale factor given
    if transformType=="dilate":
        vertices = vertices / scale
        scaleFactor=x
        scale+=scaleFactor
        vertices = vertices * scale
        
    

    #find objects edges between each vertex
    generateEdges()


def generateEdges():
    
    global vertices

    if objectType=="cube":
        edges = np.array([
            [vertices[0], vertices[1]],
            [vertices[1], vertices[2]],
            [vertices[2], vertices[3]],
            [vertices[3], vertices[0]],
            [vertices[4], vertices[5]],
            [vertices[5], vertices[6]],
            [vertices[6], vertices[7]],
            [vertices[7], vertices[4]],
            [vertices[0], vertices[4]],
            [vertices[1], vertices[5]],
            [vertices[2], vertices[6]],
            [vertices[3], vertices[7]]
        ])
    elif objectType=="cuboid":
        edges = np.array([
            [vertices[0], vertices[1]],  # Edge 0 to 1
            [vertices[0], vertices[2]],  # Edge 0 to 2
            [vertices[0], vertices[4]],  # Edge 0 to 4
            [vertices[1], vertices[3]],  # Edge 1 to 3
            [vertices[1], vertices[5]],  # Edge 1 to 5
            [vertices[2], vertices[3]],  # Edge 2 to 3
            [vertices[2], vertices[6]],  # Edge 2 to 6
            [vertices[3], vertices[7]],  # Edge 3 to 7
            [vertices[4], vertices[5]],  # Edge 4 to 5
            [vertices[4], vertices[6]],  # Edge 4 to 6
            [vertices[5], vertices[7]],  # Edge 5 to 7
            [vertices[6], vertices[7]]   # Edge 6 to 7
        ])
    elif objectType=="pyramid":
        edges = np.array([
            [vertices[0], vertices[1]],  # Edge 0 to 1 (Base)
            [vertices[1], vertices[3]],  # Edge 1 to 3 (Base)
            [vertices[3], vertices[2]],  # Edge 3 to 2 (Base)
            [vertices[2], vertices[0]],  # Edge 2 to 0 (Base)
            [vertices[0], vertices[4]],  # Edge 0 to 4 (Apex)
            [vertices[1], vertices[4]],  # Edge 1 to 4 (Apex)
            [vertices[2], vertices[4]],  # Edge 2 to 4 (Apex)
            [vertices[3], vertices[4]]
            ])
    
    drawObject(edges)

#draw each edge

def drawObject(edges):
    cube.clear()  # Clear the previous drawing

    for edge in edges:
        x1, y1 = edge[0][:2]
        x2, y2 = edge[1][:2]
        cube.penup()
        cube.goto(x1, y1)
        cube.pendown()
        cube.goto(x2, y2)

    screen.update()  # Update the screen with the new drawing


def createObject():
    global vertices, objectType
    if objectType=="cube":
        vertices = np.array([
            [-1, -1, -1],
            [ 1, -1, -1],
            [ 1,  1, -1],
            [-1,  1, -1],
            [-1, -1,  1],
            [ 1, -1,  1],
            [ 1,  1,  1],
            [-1,  1,  1]
        ])

    if objectType=="pyramid":
        a, h = 2, 3

        # Pyramid vertices (4 base corners + 1 apex)
        vertices = np.array([[-a, -a, 0],  # Base vertex 1
        [-a,  a, 0],  # Base vertex 2
        [ a, -a, 0],  # Base vertex 3
        [ a,  a, 0],  # Base vertex 4
        [ 0,  0, h]]) # Apex
        
    if objectType=="cuboid":
        # Dimensions of the cuboid (half-lengths along each axis)
        a, b, c = 2, 1, 3

        # Cuboid vertices centered at origin
        vertices = np.array([[-a, -b, -c],
            [-a, -b,  c],
            [-a,  b, -c],
            [-a,  b,  c],
            [ a, -b, -c],
            [ a, -b,  c],
            [ a,  b, -c],
            [ a,  b,  c]])


#object initialisation
objectType=input("What would you like to create? A cube/pyramid/cuboid: ")
scale=int(input("Enter the scale (1-100): "))
print("-----object initialised-----")
print("To view your object open up the new turtle window that has just appeared")
print("it can be controlled by using WASD to rotate around centre, arrow keys to move it, and =/- to increase/decrease scale")

# Set up the screen
screen = turtle.Screen()
screen.bgcolor("black")

# Create a turtle
cube = turtle.Turtle()
cube.speed(0) 
screen.tracer(0)
cube.hideturtle()

#create corresponding object

createObject()

#scale object 
vertices = vertices * scale

cube.color("white")   # Set the color of the trail to blue
cube.pensize(3)      # Set the thickness of the trail


generateEdges() # generate edges and draw object



screen.listen()
#rotate
screen.onkeypress(lambda: transformObject(True,False,False,0.1,"rotate"), "s") 
screen.onkeyrelease(lambda: transformObject(True,False,False,0.1,"rotate"), "s")
screen.onkeypress(lambda: transformObject(True,False,False,-0.1,"rotate"), "w")  
screen.onkeyrelease(lambda: transformObject(True,False,False,-0.1,"rotate"), "w")  
screen.onkeypress(lambda: transformObject(False,True,False,0.1,"rotate"), "d")  
screen.onkeyrelease(lambda: transformObject(False,True,False,0.1,"rotate"), "d")  
screen.onkeypress(lambda: transformObject(False,True,False,-0.1,"rotate"), "a")  
screen.onkeyrelease(lambda: transformObject(False,True,False,-0.1,"rotate"), "a")  
screen.onkeypress(lambda: transformObject(False,False,True,0.1,"rotate"), "v")  
screen.onkeyrelease(lambda: transformObject(False,False,True,0.1,"rotate"), "v")  #

#translate
screen.onkeypress(lambda: transformObject(0,1,0,0,"translate"), "Up")  
screen.onkeyrelease(lambda: transformObject(0,1,0,0,"translate"), "Up")
screen.onkeypress(lambda: transformObject(0,-1,0,0,"translate"), "Down")  
screen.onkeyrelease(lambda: transformObject(0,-1,0,0,"translate"), "Down")  
screen.onkeypress(lambda: transformObject(1,0,0,0,"translate"), "Right")  
screen.onkeyrelease(lambda: transformObject(1,0,0,0.1,"translate"), "Right")  
screen.onkeypress(lambda: transformObject(-1,0,0,-0.1,"translate"), "Left")  
screen.onkeyrelease(lambda: transformObject(-1,0,0,-0.1,"translate"), "Left")  
screen.onkeypress(lambda: transformObject(0,0,1,0.1,"translate"), "m")  
screen.onkeyrelease(lambda: transformObject(0,0,1,0.1,"translate"), "m")  

#dilate
screen.onkeypress(lambda: transformObject(1,0,0,0,"dilate"), "=")  
screen.onkeypress(lambda: transformObject(-1,0,0,0,"dilate"), "-")  

# Keep the window open and responsive
screen.mainloop()
