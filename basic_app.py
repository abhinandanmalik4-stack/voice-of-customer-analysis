"""Small interface for learning customer feedback analysis."""
import streamlit as st
from basic_analysis import SAMPLE_REVIEWS, analyze_reviews, count_themes

st.set_page_config(page_title="Customer feedback analyzer", layout="wide")
st.title("Customer feedback analyzer")
st.caption("Find common topics and sentiment in customer feedback.")
st.info("The prefilled reviews are fictional practice examples. Analysis uses simple English keyword rules.")
with st.form("reviews"):
    review_text = st.text_area("Enter one review per line", value="\n".join(SAMPLE_REVIEWS), height=260, key="review_text")
    submitted = st.form_submit_button("Analyze reviews")
if submitted:
    try:
        st.session_state["basic_results"] = analyze_reviews(review_text)
        st.session_state["analyzed_input"] = review_text
    except ValueError as error:
        st.session_state.pop("basic_results", None)
        st.error(str(error))

if "basic_results" in st.session_state:
    results = st.session_state["basic_results"]
    st.caption("Results from your last analysis. After editing the input, click Analyze reviews again.")
    with st.container(horizontal=True):
        st.metric("Unique reviews", len(results), border=True)
        st.metric("Positive", int(results["Sentiment"].eq("Positive").sum()), border=True)
        st.metric("Negative or mixed", int(results["Sentiment"].isin(["Negative", "Mixed"]).sum()), border=True)
    st.dataframe(results, hide_index=True, alt="Reviews, topics, sentiment and matched words")
    st.subheader("Common topics")
    st.bar_chart(count_themes(results), alt="Number of reviews mentioning each topic")
    st.caption("One review may mention multiple topics. Blank lines and duplicate reviews are removed.")
    st.download_button("Download results CSV", results.to_csv(index=False), "feedback_results.csv", "text/csv")
    st.warning("Check important reviews yourself: keywords can miss sarcasm, context and complex negation.")
