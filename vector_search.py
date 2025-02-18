import weaviate
import weaviate.classes as wvc
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve credentials from environment variables
cluster_url = os.getenv("WEAVIATE_CLUSTER_URL")
api_key = os.getenv("WEAVIATE_API_KEY")
voyage_ai_api_key = os.getenv("VOYAGE_AI_API_KEY")

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=cluster_url,                                    
    auth_credentials=wvc.init.Auth.api_key(api_key),   
    headers={"X-VoyageAI-Api-Key": voyage_ai_api_key}            
)

try:
    pass  # Work with the client. Close client gracefully in the finally block.
    questions = client.collections.get("WikipediaArticles")

    response = questions.query.near_text(
        query="Blockchain",
        limit=2
    )

    print(response.objects[0].properties)
    print(response.objects[1].properties)

finally:
    client.close() 
