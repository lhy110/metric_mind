import unittest
import numpy as np
from streamlit.testing.v1 import AppTest
from data_generator import generate_data
from analysis import summarize, discover, difference_ci, recommend
from store import store_html

class MetricMindTests(unittest.TestCase):
    def test_accounting(self):
        d=generate_data(); s=summarize(d)
        self.assertEqual(len(d),20000)
        self.assertTrue(d.visitor_id.is_unique)
        np.testing.assert_allclose(s.conversion,[.03,.036])
        np.testing.assert_allclose(s.rpv,[3.60,3.42])
        np.testing.assert_allclose(s.aov,[120,95])
        self.assertEqual(list(s.returns),[15,43])
        self.assertTrue((~d.returned | d.converted).all())
        self.assertTrue((d.loc[~d.converted,'order_value']==0).all())
        self.assertTrue(generate_data().equals(d))
        self.assertAlmostEqual(d.order_value.sum(),70200)
    def test_discovery(self):
        d=generate_data(); r=recommend(d)
        self.assertEqual((r['factor'],r['segment']),('discount_sensitivity','High'))
        self.assertAlmostEqual(r['delta'],-1.2)
        self.assertTrue(r['wrong_metric'])
        _,low,high=difference_ci(d[d.variant=='A'].order_value,d[d.variant=='B'].order_value)
        self.assertLess(low,0); self.assertGreater(high,0)
        rows=discover(d); self.assertEqual(len(rows),10)
        self.assertTrue((rows.ci_low <= rows.delta).all())
        self.assertTrue((rows.ci_high >= rows.delta).all())
    def test_workflow(self):
        at=AppTest.from_file('app.py',default_timeout=30).run()
        next(b for b in at.button if b.label=='Start the customer experiment →').click().run()
        self.assertEqual(len(at.exception),0)
        at.radio(key='mode').set_value('Explore evidence').run()
        self.assertEqual(len(at.get('plotly_chart')),1)
        for option in ['Conversion rate','Average order value','Return rate','Revenue per visitor']:
            at.radio[1].set_value(option).run()
            self.assertEqual(len(at.exception),0)
        def click(label):
            next(b for b in at.button if b.label==label).click().run()
            self.assertEqual(len(at.exception),0)
        click('Analyze Optimization Objective')
        self.assertTrue(at.session_state['objective'])
        click('Find Overlooked Factors')
        self.assertEqual(len(at.get('plotly_chart')),2)
        self.assertEqual(len(at.dataframe),1)
        click('Generate Better Experience')
        self.assertTrue(at.session_state['adapted'])
        self.assertTrue(any('Buy better.' in m.value for m in at.markdown))
        self.assertTrue(any('FOLLOW-UP EXPERIMENT' in t.value for t in at.text))
        click('Reset Demo')
        self.assertFalse(at.session_state['adapted'])
        self.assertFalse(at.session_state['objective'])
        self.assertEqual(len(at.get('plotly_chart')),1)
        click('Generate Better Experience')
        self.assertTrue(at.session_state['factors'])
        self.assertTrue(at.session_state['objective'])
    def test_presentation_arithmetic(self):
        d=generate_data(); s=summarize(d)
        self.assertAlmostEqual(100*(s.loc['B','conversion']/s.loc['A','conversion']-1),20)
        self.assertAlmostEqual(100*(s.loc['B','rpv']/s.loc['A','rpv']-1),-5)
        rows=discover(d); rows=rows[rows.factor=='discount_sensitivity'].set_index('segment')
        self.assertAlmostEqual(rows.loc['High','delta']*rows.loc['High','n_a'],-4800)
        self.assertAlmostEqual(rows.loc['Low','delta']*rows.loc['Low','n_a'],3000)
        self.assertAlmostEqual((rows.delta*rows.n_a).sum(),-1800)
        g=summarize(d[d.discount_sensitivity=='High'])
        self.assertAlmostEqual(g.loc['B','conversion']/g.loc['A','conversion'],2)
        self.assertAlmostEqual(g.loc['B','rpv']/g.loc['A','rpv'],2/3)

    def test_guided_demo(self):
        at=AppTest.from_file('app.py',default_timeout=30).run()
        next(b for b in at.button if b.label=='Start the customer experiment →').click().run()
        self.assertEqual(at.session_state['stage'],1)
        self.assertFalse(any('−5%' in m.value for m in at.markdown))
        for label,stage in [('Reveal the business outcome →',2),('Find the overlooked factor →',3),('Design the next experiment →',4)]:
            next(b for b in at.button if b.label==label).click().run()
            self.assertEqual(len(at.exception),0)
            self.assertEqual(at.session_state['stage'],stage)
        self.assertTrue(any('Buy better.' in m.value for m in at.markdown))
        self.assertTrue(any('FOLLOW-UP EXPERIMENT' in t.value for t in at.text))
        next(b for b in at.button if b.label=='← Back').click().run()
        self.assertEqual(at.session_state['stage'],3)
        next(b for b in at.button if b.label=='Reset Demo').click().run()
        self.assertEqual(at.session_state['stage'],0)
        self.assertFalse(at.session_state['adapted'])

    def test_session_isolation(self):
        first=AppTest.from_file('app.py',default_timeout=30).run()
        next(b for b in first.button if b.label=='Start the customer experiment →').click().run()
        next(b for b in first.button if b.label=='Reveal the business outcome →').click().run()
        second=AppTest.from_file('app.py',default_timeout=30).run()
        next(b for b in second.button if b.label=='Start the customer experiment →').click().run()
        self.assertEqual(first.session_state['stage'],2)
        self.assertEqual(second.session_state['stage'],1)

    def test_human_steering(self):
        from steering import generate_design, DEFAULT_BUSINESS, DEFAULT_DESIGN
        from store import store_html
        d=generate_design('Focus: budget', 'CTA: Compare honestly')
        self.assertEqual(d['focus'],'budget')
        self.assertEqual(d['cta'],'Compare honestly')
        self.assertNotEqual(d['headline'],generate_design(DEFAULT_BUSINESS,DEFAULT_DESIGN)['headline'])
        self.assertEqual(generate_design('Focus: budget','Focus: durability')['focus'],'durability')
        with self.assertRaises(ValueError): generate_design('Focus: nonsense','')
        malicious=generate_design('', 'Headline: <script>alert(1)</script>')
        self.assertNotIn('<script>',store_html(True,design=malicious))
        at=AppTest.from_file('app.py',default_timeout=30).run()
        next(b for b in at.button if b.label=='Start the customer experiment →').click().run()
        def click(label):
            next(b for b in at.button if b.label==label).click().run()
            self.assertEqual(len(at.exception),0)
        click('Reveal the business outcome →')
        at.text_area(key='business_editor').set_value('Focus: budget\nTone: bold').run()
        click('Find the overlooked factor →')
        self.assertEqual(at.session_state['business_brief'],'Focus: budget\nTone: bold')
        at.text_area(key='design_editor').set_value('Headline: Buy with confidence\nCTA: Compare the options').run()
        click('Generate human-steered design')
        self.assertEqual(at.session_state['generated_design']['focus'],'budget')
        self.assertTrue(any('Buy with confidence' in m.value for m in at.markdown))
        click('Design the next experiment →')
        self.assertTrue(any('Buy with confidence' in m.value for m in at.markdown))
        self.assertTrue(any('Compare the options' in t.value for t in at.text))
        click('← Back')
        self.assertIn('Buy with confidence',at.text_area(key='design_editor').value)
        at.text_area(key='design_editor').set_value('Focus: durability').run()
        self.assertTrue(any('Prompt changed' in w.value for w in at.warning))
        click('Generate human-steered design')
        self.assertEqual(at.session_state['generated_design']['focus'],'durability')
        click('Reset Demo')
        self.assertEqual(at.session_state['business_brief'],DEFAULT_BUSINESS)
        self.assertNotIn('generated_design',at.session_state)

    def test_public_launcher(self):
        from start import server_command
        from unittest.mock import patch
        with patch.dict('os.environ', {'PORT':'9999'}):
            cmd=server_command()
            self.assertIn('--server.port=9999',cmd)
            self.assertIn('--server.address=0.0.0.0',cmd)
        with patch.dict('os.environ', {'PORT':'0'}):
            with self.assertRaises(ValueError): server_command()

    def test_story_page(self):
        at=AppTest.from_file('app.py',default_timeout=30).run()
        self.assertFalse(at.exception)
        self.assertEqual(at.session_state['stage'],0)
        self.assertTrue(any('Coframe' in m.value for m in at.markdown))
        next(b for b in at.button if b.label=='Start the customer experiment →').click().run()
        self.assertEqual(at.session_state['stage'],1)
        next(b for b in at.button if b.label=='← Back').click().run()
        self.assertEqual(at.session_state['stage'],0)
        self.assertFalse(at.exception)

    def test_css_isolation(self):
        before,after=store_html(False),store_html(True)
        self.assertIn('.store-deals {',before)
        self.assertNotIn('.store-deals {',after)
        self.assertIn('.store-value {',after)
        self.assertNotIn('.store-value {',before)

    def test_design_changes(self):
        a,b=store_html(False),store_html(True)
        for content in ['Buy better.','Find your everyday fit','Everyday Carry System','Compare sizes']:
            self.assertIn(content,b)
            self.assertNotIn(content,a)

if __name__=='__main__': unittest.main(verbosity=2)
