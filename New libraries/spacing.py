import math


#PHYSICAL IMPORTANT THINGS
#1: All angles in radians please.
#2: North is +y
#3: East is +x


#Creating a superclass that will allow basic spatial operations and comparisons to be made
class Physical:
    def __init__(self,x,y,w0=0.3,d=None):
        self.x = x
        self.y = y
        self.w0 = w0
        #will always be positive
        self.direction = d#%2*math.pi

    #Function to find cartesian distance between 2 objects
    def dist(self,op):
        dx = self.x - op.x
        dy = self.y - op.y
        return (dx**2 + dy**2)**0.5

    #N.B. this should ideally only be used with physical objects with directions.
    #Used to
    def get_bearing(self,op):
        dx = op.x - self.x
        dy = op.y - self.y
        return math.atan2(dx,dy)

    def rotate(self,amount):
        self.direction = (self.direction + amount) % 2*math.pi

    def moveabs(self,dx,dy):
        self.x += dx
        self.y += dy

    def movepolar(self,dforward,dright):
        self.moveabs(dright*math.cos(self.direction),dright*math.sin(self.direction))
        self.moveabs(dforward*math.sin(self.direction),dforward*math.cos(self.direction))

    #returns the angle bearing of the Other Physical taking the current physical's facing as north
    def get_relative_bearing(self,op):
        theta = 0
        bearing = self.get_bearing(op)
        theta = (bearing-self.direction)%(2*math.pi)
        return theta


    #Works out as a boolean whether another Physical is overall in front of this one
    def is_infront(self,op):
        if math.cos(self.get_relative_bearing(op)) > 0:
            return True
        else:
            return False

    #returns on a scale of -1 to 1 how "in front" the other Physical is: will be useful when ears begin to implement HRTFs
    def how_in_front(self,op):
        return math.cos(self.get_relative_bearing(op))