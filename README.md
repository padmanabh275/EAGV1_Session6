# Cognitive Agent Framework

A modular agent system implementing four cognitive layers: Perception, Memory, Decision-Making, and Action. The system uses user preferences to provide personalized responses and actions.

## Project Structure

```
.
├── perception.py      # Perception layer (LLM-based input processing)
├── memory.py         # Memory layer (context and history management)
├── decision_making.py # Decision-making layer (reasoning and action selection)
├── action.py         # Action layer (execution of decisions)
├── main.py           # Main agent implementation
├── app.py            # Streamlit web interface
└── requirements.txt  # Project dependencies
```

## Features

- Four-layer cognitive architecture
- User preference-based personalization
- Asynchronous processing
- Type-safe with Pydantic models
- Transparent reasoning chain
- Confidence scoring
- Memory management
- Action execution tracking
- Powered by Google's Gemini 2.0 Flash
- Interactive web interface with Streamlit
- Real-time analytics and visualizations

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

## Usage

### Command Line Interface
Run the agent:
```bash
python main.py
```

### Web Interface
Run the Streamlit app:
```bash
streamlit run app.py
```

The web interface provides:
1. User preference setup
2. Interactive chat interface
3. Confidence visualization
4. Reasoning chain display
5. Response analytics
6. Real-time performance metrics

## Cognitive Layers

### 1. Perception Layer
- Processes input using Google's Gemini 2.0 Flash
- Incorporates user preferences
- Provides confidence scores
- Outputs structured responses

### 2. Memory Layer
- Stores and retrieves context
- Manages memory importance
- Provides relevant historical context
- Maintains memory limits

### 3. Decision-Making Layer
- Evaluates possible actions
- Generates reasoning chains
- Calculates confidence scores
- Selects optimal actions

### 4. Action Layer
- Executes selected actions
- Handles different action types
- Provides execution results
- Tracks execution time

## Web Interface Features

### User Preferences
- Interactive form for setting preferences
- Easy preference management
- Reset functionality

### Chat Interface
- Real-time chat display
- Message history
- Confidence meters
- Expandable reasoning chains

### Analytics
- Response time tracking
- Confidence visualization
- Model information
- Performance metrics

## Models

### UserPreferences
```python
class UserPreferences(BaseModel):
    likes: List[str]
    location: str
    favorite_topics: List[str]
    additional_context: Dict[str, Any]
```

### AgentResponse
```python
class AgentResponse(BaseModel):
    output: Any
    confidence: float
    reasoning_chain: list[str]
    execution_time: float
```

## Action Types

The agent can perform the following actions:
- RESPOND: Generate responses
- SEARCH: Search for information
- CALCULATE: Perform calculations
- CREATE: Create new items
- MODIFY: Modify existing items
- DELETE: Delete items

## Error Handling

The system includes comprehensive error handling:
- Input validation
- Action execution errors
- Memory management errors
- Preference validation
- API error handling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License 