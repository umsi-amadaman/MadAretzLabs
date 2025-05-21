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
# Step 3: Build and show updated vertical timeline
if all(m > 0 for m in time_inputs):
    df = pd.DataFrame({"task": reverse_tasks, "minutes": time_inputs})

    timeline = []
    current_time = 0
    for _, row in df.iterrows():
        timeline.append((row["task"], row["minutes"], "task"))
        current_time += row["minutes"]

        # Add 5 min break after every task
        timeline.append(("Break", 5, "short_break"))
        current_time += 5

        # If we just crossed an hour mark, add a 10 min break
        if current_time // 60 > (current_time - 5) // 60:
            timeline.append(("Hour Break", 10, "long_break"))
            current_time += 10

    # Prepare for vertical bar chart
    labels = [item[0] for item in timeline]
    durations = [item[1] for item in timeline]
    colors = [
        "gray" if t[2] == "short_break" else
        "white" if t[2] == "long_break" else
        None
        for t in timeline
    ]

    fig, ax = plt.subplots(figsize=(4, len(timeline) * 0.5))
    bars = ax.bar(range(len(durations)), durations, color=colors, edgecolor='black')

    # Add labels
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=90)
    ax.set_ylabel("Minutes")
    ax.set_title("Planned Timeline (Vertical)")

    st.pyplot(fig)
