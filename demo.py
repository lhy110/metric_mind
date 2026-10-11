"""Progressive disclosure: a 90-second evidence-to-experiment story."""
import streamlit as st
import plotly.graph_objects as go
from analysis import summarize, discover, recommend, difference_ci, experiment_plan
from store import store_html
from steering import DEFAULT_BUSINESS, DEFAULT_DESIGN, generate_design, export_prompt


def reset():
    st.session_state.stage = 0
    for key in ['business_brief','design_prompt','generated_design','generated_source','business_editor','design_editor']:
        st.session_state.pop(key,None)
    for k in ['objective','factors','adapted']: st.session_state[k] = False


def move(step):
    st.session_state.stage = min(4,max(0,st.session_state.stage+step))


def save_editor(widget, destination):
    st.session_state[destination] = st.session_state[widget]


def steering_source():
    return (st.session_state.business_brief, st.session_state.design_prompt)


def chart(values, labels, unit, colors=None):
    fig=go.Figure(go.Bar(x=labels,y=values,marker_color=colors or ['#8096b7','#087f6d'],width=.5,
        text=[f'${v:.2f}' if unit=='$' else f'{v:.2f}%' for v in values],textposition='outside'))
    fig.update_layout(height=255,margin=dict(l=10,r=10,t=35,b=10),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',font=dict(color='#33485e',size=15),yaxis=dict(range=[0,max(values)*1.25],gridcolor='#e1e7ef',title='Revenue / visitor ($)' if unit=='$' else 'Conversion (%)'),xaxis=dict(fixedrange=True),showlegend=False)
    return fig


def render_demo(df):
    if 'stage' not in st.session_state: st.session_state.stage=0
    st.session_state.setdefault('business_brief',DEFAULT_BUSINESS)
    st.session_state.setdefault('design_prompt',DEFAULT_DESIGN)
    stage=st.session_state.stage; s=summarize(df); a,b=s.loc['A'],s.loc['B']; r=recommend(df)
    st.markdown('''<style>.demo-hero{background:radial-gradient(ellipse at top right,#d1eee177,transparent 65%),#ffffff;border:1px solid #d5e2e9;border-radius:20px;padding:24px 32px;margin:8px 0 18px}.demo-number{font-size:76px;font-weight:750;letter-spacing:-4px;line-height:1.1;color:#087f6d}.demo-label{color:#526478;font-size:15px;margin-top:8px}.demo-title{font-size:29px;font-weight:650;letter-spacing:-.8px;margin:8px 0}.demo-copy{color:#3e536b;font-size:17px;line-height:1.55}.stage-track{display:flex;gap:10px;margin:18px 0}.stage-item{flex:1;padding:13px;border-bottom:3px solid #d9e3ec;color:#526478}.stage-item.active{border-color:#087f6d;color:#075e50;background:#e8f5ef}.evidence-label{font-size:11px;letter-spacing:1.5px;color:#087f6d}@media(max-width:700px){.demo-number{font-size:55px}.stage-item{font-size:11px;padding:8px}.demo-hero{padding:18px}}
</style>''',unsafe_allow_html=True)
    if stage == 0:
        from story import render_story
        render_story()
        return
    st.markdown('<div class="kicker">◈ METRICMIND LITE / THE AI SCIENTIST FOR THE LIVING INTERNET</div>',unsafe_allow_html=True)
    st.markdown('### Better experiments. Evidence you can explain.')
    st.caption('90-second guided demo · 20,000 synthetic visitors · Deterministic analysis · No API keys')
    names=['The apparent win','The business check','The overlooked factor','The next experiment']
    st.markdown('<div class="stage-track">'+''.join(f'<div class="stage-item {"active" if i==stage else ""}">0{i} · {name}</div>' for i,name in enumerate(names,1))+'</div>',unsafe_allow_html=True)
    back,progress,nxt,reset_col=st.columns([1,2,2,1])
    back.button('← Back',disabled=False,on_click=move,args=(-1,),width='stretch')
    progress.caption(f'STAGE {stage} OF 4 · '+['0–15 seconds','15–35 seconds','35–60 seconds','60–90 seconds'][stage-1])
    nxt.button(['Reveal the business outcome →','Find the overlooked factor →','Design the next experiment →','Experiment ready'][stage-1],disabled=stage==4,on_click=move,args=(1,),type='primary',width='stretch')
    reset_col.button('Reset Demo',on_click=reset,width='stretch')

    if stage==1:
        uplift=100*(b.conversion/a.conversion-1)
        st.markdown(f'<div class="demo-hero"><div class="evidence-label">OBSERVED / CONVERSION</div><div class="demo-number">+{uplift:.0f}%</div><div class="demo-title">The AI page looks like a winner.</div><div class="demo-copy">More visitors buy. Is that enough to call the experiment a success?</div></div>',unsafe_allow_html=True)
        left,right=st.columns([2,1])
        with left: st.plotly_chart(chart([100*a.conversion,100*b.conversion],['A · Original','B · Conversion optimized'],'%'),width='stretch')
        with right:
            st.metric('Additional orders',f'{int(b.orders-a.orders):+d}')
            st.caption(f'{int(a.orders)} → {int(b.orders)} orders\n\n10,000 visitors in each arm\n\n+0.60 percentage points = +20% relative')
        st.caption('Say: “The AI increased conversion by 20%. Most dashboards would celebrate. MetricMind asks one more question.”')
    elif stage==2:
        drop=100*(b.rpv/a.rpv-1)
        st.markdown(f'<div class="demo-hero"><div class="evidence-label">OBSERVED / BUSINESS OUTCOME</div><div class="demo-number" style="color:#b8522b">{drop:.0f}%</div><div class="demo-title">More orders. Less revenue per visitor.</div><div class="demo-copy">Smaller purchases erased the conversion gain. Make revenue per visitor the primary metric; keep returns as a guardrail.</div></div>',unsafe_allow_html=True)
        left,right=st.columns([2,1])
        with left: st.plotly_chart(chart([a.rpv,b.rpv],['A · Original','B · Conversion optimized'],'$', ['#8096b7','#b8522b']),width='stretch')
        with right:
            st.metric('Average order value',f'${b.aov:.0f}',f'{b.aov-a.aov:.0f} vs A')
            st.metric('Less revenue / 10,000 visitors',f'${(a.rpv-b.rpv)*10000:,.0f}')
        _,lo,hi=difference_ci(df[df.variant=='A'].order_value,df[df.variant=='B'].order_value)
        st.caption(f'Observed decline, not a proven population effect: 95% revenue-difference CI [${lo:.2f}, ${hi:.2f}] includes zero.')
        with st.expander('Show the arithmetic & return guardrail'):
            st.write(f'A: {a.conversion:.3f} × ${a.aov:.0f} = ${a.rpv:.2f}/visitor. B: {b.conversion:.3f} × ${b.aov:.0f} = ${b.rpv:.2f}/visitor.')
            st.write(f'Returns: {int(a.returns)}/{int(a.orders)} = {100*a.return_rate:.2f}%; {int(b.returns)}/{int(b.orders)} = {100*b.return_rate:.2f}%. Gross revenue excludes refunds. Retained revenue per visitor: A ${a.retained_rpv:.2f}, B ${b.retained_rpv:.2f}. Neither is profit.')
        st.markdown('#### Human co-steer / Set the objective')
        st.text_area('Business brief for the design',value=st.session_state.business_brief,key='business_editor',height=110,on_change=save_editor,args=('business_editor','business_brief'))
        st.caption('Edit Focus: fit, budget, or durability and Tone: calm or bold. These directives change the local design. Other prose is retained in the ChatGPT-ready prompt; it is not interpreted locally. The measured metrics and experiment primary remain unchanged.')
        st.caption('Say: “Revenue per visitor fell 5%. The result is uncertain, but conversion alone is clearly an incomplete scorecard.”')
    elif stage==3:
        rows=discover(df); worst=rows.iloc[0]; group=df[df[worst.factor]==worst.segment]; gs=summarize(group)
        st.markdown(f'<div class="demo-hero"><div class="evidence-label">EXPLORATORY FINDING / 4 FACTORS, 10 SEGMENTS SCANNED</div><div class="demo-title">{r["target"].capitalize()} is the clue.</div><div class="demo-copy">In this group, conversion doubles while revenue per visitor falls by one-third. More low-value purchases are a plausible explanation to test.</div></div>',unsafe_allow_html=True)
        c1,c2,c3=st.columns(3)
        c1.metric('Segment conversion',f'{100*gs.loc["B","conversion"]:.0f}%',f'{100*gs.loc["A","conversion"]:.0f}% → {100*gs.loc["B","conversion"]:.0f}%')
        c2.metric('Segment revenue / visitor',f'${gs.loc["B","rpv"]:.2f}',f'{worst.delta:.2f} vs A')
        c3.metric('Visitors per arm',f'{int(worst.n_a):,}',delta=None)
        contrasts=rows[rows.factor==worst.factor].copy()
        contrasts['Revenue change ($)']=(contrasts.delta*contrasts.n_a).round(2)
        st.dataframe(contrasts[['segment','n_a','orders_a','orders_b','rpv_a','rpv_b','Revenue change ($)']].rename(columns={'segment':'Discount sensitivity','n_a':'Visitors / arm','orders_a':'Orders A','orders_b':'Orders B','rpv_a':'Revenue/visitor A','rpv_b':'Revenue/visitor B'}),hide_index=True,width='stretch')
        st.caption(f'Average order value in high sensitivity: ${gs.loc["A","aov"]:.0f} → ${gs.loc["B","aov"]:.0f}. Smaller purchases are directly observed; the reason is a hypothesis.')
        st.markdown('**The loss has a location:** high sensitivity contributes **−$4,800**, offset by **+$3,000** in low sensitivity. Net: **−$1,800**. Segment sizes are identical across arms.')
        st.caption('A measured customer factor, not a discovered unobserved confounder. This pattern motivates a hypothesis; it does not prove why shoppers behaved differently.')
        with st.expander('Audit the discovery: every segment, counts & confidence intervals'):
            st.dataframe(rows.round(3),hide_index=True,width='stretch')
            st.write('Ranked by the most negative observed B−A revenue/visitor difference, not by an LLM or a significance claim. Nominal 95% Welch intervals include non-buyers. Overlapping segments, multiple comparisons and selection bias require independent confirmation. Sensitivity is measured before exposure; this fixture deliberately plants the pattern.')
        st.markdown('#### Human co-steer / Refine and generate')
        with st.expander('Business brief carried forward'):
            st.text(st.session_state.business_brief)
        st.text_area('Design prompt (ChatGPT-ready)',value=st.session_state.design_prompt,key='design_editor',height=150,on_change=save_editor,args=('design_editor','design_prompt'))
        st.caption('Offline prompt interpreter, not live ChatGPT. Supported directives: Focus, Tone, Headline, CTA. Design directives override the business brief. For example: Focus: budget or Headline: Choose only what you need. Other prose is export-only.')
        if st.button('Generate human-steered design',type='primary'):
            try:
                st.session_state.generated_design=generate_design(*steering_source())
                st.session_state.generated_source=steering_source()
            except ValueError as exc:
                st.error(str(exc))
        if 'generated_design' in st.session_state:
            if st.session_state.generated_source != steering_source():
                st.warning('Prompt changed. Generate again to apply it; the preview below is the last generated design.')
            st.caption(st.session_state.generated_design['rationale'])
            st.markdown(store_html(True,r['target'],compact=True,design=st.session_state.generated_design),unsafe_allow_html=True)
            st.caption('Human-authored copy is a draft; review product claims before a real experiment.')
        st.download_button('Download ChatGPT-ready prompt',export_prompt(*steering_source(),r['target']),'metricmind_design_prompt.txt','text/plain')
        st.caption('Say: “We scanned four measured factors. Discount-sensitive shoppers bought twice as often, but their purchases were smaller. Now we have a specific, testable design brief.”')
    else:
        st.markdown('<div class="demo-title">Make the recommendation understandable. Then test it.</div>',unsafe_allow_html=True)
        if 'generated_design' not in st.session_state:
            try:
                st.session_state.generated_design=generate_design(*steering_source())
                st.session_state.generated_source=steering_source()
            except ValueError as exc:
                st.error(f'{exc} Go Back to edit the prompt.'); return
        design=st.session_state.generated_design
        if st.session_state.generated_source != steering_source():
            st.warning('Showing the last generated design. Go Back and regenerate to apply pending prompt changes.')
        st.caption(design['rationale'])
        l,rr=st.columns(2)
        with l:
            st.markdown('**CURRENT B / Discount-led**')
            st.markdown(store_html(False,compact=True),unsafe_allow_html=True)
        with rr:
            st.markdown('**PROPOSED C / Value-led**')
            st.markdown(store_html(True,r['target'],compact=True,design=design),unsafe_allow_html=True)
        mechanism={'fit':'clearer product-fit guidance','budget':'transparent total prices and individual-item comparisons','durability':'clearer materials and care information'}[design['focus']]
        hypothesis=f'{mechanism.capitalize()} will increase revenue per visitor without worsening returns; this is untested.'
        st.markdown('**Fresh 50/50 test:** current B vs proposed C for high-sensitivity visitors. **Primary:** revenue per visitor. **Guardrails:** returns, conversion and retained revenue. **Hypothesis:** '+hypothesis)
        base_brief='\n'.join('Hypothesis: '+hypothesis if line.startswith('Hypothesis:') else line for line in experiment_plan(df).splitlines())
        brief=base_brief+'\nHUMAN-STEERED TREATMENT SPECIFICATION\n'+design['rationale']+'\nHeadline: '+design['headline']+'\nCTA: '+design['cta']+'\n\n'+export_prompt(*st.session_state.generated_source,r['target'])
        with st.expander('Decision rule & complete experiment brief'):
            st.text(brief)
        st.download_button('Download experiment brief',brief,'metricmind_experiment.txt','text/plain')
        st.caption('Say: “The system proposes a better experience and tells us exactly how to test it. Humans can inspect the evidence before accepting the idea.”')
    with st.expander('Trust & methodology'):
        st.write('This is an engineered synthetic fixture, not live evidence or a claim about Coframe performance. The “AI scientist” concept uses deterministic rules in this demo. All totals come from 20,000 visitor records. Uncertainty intervals illustrate independent visitor sampling; the fixture fixes its counts. Associations do not establish a causal mechanism. Follow-up randomization tests the redesign; it cannot by itself prove the psychological mechanism. No API calls, no fabricated redesign results.')
        st.download_button('Download underlying data',df.to_csv(index=False),'synthetic_visitors.csv','text/csv')
