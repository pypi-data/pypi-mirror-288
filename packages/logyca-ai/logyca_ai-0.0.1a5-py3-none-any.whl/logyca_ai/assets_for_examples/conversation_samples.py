from app.utils.schemes.input.conversations import (
    AssistantMessage,
    Content,
    ImageMessage,
    PDFMessage,
    UserMessage,
)
from app.utils.constants.content import ContentType
from app.utils.constants.image import ImageResolution
from app.utils.schemes.input.content_base64_image_sample import image_base64_sample
from app.utils.schemes.input.content_base64_pdf_sample import pdf_base64_sample

content_simple_example = Content(
    system="""
                Voy a definirte tu personalidad, contexto y proposito.
                Actua como un experto en venta de frutas.
                Se muy positivo.
                Trata a las personas de usted, nunca tutees sin importar como te escriban.
            """.strip(),
    messages=[
        UserMessage(user="Dime 5 frutas amarillas"),
        AssistantMessage(assistant="""
                ¡Claro! Aquí te van 5 frutas amarillas:

                1. Plátano
                2. Piña
                3. Mango
                4. Melón
                5. Papaya
            """
        ),
        UserMessage(user="Dame los nombres en ingles."),
    ]
    )

def get_content_image_sample(image_sample_base64:bool=False)->Content:
    image_resolution=str(ImageResolution.AUTO)
    if image_sample_base64:
        base64_content_or_url=image_base64_sample
        image_format="png"
        type_message=ContentType.IMAGE_BASE64
    else:
        base64_content_or_url="https://raw.githubusercontent.com/logyca/python-libraries/main/logyca-ai/samples/assets_for_conversations/file_or_documents/imagen.png"
        image_format=ContentType.IMAGE_URL
        type_message=ContentType.IMAGE_URL
    return Content(
        system="""
                Actua como una maquina lectora de imagenes.
                Devuelve la información sin lenguaje natural, sólo responde lo que se está solicitando.
                El dispositivo que va a interactuar contigo es una api, y necesita la información sin markdown u otros caracteres especiales.
                """.strip(),
        messages=[
            UserMessage(
                user="Extrae el texto que recibas en la imagen y devuelvelo en formato json.",
                type=type_message,
                additional_content=ImageMessage(
                    base64_content_or_url=base64_content_or_url,
                    image_format=image_format,
                    image_resolution=image_resolution,
                ).to_dict()
            )
        ]
    )

def get_content_pdf_sample(pdf_sample_base64:bool=False)->Content:
    if pdf_sample_base64:
        base64_content_or_url=pdf_base64_sample
        pdf_format="pdf"
        type_message=ContentType.PDF_BASE64
    else:
        base64_content_or_url="https://raw.githubusercontent.com/logyca/python-libraries/main/logyca-ai/samples/assets_for_conversations/file_or_documents/Registro_sanitario_7702007075540_RS.pdf"
        pdf_format=ContentType.PDF_URL
        type_message=ContentType.PDF_URL
    return Content(
        system="""
                No uses lenguaje natural para la respuesta.
                Dame la información que puedas extraer de la imagen en formato JSON.
                Solo devuelve la información, no formatees con caracteres adicionales la respuesta.
                """.strip(),
        messages=[
            UserMessage(
                user="Dame los siguientes datos: Expediente, radicación, Fecha, Numero de registro, Vigencia.",
                type=type_message,
                additional_content=PDFMessage(
                    base64_content_or_url=base64_content_or_url,
                    pdf_format=pdf_format,
                ).to_dict()
            )
        ]
    )



