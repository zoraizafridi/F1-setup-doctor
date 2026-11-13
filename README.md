# F1 Setup Doctor

A rule-based expert system that diagnoses Formula 1 car handling problems and recommends setup changes. The user describes a problem (for example understeer in a slow corner), the system asks follow-up questions, chains the answers through a knowledge base of 80 rules, and returns ranked fixes with a confidence value and an explanation for each.

The interface is built with Streamlit.

## Features

- **Guided investigation.** Pick a main problem, answer a short set of questions, and run the diagnosis.
- **Rule base of 80 rules** across nine categories: Understeer, Oversteer, Tyres, Braking, Traction, Straights, Kerbs, Cross-check and Track.
- **Certainty factors.** Each rule carries a confidence value (`cf`) so recommendations can be ranked.
- **Explanations.** Every recommended fix shows the rule that fired and why.
- **Numeric readings.** Sliders for tyre temperature and brake disc temperature are converted into facts before the rules run.
- **Track presets.** Nine circuits mapped to high, medium or low downforce, which feed the track-specific rules.
- **Top-down car diagram.** The parts affected by the recommended fixes are highlighted on an SVG car.
- **Status chips.** A summary row of the current situation (problem, conditions, track type).
- **Scenario laboratory.** Six ready-made cases that run the engine without answering questions by hand.

## Project structure

| File | Purpose |
|---|---|
| `app.py` | Streamlit interface: Home, Investigate and Scenarios tabs |
| `engine.py` | Inference engine: matches facts against rules and returns the diagnosis |
| `rules.py` | The knowledge base: the `RULES` list (R01 to R80) |
| `questions.py` | Questions per problem, numeric readings, track presets and test scenarios |
| `car.py` | Maps fixes to car parts and draws the SVG car diagram |

## Rule format

Each rule is a dictionary in `rules.py`:

```python
{"id": "R72", "category": "Track",
 "if": {"problem": "understeer", "track": "high_downforce"},
 "fix": "Increase front wing angle", "cf": 0.7,
 "why": "On a high-downforce track more front wing costs little lap time and adds grip at the front."}
```

A rule fires when every condition in `if` matches the current facts. To add knowledge, append a new dictionary to the end of `RULES` with the next unused id.

## Getting started

Requirements: Python 3.9 or newer.

```bash
pip install streamlit
streamlit run app.py
```

The app opens in your browser at `http://localhost:8501`.

## Usage

1. Open the **Investigate** tab.
2. Choose the main problem and, optionally, a track.
3. Answer the questions and adjust the temperature sliders.
4. Click **Run investigation** to see the ranked fixes, the explanations and the highlighted car parts.

To see the system work without entering anything, open the **Scenarios** tab, choose a case and click **Run scenario**.

## Scenarios

| ID | Case |
|---|---|
| SCN-01 | Understeer at a slow hairpin |
| SCN-02 | Oversteer on corner entry |
| SCN-03 | Rear locking under braking |
| SCN-04 | Wheelspin in the wet |
| SCN-05 | Low top speed at Monza |
| SCN-06 | Bottoming out over kerbs at Monaco |

## Notes

The recommendations are a simplified teaching model and are not real engineering advice for a race car.