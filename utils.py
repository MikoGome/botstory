import random

#add some variance to the delay_time
def variance(time, percent):
    new_time = None
    if type(percent) is tuple:
        new_time = time * random.randrange(100-percent[0], 100+percent[1])/100
    else:
        new_time = time * random.randrange(100-percent, 100+percent)/100
    return new_time

def lerp(a, b, t):
    return a + (b - a) * t