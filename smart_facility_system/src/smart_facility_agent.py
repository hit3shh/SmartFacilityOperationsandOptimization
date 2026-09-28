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

OCCUPANCY_PROJECT_PATH = os.path.join(
    SPRINGBOARD_DIR,
    "M3_Occupancy_and_Security_Intelligence",
    "occupancy_system"
)

OCCUPANCY_SRC_PATH = os.path.join(
    OCCUPANCY_PROJECT_PATH,
    "src"
)

SECURITY_PROJECT_PATH = os.path.join(
    SPRINGBOARD_DIR,
    "M3_Occupancy_and_Security_Intelligence",
    "security_system"
)

SECURITY_SRC_PATH = os.path.join(
    SECURITY_PROJECT_PATH,
    "src"
)

# M4 COST OPTIMIZATION
COST_PROJECT_PATH = os.path.join(
    SPRINGBOARD_DIR,
    "M4_Cost_Optimization"
)

COST_SRC_PATH = os.path.join(
    COST_PROJECT_PATH,
    "src"
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
# IMPORT OCCUPANCY AGENT
# ==================================================

def get_occupancy_agent_class():

    if OCCUPANCY_SRC_PATH in sys.path:

        sys.path.remove(
            OCCUPANCY_SRC_PATH
        )

    sys.path.insert(
        0,
        OCCUPANCY_SRC_PATH
    )

    module = importlib.import_module(
        "occupancy_agent"
    )

    return module.OccupancyAgent


# ==================================================
# IMPORT SECURITY AGENT
# ==================================================

def get_security_agent_class():

    if SECURITY_SRC_PATH in sys.path:

        sys.path.remove(
            SECURITY_SRC_PATH
        )

    sys.path.insert(
        0,
        SECURITY_SRC_PATH
    )

    module = importlib.import_module(
        "security_agent"
    )

    return module.SecurityAgent


# ==================================================
# IMPORT COST OPTIMIZATION AGENT
# ==================================================

def get_cost_optimization_agent_class():

    if COST_SRC_PATH in sys.path:

        sys.path.remove(
            COST_SRC_PATH
        )

    sys.path.insert(
        0,
        COST_SRC_PATH
    )

    module = importlib.import_module(
        "cost_optimization_agent"
    )

    return module.CostOptimizationAgent


# ==================================================
# SMART FACILITY AGENT
# ==================================================

class SmartFacilityAgent:

    def __init__(
        self,
        maintenance_model_path
    ):

        # ------------------------------------------
        # Import agent classes
        # ------------------------------------------

        EnergyAgent = (
            get_energy_agent_class()
        )

        MaintenanceAgent = (
            get_maintenance_agent_class()
        )

        OccupancyAgent = (
            get_occupancy_agent_class()
        )

        SecurityAgent = (
            get_security_agent_class()
        )

        CostOptimizationAgent = (
            get_cost_optimization_agent_class()
        )

        # ------------------------------------------
        # Initialize agents
        # ------------------------------------------

        self.energy_agent = (
            EnergyAgent()
        )

        self.maintenance_agent = (
            MaintenanceAgent(
                maintenance_model_path
            )
        )

        self.occupancy_agent = (
            OccupancyAgent()
        )

        self.security_agent = (
            SecurityAgent()
        )

        self.cost_optimization_agent = (
            CostOptimizationAgent()
        )


    # ==================================================
    # ENERGY ANALYSIS
    # ==================================================

    def run_energy_analysis(
        self,
        energy_df
    ):

        return (
            self.energy_agent.run_analysis(
                energy_df
            )
        )


    # ==================================================
    # MAINTENANCE ANALYSIS
    # ==================================================

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


    # ==================================================
    # OCCUPANCY ANALYSIS
    # ==================================================

    def run_occupancy_analysis(
        self,
        occupancy_df
    ):

        return (
            self.occupancy_agent.analyze(
                occupancy_df
            )
        )


    # ==================================================
    # SECURITY ANALYSIS
    # ==================================================

    def analyze_security_event(
        self,
        event
    ):

        return (
            self.security_agent
            .analyze_event(
                event
            )
        )


    def get_security_alert_history(
        self
    ):

        return (
            self.security_agent
            .get_alert_history()
        )


    def clear_security_alert_history(
        self
    ):

        return (
            self.security_agent
            .clear_alert_history()
        )


    # ==================================================
    # COST OPTIMIZATION ANALYSIS - M4
    # ==================================================

    def run_cost_analysis(self):

        return (
            self.cost_optimization_agent
            .run_analysis()
        )


    # ==================================================
    # COMBINED FACILITY INSIGHT
    # ==================================================

    def generate_facility_insight(
        self,
        energy_results,
        maintenance_result,
        cost_results=None
    ):

        # ------------------------------------------
        # Energy information
        # ------------------------------------------

        energy_summary = (
            energy_results["summary"]
        )

        anomaly_count = (
            energy_results["anomaly_count"]
        )

        peak_usage = (
            energy_results["peak_usage"]
        )

        # ------------------------------------------
        # Maintenance information
        # ------------------------------------------

        maintenance_risk = (
            maintenance_result["risk_level"]
        )

        insights = []

        # ------------------------------------------
        # Energy insight
        # ------------------------------------------

        insights.append(
            (
                "Energy system analysis completed. "
                f"Total energy consumption: "
                f"{energy_summary['total_energy']:.2f}."
            )
        )

        # ------------------------------------------
        # Peak energy insight
        # ------------------------------------------

        insights.append(
            (
                "Peak energy usage occurs around "
                f"{peak_usage['peak_hour']}:00."
            )
        )

        # ------------------------------------------
        # Energy anomaly insight
        # ------------------------------------------

        if anomaly_count > 0:

            insights.append(
                (
                    f"{anomaly_count} energy anomalies "
                    "were detected and should be monitored."
                )
            )

        # ------------------------------------------
        # Maintenance insight
        # ------------------------------------------

        insights.append(
            (
                f"Machine "
                f"{maintenance_result['product_id']} "
                f"has a {maintenance_risk} maintenance "
                "risk level."
            )
        )

        # ------------------------------------------
        # COST INSIGHTS - M4
        # ------------------------------------------

        if cost_results is not None:

            total_cost = (
                cost_results[
                    "total_operational_cost"
                ]
            )

            total_budget = (
                cost_results[
                    "total_budget"
                ]
            )

            budget_variance = (
                cost_results[
                    "budget_variance"
                ]
            )

            budget_status = (
                cost_results[
                    "budget_status"
                ]
            )

            potential_savings = (
                cost_results[
                    "potential_savings"
                ]
            )

            insights.append(
                (
                    f"Total operational cost is "
                    f"{total_cost:,.2f} against a "
                    f"budget of {total_budget:,.2f}."
                )
            )

            insights.append(
                (
                    f"Budget status: {budget_status}. "
                    f"Budget variance: "
                    f"{budget_variance:,.2f}."
                )
            )

            insights.append(
                (
                    f"Potential cost savings of "
                    f"{potential_savings:,.2f} "
                    "were identified."
                )
            )

        # ------------------------------------------
        # FACILITY PRIORITY
        # ------------------------------------------

        if maintenance_risk in [
            "Critical",
            "High"
        ]:

            priority = "High"

            combined_recommendation = (
                "Prioritize maintenance inspection "
                "for the high-risk machine while "
                "continuing to monitor energy "
                "consumption and operational costs."
            )

        elif (
            cost_results is not None
            and cost_results["budget_status"]
            == "Over Budget"
        ):

            priority = "High"

            combined_recommendation = (
                "Operational costs are above the "
                "allocated budget. Prioritize "
                "energy optimization, predictive "
                "maintenance and vendor cost control."
            )

        elif anomaly_count > 100:

            priority = "Medium"

            combined_recommendation = (
                "Prioritize investigation of unusual "
                "energy consumption patterns while "
                "continuing equipment and cost monitoring."
            )

        else:

            priority = "Low"

            combined_recommendation = (
                "Facility conditions appear stable. "
                "Continue regular energy, equipment "
                "and cost monitoring."
            )

        # ------------------------------------------
        # RETURN FACILITY INSIGHT
        # ------------------------------------------

        return {

            "facility_priority":
                priority,

            "insights":
                insights,

            "combined_recommendation":
                combined_recommendation
        }


    # ==================================================
    # COMPLETE FACILITY ANALYSIS
    # ==================================================

    def run_complete_analysis(
        self,
        energy_df,
        machine_data
    ):

        # ------------------------------------------
        # Energy Agent
        # ------------------------------------------

        energy_results = (
            self.run_energy_analysis(
                energy_df
            )
        )

        # ------------------------------------------
        # Maintenance Agent
        # ------------------------------------------

        maintenance_result = (
            self.analyze_machine(
                machine_data
            )
        )

        # ------------------------------------------
        # Cost Optimization Agent - M4
        # ------------------------------------------

        cost_results = (
            self.run_cost_analysis()
        )

        # ------------------------------------------
        # Facility Intelligence
        # ------------------------------------------

        facility_insight = (
            self.generate_facility_insight(
                energy_results,
                maintenance_result,
                cost_results
            )
        )

        # ------------------------------------------
        # Return complete results
        # ------------------------------------------

        return {

            "energy_results":
                energy_results,

            "maintenance_result":
                maintenance_result,

            "cost_results":
                cost_results,

            "facility_insight":
                facility_insight
        }