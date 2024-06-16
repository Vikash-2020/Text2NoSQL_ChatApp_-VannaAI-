# from llama_index.core import ServiceContext, StorageContext, load_index_from_storage
# from llama_index.llms.azure_openai import AzureOpenAI
# from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
# from llama_index.core.retrievers import VectorIndexRetriever
import os
from app_secrets import gpt3_azure_api_key, gpt3_azure_endpoint, azure_api_version
from Prompt import get_prompts
from train_data import train_data
from llama_index import Document, VectorStoreIndex
import nest_asyncio
nest_asyncio.apply()

from llama_index.llms import AzureOpenAI
from llama_index.embeddings import AzureOpenAIEmbedding
import nest_asyncio
from llama_index import ServiceContext, StorageContext, load_index_from_storage

from llama_index.retrievers import VectorIndexRetriever




llm = AzureOpenAI(
    model="gpt-35-turbo-16k",
    deployment_name="DanielChatGPT16k",
    api_key=gpt3_azure_api_key,
    azure_endpoint=gpt3_azure_endpoint,
    api_version=azure_api_version,
    max_tokens=1000
)
embed_model = AzureOpenAIEmbedding(
    model="text-embedding-ada-002",
    deployment_name="text-embedding-ada-002",
    api_key=gpt3_azure_api_key,
    azure_endpoint=gpt3_azure_endpoint,
    api_version=azure_api_version,
)

service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)


persist_dir = './storage'
is_local_vector_store = os.path.exists(persist_dir) and os.listdir(persist_dir)

if is_local_vector_store:
    print("loading index from storage")
    storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
    print(storage_context)
    index = load_index_from_storage(storage_context, service_context=service_context)

else:

    # Create custom nodes
    nodes = []
    for data in train_data.keys():
        # node = TextNode(text=data)
        node =  Document(text=data)
        node.metadata = {"NoSQL":train_data[data]}
        nodes.append(node)

    index = VectorStoreIndex(nodes, service_context=service_context, show_progress=True)

    # Save the index to storage
    index.storage_context.persist(persist_dir = './storage')


# configure retriever
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=5,
)


def retrieve_prompt(user_query):
    retrieved_node = retriever.retrieve(user_query)
    similar_nosql = "\n\n".join([i.metadata["NoSQL"] for i in retrieved_node])

    return get_prompts(similar_nosql=similar_nosql)


def  update_vectorstore(user_query):
    pass

