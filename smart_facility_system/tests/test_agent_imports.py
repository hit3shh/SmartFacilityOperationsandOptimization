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
    """
    Removes previously imported modules starting with src.
    This prevents conflicts because both projects
    contain a package named 'src'.
    """

    modules_to_remove = []

    for module_name in sys.modules:
        if module_name == "src" or module_name.startswith("src."):
            modules_to_remove.append(module_name)

    for module_name in modules_to_remove:
        del sys.modules[module_name]


# ==================================================
# IMPORT ENERGY AGENT
# ==================================================

def import_energy_agent():

    print("\nTesting Energy Agent import...")

    # Clear previous src imports
    clear_src_modules()

    # Give priority to Milestone 1 project
    if str(ENERGY_PROJECT_PATH) in sys.path:
        sys.path.remove(str(ENERGY_PROJECT_PATH))

    sys.path.insert(
        0,
        str(ENERGY_PROJECT_PATH)
    )

    # Import Energy Agent
    module = importlib.import_module(
        "src.energy_agent"
    )

    EnergyAgent = module.EnergyAgent

    print(
        "Energy Agent imported successfully!"
    )

    return EnergyAgent


# ==================================================
# IMPORT MAINTENANCE AGENT
# ==================================================

def import_maintenance_agent():

    print("\nTesting Maintenance Agent import...")

    # Clear previous src imports
    clear_src_modules()

    # Give priority to Milestone 2 project
    if str(MAINTENANCE_PROJECT_PATH) in sys.path:
        sys.path.remove(
            str(MAINTENANCE_PROJECT_PATH)
        )

    sys.path.insert(
        0,
        str(MAINTENANCE_PROJECT_PATH)
    )

    # Import Maintenance Agent
    module = importlib.import_module(
        "src.maintenance_agent"
    )

    MaintenanceAgent = module.MaintenanceAgent

    print(
        "Maintenance Agent imported successfully!"
    )

    return MaintenanceAgent


# ==================================================
# MAIN TEST
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

    # ----------------------------------------------

    EnergyAgent = import_energy_agent()

    # ----------------------------------------------

    MaintenanceAgent = import_maintenance_agent()

    # ----------------------------------------------

    print(
        "\n========== IMPORT TEST COMPLETED =========="
    )

    print(
        "Both agents were imported successfully!"
    )

    print(
        "\nEnergy Agent Class:"
    )

    print(
        EnergyAgent
    )

    print(
        "\nMaintenance Agent Class:"
    )

    print(
        MaintenanceAgent
    )