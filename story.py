"""Page 0: verified Coframe positioning and a clearly fictional customer story."""
from pathlib import Path
import streamlit as st
import base64


def render_story():
    st.markdown('<div class="kicker">PAGE 0 / THE CUSTOMER STORY</div>',unsafe_allow_html=True)
    logo=Path(__file__).parent/'assets'/'coframe-logo.png'
    if logo.exists():
        encoded=base64.b64encode(logo.read_bytes()).decode()
        st.markdown(f'<div style="display:inline-block;background:white;padding:16px 22px;border-radius:10px"><img alt="Coframe logo" src="data:image/png;base64,{encoded}" style="width:210px;max-width:100%;height:auto"></div>',unsafe_allow_html=True)
    else: st.markdown('## Coframe')
    st.title('Faster experiments. Decisions people can trust.')
    st.markdown('**MetricMind is a proposed human-steered scientific review layer alongside Coframe’s website optimization workflow.**')
    st.caption('Independent hackathon concept · No live Coframe integration · No partnership or endorsement implied')
    l,r=st.columns(2)
    with l:
        st.markdown('### Coframe / Build, test, personalize')
        st.write('Coframe describes a workflow that analyzes a site and its goals, generates copy, code and visual variants for human approval, then tests and personalizes experiences. It already addresses revenue, audience segmentation and human review.')
        st.markdown('### MetricMind / Inspect, steer, propose')
        st.write('Our demo adds an explicit place to examine the business objective, inspect overlooked segment evidence, challenge an interpretation and co-steer the next experiment. The proposed handoff is an approved brief and design—not an automatic deployment.')
    with r:
        st.markdown('### Meet Field & Form')
        st.caption('Fictional retailer created for this demonstration—not a claimed Coframe customer.')
        st.write('An everyday-bag retailer sells individual accessories and complete carry sets. Its growth lead wants more valuable purchases, while its merchandising team wants customers to choose products that fit their needs.')
        st.write('The team runs an illustrative website A/B test: original A versus a discount-led B. Both receive 10,000 visitors. At first, the conversion dashboard looks encouraging.')
        st.markdown('**The question:** Does the apparent win help the business—and what should the team test next?')
    st.markdown('### A complementary workflow')
    c1,c2,c3=st.columns(3)
    c1.markdown('**1 · Coframe workflow**\n\nGenerate, approve and test website variants.')
    c2.markdown('**2 · Proposed MetricMind review**\n\nInspect outcomes → explain evidence → let a human steer the hypothesis.')
    c3.markdown('**3 · Proposed handoff**\n\nSend the approved brief and design into a new randomized experiment.')
    st.info('Complex reasoning should produce a simple, inspectable action. The human can understand the evidence, revise the recommendation and decide what to test.')
    st.caption('The upcoming figures are generated synthetic data, not a Coframe case study or evidence of underperformance. The demo uses deterministic rules, not high-dimensional learned inference.')
    with st.expander('Sources & scope'):
        st.markdown('[Coframe: official product workflow](https://www.coframe.com/) · [Coframe: AI-driven variant creation](https://docs.coframe.com/editor/variant-creation)')
        st.write('Product description checked October 10, 2026. Coframe branding identifies the company being discussed. Field & Form, its products and all experimental outcomes are fictional. MetricMind is a complement concept, not a claim that Coframe lacks these capabilities.')
    if st.button('Start the customer experiment →',type='primary',width='stretch'):
        st.session_state.stage=1
        st.rerun()
