# CSP Campus Class Scheduling System

A Constraint Satisfaction Problem (CSP) based laboratory scheduling system for UISU-Africa using Google OR-Tools.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://csp-campus-class-scheduling-wlbrihwj9bevrnxrp5jemp.streamlit.app/)

##  Table of Contents

- [Overview](#overview)
- [Concept of Constraint Satisfaction Problems](#concept-of-constraint-satisfaction-problems)
- [Problem Statement](#problem-statement)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Implementation Details](#implementation-details)
- [Team Contributions](#team-contributions)
- [Project Structure](#project-structure)
- [Conclusion](#conclusion)

##  Overview

This project automates the creation of weekly laboratory schedules for 5 laboratories in the LKB Building at UISU-Africa. The system handles up to 200 classes per semester taught by 60 faculty members using a Constraint Satisfaction Programming (CSP) approach implemented with Google OR-Tools.

**Live Demo:** [Streamlit Web App](https://csp-campus-class-scheduling-wlbrihwj9bevrnxrp5jemp.streamlit.app/)

##  Concept of Constraint Satisfaction Problems (CSP)

CSPs (Constraint Satisfaction Problems) are search problems where the solution must satisfy a set of constraints. The problem is framed as a collection of variables, each with a set of possible values (domains), and a collection of constraints that restrict the values the variables can take simultaneously.

This approach is powerful in situations where we must make optimal or feasible decisions given limited resources or rules — like scheduling, assignment, or planning problems.

### Components of CSP:

- **Variables:** These are the unknowns we are solving for. In a scheduling problem, they can represent elements like time slots, locations, or resources.

- **Domains:** Each variable has a domain — a set of values it can take. For example, a time slot variable might have a domain of 7 possible time blocks in a day.

- **Constraints:** These are the rules that must be respected. They ensure the feasibility of the final assignment. Constraints can be:
  - **Hard constraints**, which must be strictly satisfied (e.g., no faculty can teach two classes at the same time).
  - **Soft constraints**, which are desirable but not mandatory.

A CSP solver uses these constraints, along with heuristics, to reduce the search space and find a feasible solution efficiently.

##  Problem Statement: Laboratory Scheduling at UISU-Africa

We aim to design a weekly laboratory schedule for **5 laboratories** in the LKB Building at **UISU-Africa**. Our university offers **200 classes per semester**, taught by **60 faculty members**.

To automate this process, we adopted a **Constraint Satisfaction Programming (CSP)** approach, implemented using **Google OR-Tools**, a robust library for constraint solving.

Initially, we considered using the `constraint` Python library, but we found it ineffective for scaling and handling the complexity of the problem. Hence, we transitioned to using `ortools.sat.python.cp_model`, which proved more efficient and flexible.

### Input Format

Our program takes input from an Excel file named `classes_input2.xlsx` with the following columns:

- **id**: Unique class identifier (e.g., DSA2020)
- **faculty**: ID of the faculty member assigned to teach the class (0–59)
- **is_concentration**: Whether the class is a concentration course (1 for yes, 0 for no)
- **is_double**: Whether the class is a double session class (1 for yes, 0 for no)

### Output Format

The program returns an output Excel file named `lab_schedule.xlsx` with the complete lab schedule including:
- Class ID
- Faculty ID
- Assigned Lab
- Time Slot
- Days
- Type of Class (Concentration or Regular)
- Whether it's a Double Class

### Variables, Domain, and Constraints

#### Variables:
- **Lab** assigned to each class
- **Time slot** for each class
- **Day pair** (e.g., Mon/Wed, Tue/Thu, or single days)

#### Domains:
- **Lab:** Lab1 to Lab5
- **Time slot:** 7 possible slots in a day
- **Day pair:** 7 combinations of days (MonWed, TueThu, Mon, Tue, etc.)

#### Constraints:
1. **No time overlap for same-semester classes**
2. **No faculty teaching more than one class at the same time**
3. **Concentration classes must be held in smaller labs (Lab4 or Lab5)**
4. **Double classes must be scheduled on Mon/Wed or Tue/Thu**

> **Note:** While the university offers 200 classes, we reduced the number to **100** in our experiment due to performance limitations on our local machines.

##  Features

- **Automated Scheduling**: Generates optimal lab schedules based on constraints
- **Constraint Handling**:
  - No time overlap for classes
  - No faculty teaching multiple classes simultaneously
  - Concentration classes assigned to smaller labs
  - Double classes scheduled on appropriate day pairs
- **Excel Integration**: Import class data and export schedules via Excel
- **Web Interface**: User-friendly Streamlit GUI for non-technical users
- **Scalable Solution**: Handles up to 200 classes across 5 laboratories

##  Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/csp-campus-class-scheduling.git
cd csp-campus-class-scheduling
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

##  Usage

### Command Line Interface

Run the main scheduling script using Jupyter Notebook:

```bash
jupyter notebook lab_scheduling.ipynb
```

Make sure `classes_input2.xlsx` is in the same directory.

### Web Interface (GUI)

To make our scheduling tool more accessible and user-friendly, we developed a simple web application using Streamlit, which provides an interactive interface for uploading the course input file and downloading the generated schedule.

Launch the Streamlit web application:

```bash
streamlit run GUI.py
```

This will open a web browser where you can:
1. Upload your class input file (Excel format)
2. Generate the schedule automatically
3. Download the resulting schedule as an Excel file

The web app eliminates the need to interact directly with the code, making it accessible to administrators and staff without programming knowledge.

##  Implementation Details

### Implementation Overview

We now walk through the implementation of our CSP model using OR-Tools.

The code follows these major steps:

1. **Reading and validating input data**
2. **Creating decision variables for lab, timeslot, and daypair**
3. **Defining hard constraints**
4. **Adding special rules for concentration and double classes**
5. **Solving the model using CP-SAT solver**
6. **Exporting the resulting schedule to Excel**

### Step 1: Defining Variables and Domains


We create three variables for each class:
- **lab**: An integer between 0 and 4, representing the 5 labs
- **slot**: An integer between 0 and 6, representing the 7 time slots per day
- **daypair**: An integer between 0 and 6, representing the 7 day combinations

These are defined using `model.NewIntVar()`:

```python
lab = model.NewIntVar(0, len(labs_all) - 1, f"{cls['id']}_lab")
slot = model.NewIntVar(0, len(timeslots) - 1, f"{cls['id']}_slot")
daypair = model.NewIntVar(0, len(day_pairs) - 1, f"{cls['id']}_daypair")
```

The variables are stored in a dictionary for easy access per class.

#### Available Resources

**Laboratories:**
- Lab1, Lab2, Lab3 (General purpose labs)
- Lab4, Lab5 (Small labs for concentration classes)

**Time Slots:**
- 7:00-8:40 AM
- 9:00-10:40 AM
- 11:00-12:40 PM
- 1:20-3:00 PM
- 3:30-5:10 PM
- 5:30-7:10 PM
- 7:30-9:10 PM

**Day Pairs:**
- MonWed, TueThu (for double classes)
- Mon, Tue, Wed, Thu, Fri (for single classes)

### Step 2: Defining Constraints



#### A. Avoiding Lab-Time-Day Overlaps
No two classes should be in the same lab at the same time on the same day. This is ensured by:

```python
model.AddBoolOr([same_lab.Not(), same_slot.Not(), same_day.Not()])
```

#### B. Faculty Conflict Avoidance
No faculty member can teach two classes at the same time (same slot and same day):

```python
if cls1["faculty"] == cls2["faculty"]:
    # same time means same slot and same day
    same_time = model.NewBoolVar(f"same_time_{i}_{j}")
    model.AddBoolAnd([same_slot, same_day]).OnlyEnforceIf(same_time)
    model.AddBoolOr([same_slot.Not(), same_day.Not()]).OnlyEnforceIf(same_time.Not())
    model.Add(same_time == 0)  # no overlap for same faculty
```

#### C. Concentration Classes in Small Labs
Classes marked as concentration must be scheduled only in Lab4 or Lab5:

```python
model.AddAllowedAssignments(
    [class_vars[cls["id"]]["lab"]],
    [(labs_all.index(lab),) for lab in labs_small]
)
```

#### D. Double Classes on Mon/Wed or Tue/Thu Only
These are restricted to specific day pairs:

```python
allowed_double_days = [day_pairs.index("MonWed"), day_pairs.index("TueThu")]
for cls in classes:
    if cls["is_double"]:
        model.AddAllowedAssignments(
            [class_vars[cls["id"]]["daypair"]],
            [(d,) for d in allowed_double_days]
        )
```

All these constraints ensure the solution is practical, realistic, and follows institutional rules.

### Step 3: Solving the Model and Exporting the Output


We solve the problem using:

```python
solver = cp_model.CpSolver()
status = solver.Solve(model)
```

If a feasible or optimal solution is found, we extract the values and format them into a readable DataFrame. The final schedule is saved as an Excel file:

```python
if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
    schedule = []
    for cls in classes:
        v = class_vars[cls["id"]]
        schedule.append({
            "Class": cls["id"],
            "Faculty": f"Faculty_{cls['faculty'] + 1}",
            "Lab": labs_all[solver.Value(v["lab"])],
            "Time": timeslots[solver.Value(v["slot"])],
            "Days": day_pairs[solver.Value(v["daypair"])],
            "Type": "Concentration" if cls["is_concentration"] else "Regular",
            "Double Class": "Yes" if cls["is_double"] else "No"
        })
    df = pd.DataFrame(schedule)
    df.to_excel("lab_schedule.xlsx", index=False)
else:
    print("No feasible schedule found.")
```

This file contains:
- Class ID
- Faculty ID
- Assigned Lab
- Time Slot
- Days
- Type of Class (Concentration or Regular)
- Whether it's a Double Class

##  Team Contributions

- **Aime**: Defining Variables and Domains
- **Zakariya & Rachael**: Defining Constraints
- **Sean & Crispin**: Solving the Model and Exporting Output

##  Project Structure

```
csp-campus-class-scheduling/
│
├── GUI.py                      # Streamlit web application
├── lab_scheduling.ipynb        # Main scheduling script (Jupyter notebook)
├── classes_input2.xlsx         # Sample input file with class data
├── lab_schedule.xlsx           # Sample output file with generated schedule
├── requirements.txt            # Python dependencies
├── runtime.txt                 # Python version for deployment                 
└── README.md                   # This file
```

##  Conclusion

This project demonstrates the power of CSPs in solving real-world scheduling problems. Using OR-Tools, we modeled variables, defined their domains, and encoded institutional constraints to automatically generate a lab schedule that avoids conflicts and follows policy rules.

Despite initial performance limitations with other libraries and with large input sizes, our final approach is scalable and can be further optimized or extended to include soft constraints (like preferred times or faculty availability) in future versions.

