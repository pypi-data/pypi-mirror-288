from app.utils.constants.content import ContentType, ContentRole
from app.utils.schemes.input.conversations import Content, UserMessage, ImageMessage, PDFMessage
from app.utils.schemes.output.conversations import ConversationAnswer, ConversationUsage
from openai import AsyncAzureOpenAI
from openai.types.completion_usage import CompletionUsage
from starlette import status as http_status

class AzureOpenAIChatGPT():

    def __init__(self,azure_endpoint:str,api_key:str,api_version:str) -> None:
        self.client = AsyncAzureOpenAI(
            azure_endpoint=f"https://{azure_endpoint}.openai.azure.com",
            api_key=api_key,
            api_version=api_version
        )
    
    def build_conversation_message_list(self,content:Content)->list:
        """Description
        
        ### Example message list with conversation history
        ```Python
        messages=[
                {"role":"system","content":""},
                {"role":"user","content":""},
                {"role":"assistant","content":""},
                {"role":"user","content":""},
                {"role":"assistant","content":""},
        ]
        ```
        """


        messages= []

        if content.system and content.system!="":
            messages.append({"role":str(ContentRole.SYSTEM),"content":content.system})

        for message in content.messages:
            assistant_message = message.get(ContentRole.ASSISTANT,None)
            if assistant_message is not None:
                messages.append({"role":str(ContentRole.ASSISTANT),"content":assistant_message})
            else:
                user_message = message.get(ContentRole.USER,None)
                if user_message is None:
                    raise ValueError(f"Unsopported role {user_message}")
                else:
                    type_message = message.get("type",None)                

                    if type_message in ImageMessage.get_default_types():
                        additional_content = message.get("additional_content",None)
                        messages.append({"role":str(ContentRole.USER),"content":[
                            ImageMessage(**additional_content).build_message_content()
                        ]})

                    if type_message in PDFMessage.get_default_types():
                        additional_content = message.get("additional_content",None)
                        messages.append({"role":str(ContentRole.USER),"content":
                            PDFMessage(**additional_content).build_message_content()
                        })

                    if user_message is not None and user_message!="":
                        messages.append({"role":str(ContentRole.USER),"content":user_message})


        return messages

    async def conversation_async(self,
        model:str,
        messages:list,
        limit_tokens_answer:int=4000,
        temperature:float=0.7,
        top_p:float=0.95)->tuple[int,ConversationAnswer]:
        """Description
        :return int,str: Http Status Code Response, Message
        
        References:

        - https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/migration
        
        """
        try:
            completion = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature, # The closer you get to 1 the answer changes, if you want the same answer you should get closer to zero
                max_tokens=limit_tokens_answer,
                top_p=top_p, # 0.1 means only the tokens comprising the top 10% probability mass are considered. Default 1 => 100% probability mass are considered
                frequency_penalty=0,
                presence_penalty=0,
                stop=None
            )
            response=completion.model_dump()
            usage:CompletionUsage = completion.usage
            conversation_response = ConversationAnswer()
            conversation_response.assistant = str(response['choices'][0]['message']['content']).strip()
            conversation_response.usage_data = ConversationUsage(**usage.__dict__)
            return http_status.HTTP_200_OK,conversation_response
        except Exception as e:
            return http_status.HTTP_429_TOO_MANY_REQUESTS,str(e)

