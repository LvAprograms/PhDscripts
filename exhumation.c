#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <memory.h>
#include "exhumation.h"

char basepath[] = "/media/luuk/alphav8x1/PhD/ErosionModelling/ChenFDSPMseries/";
char prefix[] = "sfc_";
char extension[] = ".vtk";
char model[] = "vel1k1/";
// datadict = {0: "coordinates", 1:"elevation", 2: "horz_vel_x", 3: "horz_vel_z", 4:"dhdt_advection", 5: "dhdt_uplift", 6:"dhdt_ers_sed",
//             7: "base_diffusivity", 8: "eff_cell_diffusivity"};
double secinyr =  60 * 60 * 24 * 365.25;

int main() {
    /*goal: do the math now done in exhumation.py and save the result as a (temporary) output file which you can visualise in python */
    char filepath[] = strcat(basepath, model);
    printf("%s\n", filepath);
    char newpath[] = strcat(filepath, prefix);
    printf("%s\n", newpath);
    // FILE* fp = fopen("%s%s%s%s",basepath, model, prefix, model)
    // read_data
    return 0;
}

  