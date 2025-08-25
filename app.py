import streamlit as st
import sys
from pathlib import Path

#Add current directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

#Import from fixed init
from init import create_chat_pipeline, YuktiKnowledgeBase

#Page configuration
st.set_page_config(
    page_title="YuktiAI",
    page_icon="🤖",
    layout="wide"
)

def main():
    st.title("🤖 YuktiAI")
    st.markdown("*Your standalone AI assistant*")
    
    #Initialize YuktiAI
    if 'yukti_initialized' not in st.session_state:
        
        with st.container():
            st.info("👋 Welcome to YuktiAI! Click the button below to start.")
            
            if st.button("🚀 Initialize YuktiAI", type="primary", use_container_width=True):
                
                with st.spinner("🔄 Initializing YuktiAI..."):
                    
                    try:
                        #Create chat pipeline
                        pipeline = create_chat_pipeline()
                        
                        if pipeline:
                            st.success("✅ Chat pipeline created successfully!")
                            
                            #Initialize the pipeline
                            init_result = pipeline.initialize_pipeline()
                            
                            if init_result["success"]:
                                st.session_state.yukti_initialized = True
                                st.session_state.pipeline = pipeline
                                st.session_state.knowledge_base = YuktiKnowledgeBase()
                                
                                st.success("🎉 YuktiAI initialized successfully!")
                                st.balloons()
                                st.rerun()
                                
                            else:
                                st.error(f"❌ Pipeline initialization failed:")
                                st.error(init_result['message'])
                                
                                #Show specific help based on the error
                                if not init_result.get("ollama_status", False):
                                    st.markdown("""
                                    **🔧 Ollama Setup Required:**
                                    
                                    1. **Install Ollama:** Visit https://ollama.com/download
                                    2. **Start Ollama:** Run `ollama serve` in terminal
                                    3. **Try again** by clicking Initialize
                                    """)
                                elif not init_result.get("model_status", False):
                                    st.markdown(f"""
                                    **📥 Model Download Required:**
                                    
                                    1. **Pull the model:** Run `ollama pull llama3.2:3b`
                                    2. **Wait for download** to complete
                                    3. **Try again** by clicking Initialize
                                    """)
                        else:
                            st.error("❌ Failed to create chat pipeline")
                            st.error("Please check that all dependencies are installed correctly.")
                            
                    except Exception as e:
                        st.error(f"❌ Unexpected error during initialization: {str(e)}")
        
        # Show setup instructions
        with st.expander("📋 Setup Instructions", expanded=True):
            st.markdown("""
            **Prerequisites:**
            
            1. **Install Ollama:**
               - Download from: https://ollama.com/download
               - Install for your operating system
            
            2. **Start Ollama Service:**
               ```
               ollama serve
               ```
            
            3. **Download Required Model:**
               ```
               ollama pull llama3.2:3b
               ```
            
            4. **Initialize YuktiAI:**
               - Click the "Initialize YuktiAI" button above
               - Wait for successful initialization
               - Start chatting!
            
            **Need Help?**
            - Make sure Ollama is running before initialization
            - Check that the model download completed successfully
            - Restart this app if you encounter issues
            """)
        
        return
    
    #Main chat interface
    if st.session_state.get('yukti_initialized', False):
        
        #Sidebar
        with st.sidebar:
            st.header("🎛️ YuktiAI Controls")
            
            #Status indicator
            status = st.session_state.pipeline.get_system_status()
            
            if status['ollama_running']:
                st.success("🟢 Ollama: Connected")
            else:
                st.error("🔴 Ollama: Disconnected")
            
            if status['model_available']:
                st.success(f"🤖 Model: {status['current_model']}")
            else:
                st.error("❌ Model: Not Available")
            
            st.markdown("---")
            
            #Controls
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.session_state.pipeline.clear_conversation()
                st.rerun()
            
            if st.button("🔄 Refresh Status", use_container_width=True):
                st.rerun()
            
            st.markdown("---")
            
            #Stats
            memory_stats = status.get('memory_stats', {})
            st.metric("💭 Conversations", memory_stats.get('total_conversations', 0))
            
            st.markdown("---")
            
            #About
            with st.expander("ℹ️ About YuktiAI"):
                st.markdown("""
                **YuktiAI Features:**
                • Comprehensive answers across domains
                • No external redirections
                • Conversation memory
                • Professional formatting
                • Offline operation with Ollama
                
                **Version:** 1.0.0
                **Model:** LLaMA 3.2-3B
                """)
        
        #Initialize chat history
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
            
            #Add welcome message
            welcome_msg = st.session_state.knowledge_base.get_random_greeting()
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": welcome_msg
            })
        
        #Display chat messages
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        #Chat input
        if prompt := st.chat_input("Ask YuktiAI anything...", key="chat_input"):
            
            #Add user message
            st.session_state.chat_history.append({
                "role": "user", 
                "content": prompt
            })
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            #Generate response
            with st.chat_message("assistant"):
                
                with st.spinner("🤔 YuktiAI is thinking..."):
                    try:
                        response = st.session_state.pipeline.get_response(prompt)
                        st.markdown(response)
                        
                        #Add to history
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": response
                        })
                        
                    except Exception as e:
                        error_msg = f"❌ Error generating response: {str(e)}"
                        st.error(error_msg)
                        
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": error_msg
                        })

if __name__ == "__main__":
    main()