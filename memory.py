from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class MemoryEntry(BaseModel):
    """Model for a single memory entry"""
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    importance: float = Field(ge=0.0, le=1.0, default=0.5)

class MemoryResponse(BaseModel):
    """Model for memory layer response"""
    relevant_memories: List[MemoryEntry]
    context_summary: str
    confidence_score: float = Field(ge=0.0, le=1.0)

class MemoryLayer:
    def __init__(self):
        self.memories: List[MemoryEntry] = []
        self.max_memories: int = 1000  # Maximum number of memories to store

    def add_memory(self, content: str, metadata: Optional[Dict[str, Any]] = None, importance: float = 0.5) -> None:
        """Add a new memory entry"""
        if metadata is None:
            metadata = {}
        
        new_memory = MemoryEntry(
            content=content,
            metadata=metadata,
            importance=importance
        )
        
        self.memories.append(new_memory)
        
        # Maintain memory limit
        if len(self.memories) > self.max_memories:
            self.memories = sorted(self.memories, key=lambda x: (x.importance, x.timestamp), reverse=True)
            self.memories = self.memories[:self.max_memories]

    def retrieve_relevant_memories(self, query: str, max_results: int = 5) -> MemoryResponse:
        """Retrieve memories relevant to the query"""
        # Sort memories by importance and recency
        sorted_memories = sorted(
            self.memories,
            key=lambda x: (x.importance, x.timestamp),
            reverse=True
        )
        
        # For now, return the most recent and important memories
        # In a real implementation, this would use semantic search
        relevant_memories = sorted_memories[:max_results]
        
        # Create a summary of the context
        context_summary = " ".join([mem.content for mem in relevant_memories])
        
        return MemoryResponse(
            relevant_memories=relevant_memories,
            context_summary=context_summary,
            confidence_score=0.8  # This could be calculated based on relevance
        )

    def clear_memories(self) -> None:
        """Clear all stored memories"""
        self.memories = [] 