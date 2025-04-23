from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from decision_making import ActionType, Decision
import asyncio

class ActionResult(BaseModel):
    """Model for action execution result"""
    success: bool
    output: Any
    error: Optional[str] = None
    execution_time: float = Field(ge=0.0)
    model: str = "gemini-2.0-flash"

class ActionLayer:
    def __init__(self):
        self.action_handlers = {
            ActionType.RESPOND: self._handle_respond,
            ActionType.SEARCH: self._handle_search,
            ActionType.CALCULATE: self._handle_calculate,
            ActionType.CREATE: self._handle_create,
            ActionType.MODIFY: self._handle_modify,
            ActionType.DELETE: self._handle_delete
        }
        self.model = "gemini-2.0-flash"

    async def execute_action(self, decision: Decision) -> ActionResult:
        """Execute a decision and return the result"""
        start_time = asyncio.get_event_loop().time()
        
        try:
            if decision.action_type not in self.action_handlers:
                raise ValueError(f"Unknown action type: {decision.action_type}")

            handler = self.action_handlers[decision.action_type]
            output = await handler(decision.parameters)
            
            execution_time = asyncio.get_event_loop().time() - start_time
            
            return ActionResult(
                success=True,
                output=output,
                execution_time=execution_time,
                model=self.model
            )
            
        except Exception as e:
            execution_time = asyncio.get_event_loop().time() - start_time
            return ActionResult(
                success=False,
                output=None,
                error=str(e),
                execution_time=execution_time,
                model=self.model
            )

    async def _handle_respond(self, parameters: Dict[str, Any]) -> str:
        """Handle respond action"""
        context = parameters.get("context", {})
        model = parameters.get("model", "gemini-2.0-flash")
        return f"[{model}] Responding to context: {context}"

    async def _handle_search(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle search action"""
        query = parameters.get("query", "")
        model = parameters.get("model", "gemini-2.0-flash")
        return {"results": f"[{model}] Search results for: {query}"}

    async def _handle_calculate(self, parameters: Dict[str, Any]) -> float:
        """Handle calculate action"""
        expression = parameters.get("expression", "0")
        model = parameters.get("model", "gemini-2.0-flash")
        result = eval(expression)  # In production, use a safer evaluation method
        return float(f"[{model}] {result}")

    async def _handle_create(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle create action"""
        item_type = parameters.get("type", "unknown")
        model = parameters.get("model", "gemini-2.0-flash")
        return {"status": f"[{model}] created", "type": item_type}

    async def _handle_modify(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle modify action"""
        item_id = parameters.get("id", "unknown")
        model = parameters.get("model", "gemini-2.0-flash")
        return {"status": f"[{model}] modified", "id": item_id}

    async def _handle_delete(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle delete action"""
        item_id = parameters.get("id", "unknown")
        model = parameters.get("model", "gemini-2.0-flash")
        return {"status": f"[{model}] deleted", "id": item_id} 