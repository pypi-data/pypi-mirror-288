from aishield.constants import Attack
from aishield.object_detection.base_od import ODVulnerabilityConfig
from aishield.utils.util import delete_keys_from_dict
from aishield.utils import logger

LOG = logger.getLogger(__name__)


class VulnConfig(ODVulnerabilityConfig):
    def __init__(self, defense_generate):
        super().__init__()
        if defense_generate:
            LOG.warning('defense is not supported for this task. Proceeding with defense_generate as False')
        self.encryption_strategy = 0
        self.use_model_api = 'no'
        self.model_api_details = ''
        self.attack = Attack.EXTRACTION

    @property
    def encryption_strategy(self):
        return self.__encryption_strategy

    @encryption_strategy.setter
    def encryption_strategy(self, encryption_strategy):
        valid_encryption_strategy = [0, 1]
        if encryption_strategy not in valid_encryption_strategy:
            raise Exception('encryption_strategy can be 0 or 1')
        self.__encryption_strategy = encryption_strategy

    def get_all_params(self):
        params = super(VulnConfig, self).get_all_params()
        params = delete_keys_from_dict(params, ['task_type', 'attack'])
        return params
