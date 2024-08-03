from logyca_ai.utils.constants.content import ContentType, ContentRole
from logyca_ai.utils.constants.image import ImageResolution
from logyca_ai.utils.helpers.content_loaders import url_file_to_base64, extract_text_from_pdf_base64
from pydantic import BaseModel, AliasChoices, Field, model_validator
from typing import Any

class MessageExceptionErrors:
    UNSUPPORTED_IMAGE_FORMAT="Unsupported image format: {}"
    UNSUPPORTED_PDF_FORMAT="Unsupported image format: {}"

class Content(BaseModel):
    system: str = Field(default="Personality, context, purpose.",validation_alias=AliasChoices(ContentRole.SYSTEM))
    messages: list = Field(default=[],validation_alias=AliasChoices("messages"))
    
    @model_validator(mode="before")
    def check_keys(cls, values):
        return values

    def to_dict(self)->dict:
        return self.__dict__

class UserMessage(BaseModel):
    additional_content: Any = Field(default="",validation_alias=AliasChoices("additional_content"))
    type: str = Field(default=ContentType.TEXT,validation_alias=AliasChoices("type"))
    user: str = Field(default="",validation_alias=AliasChoices("user"))
    
    @model_validator(mode="before")
    def check_keys(cls, values):
        return values

    def to_dict(self)->dict:
        return self.__dict__

    @classmethod
    def get_supported_types(cls)->list:        
        return ContentType.get_type_list()

    @classmethod
    def get_default_types(cls)->list:        
        return [ContentType.TEXT]

class AssistantMessage(BaseModel):
    assistant: str = Field(default="",validation_alias=AliasChoices("assistant"))
    
    @model_validator(mode="before")
    def check_keys(cls, values):
        return values

    def to_dict(self)->dict:
        return self.__dict__
    
class ImageMessage(BaseModel):
    base64_content_or_url: str = Field(default="",validation_alias=AliasChoices("base64_content_or_url"))
    image_format: str = Field(default="",validation_alias=AliasChoices("image_format"))
    image_resolution: str = Field(default=ImageResolution.AUTO,validation_alias=AliasChoices("image_resolution"))
    
    @model_validator(mode="before")
    def check_keys(cls, values):
        return values

    def to_dict(self)->dict:
        return self.__dict__
    
    def __get_mime_types(self,extension:str=None)->str|dict|None:
        mime_types={
            "bmp":"bmp",
            "gif":"gif",
            "jpeg":"jpeg",
            "jpg":"jpg",
            "png":"png",
            "svg":"svg+xml",
            "webp":"webp",
        }
        if extension is None:
            return mime_types
        else:
            mime_type=mime_types.get(extension,None)
            if mime_type is None:
                return None
            else:
                return mime_type

    @classmethod
    def get_supported_formats(cls)->list:        
        return [key for key, value in cls().__get_mime_types().items()]
        
    @classmethod
    def get_default_types(cls)->list:        
        return [ContentType.IMAGE_URL,ContentType.IMAGE_BASE64]

    def build_message_content(self)->dict|None:
        if self.image_format == ContentType.IMAGE_URL:
            url=self.base64_content_or_url
        else:
            mime_type=self.__get_mime_types(self.image_format)
            if mime_type is None:
                raise ValueError(MessageExceptionErrors.UNSUPPORTED_IMAGE_FORMAT.format(self.image_format))
            url=f"data:image/{mime_type};base64,{self.base64_content_or_url}"
        return {
            "type": "image_url",
            "image_url": {
            "url" : url, 
            "detail" : str(self.image_resolution)
            }
        }


class PDFMessage(BaseModel):
    base64_content_or_url: str = Field(default="",validation_alias=AliasChoices("base64_content_or_url"))
    pdf_format: str = Field(default="",validation_alias=AliasChoices("pdf_format"))
    
    @model_validator(mode="before")
    def check_keys(cls, values):
        return values

    def to_dict(self)->dict:
        return self.__dict__
    
    def __get_pdf_formats(self,extension:str=None)->str|dict|None:
        pdf_formats={
            "pdf":"pdf",
        }
        if extension is None:
            return pdf_formats
        else:
            mime_type=pdf_formats.get(extension,None)
            if mime_type is None:
                return None
            else:
                return mime_type

    @classmethod
    def get_supported_formats(cls)->list:        
        return [key for key, value in cls().__get_pdf_formats().items()]
        
    @classmethod
    def get_default_types(cls)->list:        
        return [ContentType.PDF_URL,ContentType.PDF_BASE64]

    def build_message_content(self)->str|None:
        if self.pdf_format == ContentType.PDF_URL:
            pdf_text=extract_text_from_pdf_base64(url_file_to_base64(self.base64_content_or_url))
        else:
            pdf_text=extract_text_from_pdf_base64(self.base64_content_or_url)
        return pdf_text
   