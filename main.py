from Similarity_search.similarity import retrieve_top_k
from text_chunking.chunking import *
from text_chunking.loadingdata import *
from text_embedding.embedding import *
from text_chunking.text_splitter_langchain import split_documents
from prompting import build_prompt
from llm import generate_answer

from dotenv import load_dotenv
load_dotenv()

CONFIDENCE_THRESHOLD = 0.35
MINIMUM_THRESHOLD = 0.20   # hard fail threshold

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
documents = load_documents('/Users/adhyayan/PycharmProjects/LemniscaRAG/clearpath_docs')

# chunks = create_chunks(documents)
chunks = split_documents(documents)

chunks_embedded = embed_chunks(chunks)
print("Chunks:", len(chunks))
print("Embedding dim:", len(chunks_embedded[0]["embedding"]))

query = "how do i cook eggs?"
# top_chunks = retrieve_top_k(query, chunks_embedded, embedding_model, k=3)
retrieved = retrieve_top_k(query, chunks_embedded, embedding_model, k=4)

# for chunk in top_chunks:
#     print("-----")
#     print("File:", chunk["filename"])
#     print("Text:", chunk["text"][:])

if not retrieved:
    print("No-context response — no relevant chunks retrieved.")
    exit()

top_score = retrieved[0][0]

print("Top similarity score:", top_score)

if top_score < MINIMUM_THRESHOLD:
    print("No-context response — the system found no relevant information.")
    exit()

if top_score < CONFIDENCE_THRESHOLD:
    print("Low confidence — please verify with support.")
    exit()

top_chunks = [item[1] for item in retrieved]

prompt = build_prompt(query, top_chunks)
answer = generate_answer(prompt)

print(answer)