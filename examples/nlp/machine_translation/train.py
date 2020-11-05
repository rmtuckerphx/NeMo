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


import pytorch_lightning as pl
from omegaconf import DictConfig

from nemo.collections.common.callbacks import MachineTranslationLogEvalCallback
from nemo.collections.nlp.models.machine_translation import TransformerMTModel
from nemo.core.config import hydra_runner
from nemo.utils import logging
from nemo.utils.exp_manager import exp_manager
from nemo.utils.get_rank import is_global_rank_zero


@hydra_runner(config_path="conf", config_name="transformer_mt_config")
def main(cfg: DictConfig) -> None:
    logging.info(f'Config: {cfg.pretty()}')
    trainer = pl.Trainer(**cfg.trainer, callbacks=[MachineTranslationLogEvalCallback()])
    exp_manager(trainer, cfg.get("exp_manager", None))
    transformer_mt = TransformerMTModel(cfg.model, trainer=trainer)
    trainer.fit(transformer_mt)
    if is_global_rank_zero():
        with open("best_checkpoint_path.txt", 'w') as f:
            f.write(trainer.checkpoint_callback.best_model_path)


if __name__ == '__main__':
    main()