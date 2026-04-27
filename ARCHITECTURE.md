# System Architecture
## Logistics Research Agent

---

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                           │
│                    (React + Vite Frontend)                       │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Research   │  │  Knowledge   │  │ Statistics   │          │
│  │     Page     │  │     Base     │  │     Page     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTP/REST API
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                      API GATEWAY                                 │
│                   (FastAPI Backend)                              │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Endpoint Handlers                            │   │
│  │  • /api/research        • /api/knowledge                 │   │
│  │  • /api/stats          • /health                         │   │
│  └───────────────────┬──────────────────────────────────────┘   │
│                      │                                           │
│  ┌──────────────────▼──────────────────────────────────────┐   │
│  │         Business Logic Layer                             │   │
│  │                                                           │   │
│  │  ┌──────────────────┐    ┌──────────────────┐           │   │
│  │  │  Research Crew   │    │ Knowledge Manager│           │   │
│  │  │   Orchestrator   │    │                  │           │   │
│  │  └──────────────────┘    └──────────────────┘           │   │
│  └───────────────────┬──────────────────────────────────────┘   │
└────────────────────────┼────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   CrewAI     │  │  LangChain   │  │ Knowledge    │
│  Multi-Agent │  │    Tools     │  │  Repository  │
│   Framework  │  │              │  │              │
└──────┬───────┘  └──────┬───────┘  └──────────────┘
       │                 │
       ▼                 ▼
┌──────────────┐  ┌──────────────┐
│  Anthropic   │  │ DuckDuckGo   │
│   Claude     │  │    Search    │
│  Sonnet 4    │  │              │
└──────────────┘  └──────────────┘
```

---

## 🤖 Multi-Agent Research System

```
                    ┌─────────────────────┐
                    │   User Research     │
                    │       Query         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Research Crew      │
                    │   Orchestrator      │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
   ┌──────────────────┐ ┌──────────────┐ ┌──────────────┐
   │   AGENT 1        │ │   AGENT 2    │ │   AGENT 3    │
   │ Data Gatherer    │ │  Analyst     │ │  QA Specialist│
   │                  │ │              │ │               │
   │ • Web Search     │ │ • Pattern    │ │ • Fact Check  │
   │ • Source Find    │ │   Analysis   │ │ • Validation  │
   │ • Extract Data   │ │ • Insights   │ │ • Verification│
   └─────────┬────────┘ └──────┬───────┘ └──────┬────────┘
             │                 │                 │
             └────────┬────────┴────────┬────────┘
                      │                 │
                      ▼                 ▼
              ┌──────────────────┐ ┌──────────────┐
              │   AGENT 4        │ │  Knowledge   │
              │  Synthesizer     │ │   Manager    │
              │                  │ │              │
              │ • Compile        │ │ • Save       │
              │ • Summarize      │ │ • Index      │
              │ • Structure      │ │ • Tag        │
              └────────┬─────────┘ └──────┬───────┘
                       │                  │
                       ▼                  ▼
              ┌──────────────────┐ ┌──────────────┐
              │  Final Report    │ │  Knowledge   │
              │  to User         │ │  Repository  │
              └──────────────────┘ └──────────────┘
```

---

## 📊 Data Flow Diagram

```
┌──────────┐
│  User    │
│  Input   │
└────┬─────┘
     │ 1. Submit Query
     ▼
┌──────────────────┐
│  Frontend UI     │ POST /api/research
│  (React)         ├────────────────────┐
└──────────────────┘                    │
                                        ▼
                              ┌──────────────────┐
                              │  FastAPI         │
                              │  Endpoint        │
                              └────────┬─────────┘
                                       │ 2. Validate Request
                                       ▼
                              ┌──────────────────┐
                              │ Research Crew    │
                              │ Orchestrator     │
                              └────────┬─────────┘
                                       │ 3. Initialize Agents
                                       ▼
                    ┌──────────────────────────────────┐
                    │      Agent Execution             │
                    │  ┌─────────────────────────┐    │
                    │  │ 1. Data Gathering       │    │
                    │  │    ├─ Web Search        │    │
                    │  │    ├─ Source Validation │    │
                    │  │    └─ Extract Info      │    │
                    │  └──────────┬──────────────┘    │
                    │             │                    │
                    │  ┌──────────▼──────────────┐    │
                    │  │ 2. Analysis             │    │
                    │  │    ├─ Pattern Finding   │    │
                    │  │    ├─ Trend Analysis    │    │
                    │  │    └─ Insight Gen       │    │
                    │  └──────────┬──────────────┘    │
                    │             │                    │
                    │  ┌──────────▼──────────────┐    │
                    │  │ 3. Quality Assurance    │    │
                    │  │    ├─ Fact Check        │    │
                    │  │    ├─ Verify Sources    │    │
                    │  │    └─ Validate Claims   │    │
                    │  └──────────┬──────────────┘    │
                    │             │                    │
                    │  ┌──────────▼──────────────┐    │
                    │  │ 4. Synthesis            │    │
                    │  │    ├─ Create Summary    │    │
                    │  │    ├─ Format Report     │    │
                    │  │    └─ Structure Output  │    │
                    │  └──────────┬──────────────┘    │
                    └─────────────┼───────────────────┘
                                  │ 4. Research Results
                                  ▼
                        ┌──────────────────┐
                        │ Knowledge Manager│
                        │                  │
                        │ • Parse Results  │
                        │ • Extract Tags   │
                        │ • Save to Disk   │
                        │ • Update Index   │
                        └────────┬─────────┘
                                 │ 5. Confirmation
                                 ▼
                        ┌──────────────────┐
                        │  API Response    │
                        │  (JSON)          │
                        └────────┬─────────┘
                                 │ 6. HTTP Response
                                 ▼
                        ┌──────────────────┐
                        │  Frontend UI     │
                        │  Display Results │
                        └──────────────────┘
```

---

## 🗄️ Knowledge Repository Structure

```
knowledge_repository/
│
├── index.json                          # Master index
│   {
│     "entries": [
│       {
│         "id": "kb_20240427_...",
│         "query": "...",
│         "summary": "...",
│         "tags": ["tag1", "tag2"],
│         "timestamp": "..."
│       }
│     ]
│   }
│
└── entries/                            # Individual research entries
    │
    ├── kb_20240427_123456_report.txt  # Full text report
    │   ┌─────────────────────────────────────────┐
    │   │ LOGISTICS RESEARCH REPORT              │
    │   │ ======================================  │
    │   │                                         │
    │   │ Query: How is AI transforming...       │
    │   │ Date: 2024-04-27T12:34:56Z            │
    │   │                                         │
    │   │ EXECUTIVE SUMMARY                      │
    │   │ ...detailed summary...                 │
    │   │                                         │
    │   │ KEY FINDINGS                           │
    │   │ 1. ...                                 │
    │   │ 2. ...                                 │
    │   │                                         │
    │   │ DETAILED ANALYSIS                      │
    │   │ ...comprehensive report...             │
    │   └─────────────────────────────────────────┘
    │
    └── kb_20240427_123456_meta.json   # Metadata
        {
          "id": "kb_20240427_123456_789012",
          "query": "Research query",
          "summary": "Executive summary",
          "key_findings": [...],
          "sources": [...],
          "tags": [...],
          "timestamp": "2024-04-27T12:34:56.789Z"
        }
```

---

## 🔄 Request/Response Flow

### Research Request Flow

```
1. User Action
   └─► Click "Conduct Research"

2. Frontend Validation
   └─► Validate query length, depth selection

3. API Call
   └─► POST /api/research
       Body: {
         "query": "...",
         "depth": "standard",
         "save_to_knowledge_base": true
       }

4. Backend Processing
   ├─► Validate request (Pydantic)
   ├─► Generate research ID
   ├─► Initialize research crew
   ├─► Execute agent tasks (sequential)
   │   ├─► Data Gathering Task
   │   ├─► Analysis Task
   │   ├─► QA Task
   │   └─► Synthesis Task
   ├─► Parse results
   └─► Save to knowledge base (if requested)

5. Response
   └─► Return JSON {
         "research_id": "...",
         "summary": "...",
         "key_findings": [...],
         "sources": [...],
         "full_report": "...",
         "saved_to_kb": true
       }

6. Frontend Update
   └─► Display results in UI
```

---

## 🔌 API Integration Points

```
┌──────────────────────────────────────────────────────┐
│              External Services                        │
├──────────────────────────────────────────────────────┤
│                                                       │
│  ┌─────────────────┐      ┌─────────────────┐       │
│  │  Anthropic API  │      │ DuckDuckGo API  │       │
│  │                 │      │                 │       │
│  │ • Claude Model  │      │ • Web Search    │       │
│  │ • Token Usage   │      │ • Results       │       │
│  │ • Responses     │      │ • Snippets      │       │
│  └────────┬────────┘      └────────┬────────┘       │
│           │                        │                 │
└───────────┼────────────────────────┼─────────────────┘
            │                        │
            ▼                        ▼
┌──────────────────────────────────────────────────────┐
│           LangChain Integration Layer                 │
│                                                       │
│  ┌─────────────────┐      ┌─────────────────┐       │
│  │ ChatAnthropic   │      │ DuckDuckGo Tool │       │
│  │ Wrapper         │      │ Wrapper         │       │
│  └────────┬────────┘      └────────┬────────┘       │
│           │                        │                 │
│           └────────────┬───────────┘                 │
│                        │                             │
└────────────────────────┼─────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────┐
│              CrewAI Agent Framework                   │
│                                                       │
│  Agents use LangChain tools to:                      │
│  • Make LLM calls via ChatAnthropic                  │
│  • Search web via DuckDuckGo                         │
│  • Process and analyze information                   │
│  • Generate structured outputs                       │
└──────────────────────────────────────────────────────┘
```

---

## 💾 State Management

### Backend State

```
┌─────────────────────────────────────────┐
│        In-Memory State                   │
│  (research_jobs dictionary)              │
│                                          │
│  {                                       │
│    "research_xyz": {                     │
│      "status": "processing",             │
│      "progress": 50,                     │
│      "message": "Analyzing data..."      │
│    }                                     │
│  }                                       │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│      Persistent State                    │
│  (File System)                           │
│                                          │
│  knowledge_repository/                   │
│    ├── index.json                        │
│    └── entries/                          │
│        ├── *.txt                         │
│        └── *.json                        │
└─────────────────────────────────────────┘
```

### Frontend State

```
React Component State
├── ResearchPage
│   ├── query (string)
│   ├── depth (string)
│   ├── isResearching (boolean)
│   ├── result (object)
│   └── error (string)
│
├── KnowledgeBasePage
│   ├── entries (array)
│   ├── selectedEntry (object)
│   ├── filterTag (string)
│   └── isLoading (boolean)
│
└── StatisticsPage
    ├── stats (object)
    ├── health (object)
    └── isLoading (boolean)
```

---

## 🔒 Security Architecture

```
┌─────────────────────────────────────────────────┐
│              Security Layers                     │
├─────────────────────────────────────────────────┤
│                                                  │
│  1. Environment Variables                       │
│     • API keys in .env (not committed)          │
│     • Sensitive config isolated                 │
│                                                  │
│  2. Input Validation                            │
│     • Pydantic models validate all inputs       │
│     • Type checking enforced                    │
│     • Length limits on queries                  │
│                                                  │
│  3. CORS Configuration                          │
│     • Controlled cross-origin requests          │
│     • Configurable allowed origins              │
│                                                  │
│  4. Error Handling                              │
│     • Sanitized error messages                  │
│     • No sensitive data in responses            │
│     • Proper exception catching                 │
│                                                  │
│  5. API Rate Limiting (Production)              │
│     • Prevent abuse                             │
│     • Resource protection                       │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## 📈 Scalability Considerations

### Current Architecture (Single Instance)
```
┌──────────────┐
│   Frontend   │
│   (Static)   │
└──────┬───────┘
       │
┌──────▼───────┐
│   Backend    │
│  (FastAPI)   │
└──────┬───────┘
       │
┌──────▼───────┐
│ File System  │
│   Storage    │
└──────────────┘
```

### Scalable Architecture (Future)
```
┌──────────────┐     ┌──────────────┐
│   Frontend   │     │   Frontend   │
│   (CDN)      │     │   (CDN)      │
└──────┬───────┘     └──────┬───────┘
       │                    │
       └─────────┬──────────┘
                 │
         ┌───────▼────────┐
         │ Load Balancer  │
         └───────┬────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
┌───▼───┐   ┌───▼───┐   ┌───▼───┐
│Backend│   │Backend│   │Backend│
│   1   │   │   2   │   │   3   │
└───┬───┘   └───┬───┘   └───┬───┘
    │           │           │
    └───────────┼───────────┘
                │
        ┌───────▼────────┐
        │   Database     │
        │  (PostgreSQL)  │
        └────────────────┘
```

---

This architecture provides a solid foundation for an enterprise-grade research agent system!
