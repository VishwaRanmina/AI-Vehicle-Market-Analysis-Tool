import os

from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI



load_dotenv()
os.environ["USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"

API_KEY = os.getenv("OPENAI_API_KEY")
API_URL = os.getenv("OPENROUTER_URL")

summarizer_llm = ChatOpenAI(model="meta-llama/llama-3.3-70b-instruct:free",
                            api_key=API_KEY,
                            base_url=API_URL)

car_model = "axio"

urls = [
    f"https://ikman.lk/en?query={car_model}",
    f"https://riyasewana.com/search/{car_model}"
]

website_loader = WebBaseLoader(urls)
docs = website_loader.load()

summarizer_prompt = ChatPromptTemplate.from_template(
    """Extract car price in rupees, manufacture year , milage for the given car below
    {car_model}
    

    
    Website Data:
    {docs}
    """
)

summarizer_chain = summarizer_prompt | summarizer_llm
ads_summary = summarizer_chain.invoke({"car_model": car_model, "docs":"\n".join([doc.page_content for doc in docs])})

print(ads_summary.content)

response_prompt = ChatPromptTemplate.from_template("""
        you are an automotive assistance helping users find the best car deals.
        Here is summarized list of car ads for {car_model}
        
        {ads_summary}
        
        Highlight key insights, provide a 1-3 summary ,also provide best average price to buy.    """)

analyze_llm = ChatOpenAI(model="meta-llama/llama-3.3-70b-instruct:free",
                         api_key=API_KEY,
                         base_url=API_URL)

analyze_chain = response_prompt | analyze_llm

output = analyze_chain.invoke({"car_model" : car_model , "ads_summary": ads_summary})
print(output)