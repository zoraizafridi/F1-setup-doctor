YES_NO = ["yes", "no"]
PHASE = ["entry", "mid", "exit"]
SPEED = ["slow", "medium", "fast"]

QUESTIONS = {
    "understeer": {
        "phase": ("Where in the corner does it happen?", PHASE),
        "speed": ("How fast is the corner?", SPEED),
        "front_hot": ("Are the front tyres overheating?", YES_NO),
    },
    "oversteer": {
        "phase": ("Where in the corner does it happen?", PHASE),
        "speed": ("How fast is the corner?", SPEED),
        "rear_hot": ("Are the rear tyres overheating?", YES_NO),
    },
    "braking": {
        "lockup": ("Which wheels lock under braking?", ["front", "rear", "none"]),
        "rear_unstable": ("Is the rear unstable while braking?", YES_NO),
        "brake_hot": ("Are the brakes overheating or fading?", YES_NO),
        "stops_late": ("Does the car take too long to stop?", YES_NO),
    },
    "traction": {
        "speed": ("How fast is the corner?", SPEED),
        "wheelspin": ("Is there wheelspin on throttle?", YES_NO),
        "power_snap": ("Does the rear snap on throttle?", YES_NO),
        "rear_hot": ("Are the rear tyres overheating?", YES_NO),
    },
    "tyres": {
        "tyre_issue": (
            "Which tyre problem do you see?",
            ["front_overheat", "rear_overheat", "front_wear", "rear_wear",
             "inner_wear", "outer_wear", "cold_tyres"],
        ),
    },
    "straight": {
        "straight_issue": (
            "What is wrong on the straights?",
            ["low_top_speed", "poor_acceleration", "unstable_at_speed"],
        ),
        "corner_grip": ("How is the grip in corners?", ["good", "poor"]),
    },
    "kerbs": {
        "kerb_issue": (
            "What happens over kerbs?",
            ["bouncing", "bottoming", "snap_over_kerb"],
        ),
    },
}

COMMON = {
    "weather": ("What are the track conditions?", ["dry", "wet"]),
    "fuel": ("What is the fuel load?", ["heavy", "light"]),
}

READINGS = {
    "front_hot": ("Front tyre temperature (°C)", 60, 140, 90, 105),
    "rear_hot": ("Rear tyre temperature (°C)", 60, 140, 90, 105),
    "brake_hot": ("Brake disc temperature (°C)", 300, 1100, 600, 800),
}

TRACKS = {
    "Monaco": "high_downforce",
    "Hungaroring": "high_downforce",
    "Singapore": "high_downforce",
    "Zandvoort": "high_downforce",
    "Mexico City": "high_downforce",
    "Silverstone": "medium_downforce",
    "Suzuka": "medium_downforce",
    "Barcelona": "medium_downforce",
    "Bahrain": "medium_downforce",
    "Melbourne": "medium_downforce",
    "Austin": "medium_downforce",
    "Interlagos": "medium_downforce",
    "Abu Dhabi": "medium_downforce",
    "Spa-Francorchamps": "low_downforce",
    "Monza": "low_downforce",
    "Baku": "low_downforce",
    "Montreal": "low_downforce",
    "Red Bull Ring": "low_downforce",
    "Jeddah": "low_downforce",
}

SCENARIOS = {
    "SCN-01 Understeer at a slow hairpin": {
        "description": "The car pushes wide in the middle of a slow hairpin. The fuel load is heavy and the front tyres are overheating.",
        "facts": {"problem": "understeer", "phase": "mid", "speed": "slow",
                  "front_hot": "yes", "weather": "dry", "fuel": "heavy"},
    },
    "SCN-02 Oversteer on corner entry": {
        "description": "The rear steps out as soon as the driver turns in for a slow corner, late in the race on a light fuel load.",
        "facts": {"problem": "oversteer", "phase": "entry", "speed": "slow",
                  "rear_hot": "no", "weather": "dry", "fuel": "light"},
    },
    "SCN-03 Rear locking under braking": {
        "description": "The rear wheels lock and the car feels unstable on the way into a heavy braking zone.",
        "facts": {"problem": "braking", "lockup": "rear", "rear_unstable": "yes",
                  "brake_hot": "no", "stops_late": "no", "weather": "dry", "fuel": "heavy"},
    },
    "SCN-04 Wheelspin in the wet": {
        "description": "Heavy wheelspin out of slow corners on a wet track, with the rear tyres running hot.",
        "facts": {"problem": "traction", "speed": "slow", "wheelspin": "yes",
                  "power_snap": "no", "rear_hot": "yes", "weather": "wet", "fuel": "heavy"},
    },
    "SCN-05 Low top speed at Monza": {
        "description": "The car is quick through the corners but loses time on the long straights of a low-downforce track.",
        "facts": {"problem": "straight", "straight_issue": "low_top_speed",
                  "corner_grip": "good", "track": "low_downforce",
                  "weather": "dry", "fuel": "light"},
    },
    "SCN-06 Bottoming out over kerbs at Monaco": {
        "description": "The floor scrapes the track every time the car rides a kerb on a high-downforce street circuit.",
        "facts": {"problem": "kerbs", "kerb_issue": "bottoming",
                  "track": "high_downforce", "weather": "dry", "fuel": "heavy"},
    },
}