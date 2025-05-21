import streamlit as st
from streamlit_sortables import sort_items
import pandas as pd
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title="Homework Scheduler", layout="centered")
st.title("Weekly Homework Scheduler")

# Task list
tasks = [
    "Spanish Vocabulary",
    "English Report Draft",
    "History Chapter Notes",
    "Algebra Problem Set",
    "Music Practice"
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

# Initialize symbols and colors once
if "task_symbols" not in st.session_state:
    random.shuffle(color_blocks)
    st.session_state.task_symbols = {task: color_blocks[i] for i, task in enumerate(tasks)}
    st.session_state.task_colors = {
        task: symbol_colors[st.session_state.task_symbols[task]] for task in tasks
    }

# Initialize emoji-labeled task order
if "sorted_labels" not in st.session_state:
    emoji_labels = [
        f"{st.session_state.task_symbols[task]} {task}" for task in tasks
    ]
    st.session_state.sorted_labels = emoji_labels

# Show sortable widget
st.markdown("### Let's arrange tasks from your favorite to least favorite")
new_order = sort_items(st.session_state.sorted_labels, direction="vertical")

if new_order != st.session_state.sorted_labels:
    st.session_state.sorted_labels = new_order

# Strip emoji to get clean task names
sorted_tasks = [label.split(' ', 1)[1] for label in st.session_state.sorted_labels]

# Time input section
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

# Generate timeline only when all inputs are filled
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

    # Draw stacked bar timeline
    fig, ax = plt.subplots(figsize=(2, 6))
    start = 0
    for label, duration, typ in timeline:
        color = (
            "gray" if typ == "short_break" else
            "white" if typ == "long_break" else
            st.session_state.task_colors.get(label, "#000000")
        )
        ax.barh(0, duration, left=start, color=color, edgecolor='black')
        ax.text(start + duration / 2, 0, label, ha='center', va='center', fontsize=8, rotation=90)
        start += duration

    ax.set_xlim(0, start)
    ax.set_yticks([])
    ax.set_xlabel("Minutes")
    ax.set_title("Planned Timeline (Stacked)")

    st.pyplot(fig)

    st.markdown("### If this looks good, we can start the timer.")
