import streamlit as st
from streamlit_sortables import sort_items
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Let user sort tasks
st.header("Daily Assignment Planner")

st.markdown("### Let's arrange tasks from your favorite to least favorite")
default_tasks = [
    "Spanish Vocabulary",
    "English Report Draft",
    "History Chapter 5 Notes",
    "Algebra Problem Set",
    "Biology Lab Write-Up",
    "Clarinet Practice"
]

sorted_tasks = sort_items(default_tasks, direction="vertical")

# Step 2: Prompt for time estimates
st.markdown(
    "### Ok that was great! Now let’s figure out how much time each task needs. "
    "In the future I can estimate based on how long you needed and what grade you got."
)

reverse_tasks = list(reversed(sorted_tasks))

time_inputs = []
for task in reverse_tasks:
    minutes = st.number_input(f"How many minutes for '{task}'?", min_value=0, step=5, key=task)
    time_inputs.append(minutes)

# Step 3: Build and show timeline
if all(m > 0 for m in time_inputs):
    df = pd.DataFrame({"task": reverse_tasks, "minutes": time_inputs})

    # Add breaks every 60 minutes
    timeline = []
    current_time = 0
    for _, row in df.iterrows():
        timeline.append((current_time, row["minutes"], row["task"]))
        current_time += row["minutes"]
        # Insert a break every 60 min of work time (not counting breaks)
        if current_time // 60 > (current_time - row["minutes"]) // 60:
            timeline.append((current_time, 10, "Break"))
            current_time += 10

    # Plot timeline
    fig, ax = plt.subplots(figsize=(8, 2))
    start = 0
    for start_min, duration, label in timeline:
        ax.barh(0, duration, left=start_min, color="lightgray" if label == "Break" else None, edgecolor="black")
        ax.text(start_min + duration / 2, 0, label, ha="center", va="center", fontsize=8)
    ax.set_xlim(0, current_time)
    ax.set_yticks([])
    ax.set_xlabel("Minutes")
    ax.set_title("Planned Timeline with Breaks")
    st.pyplot(fig)
