"""
Tests for adaptive player model updates and bounded traits.
"""
import unittest
from models.player import PlayerProfile
from core.player_model import PlayerModelEngine

class TestPlayerModel(unittest.TestCase):

    def setUp(self):
        self.profile = PlayerProfile(id="test_player", name="TestHero")

    def test_bounded_preference_updates(self):
        initial_exploration = self.profile.traits.exploration_preference
        updated = PlayerModelEngine.record_action(self.profile, action_category="exploration")
        self.assertAlmostEqual(updated.traits.exploration_preference, initial_exploration + 0.05, places=2)
        # Should not exceed 1.0 even after many updates
        for _ in range(30):
            updated = PlayerModelEngine.record_action(updated, action_category="exploration")
        self.assertLessEqual(updated.traits.exploration_preference, 1.0)

    def test_concept_mastery_and_challenge_level_adaptation(self):
        # Initial mastery
        self.assertEqual(self.profile.traits.concept_mastery["sequence"], 0.0)
        self.assertEqual(self.profile.traits.challenge_level, 1)

        # Successful puzzle attempt
        updated = PlayerModelEngine.record_action(
            self.profile, action_category="puzzle", challenge_success=True, concept="sequence"
        )
        self.assertGreater(updated.traits.concept_mastery["sequence"], 0.3)

        # Multiple successes increase challenge level
        updated = PlayerModelEngine.record_action(updated, "puzzle", True, "conditions")
        updated = PlayerModelEngine.record_action(updated, "puzzle", True, "loops")
        self.assertGreaterEqual(updated.traits.challenge_level, 2)

if __name__ == "__main__":
    unittest.main()
