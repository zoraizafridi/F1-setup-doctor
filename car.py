NAMES = {
    "front_wing": "Front wing",
    "rear_wing": "Rear wing",
    "front_axle": "Front axle",
    "rear_axle": "Rear axle",
    "brakes": "Brakes",
    "differential": "Differential and gearbox",
}

KEYWORDS = [
    (["front wing"], ["front_wing"]),
    (["rear wing"], ["rear_wing"]),
    (["brak"], ["brakes"]),
    (["differential", "gear"], ["differential"]),
    (["front"], ["front_axle"]),
    (["rear"], ["rear_axle"]),
    (["suspension", "ride height", "pressure", "camber"], ["front_axle", "rear_axle"]),
]

SHAPES = [
    ("front_wing", "rect", 'x="30" y="16" width="140" height="14" rx="3"'),
    ("rear_wing", "rect", 'x="34" y="298" width="132" height="16" rx="3"'),
    ("front_axle", "rect", 'x="64" y="94" width="72" height="4"'),
    ("rear_axle", "rect", 'x="64" y="261" width="72" height="4"'),
    ("body", "polygon", 'points="106,30 114,110 120,170 118,230 114,290 86,290 82,230 80,170 86,110 94,30"'),
    ("body", "ellipse", 'cx="100" cy="175" rx="10" ry="18"'),
    ("front_axle", "rect", 'x="40" y="70" width="24" height="52" rx="6"'),
    ("front_axle", "rect", 'x="136" y="70" width="24" height="52" rx="6"'),
    ("rear_axle", "rect", 'x="32" y="232" width="32" height="62" rx="7"'),
    ("rear_axle", "rect", 'x="136" y="232" width="32" height="62" rx="7"'),
    ("differential", "rect", 'x="90" y="250" width="20" height="26" rx="4"'),
    ("brakes", "circle", 'cx="52" cy="96" r="6"'),
    ("brakes", "circle", 'cx="148" cy="96" r="6"'),
    ("brakes", "circle", 'cx="48" cy="263" r="6"'),
    ("brakes", "circle", 'cx="152" cy="263" r="6"'),
]


def parts_for(fix):
    text = fix.lower()
    for words, parts in KEYWORDS:
        if any(word in text for word in words):
            return parts
    return []


def car_svg(active):
    shapes = "".join(
        f'<{tag} class="{"on" if part in active else "off"}" {attrs}/>'
        for part, tag, attrs in SHAPES
    )
    return f'<div class="car"><svg viewBox="0 0 200 330" xmlns="http://www.w3.org/2000/svg">{shapes}</svg></div>'