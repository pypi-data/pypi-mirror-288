from aishield.constants import Attack
from aishield.object_detection.base_od import ODVulnerabilityConfig
from aishield.utils.util import delete_keys_from_dict
from aishield.utils import logger

LOG = logger.getLogger(__name__)


class VulnConfig(ODVulnerabilityConfig):
    def __init__(self, defense_generate):
        super().__init__()
        self.use_model_api = 'no'
        self.model_api_details = ''
        self.normalize_data = 'no'
        self.defense_bestonly = "no"
        self.attack = Attack.EVASION


    @property
    def defense_bestonly(self):
        return self.__defense_bestonly

    @defense_bestonly.setter
    def defense_bestonly(self, defense_bestonly):
        self.__defense_bestonly = defense_bestonly

    @property
    def normalize_data(self):
        return self.__normalize_data

    @normalize_data.setter
    def normalize_data(self, normalize_data):
        if normalize_data.lower() not in ['yes', 'no']:
            raise Exception('normalize_data field can be yes or no')
        self.__normalize_data = normalize_data

    def get_all_params(self):
        params = super(VulnConfig, self).get_all_params()
        params = delete_keys_from_dict(params, ['task_type', 'attack'])
        return params
