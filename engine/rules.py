
def score_rules(signals):
    """
    Classify a simulated UPI payment as GREEN, AMBER, or RED.
    This is a prototype rule engine, not a real banking fraud detector.
    """

    families = []
    reasons = []

    # 1. Identify independent risk families
    if signals.get("on_call"):
        families.append("Call")

    if signals.get("remote_access_active") or signals.get("screen_share_active"):
        families.append("Device")

    if (
        signals.get("payee_first_time")
        or signals.get("payee_on_mule_list")
        or signals.get("vpa_lookalike_score", 0) >= 0.7
    ):
        families.append("Payee")

    if (
        signals.get("is_collect")
        or signals.get("hour_odd")
        or signals.get("amount_zscore", 0) >= 2
        or signals.get("retry_count", 0) >= 2
    ):
        families.append("Behaviour")

    if signals.get("device_or_sim_change_72h"):
        families.append("Account")

    # 2. Detect combinations that deserve extra caution
    hard_signal = (
        (signals.get("payee_on_mule_list") and signals.get("on_call"))
        or (
            signals.get("remote_access_active")
            and signals.get("payee_first_time")
        )
    )

    # 3. Assign the risk tier
    if len(families) >= 3 or (hard_signal and len(families) >= 2):
        tier = "RED"
    elif len(families) >= 2:
        tier = "AMBER"
    else:
        tier = "GREEN"

    # 4. Explain the decision in simple language
    if signals.get("on_call") and signals.get("payee_first_time"):
        reasons.append("You are on a call while paying a new payee.")

    if signals.get("remote_access_active") or signals.get("screen_share_active"):
        reasons.append("A remote-access or screen-sharing signal is active (simulated).")

    if signals.get("payee_on_mule_list"):
        reasons.append("The payee appears on the simulated mule list.")

    if signals.get("is_collect"):
        reasons.append("Verify why you are being asked to approve this collect request.")

    if not reasons:
        reasons.append("No strong risk pattern was detected.")

    return {
        "tier": tier,
        "active_families": families,
        "hard_signal": bool(hard_signal),
        "reasons": reasons[:3],
        "simulation_only": True,
    }
