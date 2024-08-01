from typing import List, Optional, Union

from api_schemas.base import BaseInputModel
from docarray import BaseDoc, DocList
from docarray.base_doc.doc import BaseDocWithoutId
from docarray.typing.bytes import ImageBytes
from docarray.typing.url import AnyUrl
from docarray.utils._internal.pydantic import bytes_validator
from pydantic import BaseModel, Field, root_validator


class ExecutorUsage(BaseDoc):
    """
    The usage of the classification services to report,
    e.g. number of tokens in case of text input
    """

    total_tokens: int = Field(
        description='The number of tokens used to embed the input text'
    )


# EXECUTOR MODELS
## Model to be imported by the Executor and used by the Universal API
class TextDoc(BaseDoc):
    """Document containing a text field"""

    text: str


class Label(BaseDocWithoutId):
    label: str = Field(description='The label of the classification')
    confidence: Optional[float] = Field(
        description='The confidence of the classification'
    )


class SerializeImageBytes(ImageBytes):
    @classmethod
    def _docarray_validate(
        cls,
        value,
    ):
        if isinstance(value, str):
            import base64

            return cls(base64.b64decode(value))
        else:
            value = bytes_validator(value)
            return cls(value)

    def _docarray_to_json_compatible(self):
        """
        Convert itself into a json compatible object
        """
        import base64

        encoded_str = base64.b64encode(self).decode('utf-8')
        return encoded_str


class Url(AnyUrl):
    @classmethod
    def _docarray_validate(
        cls,
        value,
    ):
        import urllib.parse

        if isinstance(value, str):
            if urllib.parse.urlparse(value).scheme not in {'http', 'https'}:
                raise ValueError(
                    'This does not have a valid URL schema ("http" or "https")'
                )

        return cls(value)

    @classmethod
    def is_extension_allowed(cls, value) -> bool:
        """Returns a list of allowed file extensions for the class
        that are not covered by the mimetypes library."""
        import urllib.parse

        if isinstance(value, str):
            if urllib.parse.urlparse(value).scheme in {'http', 'https'}:
                return True
            else:
                return False

        return True


class ImageDoc(BaseDoc):
    """ImageDoc with fields"""

    url: Optional[Url] = Field(
        description='URL of an image file',
        default=None,
    )
    bytes: Optional[SerializeImageBytes] = Field(
        description='base64 representation of the Image.',
        default=None,
    )
    image: Optional[Union[Url, SerializeImageBytes]] = Field(
        description='Image representation that can hold URL of an image or a base64 representation',  # noqa
        default=None,
    )

    @root_validator(pre=False)
    def validate_all_input(cls, value):
        if (
            value.get('image', None) is None
            and value.get('url', None) is None
            and value.get('bytes', None) is None
        ):
            raise ValueError('image, URL or bytes need to be provided')
        if value.get('image', None) is not None:
            image = value.get('image')
            if isinstance(image, SerializeImageBytes):
                value['bytes'] = image
                value['image'] = None
            elif isinstance(image, AnyUrl):
                value['url'] = image
                value['image'] = None
            else:
                raise ValueError(
                    'image must be a valid URL or base64 image representation'
                )
        return value


## Model to be imported by the Executor and used by the Universal API
class ClassificationOutputDoc(BaseDoc):
    """Document to be returned by the classification backend, containing the
    classification result and the token usage for the corresponding input texts"""

    # TODO: remove the optional
    prediction: Optional[str] = Field(
        description='The label with the highest probability'
    )
    confidence: Optional[float] = Field(
        description='The softmax probability of the prediction'
    )
    labels: Optional[List[Label]] = Field(
        description='List of labels with their corresponding probabilities'
    )
    usage: Optional[ExecutorUsage]


# UNIVERSAL API MODELS
class TextClassificationInput(BaseDocWithoutId):
    """The input to the API for text classification"""

    model: str = Field(
        description='The identifier of the model.\n'
        '\nAvailable models and corresponding param size and dimension:\n'
        '- `jina-clip-v1`,\t223M,\t768\n'
        '- `jina-embeddings-v2-base-en`,\t137M,\t768\n'
        '- `jina-embeddings-v2-base-es`,\t161M,\t768\n'
        '- `jina-embeddings-v2-base-de`,\t161M,\t768\n'
        '- `jina-embeddings-v2-base-zh`,\t161M,\t768\n'
        '- `jina-embeddings-v2-base-code`,\t137M,\t768\n'
        '\nFor more information, please checkout our [technical blog](https://arxiv.org/abs/2307.11224).\n',  # noqa
    )

    input: Union[List[Optional[str]], Optional[str], List[TextDoc], TextDoc] = Field(
        description='List of texts to classify',
    )
    labels: Union[List[Label], List[str]] = Field(
        description='List of labels for classification'
    )

    @classmethod
    def validate(
        cls,
        value,
    ):
        if 'input' not in value:
            raise ValueError('"input" field missing')
        if 'model' not in value:
            raise ValueError('you must provide a model parameter')
        if 'labels' not in value:
            raise ValueError('you must provide a labels parameter')

        return super().validate(value)

    class Config(BaseDoc.Config):
        extra = 'forbid'
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "model": "jina-embeddings-v2-base-en",
                "input": ["Hello, world!", "How are you?"],
                "labels": ["Apple", "Banana"],
            },
        }


class ImageClassificationInput(BaseDocWithoutId):
    """The input to the API for image classifcation"""

    model: str = Field(
        description='The identifier of the model.\n'
        '\nAvailable models and corresponding param size and dimension:\n'
        '- `jina-clip-v1`,\t223M,\t768\n'
        '\nFor more information, please checkout our [technical blog](https://arxiv.org/abs/2405.20204).\n',  # noqa
    )

    input: Union[ImageDoc, List[ImageDoc]] = Field(
        description='List of images to embed',
    )
    labels: Union[List[Label], List[str]] = Field(
        description='List of labels for classification'
    )

    @classmethod
    def validate(
        cls,
        value,
    ):
        if 'input' not in value:
            raise ValueError('"input" field missing')
        if 'model' not in value:
            raise ValueError('you must provide a model parameter')
        if 'labels' not in value:
            raise ValueError('you must provide a labels parameter')

        return super().validate(value)

    class Config(BaseDoc.Config):
        extra = 'forbid'
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "model": "clip",
                "input": ["bytes or URL"],
                "labels": ["Apple", "Banana"],
            },
        }


class MixedClassificationInput(BaseDocWithoutId):
    """The input to the API for text and image classification"""

    model: str = Field(
        description='The identifier of the model.\n'
        '\nAvailable models and corresponding param size and dimension:\n'
        '- `jina-clip-v1`,\t223M,\t768\n'
        '\nFor more information, please checkout our [technical blog](https://arxiv.org/abs/2405.20204).\n',  # noqa
    )

    input: List[Union[ImageDoc, TextDoc, str]] = Field(
        description='List of text and images to embed',
    )
    labels: Union[List[Label], List[str]] = Field(
        description='List of labels for classification'
    )

    @classmethod
    def validate(
        cls,
        value,
    ):
        if 'input' not in value:
            raise ValueError('"input" field missing')
        if 'model' not in value:
            raise ValueError('you must provide a model parameter')
        if 'labels' not in value:
            raise ValueError('you must provide a labels parameter')

        return super().validate(value)

    class Config(BaseDoc.Config):
        extra = 'forbid'
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "model": "clip",
                "input": ["bytes or URL or str"],
                "labels": ["Apple", "Banana"],
            },
        }


class ClassificationObject(BaseDocWithoutId):
    """Classification object"""

    object: str = 'classification'
    index: int = Field(
        description='The index of the classification output, corresponding to the index in the list of inputs'  # noqa
    )
    prediction: str = Field(description='The label with the highest probability')
    confidence: float = Field(description='The softmax probability of the prediction')
    labels: DocList[Label] = Field(
        description='List of labels with their corresponding probabilities'
    )

    class Config(BaseDocWithoutId.Config):
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "prediction": "label1",
                "confidence": 0.7,
                "labels": [
                    {"label": "label1", "confidence": 0.5},
                    {"label": "label2", "confidence": 0.3},
                ],
                "object": "classification",
            }
        }


class Usage(BaseModel):
    total_tokens: int = Field(
        description='The number of tokens used by all the texts in the input'
    )
    prompt_tokens: int = Field(description='Same as total_tokens')


class ModelClassificationOutput(BaseInputModel):
    """Output of the classification service"""

    object: str = 'list'
    data: DocList[ClassificationObject] = Field(
        description='A list of Classification Objects returned by the classification service'  # noqa
    )
    usage: Usage = Field(
        description='Total usage of the request. Sums up the usage from each individual input'  # noqa
    )

    class Config(BaseInputModel.Config):
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "data": [
                    {
                        "index": 0,
                        "prediction": "label1",
                        "confidence": 0.7,
                        "labels": [
                            {"label": "label1", "confidence": 0.5},
                            {"label": "label2", "confidence": 0.3},
                        ],
                        "object": "classification",
                    },
                    {
                        "index": 1,
                        "prediction": "label2",
                        "confidence": 0.8,
                        "labels": [
                            {"label": "label1", "confidence": 0.2},
                            {"label": "label2", "confidence": 0.8},
                        ],
                        "object": "classification",
                    },
                ],
                "usage": {"total_tokens": 15, "prompt_tokens": 15},
            }
        }
