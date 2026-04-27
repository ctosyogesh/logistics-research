<<<<<<< HEAD
# logistics-research-agent
AI-powered autonomous research assistant for logistics industry
=======
# Logistics Research Agent

An advanced, LLM-powered autonomous researcher agent for the Logistics industry built with LangChain, CrewAI, FastAPI, and React.

## 🌟 Features

- **Autonomous Multi-Agent Research**: Leverages CrewAI to orchestrate specialized AI agents that autonomously navigate the web
- **Logistics Industry Specialization**: Agents are fine-tuned for supply chain, transportation, warehousing, and logistics topics
- **Comprehensive Analysis**: Processes queries through multiple research phases:
  - Data gathering from diverse web sources
  - Deep analysis and synthesis
  - Quality assurance and verification
  - Executive summary generation
- **Knowledge Repository**: Automatically persists research findings to a text-based knowledge base
- **Modern UI**: Clean, responsive React frontend with dark theme
- **Real-time Research**: Watch as agents conduct research in real-time
- **Multiple Research Depths**: Quick, Standard, or Comprehensive research modes

## 🏗️ Architecture

### Backend (FastAPI + LangChain + CrewAI)

- **FastAPI**: High-performance API server
- **LangChain**: LLM orchestration and tooling
- **CrewAI**: Multi-agent coordination framework
- **Groq Llama 3.3**: Fast, powerful AI model
- **DuckDuckGo Search**: Web search integration

#### Agent Crew Structure

1. **Data Intelligence Specialist**: Gathers information from web sources
2. **Senior Research Analyst**: Analyzes and identifies patterns
3. **Quality Assurance Specialist**: Verifies accuracy and completeness
4. **Strategic Insights Synthesizer**: Creates final comprehensive reports

### Frontend (React + Vite)

- **React 18**: Modern UI library
- **Vite**: Fast build tool and dev server
- **React Router**: Client-side routing
- **Axios**: HTTP client
- **Lucide Icons**: Beautiful icon set

## 📋 Prerequisites

- **Python 3.9+**
- **Node.js 16+**
- **Groq API Key** (get one at https://console.groq.com/)

## 🚀 Installation & Setup

### 1. Clone or Navigate to Project

```bash
cd /home/claude/logistics-research-agent
```

### 2. Backend Setup

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt --break-system-packages

# Create .env file
cp .env.example .env

# Edit .env and add your Groq API key
# GROQ_API_KEY=your_actual_api_key_here
```

### 3. Frontend Setup

```bash
cd ../frontend

# Install Node dependencies
npm install
```

## 🎯 Running the Application

### Start Backend Server

```bash
cd backend
python main.py
```

The API will be available at `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

### Start Frontend Development Server

In a new terminal:

```bash
cd frontend
npm run dev
```

The application will be available at `http://localhost:3000`

## 📚 API Documentation

### Endpoints

#### Research

**POST** `/api/research`
- Conduct new research
- Body: `{ "query": "string", "depth": "standard", "save_to_knowledge_base": true }`
- Returns: Research results with summary, key findings, sources, and full report

**GET** `/api/research/{research_id}/status`
- Get research job status
- Returns: Current status and progress

#### Knowledge Base

**GET** `/api/knowledge`
- List knowledge base entries
- Query params: `limit` (default: 20), `tag` (optional filter)

**GET** `/api/knowledge/{entry_id}`
- Get specific knowledge entry with full report

**DELETE** `/api/knowledge/{entry_id}`
- Delete a knowledge base entry

#### Statistics

**GET** `/api/stats`
- Get system statistics
- Returns: Research job stats and knowledge base metrics

**GET** `/health`
- Health check endpoint

## 💡 Usage Examples

### Example Research Queries

1. **Supply Chain Optimization**
   ```
   What are the latest trends in AI-powered supply chain optimization?
   ```

2. **Last-Mile Delivery**
   ```
   How are autonomous vehicles transforming last-mile delivery in urban areas?
   ```

3. **Warehouse Automation**
   ```
   What are the best practices for implementing warehouse robotics in 2024?
   ```

4. **Sustainability**
   ```
   How are logistics companies reducing carbon emissions through green initiatives?
   ```

5. **Technology Integration**
   ```
   What role does blockchain play in improving supply chain transparency?
   ```

### Research Depths

- **Quick** (3 sources): Fast overview for simple queries
- **Standard** (5 sources): Balanced depth for most use cases
- **Comprehensive** (8+ sources): In-depth analysis for complex topics

## 🗂️ Project Structure

```
logistics-research-agent/
├── backend/
│   ├── agents/
│   │   ├── __init__.py
│   │   └── research_crew.py       # CrewAI agent definitions
│   ├── utils/
│   │   ├── __init__.py
│   │   └── knowledge_manager.py   # Knowledge base management
│   ├── knowledge_repository/       # Saved research (created at runtime)
│   ├── main.py                     # FastAPI application
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ResearchPage.jsx
│   │   │   ├── ResearchPage.css
│   │   │   ├── KnowledgeBasePage.jsx
│   │   │   ├── KnowledgeBasePage.css
│   │   │   ├── StatisticsPage.jsx
│   │   │   └── StatisticsPage.css
│   │   ├── services/
│   │   │   └── api.js              # API client
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 🔧 Configuration

### Environment Variables (Backend)

```bash
# Required
GROQ_API_KEY=your_api_key

# Optional
PORT=8000
HOST=0.0.0.0
DEBUG=True
KNOWLEDGE_BASE_PATH=./knowledge_repository
```

### Frontend Configuration

Create `.env` in frontend directory (optional):

```bash
VITE_API_URL=http://localhost:8000
```

## 📊 Knowledge Repository

Research results are automatically saved to:
```
backend/knowledge_repository/
├── entries/
│   ├── kb_20240427_123456_123456_report.txt
│   ├── kb_20240427_123456_123456_meta.json
│   └── ...
└── index.json
```

Each entry contains:
- **Full Report**: Complete research analysis in text format
- **Metadata**: Query, summary, tags, timestamp in JSON
- **Index**: Searchable catalog of all entries

## 🎨 Features in Detail

### Multi-Agent Research Process

1. **Query Analysis**: AI agents analyze the research query
2. **Web Navigation**: Autonomous search across multiple sources
3. **Data Extraction**: Intelligent content extraction and filtering
4. **Quality Verification**: Cross-checking facts and validating sources
5. **Synthesis**: Creating structured, comprehensive reports
6. **Knowledge Persistence**: Automatic saving to repository

### Knowledge Base Features

- Browse all saved research
- Filter by tags (auto-generated from content)
- View detailed research reports
- Delete unwanted entries
- Full-text search capabilities

### Statistics Dashboard

- Total research jobs conducted
- Success rate metrics
- Knowledge base size and growth
- Most researched topics
- Recent activity tracking

## 🚨 Troubleshooting

### Backend Issues

**Import Errors**
```bash
pip install -r requirements.txt --break-system-packages
```

**API Key Not Found**
- Ensure `.env` file exists in `backend/` directory
- Verify `ANTHROPIC_API_KEY` is set correctly

**Port Already in Use**
- Change `PORT` in `.env` file
- Kill existing process: `lsof -ti:8000 | xargs kill -9`

### Frontend Issues

**Dependencies Not Installing**
```bash
rm -rf node_modules package-lock.json
npm install
```

**CORS Errors**
- Ensure backend is running
- Check API URL in frontend configuration

## 🔐 Security Notes

- Never commit `.env` files with real API keys
- Use environment variables for sensitive data
- Implement rate limiting in production
- Add authentication for production deployments

## 🚀 Production Deployment

### Backend

1. Set `DEBUG=False` in environment
2. Use production ASGI server (Gunicorn + Uvicorn)
3. Configure proper CORS origins
4. Set up SSL/TLS certificates
5. Implement authentication middleware

### Frontend

```bash
npm run build
```

Serve the `dist/` directory with nginx or similar.

## 📝 License

This project is for demonstration purposes.

## 🤝 Contributing

This is a demonstration project. Feel free to fork and modify for your needs.

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation at `/docs`
3. Examine backend logs for errors

## 🎯 Future Enhancements

- [ ] User authentication and multi-tenancy
- [ ] Advanced search with filters
- [ ] Export reports to PDF/DOCX
- [ ] Scheduled research jobs
- [ ] Email notifications
- [ ] Integration with more data sources
- [ ] Real-time collaboration features
- [ ] Custom agent configuration
- [ ] Research templates
- [ ] Analytics dashboard

## 🏆 Credits

Built with:
- [FastAPI](https://fastapi.tiangolo.com/)
- [LangChain](https://www.langchain.com/)
- [CrewAI](https://www.crewai.io/)
- [Groq](https://groq.com/)
- [React](https://react.dev/)
- [Vite](https://vitejs.dev/)

---

**Note**: This application requires an active Groq API key and makes real web searches. Groq offers generous free tier limits for testing and development.
>>>>>>> f03c5c2 (Initial commit: Logistics Research Agent with Groq Llama 3.3)
