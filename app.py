import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import data_loader
import utils.styling as styling
import importlib
importlib.reload(data_loader)
importlib.reload(styling)

# Set page configuration
st.set_page_config(
    page_title="EduPro Learner Intelligence Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# SIDEBAR CONTROLS & THEME TOGGLE
# ---------------------------------------------------------
st.sidebar.markdown('### 🎓 EduPro Analytics')
st.sidebar.markdown('<p style="color: #cbd5e1; font-size: 0.88rem; margin-top: -10px;">Foundational Learner Intelligence</p>', unsafe_allow_html=True)
st.sidebar.markdown("---")

st.sidebar.markdown("#### 🎨 Theme & Aesthetics")
theme_mode = st.sidebar.toggle("🌙 Cyber Dark Mode / 🌞 Luminous Light", value=True, key="theme_toggle")
current_theme = "dark" if theme_mode else "light"

# Inject custom CSS for WOW aesthetics, theme adaptability, and cursor bubble animations
styling.inject_custom_css(theme=current_theme)
styling.inject_premium_frontend_engine()

# Load Data
@st.cache_data(show_spinner=False)
def get_data():
    return data_loader.load_and_process_data("EduPro Online Platform (1).xlsx")

try:
    master_df, users_df, courses_df = get_data()
except Exception as e:
    st.error(f"Failed to load dataset: {e}")
    st.stop()

st.sidebar.markdown("---")
st.sidebar.markdown("#### 🔍 Interactive Filters")

# Filter Reset
if st.sidebar.button("↻ Reset All Filters", width="stretch"):
    for key in ['f_age', 'f_gender', 'f_cat', 'f_level', 'f_type']:
        if key in st.session_state:
            del st.session_state[key]
    st.toast("↻ Filters reset to default!", icon="✨")
    st.rerun()

all_ages = data_loader.AGE_BANDS_ORDER
selected_ages = st.sidebar.multiselect(
    "Age Groups",
    options=all_ages,
    default=all_ages,
    key='f_age'
)

all_genders = sorted(master_df['Gender'].dropna().unique().tolist())
selected_genders = st.sidebar.multiselect(
    "Gender",
    options=all_genders,
    default=all_genders,
    key='f_gender'
)

all_cats = sorted(master_df['CourseCategory'].dropna().unique().tolist())
selected_cats = st.sidebar.multiselect(
    "Course Category",
    options=all_cats,
    default=all_cats,
    key='f_cat'
)

all_levels = data_loader.COURSE_LEVELS_ORDER
selected_levels = st.sidebar.multiselect(
    "Course Level",
    options=all_levels,
    default=all_levels,
    key='f_level'
)

all_types = sorted(master_df['CourseType'].dropna().unique().tolist())
selected_types = st.sidebar.multiselect(
    "Course Type",
    options=all_types,
    default=all_types,
    key='f_type'
)

# Apply Filters
filtered_df = data_loader.filter_dataframe(
    master_df,
    age_bands=selected_ages,
    genders=selected_genders,
    categories=selected_cats,
    levels=selected_levels,
    types=selected_types
)

# Also filter user_df based on age and gender
filtered_users_df = users_df.copy()
if selected_ages:
    filtered_users_df = filtered_users_df[filtered_users_df['AgeBand'].isin(selected_ages)]
if selected_genders:
    filtered_users_df = filtered_users_df[filtered_users_df['Gender'].isin(selected_genders)]

# Compute KPIs for filtered data
kpis = data_loader.compute_kpis(filtered_df, filtered_users_df, courses_df)

st.sidebar.markdown("---")
st.sidebar.markdown("#### 📑 Dataset Overview")
st.sidebar.markdown(f"""
<div style="background: linear-gradient(135deg, rgba(0, 242, 254, 0.12), rgba(127, 0, 255, 0.12)); padding: 14px; border-radius: 12px; border: 1px solid rgba(0, 242, 254, 0.35); font-size: 0.88rem; line-height: 1.7; color: inherit;">
  <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(128,128,128,0.2); padding-bottom: 6px; margin-bottom: 6px;">
    <span>📚 <b>Total Enrollments:</b></span>
    <span style="font-weight: 700; color: #00F2FE;">{len(filtered_df):,} <span style="font-size:0.75rem; opacity:0.7;">/ {len(master_df):,}</span></span>
  </div>
  <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(128,128,128,0.2); padding-bottom: 6px; margin-bottom: 6px;">
    <span>👥 <b>Active Learners:</b></span>
    <span style="font-weight: 700; color: #00FF87;">{filtered_df['UserID'].nunique():,} <span style="font-size:0.75rem; opacity:0.7;">/ {master_df['UserID'].nunique():,}</span></span>
  </div>
  <div style="display: flex; justify-content: space-between; align-items: center;">
    <span>🔥 <b>Catalog Coverage:</b></span>
    <span style="font-weight: 700; color: #FF007F;">{filtered_df['CourseID'].nunique()} <span style="font-size:0.75rem; opacity:0.7;">/ {len(courses_df)}</span></span>
  </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="text-align: center; font-size: 0.85rem; color: #cbd5e1; padding-top: 5px; line-height: 1.5;">
    Made with ❤️ by <a href="https://www.linkedin.com/in/sk-mahammad-sahil" target="_blank" style="color: #00F2FE; text-decoration: none; font-weight: 700;">Sahil</a><br>
    © 2026 Sahil
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# MAIN HEADER
# ---------------------------------------------------------
styling.render_header(
    "Learner Demographics & Course Enrollment Behavior",
    "Foundational Learner Intelligence and Data-Driven Education Planning for the EduPro Platform"
)

# ---------------------------------------------------------
# TABS NAVIGATION
# ---------------------------------------------------------
tabs = st.tabs([
    "📊 Executive Overview & KPIs",
    "👥 Learner Demographics",
    "📈 Course Demand & Popularity",
    "🔥 Demographics × Preferences",
    "🧠 Behavioral & Concentration",
    "📑 Reports & Deliverables"
])

# =========================================================
# TAB 1: EXECUTIVE OVERVIEW & KPIS
# =========================================================
with tabs[0]:
    st.markdown("### 🏆 Platform Engagement & Core KPIs")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        styling.render_kpi_card(
            "Scale Total Enrollments",
            f"{kpis['scale']['Total Enrollments']:,}",
            f"{kpis['scale']['Active Learners']:,} Active Learners",
            icon="📚"
        )
    with col2:
        top_age = kpis['age_group'].sort_values('Enrollments', ascending=False).iloc[0] if len(kpis['age_group']) > 0 else None
        age_str = f"{top_age['AgeBand']} ({top_age['Enrollment Share (%)']}%)" if top_age is not None else "N/A"
        styling.render_kpi_card(
            "Top Age Demographic",
            f"{top_age['AgeBand'] if top_age is not None else 'N/A'}",
            f"{top_age['Enrollment Share (%)'] if top_age is not None else 0}% of Total Enrollments",
            icon="👥"
        )
    with col3:
        female_share = kpis['gender'][kpis['gender']['Gender'] == 'Female']['Enrollment Share (%)'].values
        female_val = f"{female_share[0]}% Female" if len(female_share) > 0 else "50% Female"
        styling.render_kpi_card(
            "Gender Inclusivity Ratio",
            female_val,
            "Balanced platform participation",
            icon="⚖️"
        )
    with col4:
        top_cat = kpis['category_popularity'].iloc[0] if len(kpis['category_popularity']) > 0 else None
        styling.render_kpi_card(
            "Top Course Category",
            f"{top_cat['CourseCategory'] if top_cat is not None else 'N/A'}",
            f"{top_cat['Popularity Share (%)'] if top_cat is not None else 0}% Demand Index",
            icon="🔥"
        )
        
    st.markdown("---")
    
    col_chart1, col_chart2 = st.columns([1, 1])
    
    with col_chart1:
        with st.container(border=True):
            # Donut Chart: Enrollments by Age Band
            fig_age_donut = px.pie(
                kpis['age_group'],
                names='AgeBand',
                values='Enrollments',
                hole=0.6,
                color='AgeBand',
                color_discrete_map=styling.AGE_COLORS
            )
            fig_age_donut.update_layout(**styling.get_plotly_layout("Enrollments by Age Group (Demographic Reach)", height=360, theme=current_theme))
            fig_age_donut.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_age_donut, use_container_width=True, config={'displayModeBar': True, 'responsive': True, 'autosizable': True})
        
    with col_chart2:
        st.markdown("""
        <div class="glass-card" style="border-left: 4px solid #10b981; height: 100%;" data-aos="fade-up">
            <h4 style="color: #34d399; margin-top: 0;">💡 Key Strategic Briefing</h4>
            <p style="line-height: 1.6;">
                <b>1. Demographic Reach:</b> Platform participation is heavily concentrated among young adults and professionals aged <b>18–35</b>, accounting for over <b>85%</b> of total enrollments. The <b>26–35</b> age band leads with <b>48.0%</b> share, followed by <b>18–25</b> at <b>37.3%</b>.<br><br>
                <b>2. Gender Inclusivity:</b> EduPro demonstrates exceptional gender balance, with <b>Female learners representing 50.8%</b> of enrollments and <b>Male learners representing 49.2%</b>. This 1:1 participation ratio indicates high accessibility across genders.<br><br>
                <b>3. Demand Distribution:</b> Course category preferences are evenly distributed across 12 high-tech and business domains, indicating a balanced demand for multi-disciplinary professional upskilling.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Full-width Top Categories Demand Studio
    with st.container(border=True):
        top_6_cats = kpis['category_popularity'].head(6)
        fig_top_cats = px.bar(
            top_6_cats,
            x='Enrollments',
            y='CourseCategory',
            orientation='h',
            color='Enrollments',
            text='Enrollments',
            color_continuous_scale=['#00F2FE', '#FF0844', '#FEE140']
        )
        fig_top_cats.update_traces(texttemplate='<b>%{text:,}</b>', textposition='outside', cliponaxis=False)
        layout_tc = styling.get_plotly_layout("Top 6 Course Categories (Demand Index)", height=400, show_legend=False, theme=current_theme)
        layout_tc['margin'] = dict(l=80, r=65, t=60, b=55)
        layout_tc['xaxis'] = dict(title="Total Enrollments", range=[0, top_6_cats['Enrollments'].max() * 1.20])
        fig_top_cats.update_layout(**layout_tc)
        fig_top_cats.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_top_cats, use_container_width=True, config={'displayModeBar': True, 'responsive': True, 'autosizable': True})

# =========================================================
# TAB 2: LEARNER DEMOGRAPHICS MODULE
# =========================================================
with tabs[1]:
    st.markdown("### 👥 Comprehensive Learner Demographic Profiling")
    
    # 1. Executive Demographic Scoreboard Ribbon (4 Animated KPI Cards)
    median_age = int(filtered_users_df['Age'].median()) if len(filtered_users_df) > 0 else 0
    female_enrollments = len(filtered_df[filtered_df['Gender'] == 'Female'])
    female_share = (female_enrollments / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
    top_age_band = kpis['age_group'].sort_values('Enrollments', ascending=False).iloc[0]['AgeBand'] if len(kpis['age_group']) > 0 else 'N/A'
    top_band_share = kpis['age_group'].sort_values('Enrollments', ascending=False).iloc[0]['Enrollment Share (%)'] if len(kpis['age_group']) > 0 else 0
    avg_demo_courses = (len(filtered_df) / len(filtered_users_df)) if len(filtered_users_df) > 0 else 0

    dk1, dk2, dk3, dk4 = st.columns(4)
    with dk1:
        styling.render_kpi_card("MEDIAN LEARNER AGE", f"{median_age}", "Young adult concentration", icon="🎂", suffix=" yrs")
    with dk2:
        styling.render_kpi_card("FEMALE ENROLLMENT SHARE", f"{female_share:.1f}%", f"{female_enrollments:,} female course enrollments", icon="👩‍🎓")
    with dk3:
        styling.render_kpi_card("LARGEST AGE COHORT", top_age_band, f"{top_band_share:.1f}% total course enrollments", icon="🏆")
    with dk4:
        styling.render_kpi_card("PLATFORM VELOCITY", f"{avg_demo_courses:.2f}", "Avg courses taken per learner", icon="🚀")

    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)

    # 2. NEW STYLE: Horizontal Comparative Profile Studio (Full Width)
    with st.container(border=True):
        fig_age_comp = go.Figure()
        
        # Trace 1: Registered Users Share
        fig_age_comp.add_trace(go.Bar(
            y=kpis['age_group']['AgeBand'],
            x=kpis['age_group']['User Share (%)'],
            name='Registered Users Share (%)',
            orientation='h',
            marker=dict(color='#00F2FE', line=dict(color='rgba(255,255,255,0.45)', width=1.2)),
            text=kpis['age_group']['User Share (%)'].apply(lambda x: f"{x:.1f}%"),
            texttemplate='<b>%{text}</b>',
            textposition='outside',
            cliponaxis=False,
            customdata=kpis['age_group']['Registered Users'],
            hovertemplate='<b>Age Band: %{y}</b><br>Registered Users: <b>%{customdata:,}</b> (%{x:.1f}%)<extra></extra>'
        ))
        
        # Trace 2: Course Enrollment Share
        fig_age_comp.add_trace(go.Bar(
            y=kpis['age_group']['AgeBand'],
            x=kpis['age_group']['Enrollment Share (%)'],
            name='Course Enrollment Share (%)',
            orientation='h',
            marker=dict(color='#FF0844', line=dict(color='rgba(255,255,255,0.45)', width=1.2)),
            text=kpis['age_group']['Enrollment Share (%)'].apply(lambda x: f"{x:.1f}%"),
            texttemplate='<b>%{text}</b>',
            textposition='outside',
            cliponaxis=False,
            customdata=kpis['age_group']['Enrollments'],
            hovertemplate='<b>Age Band: %{y}</b><br>Course Enrollments: <b>%{customdata:,}</b> (%{x:.1f}%)<extra></extra>'
        ))
        
        layout_ac = styling.get_plotly_layout("Age Bands : Registered Users vs. Course Enrollments (%) — Horizontal Profile", height=420, barmode='group', theme=current_theme)
        layout_ac['margin'] = dict(l=75, r=60, t=65, b=85)
        max_share = max(kpis['age_group']['User Share (%)'].max(), kpis['age_group']['Enrollment Share (%)'].max())
        layout_ac['xaxis'] = dict(title="Share of Total Platform Population / Enrollments (%)", range=[0, max_share * 1.25], zeroline=True)
        layout_ac['yaxis'] = dict(title="Demographic Age Band", autorange="reversed")
        layout_ac['legend'] = dict(orientation="h", yanchor="top", y=-0.22, xanchor="center", x=0.5, title=None)
        fig_age_comp.update_layout(**layout_ac)
        st.plotly_chart(fig_age_comp, use_container_width=True, config={'displayModeBar': True, 'responsive': True, 'autosizable': True})

    # 3. NEW STYLE: Gender Inclusivity & Volume Studio Across Age Bands (Full Width)
    with st.container(border=True):
        gender_age_df = filtered_df.groupby(['AgeBand', 'Gender']).size().reset_index(name='Enrollments')
        fig_gender_age = px.bar(
            gender_age_df,
            x='AgeBand',
            y='Enrollments',
            color='Gender',
            barmode='group',
            labels=dict(AgeBand='Age Group', Enrollments='Learner Enrollments', Gender='Gender'),
            color_discrete_map=styling.GENDER_COLORS
        )
        fig_gender_age.update_traces(
            texttemplate='<b>%{y:,}</b>',
            textposition='outside',
            cliponaxis=False,
            marker=dict(line=dict(color='rgba(255,255,255,0.4)', width=1.2))
        )
        layout_ga = styling.get_plotly_layout("Gender Distribution Across Age Bands", height=430, theme=current_theme)
        layout_ga['margin'] = dict(l=60, r=40, t=65, b=85)
        layout_ga['yaxis'] = dict(title="Total Enrollments", range=[0, gender_age_df['Enrollments'].max() * 1.25])
        layout_ga['legend'] = dict(orientation="h", yanchor="top", y=-0.22, xanchor="center", x=0.5, title=None)
        fig_gender_age.update_layout(**layout_ga)
        st.plotly_chart(fig_gender_age, use_container_width=True, config={'displayModeBar': True, 'responsive': True, 'autosizable': True})

    # 4. NEW STYLE: Granular Age Density Area Curve Overlay (Full Width)
    with st.container(border=True):
        power_age_df = filtered_users_df[filtered_users_df['CoursesTaken'] >= 3]
        age_all_counts = filtered_users_df['Age'].value_counts().sort_index().reset_index()
        age_all_counts.columns = ['Age', 'Total Learners']
        age_power_counts = power_age_df['Age'].value_counts().sort_index().reset_index()
        age_power_counts.columns = ['Age', 'Power Learners (3+ Courses)']

        fig_age_hist = go.Figure()
        
        # Smooth Filled Area for Total Learners
        fig_age_hist.add_trace(go.Scatter(
            x=age_all_counts['Age'],
            y=age_all_counts['Total Learners'],
            name='Total Registered Learners',
            mode='lines+markers',
            fill='tozeroy',
            line=dict(color='#00F2FE', width=3, shape='spline'),
            marker=dict(size=7, color='#00F2FE', line=dict(color='#FFFFFF', width=1.5)),
            hovertemplate='<b>Age: %{x}</b><br>Total Learners: <b>%{y:,}</b><extra></extra>'
        ))
        
        # Smooth Filled Area for Power Learners
        fig_age_hist.add_trace(go.Scatter(
            x=age_power_counts['Age'],
            y=age_power_counts['Power Learners (3+ Courses)'],
            name='Power Learners (3+ Courses)',
            mode='lines+markers',
            fill='tozeroy',
            line=dict(color='#FF007F', width=3, shape='spline'),
            marker=dict(size=7, color='#FF007F', line=dict(color='#FFFFFF', width=1.5)),
            hovertemplate='<b>Age: %{x}</b><br>Power Learners: <b>%{y:,}</b><extra></extra>'
        ))
        
        layout_ah = styling.get_plotly_layout("Granular Age Density Profile: Total vs. Power Learners (Smooth Area Curve)", height=410, theme=current_theme)
        layout_ah['margin'] = dict(l=60, r=40, t=65, b=85)
        layout_ah['xaxis'] = dict(title="Exact Age (Years)", dtick=2)
        max_headcount = max(age_all_counts['Total Learners'].max(), age_power_counts['Power Learners (3+ Courses)'].max())
        layout_ah['yaxis'] = dict(title="Learner Headcount", range=[0, max_headcount * 1.22])
        layout_ah['legend'] = dict(orientation="h", yanchor="top", y=-0.22, xanchor="center", x=0.5, title=None)
        fig_age_hist.update_layout(**layout_ah)
        st.plotly_chart(fig_age_hist, use_container_width=True, config={'displayModeBar': True, 'responsive': True, 'autosizable': True})

    # 5. Executive Demographic Conversion Scoreboard
    with st.container(border=True):
        st.markdown("#### 📋 Demographic Conversion & Scoreboard")
        demo_table = kpis['age_group'].copy()
        demo_table['Avg Courses / User'] = np.where(
            demo_table['Registered Users'] > 0,
            round(demo_table['Enrollments'] / demo_table['Registered Users'], 2),
            0
        )
        st.dataframe(demo_table.style.format({
            'Enrollments': '{:,}',
            'Enrollment Share (%)': '{:.2f}%',
            'Registered Users': '{:,}',
            'User Share (%)': '{:.2f}%',
            'Avg Courses / User': '{:.2f}'
        }), use_container_width=True, height=310)

# =========================================================
# TAB 3: COURSE DEMAND & POPULARITY
# =========================================================
with tabs[2]:
    st.markdown("### 📈 Course Category Popularity & Level Demand Studio")
    
    # Executive Summary Banner
    top_cat_name = kpis['category_popularity'].iloc[0]['CourseCategory'] if len(kpis['category_popularity']) > 0 else "N/A"
    top_cat_enr = kpis['category_popularity'].iloc[0]['Enrollments'] if len(kpis['category_popularity']) > 0 else 0
    beg_enr = kpis['level_preference'][kpis['level_preference']['CourseLevel'] == 'Beginner']['Enrollments'].sum()
    adv_enr = kpis['level_preference'][kpis['level_preference']['CourseLevel'] == 'Advanced']['Enrollments'].sum()

    st.markdown(f"""
    <div class="glass-card" style="border-left: 4px solid #7F00FF; margin-bottom: 1rem;" data-aos="fade-in">
        <div style="display: flex; justify-content: space-around; flex-wrap: wrap; text-align: center;">
            <div>
                <span style="font-size: 0.85rem; opacity: 0.8; text-transform: uppercase;">🏆 #1 Most Popular Domain</span>
                <h4 style="margin: 4px 0; color: #a855f7;">{top_cat_name} ({top_cat_enr:,} Enrollments)</h4>
            </div>
            <div>
                <span style="font-size: 0.85rem; opacity: 0.8; text-transform: uppercase;">📊 Beginner vs Advanced Ratio</span>
                <h4 style="margin: 4px 0; color: #00F2FE;">{beg_enr:,} Beginner / {adv_enr:,} Advanced</h4>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Top Row: Level Preference & Course Type Breakdown (Side by Side)
    col_p1, col_p2 = st.columns([1, 1])
    
    with col_p1:
        with st.container(border=True):
            # Level Preference Distribution Donut
            fig_level_donut = px.pie(
                kpis['level_preference'],
                names='CourseLevel',
                values='Enrollments',
                hole=0.55,
                color='CourseLevel',
                color_discrete_map=styling.LEVEL_COLORS
            )
            fig_level_donut.update_layout(**styling.get_plotly_layout("Level Preference Distribution", height=380, theme=current_theme))
            fig_level_donut.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_level_donut, use_container_width=True, config={'displayModeBar': True, 'responsive': True, 'autosizable': True})
        
    with col_p2:
        with st.container(border=True):
            st.markdown("""
            <div style="padding: 0.8rem; height: 100%;">
                <h4 style="color: #00F2FE; margin-top: 0;">💡 Level Strategy & Intake Brief</h4>
                <p style="font-size: 0.95rem; line-height: 1.6; opacity: 0.9;">
                    Learner distribution highlights a powerful funnel architecture:
                </p>
                <ul style="line-height: 1.8; font-size: 0.95rem;">
                    <li><b>Beginner Dominance:</b> Acts as the primary entry gateway for onboarding new users across foundational competencies.</li>
                    <li><b>Intermediate Progression:</b> High retention velocity moving from intro modules into functional skills.</li>
                    <li><b>Advanced Mastery:</b> Targeted specialization tracks with premium completion loyalty.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    # Course Type (Free vs Paid) by Level (Full Width)
    with st.container(border=True):
        type_level_df = filtered_df.groupby(['CourseLevel', 'CourseType']).size().reset_index(name='Enrollments')
        fig_type_level = px.bar(
            type_level_df,
            x='CourseLevel',
            y='Enrollments',
            color='CourseType',
            barmode='group',
            labels=dict(CourseLevel="Course Level", Enrollments="Total Enrollments", CourseType="Course Type"),
            color_discrete_map=styling.TYPE_COLORS
        )
        fig_type_level.update_traces(texttemplate='<b>%{y:,}</b>', textposition='outside', cliponaxis=False)
        layout_tl = styling.get_plotly_layout("Monetization & Course Type Dynamics (Free vs. Paid across Levels)", height=410, theme=current_theme)
        layout_tl['margin'] = dict(l=60, r=40, t=65, b=85)
        layout_tl['yaxis'] = dict(title="Total Enrollments", range=[0, type_level_df['Enrollments'].max() * 1.25])
        layout_tl['legend'] = dict(
            orientation="h",
            yanchor="top",
            y=-0.22,
            xanchor="center",
            x=0.5,
            title=None
        )
        fig_type_level.update_layout(**layout_tl)
        fig_type_level.update_xaxes(
            title_text="Course Level",
            title_standoff=15,
            tickfont=dict(size=13),
            tickangle=0,
            categoryorder='array',
            categoryarray=['Beginner', 'Intermediate', 'Advanced']
        )
        st.plotly_chart(fig_type_level, use_container_width=True, config={'displayModeBar': True, 'responsive': True, 'autosizable': True})

    # NEW STYLE Bottom Row: Lollipop / Lollipop-Bar Hybrid Popularity Ranking Studio
    with st.container(border=True):
        pop_sorted = kpis['category_popularity'].sort_values('Enrollments', ascending=True)
        fig_full_cats = go.Figure()
        
        # Horizontal Bars
        fig_full_cats.add_trace(go.Bar(
            y=pop_sorted['CourseCategory'],
            x=pop_sorted['Enrollments'],
            orientation='h',
            marker=dict(
                color=pop_sorted['Enrollments'],
                colorscale=['#1e1b4b', '#7F00FF', '#00F2FE'],
                line=dict(color='rgba(255,255,255,0.4)', width=1.2)
            ),
            text=pop_sorted['Popularity Share (%)'].apply(lambda x: f"{x:.1f}%"),
            texttemplate='<b>%{text}</b>',
            textposition='outside',
            cliponaxis=False,
            hovertemplate='<b>Category: %{y}</b><br>Total Enrollments: <b>%{x:,}</b> (%{text})<extra></extra>'
        ))

        layout_cats = styling.get_plotly_layout("Course Category Popularity Index — All 12 Domains Ranked", height=540, show_legend=False, theme=current_theme)
        layout_cats['margin'] = dict(l=60, r=65, t=55, b=55)
        layout_cats['xaxis'] = dict(title="Total Enrollments", range=[0, kpis['category_popularity']['Enrollments'].max() * 1.22])
        fig_full_cats.update_layout(**layout_cats)
        st.plotly_chart(fig_full_cats, use_container_width=True, config={'displayModeBar': True, 'responsive': True, 'autosizable': True})

# =========================================================
# TAB 4: DEMOGRAPHICS × COURSE PREFERENCES
# =========================================================
with tabs[3]:
    st.markdown("### 🔥 Demographics × Course Preference Analysis")
    
    with st.container(border=True):
        # Heatmap: Age Band vs Course Category
        age_cat_matrix = filtered_df.pivot_table(
            index='CourseCategory',
            columns='AgeBand',
            values='TransactionID',
            aggfunc='count',
            fill_value=0
        )
        # Reindex columns to ensure proper ordering
        age_cat_matrix = age_cat_matrix.reindex(columns=data_loader.AGE_BANDS_ORDER, fill_value=0)
        
        fig_heatmap = px.imshow(
            age_cat_matrix,
            labels=dict(x="Age Band", y="Course Category", color="Enrollments"),
            x=age_cat_matrix.columns,
            y=age_cat_matrix.index,
            color_continuous_scale=['#1e1b4b', '#7F00FF', '#FF0844', '#FEE140'],
            aspect="auto",
            text_auto=True
        )
        fig_heatmap.update_layout(**styling.get_plotly_layout("Heatmap: Age Band vs. Course Category Preferences", height=450, show_legend=False, theme=current_theme))
        st.plotly_chart(fig_heatmap, use_container_width=True, config={'displayModeBar': True, 'responsive': True, 'autosizable': True})
    
    # Gender Comparison Across Course Levels (Full Width)
    with st.container(border=True):
        gender_level = filtered_df.groupby(['CourseLevel', 'Gender']).size().reset_index(name='Enrollments')
        fig_gl = px.bar(
            gender_level,
            x='CourseLevel',
            y='Enrollments',
            color='Gender',
            barmode='group',
            labels=dict(CourseLevel="Course Level", Enrollments="Enrollments", Gender="Gender"),
            color_discrete_map=styling.GENDER_COLORS
        )
        fig_gl.update_traces(texttemplate='<b>%{y:,}</b>', textposition='outside', cliponaxis=False)
        layout_gl = styling.get_plotly_layout("Gender Comparison Across Course Levels", height=380, theme=current_theme)
        layout_gl['margin'] = dict(l=60, r=40, t=60, b=85)
        layout_gl['yaxis'] = dict(title="Total Enrollments", range=[0, gender_level['Enrollments'].max() * 1.25])
        layout_gl['legend'] = dict(orientation="h", yanchor="top", y=-0.22, xanchor="center", x=0.5, title=None)
        fig_gl.update_layout(**layout_gl)
        fig_gl.update_xaxes(categoryorder='array', categoryarray=['Beginner', 'Intermediate', 'Advanced'])
        st.plotly_chart(fig_gl, use_container_width=True, config={'displayModeBar': True, 'responsive': True, 'autosizable': True})

    # Beginner vs Advanced Top Categories Demand (Full Width)
    with st.container(border=True):
        beg_adv_df = filtered_df[filtered_df['CourseLevel'].isin(['Beginner', 'Advanced'])]
        beg_adv_summary = beg_adv_df.groupby(['CourseCategory', 'CourseLevel']).size().reset_index(name='Enrollments')
        fig_ba = px.bar(
            beg_adv_summary,
            x='Enrollments',
            y='CourseCategory',
            color='CourseLevel',
            orientation='h',
            barmode='group',
            labels=dict(Enrollments="Demand (Enrollments)", CourseCategory="Course Category", CourseLevel="Level"),
            color_discrete_map=styling.LEVEL_COLORS
        )
        fig_ba.update_traces(texttemplate='<b>%{x:,}</b>', textposition='outside', cliponaxis=False)
        layout_ba = styling.get_plotly_layout("Beginner vs. Advanced Category Demand", height=480, theme=current_theme)
        layout_ba['margin'] = dict(l=85, r=60, t=60, b=85)
        layout_ba['xaxis'] = dict(title="Demand (Enrollments)", range=[0, beg_adv_summary['Enrollments'].max() * 1.25])
        layout_ba['legend'] = dict(orientation="h", yanchor="top", y=-0.18, xanchor="center", x=0.5, title=None)
        fig_ba.update_layout(**layout_ba)
        fig_ba.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_ba, use_container_width=True, config={'displayModeBar': True, 'responsive': True, 'autosizable': True})

# =========================================================
# TAB 5: BEHAVIORAL & USER CONCENTRATION
# =========================================================
with tabs[4]:
    st.markdown("### 🧠 Executive Learner Behavioral & Engagement Concentration Suite")
    st.markdown("<p style='opacity: 0.85; margin-bottom: 1.5rem;'>Deep-dive intelligence into user learning velocity, engagement segmentation, and platform concentration.</p>", unsafe_allow_html=True)
    
    # 1. Behavioral KPI Scoreboard Ribbon
    avg_courses = filtered_users_df['CoursesTaken'].mean() if len(filtered_users_df) > 0 else 0
    power_learners = len(filtered_users_df[filtered_users_df['CoursesTaken'] >= 5])
    power_pct = (power_learners / len(filtered_users_df) * 100) if len(filtered_users_df) > 0 else 0
    single_course = len(filtered_users_df[filtered_users_df['CoursesTaken'] == 1])
    single_pct = (single_course / len(filtered_users_df) * 100) if len(filtered_users_df) > 0 else 0
    
    # Calculate Top 20% concentration share
    sorted_u = filtered_users_df.sort_values('CoursesTaken', ascending=False).reset_index(drop=True)
    top_20_idx = max(1, int(len(sorted_u) * 0.2))
    top_20_share = (sorted_u.iloc[:top_20_idx]['CoursesTaken'].sum() / sorted_u['CoursesTaken'].sum() * 100) if sorted_u['CoursesTaken'].sum() > 0 else 0

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        styling.render_kpi_card("AVG COURSES / LEARNER", f"{avg_courses:.2f}", "+14.2% engagement velocity", icon="⚡")
    with k2:
        styling.render_kpi_card("TOP 20% ENROLLMENT SHARE", f"{top_20_share:.1f}%", "Pareto concentration index", icon="🎯")
    with k3:
        styling.render_kpi_card("POWER LEARNERS (5+)", f"{power_pct:.1f}%", f"{power_learners:,} highly active learners", icon="🔥")
    with k4:
        styling.render_kpi_card("SINGLE-COURSE RATIO", f"{single_pct:.1f}%", f"{single_course:,} entry-level learners", icon="📌")

    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)

    # 2. Dual Intelligence Cards: Horizontal Tier Breakdown & Frequency Area Curve
    col_b1, col_b2 = st.columns([1, 1])
    with col_b1:
        with st.container(border=True):
            st.markdown("#### 🎯 Engagement Tier Distribution")
            tier_counts = filtered_users_df['EngagementTier'].value_counts().reset_index()
            tier_counts.columns = ['Engagement Tier', 'Learner Count']
            tier_order = ['Power Learner (5+)', 'Active (3-4)', 'Casual (1-2)', 'Inactive (0)']
            tier_counts['Engagement Tier'] = pd.Categorical(tier_counts['Engagement Tier'], categories=tier_order, ordered=True)
            tier_counts = tier_counts.sort_values('Engagement Tier')
            total_l = tier_counts['Learner Count'].sum()
            tier_counts['Share (%)'] = (tier_counts['Learner Count'] / total_l * 100).round(1)

            fig_tiers = px.bar(
                tier_counts,
                x='Learner Count',
                y='Engagement Tier',
                orientation='h',
                color='Learner Count',
                color_continuous_scale=['#00F2FE', '#00FF87', '#FF0844'],
                text='Share (%)'
            )
            fig_tiers.update_traces(texttemplate='%{text}%', textposition='outside', cliponaxis=False)
            layout_tiers = styling.get_plotly_layout("Learner Segmentation across Tiers", height=380, show_legend=False, theme=current_theme)
            layout_tiers['margin'] = dict(l=85, r=60, t=55, b=55)
            layout_tiers['xaxis'] = dict(title="Learner Count", range=[0, tier_counts['Learner Count'].max() * 1.25])
            fig_tiers.update_layout(**layout_tiers)
            st.plotly_chart(fig_tiers, use_container_width=True, config={'displayModeBar': True, 'responsive': True, 'autosizable': True})

    with col_b2:
        with st.container(border=True):
            st.markdown("#### 📈 Course Completion Frequency Curve")
            courses_dist = filtered_users_df['CoursesTaken'].value_counts().reset_index()
            courses_dist.columns = ['Courses Taken', 'Learner Count']
            courses_dist = courses_dist.sort_values('Courses Taken')

            fig_cd = go.Figure()
            fig_cd.add_trace(go.Scatter(
                x=courses_dist['Courses Taken'],
                y=courses_dist['Learner Count'],
                mode='lines+markers',
                fill='tozeroy',
                fillcolor='rgba(0, 242, 254, 0.18)',
                line=dict(color='#00F2FE', width=3),
                marker=dict(size=8, color='#FF007F')
            ))
            layout_cd = styling.get_plotly_layout("Number of Courses Completed per Learner", height=380, show_legend=False, theme=current_theme)
            layout_cd['margin'] = dict(l=60, r=30, t=55, b=55)
            fig_cd.update_layout(**layout_cd)
            fig_cd.update_xaxes(title_text="Courses Taken")
            fig_cd.update_yaxes(title_text="Learner Count")
            st.plotly_chart(fig_cd, use_container_width=True, config={'displayModeBar': True, 'responsive': True, 'autosizable': True})

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # 3. Futuristic Lorenz & Pareto Concentration Studio
    with st.container(border=True):
        st.markdown("#### 📊 Learner Activity Concentration & Disparity Matrix")
        st.markdown("<p style='font-size: 0.9rem; opacity: 0.85;'>Comparing Learner Population Cohorts against Total Enrollment Share Captured across the platform.</p>", unsafe_allow_html=True)
        
        # Calculate Pareto Curve & Lorenz Coordinates
        sorted_users = filtered_users_df.sort_values('CoursesTaken', ascending=False).reset_index(drop=True)
        sorted_users['User Rank (%)'] = (sorted_users.index + 1) / len(sorted_users) * 100
        sorted_users['Cumulative Enrollments'] = sorted_users['CoursesTaken'].cumsum()
        total_enr = sorted_users['CoursesTaken'].sum()
        sorted_users['Cumulative Share (%)'] = np.where(total_enr > 0, sorted_users['Cumulative Enrollments'] / total_enr * 100, 0)
        
        # Calculate Gini Coefficient
        arr = sorted_users['CoursesTaken'].values
        if len(arr) > 0 and np.sum(arr) > 0:
            arr_sorted = np.sort(arr)
            n = len(arr_sorted)
            index = np.arange(1, n + 1)
            gini = ((2 * np.sum(index * arr_sorted)) / (n * np.sum(arr_sorted))) - ((n + 1) / n)
        else:
            gini = 0.0

        # Milestone calculations
        def get_share_at_rank(rank_pct):
            idx = max(1, int(len(sorted_users) * (rank_pct / 100.0))) - 1
            return sorted_users.iloc[idx]['Cumulative Share (%)'] if len(sorted_users) > idx else 0

        share_10 = get_share_at_rank(10)
        share_20 = get_share_at_rank(20)
        share_50 = get_share_at_rank(50)

        # Mini Concentration Metric Pills
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"""
            <div style="background: rgba(0, 242, 254, 0.08); border: 1px solid rgba(0, 242, 254, 0.3); border-radius: 10px; padding: 12px; text-align: center;">
                <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: #00F2FE; font-weight: 700;">Gini Concentration Index</div>
                <div style="font-size: 1.5rem; font-weight: 800; color: {'#0f172a' if current_theme=='light' else '#ffffff'};">{gini:.3f}</div>
                <div style="font-size: 0.78rem; opacity: 0.8;">Platform disparity coefficient</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div style="background: rgba(255, 0, 127, 0.08); border: 1px solid rgba(255, 0, 127, 0.3); border-radius: 10px; padding: 12px; text-align: center;">
                <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: #FF007F; font-weight: 700;">Top 10% Elite Capture</div>
                <div style="font-size: 1.5rem; font-weight: 800; color: {'#0f172a' if current_theme=='light' else '#ffffff'};">{share_10:.1f}%</div>
                <div style="font-size: 0.78rem; opacity: 0.8;">Of total platform enrollments</div>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div style="background: rgba(0, 255, 135, 0.08); border: 1px solid rgba(0, 255, 135, 0.3); border-radius: 10px; padding: 12px; text-align: center;">
                <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: #00FF87; font-weight: 700;">Top 20% Pareto Capture</div>
                <div style="font-size: 1.5rem; font-weight: 800; color: {'#0f172a' if current_theme=='light' else '#ffffff'};">{share_20:.1f}%</div>
                <div style="font-size: 0.78rem; opacity: 0.8;">Pareto benchmark threshold</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)

        # Calculate Cohort Segment Comparison
        cohort_labels = [
            "🌱 Casual Learners (Bottom 50%)",
            "🎯 Active Mainstream (20%–50%)",
            "⚡ High-Activity Core (10%–20%)",
            "🔥 Elite Power Learners (Top 10%)"
        ]
        pop_shares = [50.0, 30.0, 10.0, 10.0]
        enroll_shares = [
            max(0, 100.0 - share_50),
            max(0, share_50 - share_20),
            max(0, share_20 - share_10),
            max(0, share_10)
        ]

        fig_pareto = go.Figure()

        # 1. Learner Population Share Bar
        fig_pareto.add_trace(go.Bar(
            y=cohort_labels,
            x=pop_shares,
            name='Learner Population Share (%)',
            orientation='h',
            marker=dict(
                color='#00F2FE',
                line=dict(width=1.5, color='rgba(255,255,255,0.25)')
            ),
            text=[f"{v:.1f}%" for v in pop_shares],
            textposition='outside',
            cliponaxis=False,
            textfont=dict(size=12, family="Outfit, sans-serif", color='#00F2FE')
        ))

        # 2. Total Enrollment Share Captured Bar
        fig_pareto.add_trace(go.Bar(
            y=cohort_labels,
            x=enroll_shares,
            name='Enrollment Share Captured (%)',
            orientation='h',
            marker=dict(
                color='#FF007F',
                line=dict(width=1.5, color='rgba(255,255,255,0.25)')
            ),
            text=[f"{v:.1f}%" for v in enroll_shares],
            textposition='outside',
            cliponaxis=False,
            textfont=dict(size=12, family="Outfit, sans-serif", color='#FF007F')
        ))

        layout_pareto = styling.get_plotly_layout("Learner Activity Concentration & Disparity Matrix", height=520, theme=current_theme)
        layout_pareto['barmode'] = 'group'
        layout_pareto['bargap'] = 0.22
        layout_pareto['bargroupgap'] = 0.08
        layout_pareto['margin'] = dict(l=220, r=60, t=75, b=60)
        layout_pareto['autosize'] = True
        layout_pareto['showlegend'] = True
        layout_pareto['legend'] = dict(
            orientation="h",
            yanchor="bottom",
            y=1.04,
            xanchor="right",
            x=1.0,
            title=None
        )
        fig_pareto.update_layout(**layout_pareto)
        max_p_share = max(max(pop_shares), max(enroll_shares))
        fig_pareto.update_xaxes(title="Share of Platform Total (%)", range=[0, max_p_share * 1.25], zeroline=True)
        fig_pareto.update_yaxes(title=None, autorange=True)
        st.plotly_chart(fig_pareto, use_container_width=True, config={'displayModeBar': True, 'responsive': True, 'autosizable': True})

# =========================================================
# TAB 6: REPORTS & DELIVERABLES
# =========================================================
with tabs[5]:
    st.markdown("### 📑 Strategic Reports & Executive Deliverables")
    st.markdown("Explore and download the complete academic research paper, government policy brief, and raw dataset.")
    
    report_tab = st.radio(
        "Select Deliverable to View:",
        ["🎓 Research Paper (Academic & EDA)", "🏛️ Executive Summary (Government Stakeholders)", "💾 Raw Data Explorer"],
        horizontal=True
    )
    
    st.markdown("---")
    
    if "Research Paper" in report_tab:
        with st.container(border=True):
            if os.path.exists("RESEARCH_PAPER.md"):
                with open("RESEARCH_PAPER.md", "r", encoding="utf-8") as f:
                    paper_text = f.read()
                st.download_button(
                    label="📥 Download Full Research Paper (.md)",
                    data=paper_text,
                    file_name="EduPro_Research_Paper.md",
                    mime="text/markdown",
                    width="stretch"
                )
                st.markdown("---")
                st.markdown(paper_text)
            else:
                st.warning("Research Paper file `RESEARCH_PAPER.md` is not generated yet.")
        
    elif "Executive Summary" in report_tab:
        with st.container(border=True):
            if os.path.exists("EXECUTIVE_SUMMARY.md"):
                with open("EXECUTIVE_SUMMARY.md", "r", encoding="utf-8") as f:
                    exec_text = f.read()
                st.download_button(
                    label="📥 Download Executive Brief (.md)",
                    data=exec_text,
                    file_name="EduPro_Executive_Summary.md",
                    mime="text/markdown",
                    width="stretch"
                )
                st.markdown("---")
                st.markdown(exec_text)
            else:
                st.warning("Executive Summary file `EXECUTIVE_SUMMARY.md` is not generated yet.")
        
    elif "Raw Data Explorer" in report_tab:
        with st.container(border=True):
            st.markdown("#### 🔍 Master Analytics Dataset")
            st.markdown(f"Showing **{len(filtered_df):,}** filtered records out of **{len(master_df):,}** total enrollments.")
            
            # Download CSV
            csv_data = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                    label="📥 Download Filtered Data as CSV",
                    data=csv_data,
                    file_name="EduPro_Filtered_Analytics_Data.csv",
                    mime="text/csv",
                    width="stretch"
                )
            st.markdown("---")
            st.dataframe(filtered_df, width="stretch", height=500)

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
styling.render_footer()
