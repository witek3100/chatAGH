# About
Aim of this project is to utilize power of large language models in conjunction with [retrieval-augmented generation](https://research.ibm.com/blog/retrieval-augmented-generation-RAG) 
to create conversational ai chatbot for academic community at AGH univeristy, allowing quick search for reliable information through user friendly web application.

Checkout initial version here:
https://api-test-2rs775oyyq-ez.a.run.app/

# Project status and next steps

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


