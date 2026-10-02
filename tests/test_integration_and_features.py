"""
Comprehensive verification test suite for MythCode repairs, character creator,
Codex of Becoming, XP progression, and Cloudflare/Gemini resilience (PART 15).
"""
import unittest
import os
import json
from core.game_engine import GameEngine
from utils.cloudflare_images import get_image_service
from utils.gemini_storyteller import GeminiStoryteller
from database.storage import SQLiteStorage

TEST_DB = "test_features_mythcode.db"

class TestMythCodeFeatures(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        import database.storage as ds
        ds._storage_instance = None
        self.engine = GameEngine(player_id="hero_tester", db_path=TEST_DB)

    def tearDown(self):
        import database.storage as ds
        ds._storage_instance = None
        if os.path.exists(TEST_DB):
            try:
                os.remove(TEST_DB)
            except Exception:
                pass

    def test_01_character_creation_and_customization(self):
        """Verify character creation with role, affinity, companion, and keepsake."""
        session = self.engine.initialize_session(
            name="Kaelen",
            pronouns="they/them",
            role="Spellweaver",
            magical_affinity="Nature",
            hair_color="Silver",
            companion="Sylvan Sprite",
            keepsake="Dried Star-Blossom",
            learning_style="Visual Step-by-Step",
            personality="Reflective & Wise"
        )
        player = session["player"]
        self.assertEqual(player["name"], "Kaelen")
        self.assertEqual(player["role"], "Spellweaver")
        self.assertEqual(player["magical_affinity"], "Nature")
        self.assertEqual(player["companion"], "Sylvan Sprite")
        self.assertEqual(player["keepsake"], "Dried Star-Blossom")

    def test_02_character_configuration_persists(self):
        """Verify character attributes reload correctly across fresh GameEngine instances."""
        self.engine.initialize_session(
            name="Seraphina",
            role="Star Cartographer",
            magical_affinity="Light",
            companion="Zephyr Finch"
        )
        # Reload via a new engine instance
        engine2 = GameEngine(player_id="hero_tester", db_path=TEST_DB)
        reloaded = engine2.state_mgr.load_or_init_player()
        self.assertEqual(reloaded.name, "Seraphina")
        self.assertEqual(reloaded.role, "Star Cartographer")
        self.assertEqual(reloaded.magical_affinity, "Light")
        self.assertEqual(reloaded.companion, "Zephyr Finch")

    def test_03_narrative_choices_produce_observable_results(self):
        """Verify that every narrative choice produces unique, stateful changes."""
        self.engine.initialize_session(name="Kaelen")
        
        # Action 1: Inspect fountain
        res1 = self.engine.execute_action("Examine the intricate stonework and dried pipes of the village fountain.")
        self.assertTrue(res1["success"])
        self.assertIn("Fountain", res1["scene"]["scene_title"])
        self.assertIn("runic conduit", res1["scene"]["scene_description"])

        # Action 2: Talk to Mira
        res2 = self.engine.execute_action("Walk over to Mira's workshop to ask about the aqueduct gears.")
        self.assertTrue(res2["success"])
        self.assertIn("Mira", res2["scene"]["speaker"])
        self.assertIn("Workshop", res2["scene"]["scene_title"])

        # Action 3: Travel downstream
        res3 = self.engine.execute_action("Travel downstream toward the River Aqueduct.")
        self.assertTrue(res3["success"])
        self.assertEqual(res3["world_state"]["current_location"], "River Aqueduct")
        self.assertIn("Aqueduct", res3["scene"]["scene_title"])

    def test_04_sequence_puzzle_accepts_intended_answer(self):
        """Verify Stage 1 sequence puzzle solves correctly and updates guardian status."""
        self.engine.initialize_session(name="Kaelen")
        steps = ["FORWARD", "FORWARD", "TURN_RIGHT", "FORWARD"]
        res = self.engine.solve_challenge("puzzle_sequence_guardian", steps)
        self.assertTrue(res["puzzle_correct"])
        self.assertEqual(res["world_state"]["clockwork_guardian"], "operational")
        self.assertIsNotNone(res["revealed_code"])

    def test_05_condition_puzzle_evaluates_correctly(self):
        """Verify Stage 2 conditions puzzle solves correctly and updates spirit trust."""
        self.engine.initialize_session(name="Kaelen")
        res = self.engine.solve_challenge("puzzle_conditional_door", "has_seal")
        self.assertTrue(res["puzzle_correct"])
        self.assertGreater(res["world_state"]["forest_spirit_trust"], 0)

    def test_06_loop_puzzle_evaluates_correctly(self):
        """Verify Stage 3 loops puzzle solves correctly and restores water supply."""
        self.engine.initialize_session(name="Kaelen")
        res = self.engine.solve_challenge("puzzle_loop_tiles", "LOOP_5_STEPS")
        self.assertTrue(res["puzzle_correct"])
        self.assertEqual(res["world_state"]["water_supply"], "restored")

    def test_07_incorrect_answers_provide_useful_feedback(self):
        """Verify incorrect puzzle solutions return informative feedback without state corruption."""
        self.engine.initialize_session(name="Kaelen")
        bad_steps = ["TURN_LEFT"]
        res = self.engine.solve_challenge("puzzle_sequence_guardian", bad_steps)
        self.assertFalse(res["puzzle_correct"])
        self.assertIn("Order matters in execution", res["puzzle_feedback"])
        self.assertEqual(res["world_state"]["clockwork_guardian"], "inactive")

    def test_08_xp_and_level_progression(self):
        """Verify player gains XP and levels up upon completing challenges."""
        self.engine.initialize_session(name="Kaelen")
        # Solve sequence (+50 XP) and conditions (+50 XP) -> 100 XP -> Level 2
        self.engine.solve_challenge("puzzle_sequence_guardian", ["FORWARD", "FORWARD", "TURN_RIGHT", "FORWARD"])
        res = self.engine.solve_challenge("puzzle_conditional_door", "has_seal")
        player = res["player_profile"]
        self.assertGreaterEqual(player["xp"], 100)
        self.assertGreaterEqual(player["level"], 2)

    def test_09_codex_of_becoming_tracks_masteries(self):
        """Verify The Codex of Becoming logs masteries upon successful puzzle completion."""
        self.engine.initialize_session(name="Kaelen")
        self.engine.solve_challenge("puzzle_sequence_guardian", ["FORWARD", "FORWARD", "TURN_RIGHT", "FORWARD"])
        learning = self.engine.state_mgr.load_or_init_learning()
        masteries = [e for e in learning.codex_entries if e.get("category") == "mastery"]
        self.assertTrue(len(masteries) >= 1)
        self.assertEqual(masteries[0]["concept"], "Sequence")

    def test_10_missing_gemini_credentials_do_not_crash(self):
        """Verify that an unavailable Gemini API falls back gracefully."""
        storyteller = GeminiStoryteller()
        storyteller.api_key = ""  # Force unavailable
        base = {"scene_title": "Silent Square", "scene_description": "Normal desc", "dialogue": "Hello", "speaker": "Thorne"}
        enriched = storyteller.enrich_scene(base, {}, {}, [], "Walk")
        self.assertEqual(enriched, base)

    def test_11_missing_cloudflare_credentials_do_not_crash(self):
        """Verify that an unavailable Cloudflare API falls back to valid SVG illustration."""
        img_service = get_image_service()
        img_service.api_token = ""  # Force unavailable
        illustration = img_service.get_illustration("River Aqueduct")
        self.assertTrue(illustration.startswith("data:image/svg+xml;base64,"))

    def test_12_json_backup_export_and_import(self):
        """Verify JSON backup export and import preserves full state."""
        self.engine.initialize_session(name="Archivist", role="Alchemist")
        self.engine.solve_challenge("puzzle_sequence_guardian", ["FORWARD", "FORWARD", "TURN_RIGHT", "FORWARD"])
        backup_str = self.engine.export_backup()
        self.assertIn("Archivist", backup_str)
        self.assertIn("operational", backup_str)

        # Restore into another session
        ok = self.engine.import_backup(backup_str)
        self.assertTrue(ok)
        reloaded = self.engine.state_mgr.load_or_init_player()
        self.assertEqual(reloaded.name, "Archivist")

    def test_13_quest_data_loadable(self):
        """Verify seed quest data loads properly."""
        quests = self.engine.quest_mgr.get_all_quests()
        self.assertTrue(len(quests) >= 1)
        self.assertEqual(quests[0].id, "quest_water_crisis")

if __name__ == "__main__":
    unittest.main()
