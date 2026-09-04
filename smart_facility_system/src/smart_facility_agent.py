import sys
import os
import importlib


# ==================================================
# PROJECT PATHS
# ==================================================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

SMART_FACILITY_DIR = os.path.dirname(
    CURRENT_DIR
)

SPRINGBOARD_DIR = os.path.dirname(
    SMART_FACILITY_DIR
)


ENERGY_PROJECT_PATH = os.path.join(
    SPRINGBOARD_DIR,
    "M1_agentic_facilityops_ai"
)

MAINTENANCE_PROJECT_PATH = os.path.join(
    SPRINGBOARD_DIR,
    "M2_Predictive_Maintenance"
)


# ==================================================
# IMPORT HELPER
# ==================================================

def clear_src_modules():

    modules_to_remove = []

    for module_name in list(sys.modules.keys()):

        if (
            module_name == "src"
            or module_name.startswith("src.")
        ):

            modules_to_remove.append(
                module_name
            )

    for module_name in modules_to_remove:

        del sys.modules[module_name]


# ==================================================
# IMPORT ENERGY AGENT
# ==================================================

def get_energy_agent_class():

    clear_src_modules()

    if ENERGY_PROJECT_PATH in sys.path:

        sys.path.remove(
            ENERGY_PROJECT_PATH
        )

    sys.path.insert(
        0,
        ENERGY_PROJECT_PATH
    )

    module = importlib.import_module(
        "src.energy_agent"
    )

    return module.EnergyAgent


# ==================================================
# IMPORT MAINTENANCE AGENT
# ==================================================

def get_maintenance_agent_class():

    clear_src_modules()

    if MAINTENANCE_PROJECT_PATH in sys.path:

        sys.path.remove(
            MAINTENANCE_PROJECT_PATH
        )

    sys.path.insert(
        0,
        MAINTENANCE_PROJECT_PATH
    )

    module = importlib.import_module(
        "src.maintenance_agent"
    )

    return module.MaintenanceAgent


# ==================================================
# SMART FACILITY AGENT
# ==================================================

class SmartFacilityAgent:

    def __init__(
        self,
        maintenance_model_path
    ):

        # Import both agent classes
        EnergyAgent = (
            get_energy_agent_class()
        )

        MaintenanceAgent = (
            get_maintenance_agent_class()
        )


        # Initialize agents
        self.energy_agent = (
            EnergyAgent()
        )

        self.maintenance_agent = (
            MaintenanceAgent(
                maintenance_model_path
            )
        )


    # ==============================================
    # ENERGY ANALYSIS
    # ==============================================

    def run_energy_analysis(
        self,
        energy_df
    ):

        return (
            self.energy_agent.run_analysis(
                energy_df
            )
        )


    # ==============================================
    # MAINTENANCE ANALYSIS
    # ==============================================

    def analyze_machine(
        self,
        machine_data
    ):

        return (
            self.maintenance_agent
            .analyze_machine(
                machine_data
            )
        )


    def get_maintenance_summary(
        self,
        maintenance_df
    ):

        return (
            self.maintenance_agent
            .get_dataset_summary(
                maintenance_df
            )
        )


    # ==============================================
    # COMBINED FACILITY INSIGHT
    # ==============================================

    def generate_facility_insight(
        self,
        energy_results,
        maintenance_result
    ):

        energy_summary = (
            energy_results["summary"]
        )

        anomaly_count = (
            energy_results["anomaly_count"]
        )

        peak_usage = (
            energy_results["peak_usage"]
        )

        maintenance_risk = (
            maintenance_result["risk_level"]
        )

        insights = []


        # Energy insight
        insights.append(
            (
                "Energy system analysis completed. "
                f"Total energy consumption: "
                f"{energy_summary['total_energy']:.2f}."
            )
        )


        # Peak usage insight
        insights.append(
            (
                "Peak energy usage occurs around "
                f"{peak_usage['peak_hour']}:00."
            )
        )


        # Anomaly insight
        if anomaly_count > 0:

            insights.append(
                (
                    f"{anomaly_count} energy anomalies "
                    "were detected and should be monitored."
                )
            )


        # Maintenance insight
        insights.append(
            (
                f"Machine {maintenance_result['product_id']} "
                f"has a {maintenance_risk} maintenance "
                "risk level."
            )
        )


        # Combined priority
        if maintenance_risk in [
            "Critical",
            "High"
        ]:

            priority = "High"

            combined_recommendation = (
                "Prioritize maintenance inspection for "
                "the high-risk machine while continuing "
                "to monitor facility energy consumption."
            )

        elif anomaly_count > 100:

            priority = "Medium"

            combined_recommendation = (
                "Prioritize investigation of unusual "
                "energy consumption patterns and continue "
                "monitoring equipment health."
            )

        else:

            priority = "Low"

            combined_recommendation = (
                "Facility conditions appear stable. "
                "Continue regular energy and equipment "
                "monitoring."
            )


        return {

            "facility_priority": priority,

            "insights": insights,

            "combined_recommendation":
                combined_recommendation
        }


    # ==============================================
    # COMPLETE FACILITY ANALYSIS
    # ==============================================

    def run_complete_analysis(
        self,
        energy_df,
        machine_data
    ):

        # Run Energy Agent
        energy_results = (
            self.run_energy_analysis(
                energy_df
            )
        )


        # Run Maintenance Agent
        maintenance_result = (
            self.analyze_machine(
                machine_data
            )
        )


        # Generate combined insight
        facility_insight = (
            self.generate_facility_insight(
                energy_results,
                maintenance_result
            )
        )


        return {

            "energy_results":
                energy_results,

            "maintenance_result":
                maintenance_result,

            "facility_insight":
                facility_insight
        }
    