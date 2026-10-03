"""
MythCode — Adaptive Multi-Agent Fantasy Adventure & Experiential Programming Learning Platform
Streamlit Edition for GitHub & Streamlit Community Cloud

Design Principle:
"The player should discover computational thinking because they are trying to solve
a problem in the fantasy world. They should not feel like they have opened a programming course."

Progression Levels:
1. SEQUENCE — "Do these magical actions in the correct order." (Sequential Execution)
2. CONDITIONS — "The door opens only if the moonstone is glowing." (if / else)
3. LOOPS — "The enchanted bridge requires the same action five times." (loops / repetition)
4. VARIABLES — "The amount of moon energy determines the spell." (variables / dynamic values)
5. FUNCTIONS — "You have discovered a reusable spell." (functions / parameterized abstraction)
6. DATA / COLLECTIONS — "The library contains a collection of enchanted objects." (lists / dictionaries / data structures)

Codex of Becoming:
- Discoveries
- Masteries
- Your Craft
"""

import streamlit as st
import pandas as pd
import time

# 1. Page Configuration
st.set_page_config(
    page_title="MythCode — The Silence of the Springs",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Fantasy Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Crimson+Pro:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@400;600&display=swap');

    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
        font-family: 'Crimson Pro', Georgia, serif;
    }
    h1, h2, h3, h4 {
        font-family: 'Cinzel', Georgia, serif !important;
        color: #FDE68A !important;
    }
    .fantasy-card {
        background: #1E293B;
        border: 1px solid rgba(245, 158, 11, 0.25);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
    }
    .epiphany-card {
        background: rgba(245, 158, 11, 0.12);
        border: 2px solid #F59E0B;
        border-radius: 14px;
        padding: 1.5rem;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
    }
    .badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-family: 'JetBrains Mono', monospace;
    }
</style>
""", unsafe_allow_html=True)

# 3. Session State Initialization
if "player" not in st.session_state:
    st.session_state.player = {
        "name": "Aria",
        "role": "Aether Scholar",
        "level": 1,
        "masteries": {
            "sequence": 0,
            "conditions": 0,
            "loops": 0,
            "variables": 0,
            "functions": 0,
            "collections": 0
        }
    }

if "world" not in st.session_state:
    st.session_state.world = {
        "location": "Whispering Village",
        "water_supply": "dry",
        "village_morale": 45,
        "spirit_trust": 0
    }

if "discoveries" not in st.session_state:
    st.session_state.discoveries = [
        {
            "title": "The Great Drought of Elarion",
            "location": "Whispering Village",
            "lore": "The mountain springs ceased flowing when the ancient resonance matrix fell out of harmonic alignment."
        }
    ]

if "spells" not in st.session_state:
    st.session_state.spells = []

if "telemetry" not in st.session_state:
    st.session_state.telemetry = [
        {"agent": "DirectorAgent", "msg": "Elarion narrative arc initialized at Whispering Village."},
        {"agent": "LogicLearningAgent", "msg": "Deterministic validation matrix loaded across 6 computational primitives."},
        {"agent": "WorldKeeperAgent", "msg": "Physical constraints verified: Mountain conduits remain dry until restoration."}
    ]

if "level1_steps" not in st.session_state:
    st.session_state.level1_steps = []

# Helper function to record epiphany
def record_epiphany(primitive, fantasy_problem, fantasy_solution, concept, explanation, code_snippet, spell_data):
    st.session_state.last_epiphany = {
        "primitive": primitive,
        "fantasy_problem": fantasy_problem,
        "fantasy_solution": fantasy_solution,
        "concept": concept,
        "explanation": explanation,
        "code": code_snippet
    }
    # Add discovery
    if not any(d["title"] == spell_data["title"] for d in st.session_state.discoveries):
        st.session_state.discoveries.append({
            "title": spell_data["title"],
            "location": spell_data["location"],
            "lore": spell_data["lore"]
        })
    # Add spell
    if not any(s["name"] == spell_data["spell_name"] for s in st.session_state.spells):
        st.session_state.spells.append({
            "name": spell_data["spell_name"],
            "primitive": primitive,
            "incantation": spell_data["incantation"],
            "python": code_snippet
        })

# 4. Sidebar Controls
with st.sidebar:
    st.markdown("### ✨ MythCode Realm")
    st.markdown(f"**Scholar:** {st.session_state.player['name']} ({st.session_state.player['role']})")
    
    total_mastery = sum(st.session_state.player["masteries"].values()) // 6
    st.progress(total_mastery / 100.0, text=f"Computational Awakening: {total_mastery}%")
    
    st.markdown("---")
    st.markdown("#### 🗺️ Kingdom Status")
    st.markdown(f"- **Current Realm:** Elarion")
    st.markdown(f"- **Location:** {st.session_state.world['location']}")
    st.markdown(f"- **Village Morale:** {st.session_state.world['village_morale']}%")
    st.markdown(f"- **Spring Waters:** {st.session_state.world['water_supply'].title()}")

# 5. Top Navigation
nav = st.radio(
    "Navigation",
    ["📖 Adventure & Story", "⚡ The Six Harmonic Trials", "📜 The Codex of Becoming", "🤖 Autonomous Agents"],
    horizontal=True,
    label_visibility="collapsed"
)

# -------------------------------------------------------------
# TAB 1: ADVENTURE & STORY
# -------------------------------------------------------------
if nav == "📖 Adventure & Story":
    st.markdown("## 📖 Chapter I: The Silence of the Springs")
    st.markdown(
        "*A living fantasy world where every spell is an act of computational thought.*"
    )
    
    st.markdown("""
    <div class="fantasy-card">
        <h3>The Silent Village Square</h3>
        <p>
            The central fountain of Whispering Village lies bone-dry, its cracked stone basin carpeted in fallen leaves.
            Elder Thorne wrings his weathered hands: <i>"Our reservoir cannot last another moon. The ancient mountain aqueducts
            require the awakening of the dormant clockwork sentinel, the peaceful unlocking of the Grove's moonstone,
            and the reignition of the Five-Stone Bridge of Light."</i>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### 🧭 Choose Your Next Path:")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🌊 River Aqueduct (Level 1: Sequence)"):
            st.session_state.world["location"] = "River Aqueduct"
            st.info("You travel down the stone road to the Seized Waterwheel.")
            
    with col2:
        if st.button("🌿 Ancient Grove (Level 2: Conditions)"):
            st.session_state.world["location"] = "Ancient Grove"
            st.info("You venture into the bioluminescent forest toward the Moonstone Gate.")
            
    with col3:
        if st.button("⚙️ Clockwork Ruins (Level 3: Loops)"):
            st.session_state.world["location"] = "Clockwork Ruins"
            st.info("You descend into the subterranean conduit chamber.")

# -------------------------------------------------------------
# TAB 2: THE SIX HARMONIC TRIALS
# -------------------------------------------------------------
elif nav == "⚡ The Six Harmonic Trials":
    st.markdown("## ⚡ The Six Harmonic Trials of Elarion")
    st.markdown("Solve fantasy problems through magical mechanisms. Pure deterministic validation verifies each solution.")
    
    trial_tab = st.selectbox(
        "Select Trial Level:",
        [
            "Trial 1: The Clockwork Sentinel's Path (Sequence)",
            "Trial 2: The Moonstone Threshold (Conditions)",
            "Trial 3: The Enchanted Bridge of Light (Loops)",
            "Trial 4: The Moon Energy Cauldron (Variables)",
            "Trial 5: Universal Pillar Scribing (Functions)",
            "Trial 6: The Grand Celestial Archive Query (Collections)"
        ]
    )
    
    # ---------------- TRIAL 1: SEQUENCE ----------------
    if "Trial 1" in trial_tab:
        st.markdown("### Level 1 — The Clockwork Sentinel's Stepping Path")
        st.markdown("> **Fantasy Interpretation:** *Do these magical actions in the exact correct order.*")
        st.markdown("The Aqueduct sentinel must walk the flagstones to engage the sluice clutch. Sequence its exact kinetic steps.")
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("+ Step Forward") and len(st.session_state.level1_steps) < 5:
                st.session_state.level1_steps.append("STEP_FORWARD")
        with c2:
            if st.button("+ Turn Right 90°") and len(st.session_state.level1_steps) < 5:
                st.session_state.level1_steps.append("TURN_RIGHT")
        with c3:
            if st.button("+ Turn Left 90°") and len(st.session_state.level1_steps) < 5:
                st.session_state.level1_steps.append("TURN_LEFT")
        with c4:
            if st.button("+ Engage Clutch") and len(st.session_state.level1_steps) < 5:
                st.session_state.level1_steps.append("ENGAGE_CLUTCH")
                
        st.markdown(f"**Current Sequence:** `{ ' -> '.join(st.session_state.level1_steps) if st.session_state.level1_steps else 'Empty' }`")
        
        col_exec, col_reset = st.columns([1, 4])
        with col_exec:
            if st.button("▶️ Execute Kinetic Sequence"):
                expected = ["STEP_FORWARD", "STEP_FORWARD", "TURN_RIGHT", "STEP_FORWARD", "ENGAGE_CLUTCH"]
                if st.session_state.level1_steps == expected:
                    st.success("✨ The Sentinel steps forward twice, pivots right, steps to the dais, and locks the clutch gear into motion!")
                    st.session_state.player["masteries"]["sequence"] = 100
                    st.session_state.world["village_morale"] = min(100, st.session_state.world["village_morale"] + 10)
                    
                    record_epiphany(
                        primitive="ACTION",
                        fantasy_problem="The bronze sentinel required an exact ordered path around obstacles to reach the gear.",
                        fantasy_solution="You arranged: Step, Step, Turn Right, Step, Engage Clutch.",
                        concept="Sequential Execution",
                        explanation="In programming, commands execute strictly top-to-bottom. Swapping steps changes the entire physical behavior.",
                        code_snippet="""# Sequential Execution
sentinel.move_forward()
sentinel.move_forward()
sentinel.turn_right()
sentinel.move_forward()
sentinel.engage_clutch()""",
                        spell_data={
                            "title": "Awakening of the Aqueduct Sentinel",
                            "location": "River Aqueduct",
                            "lore": "The sentinel obeys precise chronological commands to mesh the canal gears.",
                            "spell_name": "Kinetic Sentinel Sequence",
                            "incantation": "Forward twain, pivot right, advance once, lock the gear."
                        }
                    )
                else:
                    st.error("❌ The Sentinel bumped into a mossy obelisk or stopped short.")
                    st.markdown("**Pedagogical Hint:** It needs 2 paces forward, a rightward turn at the canal corner, 1 pace forward, and the clutch action.")
        with col_reset:
            if st.button("🔄 Reset Steps"):
                st.session_state.level1_steps = []
                st.rerun()

    # ---------------- TRIAL 2: CONDITIONS ----------------
    elif "Trial 2" in trial_tab:
        st.markdown("### Level 2 — The Moonstone Portal of the Ancient Grove")
        st.markdown("> **Fantasy Interpretation:** *The door opens only if the moonstone is glowing and an offering of peace is made.*")
        
        moonstone_lit = st.checkbox("Kindle Moonstone Radiance (True / False)", value=False)
        offering = st.selectbox("Lay Offering upon Altar:", ["Cold Iron Blade", "Gold Coins", "Peaceful Herbal Laurel"])
        
        if st.button("⚡ Test Gate Condition"):
            if moonstone_lit and offering == "Peaceful Herbal Laurel":
                st.success("✨ The runic barrier glows warm silver and dissolves! Safe passage granted into the sacred grove.")
                st.session_state.player["masteries"]["conditions"] = 100
                st.session_state.world["spirit_trust"] = 10
                
                record_epiphany(
                    primitive="CONDITION",
                    fantasy_problem="The forest spirits guard the archway against intruders, checking environmental and intent conditions.",
                    fantasy_solution="Condition verified: moonstone_is_glowing == True and offering == 'Peaceful Herbal Laurel'.",
                    concept="Conditional Branching (if / else)",
                    explanation="Conditional statements evaluate a boolean premise. If True, code runs the branch; otherwise, it takes the alternate path.",
                    code_snippet="""# Conditional Branching
if moonstone_is_glowing and offering == "Peaceful Herbal Laurel":
    portal.unlock()
    print("Welcome, peaceful traveler.")
else:
    portal.repel_intruders()
    print("The ancient runes remain sealed.")""",
                    spell_data={
                        "title": "The Moonstone Covenant",
                        "location": "Ancient Grove",
                        "lore": "Portals assess the truth of environmental conditions before altering state.",
                        "spell_name": "Lunar Ward Passage",
                        "incantation": "When radiance shines and peace is held, unseal the archway."
                    }
                )
            else:
                st.error("❌ The guardian runes hum dangerously and deflect your hand.")
                if not moonstone_lit:
                    st.info("Hint: The Moonstone remains dark. Kindle its celestial light.")
                else:
                    st.info("Hint: The spirits reject weapons or coinage. They accept only peaceful herbs.")

    # ---------------- TRIAL 3: LOOPS ----------------
    elif "Trial 3" in trial_tab:
        st.markdown("### Level 3 — The Enchanted Bridge of Light")
        st.markdown("> **Fantasy Interpretation:** *The enchanted bridge requires the exact same pulse five times to anchor the floating keystones.*")
        
        pulse_count = st.slider("Calibrate Repeating Pulse Iterations:", min_value=1, max_value=8, value=3)
        
        if st.button("🔮 Fire Harmonic Loop"):
            if pulse_count == 5:
                st.success("✨ Harmonic Resonance Achieved! All 5 keystones solidify into crystalline granite. The bridge is forged!")
                st.session_state.player["masteries"]["loops"] = 100
                st.session_state.world["water_supply"] = "flowing"
                
                record_epiphany(
                    primitive="REPETITION",
                    fantasy_problem="Five floating stones in the Chasm of Echoes require identical crystal strikes to solidify.",
                    fantasy_solution="You calibrated a loop of exactly 5 iterations.",
                    concept="Loops & Iteration (for / while)",
                    explanation="Loops repeat instructions multiple times automatically without duplicating code lines.",
                    code_snippet="""# Repetition via Loop
for keystone in range(1, 6):
    crystallize_stone(keystone)
    print(f"Keystone {keystone} of 5 solidified.")

print("The Chasm of Echoes is bridged!")""",
                    spell_data={
                        "title": "The Span of Five Crystals",
                        "location": "Clockwork Ruins",
                        "lore": "Chasm bridges demand repeated harmonic pulses to lock their resonance.",
                        "spell_name": "Pentaradial Harmonic Pulse",
                        "incantation": "Repeat the song of illumination fivefold until the fifth keystone locks."
                    }
                )
            elif pulse_count < 5:
                st.error(f"❌ You pulsed {pulse_count} times. The bridge dissolved before reaching the far bank (needs 5).")
            else:
                st.error(f"❌ You pulsed {pulse_count} times! The excess energy overloaded the crystal lattice (needs exactly 5).")

    # ---------------- TRIAL 4: VARIABLES ----------------
    elif "Trial 4" in trial_tab:
        st.markdown("### Level 4 — The Moon Energy Cauldron")
        st.markdown("> **Fantasy Interpretation:** *The amount of moon energy stored inside the named vessel determines the purification spell.*")
        
        col_var_name, col_var_val = st.columns(2)
        with col_var_name:
            vessel_name = st.selectbox("Vessel Identifier Name:", ["Aetherium", "PurifyingDew", "SolarEssence"])
        with col_var_val:
            energy_val = st.slider("Stored Energy Units:", min_value=10, max_value=100, value=25)
            
        if st.button("🧪 Distill Cauldron Brew"):
            if vessel_name == "PurifyingDew" and 50 <= energy_val <= 65:
                st.success(f"✨ Masterful synthesis! {vessel_name} holding {energy_val} units purifies the reservoir sediment!")
                st.session_state.player["masteries"]["variables"] = 100
                
                record_epiphany(
                    primitive="VALUE",
                    fantasy_problem="The condenser requires holding a dynamic energy quantity in a named glass container.",
                    fantasy_solution="You defined: PurifyingDew = 60.",
                    concept="Variables & Named Storage",
                    explanation="Variables are named storage containers that hold data values that can be referenced and modified.",
                    code_snippet="""# Variables & Dynamic Values
vessel_name = "PurifyingDew"
moon_energy = 60

if 50 <= moon_energy <= 65:
    brew = "Purifying Elixir Synthesized"
    print(f"Stored {moon_energy} units in container {vessel_name}.")""",
                    spell_data={
                        "title": "Reservoir Distillation Formula",
                        "location": "Lunar Observatory",
                        "lore": "Aetheric liquids can be held in named vessels with precise magnitudes.",
                        "spell_name": "Vessel of Pure Hydration",
                        "incantation": "Bind sixty pulses of silver radiance under the name PurifyingDew."
                    }
                )
            else:
                st.error("❌ The brew failed.")
                if vessel_name != "PurifyingDew":
                    st.info("Hint: The ancient recipe demands the vessel be named 'PurifyingDew'.")
                else:
                    st.info("Hint: Energy level must be calibrated between 50 and 65 units.")

    # ---------------- TRIAL 5: FUNCTIONS ----------------
    elif "Trial 5" in trial_tab:
        st.markdown("### Level 5 — Universal Pillar Restoration Scribing")
        st.markdown("> **Fantasy Interpretation:** *You have discovered a reusable spell formula. Pass parameters to heal disparate pillars.*")
        
        c_elem, c_pow = st.columns(2)
        with c_elem:
            param_elem = st.selectbox("Parameter: Elemental Affinity", ["Frost", "Spark", "Terra"])
        with c_pow:
            param_pow = st.slider("Parameter: Channeling Power", 1, 6, 3)
            
        col_test_ice, col_test_light = st.columns(2)
        with col_test_ice:
            if st.button("Invoke on Pillar of Ice"):
                if param_elem == "Frost" and param_pow >= 3:
                    st.session_state.ice_ok = True
                    st.success("Pillar of Ice stabilized with Frost (Power >= 3)!")
                else:
                    st.error("Pillar of Ice requires Frost with power >= 3.")
        with col_test_light:
            if st.button("Invoke on Pillar of Lightning"):
                if param_elem == "Spark" and param_pow >= 4:
                    st.session_state.light_ok = True
                    st.success("Pillar of Lightning stabilized with Spark (Power >= 4)!")
                else:
                    st.error("Pillar of Lightning requires Spark with power >= 4.")
                    
        if st.session_state.get("ice_ok") and st.session_state.get("light_ok"):
            st.markdown("---")
            if st.button("🏆 Inscribe Reusable Function Mastery"):
                st.session_state.player["masteries"]["functions"] = 100
                record_epiphany(
                    primitive="REUSABLE_ACTION",
                    fantasy_problem="Restoring multiple pillars without writing separate complex rites for each.",
                    fantasy_solution="You declared a single function taking (element, power) parameters and invoked it for both pillars.",
                    concept="Functions & Reusable Abstraction",
                    explanation="Functions bundle reusable logic. Write once, and execute anywhere with custom arguments.",
                    code_snippet="""# Reusable Function with Parameters
def repair_pillar(pillar_name, element, power):
    print(f"Channeling {power} units of {element} into {pillar_name}...")
    return "Stabilized"

# Call function with custom arguments:
repair_pillar("Pillar of Ice", element="Frost", power=3)
repair_pillar("Pillar of Lightning", element="Spark", power=4)""",
                    spell_data={
                        "title": "The Archmage's Universal Scribe",
                        "location": "Archmage Workshop",
                        "lore": "One formula adapts to any monument when supplied with appropriate parameters.",
                        "spell_name": "Harmonic Scribing Function",
                        "incantation": "Invoke Glyph(element, power) with targeted parameters."
                    }
                )

    # ---------------- TRIAL 6: COLLECTIONS ----------------
    elif "Trial 6" in trial_tab:
        st.markdown("### Level 6 — The Grand Celestial Archive Query")
        st.markdown("> **Fantasy Interpretation:** *The library contains a collection of enchanted relics. Query the collection to claim the key.*")
        
        relics_data = [
            {"Name": "Tear of Elarion", "Element": "Water", "Power": 95, "Purity": "Pristine"},
            {"Name": "Ignis Ember", "Element": "Fire", "Power": 80, "Purity": "Pristine"},
            {"Name": "Deepwell Pearl", "Element": "Water", "Power": 88, "Purity": "Pristine"},
            {"Name": "Brine Shard", "Element": "Water", "Power": 45, "Purity": "Corrupted"},
            {"Name": "Aether Lens", "Element": "Aether", "Power": 90, "Purity": "Pristine"}
        ]
        df_relics = pd.DataFrame(relics_data)
        st.dataframe(df_relics, use_container_width=True)
        
        cq1, cq2, cq3 = st.columns(3)
        with cq1:
            q_elem = st.selectbox("Query Element Filter:", ["All", "Water", "Fire", "Aether"])
        with cq2:
            q_min_pow = st.slider("Query Min Power:", 40, 95, 85, step=5)
        with cq3:
            q_pristine = st.checkbox("Require Pristine Only", value=True)
            
        if st.button("🔍 Sieve Celestial Vault Collection"):
            # Filter deterministically
            res = [
                r for r in relics_data
                if (q_elem == "All" or r["Element"] == q_elem)
                and r["Power"] >= q_min_pow
                and (not q_pristine or r["Purity"] == "Pristine")
            ]
            
            if len(res) == 1 and res[0]["Name"] == "Tear of Elarion" and q_elem == "Water" and q_min_pow >= 90:
                st.success("✨ Vault Unsealed! Query yielded exactly [Tear of Elarion] (Power: 95). The Master Spring flows!")
                st.session_state.player["masteries"]["collections"] = 100
                st.session_state.world["water_supply"] = "restored"
                st.session_state.world["village_morale"] = 100
                
                record_epiphany(
                    primitive="COLLECTION",
                    fantasy_problem="Finding the sole supreme Water relic among hundreds of scattered archive artifacts.",
                    fantasy_solution="You filtered the collection: [r for r in relics if r['Element'] == 'Water' and r['Power'] >= 90 and r['Purity'] == 'Pristine'].",
                    concept="Collections & Data Structures",
                    explanation="Collections (lists, arrays, sets) store groups of data that can be filtered and manipulated systematically.",
                    code_snippet="""# Querying a List of Dictionaries
relics = [
    {"name": "Tear of Elarion", "element": "Water", "power": 95, "purity": "Pristine"},
    {"name": "Deepwell Pearl", "element": "Water", "power": 88, "purity": "Pristine"},
]

# List comprehension query
master_key = [
    r for r in relics 
    if r["element"] == "Water" and r["power"] >= 90 and r["purity"] == "Pristine"
]
print(f"Master Spring Key: {master_key[0]['name']}")""",
                    spell_data={
                        "title": "The Master Spring of Elarion",
                        "location": "Grand Celestial Archive",
                        "lore": "The eternal spring answers only to the supreme relic filtered from the vault collection.",
                        "spell_name": "Celestial Archive Sieve",
                        "incantation": "Sieve the celestial vault for pristine water relics of power ninety and above."
                    }
                )
            else:
                st.error(f"❌ Query returned {len(res)} items: {[r['Name'] for r in res]}.")
                st.info("Hint: The Spring Vault requires exclusively the single Water relic with power >= 90 and Pristine purity.")

    # Show epiphany card if just unlocked
    if "last_epiphany" in st.session_state:
        ep = st.session_state.last_epiphany
        st.markdown(f"""
        <div class="epiphany-card">
            <h4>💡 You just used a programming idea: {ep['concept']} ({ep['primitive']})!</h4>
            <p><b>Fantasy Problem:</b> {ep['fantasy_problem']}</p>
            <p><b>Fantasy Solution:</b> <i>{ep['fantasy_solution']}</i></p>
            <p><b>Computational Reality:</b> {ep['explanation']}</p>
        </div>
        """, unsafe_allow_html=True)
        st.code(ep["code"], language="python")

# -------------------------------------------------------------
# TAB 3: THE CODEX OF BECOMING
# -------------------------------------------------------------
elif nav == "📜 The Codex of Becoming":
    st.markdown("## 📜 The Codex of Becoming")
    st.markdown("*A chronicle of living discoveries, computational masteries, and scribed formulas.*")
    
    sec1, sec2, sec3 = st.tabs(["Section I: Discoveries", "Section II: Masteries", "Section III: Your Craft"])
    
    with sec1:
        st.markdown("### 🗺️ World Discoveries")
        for d in st.session_state.discoveries:
            st.markdown(f"""
            <div class="fantasy-card">
                <h4>{d['title']} <span class="badge" style="background:#334155; color:#F59E0B;">{d['location']}</span></h4>
                <p>{d['lore']}</p>
            </div>
            """, unsafe_allow_html=True)
            
    with sec2:
        st.markdown("### 🏆 Computational Masteries")
        m_cols = st.columns(3)
        primitives = [
            ("Sequential Order", "ACTION", st.session_state.player["masteries"]["sequence"]),
            ("Conditional Branching", "CONDITION", st.session_state.player["masteries"]["conditions"]),
            ("Harmonic Repetition", "REPETITION", st.session_state.player["masteries"]["loops"]),
            ("Named Vessels", "VALUE", st.session_state.player["masteries"]["variables"]),
            ("Reusable Glyphs", "REUSABLE_ACTION", st.session_state.player["masteries"]["functions"]),
            ("Archival Sieves", "COLLECTION", st.session_state.player["masteries"]["collections"])
        ]
        for idx, (title, prim, val) in enumerate(primitives):
            with m_cols[idx % 3]:
                st.markdown(f"""
                <div class="fantasy-card">
                    <h4>{title}</h4>
                    <p><b>Primitive:</b> <code>{prim}</code></p>
                    <p><b>Status:</b> {'✦ Mastered' if val == 100 else 'Locked'}</p>
                </div>
                """, unsafe_allow_html=True)
                st.progress(val / 100.0)
                
    with sec3:
        st.markdown("### ⚡ Scribed Spells & Formulas")
        if not st.session_state.spells:
            st.info("No spells scribed yet. Solve the Harmonic Trials to inscribe your magical formulas!")
        else:
            for s in st.session_state.spells:
                st.markdown(f"""
                <div class="fantasy-card">
                    <h4>{s['name']} <span class="badge" style="background:#065F46; color:#6EE7B7;">{s['primitive']}</span></h4>
                    <p><i>"{s['incantation']}"</i></p>
                </div>
                """, unsafe_allow_html=True)
                st.code(s["python"], language="python")

# -------------------------------------------------------------
# TAB 4: AUTONOMOUS AGENTS
# -------------------------------------------------------------
elif nav == "🤖 Autonomous Agents":
    st.markdown("## 🤖 Autonomous Multi-Agent Telemetry")
    st.markdown("Live coordination logs from the six specialized agents.")
    
    for t in st.session_state.telemetry:
        st.markdown(f"**[{t['agent']}]:** {t['msg']}")
