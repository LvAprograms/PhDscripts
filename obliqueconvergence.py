from math import sin, cos, sqrt, pi
import sys
def oblique(angle:int, resultant:float):
    horizontal = resultant * sin(angle*(pi/180))
    vertical = resultant * cos(angle*(pi/180))
    print("For an angle of {} degrees, the horizontal and vertical velocities should be {} and {} cm/yr".format(angle, horizontal, vertical))

if __name__=="__main__":
    if len(sys.argv) > 1:
        oblique(int(sys.argv[1]), float(sys.argv[2]))
    else:
        print("usage: python3 obliqueconvergence.py angle resultant velocity")
        exit()
