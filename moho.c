/* 
What do I want?
1. read PRN file
2. extract marker x y z coordinates
3. extract density at each marker
4. calculate density contour
save contour as ASCII file if possible. 
*/
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <inttypes.h>

#include "prnreader.h" // read_prn
#include "moho.h"

#define BASEPATH "/media/luuk/betav8x1/ChenFDSPMprn/"

int main(int argc, char *argv[]) {
    if (argc < 4) {
        printf("Enter modelname, file_start, file_end, file_step after program\n");
        exit(1);
    }
    char *model = argv[1];
    uint16_t i;
    uint16_t file_start =atoi(argv[2]);
    uint16_t file_end = atoi(argv[3]);
    uint16_t file_step = atoi(argv[4]);
    printf("%d %d %d\n", file_start, file_end, file_step);
    for (i =file_start; i < file_end; i+=file_step) {
        FILE *fptr = read_prn(i, model);
        // printf("%s\n", fptr);
    }
    return 0;
}

