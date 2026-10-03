# Explain and demonstrate the feedback project
Problem: Customer feedback is scattered and hard to prioritize.
Input: Review ID, original text and provenance metadata.
Cleaning: Remove blank and duplicate normalized text.
Classification: Multi-label themes and four-way sentiment.
Aggregation: Unique review mentions and negative/mixed counts by theme.
Output: Dashboard, recommendations, owners, success metrics and CSVs for Power BI or Sheets.
Limitations: Synthetic fixture counts are not market findings. Keyword rules cannot understand all language.
Validation: Hand-label held-out real reviews. Use sentiment confusion matrices and precision/recall per theme.
Do not report fixture-template agreement as general accuracy.

Five-minute demo:
1. Analyze all 150 fixtures.
2. Filter negative setup feedback and inspect original evidence.
3. Compare theme mentions with unique review counts.
4. Show suggested actions and ownership.
5. Export and refresh the Power BI report.

Preparation:
Day 4: read cleaning and classification functions and trace a review.
Day 5: experiment with mixed and negated sentences; explain failure cases.
Day 6: refresh Power BI and explain its model.
Day 7: rehearse both projects and answer prioritization questions.

Describe what you personally ran and understood. Do not say the fixture was collected publicly.
