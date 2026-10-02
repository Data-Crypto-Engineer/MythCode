"""
Logic & Learning Agent (Agent 5).
Bridges fantasy mechanics with real computational thinking and progressive Python unlocks.
"""
from typing import Dict, Any, List, Optional
from utils.logger import setup_logger
from core.learning_engine import LearningEngine
from models.learning import LearningProgress, PythonConceptReveal

logger = setup_logger("LogicLearningAgent")

class LogicLearningAgent:
    """Explains algorithmic principles and frames code reveals within fantasy lore."""

    ROLE = "Master of Runic Logic & Algorithms"
    GOAL = "Translate ancient magical rituals into fundamental computational concepts (Sequence, Conditions, Loops)."
    BACKSTORY = (
        "An ancient Magus who discovered centuries ago that all arcana follows immutable logical structures: "
        "step-by-step sequences, conditional branches, and repetitive cyclic loops."
    )

    def __init__(self, learning_engine: Optional[LearningEngine] = None, llm=None):
        self.engine = learning_engine or LearningEngine()
        self.llm = llm

    def present_challenge(self, puzzle_id: str) -> Optional[Dict[str, Any]]:
        puzzle = self.engine.get_puzzle(puzzle_id)
        if not puzzle:
            return None
        return {
            "puzzle_id": puzzle.id,
            "concept": puzzle.concept,
            "title": puzzle.title,
            "description": puzzle.description,
            "hint": puzzle.hint,
            "grid_size": puzzle.grid_size,
            "available_options": puzzle.available_options,
            "target_count": puzzle.target_count
        }

    def evaluate_submission(
        self,
        puzzle_id: str,
        user_input: Any,
        progress: LearningProgress
    ) -> Dict[str, Any]:
        """
        Executes objective deterministic puzzle evaluation. Never executes untrusted code.
        """
        is_correct, feedback, reveal, updated_progress = self.engine.validate_puzzle(
            puzzle_id, user_input, progress
        )

        return {
            "is_correct": is_correct,
            "feedback": feedback,
            "reveal": reveal.to_dict() if reveal else None,
            "updated_progress": updated_progress,
            "agent_commentary": (
                f"Computational principle '{puzzle_id}' successfully mastered. Python syntax unlocked."
                if is_correct else
                "Re-examine the sequence or logic. In programming, syntax and order dictate the outcome."
            )
        }
