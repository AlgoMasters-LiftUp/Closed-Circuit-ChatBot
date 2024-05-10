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


class RAG():

    def __init__(self):
        print("*******************************RAG CONFIG START*******************************")
        self.embed_model_id = embed_model_id = 'sentence-transformers/all-MiniLM-L6-v2'
        device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'
        print("device: ", device)
        self.initializeEmbeddingModel(device)        

        self.model_id = 'meta-llama/Llama-2-7b-chat-hf'
        self.hf_auth = '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'
        self.initializeLLM()

        self.data_collection_name = "chatDB"
        self.db_url = "http://localhost:6333"
        self.initializeDBclient()
        self.initializesearchDB()

        self.LLMpipeline()
        self.configSystemPrompt()
        self.RAGpipeline()

        self.chat_history = []
        
    
    def initializeEmbeddingModel(self, device):
        print("******************************* initializeEmbeddingModel *******************************")
        
        # initializing the embeddings
        self.embed_model = HuggingFaceEmbeddings(
            model_name=self.embed_model_id,
            model_kwargs={'device': device},
            encode_kwargs={'device': device, 'batch_size': 32}
        )
        print("******************************* embed model started *******************************")
    
    def initializeLLM(self):
        print("******************************* initializeLLM *******************************")
        # set quantization configuration to load large model with less GPU memory
        # this requires the `bitsandbytes` library
        bnb_config = transformers.BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type='nf4',
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=bfloat16
        )

        # begin initializing HF items, need auth token for these
        model_config = transformers.AutoConfig.from_pretrained(
            self.model_id,
            use_auth_token=self.hf_auth
        )

        self.LLMmodel = transformers.AutoModelForCausalLM.from_pretrained(
            self.model_id,
            trust_remote_code=True,
            config=model_config,
            quantization_config=bnb_config,
            device_map='auto',
            use_auth_token=self.hf_auth
        )
        self.LLMmodel.eval()
        print("******************************* llm started *******************************")

    # veri tabanı erişimi için client oluşturuluyor
    def initializeDBclient(self):
        print("******************************* initializeDBclient *******************************")
        
        self.DBclient = QdrantClient(
                        url = self.db_url,
                        prefer_grpc=False
                        )
        print("******************************* dbclient started *******************************")
        
    #  veri tabanında arama yapmak için db nesnei oluşturuldu
    def initializesearchDB(self):
        print("******************************* initializesearchDB *******************************")
        
        self.searchDB = Qdrant(
                    client = self.DBclient,
                    embeddings = self.embed_model,
                    collection_name = self.data_collection_name 
                )
        print("******************************* searchdb started *******************************")
        
    def LLMpipeline(self):
        print("******************************* LLMpipeline *******************************")
        
        # llm nesnesi için gerekli bir değişken 
        tokenizer = transformers.AutoTokenizer.from_pretrained(
                    self.model_id,
                    use_auth_token=self.hf_auth
                )
        # sadece llm için bir pipeline
        pipeline = transformers.pipeline(
                    model=self.LLMmodel, tokenizer=tokenizer,
                    return_full_text=True,  # langchain expects the full text
                    task='text-generation',
                    # we pass model parameters here too
                    temperature=0.0,  # 'randomness' of outputs, 0.0 is the min and 1.0 the max
                    max_new_tokens=512,  # mex number of tokens to generate in the output
                    repetition_penalty=1.1,
                    do_sample=False
                    # without this output begins repeating
                )
        self.llm = HuggingFacePipeline(pipeline=pipeline)
        print("******************************* llm pipeline is done *******************************")
        
    def configSystemPrompt(self):
        print("******************************* configSystemPrompt *******************************")
        
        # sohbet geçmişi için alt prompt ve genel system promptu tanımlıyoruz

        contextualize_q_system_prompt = """Given a chat history and the latest user question \
        which might reference context in the chat history, formulate a standalone question \
        which can be understood without the chat history. Do NOT answer the question, \
        just reformulate it if needed and otherwise return it as is."""
        self.contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        qa_system_prompt = """You are an assistant for question-answering tasks. \
        Use the following pieces of retrieved context to answer the question. \
        If you don't know the answer, just say that you don't know. \
        Use three sentences maximum and keep the answer concise.\

        {context}"""

        # prompt = PromptTemplate.from_template(template)
        self.qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", qa_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        print("******************************* system prompt is done *******************************")
        
    def RAGpipeline(self):
        print("******************************* RAGpipeline *******************************")
        

        retriever = self.searchDB.as_retriever(search_kwargs={"k":6})
        history_aware_retriever = create_history_aware_retriever(
            self.llm, retriever, self.contextualize_q_prompt
        )

        # alt zincir
        question_answer_chain = create_stuff_documents_chain(self.llm, self.qa_prompt)

        # ana zincir
        self.rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
        print("******************************* rag pipeline is done *******************************")

    def ragQA(self, question):
        ai_msg = self.rag_chain.invoke({"input": question, "chat_history": self.chat_history})
        
        self.chat_history.extend([HumanMessage(content=question), ai_msg["answer"]])

        return ai_msg

    def updateChatHistory(self, chat:list):
        pass
