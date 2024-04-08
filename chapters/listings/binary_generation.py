import kaitiaki

STARS = kaitiaki.STARS.STARSController()
STARS.update_run_bs('..')

generate_ZAMS = False

if generate_ZAMS:
    for target in [8, 10]:
        STARS.blit()
        STARS.load_default_modin()
        STARS.setup_zams_inflation(target)

        STARS.configure_parameters({
                'DT1': 0.1,
            })

        STARS.run()

        for f in ['plot', 'out', 'modout']:
            STARS.terminal_command(f'mv {f} {f}.{target}msun')

STARS.blit()

cfgs = ['primary', 'secdry', 'binary']


def run_single(mode):
    STARS.terminal_command('cp /home/sric560/Desktop/CheckNESI/data data')
    STARS.setup_single_evolution()
    STARS.commit_parameters()

    mzams = {'primary': 10, 'secdry': 8}[mode]

    STARS.modout_to_modin(modout_location=f'modout.{mzams}msun',
                          modin_location='modin')

    STARS.run()

    for f in ['plot', 'out', 'modout']:
        STARS.terminal_command(f'mv {f} {f}.{mode}')

    print(f"{mode} complete.")


def run_binary():
    STARS.terminal_command('cp /home/sric560/Desktop/CheckNESI/data data')

    STARS.setup_binary_evolution()
    STARS.commit_parameters()

    STARS.modout_to_modin(modout_location='modout.10msun',
                          modin_location='modin')

    STARS.modout_to_modin(modout_location='modout.8msun',
                          modin_location='modin2')

    STARS.set_period(30)

    STARS.run()

    for f in ['plot', 'out', 'modout',
              'plot2', 'out2', 'modout2']:
        STARS.terminal_command(f'mv {f} {f}.binary')

    print(f"Binary complete.")


for cfg in cfgs:
    match cfg:
        case 'primary' | 'secdry':
            run_single(cfg)
        case 'binary':
            run_binary()
