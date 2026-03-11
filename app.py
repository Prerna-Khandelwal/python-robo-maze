import streamlit as st
import urllib.parse

# 1. Page Configuration
st.set_page_config(page_title="Robo-Escape", layout="centered")

# 2. Organized Maze Layout (10x8)
# P = Player Start, E = Gold Circle, X = Wall, Space = Path
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

# 3. Game State - This prevents "random" jumping
if 'r' not in st.session_state:
    st.session_state.r, st.session_state.c = 1, 1
if 'moves' not in st.session_state:
    st.session_state.moves = 0

# 4. Movement Logic with Wall Detection
def move_player(dr, dc):
    new_r = st.session_state.r + dr
    new_c = st.session_state.c + dc
    
    # Boundary and Wall Check
    if MAZE[new_r][new_c] == "X":
        # Reset to Start on Wall Hit
        st.session_state.r, st.session_state.c = 1, 1 
        st.toast("🚫 Hit a wall! Back to start!", icon="⚠️")
    else:
        # Move Successfully
        st.session_state.r, st.session_state.c = new_r, new_c
        st.session_state.moves += 1
        if MAZE[new_r][new_c] == "E":
            st.balloons() 

# 5. Professional Styling for Mobile
st.markdown("""
    <style>
    .maze-container {
        font-size: 26px !important;
        font-family: 'Courier New', Courier, monospace;
        line-height: 1.2;
        letter-spacing: 2px;
        text-align: center;
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 15px;
        white-space: pre; /* Keeps the grid organized */
    }
    .stButton button {
        width: 100%;
        height: 60px;
        font-size: 24px !important;
    }
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

# 7. Render the Maze Grid
grid_html = ""
for r_idx, row in enumerate(MAZE):
    for c_idx, char in enumerate(row):
        if r_idx == st.session_state.r and c_idx == st.session_state.c:
            grid_html += "🤖"
        elif char == "X":
            grid_html += "🟦"
        elif char == "E":
            grid_html += "🟡"
        else:
            grid_html += "⬜"
    grid_html += "\n"

st.markdown(f'<div class="maze-container">{grid_html}</div>', unsafe_allow_html=True)

# 8. Success Branding & WhatsApp Integration
if MAZE[st.session_state.r][st.session_state.c] == "E":
    st.markdown(f"""
        <div style="background-color:#00ffcc; padding:20px; border-radius:15px; text-align:center; border: 2px solid #1a1a40; margin-top: 20px;">
            <h2 style="color:#1a1a40; margin:0;">🏆 YOU ESCAPED! 🏆</h2>
            <p style="color:#1a1a40; font-size:18px;">Mastered in {st.session_state.moves} moves.</p>
            <h3 style="color:#ff0066;">Prerna Khandelwal's Python Academy</h3>
        </div>
    """, unsafe_allow_html=True)
    
    encoded_text = urllib.parse.quote(f"I beat the Robo-Maze in {st.session_state.moves} moves! I'd like a free Python trial.")
    whatsapp_url = f"https://wa.me/918949803950?text={encoded_text}"
    st.link_button("🟢 Chat with Teacher on WhatsApp", whatsapp_url, use_container_width=True)
