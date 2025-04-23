from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum

class ActionType(Enum):
    """Types of actions the agent can take"""
    RESPOND = "respond"
    SEARCH = "search"
    CALCULATE = "calculate"
    CREATE = "create"
    MODIFY = "modify"
    DELETE = "delete"

class Decision(BaseModel):
    """Model for a single decision"""
    action_type: ActionType
    parameters: Dict[str, Any]
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str
    model: str = "gemini-2.0-flash"

class DecisionResponse(BaseModel):
    """Model for decision layer response"""
    decisions: List[Decision]
    final_action: Decision
    reasoning_chain: List[str]
    model: str = "gemini-2.0-flash"

class DecisionLayer:
    def __init__(self):
        self.reasoning_chain: List[str] = []
        self.model = "gemini-2.0-flash"

    def add_reasoning_step(self, step: str) -> None:
        """Add a step to the reasoning chain"""
        self.reasoning_chain.append(f"[{self.model}] {step}")

    def evaluate_options(self, 
                        context: Dict[str, Any],
                        available_actions: List[ActionType],
                        constraints: Optional[Dict[str, Any]] = None) -> DecisionResponse:
        """Evaluate possible actions and make decisions"""
        if constraints is None:
            constraints = {}

        # Initialize decisions list
        decisions: List[Decision] = []

        # Evaluate each possible action
        for action in available_actions:
            confidence = self._calculate_confidence(action, context, constraints)
            reasoning = self._generate_reasoning(action, context)
            
            decision = Decision(
                action_type=action,
                parameters=self._get_action_parameters(action, context),
                confidence=confidence,
                reasoning=reasoning,
                model=self.model
            )
            
            decisions.append(decision)
            self.add_reasoning_step(f"Evaluated {action.value}: {reasoning}")

        # Select the best action based on confidence
        final_decision = max(decisions, key=lambda x: x.confidence)

        return DecisionResponse(
            decisions=decisions,
            final_action=final_decision,
            reasoning_chain=self.reasoning_chain,
            model=self.model
        )

    def _calculate_confidence(self, 
                            action: ActionType,
                            context: Dict[str, Any],
                            constraints: Dict[str, Any]) -> float:
        """Calculate confidence score for an action"""
        # This is a simplified confidence calculation
        # In a real implementation, this would be more sophisticated
        base_confidence = 0.5
        
        # Adjust confidence based on context
        if "user_preferences" in context:
            base_confidence += 0.2
            
        # Adjust confidence based on constraints
        if not constraints:
            base_confidence += 0.1
            
        # Adjust confidence based on model
        if context.get("model") == "gemini-2.0-flash":
            base_confidence += 0.1  # Slightly higher confidence for Flash model
            
        return min(base_confidence, 1.0)

    def _generate_reasoning(self, action: ActionType, context: Dict[str, Any]) -> str:
        """Generate reasoning for an action"""
        model_info = f"Using {context.get('model', 'gemini-2.0-flash')}"
        return f"{model_info}: Action {action.value} is appropriate given the context: {context}"

    def _get_action_parameters(self, action: ActionType, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get parameters for an action"""
        # This would be more sophisticated in a real implementation
        return {
            "context": context,
            "action_type": action.value,
            "model": context.get("model", "gemini-2.0-flash")
        } 