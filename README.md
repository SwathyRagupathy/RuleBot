# 🤖 RuleBot  

**Demonstration on RIT Auxiliary Service Student Employee Guide**  

Rulebot is an AI-powered chatbot, using local documents designed to help users interact naturally with organizational documents, policies, or guides. This project showcases how to upload or link documents (PDF, DOCX) and then ask questions answered *solely* based on the provided content.


## Tech Stack

- ⚡️ Streamlit — Interactive chatbot UI
- 🧠 LangChain — Prompt & context management
- 🔍 FAISS — Fast vector similarity search
- 🤖 GPT4All — Local LLM inference (LLaMA 3 8B)
- 💬 HuggingFace Transformers — Embedding generation

## How It Works

1. **Input**: User uploads a document or pastes a URL  
2. **Processing**: Text is extracted and split into chunks  
3. **Vectorization**: Chunks are embedded and stored in a FAISS vector index  
4. **Query**: User asks questions; system retrieves relevant chunks by similarity  
5. **Answering**: GPT4All generates answers strictly based on retrieved context  
6. **Interaction**: User chats in an intuitive Streamlit interface  


## Project Structure

``` base
rit-dining-chatbot/
├── app.py             # Streamlit chatbot app
├── build_index.py     # Script to create FAISS vector index from PDFs
├── chat_logs/         # Logs of completed chat sessions
├── requirements.txt   # All Python dependencies
└── README.md          # This file
```

This chatbot uses local policy documents, FAISS for vector search, and a locally hosted GPT4All model to provide accurate, confidential responses based on your organization’s internal rules. 

# No internet or API keys - No hallucination -> Secured Data🔒
#### It can be easily adapted to work with documents from *any* organization or domain.




