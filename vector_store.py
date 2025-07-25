from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
import pandas as pd
from config import Config
from logger import setup_logger

logger = setup_logger("VectorStoreService")

def create_vector_store():
    try:
        df = pd.read_csv(Config.CSV_DATA_PATH)
        docs = [Document(page_content=row['answer'], metadata={"question": row['question']}) for _, row in df.iterrows()]

        logger.info(f"Loaded {len(docs)} documents from {Config.CSV_DATA_PATH}")
       
        # Use local HuggingFace model for embeddings
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )


        # FAISS is fast similarity Engine (Facebook AI Similarity Search)
        ## Creating vector embeddings from Hugging face sentence transformers and storing and querying the vector empbeddings
        vector_store = FAISS.from_documents(docs, embeddings)

        logger.info("Vector store created with Hugging Face embeddings.")
        return vector_store

    except Exception as e:
        logger.error(f"Error creating vector store: {e}")
        raise
