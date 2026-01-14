import streamlit as st
import requests
import pandas as pd
import json

# ---------- Fixed Schema ----------
EXPECTED_FIELDS = [
    "Agreement Value",
    "Agreement Start Date",
    "Agreement End Date",
    "Renewal Notice (Days)",
    "Party One",
    "Party Two"
]

# ---------- Page Config ----------
st.set_page_config(
    page_title="Contract Metadata Extractor",
    page_icon="📄",
    layout="centered"
)

# ---------- Header ----------
st.markdown(
    """
    <h1 style="text-align:center;">📄 Contract Metadata Extractor</h1>
    <p style="text-align:center; color:gray;">
        AI-powered extraction of key contract details from DOCX and scanned images
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# ---------- File Upload ----------
st.subheader("Upload Contracts")
uploaded_files = st.file_uploader(
    "Upload one or more contracts (PNG or DOCX)",
    type=["png", "docx"],
    accept_multiple_files=True
)

# ---------- Extract Button ----------
if uploaded_files and st.button("🚀 Extract Metadata (Batch)"):

    results = []

    with st.spinner("Analyzing contracts using AI…"):
        for file in uploaded_files:
            try:
                files = {
                    "file": (file.name, file.getvalue())
                }

                response = requests.post(
                    "http://127.0.0.1:8000/extract",
                    files=files,
                    timeout=120
                )

                if response.status_code != 200:
                    results.append({
                        "File Name": file.name,
                        "Status": "Failed",
                        "Error": response.text
                    })
                    continue

                data = response.json()

                # ---------- FIXED SCHEMA ROW ----------
                row = {
                    "File Name": file.name
                }

                for field in EXPECTED_FIELDS:
                    row[field] = data.get(field, "")

                row["Status"] = "Success"
                results.append(row)

            except Exception as e:
                results.append({
                    "File Name": file.name,
                    "Status": "Failed",
                    "Error": str(e)
                })

    # ---------- Results ----------
    st.success("✅ Batch extraction completed")

    df = pd.DataFrame(results)

    # ---------- Enforce Column Order ----------
    COLUMN_ORDER = ["File Name"] + EXPECTED_FIELDS + ["Status"]
    df = df.reindex(columns=COLUMN_ORDER)

    st.dataframe(df, use_container_width=True)

    # ---------- Downloads ----------
    st.download_button(
        "⬇️ Download CSV",
        df.to_csv(index=False),
        "batch_contract_metadata.csv",
        "text/csv"
    )

    st.download_button(
        "⬇️ Download JSON",
        json.dumps(results, indent=2),
        "batch_contract_metadata.json",
        "application/json"
    )

# ---------- Footer ----------
st.divider()
st.markdown(
    """
    <p style="text-align:center; font-size:12px; color:gray;">
        Built with FastAPI, Streamlit, and Transformer-based Document AI
    </p>
    """,
    unsafe_allow_html=True
)
