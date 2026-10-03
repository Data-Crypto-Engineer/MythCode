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
from utils.character_visuals import generate_protagonist_svg

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
        padding: 2rem 2.2rem;
        text-align: center;
        margin-bottom: 1.8rem;
        box-shadow: 0 6px 24px rgba(74, 53, 37, 0.08);
    }

    .storybook-title {
        font-size: 2.6rem;
        font-family: 'Cinzel', serif;
        color: #4A3525;
        font-weight: 800;
        margin-bottom: 0.2rem;
        letter-spacing: 0.05em;
    }

    .storybook-subtitle {
        font-style: italic;
        color: #6B7A60;
        font-size: 1.2rem;
        margin-bottom: 0.6rem;
    }

    /* Character Creation Stanza Container */
    .stanza-card {
        background: #FFFFFF;
        border: 1px solid #E2D5C3;
        border-left: 6px solid #8A72B8;
        border-radius: 14px;
        padding: 2rem;
        margin-bottom: 1.4rem;
        box-shadow: 0 4px 18px rgba(70, 50, 30, 0.06);
    }

    .stanza-step-indicator {
        font-family: 'Cinzel', serif;
        font-size: 0.88rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #8A72B8;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .stanza-lore-quote {
        font-style: italic;
        color: #5C4033;
        font-size: 1.15rem;
        border-left: 3px solid #D7B978;
        padding-left: 1rem;
        margin: 0.8rem 0 1.4rem 0;
    }

    /* Living Protagonist Folio (Right Side Preview) */
    .living-folio-card {
        background: linear-gradient(145deg, #FFFDF9 0%, #FAF6EE 100%);
        border: 2px solid #D7B978;
        border-radius: 16px;
        padding: 1.6rem;
        text-align: center;
        box-shadow: 0 6px 20px rgba(74, 53, 37, 0.08);
    }

    .folio-title {
        font-family: 'Cinzel', serif;
        font-size: 1.35rem;
        font-weight: 700;
        color: #4A3525;
        margin-bottom: 0.2rem;
    }

    .folio-subtitle {
        font-size: 0.95rem;
        color: #7B8F72;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }

    .folio-field-box {
        background: #F4EFE6;
        border: 1px solid #E2D5C3;
        border-radius: 8px;
        padding: 0.5rem 0.8rem;
        margin: 0.4rem 0;
        font-size: 0.95rem;
        text-align: left;
        color: #382F26;
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

# Character Creation Wizard State
if "cc_step" not in st.session_state:
    st.session_state.cc_step = 1

if "cc_name" not in st.session_state:
    st.session_state.cc_name = "Aria"

if "cc_pronouns" not in st.session_state:
    st.session_state.cc_pronouns = "they/them"

if "cc_demeanor" not in st.session_state:
    st.session_state.cc_demeanor = "Scholarly & contemplative, observing the world with keen curiosity"

if "cc_complexion" not in st.session_state:
    st.session_state.cc_complexion = "Sun-kissed bronze"

if "cc_gaze" not in st.session_state:
    st.session_state.cc_gaze = "Amber gold"

if "cc_hair_style" not in st.session_state:
    st.session_state.cc_hair_style = "Braided Crown"

if "cc_hair_color" not in st.session_state:
    st.session_state.cc_hair_color = "Auburn"

if "cc_outfit" not in st.session_state:
    st.session_state.cc_outfit = "Leather Scholar Coat"

if "cc_role" not in st.session_state:
    st.session_state.cc_role = "Rune Engineer"

if "cc_personality" not in st.session_state:
    st.session_state.cc_personality = "Curious & Patient"

if "cc_affinity" not in st.session_state:
    st.session_state.cc_affinity = "Arcane"

if "cc_learning_style" not in st.session_state:
    st.session_state.cc_learning_style = "Hands-on Experimentation"

if "cc_companion" not in st.session_state:
    st.session_state.cc_companion = "Clockwork Owl"

if "cc_keepsake" not in st.session_state:
    st.session_state.cc_keepsake = "Brass Chrono-Gear"

engine: GameEngine = st.session_state.game_engine
image_service = get_image_service()
config = get_app_config()

# Safe multi-version wrappers to prevent signature TypeErrors across hot-reloads and deployments
def safe_execute_action(eng: GameEngine, action_text: str, action_id: str = None) -> dict:
    """Safely dispatches action to GameEngine with multi-version signature tolerance."""
    if action_id:
        try:
            return eng.execute_action(action_text, action_id=action_id)
        except TypeError:
            try:
                return eng.execute_action(action_text, "exploration", action_id)
            except TypeError:
                pass
    return eng.execute_action(action_text)

def safe_initialize_session(eng: GameEngine, **kwargs):
    """Safely initializes player session with multi-version signature tolerance."""
    try:
        return eng.initialize_session(**kwargs)
    except TypeError:
        try:
            return eng.initialize_session(
                name=kwargs.get("name", "Aria"),
                role=kwargs.get("role", "Rune Engineer")
            )
        except TypeError:
            return eng.initialize_session()

# 4. Sidebar: Realm Status & Character Presence
with st.sidebar:
    st.markdown("### 🏰 Kingdom of Elarion")
    state_dict = engine.state_mgr.load_or_init_world().to_dict()
    player_dict = engine.state_mgr.load_or_init_player().to_dict()
    learning_dict = engine.state_mgr.load_or_init_learning().to_dict()

    if st.session_state.game_started:
        sidebar_svg = generate_protagonist_svg(
            name=player_dict.get('name', 'Aria'),
            role=player_dict.get('role', 'Rune Engineer'),
            affinity=player_dict.get('magical_affinity', 'Arcane'),
            hair_style=player_dict.get('hair_style', 'Braided Crown'),
            hair_color=player_dict.get('hair_color', 'Auburn'),
            outfit=player_dict.get('outfit', 'Leather Scholar Coat'),
            companion=player_dict.get('companion', 'Clockwork Owl'),
            keepsake=player_dict.get('keepsake', 'Brass Chrono-Gear'),
            size=140
        )
        st.components.v1.html(sidebar_svg, height=160)

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
            st.session_state.cc_step = 1
            st.rerun()

    else:
        st.info("Inscribe your protagonist's chronicle to embark upon Chapter I: The Silence of the Springs.")

# ================= CHAPTER 0: STAGED STORYBOOK CHARACTER CREATION =================
if not st.session_state.game_started:
    st.markdown("""
    <div class="storybook-header">
        <div class="storybook-title">✨ MYTHCODE ✨</div>
        <div class="storybook-subtitle">"Every spell is a program. Every decision shapes the realm."</div>
        <p style="color: #4A3525; max-width: 720px; margin: 0 auto; font-size: 1.15rem;">
            Before your footsteps sound upon the cobblestones of Whispering Village,
            the ancient chroniclers of Elarion must inscribe who you are into the living ledger.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Staged navigation badges
    steps_meta = [
        (1, "Name"),
        (2, "Bearing"),
        (3, "Style"),
        (4, "Nature"),
        (5, "Companion"),
        (6, "Keepsake"),
        (7, "Chronicle")
    ]
    st_cols = st.columns(len(steps_meta))
    for s_idx, (num, label) in enumerate(steps_meta):
        with st_cols[s_idx]:
            is_active = (st.session_state.cc_step == num)
            btn_prefix = "🌟 " if is_active else ""
            if st.button(f"{btn_prefix}{num}. {label}", key=f"nav_step_{num}", use_container_width=True):
                st.session_state.cc_step = num
                st.rerun()

    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)

    col_wizard, col_preview = st.columns([1.35, 0.65])

    # --- LEFT COLUMN: STAGED CREATION STANZA ---
    with col_wizard:
        # STEP 1: Your Name
        if st.session_state.cc_step == 1:
            st.markdown("""
            <div class="stanza-card">
                <div class="stanza-step-indicator">Stanza I &bull; The Name Upon the Ledger</div>
                <h2 style="margin-top: 0; color: #4A3525;">What shall the realms call you?</h2>
                <div class="stanza-lore-quote">
                    "A name is the primary handle of existence—the first variable declared before any spell can weave reality."
                </div>
            </div>
            """, unsafe_allow_html=True)

            c1, c2 = st.columns([1.4, 0.8])
            with c1:
                name_in = st.text_input("Protagonist Name", value=st.session_state.cc_name, max_chars=30)
                st.session_state.cc_name = name_in.strip() or "Aria"
            with c2:
                pronoun_options = ["they/them", "she/her", "he/him", "ze/zir", "it/its"]
                p_idx = pronoun_options.index(st.session_state.cc_pronouns) if st.session_state.cc_pronouns in pronoun_options else 0
                pronouns_in = st.selectbox("How the elders speak of you", pronoun_options, index=p_idx)
                st.session_state.cc_pronouns = pronouns_in

            st.caption("Villagers, mentors, and forest spirits will address you by this name throughout your travels.")

        # STEP 2: Your Appearance
        elif st.session_state.cc_step == 2:
            st.markdown("""
            <div class="stanza-card">
                <div class="stanza-step-indicator">Stanza II &bull; Demeanor & Bearing</div>
                <h2 style="margin-top: 0; color: #4A3525;">How do you walk the world?</h2>
                <div class="stanza-lore-quote">
                    "When the morning mist parts over Whispering Village, the villagers will look first upon your gaze and your bearing."
                </div>
            </div>
            """, unsafe_allow_html=True)

            demeanor_options = [
                "Scholarly & contemplative, observing the world with keen curiosity",
                "Sturdy & grounded, weathered by mountain travels and stone quarries",
                "Nimble & poised, moving with quiet grace like forest leaves",
                "Warm & welcoming, carrying the light of kinship wherever you tread",
                "Sharp & alert, ever vigilant of shifts in the wind"
            ]
            d_idx = demeanor_options.index(st.session_state.cc_demeanor) if st.session_state.cc_demeanor in demeanor_options else 0
            st.session_state.cc_demeanor = st.selectbox("Demeanor & Bearing", demeanor_options, index=d_idx)

            col_app1, col_app2 = st.columns(2)
            with col_app1:
                gaze_options = [
                    "Amber gold",
                    "Deep river blue",
                    "Forest emerald",
                    "Obsidian dark",
                    "Amethyst violet"
                ]
                g_idx = gaze_options.index(st.session_state.cc_gaze) if st.session_state.cc_gaze in gaze_options else 0
                st.session_state.cc_gaze = st.selectbox("Eye Gaze", gaze_options, index=g_idx)

            with col_app2:
                complexion_options = [
                    "Sun-kissed bronze",
                    "Pale alabaster",
                    "Warm mahogany",
                    "Fair with rosy flush",
                    "Golden olive"
                ]
                c_idx = complexion_options.index(st.session_state.cc_complexion) if st.session_state.cc_complexion in complexion_options else 0
                st.session_state.cc_complexion = st.selectbox("Complexion & Skin Tone", complexion_options, index=c_idx)

        # STEP 3: Your Style
        elif st.session_state.cc_step == 3:
            st.markdown("""
            <div class="stanza-card">
                <div class="stanza-step-indicator">Stanza III &bull; Style & Attire</div>
                <h2 style="margin-top: 0; color: #4A3525;">Your Style and Traveling Garb</h2>
                <div class="stanza-lore-quote">
                    "A practitioner's attire tells tales of their discipline—whether forged in brass workshops or woven from celestial silk."
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_s1, col_s2 = st.columns(2)
            with col_s1:
                hair_style_options = [
                    "Braided Crown",
                    "Windswept Locks",
                    "Sleek Scholar Bob",
                    "Flowing Curls",
                    "Practical Cropped"
                ]
                hs_idx = hair_style_options.index(st.session_state.cc_hair_style) if st.session_state.cc_hair_style in hair_style_options else 0
                st.session_state.cc_hair_style = st.selectbox("Hair Style", hair_style_options, index=hs_idx)

                hair_color_options = [
                    "Auburn",
                    "Silver",
                    "Midnight Black",
                    "Golden",
                    "Emerald",
                    "Copper Crimson"
                ]
                hc_idx = hair_color_options.index(st.session_state.cc_hair_color) if st.session_state.cc_hair_color in hair_color_options else 0
                st.session_state.cc_hair_color = st.selectbox("Hair Color", hair_color_options, index=hc_idx)

            with col_s2:
                outfit_options = [
                    "Leather Scholar Coat",
                    "Traveler's Cloak",
                    "Tinkerer's Vest",
                    "Celestial Silk Tunic",
                    "Scout's Tunic"
                ]
                out_idx = outfit_options.index(st.session_state.cc_outfit) if st.session_state.cc_outfit in outfit_options else 0
                st.session_state.cc_outfit = st.selectbox("Traveling Attire", outfit_options, index=out_idx)

        # STEP 4: Your Nature
        elif st.session_state.cc_step == 4:
            st.markdown("""
            <div class="stanza-card">
                <div class="stanza-step-indicator">Stanza IV &bull; Nature, Calling & Affinity</div>
                <h2 style="margin-top: 0; color: #4A3525;">What is your nature and magical calling?</h2>
                <div class="stanza-lore-quote">
                    "Magic in Elarion obeys ancient computational laws. Your calling determines your approach to problem-solving."
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_n1, col_n2 = st.columns(2)
            with col_n1:
                role_options = [
                    "Rune Engineer",
                    "Spellweaver",
                    "Forest Guardian",
                    "Star Cartographer",
                    "Alchemist",
                    "Shadow Explorer"
                ]
                r_idx = role_options.index(st.session_state.cc_role) if st.session_state.cc_role in role_options else 0
                st.session_state.cc_role = st.selectbox("Fantasy Calling", role_options, index=r_idx)

                affinity_options = ["Arcane", "Water", "Nature", "Light", "Fire", "Wind"]
                aff_idx = affinity_options.index(st.session_state.cc_affinity) if st.session_state.cc_affinity in affinity_options else 0
                st.session_state.cc_affinity = st.selectbox("Primary Magical Affinity", affinity_options, index=aff_idx)

            with col_n2:
                personality_options = [
                    "Curious & Patient",
                    "Bold & Decisive",
                    "Thoughtful & Quiet",
                    "Witty & Resourceful",
                    "Gentle & Protective"
                ]
                pers_idx = personality_options.index(st.session_state.cc_personality) if st.session_state.cc_personality in personality_options else 0
                st.session_state.cc_personality = st.selectbox("Personality Demeanor", personality_options, index=pers_idx)

                learning_options = [
                    "Hands-on Experimentation",
                    "Deconstructive Analysis",
                    "Intuitive Pattern-Hunting",
                    "Trial & Discovery"
                ]
                learn_idx = learning_options.index(st.session_state.cc_learning_style) if st.session_state.cc_learning_style in learning_options else 0
                st.session_state.cc_learning_style = st.selectbox("Learning Disposition", learning_options, index=learn_idx)

        # STEP 5: Your Companion
        elif st.session_state.cc_step == 5:
            st.markdown("""
            <div class="stanza-card">
                <div class="stanza-step-indicator">Stanza V &bull; The Familiar Bond</div>
                <h2 style="margin-top: 0; color: #4A3525;">Who accompanies your journey?</h2>
                <div class="stanza-lore-quote">
                    "No traveler solves the deep mysteries alone. A faithful familiar perches beside you, offering guidance and companionship."
                </div>
            </div>
            """, unsafe_allow_html=True)

            companion_details = {
                "Clockwork Owl": "A mechanical familiar forged from copper and brass; tilts its head and whirs rhythmically when runes align.",
                "Sylvan Sprite": "A playful wisp of emerald leaves that flutters eagerly around problems and hums with ancient forest songs.",
                "Runestone Fox": "A nimble crimson kit with glowing runic markings along its tail; senses hidden mechanisms beneath stone.",
                "Ember Salamander": "A warm little lizard with crystalline scales that glow when you solve tricky dilemmas.",
                "Zephyr Finch": "A swift silver-winged songbird that rides drafts and chirps melodic hints when gears mesh."
            }
            comp_names = list(companion_details.keys())
            c_idx = comp_names.index(st.session_state.cc_companion) if st.session_state.cc_companion in comp_names else 0
            selected_comp = st.selectbox("Choose Your Familiar", comp_names, index=c_idx)
            st.session_state.cc_companion = selected_comp

            st.info(f"🐾 **{selected_comp}:** {companion_details[selected_comp]}")

        # STEP 6: Your Keepsake
        elif st.session_state.cc_step == 6:
            st.markdown("""
            <div class="stanza-card">
                <div class="stanza-step-indicator">Stanza VI &bull; The Cherished Keepsake</div>
                <h2 style="margin-top: 0; color: #4A3525;">What token do you carry?</h2>
                <div class="stanza-lore-quote">
                    "Before leaving your home province, you tucked one object into your pocket. Later in your journey, this keepsake will unlock deep doors."
                </div>
            </div>
            """, unsafe_allow_html=True)

            keepsake_details = {
                "Brass Chrono-Gear": "A pocket-sized interlocking cog from your mentor's very first water-clock, still ticking softly.",
                "Dried Star-Blossom": "A celestial flower pressed between parchment pages, glowing with faint luminescent pollen.",
                "River Prism": "A crystalline pendant that splits sunlight into liquid rainbows; sensitive to water flow.",
                "Carved Rune-Tablet": "A smooth slate fragment engraved with the ancient symbol of Sequence.",
                "Alchemical Vial": "A sealed phial containing a swirling droplet of pure mountain springwater."
            }
            kp_names = list(keepsake_details.keys())
            k_idx = kp_names.index(st.session_state.cc_keepsake) if st.session_state.cc_keepsake in kp_names else 0
            selected_kp = st.selectbox("Choose Your Starting Keepsake", kp_names, index=k_idx)
            st.session_state.cc_keepsake = selected_kp

            st.success(f"🗝️ **{selected_kp}:** {keepsake_details[selected_kp]}")

        # STEP 7: The Chronicle Sealed (Summary & Embark)
        elif st.session_state.cc_step == 7:
            st.markdown("""
            <div class="stanza-card">
                <div class="stanza-step-indicator">Stanza VII &bull; The Chronicle is Inscribed</div>
                <h2 style="margin-top: 0; color: #4A3525;">The Legend Begins</h2>
                <div class="stanza-lore-quote">
                    "The ink dries upon the vellum. The mountain winds call toward Whispering Village."
                </div>
            </div>
            """, unsafe_allow_html=True)

            appearance_full = f"{st.session_state.cc_demeanor}. Features: {st.session_state.cc_complexion} skin, {st.session_state.cc_gaze} gaze."

            st.markdown(f"""
            <div style="background: #FFFDF9; border: 2px solid #D7B978; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; font-style: italic; font-size: 1.15rem; line-height: 1.8; color: #362E3B;">
                "Here begins the chronicle of <strong>{st.session_state.cc_name}</strong>, a {st.session_state.cc_role} ({st.session_state.cc_pronouns})
                adorned in a {st.session_state.cc_outfit} with {st.session_state.cc_hair_style} of {st.session_state.cc_hair_color} hair.
                Attuned to the <strong>{st.session_state.cc_affinity}</strong> winds and bearing a <strong>{st.session_state.cc_personality}</strong> spirit,
                they walk with their faithful <strong>{st.session_state.cc_companion}</strong> by their side and a cherished
                <strong>{st.session_state.cc_keepsake}</strong> tucked safely in their pocket.
                Today, their journey takes them to the quiet cobblestones of Whispering Village, where the ancient water springs have stopped flowing..."
            </div>
            """, unsafe_allow_html=True)

            if st.button("🌟 Inscribe Chronicle & Embark Into Whispering Village", type="primary", use_container_width=True):
                safe_initialize_session(
                    engine,
                    name=st.session_state.cc_name,
                    pronouns=st.session_state.cc_pronouns,
                    role=st.session_state.cc_role,
                    appearance=appearance_full,
                    hair_style=st.session_state.cc_hair_style,
                    hair_color=st.session_state.cc_hair_color,
                    outfit=st.session_state.cc_outfit,
                    magical_affinity=st.session_state.cc_affinity,
                    personality=st.session_state.cc_personality,
                    companion=st.session_state.cc_companion,
                    learning_style=st.session_state.cc_learning_style,
                    keepsake=st.session_state.cc_keepsake,
                    inventory=["Explorer's Journal", st.session_state.cc_keepsake]
                )
                res = safe_execute_action(
                    engine,
                    f"{st.session_state.cc_name} arrives in Whispering Village to investigate the silent springs.",
                    action_id="examine_fountain"
                )
                st.session_state.active_scene = res["scene"]
                st.session_state.last_action_feedback = f"You arrive at Whispering Village as the morning mist parts. The central fountain is eerily silent."
                st.session_state.game_started = True
                st.rerun()

        # Step Navigation Buttons (Prev / Next)
        st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
        col_nav1, col_nav2 = st.columns([1, 1])
        with col_nav1:
            if st.session_state.cc_step > 1:
                if st.button("⬅️ Previous Stanza", use_container_width=True):
                    st.session_state.cc_step -= 1
                    st.rerun()

        with col_nav2:
            if st.session_state.cc_step < 7:
                if st.button("Continue Journey ➔", type="primary", use_container_width=True):
                    st.session_state.cc_step += 1
                    st.rerun()

    # --- RIGHT COLUMN: LIVING PROTAGONIST FOLIO ---
    with col_preview:
        st.markdown("""
        <div class="living-folio-card">
            <div class="folio-title">Protagonist's Folio</div>
            <div class="folio-subtitle">Living Chronicle Preview</div>
        </div>
        """, unsafe_allow_html=True)

        # Dynamic SVG vector portrait that reflects current choices in real-time
        preview_svg = generate_protagonist_svg(
            name=st.session_state.cc_name,
            role=st.session_state.cc_role,
            affinity=st.session_state.cc_affinity,
            hair_style=st.session_state.cc_hair_style,
            hair_color=st.session_state.cc_hair_color,
            outfit=st.session_state.cc_outfit,
            companion=st.session_state.cc_companion,
            keepsake=st.session_state.cc_keepsake,
            complexion=st.session_state.cc_complexion,
            eye_color=st.session_state.cc_gaze,
            size=220
        )
        st.components.v1.html(preview_svg, height=255)

        st.markdown(f"""
        <div style="background: #FFFDF9; border: 1px solid #D7B978; border-radius: 10px; padding: 1rem; margin-top: 0.5rem; font-size: 0.95rem;">
            <div class="folio-field-box"><strong>Hero:</strong> {st.session_state.cc_name} ({st.session_state.cc_pronouns})</div>
            <div class="folio-field-box"><strong>Calling:</strong> {st.session_state.cc_role}</div>
            <div class="folio-field-box"><strong>Affinity:</strong> {st.session_state.cc_affinity} Arcana</div>
            <div class="folio-field-box"><strong>Hair:</strong> {st.session_state.cc_hair_style} ({st.session_state.cc_hair_color})</div>
            <div class="folio-field-box"><strong>Attire:</strong> {st.session_state.cc_outfit}</div>
            <div class="folio-field-box"><strong>Familiar:</strong> {st.session_state.cc_companion}</div>
            <div class="folio-field-box"><strong>Keepsake:</strong> {st.session_state.cc_keepsake}</div>
            <div class="folio-field-box"><strong>Nature:</strong> {st.session_state.cc_personality}</div>
        </div>
        """, unsafe_allow_html=True)

# ================= CHAPTER I: PLAYABLE VERTICAL SLICE =================
else:
    scene = st.session_state.active_scene
    if not scene:
        res = safe_execute_action(engine, "Look around Whispering Village.", action_id="examine_fountain")
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
                res = safe_execute_action(engine, action_text=c_text, action_id=c_id)
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
