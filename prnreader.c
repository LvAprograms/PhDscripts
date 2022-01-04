#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>
#include <time.h>
#include <inttypes.h>

#include "prnreader.h"

FILE* read_prn(int number, char m[]) {
    char filename[128];
    snprintf(filename, sizeof(filename),
             "%s%s/%s_%d%s", BASEPATH, m, m, number, ".prn");
    // printf("%s\n", filename);
    FILE *fptr = fopen(filename, "rb");
    if (!fptr) {
        printf("Error opening file %s\n", filename);
        exit(1);
    }
    else {
        printf("File %s successfully opened \n", filename);
        extract_position(fptr, "density");
    }
    return fptr;
    // fclose(fptr);
}

int extract_position(FILE *f, char variable[]) {
    int n1;
    char* nn1[100]; 
    long int m1, m2, m3, m4;
    long int mm1;
    // Buffers for XY (?)
    double x, y, z;
    char szint = sizeof(int);
    char szlong = sizeof(long int);
    char szfloat = sizeof(float);
    char szdouble = sizeof(double);
    // size_t szcur;
    float ival0;
    double ival1; 
    // first bytes are sizes of variables
    fseek(f, szint+szlong+szfloat+szdouble, SEEK_CUR);
    printf("%ld\n", ftell(f));
    // next the grid parameters
    unsigned long test[6*szlong];
    for (n1 = 0; n1 < 6; n1++) {
        test[n1] = read_long_int(f);
        printf("position %d\n", ftell(f));
    }
    printf("%ld\n", ftell(f));
    printf("%ld\t%ld\t%ld\t%ld\t%ld\t%ld\n", test[0], test[1], test[2], test[3], test[4], test[5]);
    // fseek(f, szlong * 6, SEEK_CUR); // xnumx, ynumy, znumz, mnumx, mnumy mnumz
    fseek(f, szdouble * 3, SEEK_CUR); // xsize, ysize, zsize
    fseek(f, szlong * 3, SEEK_CUR); // pxinit, pyinit, pzinit
    fseek(f, szdouble, SEEK_CUR); //pinit
    fseek(f, szdouble * 3, SEEK_CUR); // gravity
    fseek(f, szint + szlong * 2, SEEK_CUR); // rocknum, bondnum, marknum
    fseek(f, szint, SEEK_CUR); // n0
    // char elements_read = fread(&ival1, szdouble, 1, f);
    // check_read(elements_read, 1);
    ival1 = read_double(f);
    printf("could the timesum be %lf years? \n", ival1);
    // next the rock types info
    
    // fgets(nn1, 100, f);
    // printf("reading %s\n", nn1);
    return SEEK_CUR;
}

void check_read(int elements_read, int expected_elements){
    if (elements_read != expected_elements) {
        printf("%d elements were read while %d were expected\n", elements_read, expected_elements);
        exit(1);
    }
}


union D{
    double d;
    char bytes[sizeof(double)];
};

union L{
    unsigned long l;
    unsigned char bytes[sizeof(long int)];
};

unsigned long read_long_int(FILE* fptr) {
    union L B;
    char elements_read = fread(&B.bytes, __SIZEOF_LONG__, 1, fptr);
    check_read(elements_read, 1);
    for (int i =0; i < 8; i++) {
        printf("%d ", B.bytes[i]);
    }
    printf("\n");

    return B.l;
}

double read_double(FILE* fptr) {
    union D val;
    char elements_read = fread(&val.bytes, __SIZEOF_DOUBLE__, 1, fptr);
    check_read(elements_read, 1);
    return val.d;
}
