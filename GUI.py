import streamlit as st
import pandas as pd
from ortools.sat.python import cp_model
import io

# Setup parameters
labs_all = ['Lab1', 'Lab2', 'Lab3', 'Lab4', 'Lab5']
labs_small = ['Lab4', 'Lab5']
timeslots = ["7-8:40", "9-10:40", "11-12:40", "1:20-3", "3:30-5:10", "5:30-7:10", "7:30-9:10"]
day_pairs = ["MonWed", "TueThu", "Mon", "Tue", "Wed", "Thu", "Fri"]

st.title("UISU-A Laboratory Scheduler")
st.write("Upload an Excel file with columns: `id`, `faculty`, `is_concentration`, `is_double`.")

uploaded_file = st.file_uploader("Upload Class Input Excel", type="xlsx")

def run_scheduler(df_input):
    classes = df_input.to_dict(orient="records")
    model = cp_model.CpModel()
    class_vars = {}

    for cls in classes:
        lab = model.NewIntVar(0, len(labs_all) - 1, f"{cls['id']}_lab")
        slot = model.NewIntVar(0, len(timeslots) - 1, f"{cls['id']}_slot")
        daypair = model.NewIntVar(0, len(day_pairs) - 1, f"{cls['id']}_daypair")
        class_vars[cls["id"]] = {"lab": lab, "slot": slot, "daypair": daypair}

    for i, cls1 in enumerate(classes):
        v1 = class_vars[cls1["id"]]
        for j in range(i + 1, len(classes)):
            cls2 = classes[j]
            v2 = class_vars[cls2["id"]]

            same_lab = model.NewBoolVar(f"same_lab_{i}_{j}")
            model.Add(v1["lab"] == v2["lab"]).OnlyEnforceIf(same_lab)
            model.Add(v1["lab"] != v2["lab"]).OnlyEnforceIf(same_lab.Not())

            same_slot = model.NewBoolVar(f"same_slot_{i}_{j}")
            model.Add(v1["slot"] == v2["slot"]).OnlyEnforceIf(same_slot)
            model.Add(v1["slot"] != v2["slot"]).OnlyEnforceIf(same_slot.Not())

            same_day = model.NewBoolVar(f"same_day_{i}_{j}")
            model.Add(v1["daypair"] == v2["daypair"]).OnlyEnforceIf(same_day)
            model.Add(v1["daypair"] != v2["daypair"]).OnlyEnforceIf(same_day.Not())

            model.AddBoolOr([same_lab.Not(), same_slot.Not(), same_day.Not()])

            if cls1["faculty"] == cls2["faculty"]:
                same_time = model.NewBoolVar(f"same_time_{i}_{j}")
                model.AddBoolAnd([same_slot, same_day]).OnlyEnforceIf(same_time)
                model.AddBoolOr([same_slot.Not(), same_day.Not()]).OnlyEnforceIf(same_time.Not())
                model.Add(same_time == 0)

    allowed_double_days = [day_pairs.index("MonWed"), day_pairs.index("TueThu")]
    for cls in classes:
        if cls["is_concentration"]:
            model.AddAllowedAssignments(
                [class_vars[cls["id"]]["lab"]],
                [(labs_all.index(lab),) for lab in labs_small]
            )
        if cls["is_double"]:
            model.AddAllowedAssignments(
                [class_vars[cls["id"]]["daypair"]],
                [(d,) for d in allowed_double_days]
            )

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status in [cp_model.FEASIBLE, cp_model.OPTIMAL]:
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
        return df
    else:
        return None

if uploaded_file:
    try:
        df_input = pd.read_excel(uploaded_file)
        expected_cols = {"id", "faculty", "is_concentration", "is_double"}
        if not expected_cols.issubset(df_input.columns):
            st.error(f"Excel must have columns: {expected_cols}")
        else:
            st.write("Preview of Uploaded Data:")
            st.dataframe(df_input.head())

            if st.button("Generate Schedule"):
                with st.spinner("Solving constraints and generating schedule..."):
                    df_schedule = run_scheduler(df_input)
                if df_schedule is not None:
                    st.success("Schedule generated successfully!")
                    st.dataframe(df_schedule)

                    output = io.BytesIO()
                    df_schedule.to_excel(output, index=False)
                    st.download_button("Download Schedule Excel", output.getvalue(), file_name="labo_schedule5.xlsx")
                else:
                    st.error("No feasible schedule found.")
    except Exception as e:
        st.error(f"Error reading file: {e}")
