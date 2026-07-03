import os
import pandas as pd
import numpy as np
import streamlit as st

AGE_BANDS_ORDER = ['<18', '18-25', '26-35', '36-45', '45+']
COURSE_LEVELS_ORDER = ['Beginner', 'Intermediate', 'Advanced']

def get_age_band(age):
    if pd.isna(age):
        return 'Unknown'
    age = int(age)
    if age < 18:
        return '<18'
    elif age <= 25:
        return '18-25'
    elif age <= 35:
        return '26-35'
    elif age <= 45:
        return '36-45'
    else:
        return '45+'

@st.cache_data(show_spinner=False)
def load_and_process_data(filepath="EduPro Online Platform (1).xlsx"):
    """
    Loads raw datasets from Excel sheets, performs referential integrity checks,
    merges into a master analytics dataframe, and creates demographic features.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset file not found at path: {filepath}")
    
    excel_file = pd.ExcelFile(filepath)
    users_df = pd.read_excel(excel_file, sheet_name='Users')
    courses_df = pd.read_excel(excel_file, sheet_name='Courses')
    transactions_df = pd.read_excel(excel_file, sheet_name='Transactions')
    
    # Feature Engineering: Age Bands
    users_df['AgeBand'] = users_df['Age'].apply(get_age_band)
    users_df['AgeBand'] = pd.Categorical(users_df['AgeBand'], categories=AGE_BANDS_ORDER, ordered=True)
    
    # Ensure categorical ordering for courses
    courses_df['CourseLevel'] = pd.Categorical(courses_df['CourseLevel'], categories=COURSE_LEVELS_ORDER, ordered=True)
    
    # Referential Integrity & Merge
    master_df = transactions_df.merge(users_df, on='UserID', how='inner').merge(courses_df, on='CourseID', how='inner')
    
    # Convert TransactionDate to datetime if possible
    if 'TransactionDate' in master_df.columns:
        master_df['TransactionDate'] = pd.to_datetime(master_df['TransactionDate'], errors='coerce')
        master_df['MonthYear'] = master_df['TransactionDate'].dt.to_period('M').astype(str)
    
    # Compute user-level aggregates
    user_course_counts = master_df.groupby('UserID').size().reset_index(name='CoursesTaken')
    users_df = users_df.merge(user_course_counts, on='UserID', how='left')
    users_df['CoursesTaken'] = users_df['CoursesTaken'].fillna(0).astype(int)
    
    # User engagement tier
    def get_engagement_tier(count):
        if count == 0:
            return 'Inactive (0)'
        elif count <= 2:
            return 'Casual (1-2)'
        elif count <= 4:
            return 'Active (3-4)'
        else:
            return 'Power Learner (5+)'
    
    users_df['EngagementTier'] = users_df['CoursesTaken'].apply(get_engagement_tier)
    
    return master_df, users_df, courses_df

def compute_kpis(master_df, users_df, courses_df):
    """
    Calculates the 5 Core KPIs required by the analytical guide, plus additional
    engagement and platform health metrics.
    """
    total_enrollments = len(master_df)
    total_users = len(users_df)
    active_users = master_df['UserID'].nunique()
    avg_courses_per_learner = total_enrollments / active_users if active_users > 0 else 0
    total_courses_offered = len(courses_df)
    
    # 1. Scale Total Enrollments
    scale_kpi = {
        'Total Enrollments': total_enrollments,
        'Active Learners': active_users,
        'Total Registered Users': total_users,
        'Avg Courses per Active Learner': round(avg_courses_per_learner, 2),
        'Course Catalog Size': total_courses_offered
    }
    
    # 2. Enrollments by Age Group (Demographic Reach)
    age_enrollments = master_df['AgeBand'].value_counts().reindex(AGE_BANDS_ORDER, fill_value=0)
    age_users = users_df['AgeBand'].value_counts().reindex(AGE_BANDS_ORDER, fill_value=0)
    age_kpi = pd.DataFrame({
        'Enrollments': age_enrollments,
        'Enrollment Share (%)': round(age_enrollments / total_enrollments * 100, 2) if total_enrollments > 0 else 0,
        'Registered Users': age_users,
        'User Share (%)': round(age_users / total_users * 100, 2) if total_users > 0 else 0
    }).reset_index().rename(columns={'index': 'AgeBand'})
    
    # 3. Gender Participation Ratio (Inclusivity Metric)
    gender_enrollments = master_df['Gender'].value_counts()
    gender_users = users_df['Gender'].value_counts()
    gender_kpi = pd.DataFrame({
        'Enrollments': gender_enrollments,
        'Enrollment Share (%)': round(gender_enrollments / total_enrollments * 100, 2) if total_enrollments > 0 else 0,
        'Registered Users': gender_users,
        'User Share (%)': round(gender_users / total_users * 100, 2) if total_users > 0 else 0
    }).reset_index().rename(columns={'index': 'Gender'})
    
    # 4. Category Popularity Index (Course Demand)
    cat_enrollments = master_df['CourseCategory'].value_counts()
    cat_kpi = pd.DataFrame({
        'Enrollments': cat_enrollments,
        'Popularity Share (%)': round(cat_enrollments / total_enrollments * 100, 2) if total_enrollments > 0 else 0
    }).reset_index().rename(columns={'index': 'CourseCategory'}).sort_values('Enrollments', ascending=False)
    cat_kpi['Rank'] = range(1, len(cat_kpi) + 1)
    
    # 5. Level Preference Distribution (Skill Maturity Insight)
    level_enrollments = master_df['CourseLevel'].value_counts().reindex(COURSE_LEVELS_ORDER, fill_value=0)
    level_kpi = pd.DataFrame({
        'Enrollments': level_enrollments,
        'Preference Share (%)': round(level_enrollments / total_enrollments * 100, 2) if total_enrollments > 0 else 0
    }).reset_index().rename(columns={'index': 'CourseLevel'})
    
    return {
        'scale': scale_kpi,
        'age_group': age_kpi,
        'gender': gender_kpi,
        'category_popularity': cat_kpi,
        'level_preference': level_kpi
    }

def filter_dataframe(master_df, age_bands=None, genders=None, categories=None, levels=None, types=None):
    """
    Applies multi-dimensional user filters to the master dataset.
    """
    df = master_df.copy()
    if age_bands and len(age_bands) > 0:
        df = df[df['AgeBand'].isin(age_bands)]
    if genders and len(genders) > 0:
        df = df[df['Gender'].isin(genders)]
    if categories and len(categories) > 0:
        df = df[df['CourseCategory'].isin(categories)]
    if levels and len(levels) > 0:
        df = df[df['CourseLevel'].isin(levels)]
    if types and len(types) > 0:
        df = df[df['CourseType'].isin(types)]
    return df
