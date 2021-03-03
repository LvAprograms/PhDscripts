import numpy as np
from matplotlib import pyplot as plt
from numpy.core.defchararray import index
import logging 

# logging.

basepath = "/media/luuk/alphav8x1/PhD/ErosionModelling/ChenFDSPMseries/"
prefix = "/sfc_"
extension = ".vtk"
models = ["vel1k1"]
datadict = {0: "coordinates", 1:"elevation", 2: "horz_vel_x", 3: "horz_vel_z", 4:"dhdt_advection", 5: "dhdt_uplift", 6:"dhdt_ers_sed",
            7: "base_diffusivity", 8: "eff_cell_diffusivity"}

class ExhumationCalculator(object):

    def __init__(self, model, nx ,nz, xsize, zsize):
        self.m = model
        self.nx, self.nz = nx, nz
        self.xsize, self.zsize = xsize, zsize
        self.npoints       = 0
        self.filerange = (10, 2410, 10)
        self.coords        = []
        self.elevation     = [] # elevation in meters
        self.horz_vel_x    = [] # horizontal velocity in x direction [m/s]
        self.horz_vel_z    = [] # horizontal velocity in z direction [m/s]
        self.dhdt_advect   = [] # change rate of elevation due to advection [m/s]
        self.dhdt_uplift   = [] # vertical velocity in y direction [m/s]
        self.dhdt_ers_sed  = [] # change rate of elevation due to erosion/sedimentation [m/s?]
        self.base_diff     = [] # base diffusivity (mostly constant) [m2/s]
        self.eff_cell_diff = [] # effective diffusivity, constant if base_diff is constant [m2/s]
        self.data          = []
        self.times         = self.read_time()
        self.uplift = []
        for i in range(self.filerange[0], self.filerange[1], self.filerange[2]):
            self.clear_for_next_step()
            self.read_data(i)
            self.process_data(str(i))
            # if i % 100 == 0:
            self.visualise(i)

    def read_time(self):
        times = {"0": [0, 0.0]} # step = [cumulative time, incremental timestep]
        i = 0
        with open(basepath + self.m + "/times.txt",'r') as f:
            for line in f.readlines():
                line = line.split()
                if int(line[0]) % 10 == 0 and int(line[0]) < self.filerange[1] and line[0] not in list(times.keys()):
                    i += 10
                    times[line[0]] = [float(line[1]), float(line[1]) - times[str(i-10)][1]]
        return times

    def read_data(self, i):
        filepath = basepath + self.m + prefix + self.m + "_" + str(i) + extension
        with open(filepath, 'rb') as f:
            j = 0
            linelength = 0
            lengths = []
            switches = [0]
            increments = []
            whichdata = 0
            self.data = f.readlines()
            for line in self.data:
                line = line.split() if type(line) != list else line
                if len(line) > 0:
                    if len(line) != linelength:
                        linelength = len(line)
                        # print(line, j, linelength)
                        switches.append(j)
                    if j == 4:
                        self.npoints = int(line[1])
                    if line[0] == b'POINTS':
                        # coordinates will follow
                        self.fill_array(j+1, whichdata)
                        self.coords = np.array(self.coords)
                        whichdata += 1
                    if line[0] == b'SCALARS':
                        # data will follow
                        self.fill_array(j+2, whichdata)
                        whichdata += 1
                j += 1
            # print(switches)
            # increments = [switches[k] - switches[k-1] for k in range(1, len(switches))]
            # print(increments)
            
    def fill_array(self, indexstart, which):
        # print("Attempting to fill array {}".format(datadict[which]))
        for k in range(indexstart, indexstart + self.npoints):
            self.data[k] = self.data[k].split()
            if which == 0 and len(self.coords) < 1:
                self.coords.append(self.data[k])
            elif which == 1:
                self.elevation.append(float(self.data[k][0]))
            # elif which == 2:
            #     self.horz_vel_x.append(float(self.data[k][0]))
            # elif which == 3:
            #     self.horz_vel_z.append(float(self.data[k][0]))
            elif which == 4:
                self.dhdt_advect.append(float(self.data[k][0]))
            elif which == 5:
                self.dhdt_uplift.append(float(self.data[k][0]))
            elif which == 6:
                self.dhdt_ers_sed.append(float(self.data[k][0]))
            else:
                # print("We are not interested in this quantity")
                break
        # print("Done\n")
    
    def process_data(self, when):
        # loop over points, add uplift * dt
        dt = self.times[when][1] * 60 * 60 * 24 * 365.25
        if when == '10':
            self.uplift = [val * dt for val in self.dhdt_uplift]
        else:
            for i, val in enumerate(self.dhdt_uplift):
                self.uplift[i] += val * dt
        print("Calculating uplift for time {}".format(self.times[when][0]))

    def clear_for_next_step(self):
        self.data = []
        self.elevation = []
        self.horz_vel_x = []
        self.horz_vel_z = []
        self.dhdt_uplift = []
        self.dhdt_advect = []
        self.dhdt_ers_sed = []

    def visualise(self,i):
        fig, ax = plt.subplots()
        I = ax.imshow(np.reshape(self.uplift, (501, 501)), vmin=0, vmax = 20000, cmap='Greens')
        C = plt.colorbar(I)
        plt.xlabel("Horizontal distance in x direction [2 km]")
        plt.ylabel("Horizontal distance in z direction [2 km]")
        C.set_label("Cumulative uplift [m]")
        # plt.pause(0.001)
        plt.title("Uplift at step {}, time = {} years".format(i, self.times[str(i)][0]))
        plt.savefig(basepath+self.m +"/uplift_{:04d}.png".format(i))


if __name__ == "__main__":
    EC = ExhumationCalculator(models[0], nx=501, nz=501, xsize = 1e6, zsize=1e6)
    print(EC.coords[0], sum(EC.elevation) / EC.npoints)
    # EC.visualise()
    plt.show()