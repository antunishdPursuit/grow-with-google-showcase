"""Streamlit interface for the Apex Engineers Business Readiness Check."""

from pathlib import Path

import streamlit as st

from diagnostic import (
    NOT_APPLICABLE,
    NO,
    QUESTIONS,
    YES,
    calculate_risk,
    find_priorities,
    generate_report,
)


st.set_page_config(
    page_title="Business Readiness Check",
    page_icon="BRC",
    layout="centered",
)


def load_styles() -> None:
    """Load the project stylesheet from the application directory."""
    stylesheet = Path(__file__).with_name("styles.css")
    st.markdown(
        f"<style>{stylesheet.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )


load_styles()

st.markdown('<div class="brc-brand-line" aria-hidden="true"></div>', unsafe_allow_html=True)
st.title("Business Readiness Check")
st.write(
    "Answer four questions to identify technology gaps and receive a "
    "prioritized modernization plan."
)
st.info(
    "Privacy: This version does not require an account and does not intentionally "
    "store your answers. Do not enter passwords, payment-card details, customer "
    "records, or other sensitive information."
)

with st.form("readiness_assessment"):
    st.subheader("About the business")
    business_name = st.text_input(
        "Business name (optional)",
        max_chars=80,
        help="Use a general or example name if you prefer not to identify the business.",
    )
    business_type = st.selectbox(
        "Business type (optional)",
        [
            "",
            "Retail storefront",
            "E-commerce",
            "Retail and e-commerce",
            "Service-based business",
            "Other",
        ],
        format_func=lambda value: "Select a business type" if not value else value,
    )

    st.subheader("Technology assessment")
    answers: dict[str, str | None] = {}
    for key, question in QUESTIONS.items():
        answers[key] = st.radio(
            question.prompt,
            options=[YES, NO, NOT_APPLICABLE],
            index=None,
            horizontal=True,
            key=f"answer_{key}",
        )

    submitted = st.form_submit_button("Generate assessment", type="primary")

if submitted:
    missing_labels = [
        QUESTIONS[key].label for key, answer in answers.items() if answer is None
    ]
    if missing_labels:
        st.warning("Answer every diagnostic question before generating the result.")
    else:
        completed_answers = {key: str(answer) for key, answer in answers.items()}
        result = calculate_risk(completed_answers)
        priorities = find_priorities(completed_answers)

        st.divider()
        st.header("Your results")

        if result.risk_percentage is None:
            st.warning(
                "A score could not be calculated because every area was marked "
                "Not applicable. Select at least one applicable area."
            )
        else:
            score_column, level_column = st.columns(2)
            score_column.metric("Technology risk score", f"{result.risk_percentage:.1f}%")
            level_column.metric("Risk level", result.risk_level)

            if priorities:
                _, highest_priority = priorities[0]
                st.subheader(f"Highest priority: {highest_priority.label}")
                st.write(highest_priority.explanation)
                st.success(highest_priority.recommendation)
            else:
                st.success(
                    "No priority gaps were identified from the answers provided."
                )

        st.subheader("Recommended next steps")
        if priorities:
            for index, (_, question) in enumerate(priorities, start=1):
                st.markdown(f"**{index}. {question.recommendation}**")
                st.write(question.explanation)
        elif result.risk_percentage is None:
            st.write("Complete at least one applicable area to receive recommendations.")
        else:
            st.write("Continue monitoring these areas as the business changes.")

        with st.expander("Review all answers"):
            for key, question in QUESTIONS.items():
                st.write(f"**{question.label}:** {completed_answers[key]}")

        report = generate_report(
            completed_answers,
            result,
            business_name=business_name,
            business_type=business_type,
        )
        st.download_button(
            "Download results report",
            data=report,
            file_name="business-readiness-check.txt",
            mime="text/plain",
            on_click="ignore",
        )

        st.caption(
            "This educational tool provides general guidance. It is not a formal "
            "security, financial, compliance, or technology audit."
        )
