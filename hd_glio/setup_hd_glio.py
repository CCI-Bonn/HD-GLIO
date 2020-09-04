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

from urllib.request import urlopen
from batchgenerators.utilities.file_and_folder_operations import *
from hd_glio.paths import folder_with_parameter_files
import shutil
import zipfile
import numpy as np


def maybe_download_weights():
    download_weights = False
    if not isfile(join(folder_with_parameter_files, 'fold_0', "model_final_checkpoint.model")) or not \
            isfile(join(folder_with_parameter_files, 'fold_0', "model_final_checkpoint.model.pkl")):
        download_weights = True
    else:
        if not isfile(join(folder_with_parameter_files, 'version')):
            download_weights = True
        else:
            text = np.loadtxt(join(folder_with_parameter_files, 'version'), dtype=str)
            if text != '2':
                download_weights = True

    if download_weights:
        if isdir(folder_with_parameter_files):
            shutil.rmtree(folder_with_parameter_files)
        maybe_mkdir_p(folder_with_parameter_files)

        out_filename = join(folder_with_parameter_files, "parameters.zip")

        if not os.path.isfile(out_filename):
            url = "https://zenodo.org/record/4014850/files/hd_glio_v2_params.zip?download=1"
            print("Downloading", url, "...")
            data = urlopen(url).read()
            with open(out_filename, 'wb') as f:
                f.write(data)

        zipfile.ZipFile(out_filename).extractall(path=folder_with_parameter_files)
        os.remove(out_filename)

