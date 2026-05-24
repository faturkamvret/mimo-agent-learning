# MiMo Agent Learning

> 🧠 Self-improving agent system powered by MiMo v2.5 long-chain reasoning

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![MiMo](https://img.shields.io/badge/MiMo-v2.5-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## Overview

A self-improving AI agent system that learns from its interactions, adapts its strategies, and continuously optimizes its performance. Uses MiMo v2.5's reasoning to reflect on past actions, identify patterns, and evolve its approach.

**Key capabilities:**
- Experience replay and memory consolidation
- Strategy evolution through self-reflection
- Performance tracking and optimization
- Transfer learning across tasks
- Meta-learning: learning how to learn

## Architecture

```
┌──────────────────────────────────────────────────────┐
│              Agent Learning System                     │
│                                                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │
│  │ Learner  │  │ Reflector│  │   Optimizer      │   │
│  │  (MiMo)  │  │  (MiMo)  │  │    (MiMo)        │   │
│  └─────┬────┘  └─────┬────┘  └────────┬─────────┘   │
│        │              │                 │              │
│  ┌─────▼──────────────▼─────────────────▼────────┐   │
│  │              Learning Loop                      │   │
│  │  [Act] → [Observe] → [Reflect] → [Adapt] →     │   │
│  │  [Improve] → [Act]...                           │   │
│  └───────────────────────────────────────────────┘   │
│        │              │                 │              │
│  ┌─────▼──┐    ┌─────▼──┐    ┌────────▼────────┐   │
│  │Memory  │    │Strategy│    │   Performance   │   │
│  │Bank    │    │Library │    │   Metrics       │   │
│  └────────┘    └────────┘    └─────────────────┘   │
└──────────────────────────────────────────────────────┘
```

## Setup

```bash
git clone https://github.com/YOUR_USERNAME/mimo-agent-learning.git
cd mimo-agent-learning

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

export MIMO_API_KEY="your-api-key"  # Optional

python main.py --demo
```

## Usage

```python
from agent_learning import LearningAgent

agent = LearningAgent(name="learner-1")

# Solve a task
result = agent.solve("Optimize the sorting algorithm for this dataset")

# Agent reflects and improves
agent.reflect()

# Check improvement
print(f"Performance trend: {agent.performance_trend()}")
print(f"Strategies learned: {len(agent.strategies)}")
```

## Demo

```bash
python main.py --demo
```

Expected output:

```
[Agent] 🧠 Learning Agent initialized
[Agent] Attempting task: "Sort 1000 items efficiently"
[Round 1] Strategy: brute_force → Score: 3.2/10
[Reflect] MiMo analysis: "Selection sort is O(n²) — try divide-and-conquer"
[Round 2] Strategy: merge_sort → Score: 7.8/10
[Reflect] MiMo analysis: "Merge sort works well — can we optimize memory?"
[Round 3] Strategy: optimized_merge → Score: 9.1/10
[Learning] 🎯 Performance improved 184% over 3 iterations

📊 Learning Summary:
  Tasks completed: 3
  Best strategy: optimized_merge (score: 9.1)
  Improvement rate: 61%/iteration
  Memory entries: 12
```

## Demo Output

<!-- ![Learning Progress](demo/learning_progress.png) -->

## Roadmap

- [ ] Multi-agent collaborative learning
- [ ] Curriculum learning (progressive task difficulty)
- [ ] Cross-domain transfer learning
- [ ] Visualization of learning curves

## License

MIT License — see [LICENSE](LICENSE).

---

*Powered by [Xiaomi MiMo v2.5](https://github.com/XiaomiMiMo)*
