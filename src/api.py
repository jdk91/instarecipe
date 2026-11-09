import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import workwithgenai
import insta
from dotenv import load_dotenv


logger = logging.getLogger(__name__)

class RecipeRequest(BaseModel):
    url: str



load_dotenv()
app = FastAPI()

@app.post("/getrecipe")
def post_recipe_url(request: RecipeRequest):
    try:
        parser = insta.InstagramURLParser(request.url)
        print("Got parser!")
        shortcode = parser.extract_shortcode()
        print("Got shortcode!")
        service = insta.InstagramService()
        desc = service.extract_description(shortcode)
        print("Got description!")
        AIinstance = workwithgenai.AIManipulation(desc)
        response = AIinstance.generate_response()

        # with open("latest_recipe.md", "w", encoding="utf-8") as f:
        #     f.write(response)

        return response
    except (TypeError, ValueError) as e:
        # Bad input / invalid URL / not a string -> Return 400 Bad Request
        raise HTTPException(status_code=400, detail=str(e))
        
    except RuntimeError as e:
        # Instagram fetching error -> Return 502 Bad Gateway or 400
        raise HTTPException(status_code=502, detail=str(e))
        
    except Exception as e:
        # Catch-all for unexpected errors
        logger.exception("Unexpected error while processing recipe URL")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

