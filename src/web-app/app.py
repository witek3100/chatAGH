import os
import time
from flask import (
  Flask,
  render_template,
  request,
  redirect,
  jsonify,
  url_for,
  Response
)

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

@app.route('/get_response/<chat_id>/<question>')
def get_streaming_response(chat_id, question):
  return Response(Chat.get_streaming_response(question, chat_id), content_type='text/event-stream')

@app.route('/chat/<chat_id>')
def chat(chat_id):
  chat = Chat(chat_id=chat_id)
  return render_template('chat_tab.html', chat=chat)

@app.route('/get_asset/<asset>')
def get_icon_url(asset):
  return url_for('static', filename=f"assets/{asset}")

@app.route('/login')
def login():
  return render_template('not_implemented.html')

@app.route('/signup')
def signup():
  return render_template('not_implemented.html')

@app.route('/sources-list')
def sources_list():
  return render_template('sources_list.html')

if __name__ == '__main__':
  app.run(
    port=int(os.environ.get("PORT", 8080)),
    host='0.0.0.0',
    debug=True
  )

