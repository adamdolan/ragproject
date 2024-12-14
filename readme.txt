This program uses the following:

LLM: OpenAI
VectorDB: chroma
Embeddings: OpenAI (through langchain)
NLP: TextBlob

Please import the following:
langchain (langchain base, langchain_openai, langchain_community)
pandas
openai
textblob
json
dotenv
os
shutil
argparse

Please adjust the DATA_PATH variable in main.py to whatever directory you're pulling PDFs from.

Menu option 1 (Extract specific information from a PDF document) will use all  the documents found in that directory
to build the vector database. Menu option 2 (Compare 2 similar PDF documents and output the differences) will list out
all the PDFs in that directory and allow the user to select 2 to compare. Menu options 3/4 do not require PDFs.

Menu option 1 is fairly straight forward in terms of RAG. It'll build out a vector DB and then allow you to query it.
When you submit a query, it'll report back what embeddings/sources it used. It's possible, depending on the exact use
case, to report back exactly what text was used for the context (which should be printed anyways as it goes through
execution).

Menu option 2 occasionally errors when running. This is because it uses a subquery generator that occasionally outputs
the wrong thing. More time is required to make this more robust. The program essentially splits the query into two,
gets a response from each of the documents being compared, and then uses that as the context for the original query.

To convert more complex JSON strings or to specify a filename, I would recommend simply calling the main function in
json_convertor.py. You'd have to pass the JSON string and, if required, a filename for output. The "menu" version is
more so a demonstration of this for simple JSON. It outputs a CSV file. The exact output can be adjusted depending on
the use case.

I'd like to spend more time on the sentiment analysis. Right now, sentiment is outputted on a -1 to 1 scale. In my
program, negative statements are regarded as those from -1 to -0.2. Neutral is -0.2 to 0.2. Positive is 0.2 to 1. These
cutoffs are arbitrary and likely require some more thought.

This program only works with simple PDFs. Shouldn't be difficult to add other file types or PDFs with more complex data
but this is what I could build with the time given.


**You will need an OpenAI api key. Use an .env file to set a variable called OPENAI_API_KEY to your key.


