# Advanced Wafer Fab Defect Expert System - Streamlit

## Local run

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Then open the local URL shown by Streamlit, usually:

```text
http://localhost:8501
```

## Deploy to Streamlit Community Cloud

1. Put `streamlit_app.py` and `requirements.txt` in a GitHub repository.
2. Go to Streamlit Community Cloud.
3. Create a new app from the GitHub repository.
4. Set the main file path to:

```text
streamlit_app.py
```

5. Deploy. The generated URL can be opened from desktop or mobile browsers.
