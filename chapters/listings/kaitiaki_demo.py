import kaitiaki

# First, instantiate the STARS code. run_bs is the location of the run_bs
# bash script, which sets up the symlinks and actually runs the code.
STARS = kaitiaki.STARS.STARSController(run_bs='..')

# Loads the default data file and solar metallicity opacity table
STARS.blit('z020')

# Loads a 1 Msun model
STARS.load_default_modin()

# Sets the code up to target a ZAMS mass of 10 Msun.
STARS.setup_zams_inflation(10)

# Executes the code, such that the final modout will be a 10 Msun model.
STARS.run()

# Equivalent to "tail -399 modout > modin" -- transfers the last 2*199+1
# lines from modout (the last converged model) to modin
STARS.modout_to_modin()

# Again, to reload data
STARS.blit()

# Set up the key parameters for our run
STARS.configure_parameters({
    'DT1': 0.1,  # Fraction of timestep to allow for lower variation
                 # (if the timestep is cut, it can be cut to 10% of its
                 # present value)
    'NM2': 499,  # Number of meshpoints.
    'DDD': 2,    # Modulus of total desired timestep
    'IML1': 5,   # WR mass-loss rates
    'RML': 0,    # This was set to 10 Msun during inflation -- should be
                 # zero so no mass is added except via the usual ML channels
                 # (this parameter, formally, sets a constant ML rate so
                 # that in the absence of other mechanisms, the mass would
                 # always decrease)
    'IMODE': 1,  # Single star mode
    'IX': 1,     # Hydrogen burning
    'IY': 1,     # Helium burning
    'IZ': 1,     # Metal burning
    'ITH': 1,    # Thermal energy generation
    'ISTART': 1  # Reset age, NMOD, and the timestep (to 10% of T_KH)
})

# Execute the model, run until the AGB.
STARS.run()
