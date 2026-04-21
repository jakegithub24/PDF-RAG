import os
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
import shutil
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your-secret-key-here")

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Global variables for RAG pipeline
vector_store = None
llm = None
embeddings = None


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file."""
    try:
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            for page_num, page in enumerate(pdf_reader.pages):
                text += f"\n--- Page {page_num + 1} ---\n"
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return ""


def build_rag_pipeline():
    """Build RAG pipeline from uploaded PDFs."""
    global vector_store, llm, embeddings
    
    try:
        # Get all PDFs from uploads folder
        pdf_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.pdf')]
        
        if not pdf_files:
            return False, "No PDF files found"
        
        print(f"📂 Found {len(pdf_files)} PDF file(s): {pdf_files}")
        
        documents = []
        
        # Extract text from all PDFs
        for pdf_file in pdf_files:
            pdf_path = os.path.join(UPLOAD_FOLDER, pdf_file)
            text = extract_text_from_pdf(pdf_path)
            print(f"📖 {pdf_file}: Extracted {len(text)} characters")
            if text:
                doc = Document(
                    page_content=text,
                    metadata={"source": pdf_file}
                )
                documents.append(doc)
        
        if not documents:
            return False, "No text extracted from PDFs"
        
        print(f"📚 Total documents created: {len(documents)}")
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,  # Further reduced to capture specific info
            chunk_overlap=50
        )
        chunked_docs = text_splitter.split_documents(documents)
        print(f"✂️ Split into {len(chunked_docs)} chunks")
        
        # Create embeddings using Ollama (nomic-embed-text)
        print("🧠 Loading embeddings model...")
        embeddings = OllamaEmbeddings(
            model=os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text:latest"),
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        )
        print("✅ Embeddings model loaded")
        
        # Create vector store
        print("📦 Building vector store...")
        vector_store = FAISS.from_documents(chunked_docs, embedding=embeddings)
        print(f"✅ Vector store created with {len(chunked_docs)} chunks")
        
        # Initialize LLM
        print("🤖 Initializing LLM...")
        llm = OllamaLLM(
            model=os.getenv("OLLAMA_MODEL", "llama3.2:3b"),
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        )
        print("✅ LLM initialized")
        
        return True, f"RAG pipeline ready! Processed {len(pdf_files)} PDF(s) into {len(chunked_docs)} chunks."
    
    except Exception as e:
        print(f"❌ Error building RAG pipeline: {e}")
        import traceback
        traceback.print_exc()
        return False, f"Error: {str(e)}"


@app.route('/')
def index():
    """Home page - document upload."""
    try:
        pdf_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.pdf')]
    except:
        pdf_files = []
    
    return render_template('upload.html', uploaded_files=pdf_files)


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle PDF file upload."""
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No file part"})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"success": False, "message": "No selected file"})
    
    if not allowed_file(file.filename):
        return jsonify({"success": False, "message": "Only PDF files are allowed"})
    
    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({"success": True, "message": f"File '{filename}' uploaded successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Error uploading file: {str(e)}"})


@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    """Delete uploaded PDF file."""
    try:
        filename = secure_filename(filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({"success": True, "message": f"File '{filename}' deleted"})
        else:
            return jsonify({"success": False, "message": "File not found"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Error deleting file: {str(e)}"})


@app.route('/start-chat', methods=['POST'])
def start_chat():
    """Initialize RAG pipeline and start chat."""
    global vector_store
    
    success, message = build_rag_pipeline()
    
    if success:
        session['rag_ready'] = True
        return jsonify({"success": True, "message": message})
    else:
        return jsonify({"success": False, "message": message})


@app.route('/chat')
def chat():
    """Chat page."""
    if not session.get('rag_ready'):
        return redirect(url_for('index'))
    
    try:
        pdf_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.pdf')]
    except:
        pdf_files = []
    
    return render_template('chat.html', uploaded_files=pdf_files)


@app.route('/query', methods=['POST'])
def query():
    """Handle RAG query."""
    global vector_store, llm
    
    if not vector_store or not llm:
        return jsonify({"success": False, "message": "RAG pipeline not initialized"})
    
    try:
        data = request.json
        user_query = data.get('query', '')
        
        if not user_query:
            return jsonify({"success": False, "message": "Empty query"})
        
        # Retrieve relevant documents
        retrieved_docs = vector_store.similarity_search(user_query, k=10)  # Increased to 10 for better coverage
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])
        
        # Debug logging
        print(f"🔍 Query: {user_query}")
        print(f"📄 Retrieved {len(retrieved_docs)} documents")
        print(f"📝 Context length: {len(context)} characters")
        for i, doc in enumerate(retrieved_docs, 1):
            print(f"  Doc {i}: {doc.page_content[:100].replace(chr(10), ' ')}...")
        print(f"⚠️ Context is {'EMPTY' if not context.strip() else 'OK'}")
        
        # Create prompt template - Ask LLM to find any mention of duration
        template = """You are a helpful assistant answering questions based on the provided documents.

<context>
{context}
</context>

Question: {question}

Please search through the context carefully. If you see any specific numbers, dates, or duration information, include it in your answer. Answer based on the provided context."""
        prompt = ChatPromptTemplate.from_template(template)
        output_parser = StrOutputParser()
        chain = prompt | llm | output_parser
        
        # Generate response
        print(f"\n📨 Sending to LLM...")
        print(f"📋 Prompt template created")
        response = chain.invoke({
            "context": context,
            "question": user_query
        })
        print(f"🤖 LLM Response: {response[:200]}...")
        print(f"✅ Response length: {len(response)} characters\n")
        
        return jsonify({
            "success": True,
            "response": response,
            "sources": [doc.metadata.get('source', 'Unknown') for doc in retrieved_docs]
        })
    
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"})


@app.route('/clear-session', methods=['POST'])
def clear_session():
    """Clear session and reset RAG pipeline."""
    global vector_store, llm, embeddings
    
    vector_store = None
    llm = None
    embeddings = None
    session.clear()
    
    return jsonify({"success": True, "message": "Session cleared"})


@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"success": False, "message": "File too large (max 50MB)"}), 413


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
