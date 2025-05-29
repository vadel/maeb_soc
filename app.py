import streamlit as st
import json
import os
import ast
from objective import evaluate_solution
from sagardotegi_problem import SagardotegiProblem
import numpy as np

LEADERBOARD_FILE = "leaderboard.json"

query_params = st.query_params()
show_admin = query_params.get("admin", ["false"])[0] == "true"

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


# Load the docs
docs = open('docs/getting_started.md', 'r')
docs_getting_started = docs.read()
docs.close()

docs = open('docs/solution_format.md', 'r')
docs_solution_format = docs.read()
docs.close()

docs = open('docs/about_sop.md', 'r')
docs_about_sop = docs.read()
docs.close()

docs = open('docs/similarity.md', 'r')
docs_similarity = docs.read()
docs.close()


# Streamlit page config
st.set_page_config(page_title="MAEB-SOC!", layout="wide")

# Title and view-only toggle in top-right
header_col1, header_spacer, header_col2 = st.columns([15, 5, 1])

def toggle_view():
    st.session_state.view_only_mode = not st.session_state.view_only_mode
    button_label = "📄 Documentation" if not st.session_state.get("view_only_mode", True) else "🏠 Back to Main Page"


with header_col1:
    st.title("🪑 Sagardotegi Optimization Challenge")
    button_label = "📄 Documentation" if not st.session_state.get("view_only_mode", False) else "🏠 Back to Main Page"
    # if st.button(button_label):
    #     st.session_state.view_only_mode = not st.session_state.view_only_mode
    #     button_label = "📄 Documentation" if not st.session_state.get("view_only_mode", True) else "🏠 Back to Main Page"
    st.button(button_label, on_click=toggle_view)

with header_col2:
    if "view_only_mode" not in st.session_state:
        st.session_state.view_only_mode = False
    # if st.button("📄\nDocs"):
    #     st.session_state.view_only_mode = not st.session_state.view_only_mode

# View-only leaderboard mode
if st.session_state.view_only_mode:
    # st.subheader("🏆 Live Leaderboard")
    # leaderboard = load_leaderboard()
    # if leaderboard:
    #     for i, entry in enumerate(leaderboard):
    #         st.markdown(f"**#{i+1} – {entry['name']}** : {entry['score']:.2f}")
    # else:
    #     st.info("No submissions yet.")

    with st.expander("About the SOP 🧑‍🏫"):
        st.markdown(docs_about_sop)

    with st.expander("Submission format 📤"):
        st.markdown(docs_solution_format)

    with st.expander("Suggested setup 🚀"):
        st.markdown(docs_getting_started)

    with st.expander("How do we measure affinity? 🔍"):
        st.markdown(docs_similarity)

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
            if not name.strip():
                st.warning("⚠️ Please enter your Team Name before submitting.")
            else:
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

    if show_admin:
        st.divider()
        admin_input = st.text_input("🔐", type="password")
        if "admin" in st.secrets and admin_input == st.secrets["admin"]["passcode"]:
            with st.expander("⚙️ Admin Panel"):
                if st.button("🔄 Reset leaderboard"):
                    save_leaderboard([])
                    st.success("Leaderboard has been reset.")

                if st.button("Visualize best solution ✨"):
                    leaderboard = load_leaderboard()
                    if leaderboard:
                        best_solution = leaderboard[0]['solution']
                        best_solution = np.array(best_solution).astype(int)

                        problem = SagardotegiProblem()
                        st.text("Nodes (authors) are placed based on keyword similarity, while colors indicate the 19 tables.")
                        st.write(problem.visualize_solution(best_solution, plot=False))

                        st.header("Layout 🪑")
                        st.markdown(problem.solution_to_layout(best_solution, print_stdout=False))


# === Right side: Full leaderboard ===
with col2:
    st.header("🏆 Live Leaderboard")
    leaderboard = load_leaderboard()
    if leaderboard:
        for i, entry in enumerate(leaderboard):
            st.markdown(f"**#{i+1} – {entry['name']}** : {entry['score']:.2f}")
    else:
        st.info("No submissions yet.")
