# Copyright (c) 2020, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import pytorch_lightning as pl
from omegaconf.listconfig import ListConfig
from pytorch_lightning import seed_everything

from nemo.collections.asr.models import ClusteringDiarizer
from nemo.core.config import hydra_runner
from nemo.utils import logging

"""
Basic run 
python speaker_diarize.py
"""

seed_everything(42)


@hydra_runner(config_path="conf", config_name="speaker_diarization.yaml")
def main(cfg):

    logging.info(f'Hydra config: {cfg.pretty()}')
    # sd_model=ClusteringDiarizer.restore_from("/data3/sdtest/model.nemo")
    sd_model = ClusteringDiarizer(cfg=cfg)
    sd_model.diarize()
    # sd_model.save_to("/data3/sdtest/model2.nemo")


if __name__ == '__main__':
    main()