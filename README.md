# ✨ MythCode ✨
### Adaptive Multi-Agent Fantasy Adventure & Experiential Programming Learning Platform

> *"Your choices shape the world. Your world shapes your mind."*

MythCode is an AI-powered experiential fantasy adventure where computational thinking and progressive Python programming emerge organically as the physical mechanics of an enchanting fantasy realm. Powered by a coordinated 6-agent **CrewAI** multi-agent architecture and built with **Streamlit** (plus a companion live interactive web applet), MythCode teaches real programming without feeling like a dry code academy.

---

## 🌟 The Product Vision & Philosophy

In the realm of **Elarion**, the mountain springs supplying Whispering Village have dried up, ancient waterwheels have seized, and dormant brass guardians stand frozen before flooded sluice gates. Rather than forcing players to write arbitrary code right away, programming concepts appear as the natural laws of the universe:
- **Sequential Execution**: A dormant Clockwork Guardian only moves when commands are assembled in precise chronological order (`move_forward()`, `turn_right()`).
- **Conditional Logic**: Sylvan runic gateways unlock only when specific state conditions evaluate to `True` (`if has_emerald_seal: open_portal() else: search_for_seal()`).
- **Loops & Iteration**: Subterranean energy conduits require sustained rhythmic repetition across 5 resonance tiles (`for step in range(5): energize_tile(step)`).

Once a mechanic is understood through interactive world play, **The Unwritten Journal** reveals its true nature: real, executable Python syntax.

---

## 🏛️ System Architecture

MythCode uses a modular architecture where each logical agent is isolated in its own module with strict single responsibilities:

```
mythcode/
├── app.py                      # Main Streamlit Application
├── requirements.txt            # Streamlit & CrewAI dependencies
├── runtime.txt                 # Verified Python version (python-3.10.12)
├── README.md                   # Complete architectural guide
├── .gitignore                  # Git exclusions for secrets, sqlite, pycache
├── .streamlit/
│   └── secrets.toml.example    # Template for LLM credentials & app settings
├── agents/                     # The 6 Dedicated CrewAI Agents
│   ├── __init__.py
│   ├── director_agent.py        # Central narrative coordinator & beat planner
│   ├── player_insight_agent.py  # Adaptive cognitive & gameplay analyst
│   ├── story_weaver_agent.py    # Living folklore, dialogue & scene generator
│   ├── world_keeper_agent.py    # Realm continuity, geography & physics gatekeeper
│   ├── logic_learning_agent.py  # Computational thinking & Python reveal instructor
│   ├── continuity_safety_agent.py # Mandatory content safety & rule auditor
│   └── mythweaver_crew.py       # Orchestration layer with conditional execution
├── core/                       # Deterministic Game Engine & Validation
│   ├── __init__.py
│   ├── game_engine.py          # Application-facing facade
│   ├── state_manager.py        # Atomic persistence & rollback manager
│   ├── state_validator.py      # Deterministic state invariant enforcement
│   ├── quest_manager.py        # Quest progression & branching pathways
│   ├── learning_engine.py      # Puzzle validation (zero eval/exec code risk)
│   └── player_model.py         # Bounded evidence-based player profile updater
├── models/                     # Structured Domain Entities
│   ├── __init__.py
│   ├── player.py               # PlayerProfile & AdaptiveTraits
│   ├── world.py                # WorldState & physical status
│   ├── quest.py                # Quest & QuestPathway
│   ├── character.py            # CharacterMemory & NPCState
│   └── learning.py             # PuzzleChallenge & PythonConceptReveal
├── data/                       # Seed Lore & Puzzle Specifications
│   ├── initial_world.json      # Starting kingdom indicators & conflicts
│   ├── quests.json             # Water crisis quest & 3 pathways
│   └── puzzles.json            # 3 programming challenge specifications
├── database/                   # Persistent Storage Layer
│   ├── __init__.py
│   └── storage.py              # SQLite storage for cross-session durability
├── utils/                      # Utilities & Error Safeguards
│   ├── __init__.py
│   ├── config.py               # Streamlit Secrets & env loader
│   ├── error_handler.py        # Redaction & safe fallback scenes
│   ├── logger.py               # Sanitized logging without leaked API keys
│   └── validators.py           # Input sanitization & boundary clamps
└── tests/                      # Automated Test Suite (17 Unit Tests)
    ├── __init__.py
    ├── test_state_validation.py
    ├── test_learning_engine.py
    ├── test_player_model.py
    ├── test_game_engine.py
    └── test_error_handling.py
```

---

## 🤖 The 6 CrewAI Agents

| Agent | Module | Role & Responsibility |
|---|---|---|
| **1. Director Agent** | `agents/director_agent.py` | Coordinates the beat, evaluates recent player intent, and proposes structured transitions. |
| **2. Player Insight Agent** | `agents/player_insight_agent.py` | Maintains an evidence-based, bounded adaptive profile (Exploration, Dialogue, Puzzle, Building, Mastery). Avoids permanent stereotypes. |
| **3. Story Weaver Agent** | `agents/story_weaver_agent.py` | Composes atmospheric descriptions and dialogue that incorporate character memories and past player choices. |
| **4. World Keeper Agent** | `agents/world_keeper_agent.py` | Guards geographic continuity, ensures resource bounds, and prevents paradoxes. |
| **5. Logic & Learning Agent** | `agents/logic_learning_agent.py` | Integrates computational thinking, explains principles in-lore, and unlocks Python syntax upon success. |
| **6. Continuity & Safety Agent** | `agents/continuity_safety_agent.py` | Mandatory safety gatekeeper. Verifies age-appropriate content, blocks unsafe strings, and confirms state boundaries. |

### Cost-Conscious Orchestration
Rather than making 6 separate API calls on every button click, `MythWeaverCrew` uses **conditional routing**:
- Dialogue/Movement actions only invoke the Director, World Keeper, and Story Weaver.
- Puzzle attempts invoke Logic & Learning and deterministic validators.
- Zero API calls are wasted when deterministic logic suffices.
- Full offline fallback ensures the application runs perfectly even without an API key.

---

## 🚀 Setup & Local Execution

### 1. Requirements
- **Python**: Verified `>=3.10` and `<3.14` (Tested on `Python 3.10.12`).
- SQLite3 (included with Python standard library).

### 2. Installation
```bash
git clone https://github.com/your-username/mythcode.git
cd mythcode

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Secrets (Optional)
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit .streamlit/secrets.toml to supply your Gemini or OpenAI API key if desired.
# When left empty, the engine gracefully uses deterministic offline lore generators.
```

### 4. Run Streamlit Application
```bash
streamlit run app.py
```

---

## ☁️ Streamlit Community Cloud Deployment

1. Push your repository to **GitHub**.
2. Navigate to [share.streamlit.io](https://share.streamlit.io).
3. Connect your GitHub account and select your repository:
   - **Main file path**: `app.py`
   - **Python version**: `3.10`
4. In the app settings on Streamlit Cloud, open **Advanced Settings > Secrets**:
   ```toml
   [llm]
   provider = "gemini"
   model = "gemini-1.5-flash"
   api_key = "YOUR_VERIFIED_GEMINI_KEY"

   [app]
   environment = "production"
   enable_agent_telemetry = true
   ```
5. Click **Deploy!**

> **Note on Storage in Streamlit Community Cloud**:
> SQLite files are stored on the ephemeral container disk. For long-term cross-session persistence across cloud redeployments, an external database (such as Supabase or Cloud SQL) can be hooked up through `database/storage.py` using the exact same interface.

---

## 🧪 Automated Testing

MythCode includes comprehensive unit tests verifying state transitions, puzzle logic, error recovery, and player model updates.

Run the test suite:
```bash
python3 -m unittest discover tests
```

### Actual Test Results (Verified)
```
Ran 17 tests in 0.028s
OK (All 17 tests passing)
```
- `test_state_validation.py`: 4 tests (bounds, invalid locations, clamped morale, water states)
- `test_learning_engine.py`: 5 tests (sequence validation, conditional evaluation, loop iterations, hint requests)
- `test_player_model.py`: 2 tests (bounded preference drift, mastery milestones, challenge level updates)
- `test_game_engine.py`: 3 tests (session initialization, action execution, multi-agent dispatch, SQLite persistence reload)
- `test_error_handling.py`: 3 tests (credential redaction, fallback scene recovery, state preservation during invalid mutations)

---

## 🗺️ MVP Scope vs. Future Roadmap

### In the MVP
- Kingdom of Elarion with 3 core locations (Whispering Village, Ancient Grove, River Aqueduct).
- 3 recurring NPCs (Mira the Inventor, Sylvan the Forest Spirit, Elder Thorne).
- Central water crisis with 3 branching pathways.
- 3 fully playable computational thinking challenges (Sequence, Conditions, Loops).
- Python code reveals in The Unwritten Journal.
- Persistent SQLite storage and adaptive player modeling.
- 6-agent CrewAI orchestration with safety gatekeeper and offline fallback.

### Future Roadmap
- Interactive Python sandbox for player-authored scripts.
- Additional programming languages (JavaScript, Java, C++).
- Visual node-based block coding for younger learners.
- Procedurally generated kingdoms and collaborative multiplayer adventures.
