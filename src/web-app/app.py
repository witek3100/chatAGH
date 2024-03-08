from src.chatbot.chat import Chat

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/home', methods=['GET'])
def home():
  return render_template('home_tab.html')

@app.route('/chat/<chat_id>', methods=['GET', 'POST'])
def chat(chat_id):
  print(chat_id)

  chat = Chat(chat_id=chat_id)

  if request.method == 'GET':
    pass

  if request.method == 'POST':
    print('asking')
    user_input = request.form.get("user_input")
    print(user_input)
    chat.ask(user_input)
    print(chat.history)

    bot_message = "This is a placeholder bot response. You can replace this with functionalities to process user input and generate responses."

  return render_template('chat_tab.html', chat=chat)

if __name__ == '__main__':
  chat = None
  app.run(debug=True)
