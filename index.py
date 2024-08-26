import os
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer,ChatterBotCorpusTrainer
from flask import Flask,render_template,request
import requests

app = Flask(__name__)

bot = ChatBot("chatbot",read_only=False, 
    logic_adapters=[
        
        {
            "import_path":"chatterbot.logic.BestMatch",
            "default_response":"Sorry I don't have an answer",
            "maximum_similarity_threshold":0.90
        }
        
        ])


trainer = ChatterBotCorpusTrainer(bot)

trainer.train("chatterbot.corpus.english")



@app.route("/")
def main():
    return render_template("index.html")

#while True:
#    user_response = input("User: ")
#    print("Chatbot: " + str(bot.get_response(user_response)))

@app.route("/get")
def get_chatbot_response():
      userText = request.args.get('userMessage')
      rawData = requests.get("https://api.openweathermap.org/data/2.5/weather?q="+userText+"&appid=9d092d23bd86ce06427e9d68e0233d2c")
      result = rawData.json()
      return result

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
