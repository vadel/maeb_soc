import streamlit as st
import json
import os
import ast
from objective import evaluate_solution

LEADERBOARD_FILE = "leaderboard.json"

# Load leaderboard
def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE, "r") as f:
        return json.load(f)

# Save leaderboard
def save_leaderboard(lb):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(lb, f, indent=2)

# Submit entry
def submit_entry(name, solution):
    score = evaluate_solution(solution)
    leaderboard = load_leaderboard()
    leaderboard = [entry for entry in leaderboard if entry["name"] != name]
    leaderboard.append({"name": name, "solution": solution, "score": score})
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)
    save_leaderboard(leaderboard)

# UI
st.title("🪑 Conference Seating Challenge")

with st.form("submission_form"):
    name = st.text_input("Team Name")
    solution_str = st.text_area("Your solution (e.g., [2, 0, 1, 3])")
    submitted = st.form_submit_button("Submit")
    if submitted:
        try:
            solution = ast.literal_eval(solution_str)
            if not isinstance(solution, list):
                st.error("Must be a list like [1, 2, 3]")
            else:
                submit_entry(name, solution)
                st.success("✅ Submitted!")
        except Exception as e:
            st.error(f"❌ Error parsing solution: {e}")

# Leaderboard
st.subheader("🏆 Live Leaderboard")
leaderboard = load_leaderboard()
if leaderboard:
    for i, entry in enumerate(leaderboard):
        st.markdown(f"**#{i+1} – {entry['name']}** : {entry['score']:.2f}")
else:
    st.info("No submissions yet.")

