"""Offline storefront previews with CSS product illustrations."""
from html import escape


def store_html(adapted=False, target='High discount sensitivity', compact=False, design=None):
    headline = 'Buy better.<br>Keep it longer.' if adapted else 'Big deals.<br>Small prices.'
    sub = 'Choose the right everyday bag with honest comparisons, clear sizing, and materials made to last.' if adapted else 'Your next favorite is on sale. Discover limited-time savings across our everyday collection.'
    cta = 'Find your everyday fit →' if adapted else 'Unlock the deals →'
    badge = 'THE CONSIDERED COLLECTION' if adapted else 'TODAY ONLY · UP TO 40% OFF'
    title = 'The Everyday Carry System' if adapted else 'The Everyday Edit'
    price = 'Compare the complete set · $205' if adapted else 'Accessories from $40'
    details = 'Compare sizes & materials &nbsp; / &nbsp; See what is included' if adapted else 'Limited-time offer &nbsp; / &nbsp; Discover more deals'
    if adapted and design:
        headline, sub, cta, badge, title, details = [escape(design[k]) for k in ['headline','sub','cta','badge','title','details']]
    html = f'''<style>
.store {{border:1px solid #334154;border-radius:18px;overflow:hidden;background:{'#e6ece3' if adapted else '#f4e9dd'};color:#1b2b25;font-family:Arial,sans-serif;}}
.store-nav{{display:flex;justify-content:space-between;padding:19px 24px;border-bottom:1px solid #b6bfae;font-size:11px;letter-spacing:2px;}}
.store-main{{padding:25px 28px 15px;}}
.store-tag{{font-size:10px;letter-spacing:2px;font-weight:700;color:{'#315e4c' if adapted else '#a2492f'};}}
.store h2{{color:#1b2b25;font-family:Georgia,serif;font-size:44px;line-height:1.02;font-weight:400;padding:13px 0;margin:0;}}
.store p{{font-size:13px;line-height:1.6;max-width:360px;color:#49564d;min-height:62px;}}
.store-cta{{display:inline-block;background:{'#204b3b' if adapted else '#b34529'};padding:12px 17px;border-radius:5px;color:white;font-size:12px;font-weight:700;}}
.shelf{{height:175px;position:relative;background:radial-gradient(ellipse at 50% 110%,#a6b19b 0%,transparent 65%);margin:15px 0;}}
.bag{{position:absolute;left:34%;bottom:12px;width:115px;height:130px;background:linear-gradient(110deg,#879781,#4b6352);border-radius:25px 25px 12px 12px;box-shadow:15px 13px 22px #26362633;transform:rotate(-8deg);}}
.bag:before{{content:'';position:absolute;width:44px;height:24px;border:7px solid #485e4b;border-bottom:0;border-radius:13px 13px 0 0;left:28px;top:-20px;}}
.bag:after{{content:'FIELD / 01';position:absolute;bottom:20px;left:17px;border:1px solid #bac6aa;padding:20px 7px 9px;color:#d3ddca;font-size:9px;border-radius:8px;}}
.pouch{{position:absolute;bottom:4px;left:61%;width:75px;height:61px;border-radius:9px;background:#c8a779;transform:rotate(9deg);box-shadow:9px 9px 14px #26362622;}}
.store-foot{{background:#ffffff50;padding:17px 25px;font-size:12px;line-height:1.9;}}
</style><div class="store"><div class="store-nav"><b>FIELD & FORM</b><span>SHOP &nbsp; ABOUT &nbsp; BAG (0)</span></div><div class="store-main"><div class="store-tag">{badge}</div><h2>{headline}</h2><p>{sub}</p><span class="store-cta">{cta}</span><div class="shelf"><div class="bag"></div><div class="pouch"></div></div><b>{title}</b><div style="font-size:12px;margin-top:7px">{price}</div></div><div class="store-foot">{details}<br>{'Personalization hypothesis: '+escape(target) if adapted else 'Illustrative current B experience · discount-led acquisition'}</div></div>'''

    if compact:
        html = html.replace('padding:19px 24px','padding:12px 18px').replace('padding:25px 28px 15px','padding:16px 20px 10px').replace('font-size:44px','font-size:32px').replace('min-height:62px','min-height:40px').replace('height:175px','height:100px').replace('width:115px;height:130px','width:82px;height:83px').replace('left:28px;top:-20px','left:14px;top:-20px').replace('bottom:20px;left:17px','bottom:10px;left:7px').replace('padding:20px 7px 9px','padding:9px 5px 5px').replace('padding:17px 25px','padding:10px 20px')
    # Scope every class: two previews must never overwrite each other's palette.
    import re
    suffix = 'value' if adapted else 'deals'
    for name in ['store-nav','store-main','store-tag','store-cta','store-foot','store','shelf','bag','pouch']:
        html = re.sub(r'\.'+name+r'(?![\w-])', '.'+name+'-'+suffix, html)
        html = html.replace('class="'+name+'"', 'class="'+name+'-'+suffix+'"')
    return html
