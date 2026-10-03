import pandas as pd
import streamlit as st
from integrations import ROOT,save_csv,push_sheet
from core import analyze,summary

st.set_page_config(page_title="Voice of customer",page_icon=":material/forum:",layout="wide")
st.title("Voice of customer analysis")
st.caption("Themes, sentiment and proposed actions for Product and CX")
st.warning("The bundled 150 reviews are generated practice data, not collected public reviews.")
mode=st.sidebar.radio("Classification",["Local keyword baseline","Claude API"])
if mode=="Claude API": st.sidebar.info("Analyze sends one API request per review to Claude. Start with a small sample; charges may apply.")
upload=st.file_uploader("Import review CSV",type="csv")
try: raw=pd.read_csv(upload if upload else ROOT/"data"/"sample_reviews.csv",dtype=str,keep_default_na=False)
except Exception:
    st.error("Could not read review CSV. Run generate_data.py if the sample file is missing.")
    st.stop()
st.caption("Required columns: review_id, text, source, source_url, is_synthetic. Real reviews require public source URLs.")
st.dataframe(raw.head(8),hide_index=True,alt="Review input preview")
limit=st.number_input("Maximum reviews to analyze",min_value=1,max_value=max(1,len(raw)),value=min(150,max(1,len(raw))))
if st.button("Analyze reviews",type="primary",key="analyze"):
    try:
        with st.spinner("Analyzing reviews"):
            result=analyze(raw.head(int(limit)),mode=="Claude API")
        save_csv(result,ROOT/"output"/"analyzed_reviews.csv")
        save_csv(summary(result),ROOT/"output"/"theme_summary.csv")
        st.session_state["result"]=result
        st.success("Saved CSVs for Google Sheets and Power BI.")
    except Exception as e: st.error(str(e) if isinstance(e,ValueError) else "Analysis failed; check configuration and connection. "+type(e).__name__)
if "result" not in st.session_state:
    st.info("Click Analyze reviews to build the dashboard.")
    st.stop()
result=st.session_state["result"]
if result.is_synthetic.eq("true").any(): st.info("This result contains synthetic reviews. Its counts are practice outputs, not market evidence.")
themes=sorted({t for item in result.themes for t in item.split(";")})
selected=st.multiselect("Themes",themes,default=themes,key="themes")
sentiments=st.multiselect("Sentiments",["positive","negative","neutral","mixed"],default=["positive","negative","neutral","mixed"],key="sentiments")
filtered=result[result.themes.map(lambda x:bool(set(x.split(";"))&set(selected)))&result.sentiment.isin(sentiments)]
with st.container(horizontal=True):
    st.metric("Unique reviews",len(filtered),border=True)
    st.metric("Negative or mixed",int(filtered.sentiment.isin(["negative","mixed"]).sum()),border=True)
    st.metric("Theme categories",len({t for x in filtered.themes for t in x.split(";")}),border=True)
if filtered.empty:
    st.info("No reviews match these filters.")
    st.stop()
stats=summary(filtered)
left,right=st.columns(2)
with left:
    st.subheader("Recurring themes")
    st.bar_chart(stats.set_index("theme")[["mentions","negative_mentions"]],alt="Theme mentions and negative feedback counts")
with right:
    st.subheader("Sentiment")
    st.bar_chart(filtered.sentiment.value_counts(),alt="Review count by sentiment")
st.caption("Reviews may have multiple themes; theme mentions can exceed the number of unique reviews.")
st.subheader("Suggested actions")
st.dataframe(stats,hide_index=True,alt="Recommendations with owners and success metrics")
st.subheader("Evidence and classification")
st.dataframe(filtered,hide_index=True,alt="Reviews and classification evidence")
st.download_button("Download classified reviews",result.to_csv(index=False),"analyzed_reviews.csv","text/csv")
st.download_button("Download theme summary",summary(result).to_csv(index=False),"theme_summary.csv","text/csv")
name=st.text_input("New Google Sheets worksheet",value="VOC analysis")
if st.button("Upload full analysis to Google Sheets"):
    try: st.link_button("Open worksheet",push_sheet(result,name))
    except Exception as e: st.error(str(e) if isinstance(e,ValueError) else "Upload failed; check credentials and sharing.")
