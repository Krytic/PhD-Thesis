def integrate_eoms(a0, e0, p):
    """
    General purpose integrator for Nyadzani & Razzaque eqns for a & e.

    Params:
        a0 - The initial semimajor axis, measured in solar radii
        e0 - The initial eccentricity, dimensionless
        p  - A vector of parameters:
                 p[1] = m1 (units: Solar Mass)
                 p[2] = m2 (units: Solar Mass)
                 p[3] = unused (will be removed in next version)
                 p[4] = unused (will be removed in next version)
                 p[5] = Lifetime (evolution + rejuvenation)

    Returns:
        A  - An array of the semimajor axes of the binary system over time. (Solar Mass)
        E  - An array of the eccentricities of the binary system over time. (no dim.)
    """

    Solar_Mass = 1.989e30       # kg
    Solar_Radius = 696340000.0  # m
    G = 6.67e-11                # m^3 kg^-1 s^-2
    c = 299792458.0             # m/s

    A = np.array([])
    E = np.array([])
    H = np.array([])

    m1, m2, _, _, evotime = p[0], p[1], p[2], p[3], p[4]

    # number of seconds in a year
    seconds_per_year = 60 * 60 * 24 * 365.25

    ########################
    #      Unit Check      #
    ########################
    a = a0 * Solar_Radius  # Meters
    e = e0                 # Dimensionless
    m1 = m1 * Solar_Mass   # Kilogram
    m2 = m2 * Solar_Mass   # Kilogram
    ########################
    #    End Unit Check    #
    ########################

    # Beta has units m^4 / s
    beta = ((64/5) * G**3 * m1 * m2 * (m1 + m2) / (c**5))

    A = np.append(A, a)
    E = np.append(E, e)
    H = np.append(H, 0.0)

    total_time = 0

    # Integrate until past the end of the universe, or a 10km orbit
    while total_time/seconds_per_year + evotime < 1e11 and a > 1e4:
        # an euler integrator: work out da/dt then times it by dt
        # to get da, which then we can work out as a = a + da/dt * dt.
        initial_da = (- beta / ((a**3) * (1 - e**2)**(7/2)))
        da = initial_da * (1 + (73/24) * e**2 + (37/96) * e**4)

        intial_de = (((-19/12) * beta) / (a**4*(1-e**2)**(5/2)))
        de = intial_de * (e + (121/304) * e**3)
        # Units: s^-1

        timeA = abs(1e-2 * a/da)

        if e > 1e-10:
            timeE = abs(1e-2 * e/de)
        else:
            de = 0
            e = 1e-10
            timeE = timeA * 10

        # maximum timestep is half of the width of the smallest BPASS time bin
        conv_frac = 0.23076752*0.5*seconds_per_year

        dt2 = (evotime + total_time/seconds_per_year)*conv_frac

        # Take a timestep that results in the smallest change: either a
        # change in E, a change in A, 1/2 the smallest BPASS bin.
        dt = min(timeE, timeA, dt2)

        a = a + dt * da
        e = e + dt * de

        A = np.append(A, a)
        E = np.append(E, e)
        H = np.append(H, dt)

        total_time = total_time + dt

    # Determine why we stopped, so the parent function can tell what went
    # "wrong".
    stop_reason = "flag_not_set"

    if total_time/seconds_per_year + evotime >= 1e11:
        stop_reason = "out_of_time"

    if a <= 1e4:
        stop_reason = "merged"

    # Solar Radii, Dimensionless
    return A / Solar_Radius, E, H, stop_reason