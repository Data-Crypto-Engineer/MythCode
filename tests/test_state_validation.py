"""
Tests for deterministic state validation and invariant protection.
"""
import unittest
from models.world import WorldState
from core.state_validator import StateValidator

class TestStateValidation(unittest.TestCase):

    def setUp(self):
        self.world = WorldState()

    def test_valid_location_transition(self):
        proposed = {"current_location": "Ancient Grove"}
        valid, issues, new_world = StateValidator.validate_transition(self.world, proposed)
        self.assertTrue(valid)
        self.assertEqual(len(issues), 0)
        self.assertEqual(new_world.current_location, "Ancient Grove")
        self.assertIn("Ancient Grove", new_world.discovered_locations)

    def test_reject_impossible_location(self):
        proposed = {"current_location": "Mars Rover Base"}
        valid, issues, new_world = StateValidator.validate_transition(self.world, proposed)
        self.assertFalse(valid)
        self.assertTrue(any("Rejected unknown location" in i for i in issues))
        # Current location should not change to invalid location
        self.assertEqual(new_world.current_location, "Whispering Village")

    def test_clamp_village_morale(self):
        # Morale clamped between 0 and 100
        proposed = {"village_morale": 999}
        valid, issues, new_world = StateValidator.validate_transition(self.world, proposed)
        self.assertTrue(valid)
        self.assertEqual(new_world.village_morale, 100)

        proposed_low = {"village_morale": -50}
        _, _, new_world_low = StateValidator.validate_transition(self.world, proposed_low)
        self.assertEqual(new_world_low.village_morale, 0)

    def test_water_supply_valid_states(self):
        proposed = {"water_supply": "restored"}
        valid, _, new_world = StateValidator.validate_transition(self.world, proposed)
        self.assertTrue(valid)
        self.assertEqual(new_world.water_supply, "restored")

        invalid_water = {"water_supply": "atomic_liquid"}
        valid_bad, issues, _ = StateValidator.validate_transition(self.world, invalid_water)
        self.assertFalse(valid_bad)
        self.assertTrue(any("Invalid water supply status" in i for i in issues))

if __name__ == "__main__":
    unittest.main()
