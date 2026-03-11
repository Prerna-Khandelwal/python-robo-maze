import streamlit as st
import urllib.parse
import random

# 1. Page Configuration
st.set_page_config(page_title="Robo-Escape", layout="centered")

# 2. Fixed Maze Layout (10x8)
# We use ' ' for empty paths where the target can appear
MAZE = [
    "XXXXXXXXXX",
    "XP       X", 
    "X  XXXX  X",
    "X    X   X",
    "X  X   X X",
    "X  XXXXX X",
    "X        X",
    "XXXXXXXXXX"
]

# 3. Game State Initialization
if 'r' not in st.session_state:
    st.session_state.r, st.session_state.c = 1, 1
if 'moves' not in st.session_state:
    st.session_state.moves = 0

# RANDOM TARGET LOGIC: 
# If target doesn't exist, find a random empty ' ' spot
if 'target' not in st.session_state:
    empty_spots = []
    for r_idx, row in enumerate(MAZE):
        for c_idx, char in enumerate(row):
            if char == " " and (r_idx != 1 or c_idx != 1): # Don't put target on the player
                empty_spots.append((r_idx, c_idx))
    st.session_state.target = random.choice(empty_spots)

# 4. Movement Logic
def move_player(dr, dc):
    new_r = st.session_state.r + dr
    new_c = st.session_state.c + dc
    
    if MAZE[new_r][new_c] == "X":
        # Reset on Wall Hit
        st.session_state.r, st.session_state.c = 1, 1 
        st.toast("🚫 Hit a wall! Resetting...", icon="⚠️")
    else:
        st.session_state.r, st.session_state.c = new_r, new_c
        st.session_state.moves += 1
        
        # Check if Robot reached the Random Target
        if (new_r, new_c) == st.session_state.target:
            st.balloons()

# 5. Professional Styling
st.markdown("""
    <style>
    .maze-container {
        font-size: 28px !important;
        font-family: 'Courier New', Courier, monospace;
        line-height: 1.2;
        letter-spacing: 2px;
        text-align: center;
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 15px;
        white-space: pre;
    }
    .stButton button { width: 100%; height: 60px; font-size: 24px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ ROBO-ESCAPE ⚡")
st.subheader(f"Moves: {st.session_state.moves}")

# 6. Thumb-Friendly Control Pad
col1, col2, col3 = st.columns([1,1,1])
with col2: st.button("▲", on_click=move_player, args=(-1, 0))
c1, c2, c3 = st.columns([1,1,1])
with c1: st.button("◀", on_click=move_player, args=(0, -1))
with c2: st.button("▼", on_click=move_player, args=(1, 0))
with c3: st.button("▶", on_click=move_player, args=(0, 1))

# 7. Render Maze with the Dynamic Target
grid_html = ""
for r_idx, row in enumerate(MAZE):
    for c_idx, char in enumerate(row):
        if r_idx == st.session_state.r and c_idx == st.session_state.c:
            grid_html += "🤖" # Robot
        elif (r_idx, r_idx == st.session_state.target[0] and c_idx == st.session_state.target[1]):
            grid_html += "🟡" # The Random Target
        elif char == "X":
            grid_html += "🟦" # Wall
        else:
            grid_html += "⬜" # Path
    grid_html += "\n"

st.markdown(f'<div class="maze-container">{grid_html}</div>', unsafe_allow_html=True)

# 8. Success Branding
if (st.session_state.r, st.session_state.c) == st.session_state.target:
    st.markdown(f"""
        <div style="background-color:#00ffcc; padding:20px; border-radius:15px; text-align:center; border: 2px solid #1a1a40; margin-top: 20px;">
            <h2 style="color:#1a1a40; margin:0;">🏆 TARGET REACHED! 🏆</h2>
            <p style="color:#1a1a40; font-size:18px;">Mastered in {st.session_state.moves} moves.</p>
            <h3 style="color:#ff0066;">Learn python with Prerna Khandelwal</h3>
        </div>
    """, unsafe_allow_html=True)
    
    encoded_text = urllib.parse.quote(f"I beat the random maze in {st.session_state.moves} moves! I want a trial.")
    whatsapp_url = f"https://wa.me/918949803950?text={encoded_text}"
    st.link_button("🟢 Chat on WhatsApp to Enroll", whatsapp_url, use_container_width=True)
    
    # Reset button for a new game
    if st.button("Play Again (New Random Target)"):
        del st.session_state['target']
        st.session_state.r, st.session_state.c = 1, 1
        st.session_state.moves = 0
        st.rerun()
