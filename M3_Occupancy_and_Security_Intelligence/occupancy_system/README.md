# Occupancy Intelligence System

Part of the **Agentic AI for Smart Facility Operations and Optimization** project.

The Occupancy Intelligence System is the occupancy-analysis component of **Milestone 3: Occupancy & Security Intelligence**. It processes room sensor data to determine current occupancy, calculate occupancy analytics, and forecast occupancy for the next 30-second interval.

---

## Overview

The Occupancy Agent provides:

- Current occupancy monitoring
- Occupancy status classification
- Occupancy rate calculation
- Average occupancy analysis
- Maximum occupancy analysis
- Next-step occupancy forecasting
- Reusable production forecasting logic
- Automated tests for the agent

The system uses historical occupancy and environmental sensor measurements to generate operational occupancy intelligence.

---

## Dataset

This module uses the **Room Occupancy Estimation** dataset from the UCI Machine Learning Repository.

**Dataset source:**

[UCI Machine Learning Repository - Room Occupancy Estimation](https://archive.ics.uci.edu/dataset/864/room%2Boccupancy%2Bestimation)

### Dataset information

- **Dataset:** Room Occupancy Estimation
- **Repository:** UCI Machine Learning Repository
- **Dataset ID:** 864
- **Sampling interval:** 30 seconds
- **Target variable:** `Room_Occupancy_Count`
- **Occupancy classes:** 0–3

The raw dataset is stored locally at:

```text
data/raw/Occupancy_Estimation.csv
