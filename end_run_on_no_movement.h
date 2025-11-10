int steady_streak = 0;
const int    STEADY_NEED  = 5;     // consecutive checks needed
const double USUM_MIN = 5e-4;  // miniumum usum
double usum_prev = 0.0;
event endSimulation (i = 100; i += 10) {
  double usum = 0.0;

  foreach (reduction(+:usum)) {

    // Grid area weighting:
    usum += (sq(u.x[]) + sq(u.y[])) * sq(Delta);
  }

  if (usum < USUM_MIN && usum_prev > usum) {
    steady_streak++;  // reset if usum is too small
    if (steady_streak >= STEADY_NEED) {
      fprintf(ferr,
        "Reached steady sum of u^2: usum=%g at time %g, step %d \n",
        usum, t, i);
      return 1;  // stop run()
    }
  } else {
    steady_streak = 0;  // reset if usum is too large
  }
  usum_prev = usum;
}

