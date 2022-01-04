#include <stdio.h>
#include <stdlib.h>
// int main();
void readPTtinput();

// int main() {
//     readPTtinput();
//     return 0;
// }

enum isSet {
    Set,
    NotSet
};

enum Found {
    Found,
    NotFound
};

struct Rectangle {
    enum isSet is_set;
    double xmin, xmax, ymin, ymax;
};

struct MarkerLogger {
    enum Found is_found;
    int indices[1000];
    int rock_ids[2];
    struct Rectangle rect;
};

int search_for_marker(struct MarkerLogger*const logger, int index) {
    if (logger->is_found == Found) {
        return logger->indices[index];
    }

    for (int ii = 0; ii < marknum; ii++) {
        if ((logger->rock_ids[0] != markt[ii]) && (logger->rock_ids[1] != markt[ii])) {
            continue;
        }

        struct Rectangle const*const rect = &logger->rect;
        if (rect->is_set == NotSet) {
            continue;
        }

        double const x = markx[ii], y = marky[ii];
        if (x > (rect->xmin + index * XINTERVAL) && x < rect->xmax &&
            y > rect->ymin && y < rect->ymax) {
            if (index == 4) logger->is_found = Found;
            logger->indices[index] = ii;
            return ii;
        }
    }

    return -1;
}


void readPTtinput() {
    //FILE* PTt = fopen("PTt.log");
    FILE *PTinput = fopen("PTt_input.dat", "r");
    char singleLine[150];
    float xmin, xmax, ymin, ymax, zmin, zmax, dx, dz;
    int complist[5];
    if (PTinput == NULL) {printf("File not found\n"); exit(1);};
    fscanf(PTinput, "%f-%s", &xmin, singleLine);
    fscanf(PTinput, "%f-%s", &xmax, singleLine);
    fscanf(PTinput, "%f-%s", &ymin, singleLine);
    fscanf(PTinput, "%f-%s", &ymax, singleLine);
    fscanf(PTinput, "%f-%s", &zmin, singleLine);
    fscanf(PTinput, "%f-%s", &zmax, singleLine);
    for (int i = 0; i < 2; i++) {
        fscanf(PTinput,"%d,", &complist[i]);
    }
    fscanf(PTinput, "%s", singleLine); // whitespace after the complist line!
    fscanf(PTinput, "%f-%s", &dx, singleLine);
    fscanf(PTinput, "%f-%s", &dz, singleLine);
    // printf("%e %e %e %e %e %e\n%d, %d %e %e\n", xmin, xmax, ymin, ymax, zmin, zmax, complist[0], complist[1], dx, dz);
    fclose(PTinput);

}
/*
PLAN:
1) download the sichuan source code and put it in a git VCS
2) modify in3mg.c 
3) check how Istvan wrote the Marker logging and just do that but for 3D. 
*/
