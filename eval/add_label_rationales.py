import json
from pathlib import Path

DATASET_FILE = (
    Path(__file__).resolve().parent / "labelled_scenarios.json"
)

RATIONALES = {
    "normal_payment":
        "No risk signals are present in this synthetic test.",
    "first_time_payee_only":
        "A first-time payee alone is treated as normal for this test.",
    "phone_call_only":
        "Being on a phone call alone is not assumed to indicate payment risk.",
    "call_and_new_payee":
        "A phone call and first-time payee occur together; the test assumes caution is warranted.",
    "remote_access_and_new_payee":
        "Remote access and a first-time payee occur together; the test treats this combination as risky.",
    "mule_payee_and_phone_call":
        "A simulated mule-list match combined with a phone call is treated as risky.",
    "collect_request_only":
        "The test assumes a collect request warrants caution, although a collect request alone does not prove fraud.",
    "three_independent_risk_families":
        "Signals from multiple independent risk families are assumed to warrant caution.",
    "screen_sharing_and_collect_request":
        "Screen sharing and a collect request occur together, so the test labels the scenario risky.",
    "multiple_behavior_signals_same_family":
        "Several unusual behavioural signals are assumed to warrant caution, even though they belong to one family.",
    "missing_signals":
        "No signals are supplied, so the scenario is labelled normal for this test.",
    "conflicting_low_and_high_vpa_context":
        "A high VPA lookalike score combined with other risk signals is treated as risky.",
    "numeric_threshold_boundary":
        "The scenario combines signals that cross configured behavioural thresholds with a phone call.",
    "vpa_score_just_below_threshold":
        "The VPA lookalike score is below the configured 0.7 threshold and no other signals are present.",
    "amount_score_just_below_threshold":
        "The amount z-score is below the configured threshold of 2 and no other signals are present.",
    "single_payment_retry":
        "One retry is below the configured retry threshold of 2.",
    "remote_access_without_other_signals":
        "The test assumes active remote access warrants caution on its own; this does not establish fraud.",
    "mule_payee_without_other_signals":
        "The test assumes a simulated mule-list match warrants caution on its own.",
    "recent_sim_change_alone":
        "The test assumes a recent device or SIM change warrants caution on its own.",
    "screen_sharing_without_other_signals":
        "The test assumes active screen sharing warrants caution on its own.",
    "several_signals_from_behaviour_family":
        "The test assumes several unusual behavioural signals can still describe a legitimate payment.",
    "remote_access_and_screen_sharing_only":
        "The test assumes these two device-related signals without other context are not sufficient to label the payment risky.",
    "multiple_signals_with_benign_context":
        "The test assumes a legitimate context despite multiple signals; the supplied signals alone cannot verify that context.",
    "call_and_recent_sim_change":
        "A phone call and recent device or SIM change occur together and are assumed to warrant caution.",
    "new_payee_and_high_vpa_lookalike_score":
        "A first-time payee and high VPA lookalike score occur together and are assumed to warrant caution."
}


def main():
    with open(DATASET_FILE, "r", encoding="utf-8") as file:
        scenarios = json.load(file)

    missing = [
        scenario["name"]
        for scenario in scenarios
        if scenario["name"] not in RATIONALES
    ]

    if missing:
        raise ValueError(
            f"Missing rationales for scenarios: {missing}"
        )

    for scenario in scenarios:
        scenario["label_rationale"] = RATIONALES[scenario["name"]]

    with open(DATASET_FILE, "w", encoding="utf-8") as file:
        json.dump(scenarios, file, indent=2)
        file.write("\n")

    print(f"Updated {len(scenarios)} scenarios with rationales.")
    print("Existing labels and signals were preserved.")


if __name__ == "__main__":
    main()