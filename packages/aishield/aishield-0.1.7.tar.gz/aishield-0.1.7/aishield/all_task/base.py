from aishield import Task
from aishield.utils.util import get_class_attributes

class AllVulnerabilityConfig:
    """
    A class to represent a Not Applicable (N/A) Task type (or) which applies to all task types.
    This can be used by analysis types, which are task-agnostic in nature, like supply chain attacks.

    Returns
    -------
    Initialized config parameters required for vulnerability analysis
    """

    def __init__(self):
        """
        Initializes the vulnerability config parameters for a NA task
        """
        self.task_type = Task.ALL_TASK

    def get_all_params(self):
        """
        Get the initialized configs for vulnerability analysis
        Returns
        -------
        class_attribs: initialized configs
        """
        class_attribs = get_class_attributes(self)
        return class_attribs