from scipy.fft import fft,ifft,fftfreq
import numpy

test = numpy.array([0.3,-0.1,-0.2,-1])
test2 = numpy.array([0.6,-0.2,-0.4,-2])
test3 = numpy.array([1,0,-1,0,1,0,-1,0])
test4 = numpy.array([1+1,0+-1,-1+1,0+-1,1+1,0+-1,-1+1,0+-1])


x = fft(test)


print(fftfreq(16,d=1/44000))
print(fft(test,16))
