from logyca_ai.utils.constants.image import ImageResolution
from logyca_ai.utils.constants.content import ContentRole, ContentType
from logyca_ai.utils.helpers.azure_openai_chatgpt import AzureOpenAIChatGPT
from logyca_ai.utils.schemes.input.conversations import Content, UserMessage, AssistantMessage, PDFMessage, ImageMessage

from samples.assets_for_conversations.conversation_samples import get_content_image_sample
from samples.assets_for_conversations.file_or_documents.imagen_base64 import image_base64_sample
from samples.assets_for_conversations.file_or_documents.Registro_sanitario_7702007075540_RS_base64 import pdf_base64_sample
