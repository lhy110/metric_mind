import streamlit as st
import plotly.graph_objects as go
from data_generator import generate_data
from analysis import summarize, difference_ci, discover, recommend, experiment_plan
from store import store_html

st.set_page_config(page_title='MetricMind Lite · The AI Scientist', page_icon='◈', layout='wide')
st.markdown('''<style>
.block-container{max-width:1420px;padding-top:2rem;padding-bottom:3rem}
h1{letter-spacing:-1.8px;font-weight:700!important}h2{letter-spacing:-.8px}
[data-testid="stMetric"]{background:#131d2b;border:1px solid #293547;padding:18px;border-radius:13px}
[data-testid="stMetricLabel"]{color:#aab9ce} [data-testid="stMetricValue"]{font-size:2rem}
.kicker{font-size:11px;letter-spacing:2.4px;color:#8bf0c9;font-weight:700}
.sub{color:#a5b5ca;font-size:16px;max-width:760px;line-height:1.6}
.workflow{display:flex;gap:12px;margin:25px 0 28px}.step{flex:1;background:#131d2b;border:1px solid #293547;border-radius:10px;padding:14px;color:#a5b5ca;font-size:13px}.step b{color:#8bf0c9;margin-right:10px}
.callout{background:linear-gradient(110deg,#182b2a,#152034);border:1px solid #335950;border-radius:15px;padding:23px;margin:10px 0 18px}.callout h3{margin:0;padding:0 0 8px;color:#b5ffe4;font-size:21px}.callout p{color:#c0cddd;line-height:1.6;margin:0}
.pill{display:inline-block;border:1px solid #385044;border-radius:20px;padding:5px 12px;color:#8bf0c9;font-size:11px}
hr{border-color:#293547} [data-testid="stSidebar"]{border-right:1px solid #293547}
</style>''', unsafe_allow_html=True)

@st.cache_data
def load():
    return generate_data()
df=load(); summary=summarize(df); rec=recommend(df)
for key in ['objective','factors','adapted']:
    if key not in st.session_state: st.session_state[key]=False
mode=st.radio('Workspace mode', ['Demo Mode','Explore evidence'], horizontal=True, key='mode')
if mode == 'Demo Mode':
    from demo import render_demo
    render_demo(df)
    st.stop()

with st.sidebar:
    st.markdown('## ◈ MetricMind\n**LITE / SCIENTIST WORKSPACE**')
    st.divider()
    st.markdown('**Experiment**\n\nFIELD & FORM / A–B 001')
    st.caption('Synthetic retail experiment\n\n20,000 visitors · 50/50 allocation\n\nFixed seed · No API required')
    st.markdown('---\n**The question changes.**\n\nFrom “Which page converts?” to “Which outcome matters?”')
    st.caption('Living Internet Build Day\n\nOctober 10, 2026\n\nIndependent hackathon concept')
    if st.button('Reset Demo', width='stretch'):
        for key in ['objective','factors','adapted']: st.session_state[key]=False
        st.rerun()
    st.download_button('Download visitor data', df.to_csv(index=False), 'synthetic_visitors.csv','text/csv',width='stretch')

st.markdown('<div class="kicker">METRICMIND LITE / THE AI SCIENTIST FOR THE LIVING INTERNET</div>',unsafe_allow_html=True)
c1,c2=st.columns([5,1])
with c1:
    st.title('More conversions. Less value.')
    st.markdown('<div class="sub">Your website learned how to sell more. MetricMind asks whether it learned to sell better.</div>',unsafe_allow_html=True)
with c2: st.markdown('<br><span class="pill">● SYNTHETIC DEMO</span>',unsafe_allow_html=True)
st.markdown('<div class="workflow">'+''.join(f'<div class="step"><b>0{i}</b>{name}</div>' for i,name in enumerate(['Observe','Discover','Adapt','Experiment'],1))+'</div>',unsafe_allow_html=True)

st.subheader('01 / Observe the business outcome')
st.caption('A = original baseline · B = conversion-optimized website · 10,000 visitors each')
cols=st.columns(4)
for col,label,value,delta,color in zip(cols,['Conversion rate · B','Revenue / visitor · B','Average order · B','Returned orders · B'],['3.60%','$3.42','$95.00','≈12%'],['+20% relative · A 3.00%','-5% relative · A $3.60','-$25.00 · A $120','+6.94 pp · A 5%'],['normal','normal','normal','inverse']):
    col.metric(label,value,delta,delta_color=color)
st.caption('B returns: 43 / 360 orders = 11.94%. A returns: 15 / 300 = 5%. Gross revenue excludes refunds; retained revenue assumes full refunds.')
metric=st.radio('Compare outcome', ['Revenue per visitor','Conversion rate','Average order value','Return rate'],horizontal=True)
key,scale,unit={'Revenue per visitor':('rpv',1,'$'),'Conversion rate':('conversion',100,'%'),'Average order value':('aov',1,'$'),'Return rate':('return_rate',100,'%')}[metric]
a,b=summary.loc['A',key]*scale,summary.loc['B',key]*scale
fig=go.Figure(go.Bar(x=['A · Original','B · AI optimized'],y=[a,b],marker_color=['#7792b8','#8bf0c9'],text=[f'{unit}{x:.2f}' if unit=='$' else f'{x:.2f}%' for x in [a,b]],textposition='outside',width=.48))
fig.update_layout(height=290,margin=dict(l=15,r=15,t=25,b=10),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',font_color='#c8d5e5',yaxis_title=metric,showlegend=False,yaxis=dict(range=[0,max(a,b)*1.25],gridcolor='#253247'))
st.plotly_chart(fig,width='stretch')

st.subheader('02 / Discover what the headline hides')
l,r=st.columns(2)
with l:
    if st.button('Analyze Optimization Objective',type='primary',width='stretch'): st.session_state.objective=True
with r:
    if st.button('Find Overlooked Factors',width='stretch'): st.session_state.factors=True
if st.session_state.objective:
    delta,lo,hi=difference_ci(df.loc[df.variant=='A','order_value'],df.loc[df.variant=='B','order_value'])
    st.markdown('<div class="callout"><div class="kicker">OBJECTIVE MISMATCH DETECTED</div><h3>Conversion won. Revenue did not.</h3><p>B generated 60 extra orders, but $1,800 less gross revenue across the same 10,000 visitors. Smaller baskets offset the conversion gain. Optimize <b>revenue per visitor</b>, with returns as a guardrail.</p></div>',unsafe_allow_html=True)
    st.info(f'Observed revenue difference (B − A): ${delta:.2f}/visitor; approximate 95% Welch CI [${lo:.2f}, ${hi:.2f}]. This interval includes zero: the observed business outcome is worse, but this sample does not establish a population-level revenue decline.')
    st.caption(f'Retained revenue / visitor after full refunds: A ${summary.loc["A","retained_rpv"]:.2f}; B ${summary.loc["B","retained_rpv"]:.2f}. Revenue is not profit; margins and lifetime value are not modeled.')
if st.session_state.factors:
    seg=discover(df)
    st.markdown(f'<div class="callout"><div class="kicker">EXPLORATORY DISCOVERY</div><h3>{rec["target"].capitalize()} stands out.</h3><p>This segment has the largest observed revenue decline: <b>${rec["delta"]:.2f} per visitor</b>. Investigate whether discount-led messaging is shifting purchases toward lower-value products.</p></div>',unsafe_allow_html=True)
    seg['label']=seg.factor.str.replace('_',' ')+' · '+seg.segment
    g=go.Figure(go.Scatter(x=seg.delta,y=seg.label,mode='markers',marker=dict(color=['#ffb58a' if v<0 else '#8bf0c9' for v in seg.delta],size=10),error_x=dict(type='data',array=seg.ci_high-seg.delta,arrayminus=seg.delta-seg.ci_low,color='#6b809e'),customdata=seg[['n_a','n_b']],hovertemplate='%{y}<br>Δ $%{x:.2f}<br>A n=%{customdata[0]} · B n=%{customdata[1]}<extra></extra>'))
    g.add_vline(x=0,line_dash='dot',line_color='#c8d5e5')
    g.update_layout(height=390,margin=dict(l=10,r=25,t=15,b=20),xaxis_title='Gross revenue / visitor difference · B − A ($), 95% CI',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',font_color='#c8d5e5',xaxis=dict(gridcolor='#253247'),yaxis=dict(autorange='reversed'))
    st.plotly_chart(g,width='stretch')
    st.warning('Exploratory associations, not causal explanations. Segments overlap; intervals are unadjusted for multiple comparisons and ranking can exaggerate extremes. No unobserved confounder can be identified from these data. Validate the selected hypothesis in a fresh randomized experiment.')
    with st.expander('Inspect segment counts & uncertainty'):
        st.dataframe(seg.drop(columns='label').round(3),width='stretch',hide_index=True)
        st.caption('Discount sensitivity is a pre-exposure synthetic preference, not inferred from clicks or purchases in this experiment. Nuisance factors are balanced; outcomes and counts are deliberately calibrated. Intervals illustrate an independent-visitor sampling model, not evidence from real customers.')

st.subheader('03 / Adapt the experience')
st.caption('Current B storefront versus a proposed redesign. A is the measurement baseline above; these previews illustrate current B and its proposed replacement.')
if st.button('Generate Better Experience',type='primary',width='content'):
    st.session_state.objective=True; st.session_state.factors=True; st.session_state.adapted=True
    st.rerun()
if st.session_state.adapted:
    st.success(f'Design brief derived from {rec["target"]}: replace urgency with product comparison, transparent pricing, and purchase-fit guidance. Untested hypothesis; no uplift is claimed.')
l,r=st.columns(2)
with l:
    st.markdown('**BEFORE / Conversion-focused**')
    st.markdown(store_html(False),unsafe_allow_html=True)
with r:
    st.markdown('**AFTER / Value-focused hypothesis**' if st.session_state.adapted else '**AFTER / Ready to generate**')
    st.markdown(store_html(True,rec['target']) if st.session_state.adapted else '<div style="height:580px;border:1px dashed #40516a;border-radius:18px;background:#101926;display:flex;align-items:center;justify-content:center;text-align:center;color:#a5b5ca"><div style="padding:35px"><div style="font-size:44px;color:#8bf0c9">◈</div><h3>Let evidence shape the experience.</h3><p>Generate a value-focused storefront<br>from the segment diagnosis.</p></div></div>',unsafe_allow_html=True)
st.caption('Store previews are illustrative, not checkout flows. Products, prices, and marketing copy are fictional; the proposed design has no measured outcomes.')

st.subheader('04 / Design the next experiment')
if st.session_state.adapted:
    st.markdown(f'**Hypothesis:** For **{rec["target"]}** visitors, clear product value and purchase-fit guidance will increase revenue per visitor without worsening returns.')
    x,y,z=st.columns(3)
    x.markdown('**Primary metric**\n\nGross revenue per randomized visitor\n\nInclude non-buyers as $0.')
    y.markdown('**Guardrails**\n\nReturns / order · conversion rate · retained revenue / visitor')
    z.markdown('**Design**\n\nFresh sample · 50/50 randomization\n\nCurrent B versus proposed experience')
    with st.expander('Evaluation & pre-registration details',expanded=True): st.text(experiment_plan(df))
    st.download_button('Download experiment brief',experiment_plan(df),'metricmind_experiment.txt','text/plain')
else: st.info('Generate the better experience to reveal its follow-up experiment.')
with st.expander('Data provenance & statistical method'):
    st.markdown('All 20,000 records are synthetic, using seed 42. Exactly 300 A orders and 360 B orders generate $36,000 and $34,200 respectively. B has 43 returned orders, the closest integer to 12%. Each order is one visitor; returned orders receive a full refund. We assume a fully matured return window. No external services or LLM are used. “AI scientist” describes the product concept; this prototype uses transparent deterministic rules.')
    st.markdown('The planted pattern is high discount sensitivity: conversion rises from 3% to 6%, while revenue per visitor drops from $3.60 to $2.40. Low sensitivity rises from $3.60 to $4.10 despite conversion falling. Welch intervals use all visitor revenues, including zeros. They are nominal, exploratory intervals on an engineered fixture, with no multiplicity adjustment. No formal interaction or causal mechanism test is claimed.')
st.caption('METRICMIND LITE  /  Observe → Discover → Adapt → Experiment  /  Synthetic evidence. Real questions.')
