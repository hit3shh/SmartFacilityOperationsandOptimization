import sys
from pathlib import Path

# Add M4 src directory to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
M4_SRC = PROJECT_ROOT / "M4_Cost_Optimization" / "src"

sys.path.insert(0, str(M4_SRC))

from cost_optimization_agent import CostOptimizationAgent


def test_data_loading():
    agent = CostOptimizationAgent()

    df = agent.load_data()

    assert not df.empty
    assert len(df) == 12
    assert "energy_cost" in df.columns
    assert "budget" in df.columns


def test_cost_analysis():
    agent = CostOptimizationAgent()

    result = agent.analyze_costs()

    assert result["total_operational_cost"] > 0
    assert "cost_breakdown" in result
    assert result["cost_breakdown"]["energy_cost"] > 0


def test_budget_analysis():
    agent = CostOptimizationAgent()

    result = agent.analyze_budget()

    assert result["total_budget"] > 0
    assert result["actual_cost"] > 0
    assert "budget_variance" in result
    assert result["budget_status"] in [
        "Within Budget",
        "Over Budget"
    ]


def test_savings_opportunities():
    agent = CostOptimizationAgent()

    opportunities = agent.identify_savings_opportunities()

    assert len(opportunities) > 0

    for opportunity in opportunities:
        assert "area" in opportunity
        assert "estimated_savings" in opportunity
        assert opportunity["estimated_savings"] >= 0


def test_roi():
    agent = CostOptimizationAgent()

    result = agent.calculate_roi()

    assert result["estimated_annual_savings"] > 0
    assert result["estimated_implementation_cost"] > 0
    assert result["estimated_roi_percent"] > 0


def test_complete_analysis():
    agent = CostOptimizationAgent()

    result = agent.run_analysis()

    assert "total_operational_cost" in result
    assert "budget_status" in result
    assert "potential_savings" in result
    assert "roi" in result
    assert "recommendations" in result

    