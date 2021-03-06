# coding: utf8

import clinica.engine as ce


class fMRIPreprocessingCLI(ce.CmdParser):

    def define_name(self):
        """Define the sub-command name to run this pipeline."""
        self._name = 'fmri-preprocessing'

    def define_description(self):
        """Define a description of this pipeline."""
        self._description = ('Preprocessing of raw fMRI datasets:\n'
                             'http://clinica.run/doc/Pipelines/fMRI_Preprocessing/')

    def define_options(self):
        """Define the sub-command arguments."""
        from clinica.engine.cmdparser import PIPELINE_CATEGORIES
        # Clinica compulsory arguments (e.g. BIDS, CAPS, group_id)
        clinica_comp = self._args.add_argument_group(PIPELINE_CATEGORIES['CLINICA_COMPULSORY'])
        clinica_comp.add_argument("bids_directory",
                                  help='Path to the BIDS directory.')
        clinica_comp.add_argument("caps_directory",
                                  help='Path to the CAPS directory.')

        # Optional arguments (e.g. FWHM)
        optional = self._args.add_argument_group(PIPELINE_CATEGORIES['OPTIONAL'])
        default_fwhm = [8, 8, 8]
        optional.add_argument("-fwhm", "--full_width_at_half_maximum",
                              metavar="FWHM",
                              nargs=3, type=int, default=default_fwhm,
                              help="A list of integers specifying the full width at half maximum (FWHM) filter size "
                                   "in the three directions x y z, in millimeters, used to smooth the images "
                                   "(default: --full_width_at_half_maximum %s)." %
                                   self.list_to_string(default_fwhm))
        optional.add_argument("-t1s", "--t1_native_space",
                              action='store_true', default=False,
                              help="When specified, the corrected fMRI data registered to the native T1 space "
                                   "of each subject are saved. This might be useful when dealing with "
                                   "parcellations that are in the native T1 space.")
        optional.add_argument("-fsbm", "--freesurfer_brain_mask",
                              action='store_true', default=False,
                              help="When specified, the pipeline uses the brain extraction generated by FreeSurfer "
                                   "during the t1-freesurfer pipeline. Otherwise, it computes it using the "
                                   "SPM Registration tool followed by empirically-estimated operations "
                                   "performed by FSL.")
        optional.add_argument("-u", "--unwarping",
                              action='store_true', default=False,
                              help="When specified, the unwarping correction step is executed. This will add "
                                   "SPM's Unwarping to the Realign step (magnitude and phasediff files are necessary "
                                   "in the BIDS directory).")

        # Clinica standard arguments (e.g. --n_procs)
        clinica_opt = self.add_clinica_standard_arguments()
        # clinica_opt.add_argument("-sl", "--slurm", action='store_true',
        #                          help='Run the pipelines using SLURM.')
        # clinica_opt.add_argument("-sa", "--sbatch_args",
        #                          help='SLURM\'s sbatch tool arguments.')

    def run_command(self, args):
        """Run the pipeline with defined args."""
        from networkx import Graph
        from fmri_preprocessing_pipeline import fMRIPreprocessing
        from clinica.utils.ux import print_end_pipeline, print_crash_files_and_exit

        parameters = {
            'full_width_at_half_maximum': args.full_width_at_half_maximum,
            't1_native_space': args.t1_native_space,
            'freesurfer_brain_mask': args.freesurfer_brain_mask,
            'unwarping': args.unwarping,
        }
        pipeline = fMRIPreprocessing(
            bids_directory=self.absolute_path(args.bids_directory),
            caps_directory=self.absolute_path(args.caps_directory),
            tsv_file=self.absolute_path(args.subjects_sessions_tsv),
            base_dir=self.absolute_path(args.working_directory),
            parameters=parameters,
            name=self.name
        )

        if args.n_procs:
            exec_pipeline = pipeline.run(plugin='MultiProc',
                                         plugin_args={'n_procs': args.n_procs})
        # elif args.slurm:
        #     exec_pipeline = pipeline.run(plugin='SLURMGraph',
        #                                  plugin_args={'dont_resubmit_completed_jobs': True,
        #                                               'sbatch_args': args.sbatch_args})
        else:
            exec_pipeline = pipeline.run()

        if isinstance(exec_pipeline, Graph):
            print_end_pipeline(self.name, pipeline.base_dir, pipeline.base_dir_was_specified)
        else:
            print_crash_files_and_exit(args.logname, pipeline.base_dir)
