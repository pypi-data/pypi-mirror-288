import os
from typing import List

from aishield.constants import (
    FileFormat,
    ReportType,
)
from aishield.utils.util import check_or_create_directory


class UploadPolicy:
    def __init__(self, policy=None):
        self.policy = policy

    @property
    def policy(self):
        return self.__policy

    @policy.setter
    def job_id(self, policy):
        self.__policy = policy


class JobDetails:
    """
    Instantiates to details of a vulnerability analysis job
    """

    def __init__(self, job_id=None, job_dashboard_uri=None, model_id=None, data_upload_uri=None, file_upload_uri=None,
                 universal_data_upload_uri=None, label_upload_uri=None,
                 minmax_upload_uri: str = None, model_upload_uri=None, fine_tuned_model_upload_uri=None, clean_model_upload_uris=[],
                 data_upload_policy: dict = {}, universal_data_upload_policy = {}, label_upload_policy: dict = {},
                 minmax_upload_policy: dict = {}, model_upload_policy: dict = {}, fine_tuned_model_upload_policy = {},
                 clean_model_upload_policies: List[dict] = []):
        """
        Constructor for Job Details class.
        Parameters
        ----------
        job_id: job_id of the submitted job
        job_dashboard_uri: uri for monitoring the progress of job and downloading of output artifacts
        model_id: model id obtained after model registration
        data_upload_uri: uri returned by model registration service where data file in zip needs to be uploaded
        label_upload_uri: uri returned by model registration service where label file in zip needs to be uploaded
        minmax_upload_uri: uri returned by model registration service where minmax(for tabular data) file in zip needs to be uploaded
        model_upload_uri: uri returned by model registration service where model file in zip needs to be uploaded
        clean_model_upload_uris: uri's returned by model registration service where clean model files in zip needs to be uploaded (for model poison check)
        """
        self.job_id = job_id
        self.job_dashboard_uri = job_dashboard_uri
        self.model_id = model_id
        self.data_upload_uri = data_upload_uri
        self.file_upload_uri = file_upload_uri
        self.universal_data_upload_uri = universal_data_upload_uri
        self.label_upload_uri = label_upload_uri
        self.model_upload_uri = model_upload_uri
        self.fine_tuned_model_upload_uri = fine_tuned_model_upload_uri
        self.minmax_upload_uri = minmax_upload_uri  # for Tabular datatype
        self.clean_model_upload_uris = clean_model_upload_uris  # for model poison analysis
        self.data_upload_policy = data_upload_policy
        self.universal_data_upload_policy = universal_data_upload_policy
        self.label_upload_policy = label_upload_policy
        self.minmax_upload_policy = minmax_upload_policy
        self.model_upload_policy = model_upload_policy
        self.fine_tuned_model_upload_policy = fine_tuned_model_upload_policy
        self.clean_model_upload_policies = clean_model_upload_policies

    @property
    def job_id(self):
        return self.__job_id

    @job_id.setter
    def job_id(self, job_id):
        self.__job_id = job_id

    @property
    def job_dashboard_uri(self):
        return self.__job_dashboard_uri

    @job_dashboard_uri.setter
    def job_dashboard_uri(self, job_dashboard_uri):
        self.__job_dashboard_uri = job_dashboard_uri

    @property
    def data_upload_uri(self):
        return self.__data_upload_uri

    @data_upload_uri.setter
    def data_upload_uri(self, data_upload_uri):
        self.__data_upload_uri = data_upload_uri

    @property
    def file_upload_uri(self):
        return self.__file_upload_uri

    @file_upload_uri.setter
    def file_upload_uri(self, file_upload_uri):
        self.__file_upload_uri = file_upload_uri

    @property
    def universal_data_upload_uri(self):
        return self.__universal_data_upload_uri

    @universal_data_upload_uri.setter
    def universal_data_upload_uri(self, universal_data_upload_uri):
        self.__universal_data_upload_uri = universal_data_upload_uri

    @property
    def label_upload_uri(self):
        return self.__label_upload_uri

    @label_upload_uri.setter
    def label_upload_uri(self, label_upload_uri):
        self.__label_upload_uri = label_upload_uri

    @property
    def minmax_upload_uri(self):
        return self.__minmax_upload_uri

    @minmax_upload_uri.setter
    def minmax_upload_uri(self, minmax_upload_uri):
        self.__minmax_upload_uri = minmax_upload_uri

    @property
    def model_upload_uri(self):
        return self.__model_upload_uri

    @model_upload_uri.setter
    def model_upload_uri(self, model_upload_uri):
        self.__model_upload_uri = model_upload_uri

    @property
    def fine_tuned_model_upload_uri(self):
        return self.__fine_tuned_model_upload_uri

    @fine_tuned_model_upload_uri.setter
    def fine_tuned_model_upload_uri(self, fine_tuned_model_upload_uri):
        self.__fine_tuned_model_upload_uri = fine_tuned_model_upload_uri

    @property
    def clean_model_upload_uris(self):
        return self.__clean_model_upload_uris

    @clean_model_upload_uris.setter
    def clean_model_upload_uris(self, clean_model_upload_uris):
        self.__clean_model_upload_uris = clean_model_upload_uris

    @property
    def model_id(self):
        return self.__model_id

    @model_id.setter
    def model_id(self, model_id):
        self.__model_id = model_id


class OutputConf:
    """
    OutputConf for getting reports(vulnerability/defense) or artifacts(defense model/sample attack data)
    """

    def __init__(self, report_type: ReportType = ReportType.VULNERABILITY, file_format: FileFormat = FileFormat.PDF,
                 save_folder_path=os.getcwd()):
        """
        Sets the OutputConf for getting reports(vulnerability/defense) or artifacts(defense model/sample attack data)
        Parameters
        ----------
        report_type: Report Type (Options : Vulnerability , Defense, Defense_artifact, Attack_samples)
        file_format: File format Type (Options : all, txt , pdf, json, xml}
        save_folder_path: output path where the artifacts would be saved
        """
        self.report_type = report_type
        self.file_format = file_format
        self.save_folder_path = save_folder_path

    @property
    def report_type(self):
        return self.__report_type

    @report_type.setter
    def report_type(self, report_type):
        self.__report_type = report_type

    @property
    def file_format(self):
        return self.__file_format

    @file_format.setter
    def file_format(self, file_format):
        self.__file_format = file_format

    @property
    def save_folder_path(self):
        return self.__save_folder_path

    @save_folder_path.setter
    def save_folder_path(self, save_folder_path):
        check_or_create_directory(save_folder_path)
        self.__save_folder_path = save_folder_path
