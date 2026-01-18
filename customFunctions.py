from math import pow
def clamp(input,min,max):
    if input>max:
        input=max
    elif input<min:
        input=min
    return input
def curveControl(input,exponet):
    invert=1
    if input<0:
        input=abs(input)
        invert=-1
    input=clamp(input,0,1)
    variable=pow(input,exponet)*invert
    return variable