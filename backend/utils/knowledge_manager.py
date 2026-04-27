import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import re

class KnowledgeManager:
    """
    Manages the text-based knowledge repository for research findings
    """
    
    def __init__(self, base_path: str = "./knowledge_repository"):
        """
        Initialize the knowledge manager
        
        Args:
            base_path: Directory path for storing knowledge entries
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        self.entries_path = self.base_path / "entries"
        self.entries_path.mkdir(exist_ok=True)
        
        self.index_path = self.base_path / "index.json"
        self._ensure_index()
    
    def _ensure_index(self):
        """Ensure the index file exists"""
        if not self.index_path.exists():
            self._save_index([])
    
    def _load_index(self) -> List[Dict]:
        """Load the knowledge base index"""
        try:
            with open(self.index_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading index: {e}")
            return []
    
    def _save_index(self, index: List[Dict]):
        """Save the knowledge base index"""
        try:
            with open(self.index_path, 'w', encoding='utf-8') as f:
                json.dump(index, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving index: {e}")
    
    def _generate_id(self) -> str:
        """Generate a unique ID for a knowledge entry"""
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')
        return f"kb_{timestamp}"
    
    def _extract_tags(self, query: str, summary: str) -> List[str]:
        """
        Extract relevant tags from query and summary
        
        Args:
            query: The research query
            summary: The research summary
            
        Returns:
            List of relevant tags
        """
        # Logistics-specific keywords
        logistics_keywords = {
            'supply chain', 'logistics', 'warehouse', 'transportation', 'freight',
            'shipping', 'delivery', 'inventory', 'last mile', 'distribution',
            'fulfillment', 'cargo', 'fleet', 'routing', 'optimization',
            'automation', 'robotics', 'ai', 'ml', 'blockchain', 'iot',
            'sustainability', 'green logistics', 'reverse logistics',
            'cold chain', 'cross-docking', 'dropshipping', '3pl', '4pl',
            'wms', 'tms', 'erp', 'saas', 'cloud', 'real-time tracking',
            'route optimization', 'demand forecasting', 'capacity planning'
        }
        
        text = (query + " " + summary).lower()
        
        # Find matching keywords
        tags = []
        for keyword in logistics_keywords:
            if keyword in text:
                # Convert to tag format
                tag = keyword.replace(' ', '_')
                tags.append(tag)
        
        # Always include a general tag
        if not tags:
            tags.append('logistics')
        
        # Limit to top 5 most relevant
        return list(set(tags))[:5]
    
    def save_research(
        self,
        query: str,
        summary: str,
        full_report: str,
        sources: List[Dict],
        key_findings: List[str]
    ) -> str:
        """
        Save research results to the knowledge base
        
        Args:
            query: The research query
            summary: Executive summary
            full_report: Complete research report
            sources: List of sources consulted
            key_findings: Key findings from research
            
        Returns:
            The ID of the saved entry
        """
        try:
            # Generate entry ID
            entry_id = self._generate_id()
            timestamp = datetime.utcnow().isoformat()
            
            # Extract tags
            tags = self._extract_tags(query, summary)
            
            # Create entry data
            entry_data = {
                "id": entry_id,
                "query": query,
                "summary": summary,
                "key_findings": key_findings,
                "sources": sources,
                "tags": tags,
                "timestamp": timestamp,
                "full_report_file": f"{entry_id}_report.txt"
            }
            
            # Save full report to text file
            report_path = self.entries_path / f"{entry_id}_report.txt"
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(f"LOGISTICS RESEARCH REPORT\n")
                f.write(f"{'='*80}\n\n")
                f.write(f"Query: {query}\n")
                f.write(f"Date: {timestamp}\n")
                f.write(f"Research ID: {entry_id}\n")
                f.write(f"\n{'='*80}\n\n")
                f.write(full_report)
                f.write(f"\n\n{'='*80}\n")
                f.write(f"END OF REPORT\n")
            
            # Save metadata to JSON
            metadata_path = self.entries_path / f"{entry_id}_meta.json"
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(entry_data, f, indent=2, ensure_ascii=False)
            
            # Update index
            index = self._load_index()
            index.insert(0, {
                "id": entry_id,
                "query": query,
                "summary": summary[:200] + "..." if len(summary) > 200 else summary,
                "tags": tags,
                "timestamp": timestamp
            })
            self._save_index(index)
            
            print(f"✓ Research saved to knowledge base: {entry_id}")
            return entry_id
            
        except Exception as e:
            print(f"Error saving research: {e}")
            raise
    
    def get_entry(self, entry_id: str) -> Optional[Dict]:
        """
        Retrieve a specific knowledge entry
        
        Args:
            entry_id: The entry ID
            
        Returns:
            Entry data or None if not found
        """
        try:
            metadata_path = self.entries_path / f"{entry_id}_meta.json"
            report_path = self.entries_path / f"{entry_id}_report.txt"
            
            if not metadata_path.exists():
                return None
            
            # Load metadata
            with open(metadata_path, 'r', encoding='utf-8') as f:
                entry_data = json.load(f)
            
            # Load full report
            if report_path.exists():
                with open(report_path, 'r', encoding='utf-8') as f:
                    entry_data['full_report'] = f.read()
            
            return entry_data
            
        except Exception as e:
            print(f"Error retrieving entry: {e}")
            return None
    
    def list_entries(
        self,
        limit: int = 20,
        tag: Optional[str] = None
    ) -> List[Dict]:
        """
        List knowledge base entries
        
        Args:
            limit: Maximum number of entries to return
            tag: Optional tag filter
            
        Returns:
            List of entry summaries
        """
        try:
            index = self._load_index()
            
            # Filter by tag if specified
            if tag:
                index = [entry for entry in index if tag in entry.get('tags', [])]
            
            # Return limited results
            return index[:limit]
            
        except Exception as e:
            print(f"Error listing entries: {e}")
            return []
    
    def delete_entry(self, entry_id: str) -> bool:
        """
        Delete a knowledge entry
        
        Args:
            entry_id: The entry ID to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            metadata_path = self.entries_path / f"{entry_id}_meta.json"
            report_path = self.entries_path / f"{entry_id}_report.txt"
            
            if not metadata_path.exists():
                return False
            
            # Delete files
            metadata_path.unlink(missing_ok=True)
            report_path.unlink(missing_ok=True)
            
            # Update index
            index = self._load_index()
            index = [entry for entry in index if entry['id'] != entry_id]
            self._save_index(index)
            
            return True
            
        except Exception as e:
            print(f"Error deleting entry: {e}")
            return False
    
    def search_entries(self, search_query: str, limit: int = 10) -> List[Dict]:
        """
        Search knowledge base entries
        
        Args:
            search_query: Search terms
            limit: Maximum results to return
            
        Returns:
            List of matching entries
        """
        try:
            index = self._load_index()
            search_lower = search_query.lower()
            
            # Simple text search
            matches = []
            for entry in index:
                query_text = entry.get('query', '').lower()
                summary_text = entry.get('summary', '').lower()
                tags_text = ' '.join(entry.get('tags', [])).lower()
                
                if (search_lower in query_text or 
                    search_lower in summary_text or 
                    search_lower in tags_text):
                    matches.append(entry)
            
            return matches[:limit]
            
        except Exception as e:
            print(f"Error searching entries: {e}")
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get knowledge base statistics
        
        Returns:
            Dictionary with statistics
        """
        try:
            index = self._load_index()
            
            # Count tags
            tag_counts = {}
            for entry in index:
                for tag in entry.get('tags', []):
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1
            
            # Get top tags
            top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            
            return {
                "total_entries": len(index),
                "total_tags": len(tag_counts),
                "top_tags": [{"tag": tag, "count": count} for tag, count in top_tags],
                "last_updated": index[0]['timestamp'] if index else None
            }
            
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {
                "total_entries": 0,
                "total_tags": 0,
                "top_tags": [],
                "last_updated": None
            }
