-- ============================================================
-- Enterprise KPI Anomaly Detection — Analysis Queries
-- Schema: ProjectID, Vendor, BusinessUnit, Category, PlannedDays,
--         ActualDays, Budget, ActualSpend, ScheduleVariancePct,
--         BudgetVariancePct, ScheduleZscore, BudgetZscore,
--         RiskTier, OTIF
-- ============================================================

-- 1. VENDOR PERFORMANCE RANKING
WITH vendor_metrics AS (
    SELECT
        Vendor,
        COUNT(ProjectID) AS total_projects,
        AVG(ScheduleVariancePct) AS avg_schedule_var,
        AVG(BudgetVariancePct)   AS avg_budget_var,
        SUM(CASE WHEN RiskTier IN ('Critical','High') THEN 1 ELSE 0 END) AS high_risk_projects,
        SUM(CASE WHEN OTIF = 'On-Time' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS otif_rate
    FROM procurement_data
    GROUP BY Vendor
)
SELECT
    Vendor, total_projects, avg_schedule_var, avg_budget_var,
    high_risk_projects, otif_rate,
    DENSE_RANK() OVER (ORDER BY avg_schedule_var DESC) AS risk_rank,
    ROUND(100.0 * high_risk_projects / total_projects, 1) AS high_risk_pct
FROM vendor_metrics
ORDER BY risk_rank;


-- 2. BUSINESS UNIT RISK CONCENTRATION
WITH bu_metrics AS (
    SELECT
        BusinessUnit,
        COUNT(ProjectID) AS total_projects,
        AVG(ScheduleVariancePct) AS avg_schedule_var,
        AVG(BudgetVariancePct)   AS avg_budget_var,
        SUM(CASE WHEN RiskTier = 'Critical' THEN 1 ELSE 0 END) AS critical_count
    FROM procurement_data
    GROUP BY BusinessUnit
)
SELECT
    BusinessUnit, total_projects, avg_schedule_var, avg_budget_var, critical_count,
    ROUND(100.0 * critical_count / SUM(critical_count) OVER (), 2) AS pct_of_all_critical
FROM bu_metrics
ORDER BY critical_count DESC;


-- 3. VENDOR × BUSINESS UNIT RISK INTERSECTION
SELECT
    Vendor,
    BusinessUnit,
    COUNT(*) AS projects,
    ROUND(AVG(ScheduleVariancePct), 1) AS avg_schedule_var,
    SUM(CASE WHEN RiskTier IN ('Critical','High') THEN 1 ELSE 0 END) AS high_risk_count,
    RANK() OVER (PARTITION BY BusinessUnit ORDER BY AVG(ScheduleVariancePct) DESC) AS rank_within_bu
FROM procurement_data
GROUP BY Vendor, BusinessUnit
ORDER BY BusinessUnit, rank_within_bu;


-- 4. PROJECTS REQUIRING IMMEDIATE INTERVENTION
SELECT
    ProjectID, Vendor, BusinessUnit, Category,
    PlannedDays, ActualDays, Budget, ActualSpend,
    ScheduleVariancePct, BudgetVariancePct,
    ScheduleZscore, BudgetZscore, RiskTier
FROM procurement_data
WHERE RiskTier = 'Critical'
ORDER BY ScheduleZscore DESC, BudgetZscore DESC;


-- 5. CATEGORY-LEVEL RISK SUMMARY
WITH category_metrics AS (
    SELECT
        Category,
        COUNT(*) AS projects,
        AVG(ScheduleVariancePct) AS avg_schedule_var,
        AVG(BudgetVariancePct)   AS avg_budget_var,
        SUM(CASE WHEN OTIF = 'Delayed' THEN 1 ELSE 0 END) AS delayed_count
    FROM procurement_data
    GROUP BY Category
)
SELECT
    Category, projects, avg_schedule_var, avg_budget_var, delayed_count,
    ROUND(100.0 * delayed_count / projects, 1) AS delay_rate_pct,
    SUM(projects) OVER () AS total_portfolio
FROM category_metrics
ORDER BY avg_schedule_var DESC;