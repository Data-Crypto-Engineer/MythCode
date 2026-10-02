"""
MythCode — Adaptive Multi-Agent Fantasy Adventure & Experiential Programming Learning Platform.
Frontend: Streamlit | Multi-Agent Orchestration: CrewAI | Storage: SQLite
"""
import streamlit as st
import time
from core.game_engine import GameEngine
from utils.config import get_app_config
from utils.error_handler import handle_exception

# Page Configuration with storybook aesthetic
st.set_page_config(
    page_title="MythCode — Multi-Agent Fantasy Adventure",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Enchanted CSS Theme (Misty lavender, warm cream, muted gold, forest green)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Crimson+Pro:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@400;600&display=swap');

    .stApp {
        background: linear-gradient(135deg, #0d131a 0%, #151d28 50%, #111a22 100%);
        color: #e6edf3;
        font-family: 'Crimson Pro', Georgia, serif;
        font-size: 1.15rem;
    }

    h1, h2, h3, h4 {
        font-family: 'Cinzel', serif !important;
        letter-spacing: 0.05em;
        color: #f6e05e !important;
    }

    .storybook-banner {
        background: radial-gradient(circle at 50% 30%, rgba(212, 175, 55, 0.15) 0%, rgba(20, 30, 45, 0.95) 100%);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 12px;
        padding: 2.2rem;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }

    .storybook-banner h1 {
        font-size: 2.8rem;
        margin-bottom: 0.3rem;
        text-shadow: 0 0 20px rgba(246, 224, 94, 0.4);
    }

    .storybook-tagline {
        font-style: italic;
        color: #9ae6b4;
        font-size: 1.3rem;
    }

    .scene-card {
        background: rgba(22, 33, 49, 0.85);
        border: 1px solid rgba(154, 230, 180, 0.25);
        border-radius: 10px;
        padding: 1.8rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }

    .speaker-label {
        font-family: 'Cinzel', serif;
        color: #f6e05e;
        font-weight: 700;
        font-size: 1.15rem;
        margin-bottom: 0.4rem;
    }

    .dialogue-box {
        background: rgba(15, 23, 36, 0.9);
        border-left: 4px solid #d4af37;
        padding: 1rem 1.4rem;
        font-style: italic;
        color: #fbd38d;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }

    .python-reveal-box {
        background: #0d1117;
        border: 1px solid #38a169;
        border-radius: 8px;
        padding: 1.2rem;
        margin: 1rem 0;
    }

    .telemetry-card {
        background: rgba(18, 25, 38, 0.95);
        border-left: 3px solid #63b3ed;
        padding: 0.8rem 1.1rem;
        margin-bottom: 0.6rem;
        font-size: 0.92rem;
        border-radius: 0 6px 6px 0;
    }

    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "game_engine" not in st.session_state:
    st.session_state.game_engine = GameEngine(player_id="player_default")

if "game_started" not in st.session_state:
    st.session_state.game_started = False

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

engine = st.session_state.game_engine
config = get_app_config()

# Sidebar: Kingdom World Status & Multi-Agent Telemetry
with st.sidebar:
    st.markdown("### 🏰 Kingdom of Elarion")
    state_dict = engine.state_mgr.load_or_init_world().to_dict()
    player_dict = engine.state_mgr.load_or_init_player().to_dict()
    learning_dict = engine.state_mgr.load_or_init_learning().to_dict()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Water Supply", state_dict.get("water_supply", "damaged").capitalize())
        st.metric("Village Morale", f"{state_dict.get('village_morale', 60)}%")
    with col2:
        st.metric("Spirit Trust", f"{state_dict.get('forest_spirit_trust', 0)} / 10")
        st.metric("Guardian", state_dict.get("clockwork_guardian", "inactive").capitalize())

    st.markdown("---")
    st.markdown("### 🧠 Adaptive Player Model")
    traits = player_dict.get("traits", {})
    st.caption(f"**Challenge Level**: {traits.get('challenge_level', 1)} / 5")
    st.progress(traits.get("exploration_preference", 0.5), text=f"Exploration: {int(traits.get('exploration_preference', 0.5)*100)}%")
    st.progress(traits.get("puzzle_preference", 0.5), text=f"Puzzle Affinity: {int(traits.get('puzzle_preference', 0.5)*100)}%")
    st.progress(traits.get("dialogue_preference", 0.5), text=f"Dialogue: {int(traits.get('dialogue_preference', 0.5)*100)}%")

    st.markdown("---")
    st.markdown("### 🤖 CrewAI Agent Telemetry")
    if st.session_state.last_telemetry:
        for t in st.session_state.last_telemetry:
            st.markdown(f"""
            <div class="telemetry-card">
                <strong style="color: #63b3ed;">{t.get('agent')}:</strong> {t.get('output')}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.caption("Awaiting player action to invoke Director and Agent workflow...")

    st.markdown("---")
    if st.button("🔄 Reset Adventure", help="Resets stored adventure and returns to character creation"):
        engine.reset_game()
        st.session_state.game_started = False
        st.session_state.active_scene = None
        st.session_state.last_telemetry = []
        st.session_state.unlocked_code = None
        st.session_state.puzzle_feedback = None
        st.session_state.selected_seq_steps = []
        st.rerun()

# ----------------- SECTION A & B: WELCOME & CHARACTER CREATION -----------------
if not st.session_state.game_started:
    st.markdown("""
    <div class="storybook-banner">
        <h1>✨ MYTHCODE ✨</h1>
        <div class="storybook-tagline">"An adaptive fantasy world where every choice teaches you something."</div>
        <p style="margin-top: 1rem; color: #cbd5e0; max-width: 650px; margin-left: auto; margin-right: auto;">
            Step into the Kingdom of Elarion. Its ancient mountain springs have gone quiet, and mysterious clockwork sentinels
            await instruction. As you explore, you will discover that magic and computational thinking share the same truth:
            instruction order matters, conditions open locked doors, and loops harmonize the world.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("📜 Chronicle Your Hero")
        char_name = st.text_input("Hero Name", value="Aria", max_chars=30)
        char_role = st.selectbox(
            "Fantasy Calling",
            ["Clockwork Scholar", "Sylvan Wayfarer", "Alchemical Artificer", "Runesmith Apprentice"]
        )
        adventure_style = st.select_slider(
            "Preferred Adventure Demeanor",
            options=["Cautious & Analytical", "Bold & Exploratory", "Diplomatic & Patient", "Experimental & Inquisitive"]
        )

        if st.button("🌟 Embark Into Elarion", type="primary", use_container_width=True):
            engine.initialize_session(name=char_name, role=char_role, style=adventure_style)
            # Execute initial arrival action
            res = engine.execute_action(f"{char_name} arrives in Whispering Village to investigate the dried springs.")
            st.session_state.active_scene = res["scene"]
            st.session_state.last_telemetry = res.get("telemetry", [])
            st.session_state.game_started = True
            st.rerun()

    with col_right:
        st.subheader("📖 The Core Philosophy")
        st.info(
            "**Your choices shape the world. Your world shapes your mind.**\n\n"
            "• **Sequence**: Guide a clockwork sentinel step-by-step through ancient sluice gates.\n"
            "• **Conditions**: Evaluate whether magical conditions allow runic portals to open.\n"
            "• **Loops**: Channel sustained rhythmic pulses to energize water conduits.\n\n"
            "*Each discovered mechanic unlocks real Python programming syntax in The Unwritten Journal.*"
        )

# ----------------- MAIN ADVENTURE INTERFACE -----------------
else:
    scene = st.session_state.active_scene
    if not scene:
        res = engine.execute_action("Look around the current location.")
        scene = res["scene"]
        st.session_state.active_scene = scene
        st.session_state.last_telemetry = res.get("telemetry", [])

    tabs = st.tabs(["🗺️ Adventure Scene", "📖 The Unwritten Journal", "📜 Quest Log", "🧩 Active Challenge"])

    # TAB 1: ADVENTURE SCENE
    with tabs[0]:
        st.markdown(f"""
        <div class="scene-card">
            <span style="font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.1em; color: #68d391;">
                📍 Location: {scene.get('location', state_dict.get('current_location', 'Whispering Village'))}
            </span>
            <h2 style="margin-top: 0.3rem;">{scene.get('scene_title', 'A Moment of Contemplation')}</h2>
            <p>{scene.get('scene_description', '')}</p>
            <div class="dialogue-box">
                <div class="speaker-label">🗣️ {scene.get('speaker', 'Elder Thorne')}:</div>
                "{scene.get('dialogue', 'Traveler, the waters await your wisdom.')}"
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Puzzle feedback or code unlock banner
        if st.session_state.puzzle_feedback:
            is_success = "achieved" in st.session_state.puzzle_feedback.lower() or "evaluates the condition as true" in st.session_state.puzzle_feedback.lower() or "activates" in st.session_state.puzzle_feedback.lower()
            if is_success:
                st.success(f"🌟 **Challenge Mastered!** {st.session_state.puzzle_feedback}")
            else:
                st.warning(f"⚠️ **Notice:** {st.session_state.puzzle_feedback}")

        if st.session_state.unlocked_code:
            reveal = st.session_state.unlocked_code
            st.markdown(f"""
            <div class="python-reveal-box">
                <h4 style="color: #68d391; margin-bottom: 0.4rem;">🐍 Python Concept Discovered: {reveal.get('concept_name')}</h4>
                <p style="color: #cbd5e0; font-size: 1rem;">{reveal.get('explanation')}</p>
            </div>
            """, unsafe_allow_html=True)
            st.code(reveal.get("code_snippet"), language="python")

        st.markdown("### 🏹 What will you do next?")
        choices = scene.get("choices", [])
        cols = st.columns(len(choices) if choices else 1)

        for idx, choice in enumerate(choices):
            with cols[idx]:
                if st.button(f"✨ {choice['text']}", key=f"choice_{choice['id']}_{idx}", use_container_width=True):
                    # Route to challenge tab if puzzle choice
                    if "puzzle" in choice['id']:
                        st.info("Directing focus to the Active Challenge tab...")
                        # Set active tab
                    res = engine.execute_action(choice['text'])
                    st.session_state.active_scene = res["scene"]
                    st.session_state.last_telemetry = res.get("telemetry", [])
                    st.session_state.unlocked_code = res.get("revealed_code")
                    st.session_state.puzzle_feedback = res.get("puzzle_feedback")
                    st.rerun()

    # TAB 2: LEARNING JOURNAL (The Unwritten Journal)
    with tabs[1]:
        st.subheader("📖 The Unwritten Journal")
        st.caption("A living compendium of computational principles unveiled through your actions in Elarion.")

        reveals = learning_dict.get("unlocked_reveals", [])
        if not reveals:
            st.info("No computational arcana has been uncovered yet. Solve challenges at the River Aqueduct, Ancient Grove, or Clockwork Ruins to unlock real Python syntax!")
        else:
            for rev in reveals:
                with st.expander(f"✨ {rev.get('concept_name')}", expanded=True):
                    st.markdown(f"**Principle:** {rev.get('explanation')}")
                    st.code(rev.get("code_snippet"), language="python")

        st.markdown("---")
        st.markdown("#### 📊 Concept Mastery Metrics")
        cm = traits.get("concept_mastery", {})
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.metric("Sequence (Step Order)", f"{int(cm.get('sequence', 0.0)*100)}%")
        with m_col2:
            st.metric("Conditions (if / else)", f"{int(cm.get('conditions', 0.0)*100)}%")
        with m_col3:
            st.metric("Loops (for iterations)", f"{int(cm.get('loops', 0.0)*100)}%")

    # TAB 3: QUEST LOG
    with tabs[2]:
        st.subheader("📜 Quest Log")
        quests = engine.quest_mgr.get_all_quests()
        for q in quests:
            st.markdown(f"### {q.title}")
            st.write(q.description)
            st.markdown(f"**Status:** {'✅ Resolved' if q.completed else '⏳ In Progress'}")

            st.markdown("#### 🗺️ Available Pathways:")
            for p in q.pathways:
                st.markdown(f"- **{p.title}** ({p.location}): {p.description}")

    # TAB 4: ACTIVE CHALLENGE (Playable Puzzles)
    with tabs[3]:
        st.subheader("🧩 Ancient Runic Challenges")
        st.caption("Interact with the mechanisms of Elarion using structured actions. Observe how logic dictates the outcome.")

        puz_choice = st.selectbox(
            "Select Challenge to Attempt:",
            [
                ("puzzle_sequence_guardian", "Stage 1: Clockwork Guardian (Sequence)"),
                ("puzzle_conditional_door", "Stage 2: Sylvan Runic Gateway (Conditions)"),
                ("puzzle_loop_tiles", "Stage 3: Resonating Conduits of Five (Loops)")
            ],
            format_func=lambda x: x[1]
        )
        puz_id = puz_choice[0]
        puzzle = engine.learning_engine.get_puzzle(puz_id)

        if puzzle:
            st.markdown(f"### {puzzle.title}")
            st.write(puzzle.description)

            # Puzzle 1: Sequence
            if puz_id == "puzzle_sequence_guardian":
                st.info("Assemble the exact sequence of 4 movement commands to guide the guardian to the altar.")
                col_btn1, col_btn2, col_btn3, col_clear = st.columns(4)
                with col_btn1:
                    if st.button("⬆️ FORWARD"):
                        st.session_state.selected_seq_steps.append("FORWARD")
                with col_btn2:
                    if st.button("➡️ TURN RIGHT"):
                        st.session_state.selected_seq_steps.append("TURN_RIGHT")
                with col_btn3:
                    if st.button("⬅️ TURN LEFT"):
                        st.session_state.selected_seq_steps.append("TURN_LEFT")
                with col_clear:
                    if st.button("🧹 Clear Steps"):
                        st.session_state.selected_seq_steps = []

                st.write(f"**Current Program Sequence:** `{' ➔ '.join(st.session_state.selected_seq_steps) if st.session_state.selected_seq_steps else 'Empty'}`")

                if st.button("⚡ Execute Program Sequence", type="primary"):
                    res = engine.solve_challenge(puz_id, st.session_state.selected_seq_steps)
                    st.session_state.active_scene = res["scene"]
                    st.session_state.last_telemetry = res.get("telemetry", [])
                    st.session_state.puzzle_feedback = res.get("puzzle_feedback")
                    st.session_state.unlocked_code = res.get("revealed_code")
                    st.rerun()

            # Puzzle 2: Conditions
            elif puz_id == "puzzle_conditional_door":
                options = puzzle.available_options or []
                selected_opt = st.radio(
                    "Evaluate Condition for the Runic Portal:",
                    options,
                    format_func=lambda opt: opt["label"]
                )
                if st.button("✨ Evaluate Condition", type="primary"):
                    res = engine.solve_challenge(puz_id, selected_opt["id"])
                    st.session_state.active_scene = res["scene"]
                    st.session_state.last_telemetry = res.get("telemetry", [])
                    st.session_state.puzzle_feedback = res.get("puzzle_feedback")
                    st.session_state.unlocked_code = res.get("revealed_code")
                    st.rerun()

            # Puzzle 3: Loops
            elif puz_id == "puzzle_loop_tiles":
                loop_action = st.radio(
                    "Choose Energy Channeling Strategy:",
                    [
                        ("LOOP_5_STEPS", "🔁 Channel a 5-step repetitive loop across all tiles (for step in range(5))"),
                        ("STEP_ONCE_AND_STOP", "⚡ Send a single solitary pulse into tile 1 only"),
                        ("RANDOM_JUMP", "🎲 Emit random erratic pulses")
                    ],
                    format_func=lambda x: x[1]
                )
                if st.button("🌀 Activate Conduit Loop", type="primary"):
                    res = engine.solve_challenge(puz_id, loop_action[0])
                    st.session_state.active_scene = res["scene"]
                    st.session_state.last_telemetry = res.get("telemetry", [])
                    st.session_state.puzzle_feedback = res.get("puzzle_feedback")
                    st.session_state.unlocked_code = res.get("revealed_code")
                    st.rerun()

            # Pedagogical Hint button
            if st.button("💡 Consult the Arcane Archives for a Hint"):
                hint_data = engine.get_hint(puz_id)
                st.info(f"**Hint:** {hint_data['hint']}")
