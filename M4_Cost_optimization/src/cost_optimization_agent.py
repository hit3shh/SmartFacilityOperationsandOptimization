"""
Cost Optimization Agent
Milestone 4 - Agentic AI for Smart Facility Operations

Responsibilities:
- Analyze operational expenditures
- Identify cost-saving opportunities
- Monitor budget compliance
- Estimate potential savings
- Calculate ROI
- Generate actionable recommendations
"""

from pathlib import Path
import pandas as pd


class CostOptimizationAgent:

    def __init__(self, data_path=None):
        """Initialize the Cost Optimization Agent."""

        if data_path is None:
            data_path = (
                Path(__file__).resolve().parent.parent
                / "data"
                / "operational_costs.csv"
            )

        self.data_path = Path(data_path)
        self.cost_df = None

    # ---------------------------------------------------------
    # DATA LOADING
    # ---------------------------------------------------------

    def load_data(self):
        """Load operational cost data."""

        self.cost_df = pd.read_csv(self.data_path)

        self.cost_df["date"] = pd.to_datetime(
            self.cost_df["date"]
        )

        return self.cost_df

    # ---------------------------------------------------------
    # COST ANALYSIS
    # ---------------------------------------------------------

    def analyze_costs(self):
        """Analyze total operational expenditure."""

        if self.cost_df is None:
            self.load_data()

        cost_columns = [
            "energy_cost",
            "maintenance_cost",
            "water_cost",
            "vendor_cost",
            "labor_cost",
            "other_cost"
        ]

        cost_breakdown = {}

        for column in cost_columns:
            cost_breakdown[column] = float(
                self.cost_df[column].sum()
            )

        total_cost = sum(cost_breakdown.values())

        return {
            "total_operational_cost": round(total_cost, 2),
            "cost_breakdown": cost_breakdown
        }

    # ---------------------------------------------------------
    # BUDGET ANALYSIS
    # ---------------------------------------------------------

    def analyze_budget(self):
        """Compare operational expenditure against budget."""

        if self.cost_df is None:
            self.load_data()

        cost_columns = [
            "energy_cost",
            "maintenance_cost",
            "water_cost",
            "vendor_cost",
            "labor_cost",
            "other_cost"
        ]

        monthly_cost = self.cost_df[cost_columns].sum(axis=1)

        total_cost = float(monthly_cost.sum())
        total_budget = float(self.cost_df["budget"].sum())

        variance = total_budget - total_cost

        if variance >= 0:
            status = "Within Budget"
        else:
            status = "Over Budget"

        return {
            "total_budget": round(total_budget, 2),
            "actual_cost": round(total_cost, 2),
            "budget_variance": round(variance, 2),
            "budget_status": status
        }

    # ---------------------------------------------------------
    # SAVINGS OPPORTUNITIES
    # ---------------------------------------------------------

    def identify_savings_opportunities(self):
        """Identify major areas where operational costs can be reduced."""

        if self.cost_df is None:
            self.load_data()

        analysis = self.analyze_costs()
        breakdown = analysis["cost_breakdown"]

        opportunities = []

        # Energy optimization
        energy_cost = breakdown["energy_cost"]

        if energy_cost > 0:
            saving = energy_cost * 0.10

            opportunities.append({
                "area": "Energy",
                "current_cost": round(energy_cost, 2),
                "estimated_savings": round(saving, 2),
                "action": (
                    "Optimize HVAC schedules, lighting and "
                    "energy consumption during low-occupancy periods."
                )
            })

        # Maintenance optimization
        maintenance_cost = breakdown["maintenance_cost"]

        if maintenance_cost > 0:
            saving = maintenance_cost * 0.08

            opportunities.append({
                "area": "Maintenance",
                "current_cost": round(maintenance_cost, 2),
                "estimated_savings": round(saving, 2),
                "action": (
                    "Use predictive maintenance to reduce "
                    "unplanned equipment failures and emergency repairs."
                )
            })

        # Vendor optimization
        vendor_cost = breakdown["vendor_cost"]

        if vendor_cost > 0:
            saving = vendor_cost * 0.07

            opportunities.append({
                "area": "Vendor Management",
                "current_cost": round(vendor_cost, 2),
                "estimated_savings": round(saving, 2),
                "action": (
                    "Review vendor utilization, contracts and "
                    "service frequency."
                )
            })

        # Labor optimization
        labor_cost = breakdown["labor_cost"]

        if labor_cost > 0:
            saving = labor_cost * 0.05

            opportunities.append({
                "area": "Labor",
                "current_cost": round(labor_cost, 2),
                "estimated_savings": round(saving, 2),
                "action": (
                    "Optimize workforce allocation based on "
                    "facility occupancy and operational demand."
                )
            })

        return opportunities

    # ---------------------------------------------------------
    # ROI CALCULATION
    # ---------------------------------------------------------

    def calculate_roi(self):
        """Estimate ROI from identified cost-saving opportunities."""

        opportunities = self.identify_savings_opportunities()

        total_savings = sum(
            item["estimated_savings"]
            for item in opportunities
        )

        # Estimated implementation cost for optimization initiatives
        implementation_cost = total_savings * 0.20

        if implementation_cost > 0:
            roi = (
                (total_savings - implementation_cost)
                / implementation_cost
            ) * 100
        else:
            roi = 0

        return {
            "estimated_annual_savings": round(total_savings, 2),
            "estimated_implementation_cost": round(
                implementation_cost, 2
            ),
            "estimated_roi_percent": round(roi, 2)
        }

    # ---------------------------------------------------------
    # RECOMMENDATIONS
    # ---------------------------------------------------------

    def generate_recommendations(self):
        """Generate actionable cost optimization recommendations."""

        budget = self.analyze_budget()
        opportunities = self.identify_savings_opportunities()

        recommendations = []

        if budget["budget_status"] == "Over Budget":
            recommendations.append(
                "Operational expenditure is above the allocated "
                "budget. Immediate cost-control measures are recommended."
            )
        else:
            recommendations.append(
                "Operational expenditure is currently within the "
                "allocated budget."
            )

        for opportunity in opportunities:
            recommendations.append(
                f"{opportunity['area']}: "
                f"{opportunity['action']} "
                f"Estimated savings: "
                f"{opportunity['estimated_savings']:.2f}."
            )

        return recommendations

    # ---------------------------------------------------------
    # COMPLETE ANALYSIS
    # ---------------------------------------------------------

    def run_analysis(self):
        """Run complete Cost Optimization Agent analysis."""

        if self.cost_df is None:
            self.load_data()

        cost_analysis = self.analyze_costs()
        budget_analysis = self.analyze_budget()
        opportunities = self.identify_savings_opportunities()
        roi = self.calculate_roi()
        recommendations = self.generate_recommendations()

        return {
            **cost_analysis,
            **budget_analysis,
            "savings_opportunities": opportunities,
            "potential_savings": roi["estimated_annual_savings"],
            "roi": roi,
            "recommendations": recommendations
        }


# -------------------------------------------------------------
# STANDALONE TEST
# -------------------------------------------------------------

if __name__ == "__main__":

    agent = CostOptimizationAgent()

    results = agent.run_analysis()

    print("\n" + "=" * 60)
    print("COST OPTIMIZATION AGENT")
    print("=" * 60)

    print(
        f"\nTotal Operational Cost: "
        f"{results['total_operational_cost']:,.2f}"
    )

    print(
        f"Total Budget: "
        f"{results['total_budget']:,.2f}"
    )

    print(
        f"Budget Variance: "
        f"{results['budget_variance']:,.2f}"
    )

    print(
        f"Budget Status: "
        f"{results['budget_status']}"
    )

    print(
        f"\nPotential Savings: "
        f"{results['potential_savings']:,.2f}"
    )

    print(
        f"Estimated ROI: "
        f"{results['roi']['estimated_roi_percent']:.2f}%"
    )

    print("\nSavings Opportunities:")

    for opportunity in results["savings_opportunities"]:
        print(
            f"- {opportunity['area']}: "
            f"{opportunity['estimated_savings']:,.2f}"
        )

    print("\nRecommendations:")

    for recommendation in results["recommendations"]:
        print(f"- {recommendation}")

    print("\n" + "=" * 60)