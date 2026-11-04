import math


#PHYSICAL IMPORTANT THINGS
#1: All angles in radians please.
#2: North is +y
#3: East is +x


#Creating a class that will allow basic spatial operations and comparisons to be made
class Physical:
    def __init__(self,x,y,w0=0.3,d=None):
        self.x = x
        self.y = y

        self.w0 = w0
        #will always be positive
        self.direction = d#%2*math.pi

    #Function to find cartesian distance between 2 objects
    def dist(self,op):
        if isinstance(op,Physical):
            dx = self.x - op.x
            dy = self.y - op.y
            return (dx**2 + dy**2)**0.5
        elif isinstance(op,RectPhysical):
            return op.dist(self)

    def disttopoint(self,x,y):
        dx = self.x - x
        dy = self.y - y
        return (dx**2 + dy**2)**0.5

    #N.B. this should ideally only be used with physical objects with directions.
    #Used to
    def get_bearing(self,op):
        dx = op.x - self.x
        dy = op.y - self.y
        return math.atan2(dx,dy)

    def get_bearing_to_point(self,x,y):
        dx = self.x - x
        dy = self.y - y

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


class RectPhysical:
    def __init__(self,x,y,w,h,w0=0.3):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.w0 = w0

    def vertices(self):
        x_coords = [self.x,self.x+self.w]
        y_coords = [self.y,self.y+self.h]
        points = []
        for x in x_coords:
            for y in y_coords:
                points.append((x,y))
        return points

    def withinx(self,op):
        return self.x < op.x < self.x+self.w

    def withiny(self,op):
        return self.y < op.y < self.y+self.h

    def findNearestPoint(self,op):
        if self.withinx(op):
            if self.withiny(op):
                return self.geddoudahere(op)
            else:
                if op.y > self.y + self.h:
                    return (op.x,self.y+self.h)
                else:
                    return (op.x,self.y)
        else:
            if self.withiny(op):
                if op.x > self.x + self.w:
                    return (self.x + self.w, op.y)
                else:
                    return (self.x, op.y)
            else:
                min = math.inf
                minindex = -1
                for i in range(4):
                    opdist = op.disttopoint(*self.vertices()[i])
                    if opdist < min:
                        minindex = i
                        min = opdist
                return self.vertices()[minindex]

    def dist(self, op):
        if self.withinx(op) and self.withiny(op):
            return -1
        else:
            return op.disttopoint(*self.findNearestPoint(op))

    def geddoudahere(self,op):
        '''

        Parameters
        ----------
        op: another Physical object that the rectangle wishes to displace from inside itself

        Returns
        -------
        nothing, but it does move the op to the closest position on one of the rectangle's edges. If this is called every frame, it should stop a player's physical from entering, effectively providing collision
        '''

        tempop = op.copy()

        disttobottom = tempop.y-self.y
        disttotop = tempop.y-self.y-self.h
        disttoleft = tempop.x-self.x
        disttoright = tempop.x-self.x-self.w

        left = disttoleft<disttoright
        up = disttotop<disttobottom

        if left and up:
            if disttoleft > disttotop:
                tempop.y = self.y+self.h
            else:
                tempop.x = self.x
        elif left:
            if disttoleft > disttobottom:
                tempop.y = self.y
            else:
                tempop.x = self.x
        elif up:
            if disttoright > disttotop:
                tempop.y = self.y+self.h
            else:
                tempop.x = self.x+self.w
        else:
            if disttoright > disttobottom:
                tempop.y = self.y
            else:
                tempop.x = self.x+self.w
        return (tempop.x,tempop.y)




class PhysHead:
    def __init__(self,centre,lear,rear,d=0.0):

        self.centre = centre
        self._lear = lear
        self._rear = rear

        self.direction = d

    def rotate(self,amount):
        self.direction += amount
        self.direction %= 2*math.pi


    @property
    def lear(self):
        leardistance = self.centre.dist(self._lear)
        learbearing = self.centre.get_relative_bearing(self._lear)
        xcoord = self.centre.x + leardistance*math.sin(learbearing+self.direction)
        ycoord = self.centre.y + learbearing*math.cos(learbearing)


        return Physical(xcoord,ycoord,0.02,learbearing)

    @property
    def rear(self):
        reardistance = self.centre.dist(self._rear)
        rearbearing = self.centre.get_relative_bearing(self._rear)
        xcoord = self.centre.x + reardistance * math.sin(rearbearing + self.direction)
        ycoord = self.centre.y + rearbearing * math.cos(rearbearing)

        return Physical(xcoord, ycoord, 0.02, rearbearing)


if __name__ == '__main__':
    rectangle = RectPhysical(0,0,4,2)
    point = Physical(5,3)
    print(rectangle.findNearestPoint(point))