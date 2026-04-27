# Complete Installation & Setup Guide
## Logistics Research Agent

---

## 📋 Prerequisites Check

Before starting, ensure you have:

- [x] **Python 3.9 or higher** - Check: `python --version` or `python3 --version`
- [x] **Node.js 16 or higher** - Check: `node --version`
- [x] **npm** - Check: `npm --version`
- [x] **Groq API Key** - Get from: https://console.groq.com/

---

## 🚀 Step-by-Step Installation

### Step 1: Download the Project

The complete project folder `logistics-research-agent` has been provided to you.

Navigate to the project:
```bash
cd logistics-research-agent
```

### Step 2: Backend Setup

#### 2.1 Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt --break-system-packages
```

**Expected output**: Installation of packages including fastapi, uvicorn, crewai, langchain, etc.

**If errors occur:**
- Ensure Python 3.9+ is installed
- Try: `pip3 install -r requirements.txt --break-system-packages`
- On Windows: Remove `--break-system-packages` flag

#### 2.2 Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file
nano .env  # or use your preferred editor (vim, code, etc.)
```

**Add your API key:**
```
GROQ_API_KEY=gsk_your_actual_key_here
```

**Save and exit:**
- In nano: `Ctrl+X`, then `Y`, then `Enter`
- In vim: Press `Esc`, type `:wq`, press `Enter`

#### 2.3 Test Backend Installation

```bash
# Still in the backend directory
python main.py
```

**Expected output:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Verify it works:**
Open browser to: `http://localhost:8000`

You should see:
```json
{
  "message": "Logistics Research Agent API",
  "version": "1.0.0",
  "status": "operational"
}
```

**Stop the server**: Press `Ctrl+C`

### Step 3: Frontend Setup

Open a new terminal (keep backend terminal available).

#### 3.1 Install Node Dependencies

```bash
# Navigate to frontend directory
cd logistics-research-agent/frontend

# Install dependencies
npm install
```

**Expected output**: Installation progress of React, Vite, and other packages.

**If errors occur:**
- Ensure Node.js 16+ is installed
- Try: `rm -rf node_modules package-lock.json && npm install`
- Check internet connection

#### 3.2 Test Frontend Installation

```bash
# Still in frontend directory
npm run dev
```

**Expected output:**
```
VITE v5.0.8  ready in XXX ms

➜  Local:   http://localhost:3000/
➜  Network: use --host to expose
```

**Verify it works:**
Open browser to: `http://localhost:3000`

You should see the Logistics Research Agent interface.

**Stop the dev server**: Press `Ctrl+C`

---

## 🎯 Running the Application

### Method 1: Using the Startup Script (Recommended)

From the project root directory:

```bash
# Make script executable (first time only)
chmod +x start.sh

# Start everything
./start.sh
```

This will start both backend and frontend servers automatically.

**You'll see:**
```
🚀 Starting Logistics Research Agent...
🔧 Starting Backend Server (Port 8000)...
🎨 Starting Frontend Server (Port 3000)...
✅ Application Started Successfully!

📍 Frontend: http://localhost:3000
📍 Backend API: http://localhost:8000
📍 API Docs: http://localhost:8000/docs
```

**To stop:** Press `Ctrl+C` once to stop both servers.

### Method 2: Manual Start (Two Terminals)

**Terminal 1 - Backend:**
```bash
cd logistics-research-agent/backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd logistics-research-agent/frontend
npm run dev
```

**To stop:** Press `Ctrl+C` in each terminal.

---

## ✅ Verification Checklist

After starting, verify everything works:

### Backend Verification
- [ ] Visit `http://localhost:8000` - Should show API info
- [ ] Visit `http://localhost:8000/docs` - Should show Swagger docs
- [ ] Visit `http://localhost:8000/health` - Should show `{"status": "healthy"}`

### Frontend Verification
- [ ] Visit `http://localhost:3000` - Should show the app
- [ ] Click on different tabs (Research, Knowledge Base, Statistics)
- [ ] No console errors in browser DevTools (F12)

### Full System Test
1. Go to Research tab
2. Enter: "What are the latest trends in warehouse automation?"
3. Select "Quick" depth
4. Click "Conduct Research"
5. Wait ~30 seconds
6. Should see results with summary and key findings

---

## 🔍 Troubleshooting

### Problem: "Port 8000 already in use"

**Solution:**
```bash
# Find what's using the port
lsof -ti:8000

# Kill the process (use the PID from above)
kill -9 <PID>

# Or change the port in backend/.env
PORT=8001
```

### Problem: "Port 3000 already in use"

**Solution:**
```bash
# The dev server will automatically try 3001, 3002, etc.
# Or kill the process:
lsof -ti:3000 | xargs kill -9
```

### Problem: "GROQ_API_KEY not found"

**Solution:**
```bash
# Verify .env file exists
ls -la backend/.env

# Check contents
cat backend/.env

# Ensure format is exactly:
GROQ_API_KEY=gsk_your_key_here
# No spaces around =
# No quotes needed
```

### Problem: "Module not found" errors

**Backend:**
```bash
cd backend
pip install -r requirements.txt --break-system-packages --force-reinstall
```

**Frontend:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Problem: Research returns errors

**Check:**
1. API key is correct and valid
2. Internet connection is working
3. Backend logs for specific error
4. Try with a simpler query first

### Problem: Frontend can't connect to backend

**Solution:**
```bash
# Verify backend is running
curl http://localhost:8000/health

# Check CORS settings in backend/main.py
# Ensure frontend is using correct API URL
```

---

## 📊 First Research Example

Once everything is running, try this:

1. **Open**: `http://localhost:3000`

2. **Enter this query:**
   ```
   How is artificial intelligence transforming supply chain optimization in 2024?
   ```

3. **Select**: Standard depth

4. **Check**: "Save to Knowledge Base" ✓

5. **Click**: "Conduct Research"

6. **Wait**: ~45 seconds

7. **Review**: 
   - Executive summary
   - 5-8 key findings
   - Detailed analysis
   - Source references

8. **Check Knowledge Base**:
   - Click "Knowledge Base" tab
   - See your saved research
   - Click "View" to see full details

9. **Check Statistics**:
   - Click "Statistics" tab
   - See research metrics

---

## 🎨 UI Overview

### Research Page
- **Query Input**: Enter your logistics question
- **Depth Selector**: Quick/Standard/Comprehensive
- **Save Toggle**: Save results to knowledge base
- **Example Queries**: Click to try pre-made queries
- **Results Section**: Summary, findings, sources, full report

### Knowledge Base Page
- **Tag Filters**: Filter by topic (auto-generated)
- **Entry Cards**: Saved research summaries
- **View Button**: See full research details
- **Delete Button**: Remove entries
- **Modal View**: Detailed research report

### Statistics Page
- **Metrics Cards**: Total entries, jobs, success rate
- **Breakdown**: Completed vs failed research
- **Top Topics**: Most researched areas
- **Health Status**: System operational status

---

## 📚 API Documentation

### Interactive API Docs

Visit: `http://localhost:8000/docs`

Features:
- Try out endpoints directly
- See request/response schemas
- Test authentication
- View all available operations

### Example API Calls

**Conduct Research:**
```bash
curl -X POST http://localhost:8000/api/research \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Impact of IoT on fleet management",
    "depth": "standard",
    "save_to_knowledge_base": true
  }'
```

**List Knowledge Base:**
```bash
curl http://localhost:8000/api/knowledge?limit=10
```

**Get Statistics:**
```bash
curl http://localhost:8000/api/stats
```

---

## 🔄 Daily Usage

### Starting Work
```bash
cd logistics-research-agent
./start.sh
```

### During Work
- Conduct research via UI
- Review results
- Browse knowledge base
- Monitor statistics

### Ending Work
- Press `Ctrl+C` to stop servers
- Research is auto-saved to knowledge base
- Knowledge base persists between sessions

---

## 💾 Data Persistence

### Knowledge Repository Location
```
logistics-research-agent/backend/knowledge_repository/
```

### Backup Your Research
```bash
# Create backup
cp -r backend/knowledge_repository backup_$(date +%Y%m%d)

# Restore backup
cp -r backup_YYYYMMDD backend/knowledge_repository
```

---

## 🎓 Next Steps

1. **Read** the full README.md for detailed features
2. **Try** different research queries
3. **Explore** the knowledge base filtering
4. **Customize** agents in `backend/agents/research_crew.py`
5. **Extend** with new features as needed

---

## 📞 Getting Help

### Documentation Files
- `README.md` - Comprehensive documentation
- `QUICKSTART.md` - Quick start guide
- `PROJECT_SUMMARY.md` - Technical overview
- This file - Installation guide

### Testing Checklist
If something doesn't work:
1. Check both servers are running
2. Verify API key in `.env`
3. Check browser console (F12)
4. Review backend terminal output
5. Try the example research query
6. Test API endpoints directly

---

## ✅ Installation Complete!

If you've followed all steps and verified the checklist, you're ready to use the Logistics Research Agent!

**Happy Researching!** 🚀📊🤖