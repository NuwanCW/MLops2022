from pathlib import Path

import pandas as pd
from tagifai import main, utils

import streamlit as st
from config import config

# Title
st.title("TagI ยท MLOps")

# ToC
st.markdown("๐ข [Data](#data)", unsafe_allow_html=True)
st.markdown("๐ [Performance](#performance)", unsafe_allow_html=True)
st.markdown("๐ [Inference](#inference)", unsafe_allow_html=True)

# Sections
st.header("๐ข Data")
projects_fp = Path(config.DATA_DIR, "labeled_projects.json")
projects = utils.load_dict(filepath=projects_fp)
df = pd.DataFrame(projects)
st.text(f"Projects (count: {len(df)})")
st.write(df)

st.header("๐ Performance")
performance_fp = Path(config.CONFIG_DIR, "performance.json")
performance = utils.load_dict(filepath=performance_fp)
st.text("Overall:")
st.write(performance["overall"])
tag = st.selectbox("Choose a tag: ", list(performance["class"].keys()))
st.write(performance["class"][tag])
tag = st.selectbox("Choose a slice: ", list(performance["slices"].keys()))
st.write(performance["slices"][tag])

st.header("๐ Inference")
text = st.text_input("Enter text:", "Transfer learning with transformers for text classification.")
run_id = st.text_input("Enter run ID:", open(Path(config.CONFIG_DIR, "run_id.txt")).read())
prediction = main.predict_tag(text=text, run_id=run_id)
st.write(prediction)
