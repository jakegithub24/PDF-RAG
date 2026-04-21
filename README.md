# PDF RAG Chatbot - Flask Application

A modern web application that lets you upload PDF documents and chat with them using a local RAG (Retrieval-Augmented Generation) pipeline.

## Features

✅ **PDF Upload** - Drag-and-drop support for multiple PDFs  
✅ **Document Management** - View and delete uploaded documents  
✅ **Local RAG Pipeline** - Fully local with Ollama (no cloud dependencies)  
✅ **Conversational AI** - Chat interface powered by Llama 3.2 3B  
✅ **Fast Embeddings** - Nomic embedding model for efficient semantic search  
✅ **Source Attribution** - See which documents your answers come from  
✅ **Modern UI** - Clean, responsive design with real-time chat  

## Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/) installed and running locally
- At least 4GB RAM (8GB+ recommended)

## Setup

### 1. Install Ollama
Download and install from [ollama.ai](https://ollama.ai)

### 2. Pull Required Models
```bash
# Pull the LLM model
ollama pull llama3.2:3b

# Pull the embedding model
ollama pull nomic-embed-text:latest
```

### 3. Start Ollama
```bash
ollama serve
```
Ollama will run on `http://localhost:11434`

### 4. Set Up Flask App

```bash
cd FlaskApp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 5. Configure .env (Optional)
Edit `.env` to customize settings:
```
FLASK_ENV=development
SECRET_KEY=yollama3.2:3b
OLLAMA_EMBEDDING_MODEL=nomic-embed-text:latest
OLLAMA_BASE_URL=http://localhost:11434et-key-change-this
OLLAMA_MODEL=mistral
MAX_UPLOAD_SIZE=52428800
```

### 6. Run the Application
```bash
python app.py
```

The app will be available at: `http://localhost:5000`

## Usage

1. **Upload Documents** - Go to the upload page and drag-drop PDF files
2. **Start Chatting** - Click "Start Chatting" to initialize the RAG pipeline
3. **Ask Questions** - Chat with your documents in the chat interface
4. **Delete Files** - Remove documents from the upload page

## How It Works

### Architecture
```
PDF Upload
    ↓
PDF Text Extraction (PyPDF2)
    ↓
Text SplittiOllama - nomic-embed-text)
    ↓
Vector Store (FAISS)
    ↓
User Query
    ↓
Similarity Search (k=3 documents)
    ↓
LLM Generation (Ollama - Llama 3.2 3B)
    ↓
LLM Generation (Ollama - Mistral)
    ↓
Response + Sources
```

### Technologies
- **Framework**: FOllama (nomic-embed-text:latest)
- **LLM**: Ollama (llama3.2:3b)
- **PDF Processing**: PyPDF2
- **Frontend**: HTML5 + CSS3 + Vanilla JS
- **Local Processing**: All models run locally on port 11434
- **PDF Processing**: PyPDF2
- **Frontend**: HTML5 + CSS3 + Vanilla JS

## Troubleshooting

### "Connection refused" error
- Make sure Ollama is running: `ollama serve`
- Check if port 11434 is accessible
 or LLM responses
- First run downloads the models (~8GB combined)
- Subsequent runs are faster
- Llama 3.2 3B is optimized for CPU, but GPU acceleration is beneficial
- For faster performance, try a smaller embedding model

### Out of memory
- Reduce `chunk_size` in `app.py` (line 85)
- Use a smaller Ollama model (e.g., `ollama pull mistral:7b`)
- Ensure you have at least 8GB RAM available

### Models not found
- Verify models are downloaded: `ollama list`
- Pull missing models: 
  ```bash
  ollama pull llama3.2:3b
  ollama pull nomic-embed-text:latest
  ```
- Check Ollama service is running on port 11434t`
- Try a different model: `ollama pull llama2`

## Project Structure

```
FlaskApp/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── uploads/              # Uploaded PDF storage
├── templates/
│   ├── base.html         # Base template
│   ├── upload.html       # Upload page
│   └── chat.html         # Chat interface
└── static/
    └── style.css         # Styling
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Upload page |
| `/upload` | POST | Upload PDF file |
| `/delete/<filename>` | POST | Delete PDF file |
| `/start-chat` | POST | Initialize RAG pipeline |
| `/chat` | GET | Chat page |
| `/query` | POST | Send chat query |
| `/clear-session` | POST | Clear session & reset |

## Performance Tips

- Use smaller PDFs for faster processing
- Pre-process large PDFs into smaller chunks
- Run on systems with 8GB+ RAM
- Use GPU for faster embeddings (requires GPU-enabled setup)

## Limitations

- PDFs are re-processed on each chat session start
- No persistent database (uploads deleted when folder cleared)
- Max file size: 50MB per PDF
- Runs locally (not suitable for many concurrent users)

## License

Free to use for personal/educational purposes.
