from chatgpt_free import ChatBot

persona = "You are a QnA answering bot. No Description for any Answer. Give only the Actual Answer in max one sentence."

# chatbot = ChatBot(persona=persona)
chatbot = ChatBot(saveChatHistory=True)

print("\nFree ChatBot - Version 1.0\n")

while True:
    try:
        message = input("\nYOU: ")
        response = chatbot.sendRequest(prompt=message)
        if response["success"]:
            reply = response["content"]
            print("BOT:", reply)
        else:
            print("~ Error:", response["message"])
    except KeyboardInterrupt:
        break


print("\nEnd of Chat!")
