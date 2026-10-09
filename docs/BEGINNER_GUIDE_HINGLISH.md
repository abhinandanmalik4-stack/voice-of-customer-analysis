# Voice of Customer: basic se interview tak

## Kyun bana rahe hain?
Maan lo 100 customers tumhara software use karte hain.
Koi kehta hai setup confusing hai, koi pricing expensive batata hai,
aur koi kehta hai app crash hoti hai.
Har review alag padhkar common problems dhoondhna time leta hai.

Voice of Customer (VoC) ka matlab customers ki needs, feedback aur complaints ko samajhna.
Hamara project reviews ko organize karta hai taaki Product aur Customer Experience teams
decide kar sakein ki kis issue ko investigate karna chahiye.

Yeh project customers ko reply nahi bhejta aur software bugs khud fix nahi karta.
Yeh feedback samajhne mein help karta hai.

## Current beginner version
1. Ek review har line mein type/paste karo.
2. Analyze reviews dabao.
3. Har review ka theme, sentiment aur matched words dekho.
4. Common topics ke counts dekho.
5. Results CSV download karo.

Prefilled ten reviews fictional practice examples hain.
Larger prototype ke 150 reviews bhi synthetic hain; unhe public reviews collected mat kehna.
Beginner analysis English keywords use karta hai, Hindi sentiment model nahi.

## Theme aur sentiment mein farq
Theme = review kis baare mein hai?
Sentiment = review mein positive/negative signal kya hai?

"The pricing is expensive."
Theme: Pricing.
Sentiment: Negative.

"Support is helpful but the app is slow."
Theme: Bugs, kyunki slow performance ka signal hai.
Sentiment: Mixed, kyunki helpful positive aur slow negative hai.

"I wish there was a calendar integration."
Theme: Feature requests.
Sentiment: Neutral under our rules, kyunki recognized sentiment word nahi hai.
Neutral ka matlab customer definitely satisfied hai aisa nahi.

One review mein setup aur pricing dono mention ho sakte hain.
Isliye theme counts ka total unique reviews se zyada ho sakta hai.

## Tools
Python: instructions likhne ki language.
Streamlit: screen, form, button aur chart banata hai.
Pandas: table aur counts handle karta hai.
Regular expression: text mein pattern/word dhoondhne ka tool.
CSV: downloadable table file.
Git: code history.
GitHub: code online host karna.
VS Code: code editor; actual app browser mein dikhegi.

## Kaise run karna hai?
VS Code: File > Open Workspace from File > Voice-of-Customer.code-workspace.
Terminal > Run Task > Run beginner feedback analyzer.
Browser: http://localhost:8502
Ya project terminal mein .\Start.cmd chalao.
Plain Python Run button use mat karo: Streamlit ko python -m streamlit run basic_app.py chahiye.
Stop: terminal mein Ctrl+C.

Current computer ka Python environment:
E:/job/placement-projects/.venv/Scripts/python.exe
Different computer par Python 3.12 aur Setup.cmd use karo,
phir Python: Select Interpreter se project ki .venv/Scripts/python.exe select karo.

## Do files pehle padho
basic_app.py = input form, Analyze button, results aur chart.
basic_analysis.py = samples, keywords, cleaning aur classification.
Other files advanced prototype ke hain, baad mein padhna.

## Data ka flow
Text input -> split into lines -> remove blank lines ->
normalize spaces -> remove duplicates -> detect themes ->
detect positive/negative clues -> results table -> chart/CSV.

Code input ko execute nahi karta. Woh sirf text ke roop mein analyze karta hai.
Analysis ke dauran koi API request ya message send nahi hota.
Results current browser session mein rehte hain; permanent copy ke liye CSV download karo.

## basic_analysis.py ka explanation
THEMES dictionary: category ke saath associated words store hote hain.
POSITIVE aur NEGATIVE lists: sentiment keywords.
contains(): full word match check karta hai.
analyze_reviews(): har line process karta hai aur results return karta hai.
seen set: repeated review ko dobara count hone se rokta hai.
casefold(): capitalization differences normalize karta hai.
Positive + negative clues = Mixed.
Sirf negative = Negative; sirf positive = Positive; neither = Neutral.
Simple not/never + positive word ko negative handle karte hain.
count_themes(): multiple themes separate karke count karta hai.

## basic_app.py ka explanation
Imports tools ko available banate hain.
st.title heading banata hai.
st.text_area reviews leta hai.
st.form input ko Analyze click tak group karta hai.
analyze_reviews review text ko results table mein badalta hai.
st.session_state last result ko reruns ke beech rakhta hai.
st.dataframe table dikhata hai.
st.bar_chart categories ke counts dikhata hai.
st.download_button CSV deta hai.

## Important limitations
Keyword rules actual language understanding nahi hain.
"Not expensive" aur sarcasm jaisi sentences galat label ho sakti hain.
Feature word praise mein bhi aa sakta hai: "export feature is great"
Feature requests label yahan broad topic bucket hai, guaranteed feature request nahi.
Source sampling biased ho sakti hai. Frequency alone business priority nahi.
High-impact bug ko low frequency ke bawajood priority mil sakti hai.
Synthetic samples se real customer behavior ya model accuracy prove nahi hoti.

## Interview explanation
Problem: scattered customer reviews mein recurring pain points dhoondhne hote hain.
Solution: Python pipeline feedback clean karti hai, themes/sentiment assign karti hai
aur results Streamlit dashboard par dikhati hai.
Design: transparent keyword baseline se start kiya; matched words inspect ho sakte hain.
Validation: empty input, duplicate reviews, multiple themes, mixed sentiment aur negation test kiye.
Limitations: nuanced language, sarcasm aur complex negation ke liye human review chahiye.

Questions:
Why remove duplicates? Repeated feedback counts ko inflate kar sakta hai.
Why mixed? Ek review mein praise aur complaint dono ho sakte hain.
Why separate theme and sentiment? Topic aur customer tone different information hain.
Why rules first? Simple, explainable aur no API cost; limitations easy to inspect.
How to improve? Manually labeled real review set, better classifier, human corrections.
How to evaluate? Sentiment confusion matrix aur per-theme precision/recall.
What are precision and recall? Predicted category kitni baar correct thi,
aur actual relevant reviews mein se kitni identify hui.
Do not claim an accuracy percentage before evaluating independent labeled examples.

## Future learning stages
1. Current rules samajhna aur examples try karna.
2. CSV import with source metadata.
3. Sentiment/theme filters and review corrections.
4. Recommendations with owners and business-impact assessment.
5. Optional Claude classification with schema checks and cost controls.
6. Google Sheets export and Power BI report.
7. Database, authentication and audit history.

Larger prototype already includes several optional features.
Start-Advanced.cmd se khulta hai. Credentials ke bina local mode use kar sakte ho.
Power BI source report included hai; Desktop rendering/refresh not yet verified.
Claude and Sheets connections need your credentials and live testing.

## First exercise
Analyze default ten examples.
Change one review to "The setup is confusing and pricing is expensive."
Predict categories and sentiment before clicking Analyze.
Paste that same line twice: unique count should count it once.
Download CSV and explain one result using its matched words.

## Git checkpoints
Har working learning stage code, relevant checks aur documentation ke saath commit hogi.
Secrets, environment folders aur runtime output Git se excluded hain.
Public repository mein confidential customer reviews upload mat karna.
