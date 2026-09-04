from src.maintenance_alerts import MaintenanceAlerts


alerts = MaintenanceAlerts()


print("\n========== MAINTENANCE ALERT TESTS ==========")


# Test 1: Critical
critical_result = alerts.generate_alert(
    health_score=35,
    health_status="Critical",
    prediction_result={
        "failure_prediction": 1,
        "failure_probability": 85.0
    }
)

print("\n--- CRITICAL CASE ---")
for key, value in critical_result.items():
    print(f"{key}: {value}")


# Test 2: High
high_result = alerts.generate_alert(
    health_score=55,
    health_status="Poor",
    prediction_result={
        "failure_prediction": 0,
        "failure_probability": 50.0
    }
)

print("\n--- HIGH RISK CASE ---")
for key, value in high_result.items():
    print(f"{key}: {value}")


# Test 3: Medium
medium_result = alerts.generate_alert(
    health_score=75,
    health_status="Warning",
    prediction_result={
        "failure_prediction": 0,
        "failure_probability": 20.0
    }
)

print("\n--- MEDIUM RISK CASE ---")
for key, value in medium_result.items():
    print(f"{key}: {value}")


# Test 4: Low
low_result = alerts.generate_alert(
    health_score=95,
    health_status="Healthy",
    prediction_result={
        "failure_prediction": 0,
        "failure_probability": 2.0
    }
)

print("\n--- LOW RISK CASE ---")
for key, value in low_result.items():
    print(f"{key}: {value}")