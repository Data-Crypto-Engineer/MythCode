"""
MythCode — Adaptive Multi-Agent Fantasy Adventure & Experiential Programming Learning Platform.
Architecture: Streamlit Storybook UI | Multi-Agent Coordination | SQLite & JSON Backup | Cloudflare AI & Gemini Layer
"""
import streamlit as st
import time
import json
from core.game_engine import GameEngine
from utils.config import get_app_config
from utils.error_handler import handle_exception
from utils.cloudflare_images import get_image_service

# 1. Page Configuration
st.set_page_config(
    page_title="MythCode — Fantasy Adventure & Programming Learning",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Warm Fantasy Storybook Visual System (PART 11)
# Palette: Warm Parchment (#F7F1E6), Soft Lavender (#DCD2F2), Sage (#C9D8C1), Muted Gold (#D7B978), Peach (#F2CDBD), Ink (#362E3B)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Crimson+Pro:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@400;600&display=swap');

    .stApp {
        background-color: #F8F4EB;
        background-image: radial-gradient(#E8DFC8 1px, transparent 1px);
        background-size: 24px 24px;
        color: #2D251E;
        font-family: 'Crimson Pro', Georgia, serif;
        font-size: 1.18rem;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Cinzel', Georgia, serif !important;
        color: #4A3525 !important;
        letter-spacing: 0.04em;
    }

    /* Storybook Banner */
    .storybook-banner {
        background: linear-gradient(135deg, #FFFDF9 0%, #F5ECE0 60%, #EFE1D0 100%);
        border: 2px solid #D7B978;
        border-radius: 16px;
        padding: 2.2rem;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 30px rgba(90, 70, 50, 0.08);
    }

    .storybook-banner h1 {
        font-size: 2.7rem;
        margin-bottom: 0.2rem;
        color: #5C4033 !important;
    }

    .storybook-tagline {
        font-style: italic;
        color: #6B7A60;
        font-size: 1.25rem;
    }

    /* Scene Card */
    .scene-card {
        background: #FFFFFF;
        border: 1px solid #E2D5C3;
        border-left: 6px solid #D7B978;
        border-radius: 12px;
        padding: 1.8rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(70, 50, 30, 0.06);
    }

    /* Dialogue Bubble */
    .dialogue-box {
        background: #FAF6EE;
        border: 1px solid #E8DFD1;
        border-left: 4px solid #7B8F72;
        padding: 1.2rem 1.6rem;
        font-style: italic;
        color: #382F26;
        border-radius: 0 10px 10px 0;
        margin: 1.2rem 0;
        line-height: 1.65;
    }

    .speaker-label {
        font-family: 'Cinzel', serif;
        color: #5C4033;
        font-weight: 700;
        font-size: 1.15rem;
        margin-bottom: 0.3rem;
    }

    /* Codex & Reveal Box */
    .codex-card {
        background: #FFFFFF;
        border: 1px solid #DCD2F2;
        border-top: 4px solid #8A72B8;
        border-radius: 12px;
        padding: 1.4rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 14px rgba(110, 90, 140, 0.07);
    }

    /* Action Buttons */
    .stButton>button {
        font-family: 'Crimson Pro', Georgia, serif !important;
        font-size: 1.05rem !important;
        border-radius: 10px !important;
        transition: all 0.2s ease !important;
    }

    .sidebar-metric {
        background: #FFFFFF;
        border: 1px solid #E8DFD1;
        border-radius: 10px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
    }

    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Session State Initialization
if "game_engine" not in st.session_state:
    st.session_state.game_engine = GameEngine(player_id="player_default")

if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "active_view" not in st.session_state:
    st.session_state.active_view = "adventure"  # "adventure", "challenges", "codex", "status", "agents", "backup"

if "active_scene" not in st.session_state:
    st.session_state.active_scene = None

if "last_telemetry" not in st.session_state:
    st.session_state.last_telemetry = []

if "puzzle_feedback" not in st.session_state:
    st.session_state.puzzle_feedback = None

if "unlocked_code" not in st.session_state:
    st.session_state.unlocked_code = None

if "selected_seq_steps" not in st.session_state:
    st.session_state.selected_seq_steps = []

if "active_challenge_id" not in st.session_state:
    st.session_state.active_challenge_id = "puzzle_sequence_guardian"

engine: GameEngine = st.session_state.game_engine
image_service = get_image_service()
config = get_app_config()

# Helper for Character SVG Avatar Generation
def generate_character_avatar_svg(name: str, role: str, affinity: str, hair_color: str, companion: str) -> str:
    color_map = {
        "Nature": "#7B8F72",
        "Light": "#E0C870",
        "Water": "#6EA8B8",
        "Fire": "#C96D57",
        "Wind": "#92B8A0",
        "Arcane": "#8A72B8"
    }
    aura_color = color_map.get(affinity, "#8A72B8")
    hair_map = {
        "Auburn": "#8B4513",
        "Silver": "#A8A8A8",
        "Midnight Black": "#202020",
        "Golden": "#DAA520",
        "Emerald": "#2E8B57"
    }
    h_color = hair_map.get(hair_color, "#8B4513")

    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 160" width="100%" height="100%">
        <circle cx="80" cy="80" r="74" fill="#FAF6EE" stroke="{aura_color}" stroke-width="4" />
        <!-- Magical Aura Ring -->
        <circle cx="80" cy="80" r="66" fill="none" stroke="{aura_color}" stroke-width="1.5" stroke-dasharray="4,3" opacity="0.7" />
        <!-- Robe/Shoulders -->
        <path d="M35,145 C45,115 115,115 125,145 Z" fill="{aura_color}" opacity="0.85" />
        <!-- Head -->
        <circle cx="80" cy="68" r="28" fill="#FADBC8" />
        <!-- Hair -->
        <path d="M52,65 C52,40 108,40 108,65 C108,48 52,48 52,65 Z" fill="{h_color}" />
        <circle cx="56" cy="64" r="7" fill="{h_color}" />
        <circle cx="104" cy="64" r="7" fill="{h_color}" />
        <!-- Eyes -->
        <circle cx="71" cy="67" r="3" fill="#362E3B" />
        <circle cx="89" cy="67" r="3" fill="#362E3B" />
        <!-- Gentle smile -->
        <path d="M75,78 Q80,82 85,78" stroke="#362E3B" stroke-width="1.5" fill="none" />
        <!-- Companion Badge on bottom right -->
        <circle cx="120" cy="120" r="16" fill="#FFFFFF" stroke="#D7B978" stroke-width="2" />
        <text x="120" y="125" font-size="14" text-anchor="middle">✨</text>
    </svg>
    """

# 4. Sidebar: Kingdom Status & Navigation
with st.sidebar:
    st.markdown("### 🏰 Kingdom of Elarion")
    state_dict = engine.state_mgr.load_or_init_world().to_dict()
    player_dict = engine.state_mgr.load_or_init_player().to_dict()
    learning_dict = engine.state_mgr.load_or_init_learning().to_dict()

    col_w1, col_w2 = st.columns(2)
    with col_w1:
        st.metric("Water Supply", state_dict.get("water_supply", "damaged").capitalize())
        st.metric("Village Morale", f"{state_dict.get('village_morale', 60)}%")
    with col_w2:
        st.metric("Spirit Trust", f"{state_dict.get('forest_spirit_trust', 0)} / 10")
        st.metric("Guardian", state_dict.get("clockwork_guardian", "inactive").capitalize())

    st.markdown("---")
    st.markdown(f"### 🧙 Hero: {player_dict.get('name', 'Aria')}")
    st.caption(f"**Role:** {player_dict.get('role', 'Rune Engineer')} | **Level {player_dict.get('level', 1)}** ({player_dict.get('xp', 0)} XP)")
    st.caption(f"**Affinity:** {player_dict.get('magical_affinity', 'Arcane')} | **Companion:** {player_dict.get('companion', 'Clockwork Owl')}")

    # Navigation Buttons (PART 3: Observable, reliable navigation)
    st.markdown("---")
    st.markdown("### 🧭 Adventure Navigation")
    
    btn_adv = st.button("🗺️ Story Scene", use_container_width=True, type="primary" if st.session_state.active_view == "adventure" else "secondary")
    if btn_adv:
        st.session_state.active_view = "adventure"
        st.rerun()

    btn_chal = st.button("🧩 Runic Challenges", use_container_width=True, type="primary" if st.session_state.active_view == "challenges" else "secondary")
    if btn_chal:
        st.session_state.active_view = "challenges"
        st.rerun()

    btn_codex = st.button("📖 The Codex of Becoming", use_container_width=True, type="primary" if st.session_state.active_view == "codex" else "secondary")
    if btn_codex:
        st.session_state.active_view = "codex"
        st.rerun()

    btn_status = st.button("📜 Quest Log & Realm", use_container_width=True, type="primary" if st.session_state.active_view == "status" else "secondary")
    if btn_status:
        st.session_state.active_view = "status"
        st.rerun()

    btn_agents = st.button("🤖 Multi-Agent Telemetry", use_container_width=True, type="primary" if st.session_state.active_view == "agents" else "secondary")
    if btn_agents:
        st.session_state.active_view = "agents"
        st.rerun()

    btn_backup = st.button("💾 Backup & Restore", use_container_width=True, type="primary" if st.session_state.active_view == "backup" else "secondary")
    if btn_backup:
        st.session_state.active_view = "backup"
        st.rerun()

    st.markdown("---")
    if st.button("🔄 Reset Adventure", help="Resets stored adventure and returns to character creation"):
        engine.reset_game()
        st.session_state.game_started = False
        st.session_state.active_scene = None
        st.session_state.last_telemetry = []
        st.session_state.unlocked_code = None
        st.session_state.puzzle_feedback = None
        st.session_state.selected_seq_steps = []
        st.session_state.active_view = "adventure"
        st.rerun()

# ----------------- SECTION A: CHARACTER CREATOR (PART 4) -----------------
if not st.session_state.game_started:
    st.markdown("""
    <div class="storybook-banner">
        <h1>✨ MYTHCODE ✨</h1>
        <div class="storybook-tagline">"Every spell is a program. Every decision changes the world."</div>
        <p style="margin-top: 1rem; color: #4A3B32; max-width: 680px; margin-left: auto; margin-right: auto;">
            Step into the Kingdom of Elarion. Its ancient mountain springs have gone quiet, and mysterious clockwork sentinels
            await instruction. As you explore, you will discover that magic and computational thinking share the same truth:
            instruction order matters, conditions open locked doors, and loops harmonize the world.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📜 Chronicle Your Hero (Character Creator)")
    col_c1, col_c2 = st.columns([1.2, 0.8])

    with col_c1:
        c_sub1, c_sub2 = st.columns(2)
        with c_sub1:
            hero_name = st.text_input("Hero Name", value="Aria", max_chars=30)
            hero_pronouns = st.selectbox("Pronouns", ["they/them", "she/her", "he/him", "ze/zir", "custom"])
            hero_role = st.selectbox(
                "Fantasy Calling",
                ["Rune Engineer", "Spellweaver", "Forest Guardian", "Star Cartographer", "Alchemist", "Shadow Explorer"]
            )
            hero_affinity = st.selectbox(
                "Primary Magical Affinity",
                ["Arcane", "Nature", "Water", "Light", "Fire", "Wind"]
            )

        with c_sub2:
            hero_hair = st.selectbox("Hair Color", ["Auburn", "Silver", "Midnight Black", "Golden", "Emerald"])
            hero_companion = st.selectbox(
                "Familiar Companion",
                ["Clockwork Owl", "Sylvan Sprite", "Runestone Fox", "Ember Salamander", "Zephyr Finch"]
            )
            hero_keepsake = st.selectbox(
                "Starting Keepsake",
                ["Brass Chrono-Gear", "Dried Star-Blossom", "River Prism", "Carved Rune-Tablet", "Alchemical Vial"]
            )
            hero_style = st.selectbox(
                "Learning Demeanor",
                ["Hands-on Experimentation", "Visual Step-by-Step", "Theoretical Lore", "Trial & Error Debugging"]
            )

        hero_personality = st.text_input("Personality Trait", value="Curious & Observant")

    with col_c2:
        st.markdown("#### Hero Portrait Preview")
        avatar_svg = generate_character_avatar_svg(hero_name, hero_role, hero_affinity, hero_hair, hero_companion)
        st.components.v1.html(avatar_svg, height=180)
        st.caption(f"**{hero_name}** the *{hero_role}*, attuned to **{hero_affinity}** arcana, accompanied by a faithful **{hero_companion}**.")

    if st.button("🌟 Embark Into Elarion", type="primary", use_container_width=True):
        engine.initialize_session(
            name=hero_name,
            pronouns=hero_pronouns,
            role=hero_role,
            magical_affinity=hero_affinity,
            hair_color=hero_hair,
            companion=hero_companion,
            keepsake=hero_keepsake,
            learning_style=hero_style,
            personality=hero_personality
        )
        res = engine.execute_action(f"{hero_name} arrives in Whispering Village to investigate the dried springs.")
        st.session_state.active_scene = res["scene"]
        st.session_state.last_telemetry = res.get("telemetry", [])
        st.session_state.game_started = True
        st.rerun()

# ----------------- SECTION B: ACTIVE GAMEPLAY VIEWS -----------------
else:
    scene = st.session_state.active_scene
    if not scene:
        res = engine.execute_action("Look around the current location.")
        scene = res["scene"]
        st.session_state.active_scene = scene
        st.session_state.last_telemetry = res.get("telemetry", [])

    # VIEW 1: STORY SCENE (PART 3 & PART 11)
    if st.session_state.active_view == "adventure":
        # Region Storybook Illustration (PART 5)
        current_loc = scene.get('location', state_dict.get('current_location', 'Whispering Village'))
        illustration_url = image_service.get_illustration(current_loc)
        if illustration_url:
            st.image(illustration_url, use_container_width=True)

        st.markdown(f"""
        <div class="scene-card">
            <div style="font-size: 0.95rem; text-transform: uppercase; letter-spacing: 0.08em; color: #7B8F72; font-weight: 600; margin-bottom: 0.4rem;">
                📍 Region: {current_loc}
            </div>
            <h2 style="margin-top: 0; color: #5C4033;">{scene.get('scene_title', 'A Moment of Contemplation')}</h2>
            <p style="color: #362E3B; font-size: 1.15rem; line-height: 1.7;">{scene.get('scene_description', '')}</p>
            <div class="dialogue-box">
                <div class="speaker-label">🗣️ {scene.get('speaker', 'Elder Thorne')}:</div>
                "{scene.get('dialogue', 'Traveler, the waters await your wisdom.')}"
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Feedback & Code Reveal Banners
        if st.session_state.puzzle_feedback:
            is_success = "achieved" in st.session_state.puzzle_feedback.lower() or "true" in st.session_state.puzzle_feedback.lower() or "activates" in st.session_state.puzzle_feedback.lower()
            if is_success:
                st.success(f"🌟 **Arcana Mastered!** {st.session_state.puzzle_feedback}")
            else:
                st.warning(f"⚠️ **Observation:** {st.session_state.puzzle_feedback}")

        if st.session_state.unlocked_code:
            reveal = st.session_state.unlocked_code
            st.markdown(f"""
            <div class="codex-card">
                <h4 style="margin-top: 0; color: #8A72B8;">✨ Runic Spell Revealed: {reveal.get('concept_name')}</h4>
                <p style="font-size: 1.05rem; color: #4A3E50;">{reveal.get('explanation')}</p>
            </div>
            """, unsafe_allow_html=True)
            st.code(reveal.get("code_snippet"), language="python")

        # Interactive Choice Buttons (PART 3: Trace complete path and produce observable results)
        st.markdown("### 🏹 What will you do next?")
        choices = scene.get("choices", [])
        cols = st.columns(len(choices) if choices else 1)

        for idx, choice in enumerate(choices):
            with cols[idx]:
                if st.button(f"✨ {choice['text']}", key=f"choice_btn_{idx}", use_container_width=True):
                    # Check if action is a challenge trigger
                    c_text = choice['text'].lower()
                    if "puzzle" in c_text or "guardian" in c_text or "condition" in c_text or "loop" in c_text:
                        if "guardian" in c_text or "sequence" in c_text:
                            st.session_state.active_challenge_id = "puzzle_sequence_guardian"
                        elif "door" in c_text or "condition" in c_text or "gateway" in c_text:
                            st.session_state.active_challenge_id = "puzzle_conditional_door"
                        elif "loop" in c_text or "tile" in c_text or "repetitive" in c_text:
                            st.session_state.active_challenge_id = "puzzle_loop_tiles"
                        st.session_state.active_view = "challenges"

                    res = engine.execute_action(choice['text'])
                    st.session_state.active_scene = res["scene"]
                    st.session_state.last_telemetry = res.get("telemetry", [])
                    st.session_state.unlocked_code = res.get("revealed_code")
                    st.session_state.puzzle_feedback = res.get("puzzle_feedback")
                    st.rerun()

    # VIEW 2: RUNIC CHALLENGES (PART 8: Playable Educational Gameplay)
    elif st.session_state.active_view == "challenges":
        st.subheader("🧩 Ancient Runic Challenges (Experiential Learning)")
        st.caption("Interact with the mechanisms of Elarion. Notice how logical rules dictate physical reality.")

        puz_choice = st.selectbox(
            "Select Challenge to Attempt:",
            [
                ("puzzle_sequence_guardian", "Stage 1: Clockwork Guardian (Sequence / Order of Commands)"),
                ("puzzle_conditional_door", "Stage 2: Sylvan Runic Gateway (Conditions / if-else Logic)"),
                ("puzzle_loop_tiles", "Stage 3: Resonating Conduits of Five (Loops / Iteration)")
            ],
            index=0 if st.session_state.active_challenge_id == "puzzle_sequence_guardian" else (1 if st.session_state.active_challenge_id == "puzzle_conditional_door" else 2),
            format_func=lambda x: x[1]
        )
        puz_id = puz_choice[0]
        st.session_state.active_challenge_id = puz_id
        puzzle = engine.learning_engine.get_puzzle(puz_id)

        if puzzle:
            st.markdown(f"""
            <div class="scene-card" style="border-left-color: #8A72B8;">
                <h3 style="margin-top: 0; color: #5C4033;">{puzzle.title}</h3>
                <p style="font-size: 1.15rem; color: #362E3B;">{puzzle.description}</p>
            </div>
            """, unsafe_allow_html=True)

            # Puzzle 1: Sequence
            if puz_id == "puzzle_sequence_guardian":
                st.info("Assemble the exact sequence of 4 movement commands to guide the sentinel forward twice, pivot right, and step to the crystal.")
                c_btn1, c_btn2, c_btn3, c_clear = st.columns(4)
                with c_btn1:
                    if st.button("⬆️ FORWARD", use_container_width=True):
                        st.session_state.selected_seq_steps.append("FORWARD")
                with c_btn2:
                    if st.button("➡️ TURN RIGHT", use_container_width=True):
                        st.session_state.selected_seq_steps.append("TURN_RIGHT")
                with c_btn3:
                    if st.button("⬅️ TURN LEFT", use_container_width=True):
                        st.session_state.selected_seq_steps.append("TURN_LEFT")
                with c_clear:
                    if st.button("🧹 Clear", use_container_width=True):
                        st.session_state.selected_seq_steps = []

                st.markdown(f"**Current Command Stack:** `{' ➔ '.join(st.session_state.selected_seq_steps) if st.session_state.selected_seq_steps else 'Empty'}`")

                if st.button("⚡ Execute Sequential Program", type="primary", use_container_width=True):
                    res = engine.solve_challenge(puz_id, st.session_state.selected_seq_steps)
                    st.session_state.active_scene = res["scene"]
                    st.session_state.last_telemetry = res.get("telemetry", [])
                    st.session_state.puzzle_feedback = res.get("puzzle_feedback")
                    st.session_state.unlocked_code = res.get("revealed_code")
                    if res.get("puzzle_correct"):
                        st.session_state.active_view = "adventure"
                    st.rerun()

            # Puzzle 2: Conditions
            elif puz_id == "puzzle_conditional_door":
                options = puzzle.available_options or []
                selected_opt = st.radio(
                    "Evaluate Condition for the Sylvan Portal:",
                    options,
                    format_func=lambda opt: opt["label"]
                )
                if st.button("✨ Evaluate Condition", type="primary", use_container_width=True):
                    res = engine.solve_challenge(puz_id, selected_opt["id"])
                    st.session_state.active_scene = res["scene"]
                    st.session_state.last_telemetry = res.get("telemetry", [])
                    st.session_state.puzzle_feedback = res.get("puzzle_feedback")
                    st.session_state.unlocked_code = res.get("revealed_code")
                    if res.get("puzzle_correct"):
                        st.session_state.active_view = "adventure"
                    st.rerun()

            # Puzzle 3: Loops
            elif puz_id == "puzzle_loop_tiles":
                loop_action = st.radio(
                    "Choose Conduit Energy Channeling Strategy:",
                    [
                        ("LOOP_5_STEPS", "🔁 Channel a 5-step repetitive loop across all tiles: for step in range(5)"),
                        ("STEP_ONCE_AND_STOP", "⚡ Send a single burst into tile 1 only and halt"),
                        ("RANDOM_JUMP", "🎲 Emit random erratic pulses")
                    ],
                    format_func=lambda x: x[1]
                )
                if st.button("🌀 Activate Conduit Loop", type="primary", use_container_width=True):
                    res = engine.solve_challenge(puz_id, loop_action[0])
                    st.session_state.active_scene = res["scene"]
                    st.session_state.last_telemetry = res.get("telemetry", [])
                    st.session_state.puzzle_feedback = res.get("puzzle_feedback")
                    st.session_state.unlocked_code = res.get("revealed_code")
                    if res.get("puzzle_correct"):
                        st.session_state.active_view = "adventure"
                    st.rerun()

            # In-character Pedagogical Hint button
            if st.button("💡 Consult the Arcane Archives for a Hint"):
                hint_data = engine.get_hint(puz_id)
                st.info(f"**Pedagogical Hint:** {hint_data['hint']}")

    # VIEW 3: THE CODEX OF BECOMING (PART 9)
    elif st.session_state.active_view == "codex":
        st.subheader("📖 THE CODEX OF BECOMING")
        st.caption("Your living compendium of computational arcana discovered through your deeds in Elarion.")

        codex_tab1, codex_tab2, codex_tab3 = st.tabs(["✨ Discoveries", "🏆 Masteries", "📜 Your Craft (Python Spells)"])

        with codex_tab1:
            st.markdown("#### Concepts Encountered in the Wild")
            enc = learning_dict.get("concepts_encountered", [])
            if not enc:
                st.info("No concepts encountered yet. Explore the River Aqueduct, Ancient Grove, or Clockwork Ruins!")
            else:
                for c in enc:
                    st.markdown(f"""
                    <div class="codex-card" style="border-top-color: #7B8F72;">
                        <h4 style="margin: 0; color: #4A3525;">🌿 Concept Discovered: {c.capitalize()}</h4>
                        <p style="margin: 0.4rem 0 0 0; color: #554433; font-size: 1.05rem;">
                            Encountered during your journey in Elarion. Practice in the Runic Challenges to achieve full mastery.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

        with codex_tab2:
            st.markdown("#### Demonstrated Computational Masteries")
            masteries = [e for e in learning_dict.get("codex_entries", []) if e.get("category") == "mastery"]
            if not masteries:
                st.info("No masteries achieved yet. Successfully solve a runic trial to etch a mastery into your Codex!")
            else:
                for m in masteries:
                    st.markdown(f"""
                    <div class="codex-card" style="border-top-color: #D7B978;">
                        <h4 style="margin: 0; color: #5C4033;">🏅 {m.get('title')}</h4>
                        <p style="margin: 0.3rem 0; color: #362E3B;"><strong>Lore:</strong> {m.get('fantasy_lore')}</p>
                        <p style="margin: 0.3rem 0; color: #4A3E50;"><strong>Computer Science:</strong> {m.get('programming_concept')}</p>
                    </div>
                    """, unsafe_allow_html=True)

        with codex_tab3:
            st.markdown("#### Accumulated Python Knowledge & Code Spells")
            reveals = learning_dict.get("unlocked_reveals", [])
            if not reveals:
                st.info("No Python spells unlocked yet. Solve the Clockwork Guardian, Sylvan Gateway, or Conduits of Five to unlock real code!")
            else:
                for rev in reveals:
                    with st.expander(f"🐍 {rev.get('concept_name')}", expanded=True):
                        st.markdown(f"**Principle:** {rev.get('explanation')}")
                        st.code(rev.get("code_snippet"), language="python")
                        st.caption("This code represents valid, executable Python syntax mirroring the magical mechanism.")

    # VIEW 4: QUEST LOG & REALM (PART 10)
    elif st.session_state.active_view == "status":
        st.subheader("📜 Quest Log & Realm Status")
        quests = engine.quest_mgr.get_all_quests()
        for q in quests:
            st.markdown(f"### {q.title}")
            st.write(q.description)
            st.markdown(f"**Status:** {'✅ Resolved' if q.completed else '⏳ In Progress'}")

            st.markdown("#### 🗺️ Available Pathways:")
            for p in q.pathways:
                st.markdown(f"- **{p.title}** (*{p.location}*): {p.description}")

        st.markdown("---")
        st.markdown("### 🕊️ Character Memories & Rapport")
        mems = engine.state_mgr.storage.get_character_memories(player_dict.get("id", "player_default"))
        if not mems:
            st.info("No recorded memories yet. As you interact with Mira, Sylvan, and Thorne, your deeds will be remembered.")
        else:
            for m in mems:
                st.markdown(f"- **{m.get('npc_name')}:** {m.get('event_summary')}")

    # VIEW 5: MULTI-AGENT TELEMETRY (PART 7)
    elif st.session_state.active_view == "agents":
        st.subheader("🤖 CrewAI Multi-Agent Architecture")
        st.caption("MythCode uses six specialized agents coordinated with conditional execution and fallback safety.")

        st.markdown("""
        1. **Director Agent:** Interprets actions, aligns quest objectives, and routes story beats.
        2. **Player Insight Agent:** Maintains bounded, evidence-based cognitive & mastery estimates.
        3. **Story Weaver Agent:** Generates evolving prose, dialogue, and choices (with Gemini enrichment).
        4. **World Keeper Agent:** Enforces physical laws, location continuity, and resource clamps.
        5. **Logic & Learning Agent:** Evaluates puzzles deterministically and unlocks Python concepts.
        6. **Continuity & Safety Agent:** Audits content for age appropriateness and state validity.
        """)

        st.markdown("#### Recent Multi-Agent Execution Telemetry:")
        if st.session_state.last_telemetry:
            for t in st.session_state.last_telemetry:
                st.markdown(f"""
                <div class="telemetry-card">
                    <strong style="color: #4A3525;">{t.get('agent')}:</strong> {t.get('output')}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Take an action in the Story Scene to observe live agent telemetry.")

    # VIEW 6: BACKUP & RESTORE (PART 13)
    elif st.session_state.active_view == "backup":
        st.subheader("💾 Backup & Restore Game Data")
        st.caption("Because Streamlit Community Cloud storage can be ephemeral, export your progress as a JSON backup!")

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.markdown("#### Export Progress")
            backup_str = engine.export_backup()
            st.download_button(
                label="📥 Download Game Backup (.json)",
                data=backup_str,
                file_name="mythcode_save_backup.json",
                mime="application/json",
                use_container_width=True
            )
            with st.expander("View Raw Backup JSON"):
                st.code(backup_str, language="json")

        with col_b2:
            st.markdown("#### Restore Progress")
            uploaded_file = st.file_uploader("Upload Saved Backup (.json)", type=["json"])
            if uploaded_file is not None:
                content = uploaded_file.read().decode("utf-8")
                if st.button("🔄 Restore from File", type="primary", use_container_width=True):
                    ok = engine.import_backup(content)
                    if ok:
                        st.success("Successfully restored your saved adventure!")
                        st.session_state.active_view = "adventure"
                        st.rerun()
                    else:
                        st.error("Failed to restore backup. Please verify the JSON file.")
