# 🚀 Web Traffic Analytics Dashboard

A comprehensive, production-ready analytics dashboard built with **Streamlit** for analyzing web traffic patterns, user behavior, and conversion optimization.

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-latest-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 📋 Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Data Requirements](#data-requirements)
- [Usage](#usage)
- [Metrics Explained](#metrics-explained)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### Executive KPI Dashboard
- Real-time tracking of 6 critical metrics
- Session volume, user counts, and conversion rates
- Bounce rate and engagement analytics
- Session duration insights

### Page Performance Analysis
- **Performance Matrix** visualizing pages across 4 categories:
  - ⭐ **Star Performers**: High traffic + High conversions
  - 🔧 **High Traffic - Low Conversion**: Optimization opportunities
  - 💎 **Hidden Gems**: High conversion but low traffic
  - ⚠️ **Needs Attention**: Low performance on all metrics
- Quality scoring algorithm
- Detailed performance tables with color-coded metrics

### Device & Geographic Analysis
- Device-level performance (Desktop, Mobile, Tablet)
- Country-wise traffic and conversion patterns
- Comparative analysis for optimization targeting

### Time-Based Intelligence
- **Hourly Heatmap**: Visual representation of traffic patterns
- Peak performance identification
- Day-of-week trends
- Optimal timing for campaigns

### AI-Powered Insights
- Automated insight generation
- Actionable recommendations based on data patterns
- Priority-ranked optimization opportunities
- Export functionality for stakeholder reports

## 🛠️ Installation

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/ahtashamd321/web-analytics-dashboard.git
cd web-analytics-dashboard
```

2. **Create virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the dashboard**
```bash
streamlit run app.py
```

5. **Access the dashboard**
Open your browser at `http://localhost:8501`

## 📊 Data Requirements

### File Format
Place your `web_traffic_data.csv` file in the project root directory.

### Required Columns
| Column | Type | Format | Example |
|--------|------|--------|---------|
| `date` | datetime | DD-MM-YYYY HH:MM | 15-01-2024 14:30 |
| `page` | string | - | Home, Product, Checkout |
| `device` | string | - | Desktop, Mobile, Tablet |
| `country` | string | - | United States, India |
| `sessions` | integer | - | 1250 |
| `users` | integer | - | 980 |
| `bounce_rate` | float | 0.0 to 1.0 | 0.45 (for 45%) |
| `conversions` | integer | - | 87 |
| `avg_session_duration` | integer | seconds | 245 |

### Sample Data
```csv
date,page,device,country,sessions,users,bounce_rate,conversions,avg_session_duration
15-01-2024 10:00,Home,Desktop,United States,1500,1200,0.35,120,180
15-01-2024 10:00,Product,Mobile,India,800,650,0.45,65,150
```

### Data Quality Tips
- Minimum recommended: 10,000+ records for meaningful insights
- Ensure no missing values in critical columns
- Bounce rate must be between 0 and 1
- Dates should be chronological

## 🎯 Usage

### Dashboard Navigation

The dashboard consists of 5 main tabs:

1. **📊 Overview**
   - High-level KPI metrics
   - Daily session trends
   - Conversion rate evolution
   - Traffic distribution by page and device

2. **📄 Page Performance**
   - Performance matrix visualization
   - Quality score rankings
   - Category-based segmentation
   - Detailed performance tables

3. **📱 Device & Country Analysis**
   - Device performance comparison
   - Geographic traffic patterns
   - Conversion rates by segment

4. **⏰ Time Analysis**
   - Traffic heatmap (day × hour)
   - Hourly performance trends
   - Weekly patterns
   - Peak time identification

5. **🎯 Insights & Recommendations**
   - Automated insights
   - Prioritized recommendations
   - Export report functionality

### Using Filters

The **sidebar** provides powerful filtering options:
- **Date Range**: Select specific time periods for analysis
- **Pages**: Focus on specific page types
- **Devices**: Analyze by device category
- **Countries**: Filter by geographic location

Filters are applied across all tabs and visualizations.

### Exporting Reports

1. Navigate to the **Insights & Recommendations** tab
2. Click the **"📥 Export Full Report"** button
3. Find `analytics_report.xlsx` in your project directory
4. The report includes:
   - Summary statistics
   - Page performance data
   - Device and country breakdowns
   - AI-generated insights

## 🧮 Metrics Explained

### Quality Score
A composite metric calculated as:
```
Quality Score = (1 - Bounce Rate) × 30% + 
                Conversion Rate × 40% + 
                Normalized Session Duration × 30%
```

This score helps identify overall page effectiveness combining user engagement, conversion performance, and time spent.

### Page Categories

Pages are automatically categorized based on performance:

- **Star Performers** ⭐
  - Sessions ≥ median AND Conversion Rate ≥ median
  - Action: Scale what's working

- **High Traffic - Low Conversion** 🔧
  - Sessions ≥ median AND Conversion Rate < median
  - Action: Optimize conversion funnel

- **Hidden Gems** 💎
  - Sessions < median AND Conversion Rate ≥ median
  - Action: Increase traffic/promotion

- **Needs Attention** ⚠️
  - Below median on both metrics
  - Action: Investigate and improve or consider removal

### Key Performance Indicators

- **Sessions**: Total number of website visits
- **Users**: Unique visitors to your site
- **Bounce Rate**: Percentage of single-page sessions
- **Conversions**: Goal completions (purchases, signups, etc.)
- **Conversion Rate**: Conversions / Sessions
- **Avg Session Duration**: Average time spent per session

## 🎨 Customization

### Modifying Visualizations

Edit chart configurations in `app.py`:

```python
# Change color schemes
fig = px.scatter(
    color_continuous_scale='Viridis'  # Try 'Blues', 'Reds', 'Greens'
)

# Customize layout
fig.update_layout(
    title="Your Custom Title",
    height=600,
    template='plotly_dark'  # Try 'plotly', 'plotly_white', 'ggplot2'
)
```

### Adding New Metrics

1. Create calculation function:
```python
@st.cache_data
def calculate_engagement_score(df):
    return (df['avg_session_duration'] / df['sessions']).mean()
```

2. Display in UI:
```python
col1, col2 = st.columns(2)
with col1:
    st.metric("Engagement Score", f"{calculate_engagement_score(filtered_df):.2f}")
```

### Custom Insights

Add custom insight logic in the insights generation function:

```python
def generate_custom_insights(df):
    insights = []
    
    # Your custom logic
    if condition:
        insights.append("Your custom insight here")
    
    return insights
```

## 🐛 Troubleshooting

### Common Issues

**Problem**: "Data file not found"
```
FileNotFoundError: web_traffic_data.csv
```
**Solution**: Ensure `web_traffic_data.csv` is in the same directory as `app.py`

---

**Problem**: "Date parsing errors"
```
ValueError: time data does not match format
```
**Solution**: Verify date format matches `DD-MM-YYYY HH:MM` exactly

---

**Problem**: "No data after filtering"
**Solution**: 
- Reset all filters in the sidebar
- Adjust date range to include your data period
- Check if filter combinations are too restrictive

---

**Problem**: "Charts not displaying properly"
**Solution**: 
- Clear Streamlit cache: Press `C` in the terminal, then `Enter`
- Restart the app with `Ctrl + C` and `streamlit run app.py`
- Check browser console for JavaScript errors

---

**Problem**: "Memory errors with large datasets"
**Solution**:
- Reduce date range
- Filter by specific pages/devices/countries
- Increase system memory allocation
- Consider data sampling for exploration

## 🚀 Performance Optimization

For large datasets (100K+ rows):

- App uses `@st.cache_data` for efficient data loading
- Filters reduce data processing load
- Aggregations are pre-calculated

**Advanced optimization**:
```python
# Increase cache size
@st.cache_data(max_entries=1000, ttl=3600)
def load_data():
    return pd.read_csv('web_traffic_data.csv')

# Sample large datasets
if len(df) > 100000:
    df = df.sample(n=100000, random_state=42)
```

## 🔐 Security & Deployment

### Local Development
This dashboard is designed for local/internal use by default.

### Production Deployment

For production environments:

1. **Authentication**
   - Use Streamlit Cloud authentication
   - Implement OAuth (Google, GitHub)
   - Add password protection

2. **Data Security**
   - Use environment variables for sensitive configs
   - Implement role-based access control
   - Enable HTTPS/SSL

3. **Deploy Options**
   - [Streamlit Community Cloud](https://streamlit.io/cloud) (Free)
   - AWS/GCP/Azure with Docker
   - Heroku
   - Self-hosted server

Example deployment:
```bash
# Using Streamlit Cloud
streamlit run app.py --server.enableCORS=false --server.enableXsrfProtection=true
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Reporting Issues
- Use the GitHub issue tracker
- Provide detailed description
- Include error messages and screenshots
- Specify Python and library versions

### Suggesting Features
Open an issue with:
- Clear description of the feature
- Use cases and benefits
- Optional: Implementation approach

### Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/ahtashamd321/web-analytics-dashboard.git

# Create branch
git checkout -b feature/your-feature

# Install dev dependencies
pip install -r requirements-dev.txt

# Make changes and test
streamlit run app.py

# Run tests (if available)
pytest tests/
```

## 💡 Roadmap

Planned features:
- [ ] Machine learning predictions for traffic forecasting
- [ ] Real-time data streaming integration
- [ ] A/B testing analysis module
- [ ] Custom alert system
- [ ] API endpoint for programmatic access
- [ ] Multi-language support
- [ ] Dark mode toggle
- [ ] PDF export functionality

## 📚 Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Python Documentation](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [Web Analytics Best Practices](https://support.google.com/analytics)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Ahtasham Anjum**

- GitHub: [@yourusername](https://github.com/ahtashamd321)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/ahtasham-anjum)

## 🙏 Acknowledgments

- Streamlit team for the amazing framework
- The open-source community
- Contributors and users of this project

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/ahtashamd321/web-analytics-dashboard/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ahtashamd321/web-analytics-dashboard/discussions)
- **Email**: ahtashamd321@gmail.com

---

**Built with ❤️ for the data analytics community**

*Transform your web analytics into actionable insights!*

⭐ **Star this repo if you find it helpful!**