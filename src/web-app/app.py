from src.chatbot.chat import Chat

from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)


@app.route('/')
def redirect_home():
  return redirect('/home')

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
    answer = chat.ask(user_input)

    return jsonify({
      'query': user_input,
      'answer': answer.content
    })

  return render_template('chat_tab.html', chat=chat)

if __name__ == '__main__':
  app.run(debug=True)
