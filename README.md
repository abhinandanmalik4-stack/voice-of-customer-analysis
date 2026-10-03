# Voice of customer analysis for a SaaS product
A runnable feedback pipeline and dashboard with optional Claude and Google Sheets integrations.

## Run
Double-click Start.cmd. It uses the installed parent environment or a local .venv.
For an independent checkout: run Setup.cmd with Python 3.12, then python generate_data.py in that environment.
Tests: python -m unittest discover -s tests -v.
Analyze produces output/analyzed_reviews.csv and output/theme_summary.csv.

## Dataset
150 bundled SYNTHETIC review fixtures generated from ten templates with distinct fictional workspace contexts.
They are practice data, not scraped public reviews, and not independent samples for an accuracy benchmark.
Upload real reviews using review_id, text, source, source_url, is_synthetic columns.
Set is_synthetic=false for real reviews, and supply source name and URL.
This validates provenance metadata presence, not source authenticity or permission to reuse.
Do not use the synthetic counts as evidence of real customer needs.

## Pipeline
Validate schema and source metadata; drop blank text; normalize whitespace and remove duplicate review text.
Assign multiple themes and one sentiment: positive, negative, neutral or mixed.
Local mode is an interpretable keyword baseline with simple negation handling.
Optional Claude mode validates its JSON taxonomy. It is not run automatically.
Aggregate unique review mentions by theme and negative/mixed mentions.
Recommendations are transparent theme-based suggestions with owners and proposed success metrics.
Filters explore sentiment and themes. Review evidence stays visible.
Power BI native project: see powerbi/README.md.
Google Sheets: import output CSVs or explicitly export to a new worksheet.

## Claude
Set ANTHROPIC_API_KEY and ANTHROPIC_MODEL in the terminal used to start the app.
Only clicking Analyze in Claude mode sends reviews to the API.
Each review is one request; select a small limit first. API usage may incur charges.
Live API behavior requires your credentials and is not claimed as tested.

## Google Sheets
Create a service account, enable Sheets and Drive APIs, share the target spreadsheet with its email as Editor.
Set GOOGLE_SERVICE_ACCOUNT_FILE and GOOGLE_SHEET_ID. The export button creates a NEW worksheet.
Credentials are not bundled. Existing remote data is not overwritten.

## Limitations
Sarcasm and nuanced sentiment need manual review. Counts do not show causality.
Repeated fixture templates test mechanics, not generalization.
Multi-label theme counts can exceed review counts.
An API/network error prevents recording partial classification output.
Single-user local prototype; production needs permissions, storage and reviewer audit history.

Official references:
https://docs.streamlit.io/develop/api-reference
https://platform.claude.com/docs/en/api/python/messages/create
https://docs.gspread.org/en/latest/oauth2.html
https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview
