import json
from math import sqrt
FILE_NAME="/home/arjun/correlation/journal.json"

def load_journal(FILE_NAME):
    with open(FILE_NAME, 'r') as file:
        return json.load(file)

def compute_phi(journal, event):
    n11 = n00 = n10 = n01 = n1p = n0p = np1 = np0 = 0

    for entry in journal:
        squirrel = entry['squirrel']
        event_present = event in entry['events']

        if squirrel and event_present:
            n11 += 1
            n1p += 1  
        elif not squirrel and not event_present:
            n00 += 1
            n0p += 1 
        elif squirrel and not event_present:
            n10 += 1
            n1p += 1  
        elif not squirrel and event_present:
            n01 += 1
            n0p += 1  

        if squirrel:
            np1 += 1
        if event_present:
            np0 += 1

    if n1p == 0 or n0p == 0 or np1 == 0 or np0 == 0:
        return 0.0

    phi = (n11 * n00 - n10 * n01) / sqrt(n1p * n0p * np1 * np0)
    return phi

def compute_correlations(FILE_NAME):
    journal = load_journal(FILE_NAME)
    correlations = {}

    for entry in journal:
        for event in entry['events']:
            if event != 'squirrel' and event not in correlations:
                correlations[event] = compute_phi(journal, event)

    return correlations

def diagnose(FILE_NAME):
    correlations = compute_correlations(FILE_NAME)

    most_positive = max(correlations, key=correlations.get)
    most_negative = min(correlations, key=correlations.get)

    print(f"\nMost Correlated Activity: {most_positive} (Correlation: {correlations[most_positive]:.2f})")
    print(f"\nLeast Correlated Activity: {most_negative} (Correlation: {correlations[most_negative]:.2f})")

    if correlations[most_positive] > 0.5:
        advice_positive = f"Avoid {most_positive} for not transforming."
        print(f"\n Advice: {advice_positive}\n")
    else:
        advice_positive = f"Increase {most_positive} for not transforming."
        print(f"\n Advice: {advice_positive}\n")

diagnose(FILE_NAME)
