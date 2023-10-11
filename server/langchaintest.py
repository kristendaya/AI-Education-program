from langchain.document_loaders import UnstructuredFileLoader
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.weaviate import Weaviate
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import os
import weaviate
import pymongo
import datetime

os.environ["OPENAI_API_KEY"] =""
os.environ["WEAVIATE_API_KEY"] =""

doc_loader = DirectoryLoader(
    './soo', # the relative directory address, remember we set root directory above
    glob='**/*.pdf',     # Let's load only pdf files in every subdirectory
    show_progress=True
)
docs = doc_loader.load()

splitter = CharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=200
)
splitted_docs_list = splitter.split_documents(docs)

auth_config = weaviate.auth.AuthApiKey(api_key=os.environ.get('WEAVIATE_API_KEY'))
client = weaviate.Client(
    url="https://korean-sat-mo5di8dh.weaviate.network",
    auth_client_secret=auth_config,
    additional_headers={
        "X-OpenAI-Api-Key": os.environ.get('OPENAI_API_KEY')
    }
)

class_obj = {
    "class": "LangChain",
    "vectorizer": "text2vec-openai",
}

try:
  # Add the class to the schema
  client.schema.create_class(class_obj)
except:
  print("Class already exists")

embeddings = OpenAIEmbeddings()
# I use 'LangChain' for index_name and 'text' for text_key
vectorstore = Weaviate(client, "LangChain", "text", embedding=embeddings)

documents = splitted_docs_list

texts = [d.page_content for d in documents]
metadatas = [d.metadata for d in documents]

vectorstore.add_texts(texts, metadatas=metadatas, embedding=embeddings)

vectorstore = Weaviate.from_texts(
    texts,
    embeddings,
    metadatas=metadatas,
    client=client,
)

llm = ChatOpenAI()
retrieval_qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type='stuff',
    retriever=vectorstore.as_retriever(),
)


time = now = datetime.datetime.now().strftime('%Y-%m-%d')
id = "01AA000"
cnt = 1
pack = 1
down = 1
while cnt < 301:
    # query = "You're an English teacher and You should make exams with the varieties of subjects in the given text. Please generate a question with the formation 'passage' in English ,'question'in Korean,'4 options'in English ,'answer' in Enlgish,'explanation'in Korean "
    # query = "You're an English teacher and You should make exams with the varieties of subjects in the given text. Please generate a question with the formation 'passage','question', '4 options','answer','explanation' "
    query = "You're an English teacher and You should make exams with the varieties of subjects in the given text. Please generate a question with the formation 'passage','question','options','answer','explanation'"
    paragraphs = retrieval_qa.run(query)
    # paragraphs = f"{paragraph} With this Passage -> Question(in Korean) -> Options -> Answer(in Korean) Please organize it in order"
    print(paragraphs)
    data = dict()
    for _ in range(0,4):
        try:
            if _ == 0:
                par = paragraphs.split("Question:")
                print(f"첫번째로 나눠지는 항목은 {par[0]}")
                print("--" * 50)
                data["qassage"] = par[0]
                data["qassage"] = data["qassage"].replace("Passage:", "").replace("\n", "")
                paragraphs = par[1]
            elif _ == 1:
                par = paragraphs.split("Options:")
                print(f"두번째로 나눠지는 항목은 {par}")
                print("--" * 50)
                data["question"] = par[0]
                data["question"] = data["question"].replace("\n", "")
                paragraphs = par[1]
            elif _ == 2:
                par = paragraphs.split("Answer:")
                print(f"세번째로 나눠지는 항목은 {par}")
                print("--" * 50)
                data["options"] = par[0]
                data["options"] = data["options"].replace("\n", "")
                paragraphs = par[1]
            else:
                print(f"네번째로 나눠지는 항목은 {paragraphs}")
                data["answer"] = paragraphs
                print("--" * 50)
                
        except IndexError as i:
            print(i)
            continue
    print(cnt)
    if cnt < 10:
        id = "01AA000"
    elif cnt < 100:
        id = "01AA00"
    elif cnt < 1000:
        id = "01AA0"
    else:
        id = "01AA"
    
    if down == 11:
        print(f"여기: {down}")
        pack += 1
        down = 1    
    print(down)
    id += str(cnt)
    print(f"id: {id}" )
    print(f"pack: {pack}")
    data["id"] = id
    data["pack"] = pack
    data["name"] = f"수능 특강 영어변형 문제{pack}"
    now = datetime.datetime.now()
    now_date = now.strftime('%Y-%m-%d')
    data["time"]= now_date
    print("여기를 지나쳤습니다.")
    myclient = pymongo.MongoClient("mongodb://43.202.26.130:27017/")
    mydb = myclient["admin"]
    mycol = mydb["koreanSAT"]
    mycol.insert_one(data)
    cnt += 1
    down +=1 
    
    
    
