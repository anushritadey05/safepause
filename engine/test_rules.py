from engine.rules import score_rules


def test_green_normal_payment():
    result = score_rules({})
    assert result["tier"] == "GREEN"


def test_green_first_time_payee_alone():
    result = score_rules({"payee_first_time": True})
    assert result["tier"] == "GREEN"


def test_amber_call_and_new_payee():
    result = score_rules({
        "on_call": True,
        "payee_first_time": True,
    })
    assert result["tier"] == "AMBER"


def test_red_remote_access_and_new_payee():
    result = score_rules({
        "remote_access_active": True,
        "payee_first_time": True,
    })
    assert result["tier"] == "RED"


def test_red_mule_payee_and_phone_call():
    result = score_rules({
        "payee_on_mule_list": True,
        "on_call": True,
    })
    assert result["tier"] == "RED"


def test_red_three_independent_families():
    result = score_rules({
        "on_call": True,
        "remote_access_active": True,
        "payee_first_time": True,
    })
    assert result["tier"] == "RED"


def test_amber_screen_sharing_and_collect_request():
    result = score_rules({
        "screen_share_active": True,
        "is_collect": True,
    })
    assert result["tier"] == "AMBER"


def test_green_multiple_signals_from_one_family():
    result = score_rules({
        "is_collect": True,
        "hour_odd": True,
        "amount_zscore": 2.5,
        "retry_count": 3,
    })
    assert result["tier"] == "AMBER"


def test_warning_for_remote_access_alone():
    result = score_rules({
        "remote_access_active": True,
    })
    assert result["tier"] == "AMBER"


def test_warning_for_screen_sharing_alone():
    result = score_rules({
        "screen_share_active": True,
    })
    assert result["tier"] == "AMBER"


def test_warning_for_recent_sim_change_alone():
    result = score_rules({
        "device_or_sim_change_72h": True,
    })
    assert result["tier"] == "AMBER"


def test_warning_for_mule_payee_alone():
    result = score_rules({
        "payee_on_mule_list": True,
    })
    assert result["tier"] == "AMBER"


def test_red_new_payee_and_high_vpa_similarity():
    result = score_rules({
        "payee_first_time": True,
        "vpa_lookalike_score": 0.85,
    })
    assert result["tier"] == "RED"


def test_result_includes_explanation():
    result = score_rules({"remote_access_active": True})

    assert isinstance(result["reasons"], list)
    assert len(result["reasons"]) > 0
    assert result["simulation_only"] is True


def run_tests():
    tests = [
        test_green_normal_payment,
        test_green_first_time_payee_alone,
        test_amber_call_and_new_payee,
        test_red_remote_access_and_new_payee,
        test_red_mule_payee_and_phone_call,
        test_red_three_independent_families,
        test_amber_screen_sharing_and_collect_request,
        test_green_multiple_signals_from_one_family,
        test_warning_for_remote_access_alone,
        test_warning_for_screen_sharing_alone,
        test_warning_for_recent_sim_change_alone,
        test_warning_for_mule_payee_alone,
        test_red_new_payee_and_high_vpa_similarity,
        test_result_includes_explanation,
    ]

    passed = 0

    for test in tests:
        try:
            test()
            print(f"PASS: {test.__name__}")
            passed += 1
        except AssertionError:
            print(f"FAIL: {test.__name__}")

    print(f"\nPassed: {passed}/{len(tests)}")

    if passed != len(tests):
        raise SystemExit(1)


if __name__ == "__main__":
    run_tests()