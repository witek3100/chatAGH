from src.chatbot.chat import Chat

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/home', methods=['GET'])
def home():
  return render_template('home_tab.html')

@app.route('/chat/<chat_id>', methods=['GET', 'POST'])
def chat(chat_id):
  chat = Chat(chat_id=chat_id)

  if request.method == 'GET':
    pass

  if request.method == 'POST':
    user_input = request.form.get('message')
    print(user_input)
    chat.ask(user_input)
    print(f'post with question: {user_input}')

  return render_template('chat_tab.html', chat=chat)

if __name__ == '__main__':
  chat = None
  app.run(debug=True)
