/* Tracking Three Phase Contact line (apparent)
# Last Update: November 12, 2020
# Author: Vatsal Sanjay
# vatsalsanjay@gmail.com
# Physics of Fluids
*/
#include "navier-stokes/centered.h"
#include "fractions.h"

scalar f1[], f2[];
char filename[1024], nameTrack[1024];
double DistCutoff;
double xTP, yTP, vTP, angle1, angle2;
double r2_max;

int main(int a, char const *arguments[])
{
  // check if all arguments are given
  if (a < 4) {
    fprintf(stderr, "Error: Missing arguments.\n");
    fprintf(stderr, "Usage: %s <filename> <nameTrack> <DistCutoff>\n", arguments[0]);
    return 1; 
  }
  // boundary conditions
  f1[left] = dirichlet(1.0);
  f2[left] = dirichlet(0.0);
  u.t[left] = dirichlet(0.0);
  sprintf (filename, "%s", arguments[1]);
  sprintf(nameTrack, "%s", arguments[2]);

  DistCutoff = atof(arguments[3]);
  restore (file = filename);
  f1.prolongation = fraction_refine;
  f2.prolongation = fraction_refine;
  boundary((scalar *){f1, f2});

  // double x0 = -4., y0 = 0.;
  face vector s[];
  s.x.i = -1;
  r2_max = -1.;
  xTP = 0., yTP = 0., vTP = 0., angle1 = 0., angle2 = 0.;
  foreach(){
    if (f2[] > 1e-6 && f2[] < 1. - 1e-6) {
      coord n2 = facet_normal (point, f2, s);
      double alpha2 = plane_alpha (f2[], n2);
      coord segment2[2];
      if (facets (n2, alpha2, segment2) == 2){
        if (f1[] > 1e-6 && f1[] < 1. - 1e-6) {
          coord n1 = facet_normal (point, f1, s);
          double alpha1 = plane_alpha (f1[], n1);
          coord segment1[2];
          if (facets (n1, alpha1, segment1) == 2){
            double x1 = x + (segment1[0].x+segment1[1].x)*Delta/2.;
            double y1 = y + (segment1[0].y+segment1[1].y)*Delta/2.;
            double x2 = x + (segment2[0].x+segment2[1].x)*Delta/2.;
            double y2 = y + (segment2[0].y+segment2[1].y)*Delta/2.;
            double dist = sqrt(sq(x1-x2)+sq(y1-y2));
            double xc = 0.5 * (x1 + x2);
            double yc = 0.5 * (y1 + y2);
            if (dist > DistCutoff){
                double r2 = sq(xc) + sq(yc);  // radius squared from origin

                if (r2 > r2_max){
                  r2_max = r2;
                  xTP = xc;
                  yTP = yc;
                  vTP = u.y[];
                  angle1 = atan2(n1.y, n1.x);
                  angle2 = atan2(n2.y, n2.x);
                }
              }
          }
        }
      }
    }
    //
    // if(interfacial(point,f1) & interfacial(point,f2) & x > x0){
    //   x0 = x;
    //   y0 = y;
    // }
  }
  if (r2_max < 0.) {
  // no triple point found
  xTP = yTP = vTP = angle1 = angle2 = 0.;
}
  fprintf(ferr, "%f %f %f %4.3e %f %f\n", t, xTP, yTP, vTP, angle1, angle2);
  FILE *fp2;
  fp2 = fopen (nameTrack, "a");
  fprintf(ferr, "%f %f %f %4.3e %f %f\n", t, xTP, yTP, vTP, angle1, angle2);
  fclose(fp2);
  // fprintf(ferr, "%f %f\n", x0, y0);
}
