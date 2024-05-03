# Python RAG Chatbot README

This repository contains a Python script for a chatbot application built using Python and customtkinter. The chatbot is designed to interact with users and provide responses based on the given context.

Here is how it looks:
![image](https://github.com/Ytalow/chatbot-python/assets/17263832/ceaf3bd2-7478-404a-9e50-a58309adc868)


## Features

- **Interactive Interface**: The chatbot provides an interactive interface for users to communicate with.
- **Contextual Responses**: Responses are generated based on the given context and conversation history.
- **PDF to Text Conversion**: Ability to convert PDF files to text for contextualization purposes.

## Requirements

- Python 3.x
- customtkinter
- dotenv
- langchain
- langchain_anthropic
- langchain_voyageai
- langsmith
- PyPDF2

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Ytalow/chatbot-python.git
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your `.env` file with the following variables:

```
LANGCHAIN_TRACING_V2=true
VOYAGE_API_KEY=your_voyage_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
LANGCHAIN_API_KEY=your_langchain_api_key
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
```

Replace `your_voyage_api_key`, `your_anthropic_api_key`, and `your_langchain_api_key` with your respective API keys.

If you need, you can sign up for them individually with the links below:

- [VoyageAI](https://voyageai.com)
- [Anthropic](https://console.anthropic.com)
- [Langchain](https://smith.langchain.com)

## Usage

1. Run the Python script:

```bash
python chatbot.py
```

2. Use the provided interface to interact with the chatbot:
   - Input your message in the entry field.
   - Press "Enter" or click the "Enter" button to submit your message.
   - The chatbot will respond accordingly based on the context and conversation history.

## Additional Notes

- Ensure that all dependencies are properly installed before running the script.
- Make sure to have the necessary permissions to access and convert PDF files if using the PDF to text conversion feature.

Feel free to customize and extend the functionality of the chatbot according to your requirements! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

