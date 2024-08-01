from src.embedd_all.index import modify_excel_for_embedding, process_pdf
from src.embedd_all.rag_query import rag_and_query
import os

ANTHROPIC_API_KEY = os.environ['ANTHROPIC_API_KEY']
PINECONE_KEY = os.environ['PINECONE_KEY']
VOYAGE_API_KEY = os.environ['VOYAGE_API_KEY']





def rag_query():
    CLAUDE_MODEL = "claude-3-5-sonnet-20240620"
    #inddex name for pine_cone vector db
    INDEX_NAME = 'index_name'
    QUERY = 'How to configure UI'
    SYSTEM_PROMPT = "You are a world-class document writer. Respond only with detailed description and implementation. Use bullet points if neccessary"
    VOYAGE_EMBED_MODEL = 'voyage-2'

    resp = rag_and_query(
        anthropic_api_key=ANTHROPIC_API_KEY,
        claude_model=CLAUDE_MODEL, 
        index_name=INDEX_NAME, 
        pinecone_key=PINECONE_KEY, 
        query=QUERY, 
        system_prompt=SYSTEM_PROMPT,
        voyage_api_key=VOYAGE_API_KEY,
        voyage_embed_model=VOYAGE_EMBED_MODEL
        )
    
    # print("resp: ", resp["text"])

    for text_block in resp:
        print(text_block.text)

if __name__ == '__main__':
    # Example usage
    # file_path = '/Users/arnabbhattachargya/Desktop/data.xlsx'
    # file_path = '/Users/arnabbhattachargya/Desktop/setu-product/UMAP.pdf'
    # context = "data"
    # dfs = modify_excel_for_embedding(file_path=file_path, context=context)
    # print(dfs[2].head(3))

    # texts = process_pdf(file_path)
    # print("Text Length: ", len(texts))
    # print("Text process: ", texts)
    rag_query()