# 🤖 YuktiAI 
    - Intelligent AI Assistant


<div align="center">

![YuktiAI](https://img.shields.io/badge/YuktiAI-v1.0.0-blue?style=for-the-badge&logo=robot)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![Ollama](https://img.shields.io/badge/Ollama-LLaMA_3.2-orange?style=for-the-badge)

**Your Intelligent AI Assistant - No External Redirections**

</div>


## 🎯 Overview

**YuktiAI** is a powerful, standalone AI assistant that provides comprehensive answers across multiple domains without external redirections. Built with **LLaMA 3.2** and **Ollama**, it offers a ChatGPT-like experience that runs entirely offline on your local machine.


## ✨ Features

- 🔒 **Complete Privacy** - Runs entirely offline
- 💡 **Multi-Domain Expertise** - Coding, business, academics, science
- 🧠 **Conversation Memory** - Maintains context across interactions
- 🎨 **Dual Interface** - Streamlit web app + HTML interface
- ⚡ **Fast & Efficient** - Optimized for local deployment
- 🚫 **No External Dependencies** - Never redirects to other services


## 🛠️ Quick Setup

### 1. Install Dependencies
```
pip install streamlit requests python-dotenv
```

### 2. Install Ollama
```
# Visit: https://ollama.com/download
ollama serve
ollama pull llama3.2:3b
```

### 3. Initialize YuktiAI
```
python init.py
```

### 4. Launch Interface
```
# Streamlit Interface
streamlit run app.py

# OR HTML Interface
python server.py
```


## 📁 Project Structure

```
YuktiAI/
├── 📄 init.py              # Complete system (all components)
├── 📄 app.py               # Streamlit interface
├── 📄 server.py            # HTTP server
├── 📄 index.html           # HTML interface
├── 📄 script.js            # JavaScript functionality
├── 📄 style.css            # Styling
├── 📄 .env                 # Configuration
├── 📄 requirements.txt     # Dependencies
└── 📄 README.md            # This file
```


## 🚀 Usage

1. **Start Ollama**: `ollama serve`
2. **Initialize**: Click "Initialize YuktiAI" in the interface
3. **Chat**: Start asking questions across any domain!

### Example Queries
```
💻 "Write a Python function for sorting algorithms"
📚 "Explain machine learning in simple terms"
🔍 "Compare React vs Vue.js"
📝 "Create a step-by-step API guide"
```


## 🎨 Interfaces

### Streamlit Interface
- Modern web interface with chat history
- Real-time status indicators
- Settings panel and export functionality

### HTML Interface
- Lightweight web interface
- Direct Ollama API integration
- Mobile-responsive design


## ⚙️ Configuration

Edit `.env` file:
```
ASSISTANT_NAME=YuktiAI
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
TEMPERATURE=0.7
MEMORY_SIZE=10
```


## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Ollama not running" | Run `ollama serve` |
| "Model not available" | Run `ollama pull llama3.2:3b` |
| Import errors | Run `python init.py` again |


## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request


## 📄 License

This project is licensed under the MIT License.


## 👥 Author

**Harsh Raj**

---

<div align="center">

**Made with ❤️ for intelligent conversations**

*Empowering AI without compromising privacy*

</div>
```


The document is concise yet comprehensive, perfect for developers who want to quickly understand and deploy YuktiAI! 🚀
