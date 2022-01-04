#ifndef BASEPATH
#define BASEPATH "/media/luuk/betav8x1/ChenFDSPMprn/"
#endif

FILE* read_prn(int number, char m[]);
int extract_position(FILE *f, char variable[]);
void check_read(int elements_read, int expected_elements);
unsigned long read_long_int(FILE* fptr);
double read_double(FILE* fptr);

