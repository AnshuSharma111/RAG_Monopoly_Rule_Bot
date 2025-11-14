# **RAG Monopoly Rule Bot**
This is a command-line chatbot that can answer queries regarding the rules of Monopoly board game. It implements RAG using the [official monopoly rulebook pdf](https://instructions.hasbro.com/api/download/C1009_en-gb_monopoly-game.pdf) as source text. The process followed is as follows:

1. **Data Source** : Official Monopoly Rulebook by Hasbro Brothers.
2. **Data Extraction** : As you may be able to observe, the pdf is not plaintext. It needs to be converted to text to be fed into a database. Since there is no apparent LaTeX structure to the file, I use OCR to extract, as best as it can, text from the PDF.
3. **Vector Database** : A large corpus of text requires it be stored in a vector database so that relevant information for the given prompt can be extracted quickly and correctly. For this effort, I employ ChromaDB as a fast and reliable database that embeds and stores data that has been divided into semantic chunks (by page and headings) This information is used to augment the user prompt to the LLM for better results.
4. **Generation** : The augmented prompt is sent to the LLM, which in this case is Gemini for no particular reason other than convenience.

The application is *CLI-based* because of the simple fact that it was built as an exercise in Retrieval Augmented Generation, not interface development.

---
# **Setup**

To run, follow the given steps:

1. Install the required libraries using "pip install lib_name":
  - pytesseract
  - chromadb
  - pdf2image
  - langchain
  - hashlib
  - sentence_transformers
2. Pytesseract and pdf2image reuire installation of software on the system that is used by their libraries. Please follow the guides here [pytesseract](https://pypi.org/project/pytesseract/) and here pdf2image(https://pdf2image.readthedocs.io/en/latest/installation.html) to install and set them up respectively.
3. Next, you will need a .env file with a key GEMINI_API_KEY and its value equal to your Gemini API key, which you can obtain [here](https://aistudio.google.com/apikey)
4. You are ready to go! **Run the file chatbot.py** and enjoy!

---
#**Remark**

The bot has a clear edge over generalised LLMs like ChatGPT and Gemini for questions that require specific game knowledge. For instance, the question

> How is money distributed to each player at the start of a game?

distinguishes the power of RAG from general Chatbots.
For any queries, contact me at anshu045sharma@gmail.com
