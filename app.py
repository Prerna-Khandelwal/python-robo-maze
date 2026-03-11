import streamlit as st

st.set_page_config(page_title="Robo-Escape", layout="centered")

# 1. The Maze Layout
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

# 2. Game State (Position)
if 'r' not in st.session_state:
    st.session_state.r, st.session_state.c = 1, 1

def move(dr, dc):
    nr, nc = st.session_state.r + dr, st.session_state.c + dc
    if MAZE[nr][nc] == "X":
        st.session_state.r, st.session_state.c = 1, 1 # Reset to start
        st.toast("🚫 Hit a wall! Back to the start!", icon="⚠️")
    else:
        st.session_state.r, st.session_state.c = nr, nc
        if MAZE[nr][nc] == "E":
            st.balloons() # Fun winning effect!

# 3. UI Elements
st.title("⚡ ROBO-ESCAPE CHALLENGE ⚡")
st.write("Rules: Use buttons to reach the Gold Circle. Don't hit walls!")

# Controller Buttons
col1, col2, col3 = st.columns([1,1,1])
with col2: st.button("↑", on_click=move, args=(-1, 0))
col_a, col_b, col_c = st.columns([1,1,1])
with col_a: st.button("←", on_click=move, args=(0, -1))
with col_b: st.button("↓", on_click=move, args=(1, 0))
with col_c: st.button("→", on_click=move, args=(0, 1))

# 4. Display the Game
# (This builds the visual maze automatically)
display = ""
for r, row in enumerate(MAZE):
    for c, char in enumerate(row):
        if r == st.session_state.r and c == st.session_state.c:
            display += "🤖"
        elif char == "X": display += "🟦"
        elif char == "E": display += "🟡"
        else: display += "⬜"
    display += "\n"

st.text(display)

if MAZE[st.session_state.r][st.session_state.c] == "E":
    st.success("MISSION COMPLETE! Join Prerna's Python Classes!")
