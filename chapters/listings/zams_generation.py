import kaitiaki
import os

# First, instantiate the STARS code. run_bs is the location of the run_bs
# bash script, which sets up the symlinks and actually runs the code.
STARS = kaitiaki.STARS.STARSController(run_bs='.')

# Loads the default data file and solar metallicity opacity table
STARS.blit('z020')

masses_to_model = [0.5, 1, 2, 4, 8]
masses_to_model.extend(range(10, 90, 10))

do_ZAMS_Track = False

output_directory = 'figures'

for ZAMS_mass in masses_to_model:
    if not os.path.exists(f'{output_directory}/plot.{ZAMS_mass}MSUN'):
        # Loads a 1 Msun model
        STARS.load_default_modin()

        # Sets the code up to target a given ZAMS mass.
        STARS.setup_zams_inflation(ZAMS_mass)

        # Executes the code.
        STARS.run()

        # Equivalent to "tail -399 modout > modin" -- transfers the last 2*199+1
        # lines from modout (the last converged model) to modin
        STARS.modout_to_modin()

        # Again, to reload data
        STARS.blit('z020')

        # Setup the data file for single-star evolution
        # This disables orbital evolution, interaction effects, and sets
        # IMODE = 1.
        STARS.setup_single_evolution()

        # Set up the key parameters for our run
        STARS.configure_parameters({
            'DT1': 0.1,  # Fraction of timestep to allow for lower variation
                         # (if the timestep is cut, it can be cut to 10% of its
                         # present value)
            'DDD': 2,    # Modulus of total desired timestep
            # The following parameters were altered during our ZAMS inflation
            # run -- set them back to "normal evolution" parameters.
            'IML1': 5,   # WR mass-loss rates
            'RML': 0,    # This was set to our target ZAMS mass during
                         # inflation -- should be zero so no mass is added
                         # except via the usual ML channels
            'IX': 1,     # Enable hydrogen burning
            'IY': 1,     # Enable helium burning
            'IZ': 1,     # Enable metal burning
            'ITH': 1,    # Enable thermal energy generation
            'NSAVE': 1,
            'ISTART': 1  # Reset age, NMOD, and the timestep (to 10% of T_KH)
        })

        # Execute the model, run until the AGB.
        STARS.run(with_live_HR=False)

        ext = f'{ZAMS_mass}MSUN'

        STARS.terminal_command(f'mv plot {output_directory}/plot.{ext}')
        STARS.terminal_command(f'mv out {output_directory}/out.{ext}')

if not os.path.exists(f'{output_directory}/plot.ZAMS_track'):
    STARS.load_default_modin()

    STARS.setup_zams_inflation(0.5)

    STARS.run()

    STARS.modout_to_modin()

    STARS.setup_zams_inflation(300)

    STARS.run()

    STARS.terminal_command(f'mv plot {output_directory}/plot.ZAMS_track')
