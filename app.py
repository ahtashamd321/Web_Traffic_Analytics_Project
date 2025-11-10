import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Web Traffic Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Load data with caching
@st.cache_data
def load_data():
    """Load and preprocess the web traffic data"""
    df = pd.read_csv('web_traffic_data.csv')
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y %H:%M')
    df['date_only'] = df['date'].dt.date
    df['hour'] = df['date'].dt.hour
    df['day_of_week'] = df['date'].dt.day_name()
    df['week'] = df['date'].dt.isocalendar().week
    return df

# Calculate KPIs
@st.cache_data
def calculate_kpis(df):
    """Calculate key performance indicators"""
    total_sessions = df['sessions'].sum()
    total_users = df['users'].sum()
    total_conversions = df['conversions'].sum()
    avg_bounce_rate = df['bounce_rate'].mean()
    avg_session_duration = df['avg_session_duration'].mean()
    conversion_rate = (total_conversions / total_sessions * 100) if total_sessions > 0 else 0
    
    return {
        'total_sessions': total_sessions,
        'total_users': total_users,
        'total_conversions': total_conversions,
        'avg_bounce_rate': avg_bounce_rate,
        'avg_session_duration': avg_session_duration,
        'conversion_rate': conversion_rate
    }

# Page performance analysis
@st.cache_data
def analyze_page_performance(df):
    """Segment pages into performance categories"""
    page_stats = df.groupby('page').agg({
        'sessions': 'sum',
        'conversions': 'sum',
        'bounce_rate': 'mean',
        'avg_session_duration': 'mean'
    }).reset_index()
    
    page_stats['conversion_rate'] = (page_stats['conversions'] / page_stats['sessions'] * 100)
    page_stats['quality_score'] = (
        (1 - page_stats['bounce_rate']) * 0.3 + 
        (page_stats['conversion_rate'] / 100) * 0.4 +
        (page_stats['avg_session_duration'] / page_stats['avg_session_duration'].max()) * 0.3
    ) * 100
    
    # Categorize pages
    median_sessions = page_stats['sessions'].median()
    median_conversions = page_stats['conversion_rate'].median()
    
    def categorize_page(row):
        if row['sessions'] >= median_sessions and row['conversion_rate'] >= median_conversions:
            return 'Star Performers'
        elif row['sessions'] >= median_sessions and row['conversion_rate'] < median_conversions:
            return 'High Traffic - Low Conversion'
        elif row['sessions'] < median_sessions and row['conversion_rate'] >= median_conversions:
            return 'Hidden Gems'
        else:
            return 'Needs Attention'
    
    page_stats['category'] = page_stats.apply(categorize_page, axis=1)
    return page_stats

# Device performance analysis
@st.cache_data
def analyze_device_performance(df):
    """Analyze performance by device type"""
    device_stats = df.groupby('device').agg({
        'sessions': 'sum',
        'users': 'sum',
        'conversions': 'sum',
        'bounce_rate': 'mean',
        'avg_session_duration': 'mean'
    }).reset_index()
    
    device_stats['conversion_rate'] = (device_stats['conversions'] / device_stats['sessions'] * 100)
    return device_stats

# Country performance analysis
@st.cache_data
def analyze_country_performance(df):
    """Analyze performance by country"""
    country_stats = df.groupby('country').agg({
        'sessions': 'sum',
        'users': 'sum',
        'conversions': 'sum',
        'bounce_rate': 'mean',
        'avg_session_duration': 'mean'
    }).reset_index()
    
    country_stats['conversion_rate'] = (country_stats['conversions'] / country_stats['sessions'] * 100)
    return country_stats

# Time-based analysis
@st.cache_data
def analyze_time_trends(df):
    """Analyze trends over time"""
    daily_stats = df.groupby('date_only').agg({
        'sessions': 'sum',
        'conversions': 'sum',
        'bounce_rate': 'mean'
    }).reset_index()
    
    daily_stats['conversion_rate'] = (daily_stats['conversions'] / daily_stats['sessions'] * 100)
    return daily_stats

# Main application
def main():
    st.markdown('<p class="main-header">🚀 Web Traffic Analytics Dashboard</p>', unsafe_allow_html=True)
    
    try:
        # Load data
        df = load_data()
        
        # Sidebar filters
        st.sidebar.header("📊 Filters")
        
        date_range = st.sidebar.date_input(
            "Date Range",
            value=(df['date_only'].min(), df['date_only'].max()),
            min_value=df['date_only'].min(),
            max_value=df['date_only'].max()
        )
        
        selected_pages = st.sidebar.multiselect(
            "Select Pages",
            options=df['page'].unique(),
            default=df['page'].unique()
        )
        
        selected_devices = st.sidebar.multiselect(
            "Select Devices",
            options=df['device'].unique(),
            default=df['device'].unique()
        )
        
        selected_countries = st.sidebar.multiselect(
            "Select Countries",
            options=df['country'].unique(),
            default=df['country'].unique()
        )
        
        # Filter data
        mask = (
            (df['date_only'] >= date_range[0]) & 
            (df['date_only'] <= date_range[1]) &
            (df['page'].isin(selected_pages)) &
            (df['device'].isin(selected_devices)) &
            (df['country'].isin(selected_countries))
        )
        filtered_df = df[mask]
        
        if filtered_df.empty:
            st.warning("No data available for the selected filters. Please adjust your selection.")
            return
        
        # Calculate KPIs
        kpis = calculate_kpis(filtered_df)
        
        # Display KPIs
        st.header("📈 Key Performance Indicators")
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            st.metric("Total Sessions", f"{kpis['total_sessions']:,.0f}")
        with col2:
            st.metric("Total Users", f"{kpis['total_users']:,.0f}")
        with col3:
            st.metric("Total Conversions", f"{kpis['total_conversions']:,.0f}")
        with col4:
            st.metric("Conversion Rate", f"{kpis['conversion_rate']:.2f}%")
        with col5:
            st.metric("Avg Bounce Rate", f"{kpis['avg_bounce_rate']*100:.1f}%")
        with col6:
            st.metric("Avg Session Duration", f"{kpis['avg_session_duration']:.0f}s")
        
        st.markdown("---")
        
        # Create tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Overview", 
            "📄 Page Performance", 
            "📱 Device & Country Analysis", 
            "⏰ Time Analysis",
            "🎯 Insights & Recommendations"
        ])
        
        with tab1:
            st.header("Traffic Overview")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Daily trend
                daily_stats = analyze_time_trends(filtered_df)
                fig_trend = go.Figure()
                fig_trend.add_trace(go.Scatter(
                    x=daily_stats['date_only'],
                    y=daily_stats['sessions'],
                    mode='lines+markers',
                    name='Sessions',
                    line=dict(color='#1f77b4', width=2)
                ))
                fig_trend.update_layout(
                    title="Daily Sessions Trend",
                    xaxis_title="Date",
                    yaxis_title="Sessions",
                    hovermode='x unified',
                    height=400
                )
                st.plotly_chart(fig_trend, use_container_width=True)
            
            with col2:
                # Conversion rate trend
                fig_conv = go.Figure()
                fig_conv.add_trace(go.Scatter(
                    x=daily_stats['date_only'],
                    y=daily_stats['conversion_rate'],
                    mode='lines+markers',
                    name='Conversion Rate',
                    line=dict(color='#2ca02c', width=2),
                    fill='tozeroy'
                ))
                fig_conv.update_layout(
                    title="Daily Conversion Rate Trend",
                    xaxis_title="Date",
                    yaxis_title="Conversion Rate (%)",
                    hovermode='x unified',
                    height=400
                )
                st.plotly_chart(fig_conv, use_container_width=True)
            
            col3, col4 = st.columns(2)
            
            with col3:
                # Page distribution
                page_sessions = filtered_df.groupby('page')['sessions'].sum().sort_values(ascending=False)
                fig_pages = px.pie(
                    values=page_sessions.values,
                    names=page_sessions.index,
                    title="Traffic Distribution by Page"
                )
                fig_pages.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pages, use_container_width=True)
            
            with col4:
                # Device distribution
                device_sessions = filtered_df.groupby('device')['sessions'].sum()
                fig_device = px.bar(
                    x=device_sessions.index,
                    y=device_sessions.values,
                    title="Traffic by Device Type",
                    labels={'x': 'Device', 'y': 'Sessions'},
                    color=device_sessions.values,
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig_device, use_container_width=True)
        
        with tab2:
            st.header("Page Performance Analysis")
            
            page_stats = analyze_page_performance(filtered_df)
            
            # Performance matrix
            col1, col2 = st.columns(2)
            
            with col1:
                fig_matrix = px.scatter(
                    page_stats,
                    x='sessions',
                    y='conversion_rate',
                    size='quality_score',
                    color='category',
                    hover_data=['page', 'bounce_rate', 'avg_session_duration'],
                    title="Page Performance Matrix",
                    labels={
                        'sessions': 'Total Sessions',
                        'conversion_rate': 'Conversion Rate (%)',
                        'quality_score': 'Quality Score'
                    },
                    color_discrete_map={
                        'Star Performers': '#2ca02c',
                        'High Traffic - Low Conversion': '#ff7f0e',
                        'Hidden Gems': '#1f77b4',
                        'Needs Attention': '#d62728'
                    }
                )
                fig_matrix.update_layout(height=500)
                st.plotly_chart(fig_matrix, use_container_width=True)
            
            with col2:
                # Top performing pages
                top_pages = page_stats.nlargest(10, 'quality_score')
                fig_top = px.bar(
                    top_pages,
                    x='quality_score',
                    y='page',
                    orientation='h',
                    title="Top 10 Pages by Quality Score",
                    labels={'quality_score': 'Quality Score', 'page': 'Page'},
                    color='quality_score',
                    color_continuous_scale='Greens'
                )
                fig_top.update_layout(height=500)
                st.plotly_chart(fig_top, use_container_width=True)
            
            # Detailed table
            st.subheader("Detailed Page Statistics")
            display_df = page_stats[['page', 'category', 'sessions', 'conversions', 
                                      'conversion_rate', 'bounce_rate', 'avg_session_duration', 
                                      'quality_score']].copy()
            display_df['bounce_rate'] = (display_df['bounce_rate'] * 100).round(2)
            display_df['conversion_rate'] = display_df['conversion_rate'].round(2)
            display_df['quality_score'] = display_df['quality_score'].round(2)
            display_df = display_df.sort_values('quality_score', ascending=False)
            
            st.dataframe(
                display_df.style.background_gradient(subset=['quality_score'], cmap='RdYlGn'),
                use_container_width=True
            )
        
        with tab3:
            st.header("Device & Country Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Device Performance")
                device_stats = analyze_device_performance(filtered_df)
                
                fig_device_perf = go.Figure()
                fig_device_perf.add_trace(go.Bar(
                    x=device_stats['device'],
                    y=device_stats['sessions'],
                    name='Sessions',
                    marker_color='lightblue'
                ))
                fig_device_perf.add_trace(go.Bar(
                    x=device_stats['device'],
                    y=device_stats['conversions'],
                    name='Conversions',
                    marker_color='darkblue'
                ))
                fig_device_perf.update_layout(
                    title="Sessions vs Conversions by Device",
                    barmode='group',
                    height=400
                )
                st.plotly_chart(fig_device_perf, use_container_width=True)
                
                st.dataframe(device_stats.style.format({
                    'bounce_rate': '{:.2%}',
                    'conversion_rate': '{:.2f}%',
                    'avg_session_duration': '{:.0f}s'
                }), use_container_width=True)
            
            with col2:
                st.subheader("Country Performance")
                country_stats = analyze_country_performance(filtered_df)
                
                fig_country = px.bar(
                    country_stats.sort_values('sessions', ascending=False).head(10),
                    x='country',
                    y='sessions',
                    title="Top 10 Countries by Sessions",
                    color='conversion_rate',
                    color_continuous_scale='Viridis'
                )
                fig_country.update_layout(height=400)
                st.plotly_chart(fig_country, use_container_width=True)
                
                st.dataframe(country_stats.sort_values('sessions', ascending=False).style.format({
                    'bounce_rate': '{:.2%}',
                    'conversion_rate': '{:.2f}%',
                    'avg_session_duration': '{:.0f}s'
                }), use_container_width=True)
        
        with tab4:
            st.header("Time-Based Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Hourly heatmap
                hourly_stats = filtered_df.groupby(['day_of_week', 'hour'])['sessions'].sum().reset_index()
                hourly_pivot = hourly_stats.pivot(index='day_of_week', columns='hour', values='sessions')
                
                # Reorder days
                day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                hourly_pivot = hourly_pivot.reindex([d for d in day_order if d in hourly_pivot.index])
                
                fig_heatmap = px.imshow(
                    hourly_pivot,
                    title="Traffic Heatmap: Day of Week vs Hour",
                    labels=dict(x="Hour of Day", y="Day of Week", color="Sessions"),
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig_heatmap, use_container_width=True)
            
            with col2:
                # Hour of day performance
                hourly_perf = filtered_df.groupby('hour').agg({
                    'sessions': 'sum',
                    'conversions': 'sum',
                    'bounce_rate': 'mean'
                }).reset_index()
                hourly_perf['conversion_rate'] = (hourly_perf['conversions'] / hourly_perf['sessions'] * 100)
                
                fig_hourly = make_subplots(specs=[[{"secondary_y": True}]])
                fig_hourly.add_trace(
                    go.Bar(x=hourly_perf['hour'], y=hourly_perf['sessions'], name='Sessions'),
                    secondary_y=False
                )
                fig_hourly.add_trace(
                    go.Scatter(x=hourly_perf['hour'], y=hourly_perf['conversion_rate'], 
                              name='Conversion Rate', mode='lines+markers', line=dict(color='red')),
                    secondary_y=True
                )
                fig_hourly.update_xaxes(title_text="Hour of Day")
                fig_hourly.update_yaxes(title_text="Sessions", secondary_y=False)
                fig_hourly.update_yaxes(title_text="Conversion Rate (%)", secondary_y=True)
                fig_hourly.update_layout(title="Hourly Performance")
                st.plotly_chart(fig_hourly, use_container_width=True)
            
            # Day of week analysis
            dow_stats = filtered_df.groupby('day_of_week').agg({
                'sessions': 'sum',
                'conversions': 'sum',
                'bounce_rate': 'mean'
            }).reset_index()
            dow_stats['conversion_rate'] = (dow_stats['conversions'] / dow_stats['sessions'] * 100)
            dow_stats['day_of_week'] = pd.Categorical(
                dow_stats['day_of_week'], 
                categories=day_order, 
                ordered=True
            )
            dow_stats = dow_stats.sort_values('day_of_week')
            
            fig_dow = px.bar(
                dow_stats,
                x='day_of_week',
                y='sessions',
                title="Traffic by Day of Week",
                color='conversion_rate',
                color_continuous_scale='RdYlGn'
            )
            st.plotly_chart(fig_dow, use_container_width=True)
        
        with tab5:
            st.header("🎯 Key Insights & Recommendations")
            
            page_stats = analyze_page_performance(filtered_df)
            device_stats = analyze_device_performance(filtered_df)
            
            # Generate insights
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.subheader("📊 Traffic Insights")
            
            # Top performing page
            best_page = page_stats.nlargest(1, 'quality_score').iloc[0]
            st.success(f"**Star Performer**: {best_page['page']} page has the highest quality score ({best_page['quality_score']:.1f}) with {best_page['sessions']:,.0f} sessions and {best_page['conversion_rate']:.2f}% conversion rate.")
            
            # Pages needing attention
            needs_attention = page_stats[page_stats['category'] == 'Needs Attention']
            if not needs_attention.empty:
                st.warning(f"**⚠️ Attention Required**: {len(needs_attention)} pages need optimization. Focus on improving '{needs_attention.iloc[0]['page']}' which has high bounce rate.")
            
            # Device insights
            best_device = device_stats.nlargest(1, 'conversion_rate').iloc[0]
            st.info(f"**Best Converting Device**: {best_device['device']} users convert at {best_device['conversion_rate']:.2f}%, consider optimizing other devices.")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.subheader("💡 Actionable Recommendations")
            
            recommendations = []
            
            # High traffic, low conversion pages
            high_traffic_low_conv = page_stats[page_stats['category'] == 'High Traffic - Low Conversion']
            if not high_traffic_low_conv.empty:
                recommendations.append(
                    f"1. **Optimize High-Traffic Pages**: Pages like {', '.join(high_traffic_low_conv['page'].head(3))} "
                    f"receive significant traffic but have below-average conversion rates. Run A/B tests on CTAs and page layout."
                )
            
            # Hidden gems
            hidden_gems = page_stats[page_stats['category'] == 'Hidden Gems']
            if not hidden_gems.empty:
                recommendations.append(
                    f"2. **Promote Hidden Gems**: {', '.join(hidden_gems['page'].head(3))} pages have excellent conversion rates "
                    f"but low traffic. Increase visibility through internal linking and marketing campaigns."
                )
            
            # High bounce rate
            high_bounce = page_stats.nlargest(3, 'bounce_rate')
            recommendations.append(
                f"3. **Reduce Bounce Rates**: Focus on {high_bounce.iloc[0]['page']} page (bounce rate: {high_bounce.iloc[0]['bounce_rate']*100:.1f}%). "
                f"Improve page load speed, content relevance, and clear CTAs."
            )
            
            # Device optimization
            worst_device = device_stats.nsmallest(1, 'conversion_rate').iloc[0]
            recommendations.append(
                f"4. **Device Optimization**: {worst_device['device']} users have the lowest conversion rate ({worst_device['conversion_rate']:.2f}%). "
                f"Ensure responsive design and test user experience on this device type."
            )
            
            # Time-based recommendation
            hourly_perf = filtered_df.groupby('hour').agg({
                'sessions': 'sum',
                'conversions': 'sum'
            }).reset_index()
            hourly_perf['conversion_rate'] = (hourly_perf['conversions'] / hourly_perf['sessions'] * 100)
            best_hour = hourly_perf.nlargest(1, 'conversion_rate').iloc[0]
            recommendations.append(
                f"5. **Timing Strategy**: Peak conversion times are around {int(best_hour['hour'])}:00. "
                f"Schedule marketing campaigns and promotions during these high-converting hours."
            )
            
            for rec in recommendations:
                st.markdown(rec)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Export recommendations
            if st.button("📥 Export Full Report"):
                report_data = {
                    'Page Performance': page_stats,
                    'Device Analysis': device_stats,
                    'Daily Trends': analyze_time_trends(filtered_df)
                }
                
                with pd.ExcelWriter('analytics_report.xlsx', engine='openpyxl') as writer:
                    for sheet_name, data in report_data.items():
                        data.to_excel(writer, sheet_name=sheet_name, index=False)
                
                st.success("✅ Report exported successfully as 'analytics_report.xlsx'!")
    
    except FileNotFoundError:
        st.error("❌ Data file 'web_traffic_data.csv' not found. Please ensure the file is in the same directory as this app.")
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")

if __name__ == "__main__":
    main()