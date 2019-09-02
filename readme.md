# HD-GLIO

## Introduction

This repository provides easy to use access to our HD-GLIO brain tumor segmentation tool. HD-GLIO is the result of a 
joint project between the Department of Neuroradiology at the Heidelberg University Hospital, Germany and the 
Division of Medical Image Computing at the German Cancer Research Center (DKFZ) Heidelberg, Germany. If you are using 
HD-GLIO, please cite the following two publications:

- Kickingereder P, Isensee F, Tursunova I, Petersen J, Neuberger U, Bonekamp D, Brugnara G, Schell M, Kessler T, 
Foltyn M, Harting I, Sahm F, Prager M, Nowosielski M, Wick A, Nolden M, Radbruch A, Debus J, Schlemmer HP, Heiland S, 
Platten M, von Deimling A, van den Bent MJ, Gorlia T, Wick W, Bendszus M, Maier-Hein KH. Automated quantitative tumour 
response assessment of MRI in neuro-oncology with artificial neural networks: a multicentre, retrospective study. 
Lancet Oncol. 2019 May;20(5):728-740. (https://doi.org/10.1016/S1470-2045(19)30098-1)
- Isensee F, Petersen J, Kohl SAA, Jaeger PF, Maier-Hein KH. nnU-Net: Breaking the Spell on 
Successful Medical Image Segmentation. arXiv preprint 2019 arXiv:1904.08128. (https://arxiv.org/abs/1904.08128)

HD-GLIO was developed with 3220 MRI examinations from 1450 brain tumor patients (80% for training and 20% for testing). 
Specifically the data included:
1) a single-institutional retrospective dataset with 694 MRI examinations from 495 patients acquired at the 
Department of Neuroradiology, Heidelberg University Hospital, Germany (corresponding to the “Heidelberg training 
dataset and Heidelberg test dataset” described in Kickingereder et al. Lancet Oncol. 2019)
2) a multicentric clinical trial dataset with 2034 MRI examinations from 532 patients acquired across 34 institutions 
in Europe  (corresponding to the “EORTC-26101 test dataset” described in Kickingereder et al. Lancet Oncol. 2019)
3) a single-institutional retrospective dataset with 492 MRI examinations from 423 patients (80% glial brain tumors, 
20% other histological entities) undergoing routine MRI at different stages of the disease (including 79 early 
postoperative MRI scans acquired <72h after surgery) at the Department of Neuroradiology, Heidelberg University 
Hospital, Germany 
 
Specifically, each MRI examination included precontrast T1-weighted, postcontrast T1-weighted, T2-weighted and FLAIR 
sequences (all sequences brain extracted and co-registered) as well as corresponding ground-truth tumor segmentation 
masks. HD-GLIO performs brain tumor segmentation for contrast-enhancing tumor and non-enhancing T2/FLAIR signal 
abnormality. We applied a variant of the nnU-Net ('no-new-Net') framework (as described in Isensee et al. arXiv preprint 2019) 
for training the HD-GLIO algorithm.

HD-GLIO is very fast on GPU with <10s run time per MRI examination. 

## Installation Instructions

###  Installation Requirements
Unlike HD-BET, HD-GLIO requires a GPU to perform brain tumor segmentation. Any GPU with 4 GB of VRAM and cuda/pytorch 
support will do. 
Running the prediction on CPU is not supported.

### Installation with Pip
Installation with pip is quick an easy, just run the following command and everything will be done for you:

`pip install hd_glio`

### Manual installation
If you intend to modify HD-GLIO, you can also install is manually:

1) Clone this repository:
    
    `git clone https://github.com/MIC-DKFZ/HD-GLIO`

2) Go into the repository (the folder with the setup.py file) and install:

    `cd HD-GLIO`

    `pip install -e .`

Per default, model parameters will be downloaded to ~/.hd_glio_params. If you wish to use a different folder, open 
hd_glio/paths.py in a text editor and modify folder_with_parameter_files.


Both manual and pip installation will install two commands with which you can use HD-GLIO from anywhere in your 
system: `hd_glio_predict` and `hd_glio_predict_folder`.

## How to use it
Using HD_GLIO is straightforward. You can use it in any terminal on your linux system. The `hd_glio_predict` and 
`hd_glio_predict_folder` commands were installed automatically. HD-GLIO requires a GPU with at least 4 GB of VRAM to run. 

### Prerequisites
HD-GLIO was trained with four MRI modalities: T1, constrast-enhanced T1, T2 and FLAIR. All these modalities must be present
in order to run HD-GLIO. 

All input files must be provided as nifti (.nii.gz) files containing 2D or 3D MRI image data. Sequences with 
multiple temporal volumes (i.e. 4D sequences) are not supported (however can be splitted upfront into the individual 
temporal volumes using fslsplit1). 

- INPUT_T1 must be a T1-weighted sequence before contrast-agent administration (T1-w) acquired as 2D with axial 
orientation (e.g. TSE) or as 3D (e.g. MPRAGE)
- INPUT_CT1 must be a T1-weighted sequence after contrast-agent administration (cT1-w) acquired as 2D with axial 
orientation (e.g. TSE) or as 3D (e.g. MPRAGE)
- INPUT_T2 must be a T2-weighted sequence (T2-w) acquired as 2D 
- INPUT_FLAIR must be a fluid attenuated inversion recovery (FLAIR) sequence acquired as 2D with axial orientation
 (e.g. TSE). A 3D acquisition (e.g. 3D TSE/FSE) may work as well.
 
(These specifications are in line with the consensus recommendations for a standardized brain tumor imaging protocol 
in clinical trials - see Ellingson et al. Neuro Oncol. 2015 Sep;17(9):1188-98 - www.ncbi.nlm.nih.gov/pubmed/26250565)

Input files must contain 3D images; Sequences with multiple temporal volumes (i.e. 4D sequences) are not supported 
(however can be splitted upfront into the individual temporal volumes using fslsplit<sup>1</sup>).

All input files must match the orientation of standard MNI152 template and must be brain extracted and co-registered. 
All non-brain voxels must be 0.
To ensure that these pre-processing steps are performed correctly you may adhere to the following example:

```
# reorient MRI sequences to standard space
fslreorient2std T1.nii.gz T1_reorient.nii.gz
fslreorient2std CT1.nii.gz CT1_reorient.nii.gz
fslreorient2std T2.nii.gz T2_reorient.nii.gz
fslreorient2std FLAIR.nii.gz FLAIR_reorient.nii.gz

# perform brain extraction using HD-BET (https://github.com/MIC-DKFZ/HD-BET)
hd-bet -i T1_reorient.nii.gz
hd-bet -i CT1_reorient.nii.gz
hd-bet -i T2_reorient.nii.gz
hd-bet -i FLAIR_reorient.nii.gz 

# register all sequences to T1
fsl5.0-flirt -in CT1_reorient.nii.gz -ref T1_reorient.nii.gz -out CT1_reorient_reg.nii.gz -dof 6 -interp spline
fsl5.0-flirt -in T2_reorient.nii.gz -ref T1_reorient.nii.gz -out T2_reorient_reg.nii.gz -dof 6 -interp spline
fsl5.0-flirt -in FLAIR_reorient.nii.gz -ref T1_reorient.nii.gz -out FLAIR_reorient_reg.nii.gz -dof 6 -interp spline

# reapply T1 brain mask (this is important because HD-GLIO expects non-brain voxels to be 0 and the registration 
process can introduce nonzero values
# T1_BRAIN_MASK.nii.gz is the mask (not the brain extracted image!) as obtained from HD-Bet
fsl5.0-fslmaths CT1_reorient_reg.nii.gz -mas T1_BRAIN_MASK.nii.gz CT1_reorient_reg_bet.nii.gz
fsl5.0-fslmaths T2_reorient_reg.nii.gz -mas T1_BRAIN_MASK.nii.gz T2_reorient_reg_bet.nii.gz
fsl5.0-fslmaths FLAIR_reorient_reg.nii.gz -mas T1_BRAIN_MASK.nii.gz FLAIR_reorient_reg_bet.nii.gz
```

After applying this example you would use `T1_reorient.nii.gz`, `CT1_reorient_reg_bet.nii.gz`, `T2_reorient_reg_bet.nii.gz` 
and `FLAIR_reorient_reg_bet.nii.gz` to proceed.


### Run HD-GLIO
HD-GLIO provides two main scripts: `hd_glio_predict` and `hd_glio_predict_folder`.

#### Predicting a single case
`hd_glio_predict` can be used to predict a single case. It is useful for exploration or if the number of cases to be 
procesed is low. Here is how to use it:

`hd_glio_predict -t1 T1_FILE -t1c CT1_FILE -t2 T2_FILE -flair FLAIR_FILE -o OUTPUT_FILE`

T1_FILE, CT1_FILE, T2_FILE, FLAIR_FILE and OUTPUT_FILE must all be niftis (end with .nii.gz). The four input files must 
be preprocesed as specified in *How to use it - Prerequisites* (ses above). 

#### Predicting multiple cases
`hd_glio_predict_folder` is useful for batch processing, especially if the number of cases to be processed is large. By 
interleaving preprocessing, inference and segmentation export we can speed up the prediction significantly. Furthermore, 
the pipeline is initialized only once for all cases, again saving a lot of computation time.  Here is how to use it:

`hd_glio_predict_folder -i INPUT_FOLDER -o OUTPUT_FOLDER`

INPUT_FOLDER hereby contains the T1, T1c, T2 and FLAIR images. In order to ensure that HD-GLIO correctly assigns 
filenames to modalities, you **must** apply the following naming convention to your data

- INPUT_T1: PATIENT_IDENTIFIER_0000.nii.gz
- INPUT_CT1: PATIENT_IDENTIFIER_0001.nii.gz
- INPUT_T2: PATIENT_IDENTIFIER_0002.nii.gz
- INPUT_FLAIR: PATIENT_IDENTIFIER_0003.nii.gz

Hereby, PATIENT_IDENTIFIER can be anything. You can use an arbitrary number of patients (by using a different 
PATIENT_IDENTIFIER for each patient). Predicted segmentations will be saved as `PATIENT_IDENTIFIER.nii.gz` in the 
OUTPUT_FOLDER


<sup>1</sup>https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/Fslutils
