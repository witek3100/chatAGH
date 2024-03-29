1. [About](#About)
2. [Tech stack](#Tech-stack)
3. [Project structure](#Project-structure)
4. [Project status and next steps](#Project-status-and-next-steps)
5. [Knowledge sources](#Knowledge-sources)
6. [Run locally instruction](#Run-locally-instruction)
7. [Credits](#Credits)

# About

CharAGH is conversational ai chatbot based on openAI's GPT4 with connection to knowledge about AGH University (statutes, websites etc.) using [retrieval-augmented generation](https://research.ibm.com/blog/retrieval-augmented-generation-RAG). Aim of the project is to create useful tool for academic society at AGH, allowing for quick retrieval of reliable information.

### Check latest version [*here*](https://chat-agh-2rs775oyyq-ez.a.run.app/home)

# Tech stack
### Chatbot
- The project's backbone is built upon the LangChain LLM framework, seamlessly integrating the OpenAI GPT4 model and utilizes Pinecone vector database for knowledge source embeddings storage, enabling RAG (Retriever-Augmented Generation). A migration to MongoDB Atlas is planned to consolidate data storage and enhance cost-effectiveness.
 
### Web App
- Serving as the user interface for chatbot, web application is created using Flask, JQuery and stores data in Mongo database. This combination ensures an intuitive experience for users interacting with the chatbot as weel as ease of development.

### Deployment
- Project is deployed within a Docker container on Google Cloud Run, offering scalability and reliability. Deployment procedures are automated using terraform and github actions.

# Project structure
<pre>
   ├── src
   |     ├── infra      ## Terraform files, deployment automation
   |     |      ├── main.tf
   |     |      └── variables.tf
   |     |
   |     ├── chatbot     ## Chatbot implementation using langchain
   |     |      ├── prompts
   |     |      ├── skills
   |     |      ├── chat.py
   |     |      └── message.py
   |     |
   |     ├── configs          ## Project configuration files
   |     |      ├── config.json
   |     |      └── requirements.txt
   |     |
   |     ├── sources             ## Knowledge sources generator (web scraper, langchain documents loader, and pinecone index initialization)
   |     |      ├── sources.json
   |     |      ├── sources_loader.py
   |     |      └── domain_scraper.py
   |     |
   |     ├── tests      ## tests - TODO
   |     |
   |     ├── web-app                 ## Web application - user interface to chatbot
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
   |     |
   |     └── utils.py      ## Utilities (logger, mongo client etc.)
   |
   └── README.md                 
</pre>

# Project status and next steps
ChatAGH is currently on early stage of development, therefore bugs are expected and amount of functionalities is limited, now only to creating new, one time chats. Next steps involves:
 - Expanding web app (among others by adding accouts funcionality, to allow users store and return to their chats),
 - Imporoving chatting by broading knowledge sources and enhancing chatbot itself (prompts, model params etc.).
 - Fixing bugs and lot of smaller changes.

# Knowledge sources
Current approach to generating knowledge sources is quite straightforward and requires improvement (expanding and filtering sources). In short, it involves scraping web pages from several domains related to agh and then loading them to pinecone using langchain. domain list:

List of domeins:
- https://www.agh.edu.pl
- https://rekrutacja.agh.edu.pl
- https://www.eaiib.agh.edu.pl
- https://www.sjo.agh.edu.pl
- https://www.swfis.agh.edu.pl
- https://sylabusy.agh.edu.pl
- https://sylabusy.agh.edu.pl/pl/
- https://skn.agh.edu.pl
- https://dss.agh.edu.pl
- https://akademik.agh.edu.pl
- https://www.miasteczko.agh.edu.pl

# Run locally instruction 

# Credits
https://www.fpgmaas.com/blog/deploying-a-flask-api-to-cloudrun

