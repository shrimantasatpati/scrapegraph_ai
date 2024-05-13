from scrapegraphai.graphs import SmartScraperGraph
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
import os
import json
from scrapegraphai.graphs import SearchGraph
from scrapegraphai.utils import convert_to_csv, convert_to_json, prettify_exec_info

os.environ["AZURE_OPENAI_API_KEY"] = "312ff50d6d954023b8748232617327b6"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://openai-lh.openai.azure.com/"
os.environ["AZURE_OPENAI_API_VERSION"] = "2023-06-01-preview"
os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"] = "LH-GPT"

llm_model_instance = AzureChatOpenAI(
    openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
    )

embedder_model_instance = AzureOpenAIEmbeddings(
    azure_deployment='LH-embedding',
    openai_api_version="2024-02-15-preview",
)

graph_config = {
    "llm": {"model_instance": llm_model_instance},
    "embeddings": {"model_instance": embedder_model_instance}
}

smart_scraper_graph = SmartScraperGraph(
    prompt="what are the additives in the top ramen?",
    source="https://world.openfoodfacts.org/product/8901014003181/top-ramen-curry-nissin",
    config=graph_config
)

result = smart_scraper_graph.run()
print(result)

with open('output.json', 'w') as json_file:
    json.dump(result, json_file, indent=4)

print("Output saved to output.json")

# ************************************************
# Get graph execution info
# ************************************************

graph_exec_info = smart_scraper_graph.get_execution_info()
print(prettify_exec_info(graph_exec_info))