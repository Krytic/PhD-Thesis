    def run_default_evolution(self, zams_mass, NM2=199):
        """Performs one run from pre-ZAMS until the end of evolution.
        Assumes NORMAL file structure.

        Not really useful for scientific applications -- just here
        for educational purposes on how STARS runs.

        Arguments:
            zams_mass {float} -- The ZAMS mass we should target.
        """
        self.output('status', 'Preparing for ZAMS evolution')
        self.terminal_command("rm modin")
        self.terminal_command("rm data")

        self.blit()
        self.load_default_modin()

        pre_zams_params = {'IML1': 9,
                           'RML': float(zams_mass),
                           'ITH': 0,
                           'IX': 0,
                           'IY': 0,
                           'IZ': 0,
                           'NM2': NM2,
                           'NCH': 3,
                           'ISTART': 0}

        self.output('status', 'Configuring Parameters')
        self.configure_parameters(pre_zams_params)
        self.output('status', 'Beginning ZAMS evolution')
        output, error, status = self.run(timeout=20*60)

        if self._verbose_output:
            self.output("status", output)
            self.output("error", error)

        out = self._output_dir
        self.output('status', 'Moving output files')
        self.terminal_command(f'mv plot {out}/plot.zams')
        self.terminal_command(f'mv out {out}/out.zams')
        self.modout_to_modin()
        self.terminal_command(f'mv modout {out}/modout.zams')

        main_evo_params = {'IML1': 5,
                           'RML': 0,
                           'ITH': 1,
                           'IX': 1,
                           'IY': 1,
                           'IZ': 1,
                           'ISTART': 1,
                           'NM2': NM2,
                           'NNMOD': 0}

        self.output('status', 'Configuring Parameters')
        self.configure_parameters(main_evo_params)

        self.output('status', 'Beginning post-ZAMS evolution')

        output, error, status = self.run(timeout=20*60)

        if self._verbose_output:
            self.output("status", output)
            self.output("error", error)

        self.output('status', 'Moving output files')

        self.terminal_command(f'mv plot {out}/plot.model')
        self.terminal_command(f'mv out {out}/out.model')
        self.terminal_command(f'mv modout {out}/modout.model')
