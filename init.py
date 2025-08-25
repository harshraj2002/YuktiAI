#!/usr/bin/env python3
"""
YuktiAI
Author: Harsh Raj
Version: 1.0.0
"""

import sys
import os
from pathlib import Path
import logging
import json
from datetime import datetime

# =============================================================================
# PROJECT METADATA
# =============================================================================

__version__ = "1.0.0"
__author__ = "Harsh Raj"
__description__ = "Intelligent AI Assistant"

# =============================================================================
# COMPLETE YUKTI SYSTEM
# =============================================================================

class YuktiSystem:
    """Complete YuktiAI system in a single class"""
    
    def __init__(self):
        self.setup_paths()
        self.setup_logging()
        self.config = None
        self.ollama_handler = None
        self.memory_handler = None
        self.response_formatter = None
        self.chat_pipeline = None
        
    def setup_paths(self):
        """Setup all paths"""
        self.YUKTI_ROOT = Path(__file__).parent.absolute()
        
        #Add to Python path
        if str(self.YUKTI_ROOT) not in sys.path:
            sys.path.insert(0, str(self.YUKTI_ROOT))
        
        #Create directories
        self.create_directories()
    
    def create_directories(self):
        """Create necessary directories"""
        directories = ['config', 'models', 'utils', 'data', 'web', 'logs', 'exports']
        
        for directory in directories:
            (self.YUKTI_ROOT / directory).mkdir(exist_ok=True)
    
    def setup_logging(self):
        """Setup Windows-compatible logging"""
        log_file = self.YUKTI_ROOT / 'logs' / 'yukti.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger('YuktiAI')

# =============================================================================
# EMBEDDED CONFIGURATION
# =============================================================================

class YuktiConfig:
    """Embedded YuktiAI Configuration"""
    
    PROJECT_NAME = "YuktiAI"
    VERSION = "1.0.0"
    ASSISTANT_NAME = "YuktiAI"
    
    #Ollama Configuration
    OLLAMA_HOST = "http://localhost:11434"
    OLLAMA_MODEL = "llama3.2:3b"
    
    #Response Configuration
    MAX_RESPONSE_LENGTH = 1000
    TEMPERATURE = 0.7
    MEMORY_SIZE = 10
    
    #System Prompt
    SYSTEM_PROMPT = """You are YuktiAI, an intelligent and helpful AI assistant.

CORE PRINCIPLES:
- Provide accurate, well-structured, and professional responses
- Use clear formatting with bullets, numbers, or sections when appropriate
- Never redirect users to external websites, search engines, or other tools
- Give complete answers based on your knowledge
- If uncertain, acknowledge limitations honestly
- Maintain a helpful and professional tone

Remember: You are YuktiAI - a standalone AI assistant that provides comprehensive answers without external redirections."""
    
    @classmethod
    def get_config_dict(cls):
        return {
            "project_name": cls.PROJECT_NAME,
            "version": cls.VERSION,
            "assistant_name": cls.ASSISTANT_NAME,
            "ollama_host": cls.OLLAMA_HOST,
            "ollama_model": cls.OLLAMA_MODEL,
            "max_response_length": cls.MAX_RESPONSE_LENGTH,
            "temperature": cls.TEMPERATURE,
            "memory_size": cls.MEMORY_SIZE
        }

# =============================================================================
# EMBEDDED OLLAMA HANDLER
# =============================================================================

class YuktiOllamaHandler:
    """Embedded Ollama handler"""
    
    def __init__(self, config):
        self.config = config
        self.base_url = config.OLLAMA_HOST
        self.model = config.OLLAMA_MODEL
        
        #Import requests here to avoid dependency issues
        try:
            import requests
            self.requests = requests
            self.session = requests.Session()
        except ImportError:
            self.requests = None
            self.session = None
            print("[ERROR] requests module not available")
    
    def check_ollama_status(self) -> bool:
        """Check if Ollama is running"""
        if not self.requests:
            return False
            
        try:
            response = self.session.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    def check_model_availability(self) -> bool:
        """Check if model is available"""
        if not self.requests:
            return False
            
        try:
            response = self.session.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                available_models = [model["name"] for model in models]
                return self.model in available_models
            return False
        except Exception:
            return False
    
    def generate_response(self, prompt: str) -> str:
        """Generate response using Ollama"""
        if not self.requests:
            return "Error: requests module not available"
            
        try:
            data = {
                "model": self.model,
                "prompt": prompt,
                "system": self.config.SYSTEM_PROMPT,
                "stream": False,
                "options": {
                    "temperature": self.config.TEMPERATURE,
                    "num_predict": self.config.MAX_RESPONSE_LENGTH
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/api/generate",
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
            else:
                return "Sorry, I encountered an error while generating the response."
                
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"

# =============================================================================
# EMBEDDED MEMORY HANDLER
# =============================================================================

class YuktiMemoryHandler:
    """Embedded memory handler"""
    
    def __init__(self, config):
        self.config = config
        self.max_memory = config.MEMORY_SIZE
        self.conversations = []
    
    def add_conversation(self, user_input: str, ai_response: str):
        """Add conversation to memory"""
        conversation = {
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "assistant": ai_response
        }
        
        self.conversations.append(conversation)
        
        if len(self.conversations) > self.max_memory:
            self.conversations = self.conversations[-self.max_memory:]
    
    def get_recent_context(self, num_recent: int = 3) -> str:
        """Get recent conversation context"""
        if not self.conversations:
            return ""
        
        recent_conversations = self.conversations[-num_recent:]
        context_parts = []
        
        for conv in recent_conversations:
            context_parts.append(f"Previous Q: {conv['user']}")
            context_parts.append(f"Previous A: {conv['assistant'][:200]}...")
        
        return "\n".join(context_parts)
    
    def clear_memory(self):
        """Clear conversation memory"""
        self.conversations.clear()
    
    def get_memory_stats(self):
        """Get memory statistics"""
        total_conversations = len(self.conversations)
        return {
            "total_conversations": total_conversations,
            "max_memory": self.max_memory,
            "memory_usage_percent": (total_conversations / self.max_memory) * 100 if self.max_memory > 0 else 0
        }

# =============================================================================
# EMBEDDED RESPONSE FORMATTER
# =============================================================================

class YuktiResponseFormatter:
    """Embedded response formatter"""
    
    def __init__(self, config):
        self.config = config
        self.assistant_name = config.ASSISTANT_NAME
    
    def detect_query_type(self, user_input: str) -> str:
        """Detect query type"""
        input_lower = user_input.lower()
        
        if any(keyword in input_lower for keyword in ['code', 'program', 'function', 'python']):
            return "code"
        elif any(keyword in input_lower for keyword in ['how to', 'tutorial', 'steps']):
            return "tutorial"
        elif any(keyword in input_lower for keyword in ['explain', 'what is', 'why']):
            return "explanation"
        elif any(keyword in input_lower for keyword in ['list', 'examples', 'types']):
            return "list"
        elif any(keyword in input_lower for keyword in ['vs', 'compare', 'difference']):
            return "comparison"
        else:
            return "general"
    
    def format_response(self, response: str, query_type: str = "general") -> str:
        """Format response based on type"""
        if not response:
            return "I apologize, but I couldn't generate a response."
        
        #Clean response
        response = response.strip()
        
        #Add formatting based on type
        if query_type == "code" and ("def " in response or "class " in response):
            response = f"**Code Solution:**\n\n{response}"
        elif query_type == "tutorial":
            response = f"**Step-by-Step Guide:**\n\n{response}"
        elif query_type == "explanation":
            response = f"**{self.assistant_name} Explains:**\n\n{response}"
        elif query_type == "comparison":
            response = f"**Comparison Analysis:**\n\n{response}"
        
        #Ensure proper ending
        if response and not response.endswith(('.', '!', '?', ':')):
            response += '.'
        
        return response
    
    def format_final_response(self, response: str, user_input: str) -> str:
        """Apply final formatting"""
        query_type = self.detect_query_type(user_input)
        return self.format_response(response, query_type)

# =============================================================================
# EMBEDDED KNOWLEDGE BASE
# =============================================================================

class YuktiKnowledgeBase:
    """Embedded knowledge base"""
    
    def __init__(self):
        self.knowledge = {
            "greetings": [
                "Hello! I'm YuktiAI, your intelligent assistant. How can I help you today?",
                "Hi there! I'm YuktiAI. What would you like to know or discuss?",
                "Welcome! I'm YuktiAI, ready to assist you with any questions you have."
            ],
            "about_yukti": """**About YuktiAI:**

YuktiAI is an intelligent AI assistant that provides answers.

**Key Capabilities:**
• Answer questions across multiple domains
• Provide coding solutions and explanations
• Help with academic and business queries
• Maintain conversation context
• Format responses professionally

**Current Limitations:**
• Cannot browse the internet
• Cannot access external APIs
• Knowledge cutoff applies
• Cannot perform real-time data retrieval""",
            
            "capabilities": "I can help you with a wide range of topics including general knowledge, coding, business advice, academic questions, explanations, tutorials, and more. I provide detailed, well-formatted responses without redirecting you to external sources."
        }
    
    def get_random_greeting(self) -> str:
        """Get random greeting"""
        import random
        return random.choice(self.knowledge["greetings"])
    
    def search_knowledge(self, query: str) -> str:
        """Search knowledge base"""
        query_lower = query.lower()
        
        if any(keyword in query_lower for keyword in ["about", "what is yukti", "who are you"]):
            return self.knowledge["about_yukti"]
        elif any(keyword in query_lower for keyword in ["capabilities", "what can you do"]):
            return self.knowledge["capabilities"]
        
        return None

# =============================================================================
# EMBEDDED CHAT PIPELINE
# =============================================================================

class YuktiChatPipeline:
    """Embedded chat pipeline"""
    
    def __init__(self):
        self.config = YuktiConfig()
        self.ollama_handler = YuktiOllamaHandler(self.config)
        self.memory_handler = YuktiMemoryHandler(self.config)
        self.formatter = YuktiResponseFormatter(self.config)
        self.knowledge_base = YuktiKnowledgeBase()
        self.initialized = False
        
        #Setup logging
        self.logger = logging.getLogger('YuktiChatPipeline')
    
    def initialize_pipeline(self):
        """Initialize the pipeline"""
        try:
            self.logger.info("[INIT] Initializing YuktiAI chat pipeline...")
            
            #Check Ollama status
            if not self.ollama_handler.check_ollama_status():
                return {
                    "success": False,
                    "ollama_status": False,
                    "model_status": False,
                    "message": "Ollama is not running. Please start Ollama with: ollama serve"
                }
            
            #Check model availability
            if not self.ollama_handler.check_model_availability():
                return {
                    "success": False,
                    "ollama_status": True,
                    "model_status": False,
                    "message": f"Model {self.config.OLLAMA_MODEL} not available. Pull it with: ollama pull {self.config.OLLAMA_MODEL}"
                }
            
            self.initialized = True
            
            self.logger.info("[OK] YuktiAI pipeline initialized successfully!")
            
            return {
                "success": True,
                "ollama_status": True,
                "model_status": True,
                "message": "YuktiAI initialized successfully!",
                "details": {
                    "model": self.config.OLLAMA_MODEL,
                    "memory_size": self.config.MEMORY_SIZE
                }
            }
            
        except Exception as e:
            self.logger.error(f"[ERROR] Pipeline initialization failed: {e}")
            return {
                "success": False,
                "ollama_status": False,
                "model_status": False,
                "message": f"Initialization failed: {str(e)}"
            }
    
    def get_response(self, user_input: str) -> str:
        """Generate response"""
        if not self.initialized:
            return "[ERROR] YuktiAI is not properly initialized. Please check the setup."
        
        if not user_input or not user_input.strip():
            return "Please provide a question or message for me to respond to."
        
        try:
            #Check knowledge base first
            kb_response = self.knowledge_base.search_knowledge(user_input)
            if kb_response:
                self.memory_handler.add_conversation(user_input, kb_response)
                return kb_response
            
            #Get conversation context
            context = self.memory_handler.get_recent_context(num_recent=2)
            
            #Prepare prompt
            if context:
                full_prompt = f"Previous context:\n{context}\n\nCurrent question: {user_input.strip()}"
            else:
                full_prompt = user_input.strip()
            
            #Generate AI response
            raw_response = self.ollama_handler.generate_response(full_prompt)
            
            if not raw_response:
                return "I apologize, but I couldn't generate a response. Please try again."
            
            #Format response
            formatted_response = self.formatter.format_final_response(raw_response, user_input)
            
            #Add to memory
            self.memory_handler.add_conversation(user_input, formatted_response)
            
            return formatted_response
            
        except Exception as e:
            self.logger.error(f"[ERROR] Error generating response: {e}")
            return "I apologize, but I encountered an error while processing your request. Please try again."
    
    def clear_conversation(self):
        """Clear conversation memory"""
        self.memory_handler.clear_memory()
    
    def get_system_status(self):
        """Get system status"""
        ollama_status = self.ollama_handler.check_ollama_status()
        model_status = self.ollama_handler.check_model_availability() if ollama_status else False
        memory_stats = self.memory_handler.get_memory_stats()
        
        return {
            "initialized": self.initialized,
            "ollama_running": ollama_status,
            "model_available": model_status,
            "current_model": self.config.OLLAMA_MODEL,
            "memory_stats": memory_stats,
            "config": self.config.get_config_dict()
        }

# =============================================================================
# MAIN FUNCTIONS
# =============================================================================

def initialize_yukti():
    """Initialize YuktiAI system"""
    try:
        system = YuktiSystem()
        system.logger.info("[INIT] YuktiAI system initialized")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to initialize YuktiAI: {e}")
        return False

def create_chat_pipeline():
    """Create chat pipeline instance"""
    try:
        pipeline = YuktiChatPipeline()
        print("[OK] Chat pipeline created successfully")
        return pipeline
    except Exception as e:
        print(f"[ERROR] Failed to create chat pipeline: {e}")
        return None

def quick_setup():
    """Quick setup for YuktiAI"""
    print("YuktiAI Quick Setup")
    print("=" * 50)
    
    success = initialize_yukti()
    
    if success:
        return {
            'success': True,
            'message': 'YuktiAI setup completed successfully!'
        }
    else:
        return {
            'success': False,
            'message': 'YuktiAI setup failed. Please check the logs.'
        }

def main():
    """Main function"""
    print(f"""
YuktiAI Unified System
Version: {__version__}
Author: {__author__}
    """)
    
    result = quick_setup()
    
    if result['success']:
        print(f"\n[OK] {result['message']}")
        
        #Test pipeline creation
        print("\n[TEST] Testing chat pipeline creation...")
        pipeline = create_chat_pipeline()
        
        if pipeline:
            print("[OK] Chat pipeline test successful")
            
            print(f"\n{'='*60}")
            print("YuktiAI System Ready!")
            print("="*60)
            print("\nNext Steps:")
            print("1. Start Ollama: ollama serve")
            print("2. Pull model: ollama pull llama3.2:3b")
            print("3. Run Streamlit: streamlit run app.py")
            print("="*60)
        else:
            print("[ERROR] Chat pipeline test failed")
    else:
        print(f"\n[ERROR] {result['message']}")

#Export everything
__all__ = [
    '__version__',
    '__author__',
    '__description__',
    'YuktiChatPipeline',
    'YuktiConfig',
    'initialize_yukti',
    'create_chat_pipeline',
    'quick_setup',
    'main'
]

if __name__ == "__main__":
    main()
else:
    print(f"YuktiAI v{__version__} - Complete System Loaded")