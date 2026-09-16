import pandas as pd
import numpy as np

np.random.seed(42)
n = 500

vendors = ['Vendor A', 'Vendor B', 'Vendor C', 'Vendor D']
vendor_weights = [0.30, 0.25, 0.25, 0.20]

business_units = ['BU-1', 'BU-2', 'BU-3', 'BU-4']
bu_weights = [0.25, 0.25, 0.25, 0.25]

categories = ['Components', 'Software', 'Hardware', 'Services']
cat_weights = [0.40, 0.25, 0.20, 0.15]

rows = []
for i in range(n):
    vendor = np.random.choice(vendors, p=vendor_weights)
    bu = np.random.choice(business_units, p=bu_weights)
    category = np.random.choice(categories, p=cat_weights)

    planned_days = int(np.random.normal(90, 15))
    planned_days = max(30, planned_days)

    # Vendor C is systematically worse; BU-2 has higher variance
    vendor_delay_factor = {'Vendor A': 1.02, 'Vendor B': 1.05, 'Vendor C': 1.25, 'Vendor D': 1.08}[vendor]
    bu_delay_factor = {'BU-1': 1.00, 'BU-2': 1.15, 'BU-3': 1.02, 'BU-4': 1.05}[bu]

    actual_days = int(planned_days * vendor_delay_factor * bu_delay_factor
                      + np.random.normal(0, 12))
    actual_days = max(15, actual_days)

    budget = int(np.random.normal(50000, 15000))
    budget = max(5000, budget)

    spend_factor = {'Vendor A': 0.98, 'Vendor B': 1.03, 'Vendor C': 1.18, 'Vendor D': 1.05}[vendor]
    actual_spend = int(budget * spend_factor + np.random.normal(0, 5000))
    actual_spend = max(1000, actual_spend)

    rows.append({
        'ProjectID': f'PRJ-{1000 + i}',
        'Vendor': vendor,
        'BusinessUnit': bu,
        'Category': category,
        'PlannedDays': planned_days,
        'ActualDays': actual_days,
        'Budget': budget,
        'ActualSpend': actual_spend,
    })

df = pd.DataFrame(rows)

# Compute variance metrics
df['ScheduleVariancePct'] = ((df['ActualDays'] - df['PlannedDays']) / df['PlannedDays'] * 100).round(2)
df['BudgetVariancePct'] = ((df['ActualSpend'] - df['Budget']) / df['Budget'] * 100).round(2)

# Z-scores
df['ScheduleZscore'] = np.abs((df['ScheduleVariancePct'] - df['ScheduleVariancePct'].mean()) / df['ScheduleVariancePct'].std()).round(2)
df['BudgetZscore'] = np.abs((df['BudgetVariancePct'] - df['BudgetVariancePct'].mean()) / df['BudgetVariancePct'].std()).round(2)

# Risk tier
def risk_tier(row):
    s, b = row['ScheduleZscore'], row['BudgetZscore']
    if s > 2 and b > 2:
        return 'Critical'
    if s > 2 or b > 2:
        return 'High'
    if s > 1 or b > 1:
        return 'Medium'
    return 'Low'

df['RiskTier'] = df.apply(risk_tier, axis=1)

# OTIF flag (On-Time-In-Full: actual days <= 1.2x planned)
df['OTIF'] = np.where(df['ActualDays'] <= df['PlannedDays'] * 1.2, 'On-Time', 'Delayed')

df.to_csv('procurement_data.csv', index=False)

print(f"Generated: procurement_data.csv ({len(df)} rows)")
print(f"Risk Tier Distribution:")
print(df['RiskTier'].value_counts().to_string())
print(f"\nOTIF Rate: {(df['OTIF'] == 'On-Time').mean() * 100:.1f}%")
print(f"Avg Schedule Variance: {df['ScheduleVariancePct'].mean():.1f}%")
print(f"Avg Budget Variance: {df['BudgetVariancePct'].mean():.1f}%")