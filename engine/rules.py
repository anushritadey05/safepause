def score_rules(signals):
    """
    Classify a simulated payment as GREEN, AMBER, or RED.

    This is a prototype rule engine, not a real banking fraud detector.
    """

    families = []
    reasons = []

    # 1. Identify independent risk families.
    if signals.get("on_call"):
        families.append("Call")

    if (
        signals.get("remote_access_active")
        or signals.get("screen_share_active")
    ):
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

    # 2. Identify individual signals that warrant caution.
    individual_warning = (
        signals.get("remote_access_active")
        or signals.get("screen_share_active")
        or signals.get("device_or_sim_change_72h")
        or signals.get("payee_on_mule_list")
        or signals.get("vpa_lookalike_score", 0) >= 0.7
    )

    # 3. Identify combinations that deserve extra caution.
    hard_signal = (
        (
            signals.get("payee_on_mule_list")
            and signals.get("on_call")
        )
        or (
            signals.get("remote_access_active")
            and signals.get("payee_first_time")
        )
        or (
            signals.get("payee_first_time")
            and signals.get("vpa_lookalike_score", 0) >= 0.7
        )
    )

    # 4. Assign the risk tier.
    behavior_warning = (
        signals.get("is_collect", False)
        or (
            signals.get("hour_odd", False)
            and signals.get("retry_count", 0) >= 2
        )
    )

    if len(families) >= 3 or hard_signal:
        tier = "RED"
    elif len(families) >= 2 or individual_warning:
        tier = "AMBER"
    elif behavior_warning:
        tier = "AMBER"
    else:
        tier = "GREEN"

    



    # 5. Explain the decision.
    if signals.get("on_call") and signals.get("payee_first_time"):
        reasons.append(
            "You are on a call while paying a new payee."
        )

    if signals.get("remote_access_active"):
        reasons.append(
            "A remote-access signal is active (simulated)."
        )

    if signals.get("screen_share_active"):
        reasons.append(
            "A screen-sharing signal is active (simulated)."
        )

    if signals.get("payee_on_mule_list"):
        reasons.append(
            "The payee appears on the simulated mule list."
        )

    if (
        signals.get("payee_first_time")
        and signals.get("vpa_lookalike_score", 0) >= 0.7
    ):
        reasons.append(
            "A new payee has a high VPA lookalike score."
        )

    if signals.get("device_or_sim_change_72h"):
        reasons.append(
            "A recent device or SIM change was detected (simulated)."
        )

    if signals.get("is_collect"):
        reasons.append(
            "Verify why you are being asked to approve this collect request."
        )

    if not reasons:
        reasons.append("No strong risk pattern was detected.")

    return {
        "tier": tier,
        "active_families": families,
        "hard_signal": bool(hard_signal),
        "reasons": reasons[:3],
        "simulation_only": True,
    }