import chromadb
from utils.api import chat
from decouple import config

together_api_key = config("TOGETHER_KEY")
collection_name = config("COLLECTION_NAME")
db_path = config("DB_PATH")

chroma_client = chromadb.PersistentClient(path=db_path)
collection = chroma_client.get_collection(name=collection_name)

print("\nEnter your questions. Press 'q' to quit.\n")

while True:
    question = input("Ask a question: ")

    if question.lower() == 'q':
        break

    result = collection.query(query_texts=[question], n_results=3)
    resultStr = result["documents"][0]

    prompt = f"""
    You are a helpful AI assitant. 
    You need to provide a response to a question asked by a user in very summarized way,
    within maximum of 3 lines.
    Here are some context from a book that you will use to generate a response: {resultStr}
    The user asks: "{question}" You respond:
    """

    chat_result = chat(prompt, together_api_key)

    print("\nPDF Answer: ", chat_result, "\n\n")