

class i3Box(object):
    def __init__(self, xbeg, xend, ybeg, yend, zbeg, zend):
        self.x0145 = xbeg
        self.x2367 = xend
        self.y0246 = ybeg
        self.y1357 = yend
        self.z0123 = zbeg 
        self.z4567 = zend
    
    def __repr__(self):
        return "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\n{12}\t{13}\t{14}\t{15}\t{16}\t{17}\t{18}\t{19}\t{20}\t{21}\n\n".format(self.x0145, 
        self.y0246, self.z0123, self.x0145, self.y1357, self.z0123, self.x2367,self.y0246, self.z0123, self.x2367, self.y1357, self.z0123, self.x0145, self.y0246,
        self.z4567, self.x0145, self.y1357, self.z4567, self.x2367, self.y0246, self.z4567, self.x2367, self.y1357, self.z4567)


class i3Boxwriter(object):
    def __init__(self, boxfile):
        self.f = boxfile
        self.boxes = []

    def write_boxes(self):
        with open("boxfile_out.dat", 'w') as f:
            for box in self.boxes:
                f.write(box.__repr__())

    def read_boxes(self):
        with open(self.f) as f:
            for i, line in enumerate(f.readlines()):
                if i > 0:
                    l = line.split()
                    self.boxes.append(i3Box(l[0], l[1], l[2], l[3], l[4], l[5]))

if __name__=="__main__":
    BW = i3Boxwriter(boxfile='boxfile.dat')
    BW.read_boxes()
    BW.write_boxes()