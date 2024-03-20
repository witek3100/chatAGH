import os

from flask import Flask, render_template, request, redirect, jsonify, url_for

from src.chatbot.chat import Chat

app = Flask(__name__, static_folder='static/')

@app.route('/')
def redirect_home():
  return redirect('/home')

@app.route('/home', methods=['GET'])
def home():
  return render_template('home_tab.html')

@app.route('/new_chat')
def create_new_chat():
  chat = Chat()
  return redirect(f'/chat/{chat.id}')

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
      'answer': answer.content_html,
      'source': answer.source
    })

  return render_template('chat_tab.html', chat=chat)

@app.route('/get_asset/<asset>')
def get_icon_url(asset):
  return url_for('static', filename=f"assets/{asset}")

@app.route('/login')
def login():
  pass

if __name__ == '__main__':
  app.run(
    port=int(os.environ.get("PORT", 8080)),
    host='0.0.0.0',
    debug=True
  )

