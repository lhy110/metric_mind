"""Transparent deterministic analysis. Intervals are exploratory model-based summaries."""
import numpy as np
import pandas as pd
from scipy import stats

FACTORS = ['discount_sensitivity', 'device', 'traffic_source', 'visitor_type']


def summarize(df):
    rows = []
    for variant, g in df.groupby('variant'):
        orders = int(g.converted.sum())
        rows.append(dict(variant=variant, visitors=len(g), orders=orders,
            conversion=orders/len(g), rpv=g.order_value.mean(),
            aov=g.order_value.sum()/orders, return_rate=g.returned.sum()/orders,
            returns=int(g.returned.sum()), retained_rpv=g.retained_revenue.mean()))
    return pd.DataFrame(rows).set_index('variant')


def difference_ci(a, b, alpha=.05):
    """B minus A; independent visitor-level Welch interval including zero purchases."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    va, vb = a.var(ddof=1)/len(a), b.var(ddof=1)/len(b)
    se = np.sqrt(va+vb)
    delta = b.mean()-a.mean()
    if se == 0:
        return float(delta), float(delta), float(delta)
    dof = (va+vb)**2/(va**2/(len(a)-1)+vb**2/(len(b)-1))
    margin = stats.t.ppf(1-alpha/2, dof)*se
    return float(delta), float(delta-margin), float(delta+margin)


def discover(df):
    rows = []
    for factor in FACTORS:
        for level, g in df.groupby(factor):
            a, b = g[g.variant=='A'], g[g.variant=='B']
            delta, low, high = difference_ci(a.order_value, b.order_value)
            rows.append(dict(factor=factor, segment=level, n_a=len(a), n_b=len(b),
                orders_a=int(a.converted.sum()), orders_b=int(b.converted.sum()),
                rpv_a=a.order_value.mean(), rpv_b=b.order_value.mean(),
                delta=delta, ci_low=low, ci_high=high,
                conversion_delta=100*(b.converted.mean()-a.converted.mean())))
    return pd.DataFrame(rows).sort_values('delta').reset_index(drop=True)


def recommend(df):
    s = summarize(df)
    segments = discover(df)
    worst = segments.iloc[0]
    return dict(wrong_metric=bool(s.loc['B','conversion']>s.loc['A','conversion'] and s.loc['B','rpv']<s.loc['A','rpv']),
                factor=worst.factor, segment=worst.segment, delta=float(worst.delta),
                primary='Gross revenue per randomized visitor',
                target=f'{worst.segment} {worst.factor.replace("_", " ")}')


def experiment_plan(df):
    r = recommend(df)
    return f'''FOLLOW-UP EXPERIMENT — MetricMind Lite
Target: {r['target']} (identified before exposure).
Hypothesis: replacing blanket discount messaging with clear product value, a guided comparison, and transparent pricing will improve revenue per visitor in this segment without worsening returns.
Control: current B experience. Treatment: proposed value-focused experience.
Randomization: 50/50 by persistent visitor ID; one assignment per visitor; same traffic allocation and measurement window. Do not target using behavior caused by treatment.
Primary: {r['primary']}, including non-buyers as zero.
Guardrails: return rate per order (maximum +2 percentage points), conversion rate (maximum -0.5 percentage points), and retained revenue per visitor after full refunds (maximum -$0.10). These are proposed tolerances to agree before launch.
Evaluation: pre-register a fixed horizon and sample size using pilot variance, a business-selected minimum detectable revenue difference, 80% power, and two-sided alpha 0.05. Use an independent new sample. Allow every order a full 30-day return window; assume full refunds for this demo. Compare intention-to-treat visitor-level revenue with a 95% Welch interval; use suitable proportion intervals for order returns and conversion. Ship only if the revenue interval is above zero and one-sided 95% guardrail bounds satisfy all pre-agreed tolerances; otherwise keep control or call it inconclusive. No repeated peeking or early stopping without a sequential design.
Interpretation: exploratory segment associations generated this hypothesis. They do not establish a causal mechanism or reveal unobserved confounders. No redesign uplift has been measured.
'''
