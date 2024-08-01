from enum import Enum


class ExtendedEnum(Enum):
    @classmethod
    def valid_types(cls):
        return list(map(lambda c: c.value, cls))


class Attack(ExtendedEnum):
    EXTRACTION = 'extraction'
    EVASION = 'evasion'
    INFERENCE = 'inference'
    POISONING = 'poisoning'
    DATA_POISONING = 'data-poisoning'
    MODEL_POISONING = 'model-poisoning'
    SUPPLY_CHAIN = 'supply-chain'


class Task(ExtendedEnum):
    IMAGE_CLASSIFICATION = 'image_classification'
    IMAGE_SEGMENTATION = 'image_segmentation'
    TIMESERIES_FORECAST = 'timeseries_forecasting'
    NLP = 'nlp'
    TABULAR_CLASSIFICATION = 'tabular_classification'
    TEXT_RECOMMENDATION = 'text_recommendation'
    OBJECT_DETECTION = 'object_detection'
    ALL_TASK = 'all_task'


class ReportType(ExtendedEnum):
    VULNERABILITY = 'vulnerability'
    DEFENSE = 'defense'
    DEFENSE_ARTIFACT = 'defense_artifact'
    ATTACK_SAMPLES = 'attack_samples'


class FileFormat(ExtendedEnum):
    TXT = 'txt'
    PDF = 'pdf'
    JSON = 'json'
    XML = 'xml'
    ALL = 'all'


class SupportedFramework(ExtendedEnum):
    TENSORFLOW = 'tensorflow'
    SCIKIT_LEARN = 'scikit-learn'
    ONNX = 'onnx'


class UploadURIKeys(ExtendedEnum):
    MODEL_ID_KEY = 'model_id'
    URLS_KEY = 'urls'
    URL_KEY = 'url'
    FIELDS_KEY = 'fields'
    DATA_UPLOAD_URI_KEY = 'data_upload_url'
    LABEL_UPLOAD_URI_KEY = 'label_upload_url'
    MODEL_UPLOAD_URI_KEY = 'model_upload_url'
    MINMAX_UPLOAD_URI_KEY = 'minmax_upload_url'
    CLEAN_MODEL1_UPLOAD_URI_KEY = 'clean_model1_upload_url'
    CLEAN_MODEL2_UPLOAD_URI_KEY = 'clean_model2_upload_url'
    FINE_TUNED_MODEL_UPLOAD_URI_KEY = 'fine_tuned_model_upload_url'
    UNIVERSAL_DATA_UPLOAD_URI_KEY = 'universal_data_upload_url'
    FILE_UPLOAD_URI = 'file_upload_url'


class ResponseStatus(ExtendedEnum):
    SUCCESS = 'success'
    FAILED = 'failed'
