import streamlit as st
import urllib.parse
import random

# 1. Page Configuration
st.set_page_config(page_title="Robo-Escape", layout="centered")

# 2. Definitive Maze Data (Logic and Visuals)
MAZE = [
    "XXXXXXXX",
    "XP     X", 
    "X  XXX  X",
    "X    X  X",
    "X  X    X",
    "X  XXXX X",
    "X       X",
    "XXXXXXXX"
]

# 3. Game State
if 'r' not in st.session_state:
    st.session_state.r, st.session_state.c = 1, 1
if 'moves' not in st.session_state:
    st.session_state.moves = 0

# SMART TARGET: Only chooses from guaranteed reachable spots
if 'target_r' not in st.session_state:
    # These coordinates are all in the open white areas
    open_spots = [
        (1,4), (1,5), (1,6), 
        (3,1), (3,2), (3,3), (3,6), 
        (4,3), (4,4), (4,5), (4,6), 
        (6,1), (6,2), (6,3), (6,4), (6,5), (6,6)
    ]
    st.session_state.target_r, st.session_state.target_c = random.choice(open_spots)

# 4. Movement Logic (The Wall Guard)
def move_player(dr, dc):
    new_r = st.session_state.r + dr
    new_c = st.session_state.c + dc
    
    # Check boundaries
    if 0 <= new_r < len(MAZE) and 0 <= new_c < len(MAZE[0]):
        # Check for wall
        if MAZE[new_r][new_c] == "X":
            st.toast("🚫 Wall!", icon="🧱")
        else:
            # Valid move
            st.session_state.r = new_r
            st.session_state.c = new_c
            st.session_state.moves += 1
            if (new_r, new_c) == (st.session_state.target_r, st.session_state.target_c):
                st.balloons()

# 5. Fixed CSS for Perfect Grid Alignment
st.markdown("""
    <style>
    .main .block-container { padding-top: 1.5rem; }
    .maze-wrapper {
        display: grid;
        grid-template-columns: repeat(8, 1fr);
        width: 100%;
        max-width: 340px;
        margin: 0 auto;
        background-color: #f0f2f6;
        padding: 8px;
        border-radius: 12px;
        border: 2px solid #d1d5db;
    }
    .cell {
        aspect-ratio: 1 / 1;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
    }
    button { height: 48px !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# 6. UI Header & Controls
st.title("⚡ ROBO-ESCAPE ⚡")
st.write(f"**Moves: {st.session_state.moves}**")

# Control Buttons
cols = st.columns(4)
with cols[0]: st.button("◀", on_click=move_player, args=(0, -1), use_container_width=True)
with cols[1]: st.button("▲", on_click=move_player, args=(-1, 0), use_container_width=True)
with cols[2]: st.button("▼", on_click=move_player, args=(1, 0), use_container_width=True)
with cols[3]: st.button("▶", on_click=move_player, args=(0, 1), use_container_width=True)

# 7. Render Aligned Grid
grid_html = '<div class="maze-wrapper">'
for r, row in enumerate(MAZE):
    for c, char in enumerate(row):
        content = ""
        if (r, c) == (st.session_state.r, st.session_state.c): content = "🤖"
        elif (r, c) == (st.session_state.target_r, st.session_state.target_c): content = "🟡"
        elif char == "X": content = "🟦"
        else: content = "⬜"
        grid_html += f'<div class="cell">{content}</div>'
grid_html += '</div>'

st.markdown(grid_html, unsafe_allow_html=True)

# 8. Success Branding
if (st.session_state.r, st.session_state.c) == (st.session_state.target_r, st.session_state.target_c):
    st.markdown(f"""
        <div style="background-color:#00ffcc; padding:15px; border-radius:10px; text-align:center; border: 2px solid #1a1a40; margin-top: 15px;">
            <h3 style="color:#1a1a40; margin:0;">🏆 MISSION COMPLETE! 🏆</h3>
            <p style="color:#1a1a40; font-size:14px; margin:5px 0;">Build games with Prerna Khandelwal</p>
            <h4 style="color:#ff0066; margin:0;">Python • Scratch • JavaScript</h4>
        </div>
    """, unsafe_allow_html=True)
    
    encoded_msg = urllib.parse.quote(f"I beat the Robo-Maze in {st.session_state.moves} moves! I want to join Prerna's class.")
    st.link_button("🟢 Connect on WhatsApp", f"https://wa.me/918949803950?text={encoded_msg}", use_container_width=True)
    
    if st.button("🔄 Play Again", use_container_width=True):
        for k in ['target_r', 'target_c']: del st.session_state[k]
        st.session_state.r, st.session_state.c, st.session_state.moves = 1, 1, 0
        st.rerun()
