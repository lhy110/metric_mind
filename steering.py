"""Small, explicit prompt interpreter; no LLM calls or arbitrary prompt execution."""
DEFAULT_BUSINESS = 'Improve revenue per visitor while protecting returns and conversion.\nFocus: fit\nTone: calm'
DEFAULT_DESIGN = 'Use the discount-sensitivity finding to help shoppers choose suitable products.\nAvoid urgency and unsupported promises.\n# Optional overrides: Focus: budget | fit | durability; Tone: calm | bold\n# Put each directive on its own line. You may also add Headline: ... and CTA: ...'


def generate_design(business, prompt):
    fields = {'focus':'fit', 'tone':'calm'}
    for text in [business,prompt]:
        for line in text.splitlines():
            if line.strip().startswith('#'): continue
            name, sep, value = line.partition(':')
            if sep and name.strip().lower() in {'focus','tone','headline','cta'}:
                fields[name.strip().lower()] = value.strip()
    if fields['focus'].lower() not in {'fit','budget','durability'}:
        raise ValueError('Focus must be fit, budget, or durability.')
    if fields['tone'].lower() not in {'calm','bold'}:
        raise ValueError('Tone must be calm or bold.')
    focus, tone = fields['focus'].lower(), fields['tone'].lower()
    options = {
        'fit': ('Buy better. Keep it longer.', 'Find your everyday fit →', 'Compare dimensions, capacity and included items before choosing the everyday bag that fits your routine.', 'The Everyday Carry System', 'Compare sizes & materials / See what is included'),
        'budget': ('Buy what you need. Nothing extra.', 'Compare total prices →', 'Compare individual pieces and the complete set. Choose only what you need, with the full price visible before checkout.', 'Your essentials, your choice', 'Compare individual items / View the complete set'),
        'durability': ('Choose for the long run.', 'Explore materials & care →', 'Inspect materials, construction and care guidance before choosing a bag for everyday use. Make an informed purchase, without durability guarantees.', 'The considered everyday collection', 'Inspect construction / Read care guidance')}
    headline,cta,sub,title,details=options[focus]
    if tone=='bold': headline={'fit':'Find your fit. Own your everyday.','budget':'Less guesswork. Clear prices.','durability':'Look closer. Choose carefully.'}[focus]
    return dict(headline=fields.get('headline',headline)[:160] or headline,
                cta=fields.get('cta',cta)[:80] or cta,sub=sub,title=title,details=details,
                badge=f'{focus.upper()} FIRST / HUMAN-STEERED',focus=focus,tone=tone,
                rationale=f'Human selected {focus} with a {tone} tone. The observed smaller baskets motivate transparent comparisons; whether this design improves revenue remains untested.')


def export_prompt(business,prompt,target):
    return f'''You are proposing a retail webpage experiment, not reporting measured uplift.
EVIDENCE: Synthetic A/B data: conversion +20% relatively; revenue per visitor -5% observed, with its 95% interval including zero. High discount sensitivity: 4,000 visitors per arm; conversion 3% to 6%; revenue per visitor $3.60 to $2.40; average order value $120 to $40. This is association, not a proven mechanism.
TARGET: {target}.
HUMAN BUSINESS BRIEF:
{business}
HUMAN DESIGN PROMPT:
{prompt}
TASK: Propose headline, product positioning, CTA and presentation. Explain how each follows the evidence and human brief. Do not invent product facts, testimonials, guarantees or achieved uplift. Include a fresh 50/50 experiment against current B, revenue per visitor as primary, returns/conversion/retained revenue as guardrails. Treat any requested alternative objective as a proposal requiring a new measurement plan.
'''
