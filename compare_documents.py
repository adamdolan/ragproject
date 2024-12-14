from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import json


PROMPT_TEMPLATE_sub = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

PROMPT_TEMPLATE_doc1 = """
Here's a query: 
{q}

---

JSON format:

"db1": "text here", "db2": "text here"

---

Using the query above and JSON format, create two queries for based on the following file names: {filename1} and 
{filename2}. Package the two queries together in a one dimension JSON string, with {filename1} query being called "db1" 
and {filename2} query being "db2".

"""

PROMPT_TEMPLATE_main = """
Answer the question based only on the following context:

{context1}
{context2}

---

Answer the question based on the above context: {question}
"""


def db_engine(db_name, query_text):
    # Prepare the DB.
    embedding_function = OpenAIEmbeddings()
    db = Chroma(persist_directory=db_name, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query_text, k=2)
    print(results)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_sub)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)

    model = ChatOpenAI()
    response_text = model.predict(prompt)

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)

    return response_text


def subquery_generator(file1, file2, main_query):
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_doc1)
    prompt = prompt_template.format(q=main_query, filename1=file1,
                                    filename2=file2)
    print(prompt)

    model = ChatOpenAI()
    response_text = model.predict(prompt)
    json1_data = json.loads(response_text)
    print(json1_data)

    context1 = db_engine("chromadb1", json1_data["db1"])
    context2 = db_engine("chromadb2", json1_data["db2"])

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_main)
    prompt = prompt_template.format(context1=context1, context2=context2, question=main_query)
    model = ChatOpenAI()
    response_text1 = model.predict(prompt)
    print(response_text1)

