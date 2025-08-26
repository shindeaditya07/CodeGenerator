import os
from typing import List, Dict, Optional
from click import prompt
from openai import api_key
import streamlit as st
from dotenv import load_dotenv
import requests
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load environment variables from.env file
load_dotenv()
st.set_page_config(page_title="Multi-Language Code Generator", layout="wide")

# Get API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    st.error("Please set the required environment variables OPENAI_API_KEY.")
    st.stop()

SUPPORTED_LANGS = ["Python", "JavaScript", "Java", "C++", "C", "HTML", "CSS"]

sys_prompt = ("""
You are an unbiased but careful senior developer, and you must write clean, efficient, and well-documented code.
When generating code, make sure to use the correct logic, syntax, and formatting. Also make sure that the code is concise, easy to understand and maintain.
Always give only the necessary code, avoid unnecessary comments and explanation, avoid extra text and follow best coding practices.
Available languages: {supported_langs}
""")

st.sidebar.title("Settings")
provider = st.sidebar.selectbox("Code Generation Provider", ["OpenAI", "CodeLama"])
if provider == "OpenAI":
    model = st.sidebar.selectbox("Model Name", ["gpt-4", "gpt-4o", "gpt-4-turbo"])
    api_key = openai_api_key
temperature = st.sidebar.slider("Creativity Temperature", 0.0, 1.0, 0.7)
max_tokens = st.sidebar.slider("Max Tokens", 128, 4096, 1200, 64)

st.title("Multi-Language Code Generator")
st.caption("Generate clean, efficient, and well-documented code in multiple languages, get line-by-line explanation and translate from 1 language to another.")
task = st.selectbox("Task", ["Code Generation", "Code Translation", "Code Explanation"])

with st.expander("Advanced Settings"):
    adv_prompt = st.text_area("System Prompt", value= sys_prompt, height=140)

llm = ChatOpenAI(model=model, openai_api_key=api_key, temperature=temperature, max_tokens=max_tokens)

    
if task == "Code Generation":
    lang = st.selectbox("Select Target Language", SUPPORTED_LANGS)
    code = st.text_area("Give your query", height=200)
    if st.button("Generate") and sys_prompt:
        query = f"Write {lang} code using the provided system prompt: {prompt}. Output only the generated code."
        messages = [SystemMessage(content=sys_prompt), HumanMessage(content=f"Write {lang} code using the provided system prompt: {code}")]
        response = llm(messages)
        output = st.code(response.content, language=lang)
        output

elif task == "Code Translation":
    source_lang = st.selectbox("Select Source Language", SUPPORTED_LANGS)
    target_lang = st.selectbox("Select Target Language", SUPPORTED_LANGS)
    code_input = st.text_input(f"Paste your {source_lang} code")
    if st.button("Translate") and code_input:
        query = f"Translate {source_lang} code to {target_lang}: \n{code_input}"
        messages = [SystemMessage(content=sys_prompt), HumanMessage(content=f"Translate {source_lang} code to {target_lang}: \n{code_input}")]
        response = llm(messages)
        output = st.code(response.content, language=target_lang)
        output

elif task == "Code Explanation":
    lang = st.selectbox("Select Language", SUPPORTED_LANGS)
    code_input = st.text_input("Paste your code")
    if st.button("Explain") and code_input:
        query = f"Explain {lang} code: \n{code_input}"
        messages = [SystemMessage(content=sys_prompt), HumanMessage(content=f"Explain the {lang} code: \n{code_input}")]
        response = llm(messages)
        output = st.code(response.content, language="markdown")
        output