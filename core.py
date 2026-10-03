import re
import pandas as pd
from integrations import claude_json
THEMES={"setup":["setup","onboarding","configure","configuration","import","installation"],
        "pricing":["price","pricing","cost","expensive","billing","invoice","subscription","plan"],
        "bugs":["bug","crash","error","broken","freeze","slow","outage"],
        "feature requests":["feature","wish","missing","integration","export","request"]}
NEGATIVE=["difficult","confusing","expensive","crash","broken","slow","frustrating","error","missing","poor","bug","not helpful"]
POSITIVE=["easy","helpful","excellent","smooth","great","clear","affordable","reliable","love"]
ACTIONS={
 "setup":("CX","Create and test a guided setup checklist.","Time to first value"),
 "pricing":("Product + Sales","Clarify plan limits and billing before purchase.","Billing-related tickets"),
 "bugs":("Engineering","Reproduce recurring issues and prioritize by customer impact.","Recurring incidents"),
 "feature requests":("Product","Validate requested workflows before committing roadmap dates.","Demand by feature"),
 "other":("CX","Review uncategorized feedback and expand the taxonomy.","Uncategorized share")}

def prepare_reviews(frame):
    required=["review_id","text","source","source_url","is_synthetic"]
    if not set(required).issubset(frame.columns): raise ValueError("Required columns: "+", ".join(required))
    df=frame[required].fillna("").astype(str).copy()
    df=df[df.text.str.strip().ne("")].copy()
    if df.empty: raise ValueError("No non-empty reviews.")
    if df.review_id.eq("").any() or df.review_id.duplicated().any(): raise ValueError("Review IDs must be non-empty and unique.")
    df["is_synthetic"]=df.is_synthetic.str.lower()
    if not df.is_synthetic.isin(["true","false"]).all(): raise ValueError("is_synthetic must be true or false.")
    public=df.is_synthetic.eq("false")
    if (public&(~df.source_url.str.match(r"^https?://")|df.source.str.strip().eq(""))).any():
        raise ValueError("Real reviews require source name and public URL.")
    df["_normal"]=df.text.str.lower().str.replace(r"\s+"," ",regex=True).str.strip()
    return df.drop_duplicates("_normal").drop(columns="_normal").reset_index(drop=True)

def classify(text):
    lower=text.lower()
    themes=[t for t,words in THEMES.items() if any(re.search(r"\b"+re.escape(w)+r"\b",lower) for w in words)]
    negative=any(re.search(r"\b"+re.escape(w)+r"\b",lower) for w in NEGATIVE)
    positive_hits=[w for w in POSITIVE if re.search(r"\b"+w+r"\b",lower)]
    for word in list(positive_hits):
        if re.search(r"\b(?:not|never)\s+(?:very\s+)?"+word+r"\b",lower):
            negative=True
            positive_hits.remove(word)
    positive=bool(positive_hits)
    sentiment="mixed" if negative and positive else "negative" if negative else "positive" if positive else "neutral"
    return {"themes":themes or ["other"],"sentiment":sentiment,"reason":"Keyword baseline; ambiguous wording needs manual review."}

def analyze(frame,use_ai=False):
    clean=prepare_reviews(frame)
    records=[]
    for row in clean.to_dict("records"):
        result=claude_json('Classify a review. JSON: {"themes":[one or more of setup, pricing, bugs, feature requests, other],"sentiment":"positive|negative|neutral|mixed","reason":"brief explanation"}. Multiple themes are allowed.',{"text":row["text"]}) if use_ai else classify(row["text"])
        if not isinstance(result,dict) or not isinstance(result.get("themes"),list) or not result["themes"]:
            raise ValueError("Invalid classifier schema.")
        if not all(isinstance(t,str) and t in [*THEMES,"other"] for t in result["themes"]) or result.get("sentiment") not in ["positive","negative","neutral","mixed"] or not isinstance(result.get("reason"),str):
            raise ValueError("Invalid classification values.")
        records.append({**row,"themes":";".join(sorted(set(result["themes"]))),"sentiment":result["sentiment"],
                        "reason":result["reason"],"method":"Claude" if use_ai else "Keyword baseline"})
    return pd.DataFrame(records)

def summary(frame):
    exploded=frame.assign(theme=frame.themes.str.split(";")).explode("theme")
    grouped=exploded.groupby("theme").agg(mentions=("review_id","nunique"),
        negative_mentions=("sentiment",lambda x:x.isin(["negative","mixed"]).sum())).reset_index()
    grouped["negative_share"]=(grouped.negative_mentions/grouped.mentions).round(3)
    grouped["owner"]=grouped.theme.map(lambda t:ACTIONS[t][0])
    grouped["recommendation"]=grouped.theme.map(lambda t:ACTIONS[t][1])
    grouped["success_metric"]=grouped.theme.map(lambda t:ACTIONS[t][2])
    return grouped.sort_values(["negative_mentions","mentions"],ascending=False)
