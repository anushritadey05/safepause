
import json
from pathlib import Path

from engine.rules import score_rules


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCENARIOS_FILE = PROJECT_ROOT / "sim" / "scenarios.json"

VALID_TIERS = {"GREEN", "AMBER", "RED"}


def run_evaluation():
    with open(SCENARIOS_FILE, "r", encoding="utf-8") as file:
        scenarios = json.load(file)

    passed = 0
    failed = 0

    tier_counts = {
        "GREEN": 0,
        "AMBER": 0,
        "RED": 0,
    }

    print("\nSafePause Risk Engine Evaluation")
    print("=" * 40)

    for scenario in scenarios:
        name = scenario["name"]
        signals = scenario["signals"]
        expected = scenario["expected_tier"]

        result = score_rules(signals)
        actual = result["tier"]

        if actual in tier_counts:
            tier_counts[actual] += 1

        checks = {
            "expected_tier": actual == expected,
            "valid_tier": actual in VALID_TIERS,
            "active_families_is_list": isinstance(
                result.get("active_families"), list
            ),
            "has_readable_reason": (
                isinstance(result.get("reasons"), list)
                and len(result["reasons"]) > 0
                and all(
                    isinstance(reason, str) and reason.strip()
                    for reason in result["reasons"]
                )
            ),
            "simulation_only": result.get("simulation_only") is True,
        }

        scenario_passed = all(checks.values())

        if scenario_passed:
            passed += 1
            status = "PASS"
        else:
            failed += 1
            status = "FAIL"

        print(
            f"{status} | {name} | "
            f"Expected: {expected} | Actual: {actual}"
        )

        for check_name, check_passed in checks.items():
            if not check_passed:
                print(f"  Failed check: {check_name}")

    total = len(scenarios)
    agreement = (
        sum(
            1 for scenario in scenarios
            if score_rules(scenario["signals"])["tier"]
            == scenario["expected_tier"]
        ) / total * 100
        if total else 0
    )

    print("=" * 40)
    print(f"Total scenarios: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Tier agreement: {agreement:.1f}%")

    print("\nRisk-tier distribution:")
    for tier, count in tier_counts.items():
        print(f"{tier}: {count}")

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    run_evaluation()
