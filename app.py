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

    # Check if team already has a better or equal score
    existing_entry = next((entry for entry in leaderboard if entry["name"] == name), None)
    if existing_entry and score <= existing_entry["score"]:
        return False, existing_entry["score"]  # Do not update

    # Otherwise, replace or add the new better entry
    leaderboard = [entry for entry in leaderboard if entry["name"] != name]
    leaderboard.append({"name": name, "solution": solution, "score": score})
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)
    save_leaderboard(leaderboard)
    return True, score


# Page title
st.set_page_config(page_title="MAEB-SOC", layout="wide")
st.title("🪑 Sagardotegi Optimization Challenge")

# View-only leaderboard mode
view_only = st.button("👀 View Only Leaderboard")

st.divider()
if view_only:
    st.subheader("🏆 Live Leaderboard")
    leaderboard = load_leaderboard()
    if leaderboard:
        for i, entry in enumerate(leaderboard):
            st.markdown(f"**#{i+1} – {entry['name']}** : {entry['score']:.2f}")
    else:
        st.info("No submissions yet.")
    st.stop()  # Prevents rest of the page (form/admin) from rendering



# Split page into two columns
col1, col2 = st.columns(2)

# Left: Submission
with col1:
    st.header("📤 Submit Your Solution")
    with st.form("submission_form"):
        name = st.text_input("Team Name")
        solution_str = st.text_area("Your solution (e.g., [2, 0, 1, 3])")

        col_submit, col_check = st.columns([1, 1], gap="small")
        with col_submit:
            submitted = st.form_submit_button("🚀 Submit")
        with col_check:
            check_position = st.form_submit_button("🔍 Find my position")

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
            if not name:
                st.warning("⚠️ Please enter your Team Name first.")
            else:
                leaderboard = load_leaderboard()
                entry = next((entry for entry in leaderboard if entry["name"] == name), None)
                if entry:
                    position = sorted(leaderboard, key=lambda x: x["score"], reverse=True).index(entry) + 1
                    st.info(f"📊 You're currently ranked **#{position}** with a score of **{entry['score']:.2f}**.")
                else:
                    st.warning("❌ Team not found in the leaderboard yet.")


# Right: Leaderboard
with col2:
    st.header("🏆 Live Leaderboard")
    leaderboard = load_leaderboard()
    if leaderboard:
        for i, entry in enumerate(leaderboard):
            st.markdown(f"**#{i+1} – {entry['name']}** : {entry['score']:.2f}")
    else:
        st.info("No submissions yet.")

