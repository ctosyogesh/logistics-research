import os
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import asyncio
from contextlib import asynccontextmanager

from agents.research_crew import LogisticsResearchCrew
from utils.knowledge_manager import KnowledgeManager

load_dotenv()

# Global instances
knowledge_manager = None
research_crew = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for FastAPI application"""
    global knowledge_manager, research_crew
    
    # Startup
    knowledge_base_path = os.getenv("KNOWLEDGE_BASE_PATH", "./knowledge_repository")
    knowledge_manager = KnowledgeManager(knowledge_base_path)
    research_crew = LogisticsResearchCrew()
    
    yield
    
    # Shutdown
    knowledge_manager = None
    research_crew = None

app = FastAPI(
    title="Logistics Research Agent API",
    description="Advanced AI-powered research agent for logistics industry insights",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class ResearchRequest(BaseModel):
    query: str = Field(..., min_length=5, max_length=500, description="Research query about logistics")
    depth: str = Field(default="standard", description="Research depth: quick, standard, or comprehensive")
    save_to_knowledge_base: bool = Field(default=True, description="Whether to save results to knowledge base")

class ResearchResponse(BaseModel):
    research_id: str
    query: str
    status: str
    summary: Optional[str] = None
    key_findings: Optional[List[str]] = None
    sources: Optional[List[Dict]] = None
    full_report: Optional[str] = None
    timestamp: str
    saved_to_kb: bool = False

class ResearchStatus(BaseModel):
    research_id: str
    status: str
    progress: int
    message: str

class KnowledgeEntry(BaseModel):
    id: str
    query: str
    summary: str
    timestamp: str
    tags: List[str]

# In-memory storage for research status (in production, use Redis or similar)
research_jobs = {}

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Logistics Research Agent API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "research": "/api/research",
            "status": "/api/research/{research_id}/status",
            "knowledge": "/api/knowledge",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "knowledge_manager": knowledge_manager is not None,
            "research_crew": research_crew is not None
        }
    }

@app.post("/api/research", response_model=ResearchResponse)
async def conduct_research(
    request: ResearchRequest,
    background_tasks: BackgroundTasks
):
    """
    Initiate a research task using the autonomous agent crew
    """
    try:
        research_id = f"research_{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}"
        
        # Initialize research job status
        research_jobs[research_id] = {
            "status": "initiated",
            "progress": 0,
            "message": "Research task created"
        }
        
        # Execute research synchronously for immediate response
        # In production, consider using Celery or similar for true background processing
        try:
            research_jobs[research_id] = {
                "status": "processing",
                "progress": 25,
                "message": "Agents analyzing query..."
            }
            
            result = await asyncio.to_thread(
                research_crew.conduct_research,
                request.query,
                request.depth
            )
            
            research_jobs[research_id] = {
                "status": "completed",
                "progress": 100,
                "message": "Research completed successfully"
            }
            
            # Save to knowledge base if requested
            saved_to_kb = False
            if request.save_to_knowledge_base and result.get("summary"):
                kb_id = knowledge_manager.save_research(
                    query=request.query,
                    summary=result.get("summary", ""),
                    full_report=result.get("full_report", ""),
                    sources=result.get("sources", []),
                    key_findings=result.get("key_findings", [])
                )
                saved_to_kb = True
            
            return ResearchResponse(
                research_id=research_id,
                query=request.query,
                status="completed",
                summary=result.get("summary"),
                key_findings=result.get("key_findings", []),
                sources=result.get("sources", []),
                full_report=result.get("full_report"),
                timestamp=datetime.utcnow().isoformat(),
                saved_to_kb=saved_to_kb
            )
            
        except Exception as e:
            research_jobs[research_id] = {
                "status": "failed",
                "progress": 0,
                "message": f"Research failed: {str(e)}"
            }
            raise HTTPException(status_code=500, detail=f"Research execution failed: {str(e)}")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initiate research: {str(e)}")

@app.get("/api/research/{research_id}/status", response_model=ResearchStatus)
async def get_research_status(research_id: str):
    """
    Get the status of a research task
    """
    if research_id not in research_jobs:
        raise HTTPException(status_code=404, detail="Research job not found")
    
    job = research_jobs[research_id]
    return ResearchStatus(
        research_id=research_id,
        status=job["status"],
        progress=job["progress"],
        message=job["message"]
    )

@app.get("/api/knowledge", response_model=List[KnowledgeEntry])
async def list_knowledge_entries(
    limit: int = 20,
    tag: Optional[str] = None
):
    """
    List entries from the knowledge base
    """
    try:
        entries = knowledge_manager.list_entries(limit=limit, tag=tag)
        return entries
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve knowledge entries: {str(e)}")

@app.get("/api/knowledge/{entry_id}")
async def get_knowledge_entry(entry_id: str):
    """
    Get a specific knowledge base entry
    """
    try:
        entry = knowledge_manager.get_entry(entry_id)
        if not entry:
            raise HTTPException(status_code=404, detail="Knowledge entry not found")
        return entry
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve knowledge entry: {str(e)}")

@app.delete("/api/knowledge/{entry_id}")
async def delete_knowledge_entry(entry_id: str):
    """
    Delete a knowledge base entry
    """
    try:
        success = knowledge_manager.delete_entry(entry_id)
        if not success:
            raise HTTPException(status_code=404, detail="Knowledge entry not found")
        return {"message": "Entry deleted successfully", "entry_id": entry_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete knowledge entry: {str(e)}")

@app.get("/api/stats")
async def get_statistics():
    """
    Get research and knowledge base statistics
    """
    try:
        kb_stats = knowledge_manager.get_statistics()
        
        # Research jobs statistics
        total_jobs = len(research_jobs)
        completed_jobs = sum(1 for job in research_jobs.values() if job["status"] == "completed")
        failed_jobs = sum(1 for job in research_jobs.values() if job["status"] == "failed")
        
        return {
            "knowledge_base": kb_stats,
            "research_jobs": {
                "total": total_jobs,
                "completed": completed_jobs,
                "failed": failed_jobs,
                "success_rate": f"{(completed_jobs/total_jobs*100):.1f}%" if total_jobs > 0 else "0%"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve statistics: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=os.getenv("DEBUG", "True").lower() == "true"
    )
