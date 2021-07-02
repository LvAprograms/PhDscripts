def check_resolution(xres, yres, zres):
    for n in range(20):
        N = getN(n)
        xsize = (N-1) * xres
        ysize = (N-1) * yres
        zsize = (N-1) * zres
        print("N = {}: xsize = {}, ysize = {}, zsize = {} km".format(N, xsize, ysize, zsize))



def getN(n):
    return 16 * n + 5

if __name__=="__main__":
    check_resolution(10, 3, 10)