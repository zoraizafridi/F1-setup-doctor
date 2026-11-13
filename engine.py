from rules import RULES


def combine(a, b):
    return a + b * (1 - a)


def diagnose(facts):
    results = {}
    fired = []
    for rule in RULES:
        if all(facts.get(key) == value for key, value in rule["if"].items()):
            fired.append(rule)
            old = results.get(rule["fix"], 0)
            results[rule["fix"]] = combine(old, rule["cf"])
    return results, fired