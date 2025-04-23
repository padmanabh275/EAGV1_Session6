import streamlit as st
import asyncio
import plotly.graph_objects as go
import pandas as pd
from main import CognitiveAgent, UserPreferences
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Cognitive Agent Interface",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .response-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .confidence-meter {
        height: 20px;
        background-color: #e0e0e0;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .confidence-fill {
        height: 100%;
        background-color: #4CAF50;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'preferences_set' not in st.session_state:
    st.session_state.preferences_set = False

def display_confidence_meter(confidence):
    """Display a confidence meter"""
    st.markdown(f"""
    <div class="confidence-meter">
        <div class="confidence-fill" style="width: {confidence*100}%"></div>
    </div>
    <p style="text-align: center;">Confidence: {confidence:.2%}</p>
    """, unsafe_allow_html=True)

def display_reasoning_chain(chain):
    """Display the reasoning chain"""
    with st.expander("Reasoning Chain", expanded=True):
        for i, step in enumerate(chain, 1):
            st.markdown(f"**Step {i}:** {step}")

def display_chat_message(role, content, confidence=None, reasoning=None):
    """Display a chat message with optional confidence and reasoning"""
    with st.chat_message(role):
        # Main content
        st.markdown("### Response")
        st.markdown(content)
        
        if confidence is not None:
            st.markdown("---")
            st.markdown("### Confidence Score")
            display_confidence_meter(confidence)
            
        if reasoning is not None:
            st.markdown("---")
            st.markdown("### Reasoning Process")
            with st.expander("View Detailed Reasoning", expanded=False):
                for i, step in enumerate(reasoning, 1):
                    st.markdown(f"""
                    <div style="padding: 5px 0;">
                        <strong>Step {i}:</strong> {step}
                    </div>
                    """, unsafe_allow_html=True)

def main():
    st.title("🤖 Cognitive Agent Interface")
    st.markdown("---")

    # Sidebar for preferences
    with st.sidebar:
        st.header("User Preferences")
        
        if not st.session_state.preferences_set:
            with st.form("preferences_form"):
                st.subheader("Tell me about yourself")
                likes = st.text_input("Your interests (comma-separated)")
                location = st.text_input("Your location")
                favorite_topics = st.text_input("Your favorite topics (comma-separated)")
                
                if st.form_submit_button("Set Preferences"):
                    if likes and location and favorite_topics:
                        preferences = UserPreferences(
                            likes=[like.strip() for like in likes.split(",")],
                            location=location.strip(),
                            favorite_topics=[topic.strip() for topic in favorite_topics.split(",")]
                        )
                        
                        # Initialize agent with preferences
                        st.session_state.agent = CognitiveAgent()
                        asyncio.run(st.session_state.agent.set_user_preferences(preferences))
                        st.session_state.preferences_set = True
                        st.success("Preferences set successfully!")
                    else:
                        st.error("Please fill in all fields")
        else:
            st.success("Preferences are set!")
            if st.button("Reset Preferences"):
                st.session_state.preferences_set = False
                st.session_state.agent = None
                st.session_state.chat_history = []
                st.rerun()

    # Main chat interface
    if st.session_state.preferences_set:
        # Display chat history
        for message in st.session_state.chat_history:
            display_chat_message(
                message["role"],
                message["content"],
                message.get("confidence"),
                message.get("reasoning")
            )

        # Chat input
        if prompt := st.chat_input("Type your message here..."):
            # Add user message to chat
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            display_chat_message("user", prompt)

            # Get agent response
            response = asyncio.run(st.session_state.agent.process(prompt))
            
            # Add agent response to chat
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response.output,
                "confidence": response.confidence,
                "reasoning": response.reasoning_chain
            })
            
            # Display agent response
            display_chat_message(
                "assistant",
                response.output,
                response.confidence,
                response.reasoning_chain
            )

            # Analytics section
            st.markdown("---")
            st.markdown("### Response Analytics")
            
            # Create two columns for metrics
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Response Time", f"{response.execution_time:.2f}s")
            with col2:
                st.metric("Model Used", response.model_used)

            # Confidence over time visualization
            st.markdown("#### Confidence Trend")
            confidence_data = pd.DataFrame({
                'Time': [datetime.now()],
                'Confidence': [response.confidence]
            })
            fig = go.Figure(data=go.Scatter(
                x=confidence_data['Time'],
                y=confidence_data['Confidence'],
                mode='lines+markers',
                line=dict(color='#4CAF50', width=2),
                marker=dict(size=8, color='#4CAF50')
            ))
            fig.update_layout(
                title="Confidence Over Time",
                xaxis_title="Time",
                yaxis_title="Confidence",
                yaxis_range=[0, 1],
                plot_bgcolor='white',
                paper_bgcolor='white'
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Please set your preferences in the sidebar to start chatting!")

if __name__ == "__main__":
    main() 