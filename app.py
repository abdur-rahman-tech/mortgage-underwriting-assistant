import os
import nest_asyncio
import litellm
import streamlit as st

# 1. Apply nest_asyncio to prevent CrewAI/asyncio event loop conflicts in Streamlit
nest_asyncio.apply()

# 2. Configure LiteLLM globally to prevent 'cache_breakpoint' errors on Groq
litellm.drop_params = True
os.environ["LITELLM_CACHE"] = "False"

from config.settings import APP_TITLE, MAX_DOCUMENT_CHARS
from crew.underwriting_crew import run_underwriting_crew
from tools.document_parser import parse_uploaded_documents
from reports.report_generator import build_report


st.set_page_config(page_title=APP_TITLE, page_icon="🏠", layout="wide")

st.title("Mortgage Underwriting Assistant")
st.caption("Five-agent underwriting support system • CrewAI + Groq + FAISS + Streamlit")

st.warning(
    "Decision-support prototype only. It does not approve or deny loans and must be reviewed "
    "by a qualified human underwriter."
)

with st.sidebar:
    st.header("Application")
    loan_program = st.selectbox(
        "Loan program",
        ["Conventional", "FHA", "VA", "USDA", "Unknown"],
        index=0,
    )
    property_value = st.number_input(
        "Property value (optional)", min_value=0.0, value=400000.0, step=5000.0
    )
    loan_amount = st.number_input(
        "Loan amount (optional)", min_value=0.0, value=320000.0, step=5000.0
    )
    proposed_housing_payment = st.number_input(
        "Proposed housing payment / month (optional)",
        min_value=0.0,
        value=2100.0,
        step=50.0,
    )

st.subheader("1. Upload borrower documents")
uploaded_files = st.file_uploader(
    "Upload PDF, TXT, or DOCX documents",
    type=["pdf", "txt", "docx"],
    accept_multiple_files=True,
)

demo = st.checkbox("Use the built-in demo application", value=not bool(uploaded_files))

if demo:
    demo_text = """
DEMO APPLICATION — FOR SOFTWARE TESTING ONLY

Borrower: John Smith
Loan Program: Conventional
Monthly gross employment income: $8,500
Other monthly income: $0
Monthly existing debt obligations: $1,750
Proposed housing payment: $2,100
Loan amount: $320,000
Property value: $400,000
Credit score: 742
Assets available for closing: $55,000

Evidence:
- January paystub, page 2: gross monthly income $8,500.
- Credit report, page 1: credit score 742.
- Bank statement, page 3: available balance $55,000.
- Loan application, page 4: loan amount $320,000 and property value $400,000.

Known issue for testing:
The application contains no current employment verification document.
"""
    documents_text = demo_text.strip()
else:
    documents_text = parse_uploaded_documents(uploaded_files)

if len(documents_text) > MAX_DOCUMENT_CHARS:
    st.info(
        f"Documents exceed the configured context limit. Text will be truncated to "
        f"{MAX_DOCUMENT_CHARS:,} characters for the prototype."
    )
    documents_text = documents_text[:MAX_DOCUMENT_CHARS]

st.subheader("2. Run underwriting review")

if st.button("Analyze Application", type="primary", use_container_width=True):
    if not documents_text.strip():
        st.error("Upload at least one document or enable the demo application.")
        st.stop()

    with st.status("Running the five-agent underwriting crew...", expanded=True) as status:
        try:
            st.write("Executing multi-agent underwriting pipeline...")
            result = run_underwriting_crew(
                application_text=documents_text,
                loan_program=loan_program,
                property_value=property_value,
                loan_amount=loan_amount,
                proposed_housing_payment=proposed_housing_payment,
            )
            st.session_state["review_result"] = result
            status.update(label="Underwriting review completed", state="complete")
        except Exception as exc:
            status.update(label="Review failed", state="error")
            st.exception(exc)
            st.stop()

# 3. Render report if results are in session state
if "review_result" in st.session_state:
    result = st.session_state["review_result"]
    report = build_report(result)

    st.subheader("3. Underwriting report")

    tabs = st.tabs(
        [
            "Final Validation",
            "Document Review",
            "Policy Review",
            "Calculations",
            "Assessment",
            "Full Report",
        ]
    )

    with tabs[0]:
        st.markdown(result.get("validation", ""))
    with tabs[1]:
        st.markdown(result.get("document_review", ""))
    with tabs[2]:
        st.markdown(result.get("policy_review", ""))
    with tabs[3]:
        st.markdown(result.get("calculation_review", ""))
    with tabs[4]:
        st.markdown(result.get("assessment", ""))
    with tabs[5]:
        st.markdown(report)

    st.download_button(
        "Download Markdown Report",
        data=report,
        file_name="underwriting_report.md",
        mime="text/markdown",
        use_container_width=True,
    )

st.divider()
st.caption("Prototype architecture: 5 CrewAI agents, deterministic Python calculations, FAISS policy retrieval, human validation.")
