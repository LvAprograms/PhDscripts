"""
SimpleStrProf
@author: Luuk van Agtmaal, december 2021
purpose: get rid of strength profile complexity/errors by constructing them for you from a simple input text file.
input file format:
layername   plateID  n    Ea     Ad    rho0 Va  mu0 mu1 zstart zend Tstart Tend, where you can put - in Tstart/end to signify None
"""

from matplotlib import pyplot as plt
from math import exp
from copy import copy


class Layer(object):
    """
    Layer class that holds the rheological properties of the rocks, as well as the layer boundary conditions.
    :params:
    n              : stress exponent
    Ea             : Activation energy [J/mol]
    Ad             : pre-exponential [Pa^(-n) s]
    rho0           : reference density [kg/m3]
    Va             : activation volume [cm^3/mol]
    sinphi_min, max: minimum and maximum friction coefficients #TODO: add Pf/Ps!?
    zstart/end     : start and end depth in km of layer
    Tstart/end     : absolute temperature at start and end of layer
    C0             : cohesion, relatively unimportant so kept constant here
    """
    def __init__(self, n, Ea, Ad, rho0, Va, sinphi_max, sinphi_min, zstart, zend, Tstart=None, Tend=None, C0=1e6) -> None:
        super().__init__()
        self.C0 = C0
        self.n = n
        self.Ea = Ea
        self.Ad = Ad
        self.Va = Va
        self.rho0 = rho0
        self.sinphi_min = sinphi_min
        self.sinphi_max = sinphi_max
        self.zstart =zstart
        self.zend = zend
        self.Tstart = Tstart
        self.Tend = Tend
    
    def __repr__(self) -> str:
        return "{} {} {} {}".format(self.zstart, self.zend, self.Tstart, self.Tend)

    

class Geotherm(object):
    """
    Geotherm class that holds all necessary properties to make geotherms for each plate. 
    :params:
    Tmoho  : Moho temperature [K]
    Tconrad: upper/lower crustal interface temperature [K]
    Tsurf  : surface temperature [K]
    TLAB   : Lithosphere-Asthenosphere boundary temperature [K]
    name   : name of the profile
    """
    def __init__(self, Tmoho, Tconrad, Tsurf, TLAB, name='test') -> None:
        super().__init__()
        self.Tmoho = Tmoho
        self.Tconrad= Tconrad
        self.Tsurf=Tsurf
        self.TLAB = TLAB
        self.T = [Tsurf]
        self.name = name

    def make_geotherm(self, z, zconrad, zmoho, zlab):
        """
        Construct the geotherm from depth vector z with defined interface levels
        :params:
        z      : depth vector in km
        zconrad: depth of upper/lower crust interface
        zmoho  : depth of Moho
        zlab   : depth of lithosphere-asthenosphere boundary
        """
        if self.Tmoho is None:  # determine if we can just use one gradient for whole lithosphere
            self.T = [self.Tsurf + i * (self.TLAB - self.Tsurf) / (zlab-1) for i in range(zlab)]
            for i in range(zlab, len(z)):
                self.T.append(self.T[i-1] + 0.5)  # asthenosphere, so adiabatic gradient
            self.plot(z, zmoho)
            return
        # if there is a Moho, use multiple gradients
        for i in range(len(z)):
            if self.Tconrad is not None: # if a upper/lower crust interface is defined, use another gradient
                if 0 < i < zconrad:
                    self.T.append(self.T[i-1] + (self.Tconrad - self.Tsurf) / (zconrad))
                elif zconrad <= i < zmoho:
                    self.T.append(self.T[i-1] + (self.Tmoho - self.Tconrad) / (zmoho - zconrad - 1))
            else:
                if 0 < i < zmoho:
                    self.T.append(self.T[i-1] + (self.Tmoho - self.Tsurf) / (zmoho))
            if zmoho <= i < zlab :
                self.T.append(self.T[i-1] + (self.TLAB - self.Tmoho) / (zlab - zmoho - 1))
            if i >= zlab and i < len(z):
                self.T.append(self.T[i-1] + 0.5)  # asthenosphere, so adiabatic gradient


    def plot(self, z, zmoho):
        """
        plots a quick and dirty geotherm for future reference
        """
        plt.figure()
        plt.plot(self.T, z, 'd--')
        print("Moho temperature for plate {} = {}°C".format(self.name, self.T[zmoho] - 273))
        plt.gca().invert_yaxis()
        plt.savefig("/home/luuk/Documents/ETH/strprofs/{}con{}mo{}s{}lab{}.png".format(self.name, self.Tconrad, self.Tmoho, self.Tsurf, self.TLAB))

    # def __repr__(self) -> str:
    #     return "{} {} {} {}".format()


class StrengthProfile(object):
    def __init__(self, name:str, rheofile:str, eii:float) -> None:
        """
        Main class of this program, which will construct the strength profiles and save them to a predefined location
        :params:
        name     : name of the model
        rheofile : name of the input file
        eii      : strainrate used for ductile calculation
        """
        super().__init__()
        self.name = name
        self.rf = rheofile
        self.eii = eii
        self.layers = {}    # dictionary that will hold all layers for each plate
        self.z = range(200) # initialise depth vector, assume 200 km depth. 
        self.GT = {}        # will contain geotherms for each plate
        self.P = {}         # will contain pressure for each plate
        self.Sbrit = {}     # will contain brittle strength of each plate  
        self.Sduct = {}     # will contain ductile strength of each plate
        self.strength = {}  # will contain the minimum of ductile and brittle strength for each plate
        self.setup()        # read input, calculate and plot all parameters

    def read_input(self):
        """
        Reads input file `self.rheofile` and fills up the layers dictionary.
        """
        with open("{}.txt".format(self.rf), 'r') as f:
            for line in f.readlines():
                if not line.startswith('#'): # check for comment (first line)
                    line = line.split()
                    name = line[0]
                    plate = line[1]
                    if plate not in self.layers.keys(): # make sure dictionary keys are not overwritten
                        self.layers[plate] = {} 
                    d = []
                    for i in range(2, len(line)):
                        if line[i] != '-':  # this means None temperatures in input file
                            v = float(line[i])
                        else:
                            v = None
                        d.append(v)
                    # now time to add the Layer object    
                    self.layers[plate][name] = Layer(n=d[0], Ea=d[1], Ad=d[2], rho0=d[3], Va=d[4], sinphi_min=d[5], 
                                                     sinphi_max=d[6], zstart=int(d[7]), zend=int(d[8]), Tstart=d[9], Tend=d[10])
        # add dummy lower crust if none is provided                                             
        for plate, layer in self.layers.items():
            if "LC" not in layer.keys():
                lp = self.layers[plate]["UC"]
                self.layers[plate]["LC"] = Layer(n=lp.n, Ea=lp.Ea, Ad=lp.Ad, rho0=lp.rho0, Va=lp.Va, sinphi_min=lp.sinphi_min, sinphi_max=lp.sinphi_max, zstart=lp.zend, zend=lp.zend)
        for plate in self.layers.keys():
            self.layers[plate]["AM"] = copy(self.layers[plate]["LM"])
            self.layers[plate]["AM"].zstart = self.layers[plate]["LM"].zend
            self.layers[plate]["AM"].zend = len(self.z)
        

    
    def brittle_strength(self, plate):
        """
        Calculates brittle strength for a specific plate
        """
        # initialise vectors with zeros
        self.P[plate]     = [0 for _ in self.z]
        self.Sbrit[plate] = [0 for _ in self.z]

        #calculate brittle strength sigma_n = C0 + sin(phi) * (1 - Pf/Ps) * P
        for l in self.layers[plate].values():
            for z in range(l.zstart, l.zend):
                if  z > 0:
                    self.P[plate][z] = (self.P[plate][z-1] + 9.81 * l.rho0 * 1000)
                else:
                    self.P[plate][z] = 0
                self.Sbrit[plate][z] = (l.C0 + l.sinphi_max*self.P[plate][z])
        for z in range(self.layers[plate]["LM"].zend, len(self.z)):
            self.P[plate][z] = (self.P[plate][z-1] + 9.81 * self.layers[plate]["LM"].rho0 * 1000)
            self.Sbrit[plate][z] = self.layers[plate]["LM"].C0 + self.layers[plate]["LM"].sinphi_min * self.P[plate][z]
    
    def ductile_strength(self, plate):
        """
        Calculates ductile strength for one plate
        """ 
        # calculate ductile strength according to (eii * Ad * exp((Ea + Va*P) / (R*T)) ** (1 / n)
        self.Sduct[plate] = [0 for _ in self.z] 
        for l in self.layers[plate].values():
            for z in range(l.zstart, l.zend):
                exponential = exp((l.Ea ) / (8.3147 * self.GT[plate].T[z])) # + l.Va * 1e-6 * self.P[plate][z] is left out because otherwise the ductile strenght is weirdly high. WHY? PRessure increases more than temperature in the asthenosphere
                pre_exp = self.eii * l.Ad 
                self.Sduct[plate][z] = (pre_exp * exponential) ** (1 / l.n)
        # for z in range(self.layers[plate]["LM"].zend, len(self.z)):
        #     l = self.layers[plate]["LM"]
        #     exponential = exp((l.Ea + l.Va * 1e-6 * self.P[plate][z]) / (8.3147 * self.GT[plate].T[z]))
        #     pre_exp = self.eii * l.Ad 
        #     self.Sduct[plate][z] = (pre_exp * exponential) ** (1 / l.n)
            # self.Sduct[plate][z] = (self.eii * self.layers[plate]["LM"].Ad * exp((self.layers[plate]["LM"].Ea + self.layers[plate]["LM"].Va * 1e-6 * 
            #                         self.P[plate][z]) / (8.3147 * self.GT[plate].T[z]))) ** (1 / self.layers[plate]["LM"].n)
    #TODO: the ductile strength is weirdly high down low. Try to fix tomorrow?

    def calc_strength(self, plate):
        """
        Calculate strength as an easy min/max comparison for one plate
        """
        self.strength[plate] = []
        for i in self.z:
            if self.Sbrit[plate][i] <= self.Sduct[plate][i]:
                self.strength[plate].append(self.Sbrit[plate][i])
            else:
                self.strength[plate].append(self.Sduct[plate][i])

    def setup(self):
        """
        Function calling the correct functions in order
        """
        self.read_input()
        for plate in self.layers.keys(): # for each plate, make geotherm then calculate brittle, ductile and final strength. Then plot. 
                    # make the geotherm of this plate
            self.GT[plate] = Geotherm(self.layers[plate]["LC"].Tend, self.layers[plate]["UC"].Tend, 
                self.layers[plate]["UC"].Tstart, self.layers[plate]["LM"].Tend, name=plate) 
            self.GT[plate].make_geotherm(z=self.z, zconrad=self.layers[plate]["UC"].zend, zmoho=self.layers[plate]["LC"].zend, 
                zlab=self.layers[plate]["LM"].zend)
            self.brittle_strength(plate)
            self.ductile_strength(plate)
            self.calc_strength(plate)
        self.plot()
    
    def plot(self):
        """
        Loop over each plate and plot the strength profile (and its constituents)
        """
        for plate in self.strength.keys():
            fig, ax = plt.subplots()
            ax.plot(self.P[plate], self.z, 'k--', label="Pressure")
            ax.plot(self.Sbrit[plate], self.z, 'r--', label="brittle")
            ax.plot(self.Sduct[plate], self.z, 'm--', label="ductile")
            # ax.plot(self.strength[plate], self.z, 'b-', label="strength")
            ax.set_xlim([0, 1e9])
            ax.set_ylim([0, max(self.z)])
            ax.set_xlabel("Differential stress [Pa]")
            ax.set_ylabel("Depth [km]")
            plt.gca().invert_yaxis()
            plt.legend()
            plt.savefig('/home/luuk/Documents/ETH/strprofs/strength_{}_{}.png'.format(self.name, plate))
            print("saved {}_{} strprof".format(self.name, plate))


if __name__== "__main__":
    SP = StrengthProfile(name="tst", rheofile="koeienschillen", eii=1e-14)



