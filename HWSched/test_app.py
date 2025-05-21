import streamlit as st
from streamlit_sortables import sort_items
import pandas as pd
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title="Homework Scheduler", layout="centered")
st.title("Tonight's Study Scheduler")

# Task list
tasks = [
    "Spanish Vocabulary",
    "English Report Draft",
    "History Chapter 2 Notes",
    "Algebra Problem Set",
    "Clarinet Practice"
]

# Color emoji blocks and matching hex codes
color_blocks = ['🟦', '🟩', '🟨', '🟪', '🟫']
symbol_colors = {
    '🟦': '#4da6ff',
    '🟩': '#4dff88',
    '🟨': '#ffff66',
    '🟪': '#bf80ff',
    '🟫': '#a0522d'
}

# Shuffle emoji and assign to tasks
if "task_symbols" not in st.session_state:
    random.shuffle(color_blocks)
    st.session_state.task_symbols = {task: color_blocks[i] for i, task in enumerate(tasks)}
    st.session_state.task_colors = {
        task: symbol_colors[st.session_state.task_symbols[task]] for task in tasks
    }

# Initialize task order with emoji labels
if "sorted_labels" not in st.session_state:
    emoji_labels = [
        f"{st.session_state.task_symbols[task]} {task}" for task in tasks
    ]
    st.session_state.sorted_labels = emoji_labels

# Show sortable list and update order if changed
st.markdown("### Click and drag the red buttons to arrange tasks from your favorite to least favorite")
new_order = sort_items(st.session_state.sorted_labels, direction="vertical")

if new_order != st.session_state.sorted_labels:
    st.session_state.sorted_labels = new_order

# Recover task names from emoji labels
sorted_tasks = [label.split(' ', 1)[1] for label in st.session_state.sorted_labels]

# Step 2: Time input per task
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

# Step 3: Timeline chart
if all(m > 0 for m in time_inputs):
    df = pd.DataFrame({"task": reverse_tasks, "minutes": time_inputs})

    timeline = []
    current_time = 0
    for _, row in df.iterrows():
        timeline.append((row["task"], row["minutes"], "task"))
        current_time += row["minutes"]

        timeline.append(("Break", 5, "short_break"))
        current_time += 5

        if current_time // 60 > (current_time - 5) // 60:
            timeline.append(("Hour Break", 10, "long_break"))
            current_time += 10

    labels = [item[0] for item in timeline]
    durations = [item[1] for item in timeline]
    colors = [
        "gray" if t[2] == "short_break" else
        "white" if t[2] == "long_break" else
        st.session_state.task_colors.get(t[0], "#000000")
        for t in timeline
    ]

    fig, ax = plt.subplots(figsize=(4, len(timeline) * 0.6))
    ax.bar(range(len(durations)), durations, color=colors, edgecolor='black')
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=90)
    ax.set_ylabel("Minutes")
    ax.set_title("Planned Timeline (Vertical)")

    st.pyplot(fig)

    st.markdown("### If this looks good, we can start the timer.")
