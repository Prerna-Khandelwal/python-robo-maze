import streamlit as st
import urllib.parse
import random

# 1. Page Configuration
st.set_page_config(page_title="Robo-Escape", layout="centered")

# 2. DEFINITIVE MAZE MAP (8x8)
# 'X' = Wall, ' ' = Path
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

# TARGET LOGIC: Guaranteed reachable spots
if 'target_r' not in st.session_state:
    open_coords = [(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(3,1),(3,2),(3,3),(3,4),(4,4),(4,5),(4,6),(6,1),(6,2),(6,3),(6,4),(6,5),(6,6)]
    # Filter out the starting position
    valid_spots = [p for p in open_coords if p != (1,1)]
    st.session_state.target_r, st.session_state.target_c = random.choice(valid_spots)

# 4. Movement Logic (The Wall Guard)
def move_player(dr, dc):
    new_r = st.session_state.r + dr
    new_c = st.session_state.c + dc
    
    # Boundary and Wall Check
    if 0 <= new_r < len(MAZE_DATA) and 0 <= new_c < len(MAZE_DATA[0]):
        # Check if the destination character is a wall
        destination_tile = MAZE_DATA[new_r][new_c]
        
        if destination_tile == "X":
            st.error("🧱 Ouch! That's a wall.")
        else:
            # Safe to move
            st.session_state.r = new_r
            st.session_state.c = new_c
            st.session_state.moves += 1
            if (new_r, new_c) == (st.session_state.target_r, st.session_state.target_c):
                st.balloons()

# 5. Professional CSS Grid (Perfect Alignment)
st.markdown("""
    <style>
    .main .block-container { padding-top: 1.5rem; }
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
    }
    .tile {
        aspect-ratio: 1 / 1;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 26px;
    }
    button { height: 50px !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# 6. UI Controls
st.title("⚡ ROBO-ESCAPE ⚡")
st.write(f"**Moves: {st.session_state.moves}**")

# Movement Buttons (Strictly aligned top row)
cols = st.columns(4)
with cols[0]: st.button("◀", on_click=move_player, args=(0, -1), use_container_width=True)
with cols[1]: st.button("▲", on_click=move_player, args=(-1, 0), use_container_width=True)
with cols[2]: st.button("▼", on_click=move_player, args=(1, 0), use_container_width=True)
with cols[3]: st.button("▶", on_click=move_player, args=(0, 1), use_container_width=True)

# 7. Render The Grid
grid_html = '<div class="maze-grid">'
for r_idx, row_str in enumerate(MAZE_DATA):
    for c_idx, char in enumerate(row_str):
        icon = ""
        # Check current robot pos
        if r_idx == st.session_state.r and c_idx == st.session_state.c:
            icon = "🤖"
        # Check target pos
        elif r_idx == st.session_state.target_r and c_idx == st.session_state.target_c:
            icon = "🟡"
        # Render wall or path
        elif char == "X":
            icon = "🟦"
        else:
            icon = "⬜"
        grid_html += f'<div class="tile">{icon}</div>'
grid_html += '</div>'

st.markdown(grid_html, unsafe_allow_html=True)

# 8. Marketing & Win Message
if (st.session_state.r, st.session_state.c) == (st.session_state.target_r, st.session_state.target_c):
    st.markdown(f"""
        <div style="background-color:#e0fff4; padding:20px; border-radius:15px; text-align:center; border: 3px solid #00c896; margin-top: 20px;">
            <h2 style="color:#1a1a40; margin:0;">🏆 YOU WON! 🏆</h2>
            <p style="color:#1a1a40; font-size:16px; margin:10px 0;">Code games like this with</p>
            <h3 style="color:#ff0066; margin:0;">Prerna Khandelwal</h3>
            <p style="font-weight:bold; color:#555;">Python • Scratch • JavaScript</p>
        </div>
    """, unsafe_allow_html=True)
    
    msg = urllib.parse.quote(f"I beat the Robo-Maze in {st.session_state.moves} moves! I want to book a trial class.")
    st.link_button("🟢 Chat with Prerna on WhatsApp", f"https://wa.me/918949803950?text={msg}", use_container_width=True)
    
    if st.button("🔄 Play Again", use_container_width=True):
        for key in ['target_r', 'target_c']: 
            if key in st.session_state: del st.session_state[key]
        st.session_state.r, st.session_state.c, st.session_state.moves = 1, 1, 0
        st.rerun()
