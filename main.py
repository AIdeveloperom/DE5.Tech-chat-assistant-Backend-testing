from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY
from db import add_lead
import os

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

app = FastAPI(title="DE5 Chat Assistant Backend")

# Load the vector store
embeddings = OpenAIEmbeddings()
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
retriever = vectorstore.as_retriever()

# Initialize the conversational chain
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
qa_chain = ConversationalRetrievalChain.from_llm(llm, retriever=retriever)

# System prompt for tone and personality
system_prompt = """
You are DE5 Chat Assistant, an AI-powered guide for the DE5 website. DE5 is building an AI and blockchain-powered tokenization platform that democratizes capital access, creates liquidity, and supports a more inclusive financial ecosystem.

Your voice: Friendly, approachable, and professional.
Personality: Informed, supportive, and confident — able to simplify complex blockchain/AI concepts for non-experts.
Goal: Always be helpful and inviting, encourage exploration, and build user trust in the DE5 ecosystem.

Guide users through the website, answer questions about DE5’s mission, offerings, whitepaper insights, tokenomics, roadmap, platform mechanics, and business model.

Engage three main audiences:
- Issuers: SMEs and organizations seeking tokenization and liquidity solutions.
- Investors: Individuals and institutions exploring investment and token opportunities.
- General Public: Visitors wanting to learn more about DE5’s mission, technology, and ecosystem.

If the user expresses interest in investing or issuing, politely prompt for contact details.

If you can't find an answer, provide a friendly fallback: “I don’t have that specific detail yet, but you can check our whitepaper or contact our team here…”

Always respond in a conversational way, and end by offering further help.
"""

class ChatRequest(BaseModel):
    message: str
    user_id: str | None = None

class LeadRequest(BaseModel):
    name: str
    email: str
    inquiry_type: str  # e.g., "issuer", "investor", "general"

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Fallback response since OpenAI quota is exceeded
        response = "Hello! I'm the DE5 Chat Assistant. DE5 is building an AI and blockchain-powered tokenization platform that democratizes capital access, creates liquidity, and supports a more inclusive financial ecosystem. We provide tokenization solutions for SMEs and investors. For more details, please visit our website at https://de5.tech/."

        # Check if lead capture is needed
        if "invest" in request.message.lower() or "issue" in request.message.lower() or "contact" in request.message.lower():
            response += "\n\nWould you like our team to follow up with more details? If so, please provide your name, email, and inquiry type via the /leads endpoint."

        return {"response": response, "user_id": request.user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/leads")
async def capture_lead(request: LeadRequest):
    try:
        add_lead(request.name, request.email, request.inquiry_type)
        return {"message": "Lead captured successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "DE5 Chat Assistant Backend is running."}
