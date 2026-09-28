import sys
import importlib
from pathlib import Path


# ==================================================
# PROJECT PATHS
# ==================================================

CURRENT_DIR = Path(__file__).resolve().parent

# smart_facility_system folder
SMART_SYSTEM_PATH = CURRENT_DIR.parent

# Springboard folder
SPRINGBOARD_PATH = SMART_SYSTEM_PATH.parent

# Milestone 1
ENERGY_PROJECT_PATH = (
    SPRINGBOARD_PATH / "M1_agentic_facilityops_ai"
)

# Milestone 2
MAINTENANCE_PROJECT_PATH = (
    SPRINGBOARD_PATH / "M2_Predictive_Maintenance"
)


# ==================================================
# REMOVE PREVIOUS SRC IMPORTS
# ==================================================

def clear_src_modules():

    modules_to_remove = []

    for module_name in sys.modules:

        if (
            module_name == "src"
            or module_name.startswith("src.")
        ):
            modules_to_remove.append(
                module_name
            )

    for module_name in modules_to_remove:

        del sys.modules[
            module_name
        ]


# ==================================================
# IMPORT ENERGY AGENT
# ==================================================

def import_energy_agent():

    clear_src_modules()

    if str(ENERGY_PROJECT_PATH) in sys.path:

        sys.path.remove(
            str(ENERGY_PROJECT_PATH)
        )

    sys.path.insert(
        0,
        str(ENERGY_PROJECT_PATH)
    )

    module = importlib.import_module(
        "src.energy_agent"
    )

    return module.EnergyAgent


# ==================================================
# IMPORT MAINTENANCE AGENT
# ==================================================

def import_maintenance_agent():

    clear_src_modules()

    if str(MAINTENANCE_PROJECT_PATH) in sys.path:

        sys.path.remove(
            str(MAINTENANCE_PROJECT_PATH)
        )

    sys.path.insert(
        0,
        str(MAINTENANCE_PROJECT_PATH)
    )

    module = importlib.import_module(
        "src.maintenance_agent"
    )

    return module.MaintenanceAgent


# ==================================================
# PYTEST TESTS
# ==================================================

def test_energy_agent_import():

    EnergyAgent = import_energy_agent()

    assert EnergyAgent is not None

    assert EnergyAgent.__name__ == "EnergyAgent"


def test_maintenance_agent_import():

    MaintenanceAgent = import_maintenance_agent()

    assert MaintenanceAgent is not None

    assert MaintenanceAgent.__name__ == "MaintenanceAgent"


# ==================================================
# MANUAL TEST
# ==================================================

if __name__ == "__main__":

    print(
        "\n========== PROJECT PATHS =========="
    )

    print(
        f"Energy Project: "
        f"{ENERGY_PROJECT_PATH}"
    )

    print(
        f"Maintenance Project: "
        f"{MAINTENANCE_PROJECT_PATH}"
    )

    EnergyAgent = import_energy_agent()

    MaintenanceAgent = import_maintenance_agent()

    print(
        "\n========== IMPORT TEST COMPLETED =========="
    )

    print(
        "Both agents were imported successfully!"
    )

    print(
        "\nEnergy Agent Class:"
    )

    print(EnergyAgent)

    print(
        "\nMaintenance Agent Class:"
    )

    print(MaintenanceAgent)