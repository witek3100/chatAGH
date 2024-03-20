# Overview
This project aims to build a conversational AI chatbot to provide information and support to students and staff of AGH University of Science and Technology. By harnessing power of Large Language Models and RAG technique, we can integrate multiple knowledge sources, like AGH websites and publicly available documents (statutes, resolutions etc.) to deliver precise and contextually appropriate responses through a user-friendly web application.

v0.1-beta - https://api-test-2rs775oyyq-ez.a.run.app/chat/65fac4aa7eda200461b4c876

# Tech stack
- Python as a main programming language
- Langchain for processing sources and implementing conversational chains
- Pinecone vector database to perform similarity search on knowledge sources and users queries
- MongoDB to store user's data, chats, logs etc.
- Web app created using Flask, Jquery

# Project structure
<pre>
   ├── src
   |     ├── chatbot
   |     |      ├── prompts
   |     |      ├── skills
   |     |      ├── chat.py
   |     |      └── message.py
   |     ├── configs
   |     |      ├── config.json
   |     |      └── requirements.txt
   |     ├── sources
   |     |      ├── sources.json
   |     |      ├── sources_loader.py
   |     |      ├── urls_finder.py
   |     |      └── vector_db.py
   |     ├── tests
   |     ├── web-app
   |     |      ├── static
   |     |      |     ├── assets
   |     |      |     ├── css
   |     |      |     |    └── chat_tab.css
   |     |      |     └── js
   |     |      |          └── chat_tab.js
   |     |      ├── templates
   |     |      |     ├── chat_tab.html
   |     |      |     └── home_tab.html
   |     |      └── app.py
   |     └── utils.py
   |
   └── README.md                 
</pre>

# Knowledge sources


