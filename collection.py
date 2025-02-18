import weaviate
from weaviate.classes.init import Auth
import requests
from weaviate.collections.classes.config import Property, DataType
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve credentials from environment variables
cluster_url = os.getenv("WEAVIATE_CLUSTER_URL")
api_key = os.getenv("WEAVIATE_API_KEY")
voyage_ai_api_key = os.getenv("VOYAGE_AI_API_KEY")

# Connect to Weaviate Cloud
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=cluster_url,
    auth_credentials=Auth.api_key(api_key),
    headers={"X-VoyageAI-Api-Key": voyage_ai_api_key}
)

print(client.is_ready())

# Step 2: Create a Collection
try:
    client.collections.create(
        name="WikipediaArticles",
        vectorizer="text2vec-voyageai", 
        properties=[
            Property(name="title", data_type=DataType.TEXT),
            Property(name="summary", data_type=DataType.TEXT),
            Property(name="url", data_type=DataType.TEXT),
        ],
    )
    print("✅ Collection 'WikipediaArticles' created!")
except Exception:
    print("⚠️ Collection already exists, continuing...")

# Step 3: Function to Fetch Wikipedia Summary

def get_wikipedia_summary(topic):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "title": data.get("title", ""),
            "summary": data.get("extract", "No summary available."),
            "url": data.get("content_urls", {}).get("desktop", {}).get("page", ""),
        }
    return None

# Step 4: Fetch and Insert Data into Weaviate
topics = ["Artificial_Intelligence", "Machine_Learning", "Quantum_Computing", "Blockchain", "Space_Exploration"]

for topic in topics:
    article = get_wikipedia_summary(topic)
    if article:
        client.collections.get("WikipediaArticles").data.insert(article)
        print(f"✅ Inserted: {article['title']}")
        time.sleep(20)

print("🎉 Wikipedia data inserted into Weaviate!")

client.close()
# Step to delete collection
# existing_collections = client.collections.list_all()
# print("Existing collections:", existing_collections)

# # If 'WikipediaArticles' exists, delete it
# if "WikipediaArticles" in existing_collections:
#     client.collections.delete("WikipediaArticles")
#     print("⚠️ Collection 'WikipediaArticles' deleted.")
# else:
#     print("✔️ Collection 'WikipediaArticles' does not exist.")

# client.close()