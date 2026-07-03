import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import plotly.express as px

# Curated High-Vibrancy Neon / Cyber Palette for maximum visual attraction
COLOR_PALETTE = [
    '#00F2FE',  # Electric Cyber Cyan
    '#FF0844',  # Luminous Neon Red/Pink
    '#00FF87',  # Vivid Mint Emerald
    '#FFB199',  # Warm Peach Coral
    '#7F00FF',  # Electric Amethyst Purple
    '#F857A6',  # Bright Magenta
    '#4FACFE',  # Sky Blue Glow
    '#FEE140',  # Vibrant Gold Amber
    '#00CDAC',  # Turquoise Mint
    '#FF007F'   # Hot Neon Pink
]

GENDER_COLORS = {
    'Female': '#FF007F', # Hot Neon Pink
    'Male': '#00F2FE',   # Cyber Cyan
    'Other': '#00FF87'   # Vivid Mint
}

AGE_COLORS = {
    '<18': '#00FF87',    # Mint
    '18-25': '#00F2FE',  # Cyan
    '26-35': '#7F00FF',  # Amethyst Purple
    '36-45': '#FF007F',  # Hot Pink
    '45+': '#FFB199'     # Coral Peach
}

LEVEL_COLORS = {
    'Beginner': '#00FF87',   # Vivid Mint
    'Intermediate': '#00F2FE', # Cyber Cyan
    'Advanced': '#FF0844'    # Neon Red
}

TYPE_COLORS = {
    'Free': '#00FF87',   # Vivid Mint
    'Paid': '#7F00FF'    # Electric Purple
}

def inject_custom_css():
    """
    Injects ultra-modern, hyper-vibrant CSS into Streamlit for a luminous dark-hybrid UI with
    glassmorphism, rainbow borders, glowing KPI cards, animated multi-gradient backgrounds, and smooth transitions.
    """
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

        /* Keyframe Animations */
        @keyframes fadeInSlideUp {
            0% { opacity: 0; transform: translateY(25px) scale(0.98); }
            100% { opacity: 1; transform: translateY(0) scale(1); }
        }

        @keyframes pulseGlow {
            0%, 100% { box-shadow: 0 4px 20px rgba(0, 242, 254, 0.25), 0 0 10px rgba(255, 0, 127, 0.15); }
            50% { box-shadow: 0 8px 35px rgba(255, 0, 127, 0.55), 0 0 25px rgba(0, 242, 254, 0.45); }
        }

        @keyframes gradientMove {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        @keyframes bgShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        @keyframes floatUpDown {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-8px); }
        }

        @keyframes borderShimmer {
            0% { border-color: rgba(0, 242, 254, 0.4); }
            50% { border-color: rgba(255, 0, 127, 0.8); }
            100% { border-color: rgba(0, 242, 254, 0.4); }
        }

        @keyframes textShimmer {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Root styling - Vibrant Aurora Grid & Multi-Gradient Dark Hybrid Theme */
        html {
            scroll-behavior: smooth !important;
        }

        html, body, [class*="css"], .stApp {
            font-family: 'Inter', sans-serif;
            background-image: 
                linear-gradient(to right, rgba(255, 255, 255, 0.035) 1px, transparent 1px),
                linear-gradient(to bottom, rgba(255, 255, 255, 0.035) 1px, transparent 1px),
                linear-gradient(-45deg, #0f172a, #1e1b4b, #2a0845, #0f172a) !important;
            background-size: 45px 45px, 45px 45px, 400% 400% !important;
            animation: bgShift 20s ease infinite !important;
            color: #f8fafc !important;
            overflow-x: hidden !important;
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
            color: #ffffff !important;
        }

        /* App container */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 3.5rem !important;
            max-width: 1400px !important;
            animation: fadeInSlideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }

        /* Custom Header Title - Electric Luminous Multi-Color Shimmer */
        .main-title {
            background: linear-gradient(270deg, #00f2fe, #ff007f, #00ff87, #7f00ff, #00f2fe);
            background-size: 300% 300%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 0.4rem;
            font-family: 'Outfit', sans-serif;
            animation: textShimmer 5s ease infinite;
            text-shadow: 0 0 35px rgba(0, 242, 254, 0.35);
        }

        .sub-title {
            color: #e2e8f0;
            font-size: 1.2rem;
            margin-bottom: 2.2rem;
            font-weight: 400;
            letter-spacing: 0.01em;
        }

        /* Glassmorphism Card Container - Vibrant Contrast */
        .glass-card {
            background: rgba(30, 41, 59, 0.65);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            border: 1px solid rgba(255, 255, 255, 0.18);
            border-radius: 18px;
            padding: 1.6rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 10px 30px 0 rgba(0, 0, 0, 0.3);
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            animation: fadeInSlideUp 0.5s ease forwards;
        }

        .glass-card:hover {
            transform: translateY(-8px) scale(1.02) perspective(1000px) rotateX(1.5deg) !important;
            border-color: #00f2fe !important;
            box-shadow: 0 20px 45px rgba(0, 242, 254, 0.35), 0 0 30px rgba(255, 0, 127, 0.25) !important;
            animation: borderShimmer 3s infinite alternate !important;
        }

        /* Streamlit Native Containers styled as Vibrant Glass Cards */
        [data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(30, 41, 59, 0.65) !important;
            backdrop-filter: blur(18px) !important;
            border: 1px solid rgba(255, 255, 255, 0.16) !important;
            border-radius: 18px !important;
            padding: 1.1rem !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25) !important;
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
            animation: fadeInSlideUp 0.6s ease forwards;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:hover {
            transform: translateY(-8px) scale(1.015) perspective(1000px) rotateX(1deg) !important;
            border-color: #00f2fe !important;
            box-shadow: 0 20px 45px rgba(0, 242, 254, 0.35), 0 0 35px rgba(127, 0, 255, 0.3) !important;
            animation: borderShimmer 3s infinite alternate !important;
        }

        /* Staggered Card Reveals on Scroll / Load */
        [data-testid="stVerticalBlockBorderWrapper"]:nth-child(1) { animation-delay: 0.05s; }
        [data-testid="stVerticalBlockBorderWrapper"]:nth-child(2) { animation-delay: 0.1s; }
        [data-testid="stVerticalBlockBorderWrapper"]:nth-child(3) { animation-delay: 0.15s; }
        [data-testid="stVerticalBlockBorderWrapper"]:nth-child(4) { animation-delay: 0.2s; }

        /* Vibrant KPI Metric Cards */
        .kpi-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(42, 8, 69, 0.85) 100%);
            border-radius: 18px;
            padding: 1.4rem;
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.18);
            border-left: 5px solid #00F2FE;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            animation: fadeInSlideUp 0.5s ease forwards;
        }

        .kpi-card:hover {
            transform: translateY(-10px) scale(1.035) perspective(1000px) rotateX(2deg) !important;
            border-left: 5px solid #FF007F !important;
            border-color: rgba(255, 0, 127, 0.8) !important;
            box-shadow: 0 22px 45px rgba(255, 0, 127, 0.45), 0 0 30px rgba(0, 242, 254, 0.35) !important;
        }

        .kpi-icon {
            font-size: 2.6rem;
            position: absolute;
            right: 1.25rem;
            top: 1.25rem;
            opacity: 0.95;
            transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
            animation: floatUpDown 4s ease-in-out infinite;
        }

        .kpi-card:hover .kpi-icon {
            transform: scale(1.25) rotate(12deg);
        }

        .kpi-title {
            color: #e2e8f0;
            font-size: 0.88rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 0.5rem;
        }

        .kpi-value {
            background: linear-gradient(90deg, #ffffff, #00f2fe, #ff007f);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.4rem;
            font-weight: 800;
            font-family: 'Outfit', sans-serif;
            margin-bottom: 0.3rem;
            animation: gradientMove 5s ease infinite;
        }

        .kpi-subtitle {
            color: #00ff87;
            font-size: 0.9rem;
            font-weight: 600;
            letter-spacing: 0.02em;
        }

        /* Streamlit Tabs - Vibrant Neon Customization */
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
            background-color: rgba(15, 23, 42, 0.8);
            padding: 10px;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }

        .stTabs [data-baseweb="tab"] {
            height: 46px;
            white-space: pre-wrap;
            background-color: transparent;
            border-radius: 12px;
            color: #cbd5e1;
            font-weight: 600;
            padding: 0 22px;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .stTabs [data-baseweb="tab"]:hover {
            color: #ffffff;
            background-color: rgba(255, 255, 255, 0.08);
            transform: translateY(-2px);
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #FF007F 0%, #7F00FF 50%, #00F2FE 100%) !important;
            background-size: 200% 200% !important;
            animation: gradientMove 4s ease infinite !important;
            color: #ffffff !important;
            border: 1px solid rgba(0, 242, 254, 0.8) !important;
            font-weight: 700 !important;
            box-shadow: 0 6px 25px rgba(255, 0, 127, 0.45), 0 0 15px rgba(0, 242, 254, 0.3) !important;
            transform: scale(1.02);
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a 0%, #1e1b4b 100%) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.15);
        }

        /* Vibrant Animated Buttons (Neon Glow, Pulse, Ripple Click, Animated Gradient) */
        @keyframes buttonPulse {
            0% { box-shadow: 0 0 15px rgba(0, 242, 254, 0.4), 0 0 5px rgba(255, 0, 127, 0.3); }
            50% { box-shadow: 0 0 30px rgba(255, 0, 127, 0.7), 0 0 18px rgba(0, 255, 135, 0.5); }
            100% { box-shadow: 0 0 15px rgba(0, 242, 254, 0.4), 0 0 5px rgba(255, 0, 127, 0.3); }
        }

        .stButton > button, .stDownloadButton > button, [data-testid="stBaseButton-secondary"] {
            background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 30%, #7F00FF 60%, #FF007F 100%) !important;
            background-size: 300% 300% !important;
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 14px !important;
            padding: 0.65rem 1.5rem !important;
            font-weight: 700 !important;
            transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1) !important;
            animation: gradientMove 4s ease infinite, buttonPulse 3s infinite !important;
            letter-spacing: 0.03em !important;
            cursor: pointer !important;
        }

        .stButton > button:hover, .stDownloadButton > button:hover, [data-testid="stBaseButton-secondary"]:hover {
            transform: translateY(-4px) scale(1.05) !important;
            box-shadow: 0 15px 35px rgba(255, 0, 127, 0.6), 0 0 30px rgba(0, 242, 254, 0.5) !important;
            border-color: #00ff87 !important;
        }

        .stButton > button:active, .stDownloadButton > button:active {
            transform: translateY(-1px) scale(0.98) !important;
        }

        /* Dashboard Effects: Animated KPI Metric Values & Dataframes */
        [data-testid="stMetricValue"] {
            background: linear-gradient(90deg, #ffffff, #00f2fe, #ff007f);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800 !important;
            font-family: 'Outfit', sans-serif !important;
            animation: gradientMove 5s ease infinite !important;
        }

        [data-testid="stDataFrame"] {
            background-color: rgba(30, 41, 59, 0.7);
            border-radius: 16px;
            border: 1px solid rgba(0, 242, 254, 0.25);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
            transition: all 0.4s ease;
        }

        [data-testid="stDataFrame"]:hover {
            border-color: #ff007f;
            box-shadow: 0 15px 35px rgba(255, 0, 127, 0.25), 0 0 20px rgba(0, 242, 254, 0.2);
            transform: translateY(-4px);
        }
    </style>
    """, unsafe_allow_html=True)

def inject_cursor_bubble():
    """
    Injects 4 vibrant background animated glowing CSS spheres and an interactive JavaScript cursor bubble
    that smoothly follows mouse movements across the Streamlit app with electric neon colors.
    """
    # 1. Inject CSS for 4 vibrant ambient floating spheres
    st.markdown("""
    <style>
        @keyframes floatOrb1 {
            0%, 100% { transform: translate(0, 0) scale(1); }
            33% { transform: translate(150px, -100px) scale(1.2); }
            66% { transform: translate(-100px, 150px) scale(0.85); }
        }

        @keyframes floatOrb2 {
            0%, 100% { transform: translate(0, 0) scale(1); }
            33% { transform: translate(-150px, 150px) scale(0.9); }
            66% { transform: translate(120px, -120px) scale(1.15); }
        }

        @keyframes floatOrb3 {
            0%, 100% { transform: translate(0, 0) scale(1); }
            50% { transform: translate(130px, 130px) scale(1.1); }
        }

        @keyframes floatOrb4 {
            0%, 100% { transform: translate(0, 0) scale(1); }
            50% { transform: translate(-140px, -140px) scale(0.95); }
        }

        .stApp::before {
            content: "";
            position: fixed;
            top: 5%;
            left: 5%;
            width: 480px;
            height: 480px;
            background: radial-gradient(circle, rgba(0, 242, 254, 0.22) 0%, rgba(127, 0, 255, 0.08) 50%, transparent 70%);
            border-radius: 50%;
            filter: blur(40px);
            z-index: 0;
            pointer-events: none;
            animation: floatOrb1 20s ease-in-out infinite;
        }

        .stApp::after {
            content: "";
            position: fixed;
            bottom: 5%;
            right: 5%;
            width: 520px;
            height: 520px;
            background: radial-gradient(circle, rgba(255, 0, 127, 0.22) 0%, rgba(0, 255, 135, 0.08) 50%, transparent 70%);
            border-radius: 50%;
            filter: blur(45px);
            z-index: 0;
            pointer-events: none;
            animation: floatOrb2 24s ease-in-out infinite;
        }

        /* Additional Ambient Neon Orbs */
        .ambient-orb-3 {
            position: fixed;
            top: 60%;
            left: 10%;
            width: 400px;
            height: 400px;
            background: radial-gradient(circle, rgba(0, 255, 135, 0.16) 0%, rgba(0, 205, 172, 0.05) 50%, transparent 70%);
            border-radius: 50%;
            filter: blur(50px);
            z-index: 0;
            pointer-events: none;
            animation: floatOrb3 22s ease-in-out infinite;
        }

        .ambient-orb-4 {
            position: fixed;
            top: 15%;
            right: 15%;
            width: 450px;
            height: 450px;
            background: radial-gradient(circle, rgba(127, 0, 255, 0.18) 0%, rgba(248, 87, 166, 0.06) 50%, transparent 70%);
            border-radius: 50%;
            filter: blur(45px);
            z-index: 0;
            pointer-events: none;
            animation: floatOrb4 26s ease-in-out infinite;
        }
    </style>
    <div class="ambient-orb-3"></div>
    <div class="ambient-orb-4"></div>
    """, unsafe_allow_html=True)

    # 2. Inject JS for ultra-vibrant interactive cursor bubble & Top Scroll Progress Bar
    js_code = """
    <script>
    const parentDoc = window.parent.document;
    
    // 1. Interactive Cursor Tracking Bubble with Ripple & Glow
    if (!parentDoc.getElementById('cursor-glow-bubble')) {
        const bubble = parentDoc.createElement('div');
        bubble.id = 'cursor-glow-bubble';
        bubble.style.cssText = `
            position: fixed;
            width: 380px;
            height: 380px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(0, 242, 254, 0.25) 0%, rgba(255, 0, 127, 0.18) 45%, rgba(0, 0, 0, 0) 70%);
            pointer-events: none;
            z-index: 99999;
            transform: translate(-50%, -50%);
            transition: left 0.08s ease-out, top 0.08s ease-out, transform 0.35s cubic-bezier(0.16, 1, 0.3, 1), background 0.3s ease;
            filter: blur(22px);
            opacity: 0.95;
            left: 50%;
            top: 50%;
        `;
        parentDoc.body.appendChild(bubble);
        
        parentDoc.addEventListener('mousemove', (e) => {
            bubble.style.left = e.clientX + 'px';
            bubble.style.top = e.clientY + 'px';
        });

        parentDoc.addEventListener('mousedown', () => {
            bubble.style.transform = 'translate(-50%, -50%) scale(1.35)';
            bubble.style.background = 'radial-gradient(circle, rgba(255, 0, 127, 0.45) 0%, rgba(0, 255, 135, 0.35) 45%, rgba(0, 0, 0, 0) 70%)';
        });

        parentDoc.addEventListener('mouseup', () => {
            bubble.style.transform = 'translate(-50%, -50%) scale(1)';
            bubble.style.background = 'radial-gradient(circle, rgba(0, 242, 254, 0.25) 0%, rgba(255, 0, 127, 0.18) 45%, rgba(0, 0, 0, 0) 70%)';
        });
    }

    // 2. Scroll-Triggered Progress Bar (Glowing Top Progress Bar)
    if (!parentDoc.getElementById('scroll-progress-indicator')) {
        const progressBar = parentDoc.createElement('div');
        progressBar.id = 'scroll-progress-indicator';
        progressBar.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            height: 4px;
            width: 0%;
            background: linear-gradient(90deg, #00F2FE, #00FF87, #7F00FF, #FF007F, #00F2FE);
            background-size: 300% 100%;
            z-index: 999999;
            transition: width 0.1s ease-out;
            box-shadow: 0 0 15px #00F2FE, 0 0 25px #FF007F;
        `;
        parentDoc.body.appendChild(progressBar);
        
        parentDoc.addEventListener('scroll', () => {
            const scrollTop = parentDoc.documentElement.scrollTop || parentDoc.body.scrollTop;
            const scrollHeight = (parentDoc.documentElement.scrollHeight || parentDoc.body.scrollHeight) - parentDoc.documentElement.clientHeight;
            const progress = scrollHeight > 0 ? (scrollTop / scrollHeight) * 100 : 0;
            progressBar.style.width = progress + '%';
        }, { passive: true });
    }
    </script>
    """
    components.html(js_code, height=0, width=0)

def render_header(title, subtitle=""):
    """
    Renders an electric modern header for the Streamlit app.
    """
    st.markdown(f'<div class="main-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="sub-title">{subtitle}</div>', unsafe_allow_html=True)

def render_kpi_card(title, value, subtitle="", icon="📊"):
    """
    Renders an HTML/CSS styled KPI card with vibrant neon hover glow animation.
    """
    html = f"""
    <div class="kpi-card">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-subtitle">{subtitle}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_footer():
    """
    Renders the custom animated GitHub footer requested by the user.
    """
    footer_html = """
    <div style="margin-top: 4.5rem; padding-top: 2rem; border-top: 1px solid rgba(255, 255, 255, 0.15); text-align: center; font-family: 'Inter', sans-serif; animation: fadeInSlideUp 0.8s ease;">
        <p style="color: #f1f5f9; font-size: 1.15rem; font-weight: 600; margin-bottom: 0.4rem; letter-spacing: 0.02em;">
            Made with ❤️ by <a href="https://github.com/Sahil-476" target="_blank" style="color: #00F2FE; text-decoration: none; font-weight: 800; border-bottom: 2px solid #FF007F; padding-bottom: 2px; transition: all 0.3s ease; text-shadow: 0 0 15px rgba(0, 242, 254, 0.4);">Sahil</a>
        </p>
        <p style="color: #94a3b8; font-size: 0.95rem; margin-top: 0; font-weight: 500;">
            © 2026 Sahil. All rights reserved.
        </p>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

def get_plotly_layout(title="", height=420, show_legend=True, barmode=None):
    """
    Returns a unified, ultra-vibrant neon theme layout for Plotly charts.
    """
    layout = dict(
        title=dict(
            text=f"<b>{title}</b>" if title else "",
            font=dict(size=17, color='#ffffff', family="Outfit, sans-serif"),
            x=0.02,
            y=0.95
        ),
        height=height,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#cbd5e1', family="Inter, sans-serif"),
        margin=dict(l=60, r=30, t=55, b=95),
        showlegend=show_legend,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.18,
            xanchor="center",
            x=0.5,
            font=dict(size=12, color='#f8fafc')
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.08)',
            zerolinecolor='rgba(0, 242, 254, 0.25)',
            tickfont=dict(color='#cbd5e1')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.08)',
            zerolinecolor='rgba(0, 242, 254, 0.25)',
            tickfont=dict(color='#cbd5e1')
        ),
        hoverlabel=dict(
            bgcolor='#0f172a',
            bordercolor='#00f2fe',
            font_size=13,
            font_family="Inter, sans-serif"
        )
    )
    if barmode:
        layout['barmode'] = barmode
    return layout

