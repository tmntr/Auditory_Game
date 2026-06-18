class Thing:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def dist(self,other):
        return ((self.x-other.x)**2 + (self.y-other.y)**2)**0.5

class Ear(Thing):
    def __init__(self,x,y):
        super().__init__(x,y)

    def calculate_delay(self,emitter):
        return self.dist(emitter)/343

    def sound_factor(self,emitter):
        return min([1,1/self.dist(emitter)**2])

    def sound_profile(self,emitter):
        delay = self.calculate_delay(emitter)
        sound_factor = self.sound_factor(emitter)
        return (delay,sound_factor)

class Emitter(Thing):
    def __init__(self,x,y):
        super().__init__(x,y)

'''emitter = Emitter(0.175, 1)
ear1 = Ear(-0.35 / 2, 0)
ear2 = Ear(0.35 / 2, 0)

print(ear1.sound_profile(emitter))
print(ear2.sound_profile(emitter))

print(ear1.sound_factor(emitter))
print(ear2.sound_factor(emitter))'''