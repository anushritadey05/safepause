import json
from pathlib import Path

from engine.rules import score_rules


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_FILE = PROJECT_ROOT / "eval" / "labelled_scenarios.json"


def predict_label(signals):
    """Convert the three risk tiers into a binary prediction."""
    result = score_rules(signals)

    if result["tier"] in ("AMBER", "RED"):
        return "RISKY"

    return "NORMAL"


def main():
    with open(DATASET_FILE, "r", encoding="utf-8") as file:
        scenarios = json.load(file)

    tp = 0
    tn = 0
    fp = 0
    fn = 0

    false_positives = []
    false_negatives = []

    print("\nSafePause Binary Classification Evaluation")
    print("=" * 55)

    for scenario in scenarios:
        name = scenario["name"]
        actual = scenario["expected_label"]
        predicted = predict_label(scenario["signals"])

        if actual == "RISKY" and predicted == "RISKY":
            tp += 1
        elif actual == "NORMAL" and predicted == "NORMAL":
            tn += 1
        elif actual == "NORMAL" and predicted == "RISKY":
            fp += 1
            false_positives.append(name)
        elif actual == "RISKY" and predicted == "NORMAL":
            fn += 1
            false_negatives.append(name)

        status = "PASS" if actual == predicted else "MISS"

        print(
            f"{status} | {name} | "
            f"Actual: {actual} | Predicted: {predicted}"
        )

    total = len(scenarios)
    accuracy = (tp + tn) / total if total else 0
    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0

    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall
        else 0
    )

    print("\nConfusion Matrix")
    print("-" * 35)
    print("                 Predicted")
    print("              NORMAL   RISKY")
    print(f"Actual NORMAL    {tn:3}      {fp:3}")
    print(f"Actual RISKY     {fn:3}      {tp:3}")

    print("\nMetrics")
    print("-" * 35)
    print(f"Total scenarios: {total}")
    print(f"Accuracy:  {accuracy:.2%}")
    print(f"Precision: {precision:.2%}")
    print(f"Recall:    {recall:.2%}")
    print(f"F1 score:  {f1:.2%}")

    print("\nFalse Positives")
    print("-" * 35)
    if false_positives:
        for name in false_positives:
            print(f"- {name}")
    else:
        print("None")

    print("\nFalse Negatives")
    print("-" * 35)
    if false_negatives:
        for name in false_negatives:
            print(f"- {name}")
    else:
        print("None")

    print("\nNote: Labels are synthetic and manually assigned.")
    print("AMBER and RED are both counted as predicted RISKY.")


if __name__ == "__main__":
    main()