import math
#wav files represent the amplitude of the sound waves

PI = math.pi

#this will actually provide the attenuation coefficient/frequency^2, as it would be inelegant to recalculate for every
#frequency rather than just multiplying when necessary


profiles = {'air':{'dvc':1.85*10**-5,'density':1.204,'sos':340,'vv':0}}

def ac(substance):
    return attenuation_coefficient(profiles[substance]['dvc'],profiles[substance]['density'],profiles[substance]['sos'],profiles[substance]['vv'])

#alpha/f**2
def attenuation_coefficient(dvc,density,sos,vv = 0):
    return ((2*dvc+3/2*vv)*4*PI**2)/(3*density*sos)

#A(d) = A*math.exp(-ac*f**2*d)
#A(d)/A = math.exp(-ac*f**2*d)
#decibel reduction = 20*log(A(d)/A)
#= -20*ac*f**2*d*log(e)


def decibel_attenuation(ac,f,d):
    return -10*ac*(f**2)*d*math.log(math.e,10)
#actually, since it will then just be plugged back into the decibel reducer, why not just use the scale factor straight away?
def attenuate(ac,f,d):
    return math.exp(-ac*d*f**2)

def attenuate_scale_factor(ac,d):
    return math.exp(-ac*d)