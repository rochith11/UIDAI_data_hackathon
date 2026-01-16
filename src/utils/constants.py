"""
Constants Module

Contains thresholds, cost estimates, and configuration constants for the analysis system.
"""

# ============================================================================
# FRICTION DETECTION THRESHOLDS
# ============================================================================

# Infrastructure Stress Thresholds
INFRASTRUCTURE_THRESHOLDS = {
    'under_provisioned': {
        'enrolment_percentile': 75,  # High enrolment threshold
        'bio_ratio_percentile': 25,  # Low biometric ratio threshold
    },
    'backlog_processing': {
        'biometric_percentile': 75,  # High biometric threshold
        'enrolment_percentile': 50,  # Below median enrolment
    },
    'data_quality_debt': {
        'demographic_percentile': 75,  # High demographic updates
        'enrolment_percentile': 50,  # Below median enrolment
    }
}

# Access Failure Thresholds
ACCESS_FAILURE_THRESHOLDS = {
    'low_activity_percentile': 10,  # Bottom 10% across all services
    'min_activity_days': 30,  # Minimum days to consider persistent
    'gap_threshold_pct': 60,  # 60% below state median
}

# Age Structure Thresholds
AGE_STRUCTURE_THRESHOLDS = {
    'high_child_ratio': 0.15,  # >15% of enrolments are 0-5
    'high_adult_ratio': 0.70,  # >70% adults
    'velocity_percentile': 75,  # High velocity threshold
}

# Migration Detection Thresholds
MIGRATION_THRESHOLDS = {
    'spike_multiplier': 2.0,  # 2x the 3-month average
    'adult_ratio_threshold': 0.70,  # >70% adults
}

# Data Quality Debt Thresholds
DATA_QUALITY_THRESHOLDS = {
    'updates_per_1000_enrolments': 100,  # >100 updates per 1000 enrolments
    'consistency_months': 6,  # Consistent over 6 months
}

# Biometric Stress Thresholds
BIOMETRIC_STRESS_THRESHOLDS = {
    'low_capture_ratio': 0.3,  # <30% biometric capture rate
    'repeat_visit_percentile': 75,  # High repeat visits
    'elderly_success_threshold': 0.5,  # <50% success for elderly
    'child_success_threshold': 0.5,  # <50% success for children
}

# Anomaly Detection Thresholds
ANOMALY_THRESHOLDS = {
    'z_score_threshold': 3.0,  # |z-score| > 3 is anomaly
    'rolling_window_days': 30,  # 30-day rolling window
    'min_data_points': 30,  # Minimum data points for analysis
}

# Severity Scoring
SEVERITY_LEVELS = {
    1: 'Low',
    2: 'Moderate',
    3: 'High',
    4: 'Critical',
    5: 'Emergency'
}

# Composite Friction Score Weights
FRICTION_SCORE_WEIGHTS = {
    'infrastructure_stress': 0.25,
    'access_failure': 0.20,
    'data_quality_debt': 0.15,
    'biometric_stress': 0.20,
    'migration_pressure': 0.10,
    'age_structure_pressure': 0.10,
}

# ============================================================================
# COST ESTIMATES (Proxy values in INR)
# ============================================================================

# Infrastructure Costs
INFRASTRUCTURE_COSTS = {
    'biometric_kit': 150000,  # ₹1.5 lakh per kit
    'mobile_van': 2500000,  # ₹25 lakh per van
    'extended_hours_monthly': 50000,  # ₹50k per month per center
    'operator_training': 10000,  # ₹10k per operator
    'equipment_calibration': 5000,  # ₹5k per device
}

# Operational Costs
OPERATIONAL_COSTS = {
    'staff_hourly_cost': 200,  # ₹200 per hour
    'avg_processing_time_minutes': 15,  # 15 minutes per update
    'verification_cost_per_case': 500,  # ₹500 per verification
    'duplicate_resolution_cost': 1000,  # ₹1000 per duplicate case
}

# Outreach Costs
OUTREACH_COSTS = {
    'awareness_campaign_district': 500000,  # ₹5 lakh per district
    'ngo_partnership_annual': 1000000,  # ₹10 lakh per year
    'incentivized_enrolment_per_person': 100,  # ₹100 per person
    'language_materials': 50000,  # ₹50k per language set
}

# Benefit Estimates (Annual savings in INR)
BENEFIT_ESTIMATES = {
    'reduced_update_burden_per_1000': 50000,  # ₹50k saved per 1000 enrolments
    'improved_biometric_success_per_pct': 100000,  # ₹1 lakh per 1% improvement
    'access_gap_closure_per_person': 500,  # ₹500 benefit per person enrolled
    'infrastructure_efficiency_gain': 200000,  # ₹2 lakh per optimized center
}

# ============================================================================
# TEMPORAL PARAMETERS
# ============================================================================

# Moving Average Windows
MOVING_AVERAGE_WINDOWS = {
    'short_term': 7,  # 7-day moving average
    'medium_term': 30,  # 30-day moving average
    'long_term': 90,  # 90-day moving average
}

# Forecast Horizons
FORECAST_HORIZONS = {
    'short_term_months': 12,  # 12-month forecast
    'long_term_months': 24,  # 24-month forecast
}

# ============================================================================
# DATA VALIDATION PARAMETERS
# ============================================================================

# Numeric Validation
NUMERIC_VALIDATION = {
    'max_daily_count_per_district': 1000000,  # 1 million max per day
    'outlier_std_threshold': 5,  # >5 std dev is outlier
    'min_interactions_for_ranking': 10,  # Minimum interactions to rank
}

# Date Validation
DATE_VALIDATION = {
    'min_year': 2020,
    'max_year': 2025,
}

# Geographic Validation
GEOGRAPHIC_VALIDATION = {
    'valid_states': [
        'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
        'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka',
        'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
        'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
        'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
        'Andaman and Nicobar Islands', 'Chandigarh', 'Dadra and Nagar Haveli and Daman and Diu',
        'Delhi', 'Jammu and Kashmir', 'Ladakh', 'Lakshadweep', 'Puducherry'
    ]
}

# ============================================================================
# VISUALIZATION PARAMETERS
# ============================================================================

# Color Schemes
COLOR_SCHEMES = {
    'stress_sequential': 'YlOrRd',  # Yellow-Orange-Red for stress
    'positive_sequential': 'YlGnBu',  # Yellow-Green-Blue for positive metrics
    'diverging': 'RdYlGn',  # Red-Yellow-Green for deviation
    'categorical': 'Set2',  # Colorblind-friendly categorical
}

# Chart Parameters
CHART_PARAMETERS = {
    'figure_width': 12,
    'figure_height': 8,
    'dpi': 300,
    'font_size': 10,
    'title_font_size': 14,
    'max_color_bins': 7,
}

# ============================================================================
# RECOMMENDATION PARAMETERS
# ============================================================================

# Priority Levels
PRIORITY_LEVELS = {
    'immediate': 'Immediate (0-3 months)',
    'short_term': 'Short-term (3-12 months)',
    'long_term': 'Long-term (1+ years)',
}

# Department Mapping
DEPARTMENT_MAPPING = {
    'infrastructure': 'Infrastructure Planning',
    'operations': 'Operations',
    'training': 'Training & Capacity Building',
    'policy': 'Policy & Strategy',
    'technology': 'Technology & Innovation',
    'outreach': 'Public Outreach & Awareness',
}

# ROI Thresholds
ROI_THRESHOLDS = {
    'high_roi': 3.0,  # >3x return
    'medium_roi': 1.5,  # 1.5-3x return
    'low_roi': 1.0,  # 1-1.5x return
}

# ============================================================================
# REPORT PARAMETERS
# ============================================================================

# Report Structure
REPORT_SECTIONS = [
    'executive_summary',
    'infrastructure_stress',
    'access_failure',
    'age_structure',
    'migration_signals',
    'data_quality_debt',
    'biometric_stress',
    'cross_dataset_insights',
    'anomaly_detection',
    'budget_prioritization',
    'implementation_roadmap',
    'appendix',
]

# Top N Rankings
TOP_N_RANKINGS = {
    'top_recommendations': 10,
    'top_friction_districts': 20,
    'top_anomalies': 10,
}
