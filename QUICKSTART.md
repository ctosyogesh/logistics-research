# Quick Start Guide

## Get Started in 3 Steps

### 1. Setup Environment

```bash
# Navigate to project
cd /home/claude/logistics-research-agent

# Setup backend
cd backend
pip install -r requirements.txt --break-system-packages
cp .env.example .env

# Edit .env and add your Groq API key
nano .env  # or use any text editor
# Add: GROQ_API_KEY=your_actual_key_here

# Setup frontend
cd ../frontend
npm install
cd ..
```

### 2. Start the Application

**Option A: Use the startup script (recommended)**
```bash
./start.sh
```

**Option B: Manual start**

Terminal 1 (Backend):
```bash
cd backend
python main.py
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

### 3. Use the Application

1. Open browser to: **http://localhost:3000**
2. Enter a logistics research query, for example:
   - "What are the latest trends in warehouse automation?"
   - "How is AI transforming supply chain optimization?"
3. Select research depth (Quick/Standard/Comprehensive)
4. Click "Conduct Research"
5. Watch the agents work and review results!

## Example Workflow

### Research a Topic
1. Go to the **Research** tab
2. Enter: "Impact of autonomous delivery drones on last-mile logistics"
3. Select "Standard" depth
4. Check "Save to Knowledge Base"
5. Click "Conduct Research"
6. Wait 30-60 seconds for completion
7. Review the comprehensive report with:
   - Executive summary
   - Key findings
   - Detailed analysis
   - Source references

### Browse Knowledge Base
1. Click **Knowledge Base** tab
2. View all saved research
3. Filter by tags (supply_chain, automation, etc.)
4. Click "View" to see full details
5. Download reports as needed

### Check Statistics
1. Click **Statistics** tab
2. View research metrics
3. See most researched topics
4. Monitor system health

## Tips for Best Results

### Research Query Tips
- Be specific: "warehouse robotics ROI analysis" vs "robots"
- Include context: "2024 trends in cold chain logistics"
- Ask focused questions: "How does X impact Y?"
- Mention logistics aspects: "supply chain", "freight", "warehousing"

### Research Depth Selection
- **Quick**: Simple factual questions, overviews
- **Standard**: Most research questions, balanced depth
- **Comprehensive**: Complex topics needing thorough analysis

### Knowledge Base Management
- Tag-based organization auto-generated
- Search by topic, date, or tags
- Delete outdated research as needed
- Export reports for sharing

## Troubleshooting

**Backend won't start**
- Check if port 8000 is available
- Verify GROQ_API_KEY in .env
- Check Python dependencies installed

**Frontend won't start**
- Ensure Node.js 16+ installed
- Delete node_modules and reinstall
- Check port 3000 is available

**Research fails**
- Verify API key is valid
- Check internet connection
- Review backend logs for errors
- Try a simpler query first

**No results returned**
- Query may be too vague
- Try different phrasing
- Check backend is running
- Review API documentation

## API Testing (Optional)

Test the API directly:

```bash
# Health check
curl http://localhost:8000/health

# Conduct research
curl -X POST http://localhost:8000/api/research \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Latest trends in logistics automation",
    "depth": "quick",
    "save_to_knowledge_base": true
  }'

# List knowledge base
curl http://localhost:8000/api/knowledge
```

## Next Steps

1. **Customize Agents**: Edit `backend/agents/research_crew.py`
2. **Add Features**: Extend API endpoints in `backend/main.py`
3. **Modify UI**: Update React components in `frontend/src/components/`
4. **Deploy**: Follow production deployment guide in README.md

## Getting Help

- Read the full README.md for detailed documentation
- Check API docs: http://localhost:8000/docs
- Review example queries in the UI
- Examine backend logs for debugging

Happy Researching! 🚀