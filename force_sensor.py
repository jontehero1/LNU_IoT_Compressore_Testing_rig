import machine
from time import sleep_ms

pin = machine.ADC(28)
lever = 0.0584
R = 3
def read_moment():
    
    value = pin.read_u16()
    
    force = value#Conversion from value to force not yet coded
    
    M2 = force * lever
    M1 = -M2/R
    Mc = -(M2*(-1 + R))/R
    
    
    return M1, Mc, M2
