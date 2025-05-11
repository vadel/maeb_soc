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

# Submit a new entry only if better
def submit_entry(name, solution):
    score = evaluate_solution(solution)
    leaderboard = load_leaderboard()
    existing_entry = next((entry for entry in leaderboard if entry["name"] == name), None)

    if existing_entry and score <= existing_entry["score"]:
        return False, existing_entry["score"]  # Keep best

    leaderboard = [entry for entry in leaderboard if entry["name"] != name]
    leaderboard.append({"name": name, "solution": solution, "score": score})
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)
    save_leaderboard(leaderboard)
    return True, score

# Streamlit page config
st.set_page_config(page_title="Conference Seating Challenge", layout="wide")

# Title and view-only toggle in top-right
header_col1, header_spacer, header_col2 = st.columns([8, 6, 1])

with header_col1:
    st.title("🪑 Conference Seating Challenge")

with header_col2:
    if "view_only_mode" not in st.session_state:
        st.session_state.view_only_mode = False
    if st.button("👁️ Leaderboard Only"):
        st.session_state.view_only_mode = not st.session_state.view_only_mode


# View-only leaderboard mode
if st.session_state.view_only_mode:
    st.subheader("🏆 Live Leaderboard")
    leaderboard = load_leaderboard()
    if leaderboard:
        for i, entry in enumerate(leaderboard):
            st.markdown(f"**#{i+1} – {entry['name']}** : {entry['score']:.2f}")
    else:
        st.info("No submissions yet.")
    st.stop()

# 2-column layout: left = form, right = leaderboard
col1, col2 = st.columns(2)

# === Left side: Submission form ===
with col1:
    st.header("📤 Submit Your Solution")
    with st.form("submission_form"):
        name = st.text_input("Team Name")
        solution_str = st.text_area("Your solution (e.g., [2, 0, 1, 3])")

        btn_col1, btn_col2 = st.columns([1, 1])
        with btn_col1:
            submitted = st.form_submit_button("🚀 Submit")
        with btn_col2:
            check_position = st.form_submit_button("🔍 Find My Position")

        if submitted:
            try:
                solution = ast.literal_eval(solution_str)
                if not isinstance(solution, list):
                    st.error("Solution must be a Python list (e.g., [1, 2, 3, 0])")
                else:
                    success, result = submit_entry(name, solution)
                    if success:
                        st.success("✅ Submission accepted and leaderboard updated!")
                    else:
                        st.warning(f"⚠️ Your score ({evaluate_solution(solution):.2f}) is not better than your previous best ({result:.2f}). Submission not saved.")
            except Exception as e:
                st.error(f"❌ Error parsing your solution: {e}")

        elif check_position:
            if not name.strip():
                st.warning("⚠️ Please enter your Team Name to check your position.")
            else:
                leaderboard = load_leaderboard()
                entry = next((entry for entry in leaderboard if entry["name"] == name), None)
                if entry:
                    position = sorted(leaderboard, key=lambda x: x["score"], reverse=True).index(entry) + 1
                    st.info(f"📊 You're currently ranked **#{position}** with a score of **{entry['score']:.2f}**.")
                else:
                    st.warning("❌ Team not found in the leaderboard yet.")

# === Right side: Full leaderboard ===
with col2:
    st.header("🏆 Live Leaderboard")
    leaderboard = load_leaderboard()
    if leaderboard:
        for i, entry in enumerate(leaderboard):
            st.markdown(f"**#{i+1} – {entry['name']}** : {entry['score']:.2f}")
    else:
        st.info("No submissions yet.")

