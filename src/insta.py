import instaloader
import re

#https://www.instagram.com/p/De9bG5IoAl3/ for testing

class InstagramURLParser:
    def __init__(self, url:str):
        if not isinstance(url,str): raise TypeError("URL is not of a str type.")
        if not url: raise ValueError("Missing url.") 
        self.url = url.strip()


    def extract_shortcode(self) -> str:
        pattern = r"(?:https?:\/\/)?(?:www\.)?instagram\.com\/(?:p|reel|tv)\/([A-Za-z0-9_-]+)"  
        match = re.search(pattern,self.url)
        if not match:
            raise ValueError("Invalid Instagram URL.")
        return match.group(1)

class InstagramService:
    def __init__(self):
        self.loader = instaloader.Instaloader()

    def extract_description(self,shortcode:str) -> str:       
        try:
            post = instaloader.Post.from_shortcode(self.loader.context, shortcode)
            return post.caption
        except Exception as e:
            raise RuntimeError(f"Failed to fetch caption for shortcode {shortcode}") from e


if __name__ == "__main__":
    try:
        parser = InstagramURLParser("https://www.instagram.com/p/DdEZOEEM3fp/")
        shortcode = parser.extract_shortcode()
        
        service = InstagramService()
        caption = service.extract_description(shortcode)
        print("Caption:", caption)

    except (TypeError, ValueError, RuntimeError) as err:
        print(f"Error: {err}")