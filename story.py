"""Concise visual opening for the independent Coframe complement demo."""
from pathlib import Path
import base64
import streamlit as st


def render_story():
    logo=Path(__file__).parent/'assets'/'coframe-logo.png'
    brand=(f'<img alt="Coframe" src="data:image/png;base64,{base64.b64encode(logo.read_bytes()).decode()}">' if logo.exists() else '<strong>Coframe</strong>')
    st.markdown('''<style>
.mm-story{color:#18283b}.mm-story *{box-sizing:border-box}
.mm-story .brandline{display:flex;align-items:center;gap:20px;margin:8px 0 23px;color:#526478;font-size:13px}
.mm-story .brandline img{width:155px;height:auto}.mm-story .brandline span{padding-left:20px;border-left:1px solid #cbd6e4}
.mm-story h1{font-size:clamp(28px,4vw,46px);line-height:1.13;letter-spacing:-1.8px;margin:0 0 12px;color:#18283b}
.mm-story .lead{color:#526478;font-size:18px;margin:0 0 22px}
.mm-story .customer{display:flex;align-items:center;gap:27px;background:#fff;border:1px solid #dbe3ed;border-radius:18px;padding:20px 28px;margin:20px 0 25px}
.mm-story .bag-scene{position:relative;width:110px;min-width:110px;height:105px;background:#edf4ef;border-radius:15px}
.mm-story .bag{position:absolute;left:32px;bottom:12px;width:49px;height:65px;border-radius:13px 13px 7px 7px;background:linear-gradient(115deg,#8d9f80,#4f6b58);box-shadow:7px 7px 9px #243c2220;transform:rotate(-8deg)}
.mm-story .bag:before{content:'';position:absolute;left:13px;top:-12px;width:22px;height:15px;border:5px solid #4f6b58;border-bottom:0;border-radius:9px 9px 0 0}
.mm-story .bag:after{content:'';position:absolute;left:9px;bottom:10px;width:32px;height:23px;border:1px solid #bbcbb4;border-radius:5px}
.mm-story .eyebrow{font-size:11px;font-weight:700;letter-spacing:1.5px;color:#087f6d;margin-bottom:6px}
.mm-story h2{font-size:24px;margin:0 0 5px;color:#18283b;padding:0}
.mm-story .customer p{margin:3px 0;color:#526478;font-size:15px}
.mm-story .flow{display:grid;grid-template-columns:1fr 34px 1fr 34px 1fr;align-items:stretch;gap:8px}
.mm-story .node{background:#fff;border:1px solid #dbe3ed;border-radius:16px;padding:20px}
.mm-story .node.selected{background:#eaf6f1;border-color:#b7dacc}
.mm-story .num{font-size:12px;color:#61758b;letter-spacing:1px;margin-bottom:12px}
.mm-story h3{margin:0 0 10px;padding:0;font-size:19px;color:#18283b}
.mm-story .node p{margin:0;color:#526478;line-height:1.6;font-size:15px}
.mm-story .arrow{display:flex;align-items:center;justify-content:center;font-size:23px;color:#668578}
.mm-story .loop{text-align:right;color:#087f6d;font-size:13px;padding:12px 10px}
.mm-story .question{font-size:23px;letter-spacing:-.5px;margin:14px 0 5px;font-weight:600;color:#18283b}
@media(max-width:700px){.mm-story .flow{grid-template-columns:1fr}.mm-story .arrow{transform:rotate(90deg);height:20px}.mm-story .customer{padding:16px;gap:15px}.mm-story .bag-scene{min-width:85px;width:85px}.mm-story .brandline{flex-wrap:wrap}.mm-story .brandline span{border:0;padding:0}.mm-story .loop{text-align:left}}
</style>''',unsafe_allow_html=True)
    st.markdown(f'''<section class="mm-story" aria-label="Coframe and MetricMind customer story">
<div class="brandline">{brand}<span>MetricMind · Independent complement concept</span></div>
<h1>Better experiments.<br>Human-steered decisions.</h1>
<p class="lead">Complex signals → clear hypotheses → testable experiences.</p>
<div class="customer"><div class="bag-scene" role="img" aria-label="Illustration of an everyday carry bag"><div class="bag"></div></div><div><div class="eyebrow">MEET THE CUSTOMER · FICTIONAL SCENARIO</div><h2>Field &amp; Form</h2><p>Everyday bags. Accessories. Complete carry sets.</p><p><strong>The goal:</strong> more valuable purchases, fewer poor-fit orders.</p></div></div>
<div class="flow" role="group" aria-label="Proposed complementary workflow">
<div class="node"><div class="num">01 / COFRAME</div><h3>Create &amp; test</h3><p>Generate variants.<br>Approve, test, personalize.</p></div>
<div class="arrow" aria-hidden="true">→</div>
<div class="node selected"><div class="num">02 / METRICMIND</div><h3>Inspect &amp; explain</h3><p>Check the objective.<br>Surface overlooked evidence.</p></div>
<div class="arrow" aria-hidden="true">→</div>
<div class="node"><div class="num">03 / HUMAN REVIEW</div><h3>Steer the next test</h3><p>Challenge the hypothesis.<br>Approve the design brief.</p></div>
</div><div class="loop">↳ Proposed handoff: a new experiment in the optimization workflow</div>
<div class="question">The page converts better. Does the business win?</div>
</section>''',unsafe_allow_html=True)
    if st.button('Start the customer experiment →',type='primary',width='stretch'):
        st.session_state.stage=1
        st.rerun()
    st.caption('Synthetic outcomes · No live integration or endorsement · 15-second introduction')
    with st.expander('Sources & scope'):
        st.markdown('[Coframe product workflow](https://www.coframe.com/) · [AI-driven variant creation](https://docs.coframe.com/editor/variant-creation)')
        st.write('Coframe already supports revenue goals, segmentation, personalization and human approval. MetricMind is a proposed additional scientific review workflow, not a claim that Coframe lacks these capabilities. Field & Form is fictional, not a claimed Coframe customer. No Coframe performance results are represented here. The demo uses deterministic rules; a high-dimensional learned inference system is not implemented. Logo sourced from the official Coframe website.')
