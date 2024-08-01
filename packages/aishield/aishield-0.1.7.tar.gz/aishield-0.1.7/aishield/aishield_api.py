from typing import Optional

from aishield.connection import RequestProcessor
from aishield.constants import (
    FileFormat,
    ReportType,
    Attack,
    Task,
    UploadURIKeys,
    ResponseStatus
)
from aishield.configs import (
    OutputConf,
    JobDetails
)
from aishield.image_classification import (
    extraction as ic_extraction,
    evasion as ic_evasion,
    poision as ic_poison
)
from aishield.tabular_classification import (
    extraction as tc_extraction,
    evasion as tc_evasion
)
from aishield.timeseries_forecasting import extraction as tsf_extraction
from aishield.image_segmentation import extraction as is_extraction
from aishield.natural_language_processing import extraction as nlp_extraction
from aishield.text_recommendation import extraction as tr_extraction
from aishield.object_detection import (
    extraction as od_extraction,
    evasion as od_evasion
)
from aishield.all_task import supply_chain as supply_chain
from aishield.utils.util import (
    uri_validator,
    get_all_keys_by_val
)
from aishield.utils.util import delete_keys_from_dict
from aishield.utils import logger

LOG = logger.getLogger(__name__)

class VulnConfig:
    """
    Instantiates the vulnerability configs based on task and attack type
    """

    def __new__(cls, task_type: Optional[Task] = Task.IMAGE_CLASSIFICATION,
                analysis_type: Optional[Attack] = Attack.EXTRACTION,
                defense_generate: Optional[bool] = True):
        """
        Return the Vulnerability Config object

        Parameters
        ----------
        task_type: Type of task. Example: Image Classification, Image Segmentation, NLP, etc.
        analysis_type: Type of analysis_type(attack) for which vulnerability assessment has to be done.Example: Extraction, Evasion,etc.
        defense_generate: Boolean flag to specify if defense needs to be generated if model found to be vulnerable

        Returns
        -------
        vul_config_obj : Class Object
        """
        task_type_val = task_type.value
        attack_val = analysis_type.value
        if task_type_val not in Task.valid_types():
            raise ValueError('task_type param value {} is not in one of the accepted values {}.'.format(task_type_val,
                                                                                                        Task.valid_types()))
        if attack_val not in Attack.valid_types():
            raise ValueError('attack param value {} is not in one of the accepted values {}.'.format(attack_val,
                                                                                                     Attack.valid_types()))
        if analysis_type == Attack.SUPPLY_CHAIN:
            vul_config_obj = supply_chain.VulnConfig()
        else:
            if task_type == Task.IMAGE_CLASSIFICATION:
                if analysis_type == Attack.EXTRACTION:
                    vul_config_obj = ic_extraction.VulnConfig(defense_generate)
                elif analysis_type == Attack.EVASION:
                    vul_config_obj = ic_evasion.VulnConfig(defense_generate)
                elif analysis_type in [Attack.POISONING, Attack.MODEL_POISONING, Attack.DATA_POISONING]:
                    vul_config_obj = ic_poison.VulnConfig(defense_generate)
                else:
                    raise NotImplementedError('Feature coming soon')
            elif task_type == Task.TABULAR_CLASSIFICATION:
                if analysis_type == Attack.EXTRACTION:
                    vul_config_obj = tc_extraction.VulnConfig(defense_generate)
                elif analysis_type == Attack.EVASION:
                    vul_config_obj = tc_evasion.VulnConfig(defense_generate)
                else:
                    raise NotImplementedError('Feature coming soon')
            elif task_type == Task.TIMESERIES_FORECAST:
                if analysis_type == Attack.EXTRACTION:
                    vul_config_obj = tsf_extraction.VulnConfig(defense_generate)
                else:
                    raise NotImplementedError('Feature coming soon')
            elif task_type == Task.IMAGE_SEGMENTATION:
                if analysis_type == Attack.EXTRACTION:
                    vul_config_obj = is_extraction.VulnConfig(defense_generate)
                else:
                    raise NotImplementedError('Feature coming soon')
            elif task_type == Task.NLP:
                if analysis_type == Attack.EXTRACTION:
                    vul_config_obj = nlp_extraction.VulnConfig(defense_generate)
                else:
                    raise NotImplementedError('Feature coming soon')
            elif task_type == Task.TEXT_RECOMMENDATION:
                if analysis_type == Attack.EXTRACTION:
                    vul_config_obj = tr_extraction.VulnConfig(defense_generate)
                else:
                    raise NotImplementedError('Feature coming soon')
            elif task_type == Task.OBJECT_DETECTION:
                if analysis_type == Attack.EXTRACTION:
                    vul_config_obj = od_extraction.VulnConfig(defense_generate)
                elif analysis_type == Attack.EVASION:
                    vul_config_obj = od_evasion.VulnConfig(defense_generate)
                else:
                    raise NotImplementedError('Feature coming soon')
            else:
                raise NotImplementedError('New task-pairs would be added soon')

        return vul_config_obj


class AIShieldApi:
    """
    Instantiates for performing vulnerability analysis
    """

    def __init__(self, api_url: str, org_id: str):
        """
        Initializes the AIShield API with request headers

        Parameters
        ----------
        api_url: api endpoint of AIShield vulnerability analysis
        org_id: organization key
        """
        if not api_url:
            raise ValueError('AIShield api is not provided')
        if not org_id:
            raise ValueError('org_id is not provided')
        if not uri_validator(api_url):
            raise ValueError('aishield api is invalid')

        headers = {
            'Cache-Control': 'no-cache',
            'Org-Id': org_id
        }
        # Get api_key from org_id
        api_key = RequestProcessor(api_url, headers).get_api_key()
        # Append the api key to the headers, which will be used for all future requests
        headers['x-api-key'] = api_key

        self.request_processor = RequestProcessor(api_url, headers)
        self.job_details = JobDetails()
        self.task_type = None
        self.analysis_type = None
        self.job_payload = None

    def register_model(self, task_type: Optional[Task] = Task.IMAGE_CLASSIFICATION,
                       analysis_type: Optional[Attack] = Attack.EXTRACTION):
        """
            Perform the initial model registration process for vulnerability analysis

            Parameters
            ----------
            task_type: Type of task. Example: Image Classification, Image Segmentation, NLP, etc.
            analysis_type: Type of analysis_type(attack) for which vulnerability assessment has to be done.Example: Extraction, Evasion,etc.

            Returns
            -------
            status: registration status: success or failed
            job_details: having information of model_id, data_upload_uri, label_upload_uri, model_upload_uri
        """
        self.task_type = task_type
        self.analysis_type = analysis_type
        model_registration_payload = {
            'task_type': task_type.value,
            "analysis_type": analysis_type.value
        }
        status, response_json = self.request_processor.register(payload=model_registration_payload)
        self.job_details.model_id = response_json[UploadURIKeys.MODEL_ID_KEY.value]

        # data_upload_uri is valid for all task/analysis types except for supply chain attack.
        if analysis_type != Attack.SUPPLY_CHAIN:
            data_upload_dtls = response_json[UploadURIKeys.URLS_KEY.value][
                UploadURIKeys.DATA_UPLOAD_URI_KEY.value]
            # data upload details
            self.job_details.data_upload_uri = data_upload_dtls[UploadURIKeys.URL_KEY.value]
            self.job_details.data_upload_policy = data_upload_dtls[UploadURIKeys.FIELDS_KEY.value]

        if analysis_type == Attack.SUPPLY_CHAIN:
            file_upload_dtls = response_json[UploadURIKeys.URLS_KEY.value][
                UploadURIKeys.FILE_UPLOAD_URI.value]
            # model upload details
            self.job_details.file_upload_uri = file_upload_dtls[UploadURIKeys.URL_KEY.value]
            self.job_details.file_upload_policy = file_upload_dtls[UploadURIKeys.FIELDS_KEY.value]

        # model urls will be fetched for all except IC model poisoning (instead accepting fine_tuned model).
        # model upload is also valid for supply chain attack
        if not (task_type == Task.IMAGE_CLASSIFICATION and analysis_type == Attack.MODEL_POISONING):
            model_upload_dtls = response_json[UploadURIKeys.URLS_KEY.value][
                UploadURIKeys.MODEL_UPLOAD_URI_KEY.value]
            # model upload details
            self.job_details.model_upload_uri = model_upload_dtls[UploadURIKeys.URL_KEY.value]
            self.job_details.model_upload_policy = model_upload_dtls[UploadURIKeys.FIELDS_KEY.value]

        if analysis_type != Attack.SUPPLY_CHAIN:
            if (task_type in [Task.IMAGE_CLASSIFICATION, Task.IMAGE_SEGMENTATION, Task.OBJECT_DETECTION]):
                # label upload details
                label_upload_dtls = response_json[UploadURIKeys.URLS_KEY.value][UploadURIKeys.LABEL_UPLOAD_URI_KEY.value]
                self.job_details.label_upload_uri = label_upload_dtls[UploadURIKeys.URL_KEY.value]
                self.job_details.label_upload_policy = label_upload_dtls[UploadURIKeys.FIELDS_KEY.value]
                # Attack.POISONING in IC refers to by default DATA_POISONING
                if analysis_type in [Attack.POISONING, Attack.DATA_POISONING]:
                    # universal data upload  - data poisoning
                    universal_data_upload_dtls = response_json[UploadURIKeys.URLS_KEY.value][
                        UploadURIKeys.UNIVERSAL_DATA_UPLOAD_URI_KEY.value]
                    self.job_details.universal_data_upload_uri = universal_data_upload_dtls[UploadURIKeys.URL_KEY.value]
                    self.job_details.universal_data_upload_policy = universal_data_upload_dtls[
                        UploadURIKeys.FIELDS_KEY.value]
                if analysis_type == Attack.MODEL_POISONING:
                    # clean models upload details - model poisoning
                    clean_model1_upload_dtls = response_json[UploadURIKeys.URLS_KEY.value][
                        UploadURIKeys.CLEAN_MODEL1_UPLOAD_URI_KEY.value]
                    clean_model2_upload_dtls = response_json[UploadURIKeys.URLS_KEY.value][
                        UploadURIKeys.CLEAN_MODEL2_UPLOAD_URI_KEY.value]
                    clean_model_upload_uris = [clean_model1_upload_dtls[UploadURIKeys.URL_KEY.value],
                                               clean_model2_upload_dtls[UploadURIKeys.URL_KEY.value]]
                    clean_model_upload_policies = [clean_model1_upload_dtls[UploadURIKeys.FIELDS_KEY.value],
                                                   clean_model2_upload_dtls[UploadURIKeys.FIELDS_KEY.value]]
                    self.job_details.clean_model_upload_uris = clean_model_upload_uris
                    self.job_details.clean_model_upload_policies = clean_model_upload_policies
                    # fine-tuned model upload details - model poisoning
                    fine_tuned_model_upload_dtls = response_json[UploadURIKeys.URLS_KEY.value][UploadURIKeys.FINE_TUNED_MODEL_UPLOAD_URI_KEY.value]
                    self.job_details.fine_tuned_model_upload_uri = fine_tuned_model_upload_dtls[UploadURIKeys.URL_KEY.value]
                    self.job_details.fine_tuned_model_upload_policy = fine_tuned_model_upload_dtls[
                        UploadURIKeys.FIELDS_KEY.value]


            elif (task_type in [Task.TABULAR_CLASSIFICATION, Task.TIMESERIES_FORECAST]):
                # minmax upload details
                minmax_upload_dtls = response_json[UploadURIKeys.URLS_KEY.value][
                    UploadURIKeys.MINMAX_UPLOAD_URI_KEY.value]
                self.job_details.minmax_upload_uri = minmax_upload_dtls[UploadURIKeys.URL_KEY.value]
                self.job_details.minmax_upload_policy = minmax_upload_dtls[UploadURIKeys.FIELDS_KEY.value]
            elif task_type in [Task.NLP, Task.TEXT_RECOMMENDATION]:
                pass  # These tasks only have data and model artifacts to upload
            else:
                raise NotImplementedError('New task-pairs would be added soon')
        return status, self.job_details

    def file_and_model_detector(self, repo_type: str = 'huggingface', repo_url: str = None, branch_name: str = 'main',
                                depth: int = 1):
        # detect model files and notebook files in a given repo
        payload = {"repo_type":repo_type, "repo_url": repo_url, "branch_name": branch_name, "depth": depth}
        status, response_json = self.request_processor.detect_or_upload_repo_artifacts(payload=payload)
        detected_files, detected_models = [], []
        if 'detected_files' in response_json:
            detected_files = response_json['detected_files']
        else:
            LOG.warning('detected_files could not be found in response')
        if 'detected_models' in response_json:
            detected_models = response_json['detected_models']
        else:
            LOG.warning('detected_models could not be found in response')

        return status, detected_files, detected_models


    def upload_repo_artifacts(self, model_id: str = None, repo_type: str = 'huggingface', repo_url: str = None,
                              branch_name: str = 'main', depth: int = 1, model_file: str = "", files: str = ""):
        upload_status_msg = []
        error_flag = False
        # upload requisite files for analysis
        upload_file = 'yes'
        payload = {"repo_type": repo_type, "repo_url": repo_url, "branch_name": branch_name, "depth": depth,
                   "upload_file": upload_file, "model_id": model_id, "model_file": model_file, "files": files}
        status, response_json = self.request_processor.detect_or_upload_repo_artifacts(payload=payload)

        # if files were provided for upload, check for file upload status
        if files and 'file_upload_status' in response_json and response_json["file_upload_status"] == 'successful':
            upload_status_msg.append('files(s) upload successful')
        else:
            error_flag = True
            upload_status_msg.append('file(s) upload failed')

        # if model-files were provided for upload, check for model-file upload status
        if model_file and 'model_upload_status' in response_json and response_json["model_upload_status"] == 'successful':
            upload_status_msg.append('model(s) upload successful')
        else:
            error_flag = True
            upload_status_msg.append('model(s) upload failed')

        if error_flag:
            raise Exception('some error occurred while uploading. Status is: {}'.format(', '.join(upload_status_msg)))
        return upload_status_msg


    def upload_input_artifacts(self, job_details: JobDetails, data_path: str = None,  universal_data_path: str = None,
                               label_path: str = None, minmax_path: str = None, model_path: str = None,
                               fine_tuned_model_path : str = None, clean_model_paths: list = None) -> list:
        """
            Upload the input artifacts such as data, label and model file

            Parameters
            ----------
            job_details: object having information such as model_id, data_upload_uri, label_upload_uri, model_upload_uri
            data_path: location of data file
            label_path: location of label file
            minmax_path: location of minmax file(used for tabular data)
            model_path: location of model file
            clean_model_paths: location of clean model files. Required for model poisoning check

            Returns
            -------
            upload_status_msg: all upload messages in a list
        """
        if clean_model_paths is None:
            clean_model_paths = []
        upload_status_msg = []
        error_flag = False
        if data_path:
            data_upload_uri = job_details.data_upload_uri
            data_upload_policy = job_details.data_upload_policy
            upload_status = self.request_processor.upload_file(file_path=data_path, upload_uri=data_upload_uri,
                                                               upload_policy=data_upload_policy)
            if upload_status == ResponseStatus.SUCCESS:
                upload_status_msg.append('data file upload successful')
            else:
                error_flag = True
                upload_status_msg.append('data file upload failed')

        if universal_data_path:
            universal_data_upload_uri = job_details.universal_data_upload_uri
            universal_data_upload_policy = job_details.universal_data_upload_policy
            upload_status = self.request_processor.upload_file(file_path=universal_data_path, upload_uri=universal_data_upload_uri,
                                                               upload_policy=universal_data_upload_policy)
            if upload_status == ResponseStatus.SUCCESS:
                upload_status_msg.append('universal_data file upload successful')
            else:
                error_flag = True
                upload_status_msg.append('universal_data file upload failed')

        if label_path:
            label_upload_uri = job_details.label_upload_uri
            label_upload_policy = job_details.label_upload_policy
            upload_status = self.request_processor.upload_file(file_path=label_path, upload_uri=label_upload_uri,
                                                               upload_policy=label_upload_policy)
            if upload_status == ResponseStatus.SUCCESS:
                upload_status_msg.append('label file upload successful')
            else:
                error_flag = True
                upload_status_msg.append('label file upload failed')

        if minmax_path:
            minmax_upload_uri = job_details.minmax_upload_uri
            minmax_upload_policy = job_details.minmax_upload_policy
            upload_status = self.request_processor.upload_file(file_path=minmax_path, upload_uri=minmax_upload_uri,
                                                               upload_policy=minmax_upload_policy)
            if upload_status == ResponseStatus.SUCCESS:
                upload_status_msg.append('minmax file upload successful')
            else:
                error_flag = True
                upload_status_msg.append('minmax file upload failed')

        if model_path:
            model_upload_uri = job_details.model_upload_uri
            model_upload_policy = job_details.model_upload_policy
            upload_status = self.request_processor.upload_file(file_path=model_path, upload_uri=model_upload_uri,
                                                               upload_policy=model_upload_policy)
            if upload_status == ResponseStatus.SUCCESS:
                upload_status_msg.append('model file upload successful')
            else:
                error_flag = True
                upload_status_msg.append('model file upload failed')

        if fine_tuned_model_path:
            fine_tuned_model_upload_uri = job_details.fine_tuned_model_upload_uri
            fine_tuned_model_upload_policy = job_details.fine_tuned_model_upload_policy
            upload_status = self.request_processor.upload_file(file_path=fine_tuned_model_path, upload_uri=fine_tuned_model_upload_uri,
                                                               upload_policy=fine_tuned_model_upload_policy)
            if upload_status == ResponseStatus.SUCCESS:
                upload_status_msg.append('fine_tuned model file upload successful')
            else:
                error_flag = True
                upload_status_msg.append('fine_tuned model file upload failed')

        if clean_model_paths:
            num_clean_models_required = 2
            if len(clean_model_paths) < 2 or not all(clean_model_paths):
                raise Exception('Model poison analysis requires atleast {} numbers of clean model'.format(
                    num_clean_models_required))
            clean_model_upload_uris = job_details.clean_model_upload_uris
            clean_model_upload_policies = job_details.clean_model_upload_policies
            for idx in range(num_clean_models_required):
                upload_status = self.request_processor.upload_file(file_path=clean_model_paths[idx],
                                                                   upload_uri=clean_model_upload_uris[idx],
                                                                   upload_policy=clean_model_upload_policies[idx])
                if upload_status == ResponseStatus.SUCCESS:
                    upload_status_msg.append('clean model file{} upload successful'.format(idx))
                else:
                    error_flag = True
                    upload_status_msg.append('clean model file{} upload failed'.format(idx))
        if error_flag:
            raise Exception('some error occurred while uploading. Status is: {}'.format(', '.join(upload_status_msg)))
        return upload_status_msg

    def vuln_analysis(self, model_id: str = None, vuln_config: VulnConfig = None):
        """
        Perform Vulnerability analysis of the model

        Parameters
        ----------
        model_id: model id obtained after model registration
        vuln_config: configs for vulnerability analysis of VulnConfig type

        Returns
        -------
        status: job status: success or failed
        job_details: having information such as job_id, monitoring link
        """

        if not model_id:
            raise ValueError('model_id must be provided')
        if not vuln_config:
            raise ValueError('vulnerability config must be provided')

        payload = {key: getattr(vuln_config, key) for key in dir(vuln_config) if not key.startswith('_')}
        payload = delete_keys_from_dict(payload, ['task_type', 'attack',
                                                  'get_all_params'])  # delete non-relevant params for API call
        # validation - raise error any key in payload has None value
        keys_with_none_val = get_all_keys_by_val(payload, None)
        if keys_with_none_val:
            raise ValueError('None values found for {}.'.format(', '.join(keys_with_none_val)))

        # task_type = vuln_config.task_type
        # attack_strategy = vuln_config.attack

        # if self.task_type != task_type or attack_strategy != self.analysis_type:
        #     raise Exception('Mismatch in task_type, analysis_type specified in model registration and analysis')

        self.job_payload = payload
        status, response_json = self.request_processor.send_for_analysis(model_id=model_id, payload=payload)
        self.job_details.job_id = response_json['job_id']
        self.job_details.job_dashboard_uri = response_json['dashboard_link']
        return status, self.job_details

    def job_status(self, job_id):
        """
        Prints the status of each vulnerability analysis while the job is running.
        Once job completes, returns with status: success or failed

        Parameters
        ----------
        job_id: job_id returned from the request

        Returns
        -------
        status: success or failed
        """
        status = self.request_processor.get_job_status(job_id=job_id,
                                                       task_type=self.task_type,
                                                       analysis_type=self.analysis_type,
                                                       job_payload=self.job_payload)
        return status

    def save_job_report(self, job_id: str = None, output_config: OutputConf = None) -> str:
        """
        Save the artifacts of the vulnerability analysis.

        Parameters
        ----------
        job_id: job_id returned from the request
        output_config: object with OutputConf Type

        Returns
        -------
        saved_loc: location where the artifact got saved.
        """
        if not job_id or job_id is None:
            raise ValueError('invalid job id value')
        file_format = output_config.file_format.value.lower()
        report_type = output_config.report_type.value.lower()
        save_folder_path = output_config.save_folder_path

        if file_format not in FileFormat.valid_types():
            raise ValueError('invalid file_format value {}. Must be one of {}'.format(file_format,
                                                                                      FileFormat.valid_types()))
        if report_type not in ReportType.valid_types():
            raise ValueError('invalid report_type value {}. Must be one of {}'.format(report_type,
                                                                                      ReportType.valid_types()))

        # poisoning supports only pdf report format type
        if self.analysis_type == Attack.POISONING and not (FileFormat(output_config.file_format) == FileFormat.PDF):
            raise ValueError('invalid file_format value. poisoning analysis supports only pdf type')

        # For below alpha release task pairs, defense artifacts are not generated
        if self.task_type in [Task.NLP, Task.TEXT_RECOMMENDATION] and \
                (ReportType(output_config.report_type) in [ReportType.DEFENSE, ReportType.DEFENSE_ARTIFACT]):
            raise ValueError('defense is not supported for this task, thus artifacts not generated.')

        saved_loc = self.request_processor.get_artifacts(job_id=job_id, report_type=report_type,
                                                         file_format=file_format,
                                                         save_folder_path=save_folder_path)
        return saved_loc
