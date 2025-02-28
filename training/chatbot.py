from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
persist_directory = 'db'
pdf_directory = 'rag_data'  # Directory containing medical PDFs
chunk_size = 1000
chunk_overlap = 200

# Initialize embeddings
hf_embeddings = HuggingFaceInferenceAPIEmbeddings(
    api_key=os.getenv('HUGGINGFACE_API_KEY'),
    model_name="sentence-transformers/all-MiniLM-l6-v2"
)

# Initialize vector database
def initialize_vector_db():
    if not os.path.exists(persist_directory) or not os.listdir(persist_directory):
        print("Creating new vector database...")
        loader = PyPDFDirectoryLoader(pdf_directory)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        text_chunks = text_splitter.split_documents(documents)
        
        vectordb = Chroma.from_documents(
            documents=text_chunks,
            embedding=hf_embeddings,
            persist_directory=persist_directory
        )
        vectordb.persist()
    else:
        print("Loading existing vector database...")
        vectordb = Chroma(
            persist_directory=persist_directory,
            embedding_function=hf_embeddings
        )
    return vectordb

vectordb = initialize_vector_db()
retriever = vectordb.as_retriever(search_kwargs={"k": 3})

# System prompt template
system_prompt = """You are a crop disease medical expert AI that provides detailed insights and recommendations for diseases. 
When given a disease name, provide:
1. Disease overview (causes, symptoms, risk factors)
2. Prevention strategies
3. Treatment options (medical and alternative)
4. Lifestyle recommendations
5. Monitoring and follow-up advice
6. Emergency warning signs

Base your response strictly on the provided context. If information is unavailable, state that clearly.
Structure your response with clear headings for each section and maintain a professional yet compassionate tone.

Context: {context}
Question: {question}"""

PROMPT = PromptTemplate(
    template=system_prompt, input_variables=["context", "question"]
)

# Initialize LLM with medical focus
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro-latest",
    api_key=os.getenv('GEMINI_API_KEY'),
    temperature=0.3,
    max_tokens=1024,
    safety_settings={
        "HARM_CATEGORY_DANGEROUS": "BLOCK_NONE",
        "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
        "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE"
    }
)

# Create retrieval chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs={"prompt": PROMPT},
    return_source_documents=True
)

# Enhanced response processor
def process_llm_response(llm_response):
    response = llm_response['result']
    sources = set()
    
    print("\n=== Disease Insights ===")
    print(response)
    
    print("\n=== Sources ===")
    for doc in llm_response["source_documents"]:
        source = os.path.basename(doc.metadata['source'])
        sources.add(source)
    
    if sources:
        print("Information verified from:")
        for src in sources:
            print(f"- {src}")
    else:
        print("No specific sources referenced")

# Example usage
def get_disease_insights(disease_name):
    query = f"Comprehensive analysis and recommendations for {disease_name}"
    llm_response = qa_chain(query)
    process_llm_response(llm_response)

# Run with your model's prediction
your_model_prediction = "blight disease"  # Replace with model output
get_disease_insights(your_model_prediction)