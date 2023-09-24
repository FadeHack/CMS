

from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
from llama_index import StorageContext, load_index_from_storage

documents = SimpleDirectoryReader('/home/mozart/yos/CMS/backend/chatbot/chatbot_data').load_data()

index = GPTVectorStoreIndex.from_documents(documents)
index.storage_context.persist('/home/mozart/yos/CMS/backend/chatbot')

