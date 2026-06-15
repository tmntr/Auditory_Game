import numpy

testarray = numpy.array([[1,0],[2,2],[3,8],[4,2],[5,4],[6,3]])

sound = numpy.array([item[0] for item in testarray])
print(sound)
max = numpy.max(sound)
for i in range(0,len(sound)):
    sound[i] /= max
print(sound)