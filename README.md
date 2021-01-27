## Data download
https://www.ngdc.noaa.gov/mgg/topo/gltiles.html and download 'g10g'  and 'h10g' 

## Program usage
Run the showcase model by running 
```
$ python3 Topomap.py
``` 
after downloading the data and putting it in the same directory as the python program.
Look at the topography, pick your own profile line (rows are vertical coords, columns horizontal coords) and run
```
$ python3 Topomap.py rs cs re ce
```
where rs, cs, re and ce are starting and ending row and columns.
You will be prompted to enter a 2D smoothing filter size. If you want the unsmoothed data, just hit Enter. The showcase plots have a filter radius of 25 km.

Enjoy!
