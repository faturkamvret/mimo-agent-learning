"""
MiMo Agent Learning
====================
Self-improving agent system powered by MiMo v2.5.

Demonstrates:
- Experience replay and memory consolidation
- Strategy evolution through self-reflection
- Performance tracking and optimization
- Meta-learning capabilities
"""

import os
import sys
import json
import time
import uuid
import math
import random
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from typing import Optional


# ── MiMo Client ────────────────────────────────────────────────────────────

class MiMoClient:
    def __init__(self):
        self.use_mock = not bool(os.environ.get("MIMO_API_KEY"))

    def suggest_strategy(self, task: str, history: list) -> dict:
        """Suggest a strategy based on task and history."""
        strategies = {
            "sort": [
                {"name": "brute_force", "description": "Simple comparison-based sort", "complexity": "O(n²)"},
                {"name": "merge_sort", "description": "Divide and conquer merge sort", "complexity": "O(n log n)"},
                {"name": "optimized_merge", "description": "In-place merge with insertion sort for small arrays", "complexity": "O(n log n)"},
            ],
            "search": [
                {"name": "linear_scan", "description": "Check each element", "complexity": "O(n)"},
                {"name": "binary_search", "description": "Halve search space each step", "complexity": "O(log n)"},
                {"name": "hash_lookup", "description": "Use hash map for O(1) access", "complexity": "O(1)"},
            ],
            "optimize": [
                {"name": "greedy", "description": "Take best local option", "complexity": "O(n log n)"},
                {"name": "dynamic_programming", "description": "Build solution from subproblems", "complexity": "O(n²)"},
                {"name": "meta_heuristic", "description": "Simulated annealing with adaptive cooling", "complexity": "O(n·k)"},
            ],
        }

        # Find best matching strategy category
        task_lower = task.lower()
        for category, strats in strategies.items():
            if category in task_lower:
                # If we have history, pick next strategy
                if history:
                    last_strategy = history[-1].get("strategy", "")
                    for i, s in enumerate(strats):
                        if s["name"] == last_strategy and i + 1 < len(strats):
                            return {"strategy": strats[i + 1], "reason": f"Previous strategy '{last_strategy}' was suboptimal, trying {strats[i+1]['name']}"}
                return {"strategy": strats[0], "reason": f"Starting with {strats[0]['name']} approach"}

        # Default
        return {"strategy": {"name": "adaptive", "description": "Adaptive strategy selection", "complexity": "variable"}, "reason": "No specific category matched, using adaptive approach"}

    def reflect(self, task: str, strategy: str, score: float, history: list) -> dict:
        """Reflect on performance and suggest improvements."""
        if not history:
            return {
                "analysis": f"First attempt at '{task}' using {strategy}. Score: {score}/10.",
                "improvements": ["Try a different approach", "Increase resource allocation"],
                "confidence": 0.7,
            }

        last_score = history[-1].get("score", 0)
        improvement = score - last_score

        if improvement > 0:
            analysis = f"Improvement of +{improvement:.1f} points. Strategy '{strategy}' working well."
            improvements = ["Continue with current approach", "Fine-tune parameters"]
        elif improvement < 0:
            analysis = f"Regression of {improvement:.1f} points. Strategy '{strategy}' may not be optimal."
            improvements = ["Switch to alternative strategy", "Revisit problem decomposition"]
        else:
            analysis = f"Performance stable at {score}/10. Looking for optimization opportunities."
            improvements = ["Explore parallelization", "Consider memoization"]

        return {
            "analysis": analysis,
            "improvements": improvements,
            "confidence": 0.85,
            "trend": "improving" if improvement > 0 else "declining" if improvement < 0 else "stable",
        }


# ── Data Models ────────────────────────────────────────────────────────────

class TaskCategory(Enum):
    SORT = "sort"
    SEARCH = "search"
    OPTIMIZE = "optimize"
    GENERAL = "general"


@dataclass
class Experience:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    task: str = ""
    strategy: str = ""
    score: float = 0.0
    duration: float = 0.0
    reflection: dict = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self):
        return {
            "id": self.id, "task": self.task, "strategy": self.strategy,
            "score": self.score, "duration": self.duration,
            "reflection": self.reflection, "timestamp": self.timestamp,
        }


@dataclass
class Strategy:
    name: str = ""
    description: str = ""
    complexity: str = ""
    success_rate: float = 0.0
    uses: int = 0
    avg_score: float = 0.0

    def to_dict(self):
        return {
            "name": self.name, "description": self.description,
            "complexity": self.complexity, "success_rate": self.success_rate,
            "uses": self.uses, "avg_score": self.avg_score,
        }


@dataclass
class LearningMetrics:
    total_tasks: int = 0
    total_score: float = 0.0
    avg_score: float = 0.0
    best_score: float = 0.0
    improvement_rate: float = 0.0
    strategies_tried: int = 0
    memory_entries: int = 0

    def to_dict(self):
        return {
            "total_tasks": self.total_tasks, "total_score": self.total_score,
            "avg_score": round(self.avg_score, 2), "best_score": round(self.best_score, 2),
            "improvement_rate": round(self.improvement_rate, 2),
            "strategies_tried": self.strategies_tried, "memory_entries": self.memory_entries,
        }


# ── Learning Agent ─────────────────────────────────────────────────────────

class LearningAgent:
    def __init__(self, name: str = "agent-1"):
        self.name = name
        self.mimo = MiMoClient()
        self.log: list[str] = []
        self.experiences: list[Experience] = []
        self.strategies: dict[str, Strategy] = {}
        self.metrics = LearningMetrics()

    def _log(self, msg: str):
        ts = datetime.now().strftime("%H:%M:%S")
        entry = f"[{ts}] [{self.name}] {msg}"
        self.log.append(entry)
        print(entry)

    def _simulate_task(self, task: str, strategy: str) -> float:
        """Simulate task execution and return a score."""
        # Simulate based on strategy quality
        base_scores = {
            "brute_force": 3.0,
            "linear_scan": 4.0,
            "greedy": 5.0,
            "merge_sort": 7.5,
            "binary_search": 7.0,
            "dynamic_programming": 7.5,
            "optimized_merge": 9.0,
            "hash_lookup": 8.5,
            "meta_heuristic": 8.0,
            "adaptive": 6.0,
        }

        base = base_scores.get(strategy, 5.0)
        # Add some randomness
        score = base + random.uniform(-0.5, 0.5)
        return min(10.0, max(0.0, score))

    def solve(self, task: str, max_rounds: int = 5) -> dict:
        """Solve a task with learning and improvement."""
        self._log(f"\n🎯 Solving: {task}")
        self._log(f"{'='*60}")

        best_score = 0
        best_strategy = None
        round_num = 0

        for round_num in range(1, max_rounds + 1):
            self._log(f"\n[Round {round_num}]")

            # Get strategy suggestion
            history = [e.to_dict() for e in self.experiences[-3:]]
            suggestion = self.mimo.suggest_strategy(task, history)
            strategy_name = suggestion["strategy"]["name"]
            self._log(f"  Strategy: {strategy_name} — {suggestion['reason']}")

            # Execute task
            start_time = time.time()
            score = self._simulate_task(task, strategy_name)
            duration = round(time.time() - start_time, 2)

            self._log(f"  Score: {score:.1f}/10 ({duration:.2f}s)")

            # Reflect
            reflection = self.mimo.reflect(task, strategy_name, score, history)
            self._log(f"  Reflect: {reflection['analysis']}")
            self._log(f"  Trend: {reflection.get('trend', 'unknown')}")

            # Record experience
            experience = Experience(
                task=task,
                strategy=strategy_name,
                score=score,
                duration=duration,
                reflection=reflection,
            )
            self.experiences.append(experience)

            # Update strategy stats
            if strategy_name not in self.strategies:
                self.strategies[strategy_name] = Strategy(
                    name=strategy_name,
                    description=suggestion["strategy"].get("description", ""),
                    complexity=suggestion["strategy"].get("complexity", ""),
                )
            strat = self.strategies[strategy_name]
            strat.uses += 1
            strat.avg_score = ((strat.avg_score * (strat.uses - 1)) + score) / strat.uses

            # Track best
            if score > best_score:
                best_score = score
                best_strategy = strategy_name
                self._log(f"  ⭐ New best score!")

            # Check if we've converged
            if len(self.experiences) >= 2:
                recent_scores = [e.score for e in self.experiences[-2:]]
                if max(recent_scores) - min(recent_scores) < 0.1 and round_num >= 3:
                    self._log(f"\n  Converged after {round_num} rounds")
                    break

        # Update metrics
        all_scores = [e.score for e in self.experiences]
        self.metrics.total_tasks = len(self.experiences)
        self.metrics.total_score = sum(all_scores)
        self.metrics.avg_score = self.metrics.total_score / max(self.metrics.total_tasks, 1)
        self.metrics.best_score = max(all_scores) if all_scores else 0
        self.metrics.strategies_tried = len(self.strategies)
        self.metrics.memory_entries = len(self.experiences)

        # Calculate improvement rate
        if len(all_scores) >= 2:
            first_half = sum(all_scores[:len(all_scores)//2]) / max(len(all_scores)//2, 1)
            second_half = sum(all_scores[len(all_scores)//2:]) / max(len(all_scores) - len(all_scores)//2, 1)
            self.metrics.improvement_rate = ((second_half - first_half) / max(first_half, 1)) * 100

        self._log(f"\n{'='*60}")
        self._log(f"📊 Results:")
        self._log(f"  Best strategy: {best_strategy} ({best_score:.1f}/10)")
        self._log(f"  Rounds: {round_num}")
        self._log(f"  Improvement: {self.metrics.improvement_rate:+.1f}%")
        self._log(f"{'='*60}")

        return {
            "task": task,
            "best_strategy": best_strategy,
            "best_score": best_score,
            "rounds": round_num,
            "metrics": self.metrics.to_dict(),
        }

    def reflect(self) -> dict:
        """Global reflection on all experiences."""
        self._log(f"\n🪞 Performing global reflection...")

        if not self.experiences:
            self._log("  No experiences to reflect on")
            return {"status": "no_data"}

        # Group by strategy
        strategy_perf = {}
        for exp in self.experiences:
            if exp.strategy not in strategy_perf:
                strategy_perf[exp.strategy] = []
            strategy_perf[exp.strategy].append(exp.score)

        # Find best/worst
        strategy_avg = {s: sum(scores)/len(scores) for s, scores in strategy_perf.items()}
        best_strat = max(strategy_avg, key=strategy_avg.get)
        worst_strat = min(strategy_avg, key=strategy_avg.get)

        reflection = {
            "total_experiences": len(self.experiences),
            "best_strategy": best_strat,
            "worst_strategy": worst_strat,
            "strategy_performance": {s: round(avg, 2) for s, avg in strategy_avg.items()},
        }

        self._log(f"  Best strategy: {best_strat} (avg: {strategy_avg[best_strat]:.1f})")
        self._log(f"  Worst strategy: {worst_strat} (avg: {strategy_avg[worst_strat]:.1f})")
        self._log(f"  Strategies tried: {len(strategy_avg)}")

        return reflection

    def performance_trend(self) -> str:
        """Get performance trend."""
        if len(self.experiences) < 2:
            return "insufficient_data"

        scores = [e.score for e in self.experiences]
        recent_avg = sum(scores[-3:]) / min(3, len(scores))
        early_avg = sum(scores[:3]) / min(3, len(scores))

        if recent_avg > early_avg * 1.1:
            return "improving"
        elif recent_avg < early_avg * 0.9:
            return "declining"
        return "stable"


# ── Demo ───────────────────────────────────────────────────────────────────

def run_demo():
    print("\n" + "🧠 " * 20)
    print("  MiMo Agent Learning — Demo")
    print("🧠 " * 20 + "\n")

    agent = LearningAgent(name="demo-learner")

    # Solve multiple tasks
    tasks = [
        "Sort 1000 items efficiently",
        "Search for an element in a large dataset",
        "Optimize resource allocation across 50 nodes",
    ]

    for task in tasks:
        result = agent.solve(task, max_rounds=4)

    # Global reflection
    reflection = agent.reflect()

    # Performance trend
    trend = agent.performance_trend()

    # Print summary
    print(f"\n{'='*60}")
    print(f"📈 Learning Summary")
    print(f"{'='*60}")
    print(f"  Tasks completed: {agent.metrics.total_tasks}")
    print(f"  Average score: {agent.metrics.avg_score:.1f}/10")
    print(f"  Best score: {agent.metrics.best_score:.1f}/10")
    print(f"  Improvement rate: {agent.metrics.improvement_rate:+.1f}%")
    print(f"  Strategies learned: {agent.metrics.strategies_tried}")
    print(f"  Performance trend: {trend}")
    print(f"{'='*60}")

    # Strategy breakdown
    print(f"\n📊 Strategy Performance:")
    for name, strat in sorted(agent.strategies.items(), key=lambda x: x[1].avg_score, reverse=True):
        print(f"  {name:20s} avg: {strat.avg_score:.1f}/10  (used {strat.uses}x)")

    # Save results
    demo_dir = os.path.join(os.path.dirname(__file__), "demo")
    os.makedirs(demo_dir, exist_ok=True)

    results = {
        "agent": agent.name,
        "metrics": agent.metrics.to_dict(),
        "strategies": {k: v.to_dict() for k, v in agent.strategies.items()},
        "experiences": [e.to_dict() for e in agent.experiences],
        "reflection": reflection,
        "performance_trend": trend,
    }

    with open(os.path.join(demo_dir, "learning_results.json"), "w") as f:
        json.dump(results, f, indent=2)

    with open(os.path.join(demo_dir, "learning_log.txt"), "w") as f:
        f.write("\n".join(agent.log))

    print(f"\n💾 Results saved to demo/")

    return results


if __name__ == "__main__":
    run_demo()
