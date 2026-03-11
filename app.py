import streamlit as st
import urllib.parse

# 1. Page Configuration
st.set_page_config(page_title="Robo-Escape", layout="centered")

# 2. Mobile-Friendly Maze Layout
MAZE = [
    "XXXXXXXXXX",
    "XP      EX", 
    "X  XXXX  X",
    "X    X   X",
    "X  X   X X",
    "X  XXXXX X",
    "X        X",
    "XXXXXXXXXX"
]

# 3. Game State
if 'r' not in st.session_state:
    st.session_state.r, st.session_state.c = 1, 1
if 'moves' not in st.session_state:
    st.session_state.moves = 0

def move(dr, dc):
    nr, nc = st.session_state.r + dr, st.session_state.c + dc
    if MAZE[nr][nc] == "X":
        st.session_state.r, st.session_state.c = 1, 1 
        st.toast("🚫 Hit a wall! Back to start!", icon="⚠️")
    else:
        st.session_state.r, st.session_state.c = nr, nc
        st.session_state.moves += 1
        if MAZE[nr][nc] == "E":
            st.balloons() 

# 4. Corrected CSS and Display (fixed unsafe_allow_html)
st.markdown("""
    <style>
    .maze-text {
        font-size: 30px !important;
        font-family: monospace;
        line-height: 1.1;
        text-align: center;
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ ROBO-ESCAPE ⚡")
st.write(f"**Moves: {st.session_state.moves}**")

# Movement Controls
col1, col2, col3 = st.columns([1,1,1])
with col2: st.button("↑", on_click=move, args=(-1, 0))
c_a, c_b, c_c = st.columns([1,1,1])
with c_a: st.button("←", on_click=move, args=(0, -1))
with c_b: st.button("↓", on_click=move, args=(1, 0))
with c_c: st.button("→", on_click=move, args=(0, 1))

# Drawing the Maze
display_grid = ""
for r, row in enumerate(MAZE):
    for c, char in enumerate(row):
        if r == st.session_state.r and c == st.session_state.c:
            display_grid += "🤖"
        elif char == "X": display_grid += "🟦"
        elif char == "E": display_grid += "🟡"
        else: display_grid += "⬜"
    display_grid += "\n"

st.markdown(f'<p class="maze-text">{display_grid}</p>', unsafe_allow_html=True)

# 5. Attractive Winning Message & WhatsApp Button
if MAZE[st.session_state.r][st.session_state.c] == "E":
    st.markdown("""
        <div style="background-color:#00ffcc; padding:20px; border-radius:15px; text-align:center; border: 2px solid #1a1a40;">
            <h1 style="color:#1a1a40; margin:0;">🏆 YOU WON! 🏆</h1>
            <p style="color:#1a1a40; font-size:18px;">Your child has the logic of a future coder!</p>
            <h3 style="color:#ff0066;">Prerna Khandelwal's Academy</h3>
        </div>
    """, unsafe_allow_html=True)
    
    msg = f"I just beat the Robo-Maze in {st.session_state.moves} moves! I want to book a free Python trial session."
    encoded_msg = urllib.parse.quote(msg)
    whatsapp_url = f"https://wa.me/918949803950?text={encoded_msg}"
    
    st.link_button("🟢 Claim Your Free Trial on WhatsApp", whatsapp_url, use_container_width=True)
