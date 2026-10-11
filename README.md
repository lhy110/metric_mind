# MetricMind Lite — The AI Scientist for the Living Internet

A complete offline Streamlit hackathon demo: **Observe → Discover → Adapt → Experiment**.
Built for the October 10, 2026 Living Internet Build Day. Independent concept, not an official Coframe integration.

## Page 0 — Coframe and the customer

The app now opens with Coframe’s positioning, the fictional Field & Form customer, and the proposed complementary workflow. Click **Start the customer experiment** to enter the original four-stage presentation. Back from stage 1 and Reset return to the story. This is not an actual Coframe integration or customer case study.

## Human co-steering

Stage 2 includes an editable business brief. Stage 3 carries that brief forward and adds a ChatGPT-ready design prompt, a **Generate human-steered design** button, and an immediate preview. Stage 4 uses the generated design and attaches its exact input prompts to the experiment brief. Reset clears prompts and generated state.

This remains API-free: the local interpreter understands explicit directives, not arbitrary natural-language requests. Supported lines:

```text
Focus: budget
Tone: bold
Headline: Buy only what you need
CTA: Compare my options
```

Focus accepts `fit`, `budget`, or `durability`; Tone accepts `calm` or `bold`. Optional Headline and CTA are literal copy overrides, escaped before display. Design-prompt directives override business-brief directives. Other prose is included in the downloadable ChatGPT-ready prompt but does not change the local rendering. No ChatGPT request is made. Review human-authored claims before a real experiment. Metrics and statistical conclusions remain fixed; asking for a different objective in free text does not silently change the measurement plan.

Go back to edit a prompt and regenerate; pending changes are labeled while the last generated design remains visible. The walkthrough can still skip editing and use the default brief.

## Public hosting

See **[DEPLOY.md](DEPLOY.md)** for Streamlit Community Cloud deployment and alternative Python/Docker hosting. The default Demo Mode works unchanged on a public URL and on Android browsers. This package is hosting-ready; no live deployment has been created.

## Run on Windows (PowerShell)

Python 3.12 recommended. Extract the updated archive into a fresh folder, then:

```powershell
cd metricmind_v2
python -m venv mm
.\mm\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

If PowerShell blocks activation, skip activation and use:

```powershell
.\mm\Scripts\python.exe -m pip install -r requirements.txt
.\mm\Scripts\python.exe -m streamlit run app.py
```

For an existing `mm` environment, just activate it, install requirements, and launch. Open http://localhost:8501. Initial dependency installation needs internet; the running demo does not need APIs, keys, fonts or image services.

macOS/Linux: `python3 -m venv mm`, then `source mm/bin/activate`, followed by the same pip and Streamlit commands.

## 90-second Demo Mode (opens by default)

Use the green next button to advance. Back revisits evidence; **Reset Demo** returns to stage one. **Explore evidence** preserves the full interactive dashboard.

1. **0–15 seconds — Apparent win:** “The AI increased conversion by 20%. Most dashboards would celebrate. MetricMind asks one more question.”
2. **15–35 seconds — Business check:** “Revenue per visitor fell 5%. The result is uncertain, but conversion alone is clearly an incomplete scorecard.”
3. **35–60 seconds — Overlooked factor:** “We scanned four measured factors. Discount-sensitive shoppers bought twice as often, but their purchases were smaller. Now we have a specific, testable design brief.”
4. **60–90 seconds — Next experiment:** “The system proposes a better experience and tells us exactly how to test it. Humans can inspect the evidence before accepting the idea.”

The presentation follows the principle **simple explanation, inspectable evidence, testable action**. Complexity is available in audit expanders rather than imposed on the audience. The 90 seconds are suggested pacing, not a timer or auto-advance.

The stage-four previews are **current B** and **proposed C**; A is the original measurement baseline. C has not been tested. Both previews use isolated CSS so their colors cannot overwrite each other. The store is illustrative, not a checkout application.

## Files

- `demo.py`: four-stage guided presentation with evidence audit and speaker cues.
- `app.py`: light dashboard, Plotly charts, workflow state, downloads, and experiment panel.
- `data_generator.py`: seeded visitor-level dataset; run `python data_generator.py` to recreate the included CSV.
- `analysis.py`: summaries, independent-sample Welch intervals, segment scan, deterministic diagnosis and experiment brief.
- `store.py`: offline CSS storefront illustrations and diagnosis-directed redesign.
- `.streamlit/config.toml`: light theme and disabled usage telemetry.
- `test_app.py`: accounting, discovery, storefront, and Streamlit interaction tests.
- `test_results.txt`: results from the final test run.
- `requirements.txt`: exact versions tested in the build environment.
- `synthetic_visitors.csv`: all 20,000 visitor records.

## Mathematical consistency

| Measure | A | B |
|---|---:|---:|
| Visitors | 10,000 | 10,000 |
| Orders | 300 | 360 |
| Conversion | 3.00% | 3.60% |
| Gross revenue | $36,000 | $34,200 |
| Revenue / visitor | $3.60 | $3.42 |
| Average order value | $120 | $95 |
| Returned orders | 15 | 43 |
| Return rate per order | 5% | 11.94% (approximately 12%) |

Exactly 12% of 360 orders would be 43.2 orders, which is impossible for binary returns; 43 is the nearest integer. Monetary values use cents, and generated order totals match the scenario exactly (up to floating-point representation). Return rates use purchasers as denominator; revenue per visitor includes every visitor. Retained revenue subtracts the full value of each returned order; it is not profit.

### Planted pattern

Each arm contains 4,000 high-sensitivity and 6,000 low-sensitivity visitors. Discount sensitivity is defined before exposure. High sensitivity has 120 A orders versus 240 B orders, with revenue $14,400 versus $9,600. Low sensitivity has 180 versus 120 orders, with revenue $21,600 versus $24,600. These jointly recover the exact aggregate values. Device, source, and new/returning status are balanced nuisance variables, randomly permuted within each arm/segment. The complete fixture deliberately fixes outcomes and counts; it is not a Monte Carlo simulation of random assignment.

### Statistical limits

The revenue intervals are visitor-level Welch t intervals, including zero revenue for non-buyers. They illustrate an independent-visitor sampling model on synthetic data. Segment intervals are exploratory, unadjusted for multiple comparisons, and based on overlapping segments. Selecting the worst segment introduces selection bias; confirm it in fresh data. This is not a formal treatment-interaction test. Associations do not establish a causal mechanism, and the app does not discover unobserved confounders. Overall observed revenue declines, but its 95% interval includes zero; the app explicitly calls the result inconclusive at population level.

The prototype's “AI scientist” is a product concept implemented with transparent deterministic logic. It scans factors rather than choosing a random redesign. For this fixture, high discount sensitivity is selected, leading to value/fit/price transparency changes. Product prices and marketing content are fictional. The mock store is a visual preview, not an ecommerce checkout.

The next experiment specifies a fresh persistent-visitor 50/50 assignment, preregistration, pilot-based sample sizing, a matured 30-day return window, and guardrail tolerances. Suggested tolerances require business agreement before launch; no real-world uplift is assumed. Revenue is not necessarily the best objective for every business: contribution margin and lifetime value are outside this minimal demo.

## Verification

```bash
python -m unittest -v test_app.py
```

The tests cover exact accounting, discovery ranking and decomposition, all four guided stages, back/reset, every explorer button and chart choice, generated experiment text, and isolated storefront CSS. Streamlit server startup and HTTP root/health endpoints were checked successfully. Browser rendering was attempted, but the browser preview service does not contain a Python runtime and could not launch Streamlit. Browser visual inspection remains unverified. The actual app was executed via Streamlit AppTest and a local server health check; this is not a screenshot review.

## Light presentation refresh

The interface uses a light background, white panels and teal accents. Page 0 is now a short visual customer story and proposed Coframe → MetricMind → human review workflow. Source and scope details remain in an expander. The startup file remains `app.py`. If a saved Streamlit appearance preference overrides the theme, choose Light in Settings.
