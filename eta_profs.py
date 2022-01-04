from matplotlib import pyplot as plt

class ViscProf(object):
    def __init__(self, fig=None, axis=None, name=None) -> None:
        super().__init__()
        if axis == None:
            self.fig, self.ax = plt.subplots()
        else:
            self.fig, self.ax = fig, axis
        self.name= name
        self.handles = []
        self.d = {}

    def read_data(self, file):
        with open(file, 'r') as f:
            for i, line in enumerate(f.readlines()):
                data = line.strip('\n').split(',')
                if i == 0:
                    for k in data:
                        self.d[k] = []
                else:
                    data = [float(d) for d in data]
                    self.d['"viscosity"'].append(data[2])
                    self.d['"temperature"'].append(data[1]-273)                    
                    self.d['"Points:2"'].append(data[-2]/1e3)

    def plot(self, name):
        if name=="IND":
            etaclr=(0.4,0.3,0.3)
            tclr = etaclr
        else:
            etaclr=(0.8, 0.6, 0.6)
            tclr=etaclr
        self.ax.semilogx(self.d['"viscosity"'], self.d['"Points:2"'], color=etaclr,  linewidth=2, label="{}".format(name))
        ax2 = self.ax.twiny()
        ax2.set_xlabel("T [deg C]")
        self.ax.set_xlabel("Effective viscosity [Pa s]")
        self.ax.set_ylabel("Depth [km]")
        self.ax.set_ylim([0, 200])
        line1 = ax2.plot(self.d['"temperature"'], self.d['"Points:2"'], color=tclr, linewidth=2, label="{}".format(name))
        self.handles.append(line1)
    
    def add_plot(self, file, name):
        self.read_data(file)
        self.plot(name)

    def save_figure(self):
        self.ax.legend(loc="lower center")
        plt.gca().invert_yaxis()
        plt.savefig("{}.png".format(self.name), res="300 dpi")

if __name__=="__main__":
    fig, ax = plt.subplots()
    VP = ViscProf(fig=fig, axis=ax, name="vel2k2")
    VP.add_plot("/media/luuk/alphav8x1/PhD/ErosionModelling/ChenFDSPMseries/vel2k2/eta_T_indenter_vel2k2/eta_ind.csv", "IND")
    VP.add_plot("/media/luuk/alphav8x1/PhD/ErosionModelling/ChenFDSPMseries/vel2k2/eta_T_eur_vel2k2/eta_eur.csv","EUR")
    VP.save_figure()
    fig, ax = plt.subplots() 
    VP = ViscProf(fig=fig, axis=ax, name="strongzones")
    VP.add_plot("/media/luuk/alphav8x1/PhD/ErosionModelling/strongzones/no_eclo/eta_ind.csv", "IND")
    VP.add_plot("/media/luuk/alphav8x1/PhD/ErosionModelling/strongzones/no_eclo/eta_eur.csv","EUR")
    VP.save_figure()