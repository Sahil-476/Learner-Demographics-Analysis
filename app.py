import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

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

# Inject custom CSS for WOW aesthetics and cursor bubble animations
styling.inject_custom_css()
styling.inject_cursor_bubble()

# Load Data
@st.cache_data(show_spinner=False)
def get_data():
    return data_loader.load_and_process_data("EduPro Online Platform (1).xlsx")

try:
    master_df, users_df, courses_df = get_data()
except Exception as e:
    st.error(f"Failed to load dataset: {e}")
    st.stop()

# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------
st.sidebar.markdown('### 🎓 EduPro Analytics')
st.sidebar.markdown('<p style="color: #cbd5e1; font-size: 0.88rem; margin-top: -10px;">Foundational Learner Intelligence</p>', unsafe_allow_html=True)
st.sidebar.markdown("---")

st.sidebar.markdown("#### 🔍 Interactive Filters")

# Filter Reset
if st.sidebar.button("↻ Reset All Filters", width="stretch"):
    for key in ['f_age', 'f_gender', 'f_cat', 'f_level', 'f_type']:
        if key in st.session_state:
            del st.session_state[key]
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
<div style="background: rgba(30,41,59,0.7); padding: 12px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.15); font-size: 0.88rem; color: #e2e8f0;">
  <b>Total Enrollments:</b> {len(filtered_df):,} / {len(master_df):,}<br>
  <b>Active Learners:</b> {filtered_df['UserID'].nunique():,} / {master_df['UserID'].nunique():,}<br>
  <b>Catalog Coverage:</b> {filtered_df['CourseID'].nunique()} / {len(courses_df)} courses
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="text-align: center; font-size: 0.85rem; color: #cbd5e1; padding-top: 5px; line-height: 1.5;">
    Made with ❤️ by <a href="https://github.com/Sahil-476" target="_blank" style="color: #818cf8; text-decoration: none; font-weight: 700;">Sahil</a><br>
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
            fig_age_donut.update_layout(**styling.get_plotly_layout("Enrollments by Age Group (Demographic Reach)", height=360))
            fig_age_donut.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_age_donut, width="stretch")
        
    with col_chart2:
        with st.container(border=True):
            # Top 6 Categories Bar Chart
            top_6_cats = kpis['category_popularity'].head(6)
            fig_top_cats = px.bar(
                top_6_cats,
                x='Enrollments',
                y='CourseCategory',
                orientation='h',
                color='Enrollments',
                color_continuous_scale=['#00F2FE', '#FF0844', '#FEE140']
            )
            fig_top_cats.update_layout(**styling.get_plotly_layout("Top 6 Course Categories (Demand Index)", height=360, show_legend=False))
            fig_top_cats.update_yaxes(autorange="reversed")
            st.plotly_chart(fig_top_cats, width="stretch")

    st.markdown("""
    <div class="glass-card" style="border-left: 4px solid #10b981;">
        <h4 style="color: #34d399; margin-top: 0;">💡 Key Strategic Briefing</h4>
        <p style="color: #e2e8f0; line-height: 1.6;">
            <b>1. Demographic Reach:</b> Platform participation is heavily concentrated among young adults and professionals aged <b>18–35</b>, accounting for over <b>85%</b> of total enrollments. The <b>26–35</b> age band leads with <b>48.0%</b> share, followed by <b>18–25</b> at <b>37.3%</b>.<br>
            <b>2. Gender Inclusivity:</b> EduPro demonstrates exceptional gender balance, with <b>Female learners representing 50.8%</b> of enrollments and <b>Male learners representing 49.2%</b>. This 1:1 participation ratio indicates high accessibility across genders.<br>
            <b>3. Demand Distribution:</b> Course category preferences are evenly distributed across 12 high-tech and business domains, indicating a balanced demand for multi-disciplinary professional upskilling.
        </p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# TAB 2: LEARNER DEMOGRAPHICS MODULE
# =========================================================
with tabs[1]:
    st.markdown("### 👥 Comprehensive Learner Demographic Profiling")
    
    col_d1, col_d2 = st.columns([1, 1])
    
    with col_d1:
        with st.container(border=True):
            # Age Distribution: Users vs Enrollments
            fig_age_comp = go.Figure()
            fig_age_comp.add_trace(go.Bar(
                x=kpis['age_group']['AgeBand'],
                y=kpis['age_group']['User Share (%)'],
                name='Registered Users Share (%)',
                marker_color='#00F2FE'
            ))
            fig_age_comp.add_trace(go.Bar(
                x=kpis['age_group']['AgeBand'],
                y=kpis['age_group']['Enrollment Share (%)'],
                name='Course Enrollment Share (%)',
                marker_color='#FF0844'
            ))
            fig_age_comp.update_layout(**styling.get_plotly_layout("Age Bands: Registered Users vs. Course Enrollments (%)", height=380, barmode='group'))
            st.plotly_chart(fig_age_comp, width="stretch")
        
    with col_d2:
        with st.container(border=True):
            # Gender Distribution across Age Bands
            gender_age_df = filtered_df.groupby(['AgeBand', 'Gender']).size().reset_index(name='Enrollments')
            fig_gender_age = px.bar(
                gender_age_df,
                x='AgeBand',
                y='Enrollments',
                color='Gender',
                barmode='stack',
                labels=dict(AgeBand='Age Group', Enrollments='Learner Enrollments', Gender='Gender'),
                color_discrete_map=styling.GENDER_COLORS
            )
            fig_gender_age.update_layout(**styling.get_plotly_layout("Gender Distribution Across Age Bands", height=400))
            st.plotly_chart(fig_gender_age, width="stretch")
        
    col_d3, col_d4 = st.columns([1, 1])
    with col_d3:
        with st.container(border=True):
            # Histogram of exact ages
            fig_age_hist = px.histogram(
                filtered_users_df,
                x='Age',
                nbins=21,
                color_discrete_sequence=['#00FF87'],
                title="Granular Age Distribution of Registered Learners"
            )
            fig_age_hist.update_layout(**styling.get_plotly_layout("Granular Age Distribution of Registered Learners", height=360, show_legend=False))
            st.plotly_chart(fig_age_hist, width="stretch")
        
    with col_d4:
        with st.container(border=True):
            # Participation levels per demographic group table
            st.markdown("#### 📋 Demographic Group Metrics Table")
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
            }), width="stretch", height=270)

# =========================================================
# TAB 3: COURSE DEMAND & POPULARITY
# =========================================================
with tabs[2]:
    st.markdown("### 📈 Course Category Popularity & Level Demand")
    
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
            fig_level_donut.update_layout(**styling.get_plotly_layout("Level Preference Distribution", height=360))
            fig_level_donut.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_level_donut, width="stretch")
        
    with col_p2:
        with st.container(border=True):
            # Course Type (Free vs Paid) by Level
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
            fig_type_level.update_layout(**styling.get_plotly_layout("Course Type (Free vs. Paid) by Level", height=360))
            st.plotly_chart(fig_type_level, width="stretch")

    # Bottom Row: Full-Width Course Category Popularity Index
    with st.container(border=True):
        # Full Category Popularity Index
        fig_full_cats = px.bar(
            kpis['category_popularity'],
            x='Enrollments',
            y='CourseCategory',
            orientation='h',
            color='Enrollments',
            color_continuous_scale=['#00FF87', '#00F2FE', '#7F00FF'],
            text='Popularity Share (%)',
            labels=dict(Enrollments="Total Enrollments", CourseCategory="Course Category")
        )
        fig_full_cats.update_traces(texttemplate='<b>%{text}%</b>', textposition='outside', cliponaxis=False)
        layout_cats = styling.get_plotly_layout("Course Category Popularity Index (All Domains)", height=520, show_legend=False)
        layout_cats['margin'] = dict(l=60, r=65, t=55, b=95)
        fig_full_cats.update_layout(**layout_cats)
        fig_full_cats.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_full_cats, width="stretch")

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
        fig_heatmap.update_layout(**styling.get_plotly_layout("Heatmap: Age Band vs. Course Category Preferences", height=450, show_legend=False))
        st.plotly_chart(fig_heatmap, width="stretch")
    
    col_dp1, col_dp2 = st.columns([1, 1])
    with col_dp1:
        with st.container(border=True):
            # Gender vs Course Level
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
            fig_gl.update_layout(**styling.get_plotly_layout("Gender Comparison Across Course Levels", height=400))
            st.plotly_chart(fig_gl, width="stretch")
        
    with col_dp2:
        with st.container(border=True):
            # Beginner vs Advanced Top Categories
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
            fig_ba.update_layout(**styling.get_plotly_layout("Beginner vs. Advanced Category Demand", height=400))
            fig_ba.update_yaxes(autorange="reversed")
            st.plotly_chart(fig_ba, width="stretch")

# =========================================================
# TAB 5: BEHAVIORAL & USER CONCENTRATION
# =========================================================
with tabs[4]:
    st.markdown("### 🧠 Learner Behavioral Patterns & Engagement Concentration")
    
    col_b1, col_b2 = st.columns([1, 1])
    with col_b1:
        with st.container(border=True):
            # Distribution of Courses Taken per Learner
            courses_dist = filtered_users_df['CoursesTaken'].value_counts().reset_index()
            courses_dist.columns = ['Courses Taken', 'Learner Count']
            courses_dist = courses_dist.sort_values('Courses Taken')
            
            fig_cd = px.bar(
                courses_dist,
                x='Courses Taken',
                y='Learner Count',
                color='Learner Count',
                color_continuous_scale=['#00F2FE', '#7F00FF', '#FF0844']
            )
            fig_cd.update_layout(**styling.get_plotly_layout("Distribution of Courses Taken per Learner", height=360, show_legend=False))
            st.plotly_chart(fig_cd, width="stretch")
        
    with col_b2:
        with st.container(border=True):
            # User Engagement Tiers Donut
            tier_counts = filtered_users_df['EngagementTier'].value_counts().reset_index()
            tier_counts.columns = ['Engagement Tier', 'Learner Count']
            
            fig_tiers = px.pie(
                tier_counts,
                names='Engagement Tier',
                values='Learner Count',
                hole=0.55,
                color_discrete_sequence=['#00F2FE', '#00FF87', '#FEE140', '#FF0844']
            )
            fig_tiers.update_layout(**styling.get_plotly_layout("Learner Engagement Segmentation", height=360))
            fig_tiers.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_tiers, width="stretch")

    with st.container(border=True):
        st.markdown("#### 📊 Pareto Enrollment Concentration Analysis")
        st.markdown("<p style='color: #cbd5e1; font-size: 0.9rem;'>Analyzing how platform course completions are distributed among registered learners.</p>", unsafe_allow_html=True)
        
        # Calculate Pareto Curve
        sorted_users = filtered_users_df.sort_values('CoursesTaken', ascending=False).reset_index(drop=True)
        sorted_users['User Rank (%)'] = (sorted_users.index + 1) / len(sorted_users) * 100
        sorted_users['Cumulative Enrollments'] = sorted_users['CoursesTaken'].cumsum()
        total_enr = sorted_users['CoursesTaken'].sum()
        sorted_users['Cumulative Share (%)'] = np.where(total_enr > 0, sorted_users['Cumulative Enrollments'] / total_enr * 100, 0)
        
        fig_pareto = go.Figure()
        fig_pareto.add_trace(go.Scatter(
            x=sorted_users['User Rank (%)'],
            y=sorted_users['Cumulative Share (%)'],
            mode='lines',
            name='Cumulative Enrollment Share (%)',
            line=dict(color='#FF0844', width=3)
        ))
        # Add reference diagonal line (equality line)
        fig_pareto.add_trace(go.Scatter(
            x=[0, 100],
            y=[0, 100],
            mode='lines',
            name='Equality Reference (Uniform Participation)',
            line=dict(color='#00F2FE', width=2, dash='dash')
        ))
        fig_pareto.update_layout(**styling.get_plotly_layout("Pareto Curve: Cumulative Learner % vs. Cumulative Enrollment Share %", height=400))
        fig_pareto.update_xaxes(title="Learner Population Rank (%)")
        fig_pareto.update_yaxes(title="Cumulative Share of Total Enrollments (%)")
        st.plotly_chart(fig_pareto, width="stretch")

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
