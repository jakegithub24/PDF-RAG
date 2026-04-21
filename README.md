# PDF RAG Chatbot - Flask Application

A modern web application that lets you upload PDF documents and chat with them using a local RAG (Retrieval-Augmented Generation) pipeline powered by Ollama.

## Features

- **PDF Upload** – Drag-and-drop support for multiple PDFs  
- **Document Management** – View and delete uploaded documents  
- **Local RAG Pipeline** – Fully local with Ollama (no cloud dependencies)  
- **Conversational AI** – Chat interface powered by Llama 3.2 3B  
- **Fast Embeddings** – Nomic embedding model for efficient semantic search  
- **Source Attribution** – See which documents your answers come from  
- **Modern UI** – Clean, responsive design with real-time chat  

## Prerequisites

- Python 3.8+  
- [Ollama](https://ollama.ai/) installed and running locally  
- At least 8GB RAM (16GB+ recommended for better performance)  

## Setup

### 1. Install Ollama
Download and install from [ollama.ai](https://ollama.ai/).

### 2. Pull Required Models
```bash
ollama pull llama3.2:3b
ollama pull nomic-embed-text:latest
```

### 3. Start Ollama
```bash
ollama serve
```
Ollama will run on `http://localhost:11434`.

### 4. Set Up Flask App
```bash
cd FlaskApp

# Create virtual environment
python -m venv myvenv
source myvenv/bin/activate        # On Windows: myvenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 5. Configure `.env`
The `.env` file is pre‑configured with optimal settings:
```
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-this
OLLAMA_MODEL=llama3.2:3b
OLLAMA_EMBEDDING_MODEL=nomic-embed-text:latest
OLLAMA_BASE_URL=http://localhost:11434
MAX_UPLOAD_SIZE=52428800
```

### 6. Run the Application
```bash
python app.py
```
The app will be available at `http://localhost:5000`.

## Usage

1. **Upload Documents** – Go to the upload page and drag‑and‑drop PDF files.  
2. **Start Chatting** – Click “Start Chatting” to initialize the RAG pipeline.  
3. **Ask Questions** – Chat with your documents in the chat interface.  
4. **View Sources** – See which PDF documents the answers come from.  
5. **Delete Files** – Remove documents from the upload page.  

## How It Works

### Architecture
```
PDF Upload → PDF Text Extraction (PyPDF2) → Chunking (300 chars, 50 overlap)
       → Embeddings (Ollama – nomic-embed-text) → Vector Store (FAISS)
       → User Query → Similarity Search (k=10) → LLM Generation (Ollama – Llama 3.2 3B)
       → Response + Sources
```

### Technologies
- **Framework**: Flask  
- **Vector Store**: FAISS  
- **Embeddings**: Ollama (`nomic-embed-text:latest`)  
- **LLM**: Ollama (`llama3.2:3b`)  
- **PDF Processing**: PyPDF2  
- **Text Splitting**: LangChain `RecursiveCharacterTextSplitter`  
- **Frontend**: HTML5 + CSS3 + Vanilla JS  
- **Local Processing**: All models run locally on port 11434  

## Troubleshooting

### Slow embeddings or LLM responses
- First run downloads the models (~8GB combined). Subsequent runs are faster.  
- Llama 3.2 3B is CPU‑optimised, but GPU acceleration helps. For better CPU performance, consider a smaller model (e.g., `ollama pull mistral`).  

### Out of memory
- Reduce `chunk_size` in `app.py` (function `build_rag_pipeline()`).  
- Use a smaller Ollama model.  
- Ensure at least 8GB free RAM; close other memory‑intensive applications.  

### Models not found
- Verify models are downloaded: `ollama list`  
- Pull missing models:  
  ```bash
  ollama pull llama3.2:3b
  ollama pull nomic-embed-text:latest
  ```
- Check that Ollama is running on port 11434.  

### Chatbot says “I don’t have this information”
- Verify the PDF contains the information you’re asking about.  
- Try rephrasing your question – semantic search looks for meaning, not exact phrases.  
- Ensure PDFs are text‑based (not scanned images).  
- Check the console for debug logs showing retrieved documents.  

### General checks
- Verify port 11434 is accessible (check firewall settings).  
- Restart Ollama occasionally to free memory.  
- Smaller PDFs are processed faster.  
- PDFs are re‑processed on each chat session start (no caching).  

## Configuration Parameters

Fine‑tune the RAG pipeline by editing `app.py`:

```python
# Text splitting (line ~85)
chunk_size=300        # Smaller = more specific chunks
chunk_overlap=50      # Overlap for context continuity

# Document retrieval (line ~210)
k=10                  # Number of documents to retrieve (higher = more context)
```

## Project Structure

```
FlaskApp/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── uploads/               # Uploaded PDF storage
├── templates/
│   ├── base.html          # Base template
│   ├── upload.html        # Upload page
│   └── chat.html          # Chat interface
└── static/
    └── style.css          # Styling
```

## API Endpoints

| Endpoint          | Method | Description                          |
|-------------------|--------|--------------------------------------|
| `/`               | GET    | Upload page                          |
| `/upload`         | POST   | Handle PDF uploads                   |
| `/delete/<id>`    | POST   | Delete an uploaded PDF               |
| `/build_rag`      | POST   | Build RAG pipeline and start chat    |
| `/chat`           | POST   | Send a message and get response      |
| `/chat_page`      | GET    | Render chat interface                |

## Limitations

- No persistent vector store – embeddings are rebuilt each session.  
- No database – uploaded files are stored only in the `uploads/` folder.  
- Max file size: 50MB per PDF.  
- Single‑user application (not optimised for concurrent use).  
- Works best with English text‑based PDFs (scanned documents/OCR are not supported).  

## Future Enhancements

- Persistent vector store (save FAISS index to disk)  
- Multi‑language support  
- Web‑based RAG parameter tuning  
- Export chat history  
- Multi‑user support with sessions  
- Stream LLM responses for faster feedback  

## License

GPL v3.0