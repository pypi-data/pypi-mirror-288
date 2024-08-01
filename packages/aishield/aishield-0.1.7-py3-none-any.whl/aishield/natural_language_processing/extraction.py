from aishield.constants import Attack
from aishield.natural_language_processing.base_nlp import NLPVulnerabilityConfig
from aishield.utils.util import delete_keys_from_dict
from aishield.utils import logger

LOG = logger.getLogger(__name__)

class VulnConfig(NLPVulnerabilityConfig):
    def __init__(self, defense_generate):
        super().__init__()
        if defense_generate:
            LOG.warning('defense is not supported for this task. Proceeding with defense_generate as False')
        self.number_of_attack_queries = 200
        self.attack_type = 'blackbox'
        self.encryption_strategy = 0
        self.use_model_api = 'no'
        self.model_api_details = ''
        self.attack = Attack.EXTRACTION

    @property
    def number_of_attack_queries(self):
        return self.__number_of_attack_queries

    @number_of_attack_queries.setter
    def number_of_attack_queries(self, num_attack_queries):
        self.__number_of_attack_queries = num_attack_queries

    @property
    def encryption_strategy(self):
        return self.__encryption_strategy

    @encryption_strategy.setter
    def encryption_strategy(self, encryption_strategy):
        valid_encryption_strategy = [0, 1]
        if encryption_strategy not in valid_encryption_strategy:
            raise Exception('encryption_strategy can be 0 or 1')
        self.__encryption_strategy = encryption_strategy

    @property
    def attack_type(self):
        return self.__attack_type

    @attack_type.setter
    def attack_type(self, attack_type):
        self.__attack_type = attack_type

    def get_all_params(self):
        params = super(VulnConfig, self).get_all_params()
        params = delete_keys_from_dict(params, ['task_type', 'attack'])
        return params
