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
# Build stacked vertical timeline
fig, ax = plt.subplots(figsize=(2, 6))
start_time = 0

for label, duration, typ in timeline:
    color = (
        "gray" if typ == "short_break" else
        "white" if typ == "long_break" else
        st.session_state.task_colors.get(label, "#000000")
    )
    ax.barh(0, duration, left=start_time, color=color, edgecolor='black')
    ax.text(start_time + duration / 2, 0, label, ha='center', va='center', fontsize=8, rotation=90)
    start_time += duration

ax.set_xlim(0, start_time)
ax.set_yticks([])
ax.set_xlabel("Minutes")
ax.set_title("Planned Timeline (Stacked)")

st.pyplot(fig)

st.markdown("### If this looks good, we can start the timer.")
