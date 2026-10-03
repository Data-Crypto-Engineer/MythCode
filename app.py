"""
MythCode — Chapter I: The Silence of the Springs
A playable fantasy adventure where every spell is a program and every decision shapes the world.
Frontend: Streamlit Storybook UI | Engine: MythCode GameEngine | Storage: SQLite & JSON Backup
"""
import streamlit as st
import time
from core.game_engine import GameEngine
from utils.config import get_app_config
from utils.cloudflare_images import get_image_service

# 1. Page Configuration
st.set_page_config(
    page_title="MythCode — The Silence of the Springs",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Warm Fantasy Storybook Visual System (Parchment, Soft Lavender, Sage, Muted Gold, Peach, Deep Ink)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Crimson+Pro:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@400;600&display=swap');

    .stApp {
        background-color: #F8F4EB;
        background-image: radial-gradient(#E8DFC8 1px, transparent 1px);
        background-size: 26px 26px;
        color: #2D251E;
        font-family: 'Crimson Pro', Georgia, serif;
        font-size: 1.2rem;
        line-height: 1.65;
    }

    /* Fantasy Storybook Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Cinzel', Georgia, serif !important;
        color: #4A3525 !important;
        letter-spacing: 0.03em;
    }

    /* Storybook Chapter Banner */
    .storybook-header {
        background: linear-gradient(135deg, #FFFDF9 0%, #F5ECE0 55%, #EFE1D0 100%);
        border: 2px solid #D7B978;
        border-radius: 16px;
        padding: 2.2rem 2.4rem;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 6px 24px rgba(74, 53, 37, 0.08);
    }

    .storybook-title {
        font-size: 2.8rem;
        font-family: 'Cinzel', serif;
        color: #4A3525;
        font-weight: 800;
        margin-bottom: 0.3rem;
        letter-spacing: 0.05em;
    }

    .storybook-subtitle {
        font-style: italic;
        color: #6B7A60;
        font-size: 1.25rem;
        margin-bottom: 0.8rem;
    }

    /* Main Scene Parchment Page */
    .parchment-scene {
        background: #FFFFFF;
        border: 1px solid #E2D5C3;
        border-left: 6px solid #D7B978;
        border-radius: 14px;
        padding: 2.2rem;
        margin-bottom: 1.6rem;
        box-shadow: 0 4px 20px rgba(70, 50, 30, 0.06);
    }

    .chapter-tag {
        font-family: 'Cinzel', serif;
        font-size: 0.88rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #7B8F72;
        font-weight: 700;
        margin-bottom: 0.4rem;
    }

    /* Character Dialogue Frame */
    .dialogue-card {
        background: #FAF6EE;
        border: 1px solid #E8DFD1;
        border-left: 4px solid #7B8F72;
        padding: 1.3rem 1.7rem;
        color: #382F26;
        border-radius: 0 12px 12px 0;
        margin: 1.4rem 0;
        font-style: italic;
        font-size: 1.15rem;
    }

    .speaker-name {
        font-family: 'Cinzel', serif;
        color: #5C4033;
        font-weight: 700;
        font-size: 1.15rem;
        font-style: normal;
        margin-bottom: 0.3rem;
    }

    /* Interaction & Immediate Feedback Card */
    .feedback-banner {
        background: #F4EFE6;
        border: 1px solid #D7B978;
        border-radius: 10px;
        padding: 1rem 1.4rem;
        margin: 1.2rem 0;
        font-size: 1.08rem;
        color: #4A3525;
    }

    /* In-world Magical Mechanism Dais */
    .mechanism-dais {
        background: linear-gradient(135deg, #FAF6EE 0%, #F5ECE0 100%);
        border: 2px solid #8A72B8;
        border-radius: 14px;
        padding: 1.8rem;
        margin: 1.5rem 0;
        box-shadow: 0 6px 18px rgba(138, 114, 184, 0.12);
    }

    /* Scroll of Arcane Discovery */
    .discovery-scroll {
        background: #FFFDF9;
        border: 2px solid #7B8F72;
        border-radius: 12px;
        padding: 1.6rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 16px rgba(123, 143, 114, 0.15);
    }

    /* Story Buttons */
    .stButton>button {
        font-family: 'Crimson Pro', Georgia, serif !important;
        font-size: 1.12rem !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.2rem !important;
        transition: all 0.25s ease !important;
    }

    /* Hero Badge in Sidebar */
    .hero-badge {
        background: #FFFDF9;
        border: 1px solid #D7B978;
        border-radius: 12px;
        padding: 1.1rem;
        margin-bottom: 1.2rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(74, 53, 37, 0.05);
    }

    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Session State Initialization
if "game_engine" not in st.session_state:
    st.session_state.game_engine = GameEngine(player_id="player_hero")

if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "active_scene" not in st.session_state:
    st.session_state.active_scene = None

if "last_action_feedback" not in st.session_state:
    st.session_state.last_action_feedback = None

if "queued_runes" not in st.session_state:
    st.session_state.queued_runes = []

if "puzzle_solved_flag" not in st.session_state:
    st.session_state.puzzle_solved_flag = False

if "show_codex" not in st.session_state:
    st.session_state.show_codex = False

if "show_backup" not in st.session_state:
    st.session_state.show_backup = False

engine: GameEngine = st.session_state.game_engine
image_service = get_image_service()
config = get_app_config()

# Helper: Generate clean avatar SVG
def get_character_portrait_svg(affinity: str, hair_color: str) -> str:
    color_map = {
        "Nature": "#7B8F72", "Light": "#E0C870", "Water": "#6EA8B8",
        "Fire": "#C96D57", "Wind": "#92B8A0", "Arcane": "#8A72B8"
    }
    aura = color_map.get(affinity, "#8A72B8")
    hair_map = {
        "Auburn": "#8B4513", "Silver": "#A8A8A8", "Midnight Black": "#202020",
        "Golden": "#DAA520", "Emerald": "#2E8B57"
    }
    h_col = hair_map.get(hair_color, "#8B4513")
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 140 140" width="100%" height="100%">
        <circle cx="70" cy="70" r="66" fill="#FAF6EE" stroke="{aura}" stroke-width="4" />
        <circle cx="70" cy="70" r="58" fill="none" stroke="{aura}" stroke-width="1.5" stroke-dasharray="3,3" opacity="0.6" />
        <path d="M30,130 C40,102 100,102 110,130 Z" fill="{aura}" opacity="0.85" />
        <circle cx="70" cy="60" r="25" fill="#FADBC8" />
        <path d="M45,56 C45,36 95,36 95,56 C95,42 45,42 45,56 Z" fill="{h_col}" />
        <circle cx="62" cy="59" r="2.5" fill="#362E3B" />
        <circle cx="78" cy="59" r="2.5" fill="#362E3B" />
        <path d="M66,69 Q70,72 74,69" stroke="#362E3B" stroke-width="1.5" fill="none" />
        <circle cx="106" cy="106" r="14" fill="#FFFFFF" stroke="#D7B978" stroke-width="2" />
        <text x="106" y="111" font-size="12" text-anchor="middle">✨</text>
    </svg>
    """

# 4. Sidebar: Realm Status & Character Presence
with st.sidebar:
    st.markdown("### 🏰 Kingdom of Elarion")
    state_dict = engine.state_mgr.load_or_init_world().to_dict()
    player_dict = engine.state_mgr.load_or_init_player().to_dict()
    learning_dict = engine.state_mgr.load_or_init_learning().to_dict()

    if st.session_state.game_started:
        st.markdown(f"""
        <div class="hero-badge">
            <div style="font-size: 1.3rem; font-weight: 700; color: #4A3525; font-family: 'Cinzel', serif;">
                {player_dict.get('name', 'Aria')}
            </div>
            <div style="font-size: 0.95rem; color: #7B8F72; font-weight: 600;">
                {player_dict.get('role', 'Rune Engineer')} &bull; Level {player_dict.get('level', 1)}
            </div>
            <div style="font-size: 0.85rem; color: #5C4033; margin-top: 0.4rem;">
                Attuned to <strong>{player_dict.get('magical_affinity', 'Arcane')}</strong> Arcana
            </div>
            <div style="font-size: 0.85rem; color: #6B7A60; margin-top: 0.2rem;">
                Companion: <strong>{player_dict.get('companion', 'Clockwork Owl')}</strong>
            </div>
            <div style="font-size: 0.85rem; color: #8A72B8; margin-top: 0.2rem;">
                Keepsake: <em>{player_dict.get('keepsake', 'Brass Chrono-Gear')}</em>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_w1, col_w2 = st.columns(2)
        with col_w1:
            st.metric("Water Supply", state_dict.get("water_supply", "damaged").capitalize())
            st.metric("Village Morale", f"{state_dict.get('village_morale', 60)}%")
        with col_w2:
            st.metric("Experience", f"{player_dict.get('xp', 0)} XP")
            st.metric("Guardian", state_dict.get("clockwork_guardian", "inactive").capitalize())

        st.markdown("---")
        # Quiet Storybook Navigation Folios
        codex_btn_label = "📖 Close The Codex" if st.session_state.show_codex else "📖 The Codex of Becoming"
        if st.button(codex_btn_label, use_container_width=True):
            st.session_state.show_codex = not st.session_state.show_codex
            st.rerun()

        backup_btn_label = "💾 Close Backup" if st.session_state.show_backup else "💾 Backup & Restore"
        if st.button(backup_btn_label, use_container_width=True):
            st.session_state.show_backup = not st.session_state.show_backup
            st.rerun()

        st.markdown("---")
        if st.button("🔄 Begin Anew", help="Resets adventure and restarts character chronicle"):
            engine.reset_game()
            st.session_state.game_started = False
            st.session_state.active_scene = None
            st.session_state.last_action_feedback = None
            st.session_state.queued_runes = []
            st.session_state.puzzle_solved_flag = False
            st.session_state.show_codex = False
            st.session_state.show_backup = False
            st.rerun()

    else:
        st.info("Chronicle your hero to embark upon Chapter I: The Silence of the Springs.")

# ================= CHAPTER I: CHARACTER CHRONICLE =================
if not st.session_state.game_started:
    st.markdown("""
    <div class="storybook-header">
        <div class="storybook-title">✨ MYTHCODE ✨</div>
        <div class="storybook-subtitle">"Every spell is a program. Every decision changes the world."</div>
        <p style="color: #4A3525; max-width: 720px; margin: 0 auto; font-size: 1.15rem;">
            Welcome to the Kingdom of Elarion. Its ancient mountain springs have gone quiet, and mysterious
            clockwork mechanisms await instruction. Through exploration, dialogue, and runic puzzle-solving,
            you will discover the foundational laws of computation through the living magic of the world.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📜 Chronicle Your Hero")
    col_c1, col_c2 = st.columns([1.3, 0.7])

    with col_c1:
        c1, c2 = st.columns(2)
        with c1:
            hero_name = st.text_input("Hero Name", value="Aria", max_chars=30)
            hero_role = st.selectbox(
                "Fantasy Calling",
                ["Rune Engineer", "Spellweaver", "Forest Guardian", "Star Cartographer", "Alchemist", "Shadow Explorer"]
            )
            hero_affinity = st.selectbox(
                "Primary Magical Affinity",
                ["Arcane", "Nature", "Water", "Light", "Fire", "Wind"]
            )

        with c2:
            hero_companion = st.selectbox(
                "Familiar Companion",
                ["Clockwork Owl", "Sylvan Sprite", "Runestone Fox", "Ember Salamander", "Zephyr Finch"]
            )
            hero_keepsake = st.selectbox(
                "Starting Keepsake",
                ["Brass Chrono-Gear", "Dried Star-Blossom", "River Prism", "Carved Rune-Tablet", "Alchemical Vial"]
            )
            hero_hair = st.selectbox("Hair Color", ["Auburn", "Silver", "Midnight Black", "Golden", "Emerald"])

        hero_pronouns = st.selectbox("Pronouns", ["they/them", "she/her", "he/him", "ze/zir", "custom"])

        if st.button("🌟 Embark Into Whispering Village", type="primary", use_container_width=True):
            engine.initialize_session(
                name=hero_name,
                pronouns=hero_pronouns,
                role=hero_role,
                magical_affinity=hero_affinity,
                companion=hero_companion,
                keepsake=hero_keepsake,
                hair_color=hero_hair
            )
            # Initial arrival into Chapter 1
            res = engine.execute_action(
                f"{hero_name} arrives in Whispering Village to investigate the silent springs.",
                action_id="examine_fountain"
            )
            st.session_state.active_scene = res["scene"]
            st.session_state.last_action_feedback = f"You arrive at Whispering Village as the morning mist parts. The central fountain is eerily silent."
            st.session_state.game_started = True
            st.rerun()

    with col_c2:
        st.markdown("#### Hero Portrait Preview")
        portrait_html = get_character_portrait_svg(hero_affinity, hero_hair)
        st.components.v1.html(portrait_html, height=160)
        st.caption(f"**{hero_name}** the *{hero_role}*, attuned to **{hero_affinity}** arcana, accompanied by a loyal **{hero_companion}**.")

# ================= CHAPTER I: PLAYABLE VERTICAL SLICE =================
else:
    scene = st.session_state.active_scene
    if not scene:
        res = engine.execute_action("Look around Whispering Village.", action_id="examine_fountain")
        scene = res["scene"]
        st.session_state.active_scene = scene

    # 1. Expandable Codex of Becoming Folio (Quiet, elegant)
    if st.session_state.show_codex:
        st.markdown("""
        <div class="discovery-scroll">
            <h3 style="margin-top: 0; color: #4A3525;">📖 THE CODEX OF BECOMING</h3>
            <p style="color: #6B7A60; font-style: italic; margin-bottom: 1rem;">
                Your living compendium of computational principles unveiled through magical discovery.
            </p>
        </div>
        """, unsafe_allow_html=True)

        cod_tab1, cod_tab2, cod_tab3 = st.tabs(["✨ Discoveries", "🏆 Masteries", "📜 Your Craft (Python Spells)"])
        with cod_tab1:
            enc = learning_dict.get("concepts_encountered", [])
            if not enc:
                st.info("No concepts encountered yet. Explore the River Aqueduct and interact with the ancient mechanisms!")
            else:
                for c in enc:
                    st.markdown(f"🌿 **Concept Encountered:** {c.capitalize()} — Discovered through Elarion's magical mechanisms.")

        with cod_tab2:
            masteries = [e for e in learning_dict.get("codex_entries", []) if e.get("category") == "mastery"]
            if not masteries:
                st.info("No masteries etched yet. Successfully align an ancient mechanism to demonstrate mastery!")
            else:
                for m in masteries:
                    st.success(f"🏅 **{m.get('title')}**\n\n*Lore:* {m.get('fantasy_lore')}\n\n*Computer Science Principle:* {m.get('programming_concept')}")

        with cod_tab3:
            reveals = learning_dict.get("unlocked_reveals", [])
            if not reveals:
                st.info("No Python spells unlocked yet. Solve the Clockwork Sentinel's sequence to reveal real code syntax!")
            else:
                for r in reveals:
                    st.markdown(f"#### 🐍 Spell Formula: {r.get('concept_name')}")
                    st.write(r.get("explanation"))
                    st.code(r.get("code_snippet"), language="python")

        st.markdown("---")

    # 2. Expandable Backup / Restore Folio
    if st.session_state.show_backup:
        st.markdown("### 💾 Adventure Backup & Recovery")
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.markdown("#### Export Current Journey")
            b_json = engine.export_backup()
            st.download_button(
                "📥 Download Adventure Backup (.json)",
                data=b_json,
                file_name="mythcode_save.json",
                mime="application/json",
                use_container_width=True
            )
        with col_b2:
            st.markdown("#### Restore Journey")
            up = st.file_uploader("Upload Backup (.json)", type=["json"])
            if up is not None:
                if st.button("Restore State from File", type="primary", use_container_width=True):
                    ok = engine.import_backup(up.read().decode("utf-8"))
                    if ok:
                        st.success("Adventure restored!")
                        st.session_state.show_backup = False
                        st.rerun()
        st.markdown("---")

    # 3. Main Scene Illustration
    current_location = scene.get('location', state_dict.get('current_location', 'Whispering Village'))
    illustration_category = "water_spring" if state_dict.get("water_supply") == "restored" and current_location == "Whispering Village" else current_location
    illus_url = image_service.get_illustration(illustration_category)
    if illus_url:
        st.image(illus_url, use_container_width=True)

    # 4. Immediate Action Feedback Banner (Requirement 5: Visible feedback after every interaction)
    if st.session_state.last_action_feedback:
        st.markdown(f"""
        <div class="feedback-banner">
            ✨ {st.session_state.last_action_feedback}
        </div>
        """, unsafe_allow_html=True)

    # 5. The Parchment Scene (Atmospheric narrative and in-character dialogue)
    st.markdown(f"""
    <div class="parchment-scene">
        <div class="chapter-tag">
            {scene.get('chapter', 'Chapter I: The Silence of the Springs')} &bull; Region: {current_location}
        </div>
        <h2 style="margin-top: 0; color: #4A3525;">{scene.get('scene_title', 'The Silent Village Square')}</h2>
        <p style="color: #362E3B; font-size: 1.18rem; line-height: 1.75;">
            {scene.get('scene_description', '')}
        </p>
        <div class="dialogue-card">
            <div class="speaker-name">🗣️ {scene.get('speaker', 'Mira the Inventor')}:</div>
            "{scene.get('dialogue', '')}"
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 6. IN-WORLD PUZZLE INTERACTION: The Clockwork Sentinel's Command Dais
    # (Requirement: Encountered naturally as part of the world, NOT a separate dashboard tab)
    is_at_sentinel = (
        scene.get("active_challenge") == "puzzle_sequence_guardian" or
        "sentinel" in scene.get("scene_title", "").lower() or
        "altar" in scene.get("scene_title", "").lower()
    )

    if is_at_sentinel and state_dict.get("clockwork_guardian") != "operational":
        st.markdown("""
        <div class="mechanism-dais">
            <h3 style="margin-top: 0; color: #5C4033;">⚙️ The Sentinel's Command Dais</h3>
            <p style="color: #4A3525; font-size: 1.12rem;">
                The silver wheel shudders in the river chasm. Three runes illuminate faintly across the Clockwork Sentinel's chest.
                Before it lies a 3&times;3 checkered stone pathway leading to the waterwheel clutch.
                Slot four movement commands into the dais in the exact order required to guide the sentinel forward twice, pivot right, and advance to the altar.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # In-world rune command buttons
        c_btn1, c_btn2, c_btn3, c_btn4 = st.columns(4)
        with c_btn1:
            if st.button("⬆️ Forward", use_container_width=True):
                st.session_state.queued_runes.append("FORWARD")
                st.session_state.last_action_feedback = "You slot an [⬆️ Forward] rune into the dais. The sentinel's internal gears click softly in anticipation."
                st.rerun()

        with c_btn2:
            if st.button("➡️ Turn Right", use_container_width=True):
                st.session_state.queued_runes.append("TURN_RIGHT")
                st.session_state.last_action_feedback = "You slot a [➡️ Turn Right] rune into the dais. A directional gear pivots with a soft chime."
                st.rerun()

        with c_btn3:
            if st.button("⬅️ Turn Left", use_container_width=True):
                st.session_state.queued_runes.append("TURN_LEFT")
                st.session_state.last_action_feedback = "You slot a [⬅️ Turn Left] rune into the dais. A directional gear clicks counter-clockwise."
                st.rerun()

        with c_btn4:
            if st.button("🧹 Clear Runes", use_container_width=True):
                st.session_state.queued_runes = []
                st.session_state.last_action_feedback = "You lift the brass locking pin. The command slots clear and reset."
                st.rerun()

        # Display currently slotted runes
        formatted_stack = " ➔ ".join([f"**[{r}]**" for r in st.session_state.queued_runes]) if st.session_state.queued_runes else "*No runes queued yet...*"
        st.markdown(f"**Slotted Rune Sequence:** {formatted_stack}")

        # Engage mechanism button
        if st.button("⚡ Engage Mechanism & Execute Sequence", type="primary", use_container_width=True):
            res = engine.solve_challenge("puzzle_sequence_guardian", st.session_state.queued_runes)
            st.session_state.active_scene = res["scene"]

            if res.get("puzzle_correct"):
                st.session_state.puzzle_solved_flag = True
                st.session_state.last_action_feedback = (
                    "The gears mesh smoothly! The Clockwork Sentinel glides forward, pivots sharply right, and locks its brass hand "
                    "into the clutch pedestal! The sluice gate bursts open, and mountain springwater rushes down into Whispering Village!"
                )
            else:
                st.session_state.last_action_feedback = (
                    "The sentinel takes a stride, halts abruptly, and its runes flicker red before resetting. "
                    "The terrain requires two steps forward into the corridor before pivoting right!"
                )
            st.rerun()

    # 7. NATURAL LEARNING REVELATION (Only shown AFTER solving the mechanism)
    if st.session_state.puzzle_solved_flag and state_dict.get("clockwork_guardian") == "operational":
        st.markdown("""
        <div class="discovery-scroll">
            <h3 style="margin-top: 0; color: #7B8F72;">✨ Arcane Discovery: The Law of Sequence</h3>
            <p style="font-size: 1.15rem; color: #382F26; line-height: 1.7;">
                The sentinel responded because your commands were arranged into a purposeful, unbroken sequence.
                Order of execution made all the difference—swapping any instruction would have steered the sentinel into the gorge.
            </p>
            <p style="font-size: 1.15rem; color: #4A3525; line-height: 1.7;">
                In the ancient craft—and in real-world <strong>Python programming</strong>—this foundational truth is called a <strong>Sequence</strong>:
                instructions executed step-by-step, line-by-line, in exact chronological order.
            </p>
            <div style="background: #FAF6EE; border-left: 3px solid #7B8F72; padding: 0.8rem 1.2rem; border-radius: 6px; margin: 1rem 0;">
                <code style="color: #2D251E; font-size: 0.95rem;">
                    # Guiding the Clockwork Sentinel<br/>
                    move_forward()<br/>
                    move_forward()<br/>
                    turn_right()<br/>
                    move_forward()<br/>
                    print("Waterwheel clutch released! Mountain springs awakened!")
                </code>
            </div>
            <p style="font-size: 0.98rem; color: #6B7A60; margin-bottom: 0;">
                🌟 <strong>Etched into The Codex of Becoming:</strong> Sequence (+50 XP). The springs of Whispering Village are restored!
            </p>
        </div>
        """, unsafe_allow_html=True)

    # 8. Interactive Choice Buttons with Stable IDs (Requirements 3 & 4: Explicit Choice IDs & Observable Consequences)
    st.markdown("### 🏹 What will you do next?")
    choices = scene.get("choices", [])
    
    # If the puzzle was just solved, inject immediate triumphant continuation choices
    if state_dict.get("clockwork_guardian") == "operational" and current_location == "River Aqueduct":
        choices = [
            {"id": "return_village_triumph", "text": "Follow the cascading water back to Whispering Village to celebrate with Elder Thorne."},
            {"id": "speak_mira", "text": "Confer with Mira beside the spinning waterwheel."},
            {"id": "goto_grove", "text": "Venture north into the Ancient Grove to investigate reports of agitated forest spirits."}
        ]

    cols = st.columns(len(choices) if choices else 1)
    for idx, choice in enumerate(choices):
        with cols[idx]:
            c_id = choice.get("id", f"choice_{idx}")
            c_text = choice.get("text", "")
            if st.button(f"✦ {c_text}", key=f"btn_{c_id}_{idx}", use_container_width=True):
                # Immediate descriptive feedback tailored to the choice
                feedback_map = {
                    "examine_fountain": "You kneel beside the stone basin, tracing runic conduits leading toward the River Gorge.",
                    "speak_mira": "You approach Mira's workbench. She looks up with hope in her eyes.",
                    "ask_mira_clues": "Mira sketches the dais pattern in the stone dust: two paces forward, turn right, one step forward.",
                    "follow_aqueduct": "You take the river path downstream toward the roaring gorge and the seized waterwheel.",
                    "interact_sentinel": "You step onto the stone dais before the Clockwork Sentinel. Its rune sockets await your commands.",
                    "examine_gears": "You examine the massive oak and brass teeth of the seized waterwheel clutch.",
                    "return_village_triumph": "You walk alongside the sparkling, cascading waters back into Whispering Village!",
                    "return_village": "You ascend the stone trail back up into the village square.",
                    "goto_grove": "You journey north into the misty, emerald canopy of the Ancient Grove."
                }
                st.session_state.last_action_feedback = feedback_map.get(c_id, f"You choose to {c_text.lower()}")

                # Execute action via GameEngine using explicit choice ID (Requirement 3)
                res = engine.execute_action(action_text=c_text, action_id=c_id)
                st.session_state.active_scene = res["scene"]
                st.session_state.puzzle_solved_flag = False
                st.rerun()

    # 9. Quiet Leyline Diagnostics (Multi-Agent Telemetry kept discrete, not overwhelming)
    with st.expander("🔮 Arcane Leyline Diagnostics (Multi-Agent Telemetry)"):
        st.caption("Elarion's multi-agent coordination architecture:")
        t_list = st.session_state.get("last_telemetry", [])
        if res_telemetry := getattr(st.session_state.get("active_scene", {}), "get", lambda k, d=None: None)("telemetry"):
            t_list = res_telemetry
        for t in t_list[-4:]:
            st.markdown(f"- **{t.get('agent')}:** {t.get('output')}")
