"""
Configuration file for Web Analytics Dashboard
Centralized settings for easy customization
"""

# ============================================================================
# DATA CONFIGURATION
# ============================================================================

DATA_FILE = 'web_traffic_data.csv'
DATE_FORMAT = '%d-%m-%Y %H:%M'

# Required columns in the dataset
REQUIRED_COLUMNS = [
    'date', 'page', 'device', 'country',
    'sessions', 'users', 'bounce_rate',
    'conversions', 'avg_session_duration'
]

# ============================================================================
# ANALYTICS CONFIGURATION
# ============================================================================

# Quality Score Weights (must sum to 1.0)
QUALITY_SCORE_WEIGHTS = {
    'bounce_rate': 0.3,      # Lower bounce = better
    'conversion_rate': 0.4,   # Higher conversion = better
    'session_duration': 0.3   # Longer sessions = better
}

# Page Performance Categories Thresholds
PERFORMANCE_THRESHOLDS = {
    'sessions_percentile': 50,      # Median by default
    'conversion_percentile': 50     # Median by default
}

# ============================================================================
# VISUALIZATION CONFIGURATION
# ============================================================================

# Color schemes for different chart types
COLOR_SCHEMES = {
    'primary': '#1f77b4',
    'success': '#2ca02c',
    'warning': '#ff7f0e',
    'danger': '#d62728',
    'info': '#17becf',
    'category_colors': {
        'Star Performers': '#2ca02c',
        'High Traffic - Low Conversion': '#ff7f0e',
        'Hidden Gems': '#1f77b4',
        'Needs Attention': '#d62728'
    },
    'gradient_scales': {
        'traffic': 'Blues',
        'conversion': 'Greens',
        'engagement': 'Purples',
        'quality': 'RdYlGn'
    }
}

# Chart default heights
CHART_HEIGHTS = {
    'small': 300,
    'medium': 400,
    'large': 500,
    'xlarge': 600
}

# ============================================================================
# UI CONFIGURATION
# ============================================================================

# Dashboard title and branding
DASHBOARD_TITLE = "Web Traffic Analytics Dashboard"
DASHBOARD_ICON = "📊"
COMPANY_NAME = "Your Company Name"

# Sidebar configuration
SIDEBAR_CONFIG = {
    'initial_state': 'expanded',
    'filter_sections': ['date', 'page', 'device', 'country']
}

# Top metrics to display
TOP_METRICS = [
    'total_sessions',
    'total_users',
    'total_conversions',
    'conversion_rate',
    'avg_bounce_rate',
    'avg_session_duration'
]

# ============================================================================
# EXPORT CONFIGURATION
# ============================================================================

EXPORT_FILENAME = 'analytics_report.xlsx'
EXPORT_SHEETS = [
    'Page Performance',
    'Device Analysis',
    'Country Analysis',
    'Daily Trends',
    'Hourly Patterns'
]

# ============================================================================
# PERFORMANCE CONFIGURATION
# ============================================================================

# Cache settings
CACHE_TTL = 3600  # Cache time-to-live in seconds (1 hour)
MAX_CACHE_ENTRIES = 1000

# Data loading optimization
CHUNK_SIZE = 10000  # For processing large files

# ============================================================================
# ALERT THRESHOLDS
# ============================================================================

# Thresholds for automated insights
ALERT_THRESHOLDS = {
    'high_bounce_rate': 0.70,        # Alert if bounce rate > 70%
    'low_conversion_rate': 1.0,      # Alert if conversion rate < 1%
    'low_session_duration': 30,      # Alert if avg session < 30 seconds
    'traffic_drop_percentage': 20,   # Alert if traffic drops > 20%
}

# ============================================================================
# BUSINESS RULES
# ============================================================================

# Define which pages are considered "conversion pages"
CONVERSION_PAGES = ['Checkout', 'Product']

# Define which pages are considered "engagement pages"
ENGAGEMENT_PAGES = ['Blog', 'About']

# Define peak hours for business
PEAK_HOURS = {
    'morning': (9, 12),
    'afternoon': (12, 17),
    'evening': (17, 21)
}

# Day of week ordering
DAY_ORDER = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
             'Friday', 'Saturday', 'Sunday']

# ============================================================================
# FORMATTING CONFIGURATION
# ============================================================================

# Number formatting
NUMBER_FORMATS = {
    'integer': '{:,.0f}',
    'float_1': '{:.1f}',
    'float_2': '{:.2f}',
    'percentage': '{:.2f}%',
    'currency': '${:,.2f}',
    'duration': '{:.0f}s'
}

# ============================================================================
# FEATURE FLAGS
# ============================================================================

# Enable/disable features
FEATURES = {
    'enable_export': True,
    'enable_filters': True,
    'enable_insights': True,
    'enable_predictions': False,  # For future ML features
    'enable_alerts': True,
    'enable_realtime': False       # For future real-time streaming
}

# ============================================================================
# ADVANCED ANALYTICS SETTINGS
# ============================================================================

# Minimum sample size for statistical significance
MIN_SAMPLE_SIZE = 100

# Confidence level for statistical tests
CONFIDENCE_LEVEL = 0.95

# Outlier detection settings
OUTLIER_METHOD = 'iqr'  # 'iqr' or 'zscore'
OUTLIER_THRESHOLD = 1.5  # IQR multiplier or Z-score threshold