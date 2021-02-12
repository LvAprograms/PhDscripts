from numpy import fromfile, array, mean, median, reshape, int16, concatenate
from math import floor, tan
from matplotlib import pyplot as plt
from scipy import ndimage
import sys

from scipy.ndimage import filters 


class SectionMaker(object):
    def __init__(self, filenames:list, xdir=True, fsize=None):
        """
        orientation 0: merge in EW direction, orientation 1: merge in NS direction
        """
        self.files = filenames
        self.data = None
        self.read_data()
        self.fig, self.axes = plt.subplots(2,1, figsize=(12,6))
        self.fsize = fsize
        self.I = self.topoimage()

    def read_data(self):
        if len(self.files) > 1:
            for f in self.files:
                d = fromfile(f, dtype=int16)
                d = reshape(d, (6000, 10800))
                if f == "h10g":
                    d = d[0:4000, 0:2000]
                else:
                    d = d[0:4000, 7000:]
                self.merge_data(d)
        else:
            d = fromfile(self.files[0], dtype=int16)
            d = reshape(d, (6000, 10800))
            d = d[0:1000, 0:2500]
            self.merge_data(d)

    def merge_data(self, data,xdir=1):
        if self.data is None:
            self.data = data
        else:
            self.data = concatenate((self.data, data), axis=xdir)

    def topoimage(self):
        if self.fsize is not None:
            self.smooth_topo()
        return self.axes[0].imshow(self.data, cmap='binary')
    
    def plot_slice(self, rowstart=0, colstart=0, rowend=0, colend=0):
        if rowend == 0:
            rowend =  self.data.shape[0]-rowend
        if colend == 0:
            colend = self.data.shape[1]-colend
        if rowstart==rowend:
            # EW profile
            self.axes[0].plot([colstart, colend],[rowstart, rowstart], 'ro-')
            self.axes[1].plot(self.data[rowstart, colstart:colend],'r')
        elif colstart==colend:
            # NS profile
            self.axes[0].plot([colstart, colstart],[rowstart, rowend], 'bo-')
            self.axes[1].plot(self.data[rowstart:rowend, colstart], 'b')
        else:
            # arbitrary profile
            self.axes[0].plot([colstart, colend], [rowstart, rowend], 'rx-')
            x, newarray = self.slice_data(rowstart, colstart, rowend, colend)
            self.axes[1].plot(x, newarray, 'r-')
            self.axes[1].set_aspect(5)
            self.axes[1].set_xlim([0, max(x)])
            self.axes[1].set_ylim([0, max(newarray)+0.5])

        
    def label_plots(self):
        self.axes[0].set_xlabel("EW distance [km]")
        self.axes[0].set_ylabel("NS distance [km]")
        self.axes[1].set_xlabel("Horizontal distance along profile [km]")
        self.axes[1].set_ylabel("Elevation [km]")
        self.axes[1].grid(b=True)
        self.fig.subplots_adjust(right=0.8)
        cbar_ax = self.fig.add_axes([0.7, 0.50, 0.05, 0.4])
        self.fig.colorbar(self.I, cax=cbar_ax)
        self.fig.suptitle("DEM (radial filtersize {}) and selected profile ".format(self.fsize))
        self.axes[1].set_title("Topography (vertical exaggeration 5x)")

    
    def slice_data(self, rs, cs, re, ce):
        """
        Should slice through the matrix. 
        """
        # calculate straight line
        # row = a*column + b
        # row(cs) = rs
        # row(ce) = re
        # a*cs + b = rs
        # a * ce + b = re
        # a * (cs - ce) = rs - re
        # a = (rs - re) / (cs - ce
        # insert back
        # b = rs - a * cs
        a = (rs - re) / (cs - ce)
        b = re - (a * ce)
        y = a = array([b + a * val for val in range(cs, ce+1)])
        newdata = []
        for i, val in enumerate(y):
            # in which grid cell are you? column = starting column + i, row = floor(y[i]) 
            ri = int(floor(val))
            ci = cs + i
            newdata.append(self.data[ri, ci]/1e3)
        return y-y[0], newdata

    def smooth_topo(self):
        if self.fsize is not None:
            self.data = ndimage.uniform_filter(self.data, size=self.fsize, mode='constant')
        else:
            pass


def showcase():
    SM = SectionMaker(['g10g'])
    # SM.plot_slice(rowstart=2700, colstart=4400,  rowend=2700, colend=5500) # EW profile through Hengduan Mountain Range
    # SM.plot_slice(rowstart=2000, colstart=5000,  rowend=4000, colend=5000) # NS profile through Hengduan Mountain Range
    SM.plot_slice(rowstart=250, colstart=950,  rowend=550, colend=1100) # arbitrary profile through Central Alps

    SM.label_plots()
    plt.show()

if __name__=="__main__":
    print("{} arguments were found".format(len(sys.argv) - 1))
    if len(sys.argv) <= 1:
        showcase()
    else:
        ip = input("If you want a smoothed topography, enter filter size in km. Hit enter otherwise: ")
        filtersize = int(ip) if len(ip) > 0 else None
        SM = SectionMaker(['g10g', 'h10g'], fsize=filtersize)
        rs, cs, re, ce = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
        SM.plot_slice(rowstart=rs, colstart=cs,  rowend=re, colend=ce) # arbitrary profile through the area

        SM.label_plots()
        plt.show()

    