"""Validate generated PBIR schemas. Requires network access to Microsoft's schema service."""
import json
from pathlib import Path
import requests
from jsonschema import Draft7Validator, RefResolver
ROOT=Path(__file__).resolve().parent
cache={}
def fetch(url):
    if url not in cache:
        r=requests.get(url.replace("schema.embedded.json", "schema-embedded.json"),timeout=30)
        r.raise_for_status()
        cache[url]=r.json()
    return cache[url]
count=0
for path in (ROOT/"VOC.Report"/"definition").rglob("*.json"):
    obj=json.loads(path.read_text(encoding="utf-8"))
    if "$schema" not in obj: continue
    url=obj["$schema"]
    doc=fetch(url)
    resolver=RefResolver(base_uri=url,referrer=doc,handlers={"https":fetch})
    errors=list(Draft7Validator(doc,resolver=resolver).iter_errors(obj))
    if errors:
        for error in errors: print(path.name,list(error.path),error.message)
        raise SystemExit(1)
    count+=1
print("Validated",count,"Power BI report definition files.")

