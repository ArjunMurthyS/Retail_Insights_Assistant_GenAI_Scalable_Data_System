import streamlit as st
import os, sys
from sales_data_analysis.data.db_manager import DBManager
from sales_data_analysis.agents.orchestrator import OrchestratorAgent

# Ensure the package is in path
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'src'))

st.set_page_config(page_title="Retail Insights Assistant", layout="wide")

st.title("🤖 Retail Insights AI Assistant")
st.markdown("Ask questions about your sales data in natural language.")

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "orchestrator" not in st.session_state:
    try:
        data_path = "Sales_Dataset/Amazon Sale Report.csv" 
        # Inside docker it might be /app/Sales_Dataset/... check Dockerfile
        if not os.path.exists(data_path):
             data_path = "/app/Sales_Dataset/Amazon Sale Report.csv"
             
        db = DBManager("sales_data.db")
        if os.path.exists(data_path):
             with st.spinner("Loading 100MB+ Dataset..."):
                db.ingest_csv(data_path)
        
        st.session_state.orchestrator = OrchestratorAgent(db)
        st.success("System Initialized & Data Loaded!")
    except Exception as e:
        st.error(f"Initialization Error: {e}")

# Chat Interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ex: What is the total revenue?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing data..."):
            try:
                if "orchestrator" in st.session_state:
                    response = st.session_state.orchestrator.process(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    st.error("System NOT initialized.")
            except Exception as e:
                st.error(f"Error: {e}")
