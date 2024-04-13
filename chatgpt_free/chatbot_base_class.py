from typing import Union
from .utils import _filterPastChatHistory, getModels
from .servers.servers_original import _getServer


# The ChatBot Class
class _BaseChatBot:
    __currentModel = ""
    __currentServer = None
    __botPersona = []
    __botPersonaRetrain = []
    __botPersonaText = None
    __saveChatHistory = False
    __chatHistory = []

    """
    Chat History contains the Chat Data.
    ### Structure:
    {
        "role": [assistant || user],
        "content": [Message Content]

    }
    """

    # Initialize the Object
    def __init__(
        self,
        model: str,
        saveChatHistory: bool = False,
        pastChatHistory: list = [],
        persona: Union[None, str] = None,
        silent=False,
    ):
        filteredChatHistory = _filterPastChatHistory(pastChatHistory)
        if not (type(filteredChatHistory) is list):
            if not (silent):
                print(f"{filteredChatHistory}\nSkipping Past History...")
            filteredChatHistory = []

        self.__currentModel = model
        self.__saveChatHistory = saveChatHistory
        self.__chatHistory = filteredChatHistory
        if persona:
            self.__botPersonaText = persona
            modifiedPersona = f"""Follow the Below Given Persona / Instructions:\n`{persona}`\nIf you get it, Just reply with `Okay!`"""
            self.__botPersona = [
                {"role": "user", "content": modifiedPersona},
                {"role": "assistant", "content": "Okay!"},
            ]
            modifiedPersonaRetrain = f"""-------------------\nRetraining: Follow the Below Given Persona / Instructions:\n`{persona}`\nIf you get it, Just reply with `Okay!`\n-------------------"""
            self.__botPersonaRetrain = [
                {"role": "user", "content": modifiedPersonaRetrain},
                {"role": "assistant", "content": "Okay!"},
            ]

        if model not in getModels():
            Server = _getServer("gpt-4")

        Server = _getServer(model)

        self.__currentServer = Server()

    # Make Request
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
        if not (self.__saveChatHistory):
            messages = self.__botPersona
        elif len(self.__chatHistory) == 0:
            messages = self.__botPersona
        elif len(self.__chatHistory) % 20 == 0:
            messages = self.__chatHistory + self.__botPersonaRetrain
        else:
            messages = self.__botPersona + self.__chatHistory

        serverResponse = self.__currentServer.makeRequest(
            prompt=prompt,
            messages=messages,
        )
        if not (serverResponse.get("success")):
            return serverResponse

        userMsg = {"role": "user", "content": prompt}
        botMsg = {"role": "assistant", "content": serverResponse.get("content")}

        if self.__saveChatHistory:
            self.__chatHistory.append(userMsg)
            self.__chatHistory.append(botMsg)

        return serverResponse

    # Get Chat History
    def getChatHistory(self):
        return self.__chatHistory

    # Clear Chat History
    def clearChatHistory(self):
        if self.__chatHistory:
            self.__chatHistory = []

    # Reset bot Persona
    def resetBotPersona(self):
        if self.__botPersona:
            self.__botPersona = []
