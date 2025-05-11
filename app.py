import streamlit as st
import json
import os
import ast
from objective import evaluate_solution

LEADERBOARD_FILE = "leaderboard.json"

# Load leaderboard from file
def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE, "r") as f:
        return json.load(f)

# Save leaderboard to file
def save_leaderboard(lb):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(lb, f, indent=2)

# Submit a new entry
def submit_entry(name, solution):
    score = evaluate_solution(solution)
    leaderboard = load_leaderboard()
    leaderboard = [entry for entry in leaderboard if entry["name"] != name]
    leaderboard.append({"name": name, "solution": solution, "score": score})
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)
    save_leaderboard(leaderboard)

# Page title
st.set_page_config(page_title="Conference Seating Challenge", layout="wide")
st.title("🪑 Conference Seating Challenge")

# Split page into two columns
col1, col2 = st.columns(2)

# Left: Submission
with col1:
    st.header("📤 Submit Your Solution")
    with st.form("submission_form"):
        name = st.text_input("Team Name")
        solution_str = st.text_area("Your solution (e.g., [2, 0, 1, 3])")
        submitted = st.form_submit_button("Submit")
        if submitted:
            try:
                solution = ast.literal_eval(solution_str)
                if not isinstance(solution, list):
                    st.error("Solution must be a Python list (e.g., [1, 2, 3, 0])")
                else:
                    submit_entry(name, solution)
                    st.success("✅ Submission successful!")
            except Exception as e:
                st.error(f"❌ Error parsing your solution: {e}")

# Right: Leaderboard
with col2:
    st.header("🏆 Live Leaderboard")
    leaderboard = load_leaderboard()
    if leaderboard:
        for i, entry in enumerate(leaderboard):
            st.markdown(f"**#{i+1} – {entry['name']}** : {entry['score']:.2f}")
    else:
        st.info("No submissions yet.")

# Admin reset (optional)
st.divider()
admin_input = st.text_input("🔐 Admin passcode (optional)", type="password")
if "admin" in st.secrets and admin_input == st.secrets["admin"]["passcode"]:
    with st.expander("⚙️ Admin Panel"):
        if st.button("🔄 Reset leaderboard"):
            save_leaderboard([])
            st.success("Leaderboard has been reset.")

