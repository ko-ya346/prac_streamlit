import json

import streamlit as st
import pandas as pd

with open("./googledrive_api.json", "r") as f:
    key = json.load(f)["api_key"]
# print(key)
URL = (
    "https://drive.google.com/file/d/1Q2c6pRbZp16tzGUFLB9X-I_7IJcROxUW/view?usp=sharing"
)
# URL = "https://drive.google.com/file/d/1Q2c6pRbZp16tzGUFLB9X-I_7IJcROxUW/view?usp=sharing"
# path = f"https://drive.google.com/uc?id={}"
path = f"https://www.googleapis.com/drive/v3/files/{URL.split('/')[-2]}?alt=media&key={key}"
# url2 = requests.get(path).text
# csv_raw = StringIO(url2)


df = pd.read_csv(path)
st.write(df.head(5))
