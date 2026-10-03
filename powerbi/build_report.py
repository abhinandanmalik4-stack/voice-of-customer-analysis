"""Generate a portable source-controlled Power BI report; rerun after moving the repository."""
import json
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"powerbi"
BASE="https://developer.microsoft.com/json-schemas/fabric/item/report/definition/"
def write(path,obj):
    path=OUT/path
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2),encoding="utf-8")
def schema(kind,version): return BASE+kind+"/"+version+"/schema.json"
tables=[]
for name,filename in [("Reviews","analyzed_reviews.csv"),("Themes","theme_summary.csv")]:
    df=pd.read_csv(ROOT/"output"/filename)
    cols=[]
    conversions=[]
    for col in df.columns:
        numeric=col in ["mentions","negative_mentions","negative_share"]
        dtype="double" if col=="negative_share" else "int64" if numeric else "string"
        cols.append({"name":col,"dataType":dtype,"sourceColumn":col,"summarizeBy":"sum" if numeric else "none"})
        conversions.append('{'+json.dumps(col)+', '+("type number" if col=="negative_share" else "Int64.Type" if numeric else "type text")+'}')
    source=str(ROOT/"output"/filename).replace("\\","/")
    expression=['let',
        '    Source = Csv.Document(File.Contents('+json.dumps(source)+'), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
        '    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
        '    Typed = Table.TransformColumnTypes(Headers, {'+", ".join(conversions)+'})',
        'in Typed']
    measures=([{"name":"Review count","expression":"DISTINCTCOUNT(Reviews[review_id])","formatString":"0"},
        {"name":"Negative or mixed","expression":'CALCULATE([Review count], Reviews[sentiment] IN {"negative", "mixed"})',"formatString":"0"}]
        if name=="Reviews" else [
        {"name":"Mentions","expression":"SUM(Themes[mentions])","formatString":"0"},
        {"name":"Negative mentions","expression":"SUM(Themes[negative_mentions])","formatString":"0"}])
    tables.append({"name":name,"columns":cols,"measures":measures,
        "partitions":[{"name":name,"mode":"import","source":{"type":"m","expression":expression}}]})
write(Path("VOC.SemanticModel/model.bim"),{"name":"VOC","compatibilityLevel":1567,
    "model":{"culture":"en-US","defaultPowerBIDataSourceVersion":"powerBI_V3",
             "tables":tables,"annotations":[{"name":"PBI_QueryOrder","value":json.dumps(["Reviews","Themes"])}]}})
write(Path("VOC.SemanticModel/definition.pbism"),{"version":"1.0","settings":{}})
write(Path("VOC.pbip"),{"version":"1.0","artifacts":[{"report":{"path":"VOC.Report"}}],"settings":{"enableAutoRecovery":True}})
write(Path("VOC.Report/definition.pbir"),{"version":"4.0","datasetReference":{"byPath":{"path":"../VOC.SemanticModel"}}})
write(Path("VOC.Report/definition/version.json"),{"$schema":schema("versionMetadata","1.0.0"),"version":"2.0.0"})
write(Path("VOC.Report/definition/report.json"),{"$schema":schema("report","3.1.0"),"themeCollection":{}})
pages=["Overview","Actions","Evidence"]
write(Path("VOC.Report/definition/pages/pages.json"),{"$schema":schema("pagesMetadata","1.0.0"),
    "pageOrder":pages,"activePageName":"Overview"})
for p in pages:
    write(Path("VOC.Report/definition/pages")/p/"page.json",
        {"$schema":schema("page","2.0.0"),"name":p,
         "displayName":p+" | Synthetic practice data","displayOption":"FitToPage","height":720,"width":1280})
def field(table,col,measure=False):
    expr={"Measure" if measure else "Column":{"Expression":{"SourceRef":{"Entity":table}},"Property":col}}
    return {"field":expr,"queryRef":table+"."+col,"nativeQueryRef":col}
def visual(page,name,type,roles,x,y,w,h):
    write(Path("VOC.Report/definition/pages")/page/"visuals"/name/"visual.json",
        {"$schema":schema("visualContainer","2.1.0"),"name":name,
         "position":{"x":x,"y":y,"z":0,"width":w,"height":h,"tabOrder":0},
         "visual":{"visualType":type,"query":{"queryState":{role:{"projections":items} for role,items in roles.items()}}}})
visual("Overview","ReviewsCard","card",{"Values":[field("Reviews","Review count",True)]},30,20,280,110)
visual("Overview","NegativeCard","card",{"Values":[field("Reviews","Negative or mixed",True)]},330,20,280,110)
visual("Overview","Sentiment","clusteredColumnChart",{"Category":[field("Reviews","sentiment")],"Y":[field("Reviews","Review count",True)]},30,160,580,480)
visual("Overview","ThemeMentions","clusteredBarChart",{"Category":[field("Themes","theme")],"Y":[field("Themes","Mentions",True),field("Themes","Negative mentions",True)]},650,160,590,480)
visual("Actions","ActionTable","tableEx",{"Values":[field("Themes",c) for c in ["theme","mentions","negative_mentions","negative_share","owner","recommendation","success_metric"]]},30,30,1210,640)
visual("Evidence","SentimentFilter","slicer",{"Values":[field("Reviews","sentiment")]},30,20,1210,100)
visual("Evidence","EvidenceTable","tableEx",{"Values":[field("Reviews",c) for c in ["review_id","text","themes","sentiment","source","source_url","is_synthetic","method"]]},30,150,1210,520)
print("Generated Power BI project with three pages and seven visuals.")
