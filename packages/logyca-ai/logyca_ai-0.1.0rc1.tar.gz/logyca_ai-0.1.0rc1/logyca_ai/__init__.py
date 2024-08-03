from logyca_ai.assets_for_examples.conversation_samples import (
    get_content_image_sample,
    get_content_pdf_sample,
    get_content_simple_sample,
    )
from logyca_ai.utils.constants.content import ContentRole, ContentType
from logyca_ai.utils.constants.image import ImageResolution
from logyca_ai.utils.helpers.azure_openai_chatgpt import AzureOpenAIChatGPT
from logyca_ai.utils.schemes.input.conversations import (
    AssistantMessage,
    Content,
    ImageMessage,
    PDFMessage,
    UserMessage,
    )
