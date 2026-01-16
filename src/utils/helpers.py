"""
Helper Functions Module

Contains common utility functions used across the analysis system.
"""

import pandas as pd
import numpy as np
from typing import Union, List, Dict, Tuple, Optional
from datetime import datetime, timedelta


# ============================================================================
# DATA VALIDATION HELPERS
# ============================================================================

def validate_numeric_column(series: pd.Series, column_name: str) -> Dict[str, any]:
    """
    Validate numeric column for common issues.
    
    Args:
        series: Pandas series to validate
        column_name: Name of the column for reporting
        
    Returns:
        Dictionary with validation results
    """
    validation_report = {
        'column': column_name,
        'total_records': len(series),
        'null_count': series.isnull().sum(),
        'negative_count': (series < 0).sum() if pd.api.types.is_numeric_dtype(series) else 0,
        'zero_count': (series == 0).sum() if pd.api.types.is_numeric_dtype(series) else 0,
        'min_value': series.min() if pd.api.types.is_numeric_dtype(series) else None,
        'max_value': series.max() if pd.api.types.is_numeric_dtype(series) else None,
        'mean_value': series.mean() if pd.api.types.is_numeric_dtype(series) else None,
        'median_value': series.median() if pd.api.types.is_numeric_dtype(series) else None,
    }
    return validation_report


def safe_divide(numerator: Union[float, pd.Series], 
                denominator: Union[float, pd.Series], 
                fill_value: float = np.nan) -> Union[float, pd.Series]:
    """
    Safely divide two numbers or series, handling division by zero.
    
    Args:
        numerator: Numerator value(s)
        denominator: Denominator value(s)
        fill_value: Value to use when denominator is zero (default: NaN)
        
    Returns:
        Result of division with safe handling of zero denominators
    """
    if isinstance(denominator, pd.Series):
        result = numerator / denominator.replace(0, np.nan)
        if not np.isnan(fill_value):
            result = result.fillna(fill_value)
    else:
        result = numerator / denominator if denominator != 0 else fill_value
    return result


def flag_outliers(series: pd.Series, n_std: float = 3.0) -> pd.Series:
    """
    Flag outliers based on standard deviation threshold.
    
    Args:
        series: Pandas series to check for outliers
        n_std: Number of standard deviations for threshold (default: 3.0)
        
    Returns:
        Boolean series indicating outliers
    """
    mean = series.mean()
    std = series.std()
    z_scores = np.abs((series - mean) / std)
    return z_scores > n_std


# ============================================================================
# TEMPORAL ANALYSIS HELPERS
# ============================================================================

def calculate_moving_average(series: pd.Series, window: int) -> pd.Series:
    """
    Calculate moving average with minimum data point validation.
    
    Args:
        series: Time series data
        window: Window size for moving average
        
    Returns:
        Moving average series
    """
    if len(series) < window:
        return pd.Series([np.nan] * len(series), index=series.index)
    return series.rolling(window=window, min_periods=window).mean()


def calculate_growth_rate(current: Union[float, pd.Series], 
                         previous: Union[float, pd.Series]) -> Union[float, pd.Series]:
    """
    Calculate growth rate with safe handling of zero baseline.
    
    Args:
        current: Current period value(s)
        previous: Previous period value(s)
        
    Returns:
        Growth rate (percentage change)
    """
    return safe_divide((current - previous), previous, fill_value=np.nan) * 100


def detect_spikes(series: pd.Series, 
                  baseline: pd.Series, 
                  multiplier: float = 2.0) -> pd.Series:
    """
    Detect spikes where values exceed baseline by a multiplier.
    
    Args:
        series: Time series to check for spikes
        baseline: Baseline series (e.g., moving average)
        multiplier: Threshold multiplier (default: 2.0)
        
    Returns:
        Boolean series indicating spikes
    """
    return series > (baseline * multiplier)


def calculate_velocity(series: pd.Series, time_diff_days: int = 1) -> pd.Series:
    """
    Calculate rate of change (velocity) of a time series.
    
    Args:
        series: Time series data
        time_diff_days: Number of days between observations (default: 1)
        
    Returns:
        Velocity series (change per day)
    """
    return series.diff() / time_diff_days


# ============================================================================
# AGGREGATION HELPERS
# ============================================================================

def aggregate_to_district_level(df: pd.DataFrame, 
                                date_col: str = 'date',
                                state_col: str = 'state',
                                district_col: str = 'district',
                                value_cols: List[str] = None) -> pd.DataFrame:
    """
    Aggregate data to district-date level.
    
    Args:
        df: Input dataframe
        date_col: Name of date column
        state_col: Name of state column
        district_col: Name of district column
        value_cols: List of columns to aggregate (sum)
        
    Returns:
        Aggregated dataframe
    """
    group_cols = [date_col, state_col, district_col]
    
    if value_cols is None:
        # Aggregate all numeric columns
        value_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    agg_dict = {col: 'sum' for col in value_cols if col in df.columns}
    
    return df.groupby(group_cols, as_index=False).agg(agg_dict)


def calculate_percentile_thresholds(series: pd.Series, 
                                    percentiles: List[int] = [10, 25, 50, 75, 90]) -> Dict[int, float]:
    """
    Calculate percentile thresholds for a series.
    
    Args:
        series: Pandas series
        percentiles: List of percentiles to calculate (default: [10, 25, 50, 75, 90])
        
    Returns:
        Dictionary mapping percentile to threshold value
    """
    return {p: series.quantile(p / 100) for p in percentiles}


# ============================================================================
# SCORING HELPERS
# ============================================================================

def calculate_severity_score(value: float, 
                             thresholds: Dict[int, float],
                             reverse: bool = False) -> int:
    """
    Calculate severity score (1-5) based on threshold ranges.
    
    Args:
        value: Value to score
        thresholds: Dictionary mapping severity level to threshold
        reverse: If True, lower values get higher severity (default: False)
        
    Returns:
        Severity score (1-5)
    """
    if pd.isna(value):
        return 0
    
    sorted_thresholds = sorted(thresholds.items(), key=lambda x: x[1], reverse=reverse)
    
    for severity, threshold in sorted_thresholds:
        if reverse:
            if value <= threshold:
                return severity
        else:
            if value >= threshold:
                return severity
    
    return 1  # Minimum severity


def calculate_composite_score(scores: Dict[str, float], 
                              weights: Dict[str, float]) -> float:
    """
    Calculate weighted composite score.
    
    Args:
        scores: Dictionary of individual scores
        weights: Dictionary of weights for each score
        
    Returns:
        Composite score (0-100)
    """
    total_weight = sum(weights.values())
    weighted_sum = sum(scores.get(key, 0) * weight for key, weight in weights.items())
    return (weighted_sum / total_weight) * 100 if total_weight > 0 else 0


def calculate_roi(benefit: float, cost: float) -> float:
    """
    Calculate Return on Investment (ROI).
    
    Args:
        benefit: Expected benefit
        cost: Implementation cost
        
    Returns:
        ROI ratio (benefit/cost)
    """
    return safe_divide(benefit, cost, fill_value=0)


# ============================================================================
# GEOGRAPHIC HELPERS
# ============================================================================

def standardize_state_name(state: str) -> str:
    """
    Standardize state name to canonical form.
    
    Args:
        state: Raw state name
        
    Returns:
        Standardized state name
    """
    if pd.isna(state):
        return 'Unknown'
    
    state = str(state).strip()
    
    # State name mapping
    state_mapping = {
        # West Bengal variants
        'west bengal': 'West Bengal',
        'westbengal': 'West Bengal',
        'w bengal': 'West Bengal',
        'w.bengal': 'West Bengal',
        
        # Odisha variants
        'orissa': 'Odisha',
        'orrisa': 'Odisha',
        
        # Chhattisgarh variants
        'chattisgarh': 'Chhattisgarh',
        'chhatisgarh': 'Chhattisgarh',
        
        # Uttarakhand variants
        'uttaranchal': 'Uttarakhand',
        
        # Delhi variants
        'new delhi': 'Delhi',
        'nct of delhi': 'Delhi',
        
        # Jammu and Kashmir variants
        'jammu & kashmir': 'Jammu and Kashmir',
        'j&k': 'Jammu and Kashmir',
        
        # Dadra and Nagar Haveli variants
        'dadra & nagar haveli': 'Dadra and Nagar Haveli and Daman and Diu',
        'daman & diu': 'Dadra and Nagar Haveli and Daman and Diu',
    }
    
    state_lower = state.lower()
    return state_mapping.get(state_lower, state)


def validate_geographic_hierarchy(df: pd.DataFrame,
                                  state_col: str = 'state',
                                  district_col: str = 'district') -> pd.DataFrame:
    """
    Validate and flag geographic hierarchy inconsistencies.
    
    Args:
        df: Input dataframe
        state_col: Name of state column
        district_col: Name of district column
        
    Returns:
        Dataframe with validation flags
    """
    df = df.copy()
    
    # Flag invalid state names (cities, numbers, etc.)
    df['invalid_state'] = df[state_col].apply(
        lambda x: str(x).isdigit() or str(x).lower() in ['jaipur', 'balanagar', '100000']
    )
    
    return df


# ============================================================================
# REPORTING HELPERS
# ============================================================================

def format_currency(amount: float, currency: str = '₹') -> str:
    """
    Format amount as currency string.
    
    Args:
        amount: Numeric amount
        currency: Currency symbol (default: ₹)
        
    Returns:
        Formatted currency string
    """
    if pd.isna(amount):
        return 'N/A'
    
    if amount >= 10000000:  # 1 crore
        return f"{currency}{amount / 10000000:.2f} Cr"
    elif amount >= 100000:  # 1 lakh
        return f"{currency}{amount / 100000:.2f} L"
    elif amount >= 1000:  # 1 thousand
        return f"{currency}{amount / 1000:.2f} K"
    else:
        return f"{currency}{amount:.2f}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Format value as percentage string.
    
    Args:
        value: Numeric value (0-1 or 0-100)
        decimals: Number of decimal places (default: 1)
        
    Returns:
        Formatted percentage string
    """
    if pd.isna(value):
        return 'N/A'
    
    # Assume if value > 1, it's already in percentage form
    if value > 1:
        return f"{value:.{decimals}f}%"
    else:
        return f"{value * 100:.{decimals}f}%"


def create_summary_statistics(series: pd.Series) -> Dict[str, float]:
    """
    Create summary statistics for a series.
    
    Args:
        series: Pandas series
        
    Returns:
        Dictionary with summary statistics
    """
    return {
        'count': len(series),
        'mean': series.mean(),
        'median': series.median(),
        'std': series.std(),
        'min': series.min(),
        'max': series.max(),
        'q25': series.quantile(0.25),
        'q75': series.quantile(0.75),
    }


# ============================================================================
# DATE HELPERS
# ============================================================================

def parse_date_flexible(date_str: str) -> Optional[datetime]:
    """
    Parse date string with multiple format attempts.
    
    Args:
        date_str: Date string to parse
        
    Returns:
        Datetime object or None if parsing fails
    """
    if pd.isna(date_str):
        return None
    
    formats = [
        '%d-%m-%Y',
        '%Y-%m-%d',
        '%d/%m/%Y',
        '%Y/%m/%d',
        '%d.%m.%Y',
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(str(date_str), fmt)
        except ValueError:
            continue
    
    return None


def get_date_range(df: pd.DataFrame, date_col: str = 'date') -> Tuple[datetime, datetime]:
    """
    Get date range from dataframe.
    
    Args:
        df: Input dataframe
        date_col: Name of date column
        
    Returns:
        Tuple of (min_date, max_date)
    """
    return df[date_col].min(), df[date_col].max()
