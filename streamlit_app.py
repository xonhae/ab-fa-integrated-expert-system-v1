import math
from datetime import datetime

import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(page_title="Wafer-Pro Defect Diagnosis", layout="wide")

st.markdown(
    """
    <style>
    :root {
        --bg: #191814;
        --panel: #22211d;
        --panel-2: #292722;
        --line: #3b3831;
        --text: #f7f0e6;
        --muted: #a49b8e;
        --orange: #f28a37;
        --red: #e76872;
        --purple: #a86ff4;
        --blue: #64b5ee;
        --green: #42b883;
        --yellow: #f3c74f;
    }
    .stApp { background: radial-gradient(circle at 15% 0%, #2a211b 0%, #191814 30%, #14130f 100%); color: var(--text); }
    header[data-testid="stHeader"] { display: none; }
    .block-container { padding-top: 0.6rem; max-width: 1800px; }
    [data-testid="stSidebar"] { background: #1f1e1a; border-right: 1px solid var(--line); }
    [data-testid="stSidebar"] * { color: var(--text); }
    h1, h2, h3, h4 { color: var(--text); }
    div[data-testid="stMetric"] {
        background: #27241f;
        border: 1px solid var(--line);
        border-radius: 10px;
        padding: 12px 14px;
    }
    div[data-testid="stMetric"] label { color: var(--muted); }
    .topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 0 18px;
        border-bottom: 1px solid var(--line);
        margin-bottom: 24px;
    }
    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 30px;
        font-weight: 800;
        color: var(--text);
    }
    .brand-badge {
        width: 42px;
        height: 42px;
        display: grid;
        place-items: center;
        border-radius: 10px;
        background: linear-gradient(135deg, #f28a37, #9c68f1);
        font-weight: 900;
        box-shadow: 0 12px 28px rgba(242, 138, 55, 0.24);
    }
    .pill {
        border: 1px solid #ab5f5f;
        border-radius: 999px;
        padding: 10px 18px;
        color: #dacfc1;
        background: rgba(42, 37, 31, 0.72);
        font-weight: 700;
    }
    .card {
        background: rgba(36, 35, 31, 0.94);
        border: 1px solid var(--line);
        border-radius: 14px;
        box-shadow: 0 18px 40px rgba(0,0,0,0.24);
        overflow: hidden;
        margin-bottom: 18px;
    }
    .card-head {
        padding: 18px 22px;
        border-bottom: 1px solid var(--line);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
    }
    .card-head h3 { font-size: 24px; line-height: 1.25; margin: 0; }
    .card-body { padding: 20px 22px; }
    .module-card {
        border: 1px solid #3d3a33;
        border-radius: 9px;
        padding: 13px 14px;
        margin-bottom: 12px;
        background: #282720;
    }
    .module-card.active { border-color: #c55a65; background: #332625; }
    .module-title { font-size: 15px; font-weight: 800; color: #f4eadd; line-height: 1.45; }
    .module-tag {
        float: right;
        color: var(--orange);
        background: rgba(242, 138, 55, 0.13);
        border-radius: 6px;
        padding: 2px 8px;
        font-size: 12px;
        font-weight: 900;
    }
    .monitor-card {
        border: 1px solid #7b1f48;
        background: #2d2024;
        border-radius: 10px;
        padding: 13px 14px;
        margin-bottom: 10px;
    }
    .monitor-card .value { font-size: 24px; font-weight: 900; color: white; margin-top: 4px; }
    .param-card {
        border: 1px solid #403d36;
        background: #23221e;
        border-radius: 12px;
        padding: 16px 18px;
        margin-bottom: 14px;
    }
    .param-label { font-weight: 900; color: white; margin-bottom: 6px; }
    .param-help { color: var(--muted); font-size: 13px; line-height: 1.5; }
    .result-hero {
        border: 1px dashed #93494d;
        border-left: 5px solid #e76872;
        background: #302321;
        border-radius: 12px;
        padding: 28px 18px;
        text-align: center;
        margin-bottom: 20px;
    }
    .result-hero .label { color: #e76872; font-weight: 900; }
    .result-hero .title { font-size: 24px; font-weight: 900; margin: 12px 0; color: white; line-height: 1.42; overflow-wrap: anywhere; }
    .result-hero .confidence { color: #e76872; font-size: 25px; font-weight: 900; }
    .bar-row { margin: 12px 0 18px; }
    .bar-line { display: flex; justify-content: space-between; gap: 12px; color: #e6d6c8; font-weight: 800; margin-bottom: 6px; }
    .track { height: 8px; border-radius: 99px; background: #3b3831; overflow: hidden; }
    .fill { height: 100%; border-radius: 99px; background: linear-gradient(90deg, #a86ff4, #64b5ee); }
    .trace {
        border: 1px solid #3d3a33;
        border-radius: 10px;
        background: #24231f;
        padding: 16px 18px;
    }
    .rule {
        display: inline-block;
        color: var(--orange);
        background: rgba(242, 138, 55, 0.13);
        border: 1px solid rgba(242, 138, 55, 0.35);
        border-radius: 5px;
        padding: 5px 8px;
        margin: 4px 8px 4px 0;
        font-family: ui-monospace, Consolas, monospace;
        font-weight: 900;
        font-size: 12px;
    }
    .rule-text { color: #f28a37; font-weight: 800; }
    .conclusion { color: #42b883; font-weight: 900; margin-top: 12px; }
    .small-note { color: var(--muted); line-height: 1.55; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background: #24231f;
        border: 1px solid var(--line);
        border-radius: 999px;
        color: var(--text);
        padding: 8px 18px;
    }
    .stTabs [aria-selected="true"] { background: var(--orange) !important; color: white !important; }
    div.stButton > button {
        width: 100%;
        background: #2d2a23;
        color: #f7f0e6;
        border: 1px solid #4b463c;
        border-radius: 9px;
        font-weight: 800;
    }
    div.stButton > button:hover {
        background: #3a2d24;
        color: #ffffff;
        border-color: #f28a37;
    }
    div[data-baseweb="input"] input {
        color: #111;
        font-weight: 800;
    }
    div[data-baseweb="select"] > div {
        min-height: 42px;
    }
    .stApp { background: #f5f7fa; color: #172033; }
    [data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid #d9e1ea; }
    [data-testid="stSidebar"] * { color: #172033; }
    h1, h2, h3, h4 { color: #172033; }
    .topbar { border-bottom: 1px solid #d9e1ea; }
    .brand { color: #172033; }
    .brand-badge { background: linear-gradient(135deg, #287271, #5b7cfa); color: #fff; box-shadow: 0 10px 24px rgba(40, 114, 113, 0.18); }
    .pill {
        border: 1px solid #c9d6e2;
        color: #516173;
        background: #ffffff;
    }
    .card {
        background: #ffffff;
        border: 1px solid #d9e1ea;
        border-radius: 10px;
        box-shadow: 0 12px 32px rgba(21, 35, 52, 0.08);
    }
    .card-head { border-bottom: 1px solid #e5ebf1; }
    .module-card { border-color: #d9e1ea; background: #f8fafc; }
    .module-card.active { border-color: #287271; background: #edf7f6; }
    .module-title { color: #172033; }
    .module-tag { color: #287271; background: #e0f2ef; }
    .monitor-card {
        border-color: #d9e1ea;
        background: #ffffff;
    }
    .monitor-card .value { color: #172033; }
    .param-card {
        border-color: #d9e1ea;
        background: #fbfcfe;
    }
    .param-label { color: #172033; }
    .param-help, .small-note { color: #667789; }
    .result-hero {
        border: 1px solid #d9e1ea;
        border-left: 6px solid #287271;
        background: #f8fbfb;
    }
    .result-hero .label { color: #287271; }
    .result-hero .title { color: #172033; }
    .result-hero .confidence { color: #287271; }
    .bar-line { color: #26384d; }
    .track { background: #e5ebf1; }
    .fill { background: linear-gradient(90deg, #287271, #5b7cfa); }
    .trace {
        border-color: #d9e1ea;
        background: #fbfcfe;
    }
    .rule {
        color: #287271;
        background: #e0f2ef;
        border-color: #b9ded8;
    }
    .rule-text { color: #375064; }
    .conclusion { color: #287271; }
    .stTabs [data-baseweb="tab"] {
        background: #ffffff;
        border: 1px solid #d9e1ea;
        color: #516173;
    }
    .stTabs [aria-selected="true"] { background: #287271 !important; color: white !important; }
    div.stButton > button {
        background: #ffffff;
        color: #172033;
        border: 1px solid #c9d6e2;
        border-radius: 8px;
    }
    div.stButton > button:hover {
        background: #edf7f6;
        color: #172033;
        border-color: #287271;
    }
    div[data-testid="stPopover"] button {
        width: 28px;
        height: 28px;
        min-height: 28px;
        padding: 0;
        border-radius: 50%;
        border: 1px solid #b8c9d6;
        background: #eef5f7;
        color: #287271;
        font-size: 15px;
        font-weight: 800;
        font-style: italic;
        font-family: Georgia, serif;
        line-height: 1;
        box-shadow: none;
    }
    div[data-testid="stPopover"] button:hover {
        background: #dff0ee;
        border-color: #287271;
        color: #164b4a;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


METRICS = [
    {
        "key": "cd_3sigma",
        "domain": "Fab",
        "evidence": "cd",
        "label": "CD 3 sigma",
        "unit": "nm",
        "min": 0.0,
        "max": 10.0,
        "default": 0.0,
        "step": 0.1,
        "thresholds": [1, 2, 3, 5, 8],
        "normal": "< 1 nm",
        "abnormal": "> 3 nm",
        "color": "#e76872",
        "help": "Critical dimension variation. True limits must be set by node, layer, and product rule.",
    },
    {
        "key": "overlay_error",
        "domain": "Fab",
        "evidence": "overlay",
        "label": "Overlay total error",
        "unit": "nm",
        "min": 0.0,
        "max": 20.0,
        "default": 0.0,
        "step": 0.5,
        "thresholds": [2, 4, 8, 12, 15],
        "normal": "< 2 nm",
        "abnormal": "> 8 nm",
        "color": "#64b5ee",
        "help": "Layer-to-layer overlay error. Use product layer-pair overlay budget for production.",
    },
    {
        "key": "thickness_nu",
        "domain": "Fab",
        "evidence": "thickness",
        "label": "Film Thickness NU",
        "unit": "%",
        "min": 0.0,
        "max": 10.0,
        "default": 0.0,
        "step": 0.1,
        "thresholds": [1, 2, 3, 5, 8],
        "normal": "< 1%",
        "abnormal": "> 3%",
        "color": "#f3c74f",
        "help": "NU% = (Max - Min) / (2 x Mean) x 100. Example: 104/96/100 nm gives NU = 4%.",
    },
    {
        "key": "etch_error",
        "domain": "Fab",
        "evidence": "etch",
        "label": "Etch depth error",
        "unit": "nm",
        "min": -20.0,
        "max": 20.0,
        "default": 0.0,
        "step": 0.5,
        "thresholds": [2, 5, 8, 12, 16],
        "absolute": True,
        "normal": "0 +/- 2 nm",
        "abnormal": "|error| > 8 nm",
        "color": "#a86ff4",
        "help": "Deviation from target etch depth. Positive and negative errors are both scored by absolute value.",
    },
    {
        "key": "particle_count",
        "domain": "Fab",
        "evidence": "particle",
        "label": "Particle count",
        "unit": "ea/wafer",
        "min": 0.0,
        "max": 100.0,
        "default": 0.0,
        "step": 1.0,
        "thresholds": [5, 10, 20, 50, 80],
        "normal": "< 5 ea/wafer",
        "abnormal": "> 20 ea/wafer",
        "color": "#42b883",
        "help": "Added particle count. Production use should specify particle size bin and inspection recipe.",
    },
    {
        "key": "residue_nm",
        "domain": "Fab",
        "evidence": "residue",
        "label": "Residue / scum thickness",
        "unit": "nm",
        "min": 0.0,
        "max": 15.0,
        "default": 0.0,
        "step": 0.1,
        "thresholds": [0.5, 1, 2, 5, 10],
        "normal": "< 0.5 nm",
        "abnormal": "> 2 nm",
        "color": "#f28a37",
        "help": "Post-develop scum, polymer residue, bottom residue, or incomplete strip residue.",
    },
    {
        "key": "plasma_delta",
        "domain": "Fab",
        "evidence": "plasma",
        "label": "RF power / bias deviation",
        "unit": "%",
        "min": -25.0,
        "max": 25.0,
        "default": 0.0,
        "step": 0.5,
        "thresholds": [2, 5, 8, 12, 20],
        "absolute": True,
        "normal": "0 +/- 2%",
        "abnormal": "|delta| > 8%",
        "color": "#64b5ee",
        "help": "Deviation from plasma recipe baseline. Used as charging and oxide-damage evidence.",
    },
    {
        "key": "scratch_signature",
        "domain": "Fab",
        "evidence": "scratch",
        "label": "Scratch / linear signature",
        "unit": "score",
        "min": 0.0,
        "max": 5.0,
        "default": 0.0,
        "step": 1.0,
        "thresholds": [1, 2, 3, 4, 5],
        "normal": "0",
        "abnormal": "> 3",
        "color": "#42b883",
        "help": "SEM/AOI 或 wafer map 上線狀刮傷特徵的工程分級。",
    },
    {
        "key": "cmp_signature",
        "domain": "Fab",
        "evidence": "cmp_signature",
        "label": "CMP profile signature",
        "unit": "score",
        "min": 0.0,
        "max": 5.0,
        "default": 0.0,
        "step": 1.0,
        "thresholds": [1, 2, 3, 4, 5],
        "normal": "0",
        "abnormal": "> 3",
        "color": "#5b7cfa",
        "help": "由 thickness/profile map、pattern density review 或截面量測判定 CMP dishing/erosion 特徵強度。",
    },
    {
        "key": "collapse_signature",
        "domain": "Fab",
        "evidence": "collapse_signature",
        "label": "Pattern collapse signature",
        "unit": "score",
        "min": 0.0,
        "max": 5.0,
        "default": 0.0,
        "step": 1.0,
        "thresholds": [1, 2, 3, 4, 5],
        "normal": "0",
        "abnormal": "> 3",
        "color": "#e76872",
        "help": "由 top-down SEM 或 cross-section SEM 判定高 aspect ratio 圖形倒塌特徵強度。",
    },
    {
        "key": "iddq_ratio",
        "domain": "FA",
        "evidence": "iddq",
        "label": "IDDQ vs baseline",
        "unit": "x",
        "min": 1.0,
        "max": 20.0,
        "default": 1.0,
        "step": 0.1,
        "thresholds": [1.5, 2, 3, 8, 15],
        "normal": "1.0x baseline",
        "abnormal": "> 3x baseline",
        "color": "#e76872",
        "help": "Standby current relative to golden baseline. 1.0x means no leakage increase.",
    },
    {
        "key": "pin_leakage",
        "domain": "FA",
        "evidence": "pin_leakage",
        "label": "Pin reverse leakage",
        "unit": "uA",
        "min": 0.0,
        "max": 100.0,
        "default": 0.0,
        "step": 1.0,
        "thresholds": [1, 5, 10, 30, 80],
        "normal": "< 1 uA",
        "abnormal": "> 10 uA",
        "color": "#a86ff4",
        "help": "Reverse leakage under defined bias. Product-specific test condition is required in production.",
    },
    {
        "key": "rvcc_gnd",
        "domain": "FA",
        "evidence": "rail_short",
        "label": "VCC-GND resistance",
        "unit": "ohm",
        "min": 0.0,
        "max": 200.0,
        "default": 200.0,
        "step": 1.0,
        "thresholds_low": [100, 50, 20, 10, 5],
        "normal": "> 100 ohm",
        "abnormal": "< 20 ohm",
        "color": "#64b5ee",
        "help": "DC resistance between power and ground. Lower resistance increases hard-short evidence.",
    },
    {
        "key": "chain_delta",
        "domain": "FA",
        "evidence": "resistance_drift",
        "label": "Chain resistance drift",
        "unit": "%",
        "min": 0.0,
        "max": 50.0,
        "default": 0.0,
        "step": 0.5,
        "thresholds": [2, 5, 10, 20, 40],
        "normal": "< 2%",
        "abnormal": "> 10%",
        "color": "#f3c74f",
        "help": "Resistance drift of test chain, via/contact chain, or interconnect structure.",
    },
    {
        "key": "hotspot_delta",
        "domain": "FA",
        "evidence": "thermal",
        "label": "Thermal hotspot delta",
        "unit": "degC",
        "min": 0.0,
        "max": 80.0,
        "default": 0.0,
        "step": 1.0,
        "thresholds": [5, 10, 15, 30, 60],
        "normal": "< 5 degC",
        "abnormal": "> 15 degC",
        "color": "#f28a37",
        "help": "Hotspot temperature above ambient or local background.",
    },
    {
        "key": "functional_fail",
        "domain": "FA",
        "evidence": "logic_fail",
        "label": "Functional fail severity",
        "unit": "score",
        "min": 0.0,
        "max": 5.0,
        "default": 0.0,
        "step": 1.0,
        "thresholds": [1, 2, 3, 4, 5],
        "normal": "0",
        "abnormal": "> 3",
        "color": "#a86ff4",
        "help": "Engineering severity score for stuck-at, timing, clock, or scan failure.",
    },
    {
        "key": "esd_signature",
        "domain": "FA",
        "evidence": "esd_signature",
        "label": "ESD damaged I/O signature",
        "unit": "score",
        "min": 0.0,
        "max": 5.0,
        "default": 0.0,
        "step": 1.0,
        "thresholds": [1, 2, 3, 4, 5],
        "normal": "0",
        "abnormal": "> 3",
        "color": "#e76872",
        "help": "I/O ESD diode, clamp, or pin-specific leakage pattern severity.",
    },
    {
        "key": "eos_signature",
        "domain": "FA",
        "evidence": "eos_signature",
        "label": "EOS burnt / overstress signature",
        "unit": "score",
        "min": 0.0,
        "max": 5.0,
        "default": 0.0,
        "step": 1.0,
        "thresholds": [1, 2, 3, 4, 5],
        "normal": "0",
        "abnormal": "> 3",
        "color": "#f28a37",
        "help": "Burnt, melted, or overstress physical/electrical signature severity.",
    },
    {
        "key": "bondwire_signature",
        "domain": "FA",
        "evidence": "bondwire_signature",
        "label": "Bond-wire continuity signature",
        "unit": "score",
        "min": 0.0,
        "max": 5.0,
        "default": 0.0,
        "step": 1.0,
        "thresholds": [1, 2, 3, 4, 5],
        "normal": "0",
        "abnormal": "> 3",
        "color": "#a86ff4",
        "help": "X-ray, wire pull/shear, intermittent open, or package-level continuity signature.",
    },
]

METRICS_BY_KEY = {metric["key"]: metric for metric in METRICS}

MORPHOLOGY_BOOSTS = {
    "Unknown / not reviewed": {},
    "Bridge-like": {"pattern": 5, "residue": 2, "rail_short": 2},
    "Open-like": {"pattern": 4, "resistance_drift": 2},
    "Residue-like": {"residue": 5, "pattern": 3},
    "Melted / Burnt": {"thermal": 4, "rail_short": 3},
    "Corrosion-like": {"environment": 4, "residue": 2, "resistance_drift": 2},
    "Scratch-like": {"particle": 3, "pattern": 4},
}

WAFER_MAP_BOOSTS = {
    "Unknown": {},
    "Random": {"particle": 2},
    "Ring": {"thickness": 3},
    "Edge": {"thickness": 2, "environment": 2},
    "Streak": {"particle": 2, "pattern": 3},
    "Center-edge": {"cd": 2, "thickness": 2},
    "Die-to-die": {"overlay": 2},
    "Wafer-to-wafer": {"thickness": 2, "plasma": 1},
}

DEFECTS = [
    {
        "id": "BRIDGE",
        "name": "圖形橋接 / 跨橋短路",
        "en": "Fabrication Bridging / Short",
        "tag": "短路",
        "group": "Fab + FA",
        "evidence": "Short fail, IDDQ increase, low VCC-GND resistance, residue, or under-etch evidence.",
        "cause": "曝光不足、顯影不完全、底部殘渣、polymer residue 或金屬蝕刻不足，使相鄰圖形形成物理連接。",
        "solution": "調整 exposure/focus、developer/rinse、descum 與 over-etch margin，並比對 CD 與 residue map。",
        "next": ["FIB cross-section", "In-lens SEM", "IDDQ / VCC-GND resistance confirmation"],
        "weights": {"cd": 10, "etch": 15, "residue": 25, "iddq": 25, "rail_short": 30, "logic_fail": 10, "pattern": 20},
    },
    {
        "id": "OPEN",
        "name": "線路斷路 / 接合開路",
        "en": "Open / Bond-wire Defect",
        "tag": "開路",
        "group": "Fab + FA",
        "evidence": "Open fail, high chain resistance, contact/via not open, bond-wire crack, or particle masking.",
        "cause": "過蝕刻、particle mask、金屬不連續、CMP erosion、via/contact 未開，或後段打線接合裂縫造成開路。",
        "solution": "檢查 etch endpoint、pre-clean、deposition coverage、via/contact etch window、wire bond pull/shear 與 continuity map。",
        "next": ["Continuity map", "Cross-section SEM", "Wire pull/shear or via/contact resistance map"],
        "weights": {"etch": 20, "particle": 15, "resistance_drift": 30, "logic_fail": 10, "pattern": 15},
    },
    {
        "id": "MISALIGN",
        "name": "層間偏移",
        "en": "Misalignment",
        "tag": "對位",
        "group": "Fab",
        "evidence": "Overlay error, via miss, contact resistance increase, or die-to-die wafer signature.",
        "cause": "Alignment mark 污染、stage drift、thermal expansion、chucking error 或 scanner matching 問題導致 overlay 偏移。",
        "solution": "清潔 alignment mark、檢查 scanner matching、stage calibration、chuck condition 與 overlay APC。",
        "next": ["Overlay X/Y/rotation", "Alignment mark review", "Tool matching check"],
        "weights": {"overlay": 40, "residue": 5, "logic_fail": 5, "pattern": 10},
    },
    {
        "id": "CDU",
        "name": "關鍵尺寸不均",
        "en": "CD Uniformity",
        "tag": "CDU",
        "group": "Fab",
        "evidence": "High CD 3 sigma, center-edge wafer signature, or process window instability.",
        "cause": "Coat、PEB、dose/focus、develop、etch loading 或 across-wafer uniformity 異常造成 CD 分佈變寬。",
        "solution": "檢查 coater、hot plate、scanner dose/focus map、develop uniformity 與 etch uniformity。",
        "next": ["CD-SEM map", "PEB temperature map", "Scanner focus/dose trend"],
        "weights": {"cd": 40, "etch": 10, "thickness": 5, "pattern": 10},
    },
    {
        "id": "OXIDE",
        "name": "電漿損傷 / 閘極氧化層擊穿",
        "en": "Plasma Damage / Gate Oxide Breakdown",
        "tag": "漏電",
        "group": "Fab + FA",
        "evidence": "RF deviation, pin leakage, gate leakage, oxide breakdown, or antenna-effect signature.",
        "cause": "Plasma charging、RF instability、grounding issue 或 antenna effect 造成 gate oxide fatigue 與漏電通道。",
        "solution": "檢查 Etch/CVD grounding、RF stability，並 review antenna diode 與 antenna ratio design rule。",
        "next": ["EMMI / OBIRCH", "Gate leakage I-V", "Antenna ratio review"],
        "weights": {"plasma": 30, "pin_leakage": 35, "thermal": 10, "iddq": 10},
    },
    {
        "id": "LATCHUP",
        "name": "Latch-up 鎖定效應",
        "en": "Latch-up Triggered Failure",
        "tag": "鎖定",
        "group": "FA + Process",
        "evidence": "Thermal hotspot, current snapback, persistent high current, and low rail resistance.",
        "cause": "寄生 PNPN thyristor 受過壓、雜訊、well resistance 或 guard ring 不足觸發，導致大電流短路。",
        "solution": "改善 guard ring 與 substrate contact，檢查 well implant dose/energy uniformity 與 latch-up rule。",
        "next": ["Latch-up test", "Thermal imaging", "OBIRCH / EMMI"],
        "weights": {"thermal": 35, "rail_short": 25, "iddq": 25, "logic_fail": 10},
    },
    {
        "id": "PARTICLE",
        "name": "顆粒污染",
        "en": "Particle Contamination",
        "tag": "污染",
        "group": "Fab",
        "evidence": "Random defects, particle count increase, or tool/chamber commonality.",
        "cause": "Chamber flaking、FOUP、robot、filter、CMP slurry、brush clean 或環境微粒造成 random killer defect。",
        "solution": "執行 tool commonality、chamber clean、filter/FOUP/robot blade review 與 particle source tracing。",
        "next": ["Defect review", "TEM-EDS", "Tool commonality"],
        "weights": {"particle": 40, "pattern": 10, "logic_fail": 5},
    },
    {
        "id": "EM",
        "name": "金屬空洞 / 電遷移劣化",
        "en": "Metal Void / Electromigration",
        "tag": "可靠度",
        "group": "Fab + Reliability",
        "evidence": "Chain resistance drift, open behavior, local heating, or interconnect void signature.",
        "cause": "Seed/liner coverage、electrofill chemistry、stress migration 或 high current density 造成 void 與高阻。",
        "solution": "檢查 seed/liner coverage、electrofill chemistry、current density、anneal condition 與 stress migration risk。",
        "next": ["Resistance drift trend", "Cross-section SEM/TEM", "Current density review"],
        "weights": {"thickness": 15, "resistance_drift": 40, "thermal": 10, "particle": 5},
    },
    {
        "id": "CORROSION",
        "name": "金屬電化學腐蝕",
        "en": "Corrosion",
        "tag": "腐蝕",
        "group": "Fab + FA",
        "evidence": "Humidity or queue-time sensitivity, metal pitting, residue, leakage, or resistance drift.",
        "cause": "Cl/F residue、水氣、wet chemistry residue 與長 queue time 會造成 electrochemical corrosion。",
        "solution": "縮短 queue time、加強 rinse/dry、檢查 wet chemistry 並改善 humidity control。",
        "next": ["Ion chromatography", "TOF-SIMS", "Surface SEM"],
        "weights": {"residue": 35, "resistance_drift": 30, "pin_leakage": 20},
    },
    {
        "id": "PEEL",
        "name": "剝離 / 薄膜脫層",
        "en": "Peeling / Delamination",
        "tag": "剝離",
        "group": "Fab",
        "evidence": "Film delamination, edge peel, particle burst, or adhesion failure.",
        "cause": "Film stress、pre-clean 不足、水氣吸附、adhesion layer 不良或 thermal mismatch 造成 delamination。",
        "solution": "調整 film stress、pre-clean/dehydration bake、adhesion layer 與 thermal budget。",
        "next": ["Film stress measurement", "Tape test", "Edge review"],
        "weights": {"thickness": 40, "particle": 10},
    },
    {
        "id": "CMP",
        "name": "CMP 凹陷 / 侵蝕",
        "en": "CMP Dishing / Erosion",
        "tag": "CMP",
        "group": "Fab",
        "evidence": "Film thickness non-uniformity, local thickness loss, or center/edge CMP signature.",
        "cause": "CMP over-polish、pattern density 差異、slurry selectivity 或 pad wear 造成局部凹陷與侵蝕。",
        "solution": "調整 polish time、downforce、slurry selectivity、dummy fill 與 pad conditioning。",
        "next": ["CMP profile map", "Film thickness map", "Pattern density review"],
        "weights": {"thickness": 45, "particle": 5, "pattern": 10},
    },
    {
        "id": "SCRATCH",
        "name": "微刮傷",
        "en": "Micro-scratch",
        "tag": "刮傷",
        "group": "Fab",
        "evidence": "Streak wafer map, particle burst, or linear defect review signature.",
        "cause": "CMP pad debris、slurry agglomeration、brush clean 或 handling 接觸造成線狀刮傷。",
        "solution": "檢查 CMP pad/slurry、brush clean condition、robot handling 與 wafer backside particles。",
        "next": ["Defect review SEM", "Tool commonality", "Scratch direction analysis"],
        "weights": {"particle": 50, "pattern": 25},
    },
    {
        "id": "COLLAPSE",
        "name": "圖形倒塌",
        "en": "Pattern Collapse",
        "tag": "倒塌",
        "group": "Fab",
        "evidence": "High CD variation, residue/bridge-like review, or wet clean/rinse sensitivity.",
        "cause": "高 aspect ratio photoresist 或細線圖形在 rinse/dry 表面張力下機械強度不足而倒塌。",
        "solution": "調整 resist thickness、drying method、rinse recipe、CD target 與 pattern support。",
        "next": ["Top-down SEM", "Cross-section SEM", "Rinse/dry recipe split"],
        "weights": {"cd": 40, "residue": 25, "pattern": 15},
    },
    {
        "id": "ESD",
        "name": "ESD 靜電放電損傷",
        "en": "ESD Damage",
        "tag": "ESD",
        "group": "FA",
        "evidence": "Pin leakage, localized damage, or I/O protection failure signature.",
        "cause": "人體、機台或操作流程中的靜電放電使 I/O ESD diode 或 gate oxide 局部受損。",
        "solution": "檢查 ESD handling、device curve trace、leakage I-V 與受損 pin 對應保護結構。",
        "next": ["Pin leakage map", "Curve trace", "Optical/SEM damage review"],
        "weights": {"pin_leakage": 55, "logic_fail": 15, "iddq": 10},
    },
    {
        "id": "EOS",
        "name": "EOS 電性過載損傷",
        "en": "Electrical Overstress",
        "tag": "EOS",
        "group": "FA",
        "evidence": "High IDDQ, thermal hotspot, low rail resistance, or burnt/melted signature.",
        "cause": "超出額定電壓、電流或功率造成金屬熔融、junction damage 或 power rail short。",
        "solution": "回查測試條件、電源序列、socket/handler、curve trace 與熱點定位。",
        "next": ["Curve trace", "Thermal imaging", "Decap + optical/SEM review"],
        "weights": {"iddq": 35, "thermal": 35, "rail_short": 25, "logic_fail": 10},
    },
    {
        "id": "BONDWIRE",
        "name": "打線斷裂 / 接合缺陷",
        "en": "Bond-wire Defect",
        "tag": "打線",
        "group": "FA",
        "evidence": "Continuity fail, high resistance, intermittent open, or bond pull/shear abnormality.",
        "cause": "打線接合能量不足、焊點疲勞、封裝應力或 EOS 熔斷導致 wire/bond open。",
        "solution": "檢查 bond pull/shear、X-ray、decap optical review 與 package stress history。",
        "next": ["X-ray inspection", "Wire pull/shear", "Decap optical review"],
        "weights": {"resistance_drift": 55, "logic_fail": 35},
    },
]

PRESETS = {
    "BRIDGE": {"residue_nm": 4.0, "etch_error": -8.0, "iddq_ratio": 6.0, "rvcc_gnd": 8.0, "functional_fail": 3.0},
    "OPEN": {"etch_error": 10.0, "chain_delta": 18.0, "functional_fail": 4.0, "particle_count": 18.0},
    "MISALIGN": {"overlay_error": 12.0, "functional_fail": 2.0},
    "CDU": {"cd_3sigma": 5.5, "thickness_nu": 3.5, "etch_error": 4.0},
    "OXIDE": {"plasma_delta": 12.0, "pin_leakage": 18.0, "iddq_ratio": 3.5, "hotspot_delta": 12.0},
    "LATCHUP": {"iddq_ratio": 10.0, "rvcc_gnd": 9.0, "hotspot_delta": 35.0, "functional_fail": 4.0},
    "PARTICLE": {"particle_count": 55.0, "functional_fail": 2.0},
    "EM": {"chain_delta": 26.0, "hotspot_delta": 18.0, "thickness_nu": 4.0},
    "CORROSION": {"residue_nm": 3.0, "chain_delta": 14.0, "pin_leakage": 8.0},
    "PEEL": {"thickness_nu": 6.0, "particle_count": 28.0},
}

STAGE_PRESETS = {
    "前段 Fab 製程/良率端": {
        "BRIDGE": {"residue_nm": 10.0, "etch_error": -16.0, "cd_3sigma": 8.0},
        "OPEN": {"etch_error": 14.0, "particle_count": 35.0},
        "MISALIGN": {"overlay_error": 15.0},
        "CDU": {"cd_3sigma": 7.0, "thickness_nu": 5.0, "etch_error": 7.0},
        "OXIDE": {"plasma_delta": 18.0},
        "PARTICLE": {"particle_count": 80.0},
        "CMP": {"thickness_nu": 8.0, "cmp_signature": 5.0},
        "SCRATCH": {"particle_count": 45.0, "scratch_signature": 5.0},
        "COLLAPSE": {"cd_3sigma": 8.0, "collapse_signature": 5.0},
    },
    "後段 FA 電性/失效分析端": {
        "OXIDE": {"pin_leakage": 55.0, "iddq_ratio": 8.0, "hotspot_delta": 18.0},
        "LATCHUP": {"iddq_ratio": 16.0, "rvcc_gnd": 4.0, "hotspot_delta": 55.0, "functional_fail": 5.0},
        "EM": {"chain_delta": 42.0, "hotspot_delta": 34.0},
        "CORROSION": {"pin_leakage": 35.0, "chain_delta": 24.0},
        "ESD": {"pin_leakage": 80.0, "functional_fail": 3.0, "esd_signature": 5.0},
        "EOS": {"iddq_ratio": 18.0, "hotspot_delta": 60.0, "eos_signature": 5.0},
        "BONDWIRE": {"chain_delta": 45.0, "functional_fail": 5.0, "bondwire_signature": 5.0},
    },
}

STAGE_DEFECT_IDS = {
    "前段 Fab 製程/良率端": ["BRIDGE", "OPEN", "MISALIGN", "CDU", "OXIDE", "PARTICLE", "CMP", "SCRATCH", "COLLAPSE"],
    "後段 FA 電性/失效分析端": ["OXIDE", "LATCHUP", "EM", "CORROSION", "ESD", "EOS", "BONDWIRE"],
}

STAGE_METRIC_DOMAIN = {
    "前段 Fab 製程/良率端": "Fab",
    "後段 FA 電性/失效分析端": "FA",
}

STAGE_WEIGHTS = {
    "前段 Fab 製程/良率端": {
        "BRIDGE": {"residue": 45, "etch": 30, "cd": 15, "pattern": 10},
        "OPEN": {"etch": 45, "particle": 25, "pattern": 10},
        "MISALIGN": {"overlay": 60, "pattern": 10},
        "CDU": {"cd": 55, "thickness": 25, "etch": 15, "pattern": 10},
        "OXIDE": {"plasma": 65, "etch": 5},
        "PARTICLE": {"particle": 65, "pattern": 15},
        "CORROSION": {"residue": 60, "environment": 10},
        "CMP": {"cmp_signature": 70, "thickness": 25, "pattern": 10},
        "SCRATCH": {"scratch": 70, "particle": 20, "pattern": 10},
        "COLLAPSE": {"collapse_signature": 70, "cd": 25, "pattern": 10},
    },
    "後段 FA 電性/失效分析端": {
        "OXIDE": {"pin_leakage": 60, "iddq": 15, "thermal": 10},
        "LATCHUP": {"thermal": 50, "rail_short": 40, "iddq": 25, "logic_fail": 10},
        "EM": {"resistance_drift": 60, "thermal": 25},
        "CORROSION": {"pin_leakage": 60, "resistance_drift": 15},
        "ESD": {"esd_signature": 70, "pin_leakage": 35, "logic_fail": 10},
        "EOS": {"eos_signature": 90, "iddq": 25, "thermal": 30, "rail_short": 5},
        "BONDWIRE": {"bondwire_signature": 70, "resistance_drift": 35, "logic_fail": 25},
    },
}

STAGE_DEFECT_DETAILS = {
    "前段 Fab 製程/良率端": {
        "BRIDGE": {"evidence": "Residue/scum、under-etch、CD 偏移或 wafer map pattern 支援圖形橋接。", "cause": "曝光、顯影、descum 或蝕刻不足，使相鄰圖形在製程端形成物理連接。", "solution": "調整 exposure/focus、developer/rinse、descum 與 over-etch margin。", "next": ["Post-etch SEM", "FIB cross-section", "CD-SEM / residue map"]},
        "OPEN": {"evidence": "Etch error、particle mask 或 metal discontinuity 支援前段線路斷路。", "cause": "過蝕刻、particle 遮蔽、金屬覆蓋不足或 via/contact 未開造成導線中斷。", "solution": "檢查 etch endpoint、pre-clean、deposition coverage 與 via/contact etch window。", "next": ["Cross-section SEM", "Via/contact profile", "Defect review"]},
        "OXIDE": {"evidence": "RF power/bias deviation 支援 plasma charging 或 antenna damage 風險。", "cause": "Etch/CVD plasma 不穩、接地不良或 antenna effect 造成氧化層預損傷。", "solution": "檢查 RF stability、chamber grounding 與 plasma recipe window。", "next": ["FDC trace review", "Antenna ratio review", "Plasma recipe comparison"]},
        "CMP": {"evidence": "CMP profile signature、Film Thickness NU 或局部厚度損失支援 CMP dishing/erosion。", "cause": "CMP over-polish、pattern density 差異或 pad/slurry 條件造成局部凹陷。", "solution": "調整 CMP time、downforce、slurry selectivity、dummy fill 與 pad conditioning。", "next": ["CMP profile map", "Film thickness map", "Pattern density review"]},
        "SCRATCH": {"evidence": "Particle count 與 streak/scratch defect review 支援微刮傷。", "cause": "Pad debris、slurry agglomeration、brush clean 或 handling 接觸造成線狀刮傷。", "solution": "檢查 CMP pad/slurry、brush clean、robot handling 與 backside particles。", "next": ["Defect review SEM", "Tool commonality", "Scratch direction analysis"]},
        "COLLAPSE": {"evidence": "Pattern collapse signature 與 CD variation 支援 pattern collapse。", "cause": "高 aspect ratio resist 在 rinse/dry 表面張力下倒塌。", "solution": "調整 resist thickness、drying method、rinse recipe 與 pattern support。", "next": ["Top-down SEM", "Cross-section SEM", "Rinse/dry recipe split"]},
    },
    "後段 FA 電性/失效分析端": {
        "OPEN": {"evidence": "Chain resistance drift、functional fail 或 continuity fail 支援接合/互連開路。", "cause": "Bond-wire crack、接合點疲勞、package interconnect open 或晶片內高阻互連造成開路。", "solution": "進行 continuity map、wire pull/shear 與局部截面確認。", "next": ["Continuity map", "Wire pull/shear", "Cross-section SEM"]},
        "OXIDE": {"evidence": "Pin leakage、IDDQ increase 或 thermal hotspot 支援氧化層擊穿。", "cause": "氧化層弱點或前期損傷在電性測試中形成漏電通道。", "solution": "用 leakage I-V、EMMI/OBIRCH 定位漏電點，並回溯 stress condition。", "next": ["Gate leakage I-V", "EMMI / OBIRCH", "Curve trace"]},
        "CORROSION": {"evidence": "Pin leakage 與 resistance drift 支援後段金屬腐蝕或 pad/interconnect 劣化。", "cause": "水氣、離子污染或封裝/儲存條件造成金屬腐蝕與漏電。", "solution": "執行表面分析、離子污染檢測與封裝環境回溯。", "next": ["Surface SEM", "Ion chromatography", "TOF-SIMS"]},
        "ESD": {"evidence": "Pin leakage 與 I/O 相關 functional fail 支援 ESD damage。", "cause": "靜電放電造成 ESD diode、I/O clamp 或 gate oxide 局部損傷。", "solution": "檢查 ESD handling、curve trace 與受損 pin 的保護結構。", "next": ["Pin leakage map", "Curve trace", "Optical/SEM damage review"]},
        "EOS": {"evidence": "高 IDDQ、低 rail resistance 與熱點支援 EOS damage。", "cause": "超出額定電壓、電流或功率造成 junction/metal 熔融與短路。", "solution": "回查測試條件、電源序列、socket/handler 與熱點位置。", "next": ["Curve trace", "Thermal imaging", "Decap + optical/SEM review"]},
        "BONDWIRE": {"evidence": "Chain resistance drift 與 continuity/functional fail 支援打線或接合開路。", "cause": "打線接合能量不足、焊點疲勞、封裝應力或 EOS 熔斷。", "solution": "執行 X-ray、wire pull/shear 與 decap optical review。", "next": ["X-ray inspection", "Wire pull/shear", "Decap optical review"]},
    },
}

DEFECT_REFERENCE_MODULES = {
    "BRIDGE": [
        {"metric": "Residue / scum thickness", "normal": "< 0.5 nm", "watch": "1-2 nm", "strong": "> 2 nm", "method": "Post-develop / post-etch SEM, residue review", "meaning": "底部殘膜或 polymer residue 可能導致相鄰線路橋接。"},
        {"metric": "Etch depth error", "normal": "0 +/- 2 nm", "watch": "|error| 5-8 nm", "strong": "|error| > 8 nm", "method": "Etch depth metrology, cross-section SEM", "meaning": "蝕刻不足時容易留下導電殘留，蝕刻過度則需同步檢查 open。"},
        {"metric": "IDDQ vs baseline", "normal": "1.0-1.5x", "watch": "2-3x", "strong": "> 3x", "method": "IDDQ / standby leakage test", "meaning": "橋接短路常使待機電流高於 golden baseline。"},
        {"metric": "VCC-GND resistance", "normal": "> 100 ohm", "watch": "20-50 ohm", "strong": "< 20 ohm", "method": "DC resistance, curve trace", "meaning": "低阻值支援 hard short 或 bridging 判斷。"},
    ],
    "OPEN": [
        {"metric": "Chain resistance drift", "normal": "< 2%", "watch": "5-10%", "strong": "> 10%", "method": "Via/contact chain, Kelvin structure", "meaning": "高阻或漂移常對應 open、void、via not open。"},
        {"metric": "Etch depth error", "normal": "0 +/- 2 nm", "watch": "|error| 5-8 nm", "strong": "|error| > 8 nm", "method": "Cross-section SEM, endpoint trend", "meaning": "過蝕刻可能造成導線斷裂，蝕刻不足可能造成 via/contact 未開。"},
        {"metric": "Functional fail severity", "normal": "0", "watch": "2-3", "strong": "> 3", "method": "Scan chain, continuity map", "meaning": "固定開路或連續性失效會反映在功能測試。"},
        {"metric": "Particle count", "normal": "< 5 ea/wafer", "watch": "10-20 ea/wafer", "strong": "> 20 ea/wafer", "method": "Defect inspection, SEM review", "meaning": "Particle mask 可能造成局部未蝕刻或開口不完全。"},
    ],
    "MISALIGN": [
        {"metric": "Overlay total error", "normal": "< 2 nm", "watch": "4-8 nm", "strong": "> 8 nm", "method": "Overlay metrology X/Y/rotation", "meaning": "疊對誤差直接支援 misalignment、via miss、contact miss。"},
        {"metric": "Wafer map pattern", "normal": "No systematic pattern", "watch": "Die-to-die", "strong": "Repeated layer-pair shift", "method": "Overlay map, scanner matching", "meaning": "Die-to-die 或 scanner signature 可提示 stage / matching 問題。"},
        {"metric": "Functional fail severity", "normal": "0", "watch": "1-2", "strong": "> 3", "method": "Bitmap fail map, electrical fail map", "meaning": "局部 via/contact miss 可能造成功能錯誤或高阻。"},
    ],
    "CDU": [
        {"metric": "CD 3 sigma", "normal": "< 1 nm", "watch": "2-3 nm", "strong": "> 3 nm", "method": "CD-SEM map, across-wafer CD trend", "meaning": "CD 分佈變寬是 CDU 異常的主要證據。"},
        {"metric": "Film Thickness NU", "normal": "< 1%", "watch": "2-3%", "strong": "> 3%", "method": "Ellipsometry / thickness map", "meaning": "薄膜不均會改變曝光、蝕刻或 CMP window。"},
        {"metric": "Etch depth error", "normal": "0 +/- 2 nm", "watch": "|error| 5-8 nm", "strong": "|error| > 8 nm", "method": "Etch uniformity map", "meaning": "Etch loading 或 chamber uniformity 會放大 CD variation。"},
        {"metric": "Wafer map pattern", "normal": "Random / flat", "watch": "Center-edge", "strong": "Ring / center-edge repeated", "method": "CD map, focus/dose map", "meaning": "Center-edge pattern 常提示 coat、PEB、focus/dose 或 etch uniformity。"},
    ],
    "OXIDE": [
        {"metric": "RF power / bias deviation", "normal": "0 +/- 2%", "watch": "|delta| 5-8%", "strong": "|delta| > 8%", "method": "FDC trace, plasma recipe comparison", "meaning": "RF 或 bias 偏移會提高 charging damage 與 antenna effect 風險。"},
        {"metric": "Pin reverse leakage", "normal": "< 1 uA", "watch": "5-10 uA", "strong": "> 10 uA", "method": "Pin leakage, gate leakage I-V", "meaning": "氧化層弱點或 plasma damage 常表現為漏電上升。"},
        {"metric": "Thermal hotspot delta", "normal": "< 5 degC", "watch": "10-15 degC", "strong": "> 15 degC", "method": "EMMI / OBIRCH / lock-in thermography", "meaning": "局部漏電通道可能形成熱點，但需與 latch-up 區分。"},
    ],
    "LATCHUP": [
        {"metric": "IDDQ vs baseline", "normal": "1.0-1.5x", "watch": "3-8x", "strong": "> 8x", "method": "Current trigger / holding current test", "meaning": "Latch-up 常伴隨大電流且觸發後不易自行恢復。"},
        {"metric": "VCC-GND resistance", "normal": "> 100 ohm", "watch": "10-20 ohm", "strong": "< 10 ohm", "method": "Curve trace, power rail resistance", "meaning": "低阻與高電流一起出現時支援 latch-up 或 hard short。"},
        {"metric": "Thermal hotspot delta", "normal": "< 5 degC", "watch": "15-30 degC", "strong": "> 30 degC", "method": "Thermal imaging, EMMI, OBIRCH", "meaning": "寄生 PNPN 導通會形成明顯局部發熱。"},
    ],
    "PARTICLE": [
        {"metric": "Particle count", "normal": "< 5 ea/wafer", "watch": "10-20 ea/wafer", "strong": "> 20 ea/wafer", "method": "Defect inspection, defect review SEM", "meaning": "Random killer defect 最直接的統計證據。"},
        {"metric": "Wafer map pattern", "normal": "No cluster", "watch": "Random / streak", "strong": "Tool-correlated random burst", "method": "Tool commonality, wafer map clustering", "meaning": "Random 分佈常指向 particle，streak 則可能來自 handling 或 brush clean。"},
        {"metric": "Material analysis", "normal": "No foreign material", "watch": "Unknown residue", "strong": "Al/Si/CMP slurry/metal particle identified", "method": "TEM-EDS, SEM-EDS, TOF-SIMS", "meaning": "元素成分可回溯污染源。"},
    ],
    "EM": [
        {"metric": "Chain resistance drift", "normal": "< 2%", "watch": "10-20%", "strong": "> 20%", "method": "Resistance trend, via chain, interconnect chain", "meaning": "金屬空洞、stress migration 或 electromigration 會造成阻值上升。"},
        {"metric": "Thermal hotspot delta", "normal": "< 5 degC", "watch": "10-15 degC", "strong": "> 15 degC", "method": "Thermal map, EMMI / OBIRCH", "meaning": "局部高阻會造成 joule heating。"},
        {"metric": "Film Thickness NU", "normal": "< 1%", "watch": "2-3%", "strong": "> 3%", "method": "Metal thickness map, CMP profile", "meaning": "厚度與覆蓋不足會提高 void / EM 風險。"},
    ],
    "CORROSION": [
        {"metric": "Residue / scum thickness", "normal": "< 0.5 nm", "watch": "1-2 nm", "strong": "> 2 nm", "method": "Surface SEM, ion chromatography", "meaning": "Cl/F 或濕製程殘留可促進金屬電化學腐蝕。"},
        {"metric": "Pin reverse leakage", "normal": "< 1 uA", "watch": "5-10 uA", "strong": "> 10 uA", "method": "Leakage test, corrosion site isolation", "meaning": "腐蝕造成金屬 pitting 或 dendrite 時可能帶來漏電。"},
        {"metric": "Chain resistance drift", "normal": "< 2%", "watch": "5-10%", "strong": "> 10%", "method": "Resistance drift trend", "meaning": "金屬腐蝕會讓 interconnect 或 pad resistance 漂移。"},
    ],
    "PEEL": [
        {"metric": "Film Thickness NU", "normal": "< 1%", "watch": "3-5%", "strong": "> 5%", "method": "Thickness map, stress wafer bow", "meaning": "薄膜不均與 film stress 常與 delamination 相關。"},
        {"metric": "Particle count", "normal": "< 5 ea/wafer", "watch": "10-20 ea/wafer", "strong": "> 20 ea/wafer", "method": "Edge inspection, defect review", "meaning": "Peeling 可能造成 particle burst 或 edge defect。"},
        {"metric": "Adhesion / stress", "normal": "Pass", "watch": "Marginal", "strong": "Tape test fail / high stress", "method": "Tape test, scratch test, wafer bow", "meaning": "黏著力不足與應力過高是剝離的核心驗證項。"},
    ],
    "CMP": [
        {"metric": "Film Thickness NU", "normal": "< 1%", "watch": "3-5%", "strong": "> 5%", "method": "Film thickness / CMP profile map", "meaning": "CMP dishing/erosion 常反映為局部厚度損失與不均。"},
        {"metric": "CMP profile signature", "normal": "0", "watch": "2-3", "strong": "> 3", "method": "Profile map, cross-section SEM, pattern density review", "meaning": "若 dishing/erosion profile 與 pattern density 高度相關，會強烈支持 CMP 類缺陷。"},
        {"metric": "Wafer map pattern", "normal": "Flat", "watch": "Center / edge trend", "strong": "Repeatable CMP signature", "method": "Wafer map clustering", "meaning": "CMP 或 planarization 問題常出現區域性圖形。"},
    ],
    "SCRATCH": [
        {"metric": "Particle count", "normal": "< 5 ea/wafer", "watch": "10-20 ea/wafer", "strong": "> 20 ea/wafer", "method": "Defect inspection / SEM review", "meaning": "刮傷常伴隨線狀缺陷與 particle burst。"},
        {"metric": "Wafer map pattern", "normal": "No line pattern", "watch": "Streak", "strong": "Repeatable scratch direction", "method": "Scratch direction analysis", "meaning": "線狀分佈可回推 handling 或 clean path。"},
    ],
    "COLLAPSE": [
        {"metric": "CD 3 sigma", "normal": "< 1 nm", "watch": "2-3 nm", "strong": "> 3 nm", "method": "Top-down CD-SEM", "meaning": "細線圖形倒塌會放大 CD variation 或造成局部 bridging-like 形貌。"},
        {"metric": "Pattern collapse signature", "normal": "0", "watch": "2-3", "strong": "> 3", "method": "Top-down SEM, cross-section SEM", "meaning": "直接觀察到高 aspect ratio resist 或細線倒塌時，應作為 pattern collapse 的主證據。"},
        {"metric": "Residue / scum thickness", "normal": "< 0.5 nm", "watch": "1-2 nm", "strong": "> 2 nm", "method": "SEM profile / cross-section", "meaning": "倒塌與殘留、濕式乾燥條件常需一起檢查。"},
    ],
    "ESD": [
        {"metric": "Pin reverse leakage", "normal": "< 1 uA", "watch": "5-10 uA", "strong": "> 10 uA", "method": "Pin leakage / curve trace", "meaning": "ESD diode 或 I/O 保護結構損傷會造成特定 pin 漏電。"},
        {"metric": "Functional fail severity", "normal": "0", "watch": "1-3", "strong": "> 3", "method": "Functional / scan test", "meaning": "I/O 或保護結構失效可能造成邏輯或介面失效。"},
    ],
    "EOS": [
        {"metric": "IDDQ vs baseline", "normal": "1.0-1.5x", "watch": "3-8x", "strong": "> 8x", "method": "IDDQ / curve trace", "meaning": "EOS 常造成高電流或短路型失效。"},
        {"metric": "Thermal hotspot delta", "normal": "< 5 degC", "watch": "15-30 degC", "strong": "> 30 degC", "method": "Thermal imaging", "meaning": "過載損傷可能出現明顯熱點或熔融點。"},
        {"metric": "VCC-GND resistance", "normal": "> 100 ohm", "watch": "10-20 ohm", "strong": "< 10 ohm", "method": "Rail resistance", "meaning": "低 rail resistance 支援 power short 或熔融短路。"},
    ],
    "BONDWIRE": [
        {"metric": "Chain resistance drift", "normal": "< 2%", "watch": "10-20%", "strong": "> 20%", "method": "Continuity / resistance map", "meaning": "打線或接合開路常表現為高阻或不連續。"},
        {"metric": "Functional fail severity", "normal": "0", "watch": "2-3", "strong": "> 3", "method": "Functional test / continuity test", "meaning": "接合開路會造成 pin/function 無法正常導通。"},
    ],
}

RULE_NAMES = {
    "cd": "RULE_CD_VARIATION",
    "overlay": "RULE_OVERLAY_SHIFT",
    "thickness": "RULE_FILM_NU",
    "etch": "RULE_ETCH_ERROR",
    "particle": "RULE_PARTICLE_COUNT",
    "residue": "RULE_RESIDUE_SCUM",
    "plasma": "RULE_PLASMA_CHARGE",
    "scratch": "RULE_SCRATCH_SIGNATURE",
    "cmp_signature": "RULE_CMP_PROFILE_SIGNATURE",
    "collapse_signature": "RULE_PATTERN_COLLAPSE_SIGNATURE",
    "environment": "RULE_ENVIRONMENT",
    "pattern": "RULE_MAP_PATTERN",
    "iddq": "RULE_IDDQ_HIGH",
    "pin_leakage": "RULE_PIN_LEAKAGE",
    "rail_short": "RULE_RES_SHORT",
    "resistance_drift": "RULE_CHAIN_DRIFT",
    "thermal": "RULE_THERMAL_HOTSPOT",
    "logic_fail": "RULE_FUNCTION_FAIL",
    "esd_signature": "RULE_ESD_IO_SIGNATURE",
    "eos_signature": "RULE_EOS_OVERSTRESS_SIGNATURE",
    "bondwire_signature": "RULE_BONDWIRE_CONTINUITY",
}

REFERENCES = [
    {"topic": "ESD / HBM", "source": "ANSI/ESDA/JEDEC JS-001 and legacy JEDEC JESD22-A114 HBM component-level ESD testing", "url": "https://www.jedec.org/standards-documents/results/js001"},
    {"topic": "Latch-up", "source": "JEDEC JESD78 IC Latch-Up Test standard", "url": "https://www.jedec.org/standards-documents/docs/jesd78"},
    {"topic": "Wafer map patterns", "source": "Jeong et al., Scientific Reports 2023, wafer map defect pattern classes including center, ring, edge, scratch, random", "url": "https://www.nature.com/articles/s41598-023-34147-2"},
    {"topic": "Wafer defect pattern classification", "source": "A voting-based ensemble feature network for semiconductor wafer defect classification, PMC", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9519991/"},
    {"topic": "Line edge / linewidth roughness", "source": "NIST, Issues in Line Edge and Linewidth Roughness Metrology", "url": "https://www.nist.gov/publications/issues-line-edge-and-linewidth-roughness-metrology"},
    {"topic": "Electromigration", "source": "NIST, Techniques and Characterization of Pulsed Electromigration at the Wafer Level", "url": "https://www.nist.gov/publications/techniques-and-characterization-pulsed-electromigration-wafer-level-0"},
]


def score_from_thresholds(value: float, metric: dict) -> int:
    value_to_score = abs(value) if metric.get("absolute") else value
    if "thresholds_low" in metric:
        return min(sum(value_to_score <= threshold for threshold in metric["thresholds_low"]), 5)
    return min(sum(value_to_score >= threshold for threshold in metric["thresholds"]), 5)


def threshold_caption(metric: dict) -> str:
    if "thresholds_low" in metric:
        return " / ".join(f"{i + 1}: <= {v:g}{metric['unit']}" for i, v in enumerate(metric["thresholds_low"]))
    return " / ".join(f"{i + 1}: >= {v:g}{metric['unit']}" for i, v in enumerate(metric["thresholds"]))


def add_boosts(scores: dict, boosts: dict) -> None:
    for key, value in boosts.items():
        scores[key] = max(scores.get(key, 0), value)


def stage_evidence_keys(stage: str) -> set[str]:
    metric_domain = STAGE_METRIC_DOMAIN[stage]
    keys = {metric["evidence"] for metric in METRICS if metric["domain"] == metric_domain}
    if metric_domain == "Fab":
        keys.update({"pattern", "environment"})
    else:
        keys.update({"pattern", "residue", "environment"})
    return keys


def build_evidence_scores(values: dict, wafer_map: str, morphology: str, allow_context_boost: bool, metric_domain: str | None = None) -> dict:
    keys = [
        "cd",
        "overlay",
        "thickness",
        "etch",
        "particle",
        "residue",
        "plasma",
        "scratch",
        "cmp_signature",
        "collapse_signature",
        "environment",
        "pattern",
        "iddq",
        "pin_leakage",
        "rail_short",
        "resistance_drift",
        "thermal",
        "logic_fail",
        "esd_signature",
        "eos_signature",
        "bondwire_signature",
    ]
    scores = {key: 0 for key in keys}
    for metric in METRICS:
        if metric_domain and metric["domain"] != metric_domain:
            continue
        scores[metric["evidence"]] = max(scores[metric["evidence"]], score_from_thresholds(values[metric["key"]], metric))
    if allow_context_boost:
        add_boosts(scores, WAFER_MAP_BOOSTS[wafer_map])
        add_boosts(scores, MORPHOLOGY_BOOSTS[morphology])
    return scores


def diagnose(evidence_scores: dict, allowed_ids: list[str] | None = None, allowed_evidence: set[str] | None = None, stage_weights: dict | None = None) -> list[dict]:
    results = []
    for defect in DEFECTS:
        if allowed_ids and defect["id"] not in allowed_ids:
            continue
        weights = stage_weights.get(defect["id"], defect["weights"]) if stage_weights else defect["weights"]
        usable_keys = allowed_evidence or set(evidence_scores.keys())
        raw_score = sum(evidence_scores.get(key, 0) * weights.get(key, 0) for key in usable_keys)
        max_score = 5 * sum(weight for key, weight in weights.items() if weight > 0 and key in usable_keys)
        fit_score = raw_score / max_score if max_score else 0
        results.append({**defect, "raw_score": raw_score, "max_score": max_score, "fit_score": fit_score})
    confidence_power = 30
    fit_total = sum(item["fit_score"] ** confidence_power for item in results)
    for item in results:
        item["probability"] = (item["fit_score"] ** confidence_power) / fit_total if fit_total else 0
    return sorted(results, key=lambda item: item["probability"], reverse=True)


def initialize_state() -> None:
    for metric in METRICS:
        slider_key = f"{metric['key']}_slider"
        input_key = f"{metric['key']}_input"
        st.session_state.setdefault(slider_key, float(metric["default"]))
        st.session_state.setdefault(input_key, float(metric["default"]))
    st.session_state.setdefault("loaded_model", "None")


def sync_from_slider(metric_key: str) -> None:
    st.session_state[f"{metric_key}_input"] = st.session_state[f"{metric_key}_slider"]


def sync_from_input(metric_key: str) -> None:
    st.session_state[f"{metric_key}_slider"] = st.session_state[f"{metric_key}_input"]


def reset_values() -> None:
    for metric in METRICS:
        st.session_state[f"{metric['key']}_slider"] = float(metric["default"])
        st.session_state[f"{metric['key']}_input"] = float(metric["default"])
    st.session_state["loaded_model"] = "None"


def load_preset(defect_id: str, stage: str | None = None) -> None:
    reset_values()
    if stage:
        preset_values = STAGE_PRESETS.get(stage, {}).get(defect_id, {})
    else:
        preset_values = PRESETS.get(defect_id, {})
    for key, value in preset_values.items():
        st.session_state[f"{key}_slider"] = float(value)
        st.session_state[f"{key}_input"] = float(value)
    st.session_state["loaded_model"] = f"{defect_id} / {stage or '典型數據'}"


def defect_by_id(defect_id: str) -> dict:
    return next(defect for defect in DEFECTS if defect["id"] == defect_id)


def stage_detail(defect: dict, stage: str, field: str):
    return STAGE_DEFECT_DETAILS.get(stage, {}).get(defect["id"], {}).get(field, defect[field])


def metric_control(metric: dict) -> float:
    st.markdown(
        f"""
        <div class="param-card">
        """,
        unsafe_allow_html=True,
    )
    title_col, help_col = st.columns([7.5, 0.8])
    with title_col:
        st.markdown(
            f"<div class='param-label'><span style='color:{metric['color']}'>●</span> {metric['label']}</div>",
            unsafe_allow_html=True,
        )
    with help_col:
        with st.popover("i", use_container_width=True):
            st.markdown(metric_explanation(metric))
    st.markdown(
        f"<div class='param-help'>正常：{metric['normal']}　|　異常：{metric['abnormal']}</div>",
        unsafe_allow_html=True,
    )
    slider_col, number_col = st.columns([4.2, 1.25])
    with slider_col:
        st.slider(
            "slider",
            min_value=float(metric["min"]),
            max_value=float(metric["max"]),
            value=float(st.session_state[f"{metric['key']}_slider"]),
            step=float(metric["step"]),
            key=f"{metric['key']}_slider",
            label_visibility="collapsed",
            on_change=sync_from_slider,
            args=(metric["key"],),
            help=metric["help"],
        )
    with number_col:
        st.number_input(
            f"數值 ({metric['unit']})",
            min_value=float(metric["min"]),
            max_value=float(metric["max"]),
            value=float(st.session_state[f"{metric['key']}_input"]),
            step=float(metric["step"]),
            key=f"{metric['key']}_input",
            label_visibility="visible",
            on_change=sync_from_input,
            args=(metric["key"],),
        )
    value = float(st.session_state[f"{metric['key']}_input"])
    score = score_from_thresholds(value, metric)
    st.caption(f"Evidence score: {score}/5 | {threshold_caption(metric)}")
    st.markdown("</div>", unsafe_allow_html=True)
    return value


def result_bar(result: dict) -> str:
    pct = result["probability"] * 100
    return f"""
    <div class="bar-row">
      <div class="bar-line"><span>{result['name']} ({result['en']})</span><span>{pct:.1f}%</span></div>
      <div class="track"><div class="fill" style="width:{pct:.1f}%"></div></div>
    </div>
    """


def topology_svg(defect_id: str, title: str) -> str:
    if defect_id == "OPEN":
        detail = """
        <path d="M92 138 C160 142 170 214 244 214" fill="none" stroke="#a86ff4" stroke-width="4" />
        <circle cx="96" cy="138" r="11" fill="#e76872" opacity="0.8" />
        <path d="M66 130 h28 m-28 10 h20 m-20 10 h34" stroke="#a86ff4" stroke-width="2" stroke-dasharray="5 5" />
        <text x="95" y="292" font-size="10" fill="#a86ff4">PHYSICAL DEFECT: Bond wire crack / open</text>
        """
    elif defect_id == "BRIDGE":
        detail = """
        <rect x="78" y="120" width="235" height="20" rx="8" fill="#6f7580" />
        <rect x="78" y="190" width="235" height="20" rx="8" fill="#6f7580" />
        <path d="M190 125 C225 140 210 182 238 198" fill="none" stroke="#e76872" stroke-width="18" opacity="0.65" />
        <text x="95" y="292" font-size="10" fill="#e76872">PHYSICAL DEFECT: conductive residue bridge</text>
        """
    elif defect_id == "OXIDE":
        detail = """
        <rect x="126" y="118" width="140" height="20" fill="#a86ff4" opacity="0.55" />
        <rect x="126" y="144" width="140" height="9" fill="#64b5ee" />
        <path d="M196 106 l-18 54 h22 l-20 62" fill="none" stroke="#f3c74f" stroke-width="5" />
        <text x="96" y="292" font-size="10" fill="#f3c74f">PHYSICAL DEFECT: gate oxide leakage path</text>
        """
    elif defect_id == "LATCHUP":
        detail = """
        <circle cx="196" cy="165" r="58" fill="#e76872" opacity="0.2" stroke="#e76872" stroke-width="4" />
        <path d="M128 165 h136 M196 96 v138" stroke="#e76872" stroke-width="5" />
        <text x="92" y="292" font-size="10" fill="#e76872">PHYSICAL DEFECT: latch-up thermal hotspot</text>
        """
    else:
        detail = """
        <circle cx="150" cy="143" r="14" fill="#42b883" opacity="0.8" />
        <circle cx="215" cy="202" r="9" fill="#f3c74f" opacity="0.8" />
        <path d="M76 172 h240" stroke="#6f7580" stroke-width="18" stroke-linecap="round" />
        <text x="96" y="292" font-size="10" fill="#42b883">PHYSICAL DEFECT: localized fab signature</text>
        """
    return f"""
    <svg viewBox="0 0 390 330" width="100%" role="img" aria-label="Topology visualizer">
      <rect width="390" height="330" rx="10" fill="#1f1e1a" />
      <rect x="58" y="68" width="274" height="210" rx="12" fill="#232323" stroke="#4f4664" stroke-width="3" />
      <rect x="112" y="105" width="168" height="142" rx="8" fill="#101720" stroke="#38435f" />
      <circle cx="196" cy="174" r="45" fill="none" stroke="#293142" />
      <line x1="28" y1="122" x2="58" y2="122" stroke="#808080" stroke-width="5" />
      <line x1="332" y1="122" x2="362" y2="122" stroke="#808080" stroke-width="5" />
      <line x1="28" y1="176" x2="58" y2="176" stroke="#808080" stroke-width="5" />
      <line x1="332" y1="176" x2="362" y2="176" stroke="#808080" stroke-width="5" />
      <line x1="28" y1="230" x2="58" y2="230" stroke="#808080" stroke-width="5" />
      <line x1="332" y1="230" x2="362" y2="230" stroke="#808080" stroke-width="5" />
      {detail}
      <text x="22" y="34" font-size="16" font-weight="800" fill="#f7f0e6">{title}</text>
    </svg>
    """


def radar_svg(results: list[dict]) -> str:
    axes = [
        ("Bridge", ["BRIDGE"]),
        ("Open", ["OPEN"]),
        ("Overlay", ["MISALIGN", "CDU"]),
        ("Oxide", ["OXIDE"]),
        ("Thermal", ["LATCHUP"]),
        ("Material", ["PARTICLE", "EM", "CORROSION", "PEEL"]),
    ]
    values = [sum(item["probability"] for item in results if item["id"] in ids) for _, ids in axes]
    max_value = max(values) if max(values) > 0 else 1
    normalized = [value / max_value for value in values]
    cx = cy = 185
    radius = 122
    count = len(axes)

    def point(index: int, scale: float) -> tuple[float, float]:
        angle = -math.pi / 2 + (math.tau * index / count)
        return cx + math.cos(angle) * radius * scale, cy + math.sin(angle) * radius * scale

    rings = []
    for scale in [0.25, 0.5, 0.75, 1.0]:
        pts = " ".join(f"{point(i, scale)[0]:.1f},{point(i, scale)[1]:.1f}" for i in range(count))
        rings.append(f'<polygon points="{pts}" fill="none" stroke="#3b3831" stroke-width="1" />')
    lines = []
    labels = []
    for i, (label, _) in enumerate(axes):
        x, y = point(i, 1)
        lx, ly = point(i, 1.16)
        lines.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="#3b3831" />')
        labels.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" font-size="11" fill="#a49b8e">{label}</text>')
    data_pts = " ".join(f"{point(i, normalized[i])[0]:.1f},{point(i, normalized[i])[1]:.1f}" for i in range(count))
    return f"""
    <svg viewBox="0 0 370 370" width="100%" role="img" aria-label="Radar probability chart">
      <rect width="370" height="370" rx="10" fill="#1f1e1a" />
      <text x="20" y="28" font-size="15" font-weight="800" fill="#f7f0e6">失效機制機率模型分佈 (Radar)</text>
      <g transform="translate(0, 14)">
        {''.join(rings)}
        {''.join(lines)}
        <polygon points="{data_pts}" fill="#a86ff4" fill-opacity="0.25" stroke="#a86ff4" stroke-width="4" />
        {''.join(labels)}
      </g>
    </svg>
    """


def reasoning_trace(top: dict, evidence_scores: dict, measurement_strength: int) -> str:
    if measurement_strength == 0:
        return "<div class='trace'><span class='small-note'>尚未達異常門檻，因此不產生推理鏈。</span></div>"
    rules = []
    for key, weight in sorted(top["weights"].items(), key=lambda item: item[1], reverse=True):
        score = evidence_scores.get(key, 0)
        if score > 0:
            rules.append(
                f"<div><span class='rule'>{RULE_NAMES.get(key, key)}</span>"
                f"<span class='rule-text'>Evidence={score}/5，Weight={weight}，Contribution={score * weight}</span></div>"
            )
    if not rules:
        rules.append("<div><span class='rule'>RULE_LOW_SIGNAL</span><span class='rule-text'>目前只有弱訊號，需補充量測。</span></div>")
    return (
        "<div class='trace'>"
        + "".join(rules)
        + f"<div style='text-align:center; color:#a49b8e; margin:10px 0;'>↓</div>"
        + f"<div class='conclusion'>CONCLUSION：{top['name']} ({top['en']})，Fit score={top['fit_score'] * 100:.1f}%</div>"
        + "</div>"
    )


def make_report(case_id: str, stage: str, top_results: list[dict], evidence_scores: dict, values: dict) -> str:
    top = top_results[0]
    domain = STAGE_METRIC_DOMAIN[stage]
    report_metrics = [metric for metric in METRICS if metric["domain"] == domain]
    active_inputs = [
        f"- {metric['label']}: {values[metric['key']]} {metric['unit']} (Evidence {score_from_thresholds(values[metric['key']], metric)}/5)"
        for metric in report_metrics
        if score_from_thresholds(values[metric["key"]], metric) > 0
    ]
    lines = [
        "Wafer-Pro Defect Diagnosis Report",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Case ID: {case_id or '-'}",
        f"Diagnosis Stage: {stage}",
        "",
        "Executive Summary",
        f"- Top diagnosis: {top['name']} ({top['en']})",
        f"- Confidence: {top['probability'] * 100:.1f}%",
        f"- Fit score: {top['fit_score'] * 100:.1f}%",
        "- Note: probabilities are relative expert-system confidence scores, not statistical fab-wide occurrence rates.",
        f"- Recommended first verification: {', '.join(stage_detail(top, stage, 'next')[:2])}",
        "",
        "Top-3 Defects",
    ]
    for index, item in enumerate(top_results, start=1):
        lines.extend(
            [
                f"{index}. {item['name']} ({item['en']}) - {item['probability'] * 100:.1f}%",
                f"   Fit score: {item['fit_score'] * 100:.1f}% | Raw score: {item['raw_score']:.1f} | Max score: {item['max_score']:.1f}",
                f"   Evidence basis: {stage_detail(item, stage, 'evidence')}",
                f"   Cause: {stage_detail(item, stage, 'cause')}",
                f"   Corrective action: {stage_detail(item, stage, 'solution')}",
                f"   Suggested verification: {', '.join(stage_detail(item, stage, 'next'))}",
            ]
        )
    lines.append("")
    lines.append("Triggered Measurements")
    lines.extend(active_inputs if active_inputs else ["- No abnormal measurement has reached a scoring threshold."])
    lines.append("")
    lines.append("Evidence Scores by Rule Key")
    for key, score in evidence_scores.items():
        lines.append(f"- {key}: {score}/5")
    lines.append("")
    lines.append("All Input Values")
    for metric in report_metrics:
        lines.append(f"- {metric['label']}: {values[metric['key']]} {metric['unit']}")
    lines.append("")
    lines.append("Immediate Engineering Actions")
    lines.append("- Re-check the highest-scoring physical/electrical evidence before changing the process recipe.")
    lines.append("- Compare the suspect lot against golden lots by tool, chamber, recipe version, wafer position, and time window.")
    lines.append("- Use the suggested verification methods above to confirm the physical failure site.")
    lines.append("")
    lines.append("Reference Basis")
    for ref in REFERENCES:
        lines.append(f"- {ref['topic']}: {ref['source']} ({ref['url']})")
    return "\n".join(lines)


def reference_rows(defect_id: str) -> list[dict]:
    return [
        {
            "量測項目": item["metric"],
            "正常參考": item["normal"],
            "警戒範圍": item["watch"],
            "強觸發範圍": item["strong"],
            "建議檢測方法": item["method"],
            "判讀意義": item["meaning"],
        }
        for item in DEFECT_REFERENCE_MODULES.get(defect_id, [])
    ]


def metric_explanation(metric: dict) -> str:
    extra_notes = {
        "cd_3sigma": "用 CD-SEM 或 CD metrology 的 across-wafer 統計值填入。數值越大，代表圖形尺寸越不均。",
        "overlay_error": "填入兩層圖形之間的總 overlay error。數值越大，越可能造成 via miss 或 contact miss。",
        "thickness_nu": "Film Thickness NU 使用不均勻度百分比表示。\n\n公式：`NU% = (Max - Min) / (2 x Mean) x 100`\n\n例：Max=104 nm、Min=96 nm、Mean=100 nm，NU = 4%。",
        "etch_error": "填入相對 target etch depth 的偏差。正值代表過蝕刻，負值代表蝕刻不足；系統會用絕對值判斷異常程度。",
        "particle_count": "填入每片 wafer 的新增 particle 數量。正式使用時要先定義 particle size bin 與 inspection recipe。",
        "residue_nm": "填入 scum、polymer residue 或 bottom residue 的厚度。殘留越厚，越容易推向 bridging、corrosion 或 via/contact 問題。",
        "plasma_delta": "填入 RF power 或 bias 相對 recipe baseline 的偏移百分比。正負偏移都可能造成 plasma charging 或 profile 異常。",
        "iddq_ratio": "填入待機電流相對 golden baseline 的倍率。1.0x 代表沒有高於基準，數值越高代表漏電或短路風險越高。",
        "pin_leakage": "填入指定 bias condition 下的接腳反向漏電。正式規格應依產品 datasheet 與測試條件設定。",
        "rvcc_gnd": "填入 VCC 與 GND 之間的 DC 阻抗。數值越低，越支持 hard short 或 latch-up 類失效。",
        "chain_delta": "填入 via/contact chain 或 interconnect chain 的阻值漂移百分比。漂移越大，越支持 open、void 或 corrosion。",
        "hotspot_delta": "填入熱點相對背景溫度的差值。差值越大，越支持 latch-up、局部漏電或高阻發熱。",
        "functional_fail": "以 0 到 5 表示功能失效嚴重度。0 代表未觀察到功能失效，5 代表嚴重且可重現。",
        "scratch_signature": "以 0 到 5 表示 SEM/AOI 或 wafer map 是否出現線狀刮傷特徵。0 代表沒有，5 代表非常明顯。",
        "cmp_signature": "以 0 到 5 表示 CMP profile map、厚度 map 或截面是否呈現 dishing/erosion 特徵。0 代表沒有，5 代表特徵非常明顯。",
        "collapse_signature": "以 0 到 5 表示 top-down SEM 或 cross-section SEM 是否直接看到圖形倒塌。0 代表沒有，5 代表特徵非常明顯。",
        "esd_signature": "以 0 到 5 表示是否出現 I/O ESD 保護結構損傷、pin-specific leakage 或 diode clamp 異常。",
        "eos_signature": "以 0 到 5 表示是否出現燒毀、熔融、過載痕跡或 power stress signature。",
        "bondwire_signature": "以 0 到 5 表示 X-ray、wire pull/shear 或 continuity test 是否支持打線/接合缺陷。",
    }
    note = extra_notes.get(metric["key"], metric["help"])
    return "\n".join(
        [
            f"### {metric['label']}",
            "",
            "**這是什麼？**",
            "",
            note,
            "",
            "**怎麼填？**",
            "",
            f"請輸入量測值，單位是 `{metric['unit']}`。",
            "",
            "**怎麼判讀？**",
            "",
            f"- 正常參考：`{metric['normal']}`",
            f"- 異常參考：`{metric['abnormal']}`",
            "",
            "**系統怎麼給分？**",
            "",
            f"`{threshold_caption(metric)}`",
        ]
    ).strip()


initialize_state()

st.markdown(
    f"""
    <div class="topbar">
      <div class="brand">
        <div class="brand-badge">W</div>
        <div>Wafer-Pro <span style="color:#f28a37; font-size:16px; border:1px solid #7c4a23; border-radius:6px; padding:4px 8px;">缺陷診斷系統</span></div>
      </div>
      <div class="pill"><span style="color:#42b883;">●</span> 已載入故障模型：{st.session_state['loaded_model']}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "<div class='card'><div class='card-head'><h3>案例設定與故障模組參考</h3></div><div class='card-body'>",
    unsafe_allow_html=True,
)
setup_cols = st.columns([1.15, 0.95, 0.95, 1.05, 1.35, 0.75])
with setup_cols[0]:
    case_id = st.text_input("Case / Tool / Lot ID", placeholder="Etcher B / Lot 26A")
with setup_cols[1]:
    wafer_map = st.selectbox("Wafer map 分佈", list(WAFER_MAP_BOOSTS.keys()))
with setup_cols[2]:
    morphology = st.selectbox("SEM/AOI/PFA 型貌補充", list(MORPHOLOGY_BOOSTS.keys()))
with setup_cols[3]:
    selected_stage = st.selectbox("診斷階段", list(STAGE_DEFECT_IDS.keys()), key="selected_stage")
with setup_cols[4]:
    stage_defects = [defect_by_id(defect_id) for defect_id in STAGE_DEFECT_IDS[selected_stage]]
    model_options = {f"{defect['name']} ({defect['id']})": defect["id"] for defect in stage_defects}
    selected_model_label = st.selectbox("缺陷模型", list(model_options.keys()), key=f"selected_model_{selected_stage}")
    selected_model_id = model_options[selected_model_label]
    model_signature = f"{selected_stage}:{selected_model_id}"
    if st.session_state.get("last_loaded_model_signature") != model_signature:
        load_preset(selected_model_id, selected_stage)
        st.session_state["last_loaded_model_signature"] = model_signature
with setup_cols[5]:
    st.button("清除輸入", on_click=reset_values, use_container_width=True)
selected_model = defect_by_id(selected_model_id)
st.caption(
    f"目前模型：{selected_stage} / {selected_model['name']}。選擇缺陷模型後，系統會自動輸入該缺陷形成時的典型數據；下方每個參數仍可用滑桿或手動數值框調整。"
)

with st.expander("查看故障模組知識庫", expanded=False):
    module_rows = [
        {
            "故障模組": defect["name"],
            "英文": defect["en"],
            "分類": selected_stage,
            "主要依據": stage_detail(defect, selected_stage, "evidence"),
            "改善方法": stage_detail(defect, selected_stage, "solution"),
        }
        for defect in stage_defects
    ]
    st.dataframe(module_rows, hide_index=True, use_container_width=True)
st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown(
    f"<div class='card'><div class='card-head'><h3>{selected_stage}量測數據輸入</h3><span class='pill'>滑桿 + 手動輸入</span></div><div class='card-body'>",
    unsafe_allow_html=True,
)
values = {}
current_metric_domain = STAGE_METRIC_DOMAIN[selected_stage]
current_metrics = [item for item in METRICS if item["domain"] == current_metric_domain]
input_cols = st.columns(2)
for index, metric in enumerate(current_metrics):
    with input_cols[index % 2]:
        values[metric["key"]] = metric_control(metric)
for metric in METRICS:
    values.setdefault(metric["key"], float(st.session_state[f"{metric['key']}_input"]))
st.markdown("</div></div>", unsafe_allow_html=True)

allowed_evidence = stage_evidence_keys(selected_stage)
base_evidence_scores = build_evidence_scores(values, "Unknown", "Unknown / not reviewed", False, current_metric_domain)
measurement_strength = sum(base_evidence_scores.values())
allow_context_boost = measurement_strength > 0
effective_wafer_map = wafer_map if allow_context_boost and current_metric_domain == "Fab" else "Unknown"
effective_morphology = morphology if allow_context_boost and current_metric_domain == "FA" else "Unknown / not reviewed"
evidence_scores = build_evidence_scores(values, effective_wafer_map, effective_morphology, allow_context_boost, current_metric_domain)
results = diagnose(evidence_scores, STAGE_DEFECT_IDS[selected_stage], allowed_evidence, STAGE_WEIGHTS[selected_stage])
top_results = results[:3]
top = top_results[0]
report = make_report(case_id, selected_stage, top_results, evidence_scores, values)

monitor_values = [
    *current_metrics[:6],
]
st.markdown("<div class='card'><div class='card-head'><h3>電性 / 製程參數即時監控</h3></div><div class='card-body'>", unsafe_allow_html=True)
monitor_cols = st.columns(6)
for column, metric in zip(monitor_cols, monitor_values):
    with column:
        st.metric(metric["label"], f"{values[metric['key']]:g} {metric['unit']}", f"Score {score_from_thresholds(values[metric['key']], metric)}/5")
st.markdown("</div></div>", unsafe_allow_html=True)

result_tab, reference_tab, visual_tab, trace_tab, ranking_tab = st.tabs(["診斷結果", "標準數據參考", "視覺化模組", "推理鏈與報告", "完整排序與權重"])

with result_tab:
    if measurement_strength == 0:
        st.info("請先輸入至少一個達到異常門檻的量測值。Wafer map 與 SEM/AOI 型貌不會單獨觸發診斷。")
    else:
        hero_col, bars_col = st.columns([1.05, 1.55])
        with hero_col:
            st.markdown(
                f"""
                <div class="result-hero">
                  <div class="label">檢測到失效機制</div>
                  <div class="title">{top['name']}<br>({top['en']})</div>
                  <div>診斷可信度 <span class="confidence">{top['probability'] * 100:.1f}%</span></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with bars_col:
            st.markdown("#### 候選缺陷機率")
            st.markdown("".join(result_bar(item) for item in results), unsafe_allow_html=True)

        st.markdown("#### Top-3 原因、形成機制與改善方法")
        for item in top_results:
            with st.expander(f"{item['name']} ({item['probability'] * 100:.1f}%)", expanded=item == top):
                st.write(f"**主要依據：** {stage_detail(item, selected_stage, 'evidence')}")
                st.write(f"**形成原因：** {stage_detail(item, selected_stage, 'cause')}")
                st.write(f"**改善方法：** {stage_detail(item, selected_stage, 'solution')}")
                st.write("**進階檢測建議：**")
                for step in stage_detail(item, selected_stage, "next"):
                    st.write(f"- {step}")

with reference_tab:
    st.markdown("#### 各缺陷標準數據參考模組")
    st.info("這些數據範圍用來做專家系統初判與教學展示。實際量產門檻需依製程節點、layer、產品規格、測試條件與廠內 SPC baseline 重新校正。")
    st.caption("欄位說明：正常參考代表低風險 baseline；警戒範圍代表需追蹤或補量測；強觸發範圍代表會明顯提高該缺陷權重；建議檢測方法用於實體驗證。")
    reference_summary_rows = []
    for defect in stage_defects:
        strong_rules = "; ".join(f"{item['metric']}: {item['strong']}" for item in DEFECT_REFERENCE_MODULES.get(defect["id"], [])[:3])
        reference_summary_rows.append(
            {
                "缺陷模組": f"{defect['name']} ({defect['en']})",
                "主要強觸發數據": strong_rules,
                "建議驗證": " / ".join(stage_detail(defect, selected_stage, "next")[:2]),
            }
        )
    st.dataframe(reference_summary_rows, hide_index=True, use_container_width=True)

    for defect in stage_defects:
        with st.expander(f"{defect['name']} ({defect['id']})", expanded=defect == top):
            st.write(f"**形成原因：** {stage_detail(defect, selected_stage, 'cause')}")
            st.write(f"**改善方法：** {stage_detail(defect, selected_stage, 'solution')}")
            st.dataframe(reference_rows(defect["id"]), hide_index=True, use_container_width=True)
    st.markdown("#### 文獻與標準參考")
    st.caption("以下資料用於建立診斷項目、測試方法與失效機制分類；實際製程門檻仍需依廠內 SPC / WAT / PCM / FA database 校正。")
    for ref in REFERENCES:
        st.markdown(f"- **{ref['topic']}**：{ref['source']}  \n  {ref['url']}")

with visual_tab:
    topo_col, radar_col = st.columns(2)
    with topo_col:
        st.markdown("#### 晶片物理失效拓撲圖")
        components.html(topology_svg(top["id"], top["name"] if measurement_strength > 0 else "等待輸入"), height=380)
    with radar_col:
        st.markdown("#### 六邊形 / Radar 機率統整")
        components.html(radar_svg(results), height=380)
    legend_cols = st.columns(4)
    legend_cols[0].markdown("<span style='color:#e76872'>■</span> Short / Leakage", unsafe_allow_html=True)
    legend_cols[1].markdown("<span style='color:#a86ff4'>■</span> Open / Bridge", unsafe_allow_html=True)
    legend_cols[2].markdown("<span style='color:#f3c74f'>■</span> Thermal / Latch-up", unsafe_allow_html=True)
    legend_cols[3].markdown("<span style='color:#64b5ee'>■</span> Oxide / Plasma", unsafe_allow_html=True)

with trace_tab:
    trace_col, report_col = st.columns([1.35, 1])
    with trace_col:
        st.markdown("#### 專家推理決策路徑 (Reasoning Trace)")
        st.markdown(reasoning_trace(top, evidence_scores, measurement_strength), unsafe_allow_html=True)
    with report_col:
        st.markdown("#### 診斷報告")
        st.download_button("匯出診斷報告", report, file_name="wafer_pro_diagnosis_report.txt", mime="text/plain", use_container_width=True)
        st.text_area("報告預覽", report, height=330)

with ranking_tab:
    rank_rows = [
        {
            "排名": index + 1,
            "候選缺陷": f"{item['name']} ({item['en']})",
            "分類": selected_stage,
            "機率": f"{item['probability'] * 100:.1f}%" if measurement_strength > 0 else "0.0%",
            "Fit score": f"{item['fit_score'] * 100:.1f}%",
            "Raw score": round(item["raw_score"], 1),
            "Max score": round(item["max_score"], 1),
        }
        for index, item in enumerate(results)
    ]
    st.dataframe(rank_rows, hide_index=True, use_container_width=True)
    with st.expander("推論與加權規則說明", expanded=True):
        st.write("1. 每個輸入數值先依門檻轉為 Evidence score 0-5。")
        st.write("2. 每種缺陷有自己的 evidence 權重矩陣；Fab 模型主要看 CD、overlay、etch、residue、particle、plasma 與 profile signature，FA 模型主要看 IDDQ、pin leakage、rail resistance、thermal、chain resistance 與失效 signature。")
        st.write("3. Raw score = sum(Evidence score x defect weight)。")
        st.write("4. Max score = 5 x sum(positive weights for that defect)。")
        st.write("5. Fit score = Raw score / Max score。最後機率由全部缺陷的 Fit score 正規化，因此不同總權重的缺陷可以公平比較。")
        st.write({"Wafer map used": effective_wafer_map, "Morphology used": effective_morphology, "Evidence scores": evidence_scores})
