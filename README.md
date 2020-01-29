This repository contains the fMRI-Preprocessing pipeline used for [[Guillon et al., 2019]](https://doi.org/10.1162/netn_a_00087)

This pipeline needs the [Clinica software platform](http://www.clinica.run) that you will have to install.

If you use this pipeline, please cite:
> **J. Guillon, M. Chavez, F. Battiston, Y. Attal, V. La Corte, M. Thiebaut de Schotten, B. Dubois, D. Schwartz, O. Colliot, F. De Vico Fallani** Disrupted core-periphery structure of multimodal brain networks in Alzheimer's disease *Network Neuroscience, 2019* [DOI](https://doi.org/10.1162/netn_a_00087) [PDF](https://www.mitpressjournals.org/doi/pdf/10.1162/netn_a_00087)

As well as neuroimagning tools behind these pipelines.

 :warning: **Please note that this repository is not maintained anymore** :warning:

Original author: Jérémy Guillon ([@jguillon](https://github.com/jguillon))

- [How to use this repo?](#how-to-use-this-repo)
- [`fmri-preprocessing` - Preprocessing of raw functional MRI](#fmri-preprocessing-preprocessing-of-raw-functional-mri)
	- [Prerequisites](#prerequisites)
	- [Dependencies](#dependencies)
	- [Running the pipeline](#running-the-pipeline)
		- [Options](#options)
			- [`--full_width_at_half_maximum`](#-fullwidthathalfmaximum)
			- [`--t1_native_space`](#-t1nativespace)
			- [`--freesurfer_brain_mask`](#-freesurferbrainmask)
			- [`--unwarping`](#-unwarping)
	- [Outputs](#outputs)
	- [Describing this pipeline in your paper](#describing-this-pipeline-in-your-paper)
		- [Example of paragraph](#example-of-paragraph)
		- [Example of paragraph (long version)](#example-of-paragraph-long-version)


## How to use this repo?
- Follow the [developper installation of Clinica](http://www.clinica.run/doc/Installation/) and install v0.4.0 version (`git checkout v0.4.0` before `conda env create -f environment.yml`)
- Clone this repo
- Create the environment variable `CLINICAPATH` like this:
```bash
export CLINICAPATH="/path/to/the/repo/clinica_pipeline_noddi"
```

When typing `clinica run` in your terminal, you should see the `fmri-preprocessing` pipeline.


## `fmri-preprocessing` - Preprocessing of raw functional MRI

This pipeline performs the preprocessing of functional MR images. It is almost fully based on [SPM tools](http://web.mit.edu/spm_v12/manual.pdf) and includes the following processing steps: correction of shifts in the time-series due to the time required to acquire each 2D slice of the volumes, called slice-timing correction [[Henson et al., 1999](http://discovery.ucl.ac.uk/5679/)]; correction of subject's movement artifacts (and an optional unwarping of the associated magnetic susceptibility) [[Friston et al., 1995](https://doi.org/10.1006/nimg.1995.1019)]; brain extraction; coregistration with the subject's T1 image in native space; spatial normalization into MNI space [[Ashburner and Friston et al., 2005](https://doi.org/10.1016/j.neuroimage.2005.02.018)]; and spatial smoothing using a Gaussian filter.


### Prerequisites

Depending on your options, you may need to execute beforehand the  pipeline [`t1-freesurfer`](http://www.clinica.run/doc/Pipelines/T1_FreeSurfer/).

> :warning: Warning :warning:
>
> You absolutely need the following fields in the JSON file associated to your `bold` image (see the official [BIDS specifications](https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/01-magnetic-resonance-imaging-data.html#task-including-resting-state-imaging-data) for more details):
>
 - `BandwidthPerPixelPhaseEncode`
 - `RepetitionTime`
 - `SliceTiming`

### Dependencies

If you only installed the core of Clinica, this pipeline needs the installation of **SPM12** on your computer and depending on your options, the software **FSL 6.0** might be required. You can find how to install these software packages on the [third-party](http://www.clinica.run/doc/Third-party/-party) page.

### Running the pipeline

The pipeline can be run with the following command line:

```shell
clinica run fmri-preprocessing bids_directory caps_directory
```

Where:

- `bids_directory` is the input folder containing the dataset in a [BIDS](http://www.clinica.run/doc/BIDS/) hierarchy.
- `caps_directory` is the output folder containing the results in a [CAPS](http://www.clinica.run/doc/CAPS/Introduction/) hierarchy.

If you want to run the pipeline on a subset of your BIDS dataset, you can use the `-tsv` flag to specify in a TSV file the participants belonging to your subset.

#### Options

<!-- I put all the options as header titles in order to be able to get the hyperlink ancher. -->

##### `--full_width_at_half_maximum`

A list of integers specifying the full width at half maximum (FWHM) filter size in the three directions `x y z`, in millimeters, used to smooth the images. Default value is: `8 8 8` (isomorphic smoothing of size 8 mm).

##### `--t1_native_space`

When specified, the corrected fMRI data registered to the native T1 space of each subject are saved. This might be useful when dealing with parcellations that are in the native T1 space, such as the ones automatically generated by the [`t1-freesurfer`](http://www.clinica.run/doc/Pipelines/T1_FreeSurfer/) pipeline using the Destrieux and Desikan atlases.

> :warning: Warning :warning:
>
> The generated file might be large and reach few gigabytes depending on your T1 resolution!

##### `--freesurfer_brain_mask`

When specified, the pipeline uses the brain extraction generated by FreeSurfer during the [`t1-freesurfer`](../T1_FreeSurfer) pipeline. Otherwise, it computes it using the **SPM** Registration tool followed by empirically-estimated operations performed by **FSL**.

> **Note:**
>
> If you apply the previous option (`--t1_native_space`) and plan to parcellate the resulting fMRI volumes using FreeSurfer-based atlases, then **this option is recommended** to keep the same mask as the one already used by FreeSurfer.

##### `--unwarping`

When specified, the unwarping correction step is executed. This will add **SPM**'s Unwarping to the Realign step. This flag can be chosen if you have a phase difference image and at least one magnitude image (case "Phase difference image and at least one magnitude image
" in the [BIDS specifications](https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/01-magnetic-resonance-imaging-data.html#phase-difference-image-and-at-least-one-magnitude-image)).

> :warning: Warning :warning:
>
>	You absolutely need the following fields in the JSON file associated your `phasediff` image (see the official [BIDS specifications](http://bids.neuroimaging.io/) for more details):
>
 - `EchoTime1`
 - `EchoTime2`
 - `PhaseEncodingDirection`

### Outputs
```
subjects/
└── sub-<participant_label>/
    └── ses-<session_label>/
        └── fmri/
            └── preprocessing/
                ├── <source_T1w>_brainmask.nii.gz
                ├── <source_bold>_motion.tsv
                ├── <source_bold>_space-Ixi549Space_fwhm-8x8x8_preproc.nii.gz
                ├── <source_bold>_space-Ixi549Space_preproc.nii.gz
                ├── <source_bold>_space-meanBOLD_preproc.nii.gz
                └── <source_bold>_space-T1w_preproc.nii.gz
```

It contains the following files:

- `<source_file>_motion.tsv`: Table of parameters estimated for the head motion correction step (**SPM**'s realign tool).
- `<source_file>_space-Ixi549Space_fwhm-<kernel_size>_preproc.nii.gz`: Smoothed version of the file below.
- `<source_file>_space-Ixi549Space_preproc.nii.gz`: Preprocessed fMRI data in Ixi549 (MNI) space.
- `<source_file>_space-meanBOLD_preproc.nii.gz`: Preprocessed fMRI registered to the mean BOLD image.
- [optional] `<source_file>_space-T1w_preproc.nii.gz`: Preprocessed fMRI registered to the T1 native space.
- `<source_T1w_file>_brainmask.nii.gz`: Brain mask used to register the fMRI volumes to the different spaces cited above.


The `<source_bold>_motion.tsv` corresponds to the translations (`TransX`, `TransY`, and `TransZ`) in mm and the rotations (`RotX`, `RotY`, and `RotZ`) in each volume as compared to the first one, generated by the Realign tool of **SPM**. Thus, the size of the array should be `Mx6`, `M` being the number of volumes in the original fMRI file.

> **Note:**
>
> The naming convention for suffixes tried to follow the [BIDS Extension Proposal 12 (BEP012): BOLD processing derivatives](https://docs.google.com/document/d/16CvBwVMAs0IMhdoKmlmcm3W8254dQmNARo-7HhE-lJU/edit#) as much as possible.



### Describing this pipeline in your paper

#### Example of paragraph
> These results have been obtained using the `fmri-preprocessing` pipeline of Clinica (http://www.clinica.run). Slice timing correction, motion correction, [unwarping], [and smoothing with a kernel of size `<kernel_size>` mm] have been applied using [SPM tools](http://web.mit.edu/spm_v12/manual.pdf). Separately the brain mask has been extracted from the T1 image of each subject using [FSL&SPM | FreeSurfer]. The resulting fMRI images have then been registered [to the brain-masked T1 image of each subject | to the MNI space | to the mean image of each subject] using SPM's registration tool.  

#### Example of paragraph (long version)
> These results have been obtained using the `fmri-preprocessing` pipeline of Clinica (http://www.clinica.run). A slice timing correction [[Henson et al., 1999](http://discovery.ucl.ac.uk/5679/)] was performed to correct for time shifts between consecutive 2D slice acquisitions using the "Slice Timing" SPM tool. Motion correction using the "Realign [& Unwarp]: Estimate and Reslice" tool from SPM was then applied to realign time-series of images acquired from the same subject using a least squares approach and a rigid body (6 parameters) spatial transformation [[Friston et al., 1995](https://doi.org/10.1006/nimg.1995.1019)]. [At the same time, an unwarping step removes the variance caused by the susceptibility-by-movement interaction by using a fieldmap computed using the SPM's "Fieldmap Toolbox".]  [The resulting corrected images were then smoothed using a Gaussian kernel of width `<kernel_size>` mm using SPM's "Smooth" tool.] Separately the brain mask has been extracted from the T1 image of each subject using [SPM's "Segment" tool followed by FSL's dilation, erosion, thresholding and filling operations | Clinica's [`t1-freesurfer`](T1_FreeSurfer) pipeline based on FreeSurfer's `recon-all` command line tool]. The resulting fMRI images have then been registered [to the brain-masked T1 image of each subject | to the MNI space | to the mean image of each subject] using SPM's "Registration" tool.  
