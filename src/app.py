"""
The frontend: a Streamlit dashboard for a business owner.

Paste customer reviews (one per line), click Analyze, and see the results.
This app does NOT call Gemini directly. It calls OUR OWN backend (api.py),
exactly the way we called external APIs in Lesson 9.

Run it (in a SECOND terminal, while api.py is also running):
    uv run streamlit run app.py
"""

from collections import Counter

import requests
import streamlit as st

# Our own database code, kept in a separate file (database.py).
from database import init_db, save_results, load_history, DB_FILE

# The address of our own backend service.
API_URL = "http://127.0.0.1:8000/getrecipe"

# Make sure the table exists before the app uses it.
init_db()

st.title("📝 Customer Recipe Creator")
st.write("Paste your instagram url.")

reviews_text = st.text_area("Recipe", height=25)

if st.button("Get Recipe"):

    recipe = reviews_text.strip()

    if not recipe:
        st.warning("Please paste at least one url recipe url.")
    else:
        results = []
        # Go through each review and ask our backend to parse url it.

        try:
            response = requests.post(API_URL, json={"url": recipe})

            if response.ok:
                data = response.json()
                results.append({               
                    "meat": data["meat"],
                    "title": data["title"],
                    "recipe": data["recipe"]
                })
                st.session_state.results = results
            else:
                try:
                    error_body = response.json()
                except ValueError:
                    error_body = None
                detail = (
                    error_body.get("detail", response.text)
                    if isinstance(error_body, dict)
                    else response.text
                )
                st.error(f"Recipe API returned {response.status_code}: {detail}")
        except requests.RequestException as error:
            st.error(f"Could not reach the recipe API: {error}")

# Save results in session_state so they survive button clicks.

# Show the results if we have any.
if "results" in st.session_state:
    results = st.session_state.results

    st.subheader("Results")
    st.dataframe(results)


    st.subheader("Summary")

        # ---- Save the full report to the database (Lesson 12) ----
    if st.button("💾 Save to database"):
        save_results(results)
        st.success(f"Saved {len(results)} reviews to {DB_FILE}")

# ---- Show everything we have ever saved (reads from the database) ----
with st.expander("📊 Saved history (all reviews in the database)"):
    history = load_history()
    if history:
        st.write(f"Total saved so far: {len(history)}")
        st.dataframe(
            [{"meat": r[0], "title": r[1], "recipe": r[2]} for r in history]
        )
    else:
        st.write("Nothing saved yet. Analyze some reviews and click Save.")