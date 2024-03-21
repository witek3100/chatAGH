# About
Aim of this project is to utilize power of large language models in conjunction with [retrieval-augmented generation](https://research.ibm.com/blog/retrieval-augmented-generation-RAG) 
to create conversational ai chatbot for academic community at AGH univeristy, allowing quick search for reliable information through user friendly web application.

### Checkout latest version [*here*](https://api-test-2rs775oyyq-ez.a.run.app/)

# Project status and next steps
CharAGH is currently on very early stage of development, therefore bugs are expected and amount of functionalities is limited, now only to creating new, one time chats. Next steps involves expanding web app (among others by adding accouts funcionality, to allow users store and return to their chats), imporoving chatting by enhancing knowledge sources as well as chatbot itself (prompts, model params etc.) and a lot of other, smaller changes and fixes.

# Tech stack
### Chatbot
- The backbone of our project relies on the langchain llm's framework, integrating OpenAI GPT4 model. Currently, knowledge sources embeddings are stored in the Pinecone vector database, allowing for, mentioned earlier, RAG technique. Migration to Mongo atlas is planned in order to store embeddings and web-app data in same place, minimizing costs.

### Web App
- Serving as the user interface for chatbot, web application is created using Flask and jQuery. This combination ensures a smooth and intuitive experience for users interacting with the chatbot as weel as ease of development.

### Deployment
- Project is deployed within a Docker container on Google Cloud Run, offering scalability and reliability. Leveraging Terraform, deployment procedures were automated, simplifying the management of infrastructure. Looking ahead, further autmation is planned, by implementing a CI/CD pipeline through GitHub Actions.

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


