#    Copyright 2019 Division of Medical Image Computing, German Cancer Research Center (DKFZ), Heidelberg, Germany
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from hd_glio.utils import blockPrint, enablePrint
blockPrint()
from nnunet.inference.predict import predict_from_folder
enablePrint()
import argparse
from hd_glio.paths import folder_with_parameter_files
from hd_glio.setup_hd_glio import maybe_download_weights


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_folder", type=str, required=True,
                        help="folder with input files, files must be named PATIENTID_0000.nii.gz, "
                             "PATIENTID_0001.nii.gz, PATIENTID_0002.nii.gz, PATIENTID_0003.nii.gz for T1, "
                             "T1c, T2 and Flair, respectively. There can be an arbitrary number of patients "
                             "in the folder (PATIENTID can be anything). CAREFUL: The files MUST fullfill the "
                             "following criteria: 1) They must be brain extracted with the non-brain region being "
                             "0 (you can achieve that by using hd-bet (https://github.com/MIC-DKFZ/HD-BET); 2) "
                             "They must be coregistered and in the same co-ordinate system (pixels arrays must be "
                             "aligned) 3) makse sure the T1, T1c, T2 and FLAIR file always have the correct "
                             "file ending (_0000.nii.gz, ...)")
    parser.add_argument("-o", "--output_folder", type=str, required=True,
                        help="output folder. This is there the resulting segmentations will be saved (as PATIENT_ID."
                             "nii.gz). Cannot be the same folder as the input folder. If output_folder does not exist "
                             "it will be created")
    parser.add_argument("-p", "--processes", default=4, type=str, required=False,
                        help="number of processes for data preprocessing and nifti export. You should not have to "
                             "touch this. So don't unless there is a clear indication that it is required. Default: 4")
    parser.add_argument('--overwrite_existing', default=True, type=str, required=False,
                        help="set to False to keep segmentations in output_folder and continue where you left off "
                             "(useful if something crashes). If True then all segmentations that may already be "
                             "present in output_folder will be overwritten. Default: True")

    args = parser.parse_args()
    input_folder = args.input_folder
    output_folder = args.output_folder
    processes = args.processes
    overwrite_existing = args.overwrite_existing

    maybe_download_weights()

    predict_from_folder(folder_with_parameter_files, input_folder, output_folder, (0, ), False, processes, processes,
                        None, 0, 1, True, overwrite_existing=overwrite_existing, checkpoint_name='model_best')


if __name__ == "__main__":
    main()
