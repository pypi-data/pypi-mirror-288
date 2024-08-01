from aishield.constants import Attack
from aishield.utils.util import delete_keys_from_dict
from aishield.all_task.base import AllVulnerabilityConfig


class VulnConfig(AllVulnerabilityConfig):
    def __init__(self):
        self.attack = Attack.SUPPLY_CHAIN


    def get_all_params(self):
        params = super(VulnConfig, self).get_all_params()
        params = delete_keys_from_dict(params, ['task_type', 'attack'])
        return params
