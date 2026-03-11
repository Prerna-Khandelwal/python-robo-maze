import streamlit as st

st.set_page_config(page_title="Robo-Escape", layout="centered")

# 1. The Maze Layout (From your original project)
MAZE = [
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XP      XXXXX           X",
    "X  XXX  XXXXX  XXXXXXX  X",
    "X  XXX         X     X  X",
    "X  XXXXXXXXXX  X  X  X  X",
    "X  X           X  X  X  X",
    "X  X  XXXXXXX  XXXX  X  X",
    "X     X        X        X",
    "X  XXXX  XXXXXXX  XXXX  X",
    "X        X           XEX ",
    "XXXXXXXXXXXXXXXXXXXXXXXXX"
]

# 2. Game State Management
if 'r' not in st.session_state:
    st.session_state.r, st.session_state.c = 1, 1

def move(dr, dc):
    nr, nc = st.session_state.r + dr, st.session_state.c + dc
    # Wall Collision Logic
    if MAZE[nr][nc] == "X":
        st.session_state.r, st.session_state.c = 1, 1 # Reposition to start
        st.toast("🚫 Oops! You hit a wall. Try again!", icon="⚠️")
    else:
        st.session_state.r, st.session_state.c = nr, nc
        # Check for Win
        if MAZE[nr][nc] == "E":
            st.balloons() 

# 3. User Interface
st.title("⚡ ROBO-ESCAPE CHALLENGE ⚡")
st.info("Rules: Reach the Gold Circle (🟡). If you hit a Blue Wall (🟦), you reset!")

# Control Buttons
col1, col2, col3 = st.columns([1,1,1])
with col2: st.button("↑", on_click=move, args=(-1, 0))
c_a, c_b, c_c = st.columns([1,1,1])
with c_a: st.button("←", on_click=move, args=(0, -1))
with c_b: st.button("↓", on_click=move, args=(1, 0))
with c_c: st.button("→", on_click=move, args=(0, 1))

# 4. Drawing the Maze
display_grid = ""
for r, row in enumerate(MAZE):
    for c, char in enumerate(row):
        if r == st.session_state.r and c == st.session_state.c:
            display_grid += "🤖"
        elif char == "X": display_grid += "🟦"
        elif char == "E": display_grid += "🟡"
        else: display_grid += "⬜"
    display_grid += "\n"

st.text(display_grid)

# Final Win Message
if MAZE[st.session_state.r][st.session_state.c] == "E":
    st.success("🏆 MISSION COMPLETE! Join Prerna Khandelwal's Python Classes!")
