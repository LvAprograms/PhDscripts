
def time_to_json(file, model):
    """
    open a "times.txt" file, read the file number, put it in a text buffer and write this to the correct *.vtr.series file
    """
    txt = '{\n\t"file-series-version" : "1.0",\n\t"files": ['
    with open(file, 'r') as f:
        for line in f.readlines():
            l = line.split()
            fileno = l[0] 
            time = float(l[1])
            if int(fileno) % 10 == 0 or time==float(0):
                txt += '\n\t\t{{ "name" : "{}{}.vtr", "time" : {}}}'.format(model,fileno, time)
                txt += ','
         
    with open("/media/luuk/alphav8x1/PhD/ErosionModelling/strongzones/{}".format(model+ ".vtr.series"), 'w') as f:
        txt = txt[0:-1] # get rid of the extra comma at the end of the series
        txt += '\n\t]\n}'
        f.write(txt)

if __name__ == "__main__":
    time_to_json('/media/luuk/alphav8x1/PhD/ErosionModelling/strongzones/strongzones_times.txt', 'sichuan')