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


def diagnose_many(fact_sets):
    results = {}
    fired = []
    seen = set()
    for facts in fact_sets:
        _, rules_fired = diagnose(facts)
        for rule in rules_fired:
            if rule["id"] in seen:
                continue
            seen.add(rule["id"])
            fired.append(rule)
            results[rule["fix"]] = combine(results.get(rule["fix"], 0), rule["cf"])
    return results, fired