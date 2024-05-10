import os
from torch import cuda, bfloat16
import transformers
import sys
from torch import cuda


# Verileri ekleme splitleme için gerekli kütüphaneler
from langchain.chains.question_answering import load_qa_chain

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

# Qdrant için gerekli kütüphaneler
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient


# rag yapısı için gerekli kütüphaneler
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

from langchain_community.llms import HuggingFacePipeline
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.embeddings.huggingface import HuggingFaceEmbeddings



# initializing the embeddings
embed_model_id = 'sentence-transformers/all-MiniLM-L6-v2'
device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'
embed_model = HuggingFaceEmbeddings(
    model_name=embed_model_id,
    model_kwargs={'device': device},
    encode_kwargs={'device': device, 'batch_size': 32}
)

# model bağlantısı kuruldu 
#cuda bağlantıları kontrolü

model_id = 'meta-llama/Llama-2-7b-chat-hf'

device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'
print(device)


# set quantization configuration to load large model with less GPU memory
# this requires the `bitsandbytes` library
bnb_config = transformers.BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=bfloat16
)

# begin initializing HF items, need auth token for these
hf_auth = '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'
model_config = transformers.AutoConfig.from_pretrained(
    model_id,
    use_auth_token=hf_auth
)

model = transformers.AutoModelForCausalLM.from_pretrained(
    model_id,
    trust_remote_code=True,
    config=model_config,
    quantization_config=bnb_config,
    device_map='auto',
    use_auth_token=hf_auth
)
model.eval()
print(f"Model loaded on {device}")


#pip install unstructured ve pip install unstructured[pdf] indirdik

# verilerimizi yüklüyoruz

loader = PyPDFLoader("/home/ktu/Masaüstü/algomasters-SON/data/scholar_1-s2.0-S0376042117301483-main.pdf")
pages = loader.load()


# verileri bölüyoruz

def split_docs(documents, chunk_size=500, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    docs = text_splitter.split_documents(documents)
    return docs

docs = split_docs(pages)


# burada verilerimizi veri tabanına gömüp aynı değişkenle arama falan da yapılabilir
# veriler veri tabanında gömülü olduğundan burası tek çalıştırılacak

collection_name = "chatDB"
url = "http://localhost:6333"


vectordb = Qdrant.from_documents(
    documents=docs,
    embedding=embed_model,
    url = url,
    prefer_grpc=False,
    collection_name=collection_name,
) 