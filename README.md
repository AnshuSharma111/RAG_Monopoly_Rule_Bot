# RAG_Monopoly_Rule_Bot
Implementing a chatbot that can answer queries regarding the rules of Monopoly and other board games.

To run, follow the given steps:

1) Install the required libraries using "pip install lib_name":
  a. pytesseract
  b. chromadb
  c. pdf2image
  d. langchain
  e. hashlib
  f. sentence_transformers
2) Pytesseract and pdf2image reuire installation of software on the system that is used by their libraries. Please follow the guides here [https://pypi.org/project/pytesseract/] and here [https://pdf2image.readthedocs.io/en/latest/installation.html] to install and set them up respectively.
3) Next, you will need a .env file with a key GEMINI_API_KEY and its value equal to your Gemini API key, which you can obtain here [https://aistudio.google.com/apikey]
4) You are ready to go! Run the file chatbot.py and enjoy!
