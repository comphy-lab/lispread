/** Title: Bubble spreading at LUBIS
# Author: Vatsal Sanjay
# vatsalsanjay@gmail.com
# Physics of Fluids
# Last Updated: Feb 10 2023
*/

// 1 is oil layer, 2 is gas bubble and 3 is water
#include "axi.h"      // axisymmetric geometry is alsays the bottom line , always need to be included first 
#include "navier-stokes/centered.h" // centered uses central difference method, now also /conserving.h might also be bossible it can get rid of blow ups due to cells moving into other cells in case of large density ratios
#define FILTERED     // spreads interface over a view grid cels to reduce jumps (mostly in curvature and fractions), the space o1
#include "three-phase.h"  // initializes fractions mu1, mu2, mu3, rho1, rho2, rho3, + smearing out
#include "tension.h"   // add surface tension
#include "distance.h"   // some geometry
#include "adapt_wavelet_limited_v2.h" // adaptive mesh refinement

#define MINlevel 3                                              // maximum grid size, opposite of MAXlevel

#define tsnap (5e-4)                // time interval, can be smaller in case of cfl convergence (tollorance needs to be made)

// Error tolerances
#define fErr (1e-3)                                 // error tolerance in VOF
#define KErr (1e-4)                                 // error tolerance in KAPPA
#define VelErr (1e-2)                            // error tolerances in velocity
#define OmegaErr (1e-2)                            // error tolerances in velocity

/** Variable definitions
Curvature(f, kappa) calculates the curvature and stores it in kappa
Curvature(f, kappa , sigma) calculates the curvature and multiplies it with sigma and stores it in kappa
tensiion.h first gets all surface forces for each interface, and saves them in phi1 and phi2 and then puts all interfaces in 
a list called list.
*/








// boundary conditions
u.t[left] = dirichlet(0.0);

// you can set pressures, velocities, height functions, (fractions but not advised)
// for every grid cel you can give boundray condition for the center or for the face (always the wall face) 
// In case whole droplets needs to have a velocity, you need to loop over all cells where hte droplet is
// open to athmosphere p= 0, neumann 0 for velocities( free surface)
// you can also define a variable that is dependent on variables to for example give a contact angle that is dependent on the veloicyt of the droplet Can also give it if else statements and play around with it to see what basilisk recognizes

double Oh_d, Oh_f, Oh_e, rho_d, rho_f, rho_e, sigma_1, sigma_2, hf, tmax, Ldomain, delta;
int MAXlevel;

int main(int argc, char const *argv[]) {

  if (argc < 14) {
    fprintf(ferr, "Need %d more argument(s): Oh_drop, Oh_film, Oh_env, rho_d, rho_f, rho_e,sigma_1, sigma_2, hf, tmax, Ldomain, delta, MAXlevel\n", 9-argc);
    return 1;
  }
  
  Oh_d = atof(argv[1]);
  Oh_f = atof(argv[2]);
  Oh_e = atof(argv[3]);
  rho_d = atof(argv[4]);
  rho_f = atof(argv[5]);
  rho_e = atof(argv[6]);
  sigma_1 = atof(argv[7]);  // liquid-env (assuming liquid has a lower surface tension then drop)
  sigma_2 = atof(argv[8]);  // drop-liquid
  hf = atof(argv[9]);  // used to determine where box start
  tmax = atof(argv[10]);
  Ldomain = atof(argv[11]); // used wherer box ends
  delta = atof(argv[12]);
  MAXlevel = atoi(argv[13]);

  L0=Ldomain;
  X0=-hf*1.001; Y0=0.;          // define origin, you can also define LD/2, can be easier
  init_grid (1 << 4);       // grid size is 2^4, you can start with Max level( not coarse) or min level(coarse) by changing the n(4) in this case
  
  char comm[80];
  sprintf (comm, "mkdir -p intermediate");
  system(comm);

  rho_drop = rho_d; mu_drop = Oh_drop;
  rho_film = rho_f; mu_film = Oh_film;
  rho_env = rho_e; mu_env = Oh_env;

  f1.sigma = sigma_1;    
  f2.sigma = sigma_2;   
  fprintf(ferr, "Level %d tmax %g. Oho %3.2e, Ohw %3.2e, Oha %3.2e, hf %3.2f\n", 
                MAXlevel, tmax, Oh_drop, Oh_film, Oh_env, hf);
  run();
}

int refRegion(double x, double y, double z){

  return (x < 1.1*hf && y < 1.0 ? MAXlevel:
          x < 5*hf && y < 1.5 ? MAXlevel-1:
          x < 1.0 && y < 2.0 ? MAXlevel-2:
          x < 3.0 && y < 2.0 ? MAXlevel-3:
          MAXlevel-4
        );
}

event init(t = 0){
  if(!restore (file = "dump")){   // it checks if it starts from a dump file, if no dump file, it initiates
    fprintf(ferr, "No dump file found, start initialization ..." );
    char filename1[60], filename2[60];
    /**
    Initialization for f1 and f2, it is better to define this here instead of earlier at the other BC
    */
    f1[left] = dirichlet(1.0);
    f2[left] = dirichlet(0.0);
    sprintf(filename1, "f1_init-%3.2f.dat", delta);
    sprintf(filename2, "f2_init-%3.2f.dat", delta);
    // write fractions into file (not needed)
    FILE * fp1 = fopen(filename1,"rb");
    if (fp1 == NULL){
      fprintf(ferr, "There is no file named %s\n", filename1);
      return 1;
    }
    FILE * fp2 = fopen(filename2,"rb");
    if (fp2 == NULL){
      fprintf(ferr, "There is no file named %s\n", filename2);
      return 1;
    }

    coord* InitialShape1;
    coord* InitialShape2;
    InitialShape1 = input_xy(fp1);
    fclose (fp1);
    InitialShape2 = input_xy(fp2);
    fclose (fp2);
    scalar d1[], d2[];
    distance (d1, InitialShape1);
    distance (d2, InitialShape2);

    // define for which regions need to be refined, also passarguments to define these regions (you can aslo pass the errors mentioned at the top, at least htat is what Aman does)
    while (adapt_wavelet_limited ((scalar *){f1, f2, d1, d2}, (double[]){1e-8, 1e-8, 1e-8, 1e-8}, refRegion).nf);
    // if a fraction aligns with an interface (between 2 cells) it gives a blow up, to fix you can shift everything with half a grid cel
    // in the header files (at the op the to pof them), the variables are defined so you can look up what basilisk c recognizes
    /**
    The distance function is defined at the center of each cell, we have
    to calculate the value of this function at each vertex. */
    vertex scalar phi1[], phi2[];
    // TODO: investigate this part
    foreach_vertex(){
      phi1[] = -(d1[] + d1[-1] + d1[0,-1] + d1[-1,-1])/4.;
      phi2[] = -(d2[] + d2[-1] + d2[0,-1] + d2[-1,-1])/4.;
    }
    /**
    We can now initialize the volume fractions in the domain. */
    fractions (phi1, f1);
    fractions (phi2, f2);
    fprintf(ferr, " done\n" );
  }
  dump (file = "dump");
  // return 1;
}

scalar KAPPA1[], KAPPA2[], omega[];

event adapt(i++) {
  vorticity (u, omega);
  curvature(f1, KAPPA1);
  curvature(f2, KAPPA2);
  foreach(){
    omega[] *= f1[]*(1-f2[]);
  }
  adapt_wavelet_limited ((scalar *){f1, f2, u.x, u.y, KAPPA1, KAPPA2, omega},
    (double[]){fErr, fErr, VelErr, VelErr, KErr, KErr, OmegaErr},
    refRegion, MINlevel);
}

event writingFiles (t = 0; t += tsnap * 10; t <= tmax + tsnap) {
  dump (file = "dump");
  char nameOut[80];
  sprintf (nameOut, "intermediate/snapshot-%5.4f", t);
  dump (file = nameOut);
}

event logWriting (i++) {
  double ke = 0.;
  foreach (reduction(+:ke)){
    ke += sq(Delta)*(sq(u.x[]) + sq(u.y[]))*rho(f1[],f2[]);
  }
  static FILE * fp;
  if (i == 0) {
    // fprintf (ferr, "i dt t ke\n");
    fp = fopen ("log", "w");
    fprintf (fp, "i dt t ke\n");
    fprintf (fp, "%d %g %g %g\n", i, dt, t, ke);
    fclose(fp);
  } else {
    fp = fopen ("log", "a");
    fprintf (fp, "%d %g %g %g\n", i, dt, t, ke);
    fclose(fp);
  }
  // fprintf (ferr, "%d %g %g %g\n", i, dt, t, ke);
}
