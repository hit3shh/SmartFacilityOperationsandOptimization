# Security Intelligence System

- Identify off-hours activity.

## Overview

The Security Intelligence System is the security-monitoring component of the
**Agentic AI for Smart Facility Operations and Optimization** project.

It analyzes facility access-control events, engineers behavioral and security
signals, detects anomalous events, and generates risk assessments and security
alerts.

The system is implemented as a reusable **Security Agent** rather than only as
a notebook-based analysis pipeline.

---

## Objectives

The Security Intelligence System is designed to:

- Monitor access-control events.
- Detect unusual or potentially unauthorized activity.
- Identify behavioral deviations.
- Incorporate resource authorization information.
- Detect activity outside an entity's home zone.
- identify off-hours activity.
- Analyze action-transition behavior.
- Generate anomaly risk scores.
- Generate security alerts with severity and reasons.

---

## Dataset

### BPHAC Dataset

The system uses the **Behaviour-Policy Hybrid Access Control (BPHAC)**
dataset.

Source:

https://zenodo.org/records/21701530

The dataset contains labeled access-control logs from a synthetic virtual
factory environment involving humans, robots, safety systems, zones,
resources, and security scenarios.

### Main Access Log

File:

```text
data/raw/access_logs_final.csv