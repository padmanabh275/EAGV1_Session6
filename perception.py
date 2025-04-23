from pydantic import BaseModel, Field
from typing import List, Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

class UserPreferences(BaseModel):
    """Model for storing user preferences and context"""
    likes: List[str] = Field(default_factory=list, description="User's interests and likes")
    location: str = Field(default="", description="User's location")
    favorite_topics: List[str] = Field(default_factory=list, description="User's favorite topics")
    additional_context: Dict[str, Any] = Field(default_factory=dict, description="Additional user context")

class PerceptionResponse(BaseModel):
    """Model for perception layer response"""
    processed_input: str
    context: Dict[str, Any]
    confidence_score: float = Field(ge=0.0, le=1.0)

class PerceptionLayer:
    def __init__(self):
        # Configure Gemini
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.user_preferences = None

    def set_user_preferences(self, preferences: UserPreferences):
        """Set user preferences for context-aware processing"""
        self.user_preferences = preferences

    async def process_input(self, input_text: str) -> PerceptionResponse:
        """Process input text with context from user preferences"""
        if not self.user_preferences:
            raise ValueError("User preferences not set. Call set_user_preferences first.")

        # Create context-aware prompt
        context_prompt = f"""
        User Context:
        - Location: {self.user_preferences.location}
        - Interests: {', '.join(self.user_preferences.likes)}
        - Favorite Topics: {', '.join(self.user_preferences.favorite_topics)}
        
        Input to process: {input_text}
        """

        try:
            # Generate response using Gemini Flash
            response = self.model.generate_content(
                context_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_p=0.8,
                    top_k=40,
                    max_output_tokens=2048,
                )
            )

            processed_text = response.text
            confidence = 0.9  # This could be calculated based on response properties

            return PerceptionResponse(
                processed_input=processed_text,
                context={"user_preferences": self.user_preferences.model_dump()},
                confidence_score=confidence
            )
        except Exception as e:
            raise Exception(f"Error in perception layer: {str(e)}") 