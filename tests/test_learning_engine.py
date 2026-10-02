"""
Tests for deterministic puzzle validation and Python code reveals.
"""
import unittest
from core.learning_engine import LearningEngine
from models.learning import LearningProgress

class TestLearningEngine(unittest.TestCase):

    def setUp(self):
        self.engine = LearningEngine("data/puzzles.json")
        self.progress = LearningProgress()

    def test_sequence_puzzle_success(self):
        puz_id = "puzzle_sequence_guardian"
        correct_steps = ["FORWARD", "FORWARD", "TURN_RIGHT", "FORWARD"]
        is_ok, feedback, reveal, updated_prog = self.engine.validate_puzzle(
            puz_id, correct_steps, self.progress
        )
        self.assertTrue(is_ok)
        self.assertIn("puz_sequence_guardian".replace("puz_", "puzzle_"), updated_prog.completed_puzzles)
        self.assertIsNotNone(reveal)
        self.assertEqual(reveal.concept_name, "Sequential Execution")
        self.assertIn("move_forward()", reveal.code_snippet)

    def test_sequence_puzzle_failure(self):
        puz_id = "puzzle_sequence_guardian"
        wrong_steps = ["FORWARD", "TURN_LEFT"]
        is_ok, feedback, reveal, updated_prog = self.engine.validate_puzzle(
            puz_id, wrong_steps, self.progress
        )
        self.assertFalse(is_ok)
        self.assertIsNone(reveal)
        self.assertIn("Order matters in execution", feedback)

    def test_conditions_puzzle_evaluation(self):
        puz_id = "puzzle_conditional_door"
        # Correct choice: has_seal
        is_ok, _, reveal, _ = self.engine.validate_puzzle(puz_id, "has_seal", self.progress)
        self.assertTrue(is_ok)
        self.assertIsNotNone(reveal)
        self.assertEqual(reveal.concept_name, "Conditional Logic (if / else)")

        # Wrong choice: force_open
        is_bad, _, reveal_bad, _ = self.engine.validate_puzzle(puz_id, "force_open", self.progress)
        self.assertFalse(is_bad)
        self.assertIsNone(reveal_bad)

    def test_loops_puzzle_evaluation(self):
        puz_id = "puzzle_loop_tiles"
        is_ok, _, reveal, _ = self.engine.validate_puzzle(puz_id, "LOOP_5_STEPS", self.progress)
        self.assertTrue(is_ok)
        self.assertIsNotNone(reveal)
        self.assertEqual(reveal.concept_name, "Iteration & Loops (for ... in range())")

    def test_hint_request(self):
        puz_id = "puzzle_sequence_guardian"
        hint, prog = self.engine.request_hint(puz_id, self.progress)
        self.assertTrue(len(hint) > 10)
        self.assertEqual(prog.hint_uses.get(puz_id), 1)

if __name__ == "__main__":
    unittest.main()
