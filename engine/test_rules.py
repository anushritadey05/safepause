
from engine.rules import score_rules

# Test 1: Normal payment → GREEN
normal = {
    "on_call": False,
    "remote_access_active": False,
    "payee_first_time": False,
    "payee_on_mule_list": False,
}

# Test 2: Phone call + first-time payee → AMBER
amber_payment = {
    "on_call": True,
    "remote_access_active": False,
    "payee_first_time": True,
    "payee_on_mule_list": False,
}

# Test 3: Multiple risk signals → RED
risky = {
    "on_call": True,
    "remote_access_active": True,
    "payee_first_time": True,
    "payee_on_mule_list": True,
}


# Check GREEN
green_result = score_rules(normal)
assert green_result["tier"] == "GREEN"
assert green_result["active_families"] == []
assert green_result["reasons"] == ["No strong risk pattern was detected."]

# Check AMBER
amber_result = score_rules(amber_payment)
assert amber_result["tier"] == "AMBER"
assert "Call" in amber_result["active_families"]
assert "Payee" in amber_result["active_families"]
assert any("new payee" in reason for reason in amber_result["reasons"])

# Check RED
red_result = score_rules(risky)
assert red_result["tier"] == "RED"
assert len(red_result["active_families"]) >= 3
assert red_result["hard_signal"] is True

assert green_result["simulation_only"] is True
assert amber_result["simulation_only"] is True
assert red_result["simulation_only"] is True


print("GREEN test passed!")
print("AMBER test passed!")
print("RED test passed!")
print("All risk-tier tests passed!")
