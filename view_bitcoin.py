import streamlit as st
import pandas as pd


# google drive上のcsvファイルのURL
URL = (
    "https://drive.google.com/file/d/1Q2c6pRbZp16tzGUFLB9X-I_7IJcROxUW/view?usp=sharing"
)
# google drive api key
KEY = st.secrets.GoogleDriveApiKey.key

@st.cache
def load_data():
    """
    Args:
        url: google drive 
    """
    path = f"https://www.googleapis.com/drive/v3/files/{URL.split('/')[-2]}?alt=media&key={KEY}"
    return pd.read_csv(path)
    

df = load_data() 


st.write(df.head(5))
