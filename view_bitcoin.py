import streamlit as st
import pandas as pd

key = st.secrets.GoogleDriveApiKey.key
print(key)
URL = (
    "https://drive.google.com/file/d/1Q2c6pRbZp16tzGUFLB9X-I_7IJcROxUW/view?usp=sharing"
)
path = f"https://www.googleapis.com/drive/v3/files/{URL.split('/')[-2]}?alt=media&key={key}"


df = pd.read_csv(path)
st.write(df.head(5))
