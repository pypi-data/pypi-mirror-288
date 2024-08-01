from pprint import pprint

from aishield.constants import Task, SupportedFramework
from aishield.utils.util import get_class_attributes


class TRVulnerabilityConfig:
    """
    Instantiates the base class for vulnerability config of Text Recommendation

    Returns
    -------
    Initialized config parameters required for vulnerability analysis 
    """

    def __init__(self):
        """
        Initializes the vulnerability config parameters for Text Recommendation task
        Parameters
        ----------
        defense_generate: if defense needs to be generated if vulnerabilities found in the model
        """
        self.model_framework = "tensorflow"
        self.task_type = Task.TEXT_RECOMMENDATION

    def get_all_params(self):
        """
        Get the initialized configs for vulnerability analysis
        Returns
        -------
        class_attribs: initialized configs
        """
        class_attribs = get_class_attributes(self)
        # pprint(class_attribs)
        return class_attribs

    @property
    def model_framework(self):
        return self.__model_framework

    @model_framework.setter
    def model_framework(self, model_framework):
        if model_framework.lower() not in SupportedFramework.valid_types():
            raise Exception('model_framework provided {} not supported. Supported: {}'
                            .format(model_framework, ', '.join(SupportedFramework.valid_types())))
        self.__model_framework = model_framework
