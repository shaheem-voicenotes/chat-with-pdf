
from PyPDF2 import PdfReader 
from chunkipy import TextChunker, TokenEstimator
import chromadb
from transformers import AutoTokenizer
from decouple import config

together_api_key = config("TOGETHER_KEY")
collection_name = config("COLLECTION_NAME")
db_path = config("DB_PATH")

class BertTokenEstimator(TokenEstimator):
    def __init__(self):
        self.bert_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

    def estimate_tokens(self, text):
        return len(self.bert_tokenizer.encode(text))

chroma_client = chromadb.PersistentClient(path=db_path)
collection = chroma_client.create_collection(name=collection_name)
  
# creating a pdf reader object 
reader = PdfReader('book.pdf') 
  
# printing number of pages in pdf file 
print(len(reader.pages)) 
  
# get full text
text = ""

for page in reader.pages:
    text += page.extract_text()


bert_token_estimator = BertTokenEstimator()

print(f"Num of chars: {len(text)}")


text_chunker = TextChunker(512, tokens=True, token_estimator=BertTokenEstimator())
chunks = text_chunker.chunk(text)

for i, chunk in enumerate(chunks):
    collection.add(
      documents=[chunk],
      ids=[f"chunk_{i}"]
    )