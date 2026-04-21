# PDF RAG Chatbot - Flask Application

A modern web application that lets you upload PDF documents and chat with them using a local RAG (Retrieval-Augmented Generation) pipeline powered by Ollama.

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
- At least 8GB RAM (16GB+ recommended for better performance)

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
python -m venv myvenv
source myvenv/bin/activate  # On Windows: myvenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 5. Configure .env
The `.env` file is pre-configured with optimal settings:
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

The app will be available at: `http://localhost:5000`

## Usage

1. **Upload Documents** - Go to the upload page and drag-drop PDF files
2. **Start Chatting** - Click "Start Chatting" to initialize the RAG pipeline
3. **Ask Questions** - Chat with your documents in the chat interface
4. **View Sources** - See which PDF documents the answers come from
5. **Delete Files** - Remove documents from the upload page

## How It Works

### Architecture
```
PDF Upload
    ↓
PDF Text Extraction (PyPDF2)
    ↓ng (300 char chunks, 50 overlap)
    ↓
Embeddings (Ollama - nomic-embed-text)
    ↓
Vector Store (FAISS)
    ↓
User Query
    ↓
Similarity Search (k=10 documents)
    ↓
LLM Generation (Ollama - Llama 3.2 3B)
    ↓
Response + Sources
```

### Technologies
- **Framework**: Flask
- **Vector Store**: FAISS
- **Embeddings**: Ollama (nomic-embed-text:latest)
- **LLM**: Ollama (llama3.2:3b)
- **PDF Processing**: PyPDF2
- **Text Splitting**: LangChain RecursiveCharacterTextSplitter
- **Frontend**: HTML5 + CSS3 + Vanilla JS
- **Local Processing**: All models run locally on port 11434
- **Frontend**: HTML5 + CSS3 + Vanilla JS

## Troubleshooting

##Verify port 11434 is accessible
- Check firewall settings

### Slow embeddings or LLM responses
- First run downloads the models (~8GB combined)
- Subsequent runs are faster
- Llama 3.2 3B is optimized for CPU, but GPU acceleration is beneficial
- For faster performance on CPU, consider a smaller model

### Out of memory
- Reduce `chunk_size` in `app.py` function `build_rag_pipeline()`
- Use a smaller Ollama model (e.g., `ollama pull mistral`)
- Ensure you have at least 8GB RAM available
- Close other applications consuming memory

### Models not found
- Verify models are downloaded: `ollama list`
- Pull missing models: 
  ```bash
  ollama pull llama3.2:3b
  ollama pull nomic-embed-text:latest
  ```
- Check Ollama service is running on port 11434

### Chatbot says "I don't have this information"
- Verify the PDF contains the information you're asking about
- Try asking differently - semantic search looks for meaning, not exact phrases
- Ensure PDFs are text-based (not scanned images)
- Check console for debug logs showing retrieved documents
- Check Ollama service is running on port 11434t`
- Tr.gitignore            # Git ignore rules
├── README.md             # This file
├── y a different model: `ollama pull llama2`

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
|-----text-based PDFs (OCR scanned documents work worse)
- Smaller PDFs are processed faster
- Run on systems with 8GB+ RAM for optimal performance
- GPU support significantly speeds up embeddings (requires GPU-enabled Ollama)
- Restart Ollama occasionally to free up memory

## Configuration Parameters

You can fine-tune the RAG pipeline by editing `app.py`:

```python
# Text splitting (line ~85)
chunk_size=300,        # Smaller = more specific chunks
chunk_overlap=50       # Overlap for context continuity

# Document retrieval (line ~210)
k=10                   # Number of documents to retrieve (higher = more context)
```

## Limitations

- PDFs are re-processed on each chat session start (no caching)
- No persistent database (embeddings not saved between sessions)
- Max file size: 50MB per PDF
- Single-user application (not optimized for concurrent usage)
- Works best with English text

## Future Enhancements

- Persistent vector store (save FAISS index to disk)
- Multi-language support
- Web-based RAG parameter tuning
- Export chat history
- Multi-user support with sessions
- Stream LLM responses for faster feedback

## License

Free to use for personal and educational purposes.

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review console output for debug logs (marked with emojis 🔍📄📝🤖)
3. Verify Ollama is running and models are downloaded
4. Ensure PDFs are valid text-based documentsenabled setup)

## Limitations

- PDFs are re-processed on each chat session start
- No persistent database (uploads deleted when folder cleared)
- Max file size: 50MB per PDF
- Runs locally (not suitable for many concurrent users)

## License

Free to use for personal/educational purposes.
