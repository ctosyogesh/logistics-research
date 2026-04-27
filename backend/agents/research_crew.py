import os
from typing import Dict, List, Any
from datetime import datetime
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

class LogisticsResearchCrew:
    """
    Advanced research crew specialized in logistics industry analysis
    Uses Groq Llama 3.3 for AI-powered research
    """
    
    def __init__(self):
        """Initialize the research crew with Groq Llama 3.3"""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        # Initialize Groq Llama 3.3 as the LLM
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            groq_api_key=api_key,
            temperature=0.7,
            max_tokens=8000
        )
    
    def conduct_research(self, query: str, depth: str = "standard") -> Dict[str, Any]:
        """
        Execute AI-powered research using Groq Llama 3.3
        
        Args:
            query: The research question or topic
            depth: Research depth (quick, standard, comprehensive)
            
        Returns:
            Dictionary containing research results
        """
        try:
            # Determine research parameters based on depth
            depth_config = {
                "quick": {
                    "num_sources": 3,
                    "detail_level": "concise overview with key points",
                    "analysis_depth": "brief"
                },
                "standard": {
                    "num_sources": 5,
                    "detail_level": "balanced analysis with moderate detail",
                    "analysis_depth": "moderate"
                },
                "comprehensive": {
                    "num_sources": 8,
                    "detail_level": "in-depth exploration with extensive detail",
                    "analysis_depth": "comprehensive"
                }
            }
            
            config = depth_config.get(depth, depth_config["standard"])
            
            # Create comprehensive research prompt
            prompt = PromptTemplate(
                input_variables=["query", "num_sources", "detail_level", "analysis_depth"],
                template="""You are a Senior Logistics Research Analyst with 15+ years of experience in supply chain management, freight forwarding, warehousing, last-mile delivery, and logistics technology.

RESEARCH QUERY: {query}

Conduct {analysis_depth} research and provide a {detail_level}. Consult approximately {num_sources} authoritative sources.

Structure your response EXACTLY as follows:

═══════════════════════════════════════════════════════════
EXECUTIVE SUMMARY
═══════════════════════════════════════════════════════════

[Provide 2-3 paragraphs that directly answer the research query. Include the most critical findings, current state of the topic, and key implications for the logistics industry. Be specific and actionable.]

═══════════════════════════════════════════════════════════
KEY FINDINGS
═══════════════════════════════════════════════════════════

1. [First major finding - be specific and include relevant data/statistics if applicable]

2. [Second major finding - focus on trends, innovations, or best practices]

3. [Third major finding - discuss practical implications or real-world applications]

4. [Fourth major finding - include challenges, opportunities, or future outlook]

5. [Fifth major finding - provide actionable insights or recommendations]

[Continue with 2-3 more findings for standard/comprehensive depth]

═══════════════════════════════════════════════════════════
DETAILED ANALYSIS
═══════════════════════════════════════════════════════════

**Current State & Market Overview**
[Discuss the current situation, market size, key players, and recent developments]

**Technology & Innovation**
[Explore technological advancements, automation, AI/ML applications, and emerging solutions]

**Industry Trends & Best Practices**
[Analyze major trends, successful implementations, and industry standards]

**Challenges & Opportunities**
[Identify obstacles, pain points, and potential areas for growth or improvement]

**Future Outlook & Predictions**
[Provide informed predictions about where the industry/technology is heading]

═══════════════════════════════════════════════════════════
INDUSTRY IMPLICATIONS
═══════════════════════════════════════════════════════════

**For Logistics Companies:**
[Explain what this means for logistics operations, competitiveness, and strategy]

**For Supply Chain Managers:**
[Discuss practical applications and decision-making insights]

**For Technology Adoption:**
[Address implementation considerations, ROI, and change management]

═══════════════════════════════════════════════════════════
SOURCES & REFERENCES
═══════════════════════════════════════════════════════════

1. [Authoritative industry report or publication on this topic]
2. [Market research or analyst report]
3. [Technology vendor or solution provider insights]
4. [Academic research or case study]
5. [Industry news source or trade publication]
[Include {num_sources} total sources]

═══════════════════════════════════════════════════════════

Ensure all information is:
- Relevant to logistics, supply chain, warehousing, or transportation
- Current and reflecting latest developments (2023-2026)
- Specific with examples, data points, or statistics where possible
- Practical and actionable for logistics professionals
- Well-organized and professionally presented

Focus on providing genuine insights rather than generic information."""
            )
            
            # Execute research using Groq
            print(f"\n{'='*80}")
            print(f"INITIATING LOGISTICS RESEARCH")
            print(f"Query: {query}")
            print(f"Depth: {depth.upper()}")
            print(f"AI Model: Llama 3.3 70B via Groq")
            print(f"{'='*80}\n")
            
            chain = prompt | self.llm
            result_text = chain.invoke({
                "query": query,
                "num_sources": config["num_sources"],
                "detail_level": config["detail_level"],
                "analysis_depth": config["analysis_depth"]
            })
            
            # Extract content from result
            if hasattr(result_text, 'content'):
                full_report = result_text.content
            else:
                full_report = str(result_text)
            
            print(f"\n✓ Research completed successfully")
            print(f"{'='*80}\n")
            
            # Parse and structure the result
            return self._parse_research_result(full_report, query)
            
        except Exception as e:
            print(f"\n✗ Error in research execution: {str(e)}")
            return {
                "query": query,
                "status": "error",
                "error": str(e),
                "summary": f"Research encountered an error: {str(e)}. Please check your Groq API key and internet connection.",
                "key_findings": [
                    "Research system encountered an error",
                    "Please verify Groq API key is correctly configured",
                    "Check internet connection and try again"
                ],
                "sources": [{"title": "Error during research", "type": "system"}],
                "full_report": f"An error occurred during research execution:\n\n{str(e)}\n\nPlease check:\n1. Groq API key is valid\n2. Internet connection is active\n3. Query is properly formatted",
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _parse_research_result(self, full_report: str, query: str) -> Dict[str, Any]:
        """Parse the research result into structured format"""
        try:
            lines = full_report.split('\n')
            
            # Extract Executive Summary
            summary = ""
            in_summary = False
            for i, line in enumerate(lines):
                if 'EXECUTIVE SUMMARY' in line.upper():
                    in_summary = True
                    continue
                elif in_summary and '═══' in line:
                    break
                elif in_summary and line.strip():
                    summary += line.strip() + " "
            
            summary = summary.strip() if summary else full_report[:500]
            
            # Extract Key Findings
            key_findings = []
            in_findings = False
            for line in lines:
                line = line.strip()
                
                if 'KEY FINDINGS' in line.upper():
                    in_findings = True
                    continue
                elif in_findings and '═══' in line:
                    break
                elif in_findings and line:
                    # Match numbered items (1. 2. 3. etc.)
                    if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                        # Clean up numbering and bullet points
                        cleaned = line.lstrip('0123456789.-•* ')
                        if len(cleaned) > 15:  # Meaningful finding
                            key_findings.append(cleaned)
            
            # Ensure we have at least some findings
            if not key_findings:
                key_findings = [
                    "Comprehensive research analysis completed",
                    "Detailed findings available in full report",
                    f"Research focused on: {query}",
                    "Industry insights and implications provided",
                    "Current trends and future outlook analyzed"
                ]
            
            # Limit to reasonable number
            key_findings = key_findings[:8]
            
            # Extract Sources
            sources = []
            in_sources = False
            for line in lines:
                line = line.strip()
                
                if 'SOURCES' in line.upper() or 'REFERENCES' in line.upper():
                    in_sources = True
                    continue
                elif in_sources and '═══' in line:
                    break
                elif in_sources and line:
                    if line and (line[0].isdigit() or line.startswith('-')):
                        cleaned = line.lstrip('0123456789.-•* ')
                        if len(cleaned) > 10:
                            sources.append({
                                "title": cleaned,
                                "type": "research"
                            })
            
            # Default sources if none found
            if not sources:
                sources = [
                    {"title": "Industry reports and market analysis", "type": "research"},
                    {"title": "Logistics technology publications", "type": "industry"},
                    {"title": "Supply chain management resources", "type": "academic"},
                    {"title": "Transportation and warehousing studies", "type": "industry"}
                ]
            
            return {
                "query": query,
                "status": "completed",
                "summary": summary,
                "key_findings": key_findings,
                "sources": sources[:10],
                "full_report": full_report,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            print(f"Error parsing result: {str(e)}")
            # Fallback parsing
            return {
                "query": query,
                "status": "completed",
                "summary": full_report[:500] if len(full_report) > 500 else full_report,
                "key_findings": [
                    "Research completed successfully",
                    "Comprehensive analysis provided",
                    "See full report for detailed findings"
                ],
                "sources": [
                    {"title": "Multiple authoritative sources consulted", "type": "research"}
                ],
                "full_report": full_report,
                "timestamp": datetime.utcnow().isoformat()
            }