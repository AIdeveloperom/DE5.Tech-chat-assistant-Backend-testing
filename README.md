# DE5 Chat Assistant Backend

This is the backend implementation for the DE5 Chat Assistant, a Python-based REST API using FastAPI. The assistant serves as an interactive guide for the DE5 website, helping users understand DE5's mission, offerings, and whitepaper insights through conversational AI.

## Project Overview

DE5 is building an AI and blockchain-powered tokenization platform that democratizes capital access, creates liquidity, and supports a more inclusive financial ecosystem. This chat assistant provides:

- **Knowledge Retrieval**: Answers questions about DE5's whitepaper, tokenomics, roadmap, platform mechanics, and business model.
- **Navigation Support**: Guides users through website sections and resources.
- **Audience Adaptation**: Tailors responses for issuers, investors, and general public.
- **Lead Capture**: Collects user contact details when they express interest.
- **Fallback Handling**: Provides friendly responses when information is unavailable.

## Architecture

The backend consists of the following components:

### 1. **main.py** - FastAPI Application
The main entry point with REST API endpoints.

**Key Features:**
- `/chat` endpoint: Handles user messages and returns AI-generated responses.
- `/leads` endpoint: Captures user contact information for lead generation.
- `/` root endpoint: Basic health check.

**Implementation Details:**
- Uses FastAPI for high-performance async API framework.
- Integrates LangChain's ConversationalRetrievalChain for context-aware responses.
- Loads pre-built ChromaDB vector store for knowledge retrieval.
- Implements error handling and fallback responses.
- Uses Pydantic models for request/response validation.

### 2. **knowledge_base.py** - Knowledge Base Builder
Scrapes the DE5 website and builds a vectorized knowledge base.

**Step-by-Step Process:**
1. **Web Scraping**: Uses BeautifulSoup to crawl https://de5.tech/ and extract all internal links.
2. **Document Loading**: Employs LangChain's WebBaseLoader to fetch and parse web pages.
3. **Text Splitting**: Breaks documents into manageable chunks (1000 characters with 200 overlap) for better retrieval.
4. **Embedding Generation**: Uses OpenAI embeddings to convert text chunks into vector representations.
5. **Vector Storage**: Persists vectors in ChromaDB for efficient similarity search.

### 3. **db.py** - Database Management
Handles lead capture using SQLite database.

**Database Schema:**
- `leads` table with columns: id, name, email, inquiry_type, timestamp
- Automatic table creation on module import
- Thread-safe operations using SQLite connections

### 4. **config.py** - Configuration Management
Manages environment variables and API keys.

**Security Note:** API keys are loaded from environment variables to avoid hardcoding sensitive information.

### 5. **requirements.txt** - Dependencies
Lists all Python packages required for the project:
- `fastapi`: Web framework
- `uvicorn`: ASGI server
- `openai`: AI model integration
- `langchain`: LLM framework for retrieval-augmented generation
- `chromadb`: Vector database
- `beautifulsoup4`: HTML parsing for web scraping
- `requests`: HTTP client for scraping
- `pydantic`: Data validation

## Setup Instructions

### Step 1: Environment Setup
1. Ensure Python 3.8+ is installed
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Environment Variables
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### Step 4: Build Knowledge Base
Run the knowledge base builder to scrape DE5 website and create vector store:
```bash
python knowledge_base.py
```
This will create a `chroma_db/` directory with the vectorized knowledge base.

### Step 5: Start the Server
```bash
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`

## API Documentation

### GET /
**Health Check**
- Returns: `{"message": "DE5 Chat Assistant Backend"}`

### POST /chat
**Chat Interaction**
- **Request Body:**
  ```json
  {
    "message": "What is DE5's mission?",
    "user_id": "optional_user_identifier"
  }
  ```
- **Response:**
  ```json
  {
    "response": "DE5 is building an AI and blockchain-powered tokenization platform...",
    "sources": ["https://de5.tech/page1", "https://de5.tech/page2"]
  }
  ```

### POST /leads
**Lead Capture**
- **Request Body:**
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "inquiry_type": "investor"
  }
  ```
- **Response:**
  ```json
  {
    "message": "Lead captured successfully"
  }
  ```

## AI Implementation Details

### Retrieval-Augmented Generation (RAG)
1. **Query Processing**: User message is processed and embedded using OpenAI embeddings.
2. **Similarity Search**: ChromaDB finds the most relevant document chunks.
3. **Context Assembly**: Retrieved chunks are combined with the query.
4. **Response Generation**: OpenAI GPT model generates a contextual response.
5. **Source Attribution**: Relevant source URLs are included in the response.

### Tone and Personality
The AI is prompted to maintain:
- Friendly, approachable, and professional tone
- Informed and supportive personality
- Ability to simplify complex concepts
- Encouraging exploration and building trust

### Fallback Mechanisms
- If knowledge base query fails, provides generic helpful responses
- Graceful error handling for API failures
- Default responses when information is unavailable

## Testing

Run the included test script:
```bash
python test_endpoints.py
```

This tests all endpoints and validates responses.

## Deployment Considerations

### Production Setup
1. Use a production WSGI server like Gunicorn
2. Set up proper environment variable management
3. Implement rate limiting and authentication
4. Use a robust database for lead storage (PostgreSQL/MySQL)
5. Set up monitoring and logging

### Security Measures
- API keys stored as environment variables
- Input validation using Pydantic
- CORS configuration for frontend integration
- Rate limiting to prevent abuse

### Scalability
- ChromaDB can be replaced with cloud vector databases (Pinecone, Weaviate)
- Implement caching for frequently asked questions
- Use async processing for heavy computations

## Future Enhancements

- **Multilingual Support**: Add language detection and translation
- **Advanced Analytics**: Track user interactions and FAQs
- **Integration**: Connect with DE5's CRM and community platforms
- **Personalization**: User journey tracking and customized responses
- **Voice Integration**: Add speech-to-text and text-to-speech capabilities

## File Structure
```
DE5.tech chat assistant backend/
├── main.py                 # FastAPI application
├── knowledge_base.py       # Knowledge base builder
├── db.py                   # Database operations
├── config.py               # Configuration management
├── requirements.txt        # Python dependencies
├── test_endpoints.py       # API testing script
├── chroma_db/              # Vector database (generated)
├── leads.db                # SQLite database (generated)
├── __pycache__/            # Python cache files
├── .git/                   # Git repository
└── README.md               # This documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and test thoroughly
4. Submit a pull request with detailed description

## License

This project is proprietary to DE5. All rights reserved.
