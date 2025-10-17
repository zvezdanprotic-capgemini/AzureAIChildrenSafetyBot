import os
from azure.ai.contentsafety.aio import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from dotenv import load_dotenv

load_dotenv()

async def is_content_safe(text: str):
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    
    # Get thresholds from environment variables
    hate_threshold = int(os.getenv('HATE_THRESHOLD', '2'))
    violence_threshold = int(os.getenv('VIOLENCE_THRESHOLD', '2'))
    sexual_threshold = int(os.getenv('SEXUAL_THRESHOLD', '2'))
    self_harm_threshold = int(os.getenv('SELF_HARM_THRESHOLD', '2'))

    # Create an async Content Safety client
    async with ContentSafetyClient(endpoint, AzureKeyCredential(key)) as client:
        # Construct request
        request = AnalyzeTextOptions(text=text)

        try:
            response = await client.analyze_text(request)
            
            categories = {
                'hate': 0,
                'self_harm': 0,
                'sexual': 0,
                'violence': 0
            }
            for result in response.categories_analysis:
                # Map enum to our lowercase keys
                if result.category == TextCategory.HATE:
                    categories['hate'] = result.severity
                elif result.category == TextCategory.SELF_HARM:
                    categories['self_harm'] = result.severity
                elif result.category == TextCategory.SEXUAL:
                    categories['sexual'] = result.severity
                elif result.category == TextCategory.VIOLENCE:
                    categories['violence'] = result.severity

            # Check against configurable thresholds
            is_safe = (
                categories['hate'] < hate_threshold and
                categories['violence'] < violence_threshold and
                categories['sexual'] < sexual_threshold and
                categories['self_harm'] < self_harm_threshold
            )

            return {
                'allowed': is_safe,
                'categories': categories
            }
                
        except HttpResponseError as e:
            print(f"Content Safety API error: {str(e)}")
            return {'allowed': False, 'categories': {}}
        except Exception as e:
            print(f"Unexpected error in content safety check: {str(e)}")
            return {'allowed': False, 'categories': {}}
