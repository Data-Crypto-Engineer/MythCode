"""
Integration tests for GameEngine, SQLite persistence, and multi-agent loops.
"""
import unittest
import os
from core.game_engine import GameEngine

TEST_DB = "test_mythcode.db"

class TestGameEngine(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        import database.storage as ds
        ds._storage_instance = None
        self.engine = GameEngine(player_id="test_hero", db_path=TEST_DB)

    def tearDown(self):
        import database.storage as ds
        ds._storage_instance = None
        if os.path.exists(TEST_DB):
            try:
                os.remove(TEST_DB)
            except Exception:
                pass

    def test_session_init_and_character_creation(self):
        data = self.engine.initialize_session(
            name="Lyra", role="Sylvan Wayfarer", style="Diplomatic & Patient"
        )
        self.assertEqual(data["player"]["name"], "Lyra")
        self.assertEqual(data["player"]["role"], "Sylvan Wayfarer")
        self.assertEqual(data["world"]["kingdom"], "Elarion")
        self.assertEqual(len(data["quests"]), 1)

    def test_action_execution_and_telemetry(self):
        self.engine.initialize_session(name="Lyra")
        res = self.engine.execute_action("Travel to the River Aqueduct to inspect the machinery.")
        self.assertTrue(res["success"])
        self.assertIn("scene", res)
        self.assertEqual(res["world_state"]["current_location"], "River Aqueduct")
        self.assertTrue(len(res["telemetry"]) >= 3)

    def test_solve_challenge_and_unlock(self):
        self.engine.initialize_session(name="Lyra")
        # Solve sequence puzzle
        sol = ["FORWARD", "FORWARD", "TURN_RIGHT", "FORWARD"]
        res = self.engine.solve_challenge("puzzle_sequence_guardian", sol)
        self.assertTrue(res["success"])
        self.assertTrue(res["puzzle_correct"])
        self.assertEqual(res["world_state"]["clockwork_guardian"], "operational")

        # Verify persistence reload in a brand new engine instance
        engine2 = GameEngine(player_id="test_hero", db_path=TEST_DB)
        reloaded_world = engine2.state_mgr.load_or_init_world()
        self.assertEqual(reloaded_world.clockwork_guardian, "operational")

        # Verify learning progress persisted
        reloaded_learn = engine2.state_mgr.load_or_init_learning()
        self.assertIn("puzzle_sequence_guardian", reloaded_learn.completed_puzzles)

if __name__ == "__main__":
    unittest.main()
