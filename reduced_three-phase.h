/**
We need the interfacial force module as well as functions to compute the
position of the interface. */

#include "iforce.h"
#include "curvature.h"

/**
We overload the acceleration() event to add gravity contributions to the
interfacial potentials of *both* interfaces (f1 and f2). */

event acceleration (i++)
{
  // Loop over all tracked interfaces (declared in threephase.h)
  for (scalar f in interfaces) {

    scalar phi = f.phi;

    // Density jump for this interface
    double drho = 0.;
    if (f.i == f1.i)
      drho = rho_film - rho_env;   // film - environment
    else if (f.i == f2.i)
      drho = rho_drop - rho_film;  // drop - film
    else
      continue; // safety: unknown interface

    // Convert to vector used by position()
    coord G1;
    foreach_dimension()
      G1.x = drho * G.x;

    // Add (or create) this interface's gravity potential contribution
    if (phi.i)
      position (f, phi, G1, Z, add = true);
    else {
      phi = new scalar;
      position (f, phi, G1, Z, add = false);
      f.phi = phi;
    }
  }
}

/**
# Reduced gravity for three-phase interfacial flows

We extend the reduced-gravity formulation used for two-phase flows to the
three-phase setup defined in [threephase.h].

In the three-phase VOF representation we have two interfaces (tracked by two
VOF tracers):
- `f1`: separates the environment (fluid 3) from the film+drop region (fluid 1+2).
  In the common "drop-in-film-in-env" configuration, this is the film–environment
  interface with density jump  [rho] = rho_film - rho_env.
- `f2`: separates the drop (fluid 2) from the film (fluid 1) with density jump
  [rho] = rho_drop - rho_film.

For each interface i we add an interfacial potential contribution
  phi_i = [rho]_i * G · (x - Z)
to the corresponding `f_i.phi` field used by `iforce.h`.

Important: This assumes the phase ordering is "drop inside film inside env",
so `f1` represents film–env and `f2` represents drop–film. If your topology
allows direct drop–env contact, you would need a more elaborate treatment.
*/