#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char* argv[]);
double Vxyz(int* x[], int* y[], int* z[], int Const, float koef, int nshiftx, int nshity, int nshiftz);

int main(int argc, char* argv[]) {
    if (argc <= 1) {
        printf("Not enough arguments were given\n");
        exit(1);
    }
    else{
        printf("%d arguments were given:\n", argc);
        for (int i=1; i < argc; i++) {
            printf("%s ",argv[i]);
        }
        printf("\n");
    }
    FILE *fp = NULL;
    fp = fopen(argv[argc-1], 'r');
    if (fp == NULL) {printf("File not found\n"); exit(1);};
    /*while(fgetc(fp) != "~")
        exit(0);
    */
   int nx = 213;
   float dx = 10e3;
   int x[nx];
   x[0] = 0;
   for (int i=1; i<nx;i++) {
       x[i] = x[i-1] + dx;
   }

   int ny = 69;
   float dy = 3e3;
   int y[ny];
   y[0] = 0;
   for (int i = 1; i < ny; i++) {
       y[i] = y[i-1] + dy;
   }

    int nz = 133;
   float dz = 10e3;
   int z[nz];
   z[0] = 0;
   for (int i = 1; i < nz; i++) {
       z[i] = z[i-1] + dz;
   }
    return 0;
    
}

double Vxyz(int* x[], int* y[], int* z[], int Const, float koef, int nshiftx, int nshifty, int nshiftz) {
    
    return Const + koef * (x+nshiftx, y+nshifty, z+nshiftz);
}