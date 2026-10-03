"""
Unit and integration tests for MythCode Narrative Intelligence and Memory Continuity.
Validates the core 4-step continuity scenario:
1. Player helps NPC.
2. Player leaves.
3. Player returns later.
4. NPC remembers.
"""
import unittest
import os
from core.game_engine import GameEngine
from models.world import WorldState

TEST_DB = "test_continuity.db"

class TestNarrativeContinuity(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        import database.storage as ds
        ds._storage_instance = None
        self.engine = GameEngine(player_id="test_hero", db_path=TEST_DB)
        self.engine.initialize_session(name="Aria", role="Rune Engineer", companion="Clockwork Owl")

    def tearDown(self):
        import database.storage as ds
        ds._storage_instance = None
        if os.path.exists(TEST_DB):
            try:
                os.remove(TEST_DB)
            except Exception:
                pass

    def test_continuity_player_helps_npc_leaves_and_returns(self):
        """
        CONTINUITY TEST:
        1. Player helps NPC (solves sentinel sequence, restoring waterwheel & workshop).
        2. Player leaves (visits village square / fountain).
        3. Player returns later (speaks with Mira at her workshop).
        4. NPC remembers (Mira acknowledges the hero restored the waterwheel and doesn't repeat her opening plea).
        """
        # Step 1: Player helps NPC by solving the sequence puzzle
        sol = ["FORWARD", "FORWARD", "TURN_RIGHT", "FORWARD"]
        res_solve = self.engine.solve_challenge("puzzle_sequence_guardian", sol)
        self.assertTrue(res_solve["success"])
        self.assertTrue(res_solve["puzzle_correct"])
        self.assertEqual(res_solve["world_state"]["clockwork_guardian"], "operational")
        self.assertEqual(res_solve["world_state"]["water_supply"], "restored")
        self.assertEqual(res_solve["world_state"]["npc_relationships"].get("Mira"), "helped")

        # Step 2: Player leaves to inspect the village fountain
        res_leave = self.engine.execute_action(
            action_text="Return to village square and inspect the fountain.",
            action_id="inspect_fountain"
        )
        self.assertTrue(res_leave["success"])
        self.assertEqual(res_leave["world_state"]["current_location"], "Whispering Village")
        self.assertIn("cascades", res_leave["scene"]["scene_description"].lower())

        # Step 3: Player returns later to Mira's workshop
        res_return = self.engine.execute_action(
            action_text="Walk over to Mira's workshop.",
            action_id="speak_mira"
        )
        self.assertTrue(res_return["success"])
        scene = res_return["scene"]

        # Step 4: NPC remembers!
        # Assert Mira explicitly remembers and thanks the hero
        self.assertEqual(scene["speaker"], "Mira the Inventor")
        self.assertIn("turning like clockwork", scene["dialogue"].lower())
        self.assertIn("saved whispering village", scene["dialogue"].lower())

        # Assert Mira does NOT contradict the world by claiming the springs are still dry
        self.assertNotIn("silence of the springs began yesterday", scene["dialogue"].lower())
        self.assertNotIn("will you accompany me to the aqueduct", scene["dialogue"].lower())

        # Assert persistent memories track the deed
        world = res_return["world_state"]
        self.assertEqual(world["npc_relationships"].get("Mira"), "helped")
        mira_mems = [m for m in world.get("persistent_memories", []) if "mira" in m.get("key", "").lower()]
        self.assertTrue(len(mira_mems) >= 1)

    def test_continuity_blueprint_help_leaves_and_returns(self):
        """
        Test that helping Mira with blueprints before the puzzle is remembered upon return.
        """
        # Step 1: Help Mira with blueprints
        res_help = self.engine.execute_action(
            action_text="Help Mira calibrate blueprint tolerances.",
            action_id="help_mira_prep"
        )
        self.assertTrue(res_help["success"])
        self.assertEqual(res_help["world_state"]["npc_relationships"].get("Mira"), "helped_prep")

        # Step 2: Leave to inspect fountain
        res_leave = self.engine.execute_action(
            action_text="Examine the village fountain.",
            action_id="inspect_fountain"
        )
        self.assertTrue(res_leave["success"])

        # Step 3: Return to Mira
        res_return = self.engine.execute_action(
            action_text="Return to Mira's workshop.",
            action_id="speak_mira"
        )
        self.assertTrue(res_return["success"])

        # Step 4: Mira remembers the calibrations
        self.assertIn("calibrat", res_return["scene"]["dialogue"].lower())

    def test_continuity_bypassed_mira_remembered(self):
        """
        Test that ignoring/bypassing Mira is acknowledged if the player later speaks to her.
        """
        # Step 1: Bypass Mira
        res_bypass = self.engine.execute_action(
            action_text="Bypass the workshop toward the river gorge.",
            action_id="bypass_mira"
        )
        self.assertTrue(res_bypass["success"])
        self.assertEqual(res_bypass["world_state"]["npc_relationships"].get("Mira"), "bypassed")

        # Step 2: Return to visit Mira
        res_visit = self.engine.execute_action(
            action_text="Visit Mira's workshop.",
            action_id="speak_mira"
        )
        self.assertTrue(res_visit["success"])

        # Step 3: Mira acknowledges hero marched straight past earlier
        self.assertIn("marching straight down", res_visit["scene"]["dialogue"].lower())

    def test_persistent_state_reloaded_cleanly(self):
        """
        Test that reloading state from SQLite preserves NPC relationships and persistent memories.
        """
        # Save a deed
        self.engine.execute_action("Help Mira prep", action_id="help_mira_prep")

        # Create new engine instance reading from same SQLite DB
        engine2 = GameEngine(player_id="test_hero", db_path=TEST_DB)
        world2 = engine2.state_mgr.load_or_init_world()
        self.assertEqual(world2.get_npc_relationship("Mira"), "helped_prep")
        self.assertTrue(world2.has_persistent_memory("mira_prep"))

if __name__ == "__main__":
    unittest.main()
