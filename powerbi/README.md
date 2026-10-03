# Native Power BI report
Open VOC.pbip with Power BI Desktop, then Refresh to load the generated CSV data.
The source-controlled report uses PBIR and a model.bim import model.
It includes Overview (review cards, sentiment and themes), Actions (recommendations), and Evidence (original text with sentiment slicer).

The report definition files are validated against Microsoft's public JSON schemas.
Rendering and refresh inside Power BI Desktop are not automatically verified here.
If Desktop requires project-format features, enable the relevant option in its settings and restart.

Data paths point to this local repository. After moving the repository, run:
python generate_data.py
python powerbi/build_report.py
Then reopen VOC.pbip and Refresh.
This rebuild overwrites generated report files, so preserve manual report edits first.

Reviews and Themes are separate tables: sentiment filtering applies to Reviews.
Themes is a preaggregated snapshot and does not respond to Reviews filters.
The app's theme/sentiment filters recompute counts, while the report shows the saved snapshot.
Synthetic practice data is identified in every page name and review row.

Fallback if your Desktop version rejects the generated model:
Get Data > Text/CSV for output/analyzed_reviews.csv and output/theme_summary.csv.
Add Review count = DISTINCTCOUNT(Reviews[review_id]).
Add Negative or mixed = CALCULATE([Review count], Reviews[sentiment] IN {"negative", "mixed"}).
Create a sentiment column chart, a theme mentions bar chart, a recommendations table and a review evidence table.
Save the report after checking its visual fields.

Reference: https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report
