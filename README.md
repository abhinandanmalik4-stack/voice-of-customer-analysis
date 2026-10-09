# Voice of Customer Analysis

A Python and Streamlit portfolio project that organizes customer feedback into topics and sentiment, helping Product and Customer Experience teams inspect recurring issues.

**Start with the beginner app:** paste one English review per line, analyze it, inspect the matched words, and download the results. It runs locally without an API key.

[Hinglish learning guide](docs/BEGINNER_GUIDE_HINGLISH.md) · [Interview walkthrough](docs/INTERVIEW.md) · [Power BI setup](powerbi/README.md)

## Why this project?

A SaaS business can receive feedback such as “setup is confusing,” “pricing is expensive,” and “the app crashes.” Reading feedback individually makes it harder to notice repeated problems.

This project groups feedback so a coordinator can ask:

- What topics appear repeatedly?
- Which reviews contain negative or mixed feedback?
- What original evidence supports an observation?
- Which team should investigate the issue?

It supports analysis and prioritization; it does not reply to customers or fix product issues automatically.

## Example

| Customer review | Topic | Sentiment in the beginner rules |
|---|---|---|
| The setup is easy and the guide is helpful. | Setup | Positive |
| The pricing is expensive. | Pricing | Negative |
| Support is helpful but the app is slow. | Bugs | Mixed |
| I wish there was a calendar integration. | Feature requests | Neutral |

Theme describes **what a review discusses**. Sentiment describes its recognized positive or negative clues. Neutral means no sentiment keyword matched; it does not prove the customer is satisfied.

## Two learning levels

| Capability | Beginner: basic_app.py | Extended: app.py |
|---|---|---|
| Input | One review per line | Review CSV with source metadata |
| Sample data | 10 fictional examples | 150 synthetic review fixtures |
| Classification | Local keyword rules | Local rules or optional Claude API |
| Results | Themes, sentiment and matched clues | Themes, sentiment, reasons and method |
| Exploration | Summary counts and topic chart | Theme and sentiment filters |
| Export | Download result CSV | CSV files, optional Google Sheets export |
| Follow-up | Inspect the original review | Suggested actions, owners and success metrics |
| Power BI | Not required | Included report source files |

The beginner app keeps results in the current browser session. Download the CSV to retain them. The extended app writes outputs to the local output folder.

## Run on Windows

### Existing local workspace

1. Open **Voice-of-Customer.code-workspace** in VS Code.
2. Select **Terminal → Run Task → Run beginner feedback analyzer**.
3. Open **http://localhost:8502** if the browser does not open automatically.
4. Keep the terminal running while using the app. Press **Ctrl+C** to stop.

You can also double-click **Start.cmd**.

### Fresh clone

Install Python 3.12, then run these commands in PowerShell:

~~~powershell
git clone https://github.com/abhinandanmalik4-stack/voice-of-customer-analysis.git
cd voice-of-customer-analysis
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run basic_app.py --server.port 8502
~~~

In VS Code, use **Python: Select Interpreter** to select your new local environment. The checked-in default interpreter path points to the shared parent environment used on the original development machine; select your local interpreter when cloning elsewhere.

Use **Start-Advanced.cmd** for the extended app. Both launchers prefer a local .venv and fall back to the development machine's parent .venv.

Do not run basic_app.py using the ordinary Python file button. Streamlit requires **python -m streamlit run basic_app.py**.

## How the beginner analysis works

1. Split the input into lines.
2. Ignore blank lines.
3. Normalize whitespace and capitalization for matching.
4. Remove duplicate normalized reviews.
5. Look for complete keywords associated with each topic.
6. Find positive and negative sentiment clues.
7. Handle simple “not/never + positive word” phrases.
8. Build a results table and count topic mentions.

Both positive and negative clues produce **Mixed**. Negative clues alone produce **Negative**, positive clues alone produce **Positive**, and neither produces **Neutral**.

A review can have several topics. Consequently, total topic mentions can exceed the number of unique reviews.

## Project structure

~~~text
basic_app.py                   Beginner interface
basic_analysis.py              Keyword rules, sample reviews and counts
app.py                         Extended dashboard
core.py                        Extended cleaning, classification and summaries
integrations.py                Claude, Google Sheets and CSV helpers
generate_data.py               Synthetic fixture/output generator
data/sample_reviews.csv        150 synthetic fixtures
powerbi/                       Power BI source report and generator
tests/                         Business-rule and interface checks
docs/                          Hinglish explanations and interview notes
.vscode/                       Run task and debugging configuration
~~~

Study **basic_app.py** and **basic_analysis.py** first. Screen code is separated from analysis so business rules can be tested independently of the interface.

## Data provenance

All bundled examples are **synthetic practice data**. The 150-review dataset uses ten templates with fictional workspace contexts; it is not a collection of public reviews or an independent accuracy benchmark.

For the extended app, an imported review CSV needs:

| Column | Meaning |
|---|---|
| review_id | Unique, non-empty review identifier |
| text | Original review text |
| source | Where the review came from |
| source_url | Public source URL for real reviews |
| is_synthetic | true for generated data, false for real reviews |

Real reviews require a source name and URL. These checks validate metadata presence, not source authenticity or reuse permission. Keep confidential customer feedback out of this public repository.

## Optional integrations

### Claude API

Set **ANTHROPIC_API_KEY** and **ANTHROPIC_MODEL** in the environment used to start the extended app. Choose a model available in your account.

Selecting Claude mode and clicking Analyze sends review text to the API. Each review generates one request; start with a small sample. API usage may incur charges. Returned classifications are checked against the expected taxonomy.

The beginner app makes no API calls. Live Claude behavior has not been verified with user credentials.

### Google Sheets

The extended app can create a new worksheet in a spreadsheet shared with your Google service account.

Configure **GOOGLE_SERVICE_ACCOUNT_FILE** and **GOOGLE_SHEET_ID** after enabling the Sheets and Drive APIs. Existing worksheet names are rejected. You can also import downloaded CSVs manually.

Live service-account export requires your credentials and has not been verified here.

### Power BI

The source project includes Overview, Actions and Evidence pages. See [Power BI instructions](powerbi/README.md).

Before opening the report in a fresh clone, generate the local output CSVs and rebuild its local source paths:

~~~powershell
.\.venv\Scripts\python.exe generate_data.py
.\.venv\Scripts\python.exe powerbi\build_report.py
~~~

Then open powerbi/VOC.pbip and refresh in Power BI Desktop. Rebuilding overwrites generated report files, so preserve any manual report edits first.

Thirteen report definition files passed schema validation. Rendering and refresh in Power BI Desktop remain unverified. The Themes table is a preaggregated snapshot and does not respond to filters on the separate Reviews table.

## Testing

~~~powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
~~~

**14 automated tests passed** for the beginner and extended applications. They cover empty input, duplicate removal, source metadata, multiple topics, mixed sentiment, basic negation, invalid AI responses, summaries, and interface interactions.

These tests establish expected behavior for selected cases. They are not a measurement of classification accuracy on real customer reviews.

## Limitations

- Keywords can miss context, sarcasm and complex negation, such as “not expensive.”
- Feature-related praise may enter the broad Feature requests bucket; inspect the text before assuming it requests a new feature.
- English keywords do not provide multilingual sentiment understanding.
- Frequency alone does not establish business impact or priority.
- Synthetic data demonstrates the workflow, not real market findings.
- This is a local prototype without authentication or a production database.

## Future additions

1. Human corrections and a review audit trail.
2. Better handling of negation and context.
3. Evaluation against independent, manually labeled real reviews.
4. Optional AI classification with cost controls.
5. Priority scoring that combines frequency with severity and customer impact.
6. Database storage, access permissions and a shared team workflow.

Several optional capabilities already exist in the extended prototype. The learning path introduces them gradually.

## Interview explanation

“I built a customer feedback analysis prototype that cleans reviews, assigns topics and sentiment, and displays recurring issues in a Streamlit dashboard. I started with transparent keyword rules so the classification clues can be inspected. The bundled data is synthetic, and contextual language remains a limitation. A next step is evaluation on independently labeled real feedback.”

Use this explanation only after running the project and understanding its processing steps. Do not claim public-review collection, live integration testing, or an accuracy percentage without evidence.

## References

- [Streamlit documentation](https://docs.streamlit.io/develop/api-reference)
- [Claude Messages API](https://platform.claude.com/docs/en/api/python/messages/create)
- [gspread authentication](https://docs.gspread.org/en/latest/oauth2.html)
- [Power BI projects](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview)
