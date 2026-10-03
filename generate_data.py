import pandas as pd
from integrations import ROOT,save_csv
from core import analyze,summary
TEMPLATES=[
 ("The setup was confusing; the import screen needs clear instructions.","setup","mixed"),
 ("Onboarding was smooth and the setup guide was helpful.","setup","positive"),
 ("The subscription is expensive and pricing limits are confusing.","pricing","negative"),
 ("The plan is affordable and billing details are clear.","pricing","positive"),
 ("A crash during report generation caused a frustrating error.","bugs","negative"),
 ("The dashboard is slow, although the support team is helpful.","bugs","mixed"),
 ("I wish there was an export feature and a calendar integration.","feature requests","neutral"),
 ("The missing integration makes our workflow difficult.","feature requests","negative"),
 ("The team was helpful and the product is reliable.","other","positive"),
 ("The report displays account activity each week.","other","neutral")]
def generate():
    rows=[]
    for i in range(150):
        text,theme,sentiment=TEMPLATES[i%len(TEMPLATES)]
        rows.append({"review_id":f"SYN-{i+1:03}","text":text+f" Context: fictional workspace {i+1}.",
            "source":"Generated portfolio practice data","source_url":"","is_synthetic":"true",
            "expected_theme":theme,"expected_sentiment":sentiment})
    raw=pd.DataFrame(rows)
    save_csv(raw,ROOT/"data"/"sample_reviews.csv")
    result=analyze(raw)
    save_csv(result,ROOT/"output"/"analyzed_reviews.csv")
    save_csv(summary(result),ROOT/"output"/"theme_summary.csv")
    return result
if __name__=="__main__":
    print("Generated",len(generate()),"synthetic review fixtures.")
