from typing import Union
from .chatbot_base_class import _BaseChatBot, getModels


# Chat Bot Class
class ChatBot:
    __baseChatBot = None

    # Initialize the Object
    def __init__(
        self,
        model="gpt-4",
        saveChatHistory: bool = False,
        pastChatHistory: list = [],
        persona: Union[None, str] = None,
        silent=False,
    ) -> None:
        """
        # Description:
            Use ChatGPT for Free!

        ### Parameters:
            model: Your Model Choice. You Can use `gpt-3.5-turbo` or `gpt-4`.
                We Suggest that you use the Default Model for a Faster and less `Daily Limit Reached` Error.
            saveChatHistory: [True | False].
                Will save the Chat History if `True`Passed
            pastChatHistory: [List of Past Chat History].
            silent: If `True` Passed, by the Program nothing will be printed in the Console.
        """
        self.__baseChatBot = _BaseChatBot(
            model,
            saveChatHistory=saveChatHistory,
            pastChatHistory=pastChatHistory,
            persona=persona,
            silent=silent,
        )

    # Send Request to Server
    def sendRequest(self, prompt):
        """
        ## Returns:
        ```
        {
            "success": Boolean,
            "content": Reply from Bot,
            "model": Model Name,
            "usage": Tokens Used,
            "message": Error Message, if "success" is False
        }
        ```
        """
        return self.__baseChatBot.sendRequest(prompt=prompt)

    # Get Chat History
    def getChatHistory(self):
        return self.__baseChatBot.getChatHistory()

    # Clear Chat History
    def clearChatHistory(self):
        self.__baseChatBot.clearChatHistory()

    # Reset bot Persona
    def resetBotPersona(self):
        self.__baseChatBot.resetBotPersona()


# Version
__version__ = "1.0"
