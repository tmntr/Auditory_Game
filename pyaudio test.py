import pygame

pygame.mixer.init()

# Create Sound and Channel instances.
sound0 = pygame.mixer.Sound('pianoc.wav')
channel0 = pygame.mixer.Channel(0)

# Play the sound (that will reset the volume to the default).
channel0.play(sound0)
# Now change the volume of the specific speakers.
# The first argument is the volume of the left speaker and
# the second argument is the volume of the right speaker.
channel0.set_volume(0.0, 1.0)


'''pygame.mixer.music.load('pianoc.wav')
pygame.mixer.music.play(0)'''

#playsound.playsound('pianoc.wav')