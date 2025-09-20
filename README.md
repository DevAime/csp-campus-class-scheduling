# Laboratory Scheduling using Constraint Satisfaction Problems (CSP)

This project implements a Constraint Satisfaction Programming (CSP) approach to generate weekly laboratory schedules.
It uses Google OR-Tools to efficiently assign classes to labs, time slots, and days while respecting hard and soft constraints.

## Concept of CSP

Constraint Satisfaction Problems (CSPs) are search problems where solutions must satisfy a set of variables, domains, and constraints.
They are widely used in scheduling, planning, and resource allocation tasks.

Variables: Unknowns to be solved (e.g., lab, time slot, day).

Domains: Possible values for each variable.

Constraints: Rules that ensure feasibility (hard constraints must be satisfied, soft constraints are desirable).

## Problem Statement: Laboratory Scheduling

5 laboratories available

Hundreds of classes per semester

Dozens of faculty members

The challenge: automatically generate a conflict-free weekly lab schedule.

We use:

Google OR-Tools (ortools.sat.python.cp_model) for constraint solving

Excel files as input/output format

## Input & Output

Input file: classes_input2.xlsx

id: Class identifier (e.g., DSA2020)

faculty: Faculty ID (e.g., 0–59)

is_concentration: 1 = yes, 0 = no

is_double: 1 = double session, 0 = single

Output file: labo_schedule3.xlsx

Contains the generated weekly lab schedule

## Example Screenshots
Input Excel File
<img width="500px" alt="image" src="https://github.com/user-attachments/assets/13c73255-a70a-4c54-9659-ca21ed30d890" />
Output Excel File
<img width="500px" alt="image" src="https://github.com/user-attachments/assets/1595527f-c8be-4907-a502-bddc0d150c43" />

## Variables, Domains, and Constraints

Variables: Lab, Time slot, Day pair
Domains:

Lab → Lab1–Lab5

Time slot → 7 per day

Day pair → 7 possible combinations

Constraints:

No overlap for same-semester classes

A faculty cannot teach two classes at the same time

Concentration classes → Lab4 or Lab5

Double sessions → Must be Mon/Wed or Tue/Thu

For experiments, class count was reduced from 200 → 100 due to local performance limits.

## Implementation Overview

Read & validate input data

Create decision variables (lab, timeslot, daypair)

Define hard constraints

Apply concentration & double-class rules

Solve model using CP-SAT Solver

Export schedule to Excel

## GUI Option

A Streamlit web app is included for ease of use:

Upload Excel input file

Generate and download schedule interactively

Run the app:

pip install streamlit
streamlit run main2.py
