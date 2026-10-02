"""
Computational thinking and progressive Python learning engine.
Deterministically validates puzzle answers and unlocks Python concept reveals.
Never executes arbitrary user code with eval() or exec().
"""
from typing import Dict, Any, List, Tuple, Optional
import json
import os
from models.learning import LearningProgress, PuzzleChallenge, PythonConceptReveal

class LearningEngine:
    """Evaluates programming challenges and manages The Unwritten Journal."""

    def __init__(self, puzzles_file: str = "data/puzzles.json"):
        self.puzzles: Dict[str, PuzzleChallenge] = {}
        self._load_puzzles(puzzles_file)

    def _load_puzzles(self, path: str):
        if not os.path.exists(path):
            return
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data.get("puzzles", []):
                p = PuzzleChallenge.from_dict(item)
                self.puzzles[p.id] = p

    def get_puzzle(self, puzzle_id: str) -> Optional[PuzzleChallenge]:
        return self.puzzles.get(puzzle_id)

    def validate_puzzle(
        self,
        puzzle_id: str,
        user_input: Any,
        progress: LearningProgress
    ) -> Tuple[bool, str, Optional[PythonConceptReveal], LearningProgress]:
        """
        Validates puzzle solution deterministically.
        Returns:
            is_correct (bool)
            feedback (str)
            reveal (Optional[PythonConceptReveal])
            updated_progress (LearningProgress)
        """
        puzzle = self.get_puzzle(puzzle_id)
        if not puzzle:
            return False, "Unknown challenge identifier.", None, progress

        # Track attempts
        progress.attempts[puzzle_id] = progress.attempts.get(puzzle_id, 0)
        progress.attempts[puzzle_id] += 1

        if puzzle.concept not in progress.concepts_encountered:
            progress.concepts_encountered.append(puzzle.concept)
            # Record Discovery in The Codex of Becoming (PART 9)
            concept_title = puzzle.concept.capitalize()
            progress.codex_entries.append({
                "category": "discovery",
                "concept": concept_title,
                "title": f"Discovery: {puzzle.title}",
                "fantasy_lore": puzzle.description,
                "programming_concept": getattr(puzzle.python_reveal, 'concept_name', concept_title),
                "code_example": getattr(puzzle.python_reveal, 'code_snippet', ''),
                "mastery_status": "In Progress"
            })

        is_correct = False
        feedback = ""

        # --- Stage 1: Sequence Validation ---
        if puzzle.concept == "sequence":
            # Expect list of steps: ["FORWARD", "FORWARD", "TURN_RIGHT", "FORWARD"]
            submitted_steps = [str(s).upper().strip() for s in (user_input if isinstance(user_input, list) else [user_input])]
            expected_steps = [s.upper().strip() for s in (puzzle.required_steps or [])]

            if submitted_steps == expected_steps:
                is_correct = True
                feedback = (
                    "Precision mechanical synchronization achieved! The Clockwork Guardian advances "
                    "in exact ordered sequence and slots the crystal into place."
                )
            else:
                is_correct = False
                feedback = (
                    f"The gears grind to a halt. Order matters in execution: you commanded "
                    f"{' -> '.join(submitted_steps) if submitted_steps else 'nothing'}, but the terrain "
                    f"requires {len(expected_steps)} precise sequential actions."
                )

        # --- Stage 2: Conditions Validation ---
        elif puzzle.concept == "conditions":
            selected_option_id = str(user_input).strip()
            # Correct option id in puzzles.json is 'has_seal'
            if selected_option_id == "has_seal":
                is_correct = True
                feedback = (
                    "The runic gate detects the Emerald Seal, evaluates the condition as True, "
                    "and parts its ancient stone arches!"
                )
            else:
                is_correct = False
                feedback = (
                    "The runes pulse red. The gatekeeper condition was not satisfied. "
                    "An if/else branch requires fulfilling the truth condition before the portal will yield."
                )

        # --- Stage 3: Loops Validation ---
        elif puzzle.concept == "loops":
            action = str(user_input).strip()
            if action == puzzle.correct_action or action == "LOOP_5_STEPS":
                is_correct = True
                feedback = (
                    "The harmonic energy loop activates! Five crystalline resonance tiles ignite "
                    "in smooth iterative succession, powering the reservoir pump."
                )
            else:
                is_correct = False
                feedback = (
                    "A single burst or random pulse dissipated before reaching the fifth tile. "
                    "A repetitive loop is required to iterate across all 5 tiles seamlessly."
                )

        # Update progress and unlocks
        reveal = None
        if is_correct:
            if puzzle_id not in progress.completed_puzzles:
                progress.completed_puzzles.append(puzzle_id)

            reveal = puzzle.python_reveal
            # Add to unlocked reveals if not already present
            already_unlocked = any(r.get("concept_name") == reveal.concept_name for r in progress.unlocked_reveals)
            if not already_unlocked:
                progress.unlocked_reveals.append(reveal.to_dict())

        return is_correct, feedback, reveal, progress

    def request_hint(self, puzzle_id: str, progress: LearningProgress) -> Tuple[str, LearningProgress]:
        puzzle = self.get_puzzle(puzzle_id)
        if not puzzle:
            return "No hint available.", progress
        progress.hint_uses[puzzle_id] = progress.hint_uses.get(puzzle_id, 0) + 1
        return puzzle.hint, progress
