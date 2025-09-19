@if _XOPEN_SOURCE < 700
  @undef _XOPEN_SOURCE
  @define _XOPEN_SOURCE 700
@endif
@if _GNU_SOURCE
@include <stdint.h>
@include <string.h>
@include <fenv.h>
@endif
#define _CATCH
#define dimension 2
#include "common.h"
#include "grid/quadtree.h"
#ifndef BASILISK_HEADER_0
#define BASILISK_HEADER_0
#line 1 "getFacet2.c"
/* Title: Getting Facets
# Author: Vatsal Sanjay
# vatsalsanjay@gmail.com
# Physics of Fluids
*/
#include "navier-stokes/centered.h"
#include "fractions.h"

scalar f2[];
char filename[80];
int main(int a, char const *arguments[])
{
  sprintf (filename, "%s", arguments[1]);
  restore (file = filename);
  #if TREE
    f2.prolongation = fraction_refine;
  #endif
  boundary((scalar *){f2});
  FILE * fp = ferr;
  output_facets(f2,fp);
  fflush (fp);
  fclose (fp);
}

#endif
