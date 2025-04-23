import asyncio
from typing import Dict, Any
from pydantic import BaseModel, Field
from perception import PerceptionLayer, UserPreferences
from memory import MemoryLayer
from decision_making import DecisionLayer, ActionType
from action import ActionLayer

class AgentResponse(BaseModel):
    """Model for agent's response"""
    output: Any
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning_chain: list[str]
    execution_time: float = Field(ge=0.0)
    model_used: str = "gemini-2.0-flash"

class CognitiveAgent:
    def __init__(self):
        self.perception = PerceptionLayer()
        self.memory = MemoryLayer()
        self.decision = DecisionLayer()
        self.action = ActionLayer()
        self.user_preferences = None

    async def set_user_preferences(self, preferences: UserPreferences) -> None:
        """Set user preferences and initialize the agent"""
        self.user_preferences = preferences
        self.perception.set_user_preferences(preferences)
        
        # Store initial context in memory
        self.memory.add_memory(
            "User preferences initialized with Gemini 2.0 Flash",
            {"preferences": preferences.model_dump(), "model": "gemini-2.0-flash"},
            importance=0.9
        )

    async def process(self, input_text: str) -> AgentResponse:
        """Process input through all cognitive layers"""
        start_time = asyncio.get_event_loop().time()

        # 1. Perception Layer
        perception_result = await self.perception.process_input(input_text)
        
        # 2. Memory Layer
        memory_result = self.memory.retrieve_relevant_memories(input_text)
        self.memory.add_memory(
            perception_result.processed_input,
            {
                "confidence": perception_result.confidence_score,
                "model": "gemini-2.0-flash"
            },
            importance=0.7
        )
        
        # 3. Decision Layer
        context = {
            "perception": perception_result.model_dump(),
            "memory": memory_result.model_dump(),
            "user_preferences": self.user_preferences.model_dump() if self.user_preferences else {},
            "model": "gemini-2.0-flash"
        }
        
        decision_result = self.decision.evaluate_options(
            context=context,
            available_actions=list(ActionType)
        )
        
        # 4. Action Layer
        action_result = await self.action.execute_action(decision_result.final_action)
        
        execution_time = asyncio.get_event_loop().time() - start_time
        
        return AgentResponse(
            output=action_result.output,
            confidence=decision_result.final_action.confidence,
            reasoning_chain=decision_result.reasoning_chain,
            execution_time=execution_time
        )

async def main():
    # Initialize the agent
    agent = CognitiveAgent()
    
    # Get user preferences
    print("Welcome! Let's get to know you better.")
    print("Please answer the following questions:")
    
    likes = input("What are your interests? (comma-separated): ").split(",")
    location = input("Where are you located? ")
    favorite_topics = input("What are your favorite topics? (comma-separated): ").split(",")
    
    preferences = UserPreferences(
        likes=[like.strip() for like in likes],
        location=location.strip(),
        favorite_topics=[topic.strip() for topic in favorite_topics]
    )
    
    await agent.set_user_preferences(preferences)
    
    print("\nGreat! I've got your preferences. How can I help you today?")
    print("(Using Gemini 2.0 Flash for fast and efficient responses)")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Goodbye!")
            break
            
        response = await agent.process(user_input)
        print(f"\nAgent: {response.output}")
        print(f"Confidence: {response.confidence:.2f}")
        print(f"Model: {response.model_used}")
        print("\nReasoning:")
        for step in response.reasoning_chain:
            print(f"- {step}")

if __name__ == "__main__":
    asyncio.run(main()) 