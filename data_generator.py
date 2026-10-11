"""Deterministic visitor-level fixture; calibrated counts, not a power simulation."""
import numpy as np
import pandas as pd


def generate_data(seed=42):
    rng = np.random.default_rng(seed)
    frames = []
    # variant, pre-treatment discount sensitivity, visitors, orders, revenue, returns
    specs = [('A','High',4000,120,14400,9), ('A','Low',6000,180,21600,6),
             ('B','High',4000,240,9600,39), ('B','Low',6000,120,24600,4)]
    for variant, sensitivity, n, orders, total, returns in specs:
        amounts = rng.lognormal(0, .22, orders)
        cents = np.floor(amounts / amounts.sum() * total * 100).astype(int)
        cents[:int(total * 100 - cents.sum())] += 1
        # Balanced nuisance covariates, randomly assigned independently of outcomes.
        d = pd.DataFrame({'variant':variant, 'discount_sensitivity':sensitivity,
            'device':rng.permutation(np.repeat(['Mobile','Desktop'], n//2)),
            'traffic_source':rng.permutation(np.repeat(['Paid social','Organic','Email','Direct'], n//4)),
            'visitor_type':rng.permutation(np.repeat(['New','Returning'], n//2)),
            'converted':np.arange(n)<orders,
            'order_value':np.r_[cents/100, np.zeros(n-orders)],
            'returned':False})
        d.loc[rng.choice(orders, returns, replace=False), 'returned'] = True
        d['retained_revenue'] = d.order_value.where(~d.returned, 0)
        frames.append(d)
    result = pd.concat(frames, ignore_index=True).sample(frac=1, random_state=seed).reset_index(drop=True)
    result.insert(0, 'visitor_id', np.arange(1, len(result)+1))
    return result

if __name__ == '__main__':
    generate_data().to_csv('synthetic_visitors.csv', index=False)
    print('Wrote 20,000 synthetic visitors to synthetic_visitors.csv')
