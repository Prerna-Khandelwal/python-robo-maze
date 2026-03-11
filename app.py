import streamlit as st
import urllib.parse
import random

# 1. Page Configuration
st.set_page_config(page_title="Robo-Escape", layout="centered")

# 2. DEFINITIVE MAZE MAP (8x8)
MAZE_DATA = [
    "XXXXXXXX",
    "X      X", 
    "X  XXX X",
    "X    X X",
    "X  X   X",
    "X  XXXXX",
    "X      X",
    "XXXXXXXX"
]

# 3. Game State Initialization
if 'r' not in st.session_state:
    st.session_state.r, st.session_state.c = 1, 1
if 'moves' not in st.session_state:
    st.session_state.moves = 0
if 'alert' not in st.session_state:
    st.session_state.alert = False

# TARGET LOGIC
if 'target_r' not in st.session_state:
    open_coords = [(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(3,1),(3,2),(3,3),(3,4),(4,4),(4,5),(4,6),(6,1),(6,2),(6,3),(6,4),(6,5),(6,6)]
    valid_spots = [p for p in open_coords if p != (1,1)]
    st.session_state.target_r, st.session_state.target_c = random.choice(valid_spots)

# 4. Movement Logic
def move_player(dr, dc):
    st.session_state.alert = False # Clear old alerts
    new_r = st.session_state.r + dr
    new_c = st.session_state.c + dc
    
    if 0 <= new_r < len(MAZE_DATA) and 0 <= new_c < len(MAZE_DATA[0]):
        if MAZE_DATA[new_r][new_c] == "X":
            st.session_state.alert = True
        else:
            st.session_state.r = new_r
            st.session_state.c = new_c
            st.session_state.moves += 1
            if (new_r, new_c) == (st.session_state.target_r, st.session_state.target_c):
                st.balloons()

# 5. Professional CSS
st.markdown("""
    <style>
    .main .block-container { padding-top: 1.5rem; }
    
    .centered-title {
        text-align: center;
        color: #1a1a40;
        font-family: 'Arial Black', Gadget, sans-serif;
        margin-bottom: 0.2rem;
    }

    .maze-grid {
        display: grid;
        grid-template-columns: repeat(8, 1fr);
        width: 100%;
        max-width: 360px;
        margin: 0 auto;
        background-color: #f8f9fa;
        padding: 12px;
        border-radius: 15px;
        border: 2px solid #dee2e6;
        position: relative;
    }
    .tile {
        aspect-ratio: 1 / 1;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 26px;
    }
    .moves-text { text-align: center; font-weight: bold; margin-bottom: 10px; }
    button { height: 50px !important; font-weight: bold !important; }
    
    .wall-alert {
        background-color: #ff4b4b;
        color: white;
        text-align: center;
        padding: 10px;
        border-radius: 8px;
        margin: 10px auto;
        max-width: 360px;
        font-weight: bold;
        animation: shake 0.5s;
    }
    
    @keyframes shake {
        0% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        50% { transform: translateX(5px); }
        75% { transform: translateX(-5px); }
        100% { transform: translateX(0); }
    }
    </style>
    """, unsafe_allow_html=True)

# 6. UI Header & Controls (CENTERED)
st.markdown('<h1 class="centered-title">⚡ ROBO-ESCAPE ⚡</h1>', unsafe_allow_html=True)
st.markdown(f'<div class="moves-text">Moves: {st.session_state.moves}</div>', unsafe_allow_html=True)

# Movement Buttons
cols = st.columns(4)
with cols[0]: st.button("◀", on_click=move_player, args=(0, -1), use_container_width=True)
with cols[1]: st.button("▲", on_click=move_player, args=(-1, 0), use_container_width=True)
with cols[2]: st.button("▼", on_click=move_player, args=(1, 0), use_container_width=True)
with cols[3]: st.button("▶", on_click=move_player, args=(0, 1), use_container_width=True)

# 7. Alert Message (Shown right above the grid)
if st.session_state.alert:
    st.markdown('<div class="wall-alert">🧱 OOPS! YOU HIT A WALL!</div>', unsafe_allow_html=True)

# 8. Render The Grid
grid_html = '<div class="maze-grid">'
for r_idx, row_str in enumerate(MAZE_DATA):
    for c_idx, char in enumerate(row_str):
        icon = ""
        if r_idx == st.session_state.r and c_idx == st.session_state.c:
            icon = "🤖"
        elif r_idx == st.session_state.target_r and c_idx == st.session_state.target_c:
            icon = "🟡"
        elif char == "X":
            icon = "🟦"
        else:
            icon = "⬜"
        grid_html += f'<div class="tile">{icon}</div>'
grid_html += '</div>'

st.markdown(grid_html, unsafe_allow_html=True)

# 9. Marketing & Win Message
if (st.session_state.r, st.session_state.c) == (st.session_state.target_r, st.session_state.target_c):
    st.markdown(f"""
        <div style="background-color:#e0fff4; padding:20px; border-radius:15px; text-align:center; border: 3px solid #00c896; margin-top: 20px;">
            <h2 style="color:#1a1a40; margin:0;">🏆 YOU WON! 🏆</h2>
            <p style="color:#1a1a40; font-size:16px; margin:10px 0;">Build games like this with Prerna Khandelwal</p>
            <p style="font-weight:bold; color:#555;">Python • Scratch • JavaScript</p>
        </div>
    """, unsafe_allow_html=True)
    
    msg = urllib.parse.quote(f"I beat the Robo-Maze in {st.session_state.moves} moves! I want to book a trial class.")
    st.link_button("🟢 Chat on WhatsApp", f"https://wa.me/918949803950?text={msg}", use_container_width=True)
    
    if st.button("🔄 Play Again", use_container_width=True):
        for key in ['target_r', 'target_c', 'alert']: 
            if key in st.session_state: del st.session_state[key]
        st.session_state.r, st.session_state.c, st.session_state.moves = 1, 1, 0
        st.rerun()
