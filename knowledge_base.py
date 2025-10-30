import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from config import OPENAI_API_KEY
import os

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def scrape_de5_website():
    base_url = "https://de5.tech/"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    for a in soup.find_all('a', href=True):
        href = str(a['href'])
        if href.startswith('/'):
            href = base_url.rstrip('/') + href
        elif not href.startswith('http'):
            continue
        if href.startswith(base_url) and href not in links:
            links.append(href)
    return links

def build_knowledge_base():
    urls = scrape_de5_website()
    if not urls:
        urls = ["https://de5.tech/"]  # fallback to base URL
    loader = WebBaseLoader(urls)
    documents = loader.load()
    if not documents:
        # Fallback to manual document
        documents = [Document(page_content="DE5 is building an AI and blockchain-powered tokenization platform that democratizes capital access, creates liquidity, and supports a more inclusive financial ecosystem. DE5 aims to provide tokenization solutions for SMEs and investors.", metadata={"source": "fallback"})]
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(docs, embeddings, persist_directory="./chroma_db")
    vectorstore.persist()
    return vectorstore

if __name__ == "__main__":
    vectorstore = build_knowledge_base()
    if vectorstore:
        print("Knowledge base built and persisted.")
    else:
        print("Failed to build knowledge base.")
