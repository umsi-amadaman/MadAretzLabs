import streamlit as st
from streamlit_sortables import sort_items
import pandas as pd
import matplotlib.pyplot as plt
import random
from bs4 import BeautifulSoup

st.set_page_config(page_title="Homework Scheduler", layout="centered")

st.title("Weekly Homework Scheduler")

# Step 1: Sort assignments by preference
st.markdown("### Let's arrange tasks from your favorite to least favorite by clicking and dragging")

tasks = [
    "Spanish Vocabulary",
    "English Report Draft",
    "History Chapter 3 Notes",
    "Algebra Problem Set",
    "Biology Lab Write-Up",
    "Tuba Practice"
]

# Assign random colors to each task
task_colors = {task: f"#{random.randint(0, 0xFFFFFF):06x}" for task in tasks}

# Generate colored task HTML
def colorize(task, color):
    return f"<div style='padding:6px 12px; background-color:{color}; border-radius:6px; color:white; font-weight:500'>{task}</div>"

colored_tasks = [colorize(task, task_colors[task]) for task in tasks]

# Sort using the HTML-wrapped task labels
sorted_html = sort_items(colored_tasks, direction="vertical", unsafe_allow_html=True)

# Strip HTML to recover clean task names
sorted_tasks = [BeautifulSoup(item, "html.parser").text for item in sorted_html]

# Step 2: Prompt for time per task (reverse order)
st.markdown(
    "### Ok that was great! Now let’s figure out how much time each task needs. "
    "In the future I can estimate based on how long you needed and what grade you got."
)

reverse_tasks = list(reversed(sorted_tasks))
time_inputs = []
for task in reverse_tasks:
    minutes = st.number_input(
        f"How many minutes for '{task}'?",
        min_value=0,
        step=5,
        key=task
    )
    time_inputs.append(minutes)

# Step 3: Visualize vertical timeline with breaks
if all(m > 0 for m in time_inputs):
    df = pd.DataFrame({"task": reverse_tasks, "minutes": time_inputs})

    timeline = []
    current_time = 0
    for _, row in df.iterrows():
        timeline.append((row["task"], row["minutes"], "task"))
        current_time += row["minutes"]

        # Add 5 min break after each task
        timeline.append(("Break", 5, "short_break"))
        current_time += 5

        # Add 10 min break at the hour mark
        if current_time // 60 > (current_time - 5) // 60:
            timeline.append(("Hour Break", 10, "long_break"))
            current_time += 10

    labels = [item[0] for item in timeline]
    durations = [item[1] for item in timeline]
    colors = [
        "gray" if t[2] == "short_break" else
        "white" if t[2] == "long_break" else
        task_colors.get(t[0], "#000000")
        for t in timeline
    ]

    fig, ax = plt.subplots(figsize=(4, len(timeline) * 0.6))
    bars = ax.bar(range(len(durations)), durations, color=colors, edgecolor='black')

    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=90)
    ax.set_ylabel("Minutes")
    ax.set_title("Planned Timeline (Vertical)")

    st.pyplot(fig)

    st.markdown("### If this looks good, we can start the timer.")
