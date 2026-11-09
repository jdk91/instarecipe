# InstaRecipe

InstaRecipe turns an Instagram post into a structured recipe. Paste a post URL
into the Streamlit app; the FastAPI backend fetches its caption and asks Google
Gemini to return the meat, dish title, ingredients, and cooking instructions.
Generated results can be saved to a local SQLite database and viewed later.

## Requirements

- Windows with Python 3.14 or newer
- A Google Gemini API key
- An Instagram post URL that InstaLoader can access

## Setup

Run these commands in PowerShell from the repository root:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install fastapi uvicorn instaloader google-genai python-dotenv pydantic requests streamlit
```

Create a `.env` file in the repository root and add your Gemini API key:

```text
GEMINI_API_KEY=your_api_key_here
```

Keep the key private; do not commit `.env` or share its contents.

## Run the application

Start the API in one PowerShell terminal from the repository root:

```powershell
.\.venv\Scripts\python.exe -m uvicorn api:app --app-dir src --reload
```

In a second terminal, also from the repository root, start Streamlit:

```powershell
.\.venv\Scripts\python.exe -m streamlit run src/app.py
```

Open the Streamlit URL printed in the second terminal (usually
`http://localhost:8501`). The API's interactive documentation is available at
`http://127.0.0.1:8000/docs`.

## Use

1. Paste an Instagram post URL (a `/p/`, `/reel/`, or `/tv/` URL) into the
   **Recipe** field.
2. Select **Get Recipe** and wait for the recipe to be generated.
3. Select **Save to database** to save the result. Saved recipes appear in the
   history panel.

The generated recipe is translated to Russian when the caption is in English.
The meat and title fields are returned in English and lowercase; ingredient
measurements use metric units, except tablespoons and teaspoons.

The database is `recipe.db` in the repository root when started with the
commands above. Instagram may restrict access to some posts; the URL must be
valid and its caption must be retrievable. API errors are displayed in the
Streamlit app, and unexpected backend errors are logged in the Uvicorn
terminal.