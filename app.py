from datetime import datetime
from uuid import uuid4

import streamlit as st

from car import NAMES, car_svg, parts_for
from engine import diagnose
from questions import COMMON, QUESTIONS, READINGS, SCENARIOS, TRACKS
from rules import RULES

STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600&family=Barlow+Condensed:wght@600;700&display=swap');
:root { color-scheme: dark; }
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #0b0f17 radial-gradient(900px 420px at 85% -8%, rgba(255, 138, 31, 0.11), transparent 60%) !important;
    font-family: 'Barlow', system-ui, sans-serif;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] *, [data-testid="stAppDeployButton"] * { color: #93a0b4 !important; }
.stApp p, .stApp li, .stApp label, .stApp summary, .stApp span, .stApp strong { color: #e9eef6; }
.stApp p, .stApp li, .stApp label, .stApp strong { font-family: 'Barlow', system-ui, sans-serif; }
[data-testid="stIconMaterial"] {
    font-family: 'Material Symbols Rounded', 'Material Symbols Outlined' !important;
    color: #93a0b4 !important;
}
.stApp h1, .stApp h2, .stApp h3, .stApp h4 {
    color: #ffffff !important;
    font-family: 'Barlow Condensed', 'Barlow', system-ui, sans-serif !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    font-weight: 700 !important;
}
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] * { color: #93a0b4 !important; }

[data-testid="stTab"] p { color: #93a0b4 !important; font-weight: 600; }
[data-testid="stTab"][data-selected="true"] p { color: #ff8a1f !important; }
.react-aria-SelectionIndicator { background: #ff8a1f !important; }

.hero {
    position: relative;
    padding: 2.4rem 1.8rem 2rem 1.8rem;
    border-radius: 18px;
    border: 1px solid rgba(255, 138, 31, 0.35);
    background: linear-gradient(135deg, rgba(255, 138, 31, 0.20), rgba(18, 25, 38, 0.92) 58%);
    margin-bottom: 1.8rem;
    overflow: hidden;
}
.hero::before {
    content: "";
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 5px;
    background: #ff8a1f;
}
.hero h1 {
    margin: 0.3rem 0 0.9rem 0; padding: 0;
    font-size: 3.2rem; line-height: 1;
    color: #ffffff !important;
    font-family: 'Barlow Condensed', 'Barlow', system-ui, sans-serif !important;
    text-transform: uppercase; letter-spacing: 0.03em; font-weight: 700;
}
.hero p { margin: 0; color: #b4bfcf !important; font-size: 1.05rem; line-height: 1.5; }
.hero .eyebrow {
    color: #ff8a1f !important;
    letter-spacing: 0.22em; font-size: 0.75rem; font-weight: 600;
}

[class*="st-key-card"] {
    background: #121926 !important;
    border: 1px solid #263247 !important;
    border-radius: 14px !important;
    padding: 0.4rem 0.4rem;
}
[data-testid="stMetric"] {
    background: #121926;
    border: 1px solid #263247;
    border-radius: 12px;
    padding: 0.7rem 0.8rem;
}
[data-testid="stMetricValue"], [data-testid="stMetricValue"] * { color: #ff8a1f !important; font-weight: 700; }
[data-testid="stMetricLabel"], [data-testid="stMetricLabel"] * { color: #93a0b4 !important; }

[data-testid="stSelectbox"] [role="group"] {
    background: #0f1520 !important;
    border: 1px solid #2c3a52 !important;
    border-radius: 10px !important;
}
[data-testid="stSelectbox"] input { color: #e9eef6 !important; -webkit-text-fill-color: #e9eef6 !important; }
[data-testid="stSelectbox"] svg { fill: #93a0b4 !important; color: #93a0b4 !important; }

[data-testid="stSlider"] [role="slider"] { background-color: #ff8a1f !important; }
[data-testid="stSliderThumbValue"], [data-testid="stSliderThumbValue"] * { color: #ff8a1f !important; }
[data-testid="stSliderTickBarMin"], [data-testid="stSliderTickBarMax"] { color: #93a0b4 !important; }

[data-testid="stRadioOption"] > div > div:first-child {
    border: 2px solid #3a4860 !important;
    background: #0f1520 !important;
}
[data-testid="stRadioOption"][data-selected="true"] > div > div:first-child {
    border-color: #ff8a1f !important;
    background: #ff8a1f !important;
}
[data-testid="stRadioOption"][data-selected="true"] > div > div:first-child > div { background: #0b0f17 !important; }

[data-testid="stCheckbox"] label > div:nth-of-type(1) {
    border: 2px solid #3a4860 !important;
    background: #0f1520 !important;
    border-radius: 6px !important;
}
[data-testid="stCheckbox"] label[data-selected="true"] > div:nth-of-type(1) {
    background: #ff8a1f !important;
    border-color: #ff8a1f !important;
}

[data-testid="stProgressBarTrack"] { background: #1b2536 !important; border-radius: 999px !important; }
[data-testid="stProgressBarTrack"] > div {
    background: linear-gradient(90deg, #ff8a1f, #ffc062) !important;
    border-radius: 999px !important;
}

[data-testid="stExpander"], [data-testid="stExpander"] details {
    background: #0f1520 !important;
    border: 1px solid #263247 !important;
    border-radius: 10px !important;
}
[data-testid="stExpander"] summary { background: transparent !important; }
[data-testid="stExpander"] summary p { color: #e9eef6 !important; }
[data-testid="stExpanderDetails"] { border-color: #263247 !important; }

[data-testid="stAlert"] {
    background: rgba(255, 138, 31, 0.09) !important;
    border: 1px solid rgba(255, 138, 31, 0.35) !important;
    border-radius: 12px !important;
}
[data-testid="stAlert"] * { color: #f2d9bd !important; }

[data-testid="stCode"], [data-testid="stCode"] pre, [data-testid="stCode"] code {
    background: #0f1520 !important;
    color: #e9eef6 !important;
    border-radius: 10px !important;
}
[data-testid="stCode"] span { color: #e9eef6 !important; }

[data-testid="stDownloadButton"] button,
button[data-testid="stBaseButton-primary"] {
    background: #ff8a1f !important;
    border: 0 !important;
    border-radius: 10px !important;
}
[data-testid="stDownloadButton"] button *,
button[data-testid="stBaseButton-primary"] * { color: #1a0f00 !important; font-weight: 600; }

.meter {
    padding: 1.4rem 1.4rem 1.2rem 1.4rem;
    border-radius: 16px;
    border: 1px solid #263247;
    background: #121926;
    margin: 0.5rem 0 1.4rem 0;
}
.meter-head { display: flex; justify-content: space-between; align-items: baseline; }
.meter .meter-label { letter-spacing: 0.2em; font-size: 0.75rem; font-weight: 600; color: #93a0b4 !important; }
.meter .meter-value {
    font-size: 2.8rem; line-height: 1; font-weight: 700;
    color: #ff8a1f !important;
    font-family: 'Barlow Condensed', 'Barlow', system-ui, sans-serif !important;
}
.meter .meter-value small { font-size: 1rem; color: #93a0b4 !important; margin-left: 0.2rem; }
.meter-track { height: 10px; border-radius: 999px; background: #1b2536; margin: 1rem 0; overflow: hidden; }
.meter-fill { height: 100%; border-radius: 999px; background: linear-gradient(90deg, #ff8a1f, #ffc062); }
.meter p { margin: 0; color: #b4bfcf !important; line-height: 1.5; }

.chips { display: flex; flex-wrap: wrap; gap: 0.4rem; margin: 0.3rem 0 1rem 0; }
.chip {
    padding: 0.25rem 0.8rem;
    border-radius: 999px;
    border: 1px solid rgba(255, 138, 31, 0.45);
    background: rgba(255, 138, 31, 0.10);
    color: #ffc062 !important;
    font-size: 0.85rem;
    font-weight: 600;
}

.car { max-width: 220px; margin: 0 auto; }
.car svg { display: block; width: 100%; height: auto; }
.car .off { fill: #1b2536; stroke: #3a4860; stroke-width: 1.5; }
.car .on {
    fill: #ff8a1f;
    stroke: #ffc062;
    stroke-width: 1.5;
    filter: drop-shadow(0 0 5px rgba(255, 138, 31, 0.9));
}

</style>
"""

st.set_page_config(page_title="F1 Setup Doctor", layout="centered")
st.markdown(STYLE, unsafe_allow_html=True)


def pretty(text):
    return text.replace("_", " ").capitalize()


def strength(cf):
    if cf >= 0.8:
        return "strong match"
    if cf >= 0.6:
        return "likely"
    return "worth trying"


def chips(facts):
    shown = [pretty(k) if v == "yes" else pretty(v) for k, v in facts.items() if v not in ("no", "not sure")]
    return '<div class="chips">' + "".join(f'<span class="chip">{label}</span>' for label in shown) + "</div>"


def ask(text, options, key):
    choices = ["not sure"] + options
    if len(choices) > 4:
        return st.selectbox(text, choices, format_func=pretty, key=key)
    return st.radio(text, choices, horizontal=True, format_func=pretty, key=key)


def reading(name, key):
    label, low, high, default, limit = READINGS[name]
    value = st.slider(label, low, high, default, key=key)
    fact = "yes" if value > limit else "no"
    st.caption(f"Derived fact: {pretty(name)} = {fact} ({value} °C against a limit of {limit} °C)")
    return fact


def build_sheet(facts, accepted, fired):
    lines = ["F1 SETUP SHEET", "", "Observations"]
    for key, value in facts.items():
        if value != "not sure":
            lines.append(f"  {pretty(key)}: {pretty(value)}")
    lines += ["", "Changes to make, in order"]
    for number, (fix, cf) in enumerate(accepted, 1):
        lines.append(f"  {number}. {fix} ({cf:.0%})")
        for rule in fired:
            if rule["fix"] == fix:
                lines.append(f"     {rule['id']}: {rule['why']}")
    lines += ["", "Change one item at a time and test it on track before the next."]
    return "\n".join(lines)


def new_report(facts, label):
    now = datetime.now()
    return {
        "facts": dict(facts),
        "label": label,
        "id": f"INV-{now:%Y%m%d-%H%M%S}-{uuid4().hex[:4].upper()}",
        "time": now.isoformat(timespec="seconds"),
    }


def show_report(report, prefix):
    facts = report["facts"]
    results, fired = diagnose(facts)
    ranked = sorted(results.items(), key=lambda item: item[1], reverse=True)
    answered = sum(1 for key, value in facts.items() if key != "problem" and value != "not sure")
    top = round(ranked[0][1] * 100) if ranked else 0

    st.header("Investigation results")
    st.write(
        "The diagnosis in plain language, the reasoning behind it, "
        "and the changes waiting for your approval."
    )
    st.caption(f"{report['label']} \u00b7 {report['id']} \u00b7 {report['time']}")
    st.markdown(chips(facts), unsafe_allow_html=True)

    if ranked:
        summary = (
            f"Strongest recommendation: {ranked[0][0]}. "
            f"{len(ranked)} change(s) were derived from {len(fired)} rule(s)."
        )
    else:
        summary = "No rule matched the information supplied, so no change is recommended."
    st.markdown(
        '<div class="meter">'
        '<div class="meter-head"><span class="meter-label">TOP CONFIDENCE</span>'
        f'<span class="meter-value">{top}<small>/100</small></span></div>'
        f'<div class="meter-track"><div class="meter-fill" style="width: {top}%"></div></div>'
        f"<p>{summary}</p></div>",
        unsafe_allow_html=True,
    )

    if not ranked:
        st.header("No matching rule found")
        st.write(
            f"The engine examined {answered} observation(s) and could not derive a finding. "
            "Either the answers do not describe a known problem, "
            "or an important answer is marked Not sure."
        )
        return

    st.header(f"{pretty(facts['problem'])} diagnosed")
    st.write(f"The engine examined {answered} observation(s) and fired {len(fired)} rule(s).")

    touched = {}
    for fix, _ in ranked:
        for part in parts_for(fix):
            touched.setdefault(part, []).append(fix)
    st.subheader("Where to look")
    left, right = st.columns(2)
    left.markdown(car_svg(touched), unsafe_allow_html=True)
    if touched:
        right.markdown("\n".join(f"- **{NAMES[part]}**: {', '.join(fixes)}" for part, fixes in touched.items()))
    else:
        right.write("These changes are about driving technique, not car parts.")

    st.subheader("Recommended changes")
    st.caption("Tick the changes you accept to build your setup sheet.")
    accepted = []
    for number, (fix, cf) in enumerate(ranked):
        with st.container(border=True, key=f"card_{prefix}_{number}"):
            if st.checkbox(f"**{fix}**", key=f"{prefix}_{report['id']}_{fix}"):
                accepted.append((fix, cf))
            st.progress(cf, text=f"{cf:.0%} confidence, {strength(cf)}")
            with st.expander("Why this recommendation"):
                for rule in fired:
                    if rule["fix"] == fix:
                        st.markdown(f"**{rule['id']}**, rule confidence {rule['cf']:.2f}")
                        st.write(rule["why"])
                        st.caption(" AND ".join(f"{k} = {v}" for k, v in rule["if"].items()))
    if accepted:
        sheet = build_sheet(facts, accepted, fired)
        st.subheader("Setup sheet")
        st.code(sheet, language=None, wrap_lines=True)
        st.download_button(
            "Download setup sheet", sheet, file_name="setup_sheet.txt", key=f"{prefix}_download"
        )


home_tab, investigate_tab, scenario_tab = st.tabs(["Home", "Investigate", "Scenarios"])

with home_tab:
    st.markdown(
        '<div class="hero">'
        '<div class="eyebrow">RULE-BASED EXPERT SYSTEM</div>'
        "<h1>F1 Setup Doctor</h1>"
        "<p>A virtual race engineer for sim racers. Describe the handling problem, "
        "read the diagnosis in plain language, accept the changes you agree with, "
        "and download a written setup sheet.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.header("What it does")
    cards = [
        ("Diagnose", f"Checks your answers against {len(RULES)} IF-THEN rules and ranks the setup changes by confidence."),
        ("Explain", "Shows the exact rules behind every recommendation, with the reason in plain words."),
        ("Plan", "Lets you accept the changes you agree with and download them as a setup sheet."),
    ]
    for title, text in cards:
        with st.container(border=True, key=f"card_home_{title}"):
            st.subheader(title)
            st.write(text)

    st.header("What is inside")
    used_facts = {key for rule in RULES for key in rule["if"]}
    stats = [
        ("Rules", len(RULES)),
        ("Conditions", sum(len(rule["if"]) for rule in RULES)),
        ("Facts", len(used_facts)),
        ("Categories", len({rule["category"] for rule in RULES})),
        ("Scenarios", len(SCENARIOS)),
    ]
    for column, (label, value) in zip(st.columns(len(stats)), stats):
        column.metric(label, value)

    st.header("How it works")
    st.markdown(
        "1. **Describe** what the car is doing.\n"
        "2. **Read the diagnosis** with a confidence for every change.\n"
        "3. **Review and accept** the changes you agree with.\n"
        "4. **Download the plan** as a setup sheet."
    )
    st.caption("Forward chaining, certainty factors, Python and Streamlit.")

with investigate_tab:
    st.header("Investigate")
    st.write(
        "Enter what you observed. Not sure means the fact is unknown, "
        "and a rule that needs it will not fire."
    )
    chip_box = st.container()
    problem = st.selectbox("Main problem", list(QUESTIONS), format_func=pretty)
    facts = {"problem": problem}
    with st.expander(f"{pretty(problem)} details", expanded=True):
        for key, (text, options) in QUESTIONS[problem].items():
            widget_key = f"inv_{problem}_{key}"
            facts[key] = reading(key, widget_key) if key in READINGS else ask(text, options, widget_key)
    with st.expander("Track and car conditions", expanded=True):
        track = st.selectbox("Track", ["Not sure"] + list(TRACKS), key="inv_track")
        facts["track"] = TRACKS.get(track, "not sure")
        if track in TRACKS:
            st.caption(f"Treated as a {pretty(TRACKS[track]).lower()} track.")
        for key, (text, options) in COMMON.items():
            facts[key] = ask(text, options, f"inv_{key}")
    chip_box.markdown(chips(facts), unsafe_allow_html=True)
    if st.button("Run investigation", type="primary", width="stretch", key="inv_run"):
        st.session_state["inv_report"] = new_report(facts, "Manual investigation")
    if "inv_report" in st.session_state:
        show_report(st.session_state["inv_report"], "inv")

with scenario_tab:
    st.header("Scenario laboratory")
    st.write(
        "Six ready-made investigations. Each supplies observations only. "
        "The diagnosis comes from the same engine used in Investigate."
    )
    choice = st.selectbox("Scenario", list(SCENARIOS))
    scenario = SCENARIOS[choice]
    st.subheader(choice)
    st.write(scenario["description"])
    questions = {**QUESTIONS[scenario["facts"]["problem"]], **COMMON, "track": ("Track type",)}
    with st.expander("Observations in this scenario", expanded=True):
        lines = []
        for key, value in scenario["facts"].items():
            label = "Main problem" if key == "problem" else questions[key][0]
            lines.append(f"- {label} **{pretty(value)}**")
        st.markdown("\n".join(lines))
    if st.button("Run scenario", type="primary", width="stretch", key="scn_run"):
        st.session_state["scn_report"] = new_report(scenario["facts"], f"Scenario {choice[:6]}")
    if "scn_report" in st.session_state:
        show_report(st.session_state["scn_report"], "scn")