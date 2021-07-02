import sys 

def cmyr2ms(speed):
    result = speed /( 3600 * 24 * 365.24 * 100) 
    # print("{} cm/yr can be converted to {} m/s".format(speed,result))
    return result

class UpLowBoundaryFluxMaster(object):
    def __init__(self, file, air_thickness = 20e3) -> None:
        self.input={}
        self.input['data'] = []
        self.process_input(file)
        for k,v in self.input.items():
            print(k, v)
        print("is input data correct?")
        self.calculate_fluxes(air_thickness)
    
    def process_input(self, file):
        print("reading bcinput.dat...")
        with open(file) as f:
            for line in f.readlines():
                l = line.split()
                if l[0] == 'xsize':
                    self.input['xsize'] = float(l[1])
                    self.input['dx'] = self.input['xsize']  / (int(l[3]) - 1)
                elif l[0] == 'ysize':
                    self.input['ysize'] = float(l[1])
                    self.input['dy'] = self.input['ysize']  / (int(l[3]) - 1)
                elif l[0] == 'zsize':
                    self.input['zsize'] = float(l[1])
                    self.input['dz'] = self.input['zsize']  / (int(l[3]) - 1)
                elif l[0] == 'permeable':
                    self.input['permeable'] = int(l[1])
                elif l[0][:1].isdigit():
                    self.input['data'].append([float(l[i]) for i in range(len(l))])
                # print(l)
    
    def calculate_fluxes(self, air_thickness):
        print("calculating upper and lower fluxes using push area times (average) push velocity")
        d = self.input['data']
        air_in = 0
        other_out = 0
        for item in d:
            x0 = item[0]
            x1 = item[1]
            y0 = item[2]
            y1 = item[3]
            z0 = item[4]
            z1 = item[5]
            v0 = item[6]
            v1 = item[7]
            if x1 != x0:
                air_in += air_thickness * (x1 - x0) * 1000 * 0.5 * (cmyr2ms(v0) + cmyr2ms(v1))
            elif z1 != z0:
                air_in += air_thickness * (z1 - z0) * 1000 * 0.5 * (cmyr2ms(v0) + cmyr2ms(v1))
            # print(air_in)
        air_out = air_in / (self.input['xsize'] * self.input['zsize'])
        if self.input['permeable']:
            print("permeable lower boundary detected")
            ynew = self.input['ysize'] + 99 * self.input['dy']
            other_out = (ynew - air_thickness) / air_thickness * air_out / 100
        else:
            print("no permeable lower boundary")
            other_out = (self.input['ysize'] - air_thickness) / air_thickness * air_out
        print("air out: {} m/s\t lower out: {} m/s".format(air_out, other_out))


if __name__=="__main__":
    UP = UpLowBoundaryFluxMaster("bcinput.dat")



