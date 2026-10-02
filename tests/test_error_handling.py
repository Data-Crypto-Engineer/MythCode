"""
Tests for error handling, fallback scenes, and safe state preservation.
"""
import unittest
from utils.error_handler import handle_exception, fallback_narrative_scene, AIProviderError
from core.state_validator import StateValidator
from models.world import WorldState

class TestErrorHandling(unittest.TestCase):

    def test_handle_exception_sanitization(self):
        fake_exc = AIProviderError("Connection timeout with api_key=AIzaSySecretKey999")
        report = handle_exception(fake_exc, "Test Context")
        self.assertEqual(report["status"], "error")
        self.assertEqual(report["error_type"], "AIProviderError")
        self.assertTrue(report["fallback_engaged"])

    def test_fallback_narrative_scene(self):
        scene = fallback_narrative_scene("River Aqueduct", "Look at waterwheel")
        self.assertIn("Aqueduct", scene["title"])
        self.assertIn("speaker", scene)
        self.assertTrue(len(scene["choices"]) > 0)

    def test_state_preserved_when_action_invalid(self):
        world = WorldState(current_location="Whispering Village", village_morale=70)
        invalid_mutation = {
            "current_location": "Invalid Unknown Dimension",
            "village_morale": "CORRUPTED_STRING"
        }
        is_valid, issues, preserved_state = StateValidator.validate_transition(world, invalid_mutation)
        self.assertFalse(is_valid)
        self.assertEqual(preserved_state.current_location, "Whispering Village")
        # Village morale preserved at 70
        self.assertEqual(preserved_state.village_morale, 70)

if __name__ == "__main__":
    unittest.main()
