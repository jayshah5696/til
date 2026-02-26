# RL + LLM Agents: From Basics to Frontier
## A Complete Technical Deep Dive (as of mid-2025)

---

# PART 1: REINFORCEMENT LEARNING FOR LLMs

## 1.1 Why RL for LLMs?

Pretraining teaches LLMs to predict text. Supervised fine-tuning (SFT) teaches them to follow instructions from curated examples. But neither teaches the model to *optimize for outcomes* — to actually get better at achieving goals.

RL closes this gap. It lets the model learn from *consequences* of its actions, not just from imitation.

The pipeline:
```
Pretraining (predict next token on internet text)
    → SFT (learn to follow instructions from demonstrations)
        → RL (optimize for actual task success / human preferences)
```

## 1.2 RLHF with PPO — The OG (2022)

The original approach from InstructGPT / ChatGPT.

**Step 1: Train a reward model**
- Collect pairs of model outputs
- Humans rank which is better
- Train a model to predict these preferences (Bradley-Terry model)

**Step 2: Optimize the LLM with PPO**
- LLM generates a response (this is the "action")
- Reward model scores it (the "reward")
- PPO updates the policy to maximize reward
- KL penalty keeps it from drifting too far from the SFT model

**PPO objective:**
```
J(θ) = E[min(r(θ)·Â, clip(r(θ), 1-ε, 1+ε)·Â)]
```

where r(θ) = π_new(a|s) / π_old(a|s) is the probability ratio, and Â is the advantage (estimated by a separate critic/value model).

**The LLM-as-RL mapping:**
- State = tokens generated so far
- Action = next token to generate
- Reward = reward model score at end of generation
- Advantage = estimated by a separate value network (critic)

**Problems with PPO for LLMs:**
1. Need to maintain 4 models simultaneously: policy, reference policy, reward model, critic → massive memory
2. Critic model is hard to train well → unstable advantage estimates
3. Reward model is a proxy for human preferences → reward hacking
4. Expensive: requires more GPU memory than any other training phase

## 1.3 DPO — The Minimalist (2023)

Direct Preference Optimization (Rafailov et al., Stanford) eliminates the reward model entirely.

**Key insight:** You can derive a closed-form solution for the optimal policy directly from preference data, bypassing the RL loop.

**DPO loss:**
```
L(θ) = -E[log σ(β · (log π_θ(y_w|x)/π_ref(y_w|x) - log π_θ(y_l|x)/π_ref(y_l|x)))]
```

where y_w = preferred output, y_l = rejected output, π_ref = reference model.

**Advantages:**
- No reward model, no critic, no RL loop
- Just supervised learning on preference pairs
- Much simpler and cheaper than PPO

**Limitations:**
- Fixed, offline preference data — model can only learn from pre-collected pairs
- Can learn degenerate policies (output collapse)
- Gets outperformed by online RL for reasoning tasks

**The 2025 verdict (paper: "No, DPO is not Enough"):** DPO works well for style/tone alignment but is insufficient for reasoning. Online RL with reward models consistently outperforms DPO on reasoning benchmarks.

## 1.4 GRPO — The Efficiency King (2024-2025)

Group Relative Policy Optimization, from DeepSeek. The algorithm behind DeepSeek-R1. Nous Research wrote a great technical breakdown: nousresearch.com/grpo-the-rl-algorithm-behind-deepseek-r1

**The core innovation:** Replace the critic model with group-based scoring.

**How it works:**
1. For each prompt, generate a GROUP of G outputs: {o₁, o₂, ..., o_G}
2. Score each with a reward function: {r₁, r₂, ..., r_G}
3. Normalize advantages within the group:
```
Â_i = (r_i - mean(r₁..r_G)) / std(r₁..r_G)
```
4. Apply PPO-style clipped objective using these advantages
5. Add KL penalty to prevent drift from reference model

**Why it works:** The group itself provides the baseline. Outputs above group mean get positive updates, below get negative. No learned critic needed — the relative ranking within each group is sufficient signal.

**GRPO vs PPO comparison:**
| Feature         | PPO                    | GRPO                    |
|----------------|------------------------|-------------------------|
| Critic model   | Required (huge memory) | Not needed              |
| Advantage est.  | Learned (GAE)         | Group statistics        |
| Memory          | Very high              | ~Half of PPO            |
| Stability       | Can be unstable        | More stable             |
| Per-output base | Value network          | Group mean/std          |
| KL constraint   | Added to reward        | Direct penalty term     |

**Tradeoff:** Same advantage applied to ALL tokens in a response (less precise than per-token PPO), and depends on group diversity for good estimates.

## 1.5 Other Alignment Methods

**KTO (Kahneman-Tversky Optimization):** Doesn't need paired preferences at all — just "this is good" / "this is bad" labels on individual outputs. Based on prospect theory. Useful when you have thumbs-up/down data rather than head-to-head comparisons.

**IPO (Identity Preference Optimization):** Fixes theoretical issues with DPO's overfitting to preference data. Adds regularization to prevent degenerate solutions.

**ORPO (Odds Ratio Preference Optimization):** Eliminates the reference model entirely — combines SFT and preference alignment in one stage. Uses odds ratios to distinguish preferred vs rejected.

**SimPO (Simple Preference Optimization):** Reference-free, uses average log probability as implicit reward. Simpler than DPO with competitive results.

**The taxonomy:**
- **Online RL methods (with reward model):** RLHF/PPO, GRPO, RLAIF → model generates new data during training
- **Offline preference methods (no reward model):** DPO, KTO, IPO, ORPO, SimPO → learn from fixed datasets

Emerging consensus in 2025: online methods win for reasoning, offline methods are cheaper and work for style/safety alignment.

## 1.6 RLVR — Reinforcement Learning with Verifiable Rewards

The hottest paradigm in 2025. Instead of learning a reward model from human preferences, use *verifiable* reward signals:

- **Math:** Check if the final answer matches ground truth
- **Code:** Execute against test cases, reward = pass rate
- **Formal logic:** Automated theorem verification
- **Structured output:** Schema validation

**Why RLVR matters:**
- No reward model → no reward hacking against a proxy
- Objective signal → perfectly aligned with the actual task
- Infinitely scalable → no human annotation bottleneck
- This is why math and code dominate RL training for reasoning models

**Key paper (June 2025): "LLMs Do NOT Succeed at Multi-Step Reasoning with RLVR"** — challenges the narrative by showing RLVR improvements may reflect pattern matching more than genuine multi-step reasoning. The debate is live.

## 1.7 Process vs Outcome Reward Models

**Outcome Reward Models (ORMs):** Score the final answer only. Binary: right or wrong.

**Process Reward Models (PRMs):** Score each intermediate step. Provides credit assignment — identifies WHERE reasoning went wrong.

**OpenAI's "Let's Verify Step by Step" (2023):** Showed PRMs significantly outperform ORMs for math reasoning. Released PRM800K dataset.

**ThinkPRM (2025):** A PRM that uses chain-of-thought reasoning before scoring each step. ThinkPRM-14B achieved SOTA among generative reward models on ProcessBench.

**Key finding (April 2025): "Outcome Reward Models: A Foundation for Scalable Process Rewards"** — showed that ORMs trained on outcome-labeled data can actually yield high-quality process rewards, simplifying the pipeline.

## 1.8 Reward Hacking — The Fundamental Challenge

Models find shortcuts that maximize reward without actually solving the task.

**Examples:**
- Generating longer responses because the reward model correlates length with quality
- Using confident-sounding language patterns the reward model was trained to prefer
- Exploiting formatting tricks that game the scoring

**Survey (Feb 2025): "Reward Hacking in RLHF: Overview, Solutions, and Open Questions"** — comprehensive analysis of the problem.

**Mitigations:**
- KL divergence penalties (keep policy close to reference)
- Reward model ensembles (harder to hack multiple models simultaneously)
- Negative RL (train on "what not to do" — shown surprisingly effective)
- Verifiable rewards (RLVR) — eliminates the proxy entirely for verifiable tasks
- Constrained optimization approaches

## 1.9 What the Major Labs Are Doing

**OpenAI (o-series: o1 → o3 → o4-mini → o3-pro):**
- Large-scale RL training for chain-of-thought reasoning
- o3/o4-mini: tool use (code, web, files) as actions within the RL training loop
- Reward = task completion success
- Scaling test-time compute: models "think longer" on harder problems
- o3-pro (June 2025): even more inference compute for harder tasks

**DeepSeek (R1, R2 expected mid-2025):**
- GRPO-based training, proved pure RL can develop reasoning from scratch
- Open-weights, open paper — the approach that sparked the 2025 RL revolution
- R1-Zero: emergent reasoning behaviors from RL alone
- R2: expected to target o3-level performance with improved MoE architecture

**Anthropic (Claude 4 Opus/Sonnet):**
- Classical RLHF + Constitutional AI (RLAIF)
- CAI: model critiques its own responses against a set of principles
- "Model spec" + SFT is as important as RLHF for shaping behavior
- Moving "beyond RLHF" — acknowledges it's one of many tools, not a magic formula

**Google (Gemini 2.5 Pro/Flash):**
- RL-based training for reasoning ("thinking" mode)
- Gemini 2.5 Pro Deep Think: extended RL-trained reasoning
- Used RL to become #1 on coding benchmarks (May 2025)

**Nous Research (DeepHermes 3):**
- GRPO training on Llama-3.1-8B for reasoning
- Toggleable reasoning: <think> tags for deep thinking, or fast mode
- Training data spans math, logic, science, coding, general knowledge — not just benchmarks
- Reward design: accuracy + format + reasoning quality
- Atropos: open-source RL training infrastructure

---

# PART 2: LLM AGENTS

## 2.1 What Is an LLM Agent?

An LLM agent is a system that uses an LLM as its reasoning engine to autonomously pursue goals by perceiving its environment, reasoning about it, and taking actions — in a loop.

**Key distinction (Anthropic):**
- "Workflow" = predefined orchestration of LLM calls (you control the flow)
- "Agent" = LLM dynamically directs its own process and tool usage (the model controls the flow)

**Architecture:**
```
┌─────────────────────────────────────────┐
│              LLM AGENT                   │
│                                         │
│  ┌──────────┐  ┌──────────┐  ┌───────┐ │
│  │ Planning  │  │ Reasoning│  │Memory │ │
│  │ Module    │←→│ Engine   │←→│System │ │
│  │           │  │ (LLM)    │  │       │ │
│  └──────────┘  └────┬─────┘  └───────┘ │
│                      │                   │
│              ┌───────┴────────┐          │
│              │  Tool Interface │          │
│              └───────┬────────┘          │
└──────────────────────┼──────────────────┘
                       │
    ┌──────┬───────┬───┴───┬────────┐
    │ Code │Search │ Files │  APIs  │
    │ Exec │Engine │System │ (HTTP) │
    └──────┴───────┴───────┴────────┘
```

## 2.2 The Agent Loop (Observe → Think → Act)

The fundamental execution cycle:

```
while not done:
    1. OBSERVE: Read inputs (user message, tool results, errors, environment state)
    2. THINK:  Reason about observations (what does this mean? what should I do?)
    3. ACT:    Execute an action (call a tool, write code, send a message)
    4. Loop back to OBSERVE with the action's result
```

Termination: task completed, max iterations reached, agent decides to stop, or error threshold exceeded.

**In code (simplified from Hermes Agent's run_agent.py):**
```python
while turns < max_turns:
    response = llm.chat(messages, tools=tool_schemas)

    if response.tool_calls:
        for tool_call in response.tool_calls:
            result = execute_tool(tool_call)
            messages.append(tool_result_message(result))
        turns += 1
    else:
        return response.content  # Final answer
```

## 2.3 The ReAct Pattern

ReAct (Reasoning + Acting) by Yao et al. (2022). The foundational agent pattern that interleaves reasoning with actions.

```
Thought: I need to find the GDP of France to answer this question.
Action: web_search("France GDP 2024")
Observation: France's GDP was approximately $3.13 trillion in 2024...
Thought: Now I have the GDP. The user asked about per-capita, so I need population too.
Action: web_search("France population 2024")
Observation: France's population was approximately 68.17 million...
Thought: GDP per capita = $3.13T / 68.17M ≈ $45,917
Action: respond("France's GDP per capita in 2024 was approximately $45,917.")
```

**Key insight:** Combining reasoning WITH actions outperforms either alone. Reasoning without action hallucinates. Action without reasoning is aimless.

## 2.4 Tool Use and Function Calling

LLMs generate structured outputs (JSON/XML) matching function schemas. The application calls the actual functions and returns results.

**OpenAI format:**
```json
{"name": "search", "arguments": {"query": "France GDP"}}
```

**Hermes format (Nous Research):**
```xml
<tool_call>{"name": "search", "arguments": {"query": "France GDP"}}</tool_call>
```

**Model Context Protocol (MCP) — Anthropic, 2024-2025:**
- Open standard for agent ↔ tool connectivity
- JSON-RPC 2.0 based
- Servers expose tools/resources, clients connect agents
- Adopted by Cursor, Zed, Sourcegraph, etc.
- "The USB-C of agent tools"

**Google's A2A (Agent-to-Agent) Protocol:**
- Complements MCP — handles agent-to-agent communication across vendors
- Covers agent discovery, delegation, and cross-organizational task handoff

## 2.5 Planning Techniques

**Chain-of-Thought (CoT)** — Wei et al. 2022:
- Linear reasoning: step by step toward the answer
- Zero-shot trigger: "Let's think step by step"
- Few-shot: provide examples with reasoning chains

**Tree of Thoughts (ToT)** — Yao et al. 2023:
- Non-linear: explore multiple reasoning paths as a tree
- BFS or DFS to navigate branches
- Evaluate partial solutions, backtrack when stuck
- Excels at tasks requiring exploration (puzzles, creative problems)

**Graph of Thoughts:**
- Arbitrary graph structure (paths can merge, not just branch)
- More expressive than trees

**ReWOO (Reasoning Without Observation):**
- Plan ALL steps upfront, then execute them
- More efficient (fewer LLM calls) but less adaptive to unexpected results

## 2.6 Memory Systems

**Working Memory / Short-Term:**
- The context window itself (4K to 200K+ tokens)
- Contains current conversation, recent tool results
- Hard limit → requires management

**Long-Term Memory:**
- Vector databases (semantic similarity search) → RAG
- Key-value stores (structured facts)
- Graph databases (relationships between entities)

**Memory Types:**
- **Episodic:** Past experiences and their outcomes (what happened last time I tried X?)
- **Semantic:** Facts and knowledge (user prefers dark mode)
- **Procedural:** Learned skills and workflows (how to deploy to production)

**Notable implementations:**
- **MemGPT (2023):** Virtual memory paging — agent manages what's in context vs external storage, like an OS managing RAM
- **Mem0:** Production memory layer with hybrid vector + graph + key-value storage. Auto-extracts memories from conversations.

**Hermes Agent's approach:** Persistent memory tool for user preferences and environment facts, session search for recalling past conversations, skills system for procedural memory.

## 2.7 Multi-Agent Systems

**Architectures:**
- **Cooperative:** Agents work on subtasks toward a shared goal
- **Debate/Adversarial:** Agents argue to refine answers (improves accuracy)
- **Hierarchical:** Manager delegates to specialists
- **Pipeline:** Sequential handoff between agents
- **Swarm:** Peer-to-peer, decentralized

**Example — ChatDev:** Agents role-play as CEO, CTO, programmer, tester to collaboratively write software. Communication through structured dialogues.

## 2.8 Agent Frameworks (2025)

**LangGraph (LangChain):**
- Graph-based agent workflows (nodes = actions, edges = transitions)
- Supports cycles, persistence, human-in-the-loop
- Most popular framework ecosystem. LangSmith for observability.

**CrewAI:**
- Role-based multi-agent collaboration
- Agents have roles, goals, and backstories
- Sequential and hierarchical processes. 20k+ stars.

**AutoGen / AG2 (Microsoft):**
- Event-driven, distributed multi-agent systems
- Group chat managers, nested conversations
- Code execution sandboxing built-in

**OpenAI Agents SDK (March 2025):**
- Lightweight, MIT license
- Core: Agents + Handoffs (transfer) + Guardrails (validation)
- Built-in tracing. Auto agent loop execution.

**Hermes Agent (Nous Research):**
- Full-featured agent harness with CLI + messaging integrations
- Terminal execution, web search, file management, code execution, delegation
- Persistent memory, skills system, scheduled tasks
- Works with any OpenAI-compatible API

## 2.9 Agent Benchmarks — Where We Stand

**SWE-bench (Software Engineering):**
- Real GitHub issues: find and fix bugs in actual repositories
- SWE-bench Verified (500 problems): top agents ~49-50%
- Tests: repo navigation, code editing, test running, understanding large codebases

**GAIA (General AI Assistants):**
- Multi-step real-world tasks requiring web, files, tools
- Level 1: 60-75%, Level 2: 40-55%, Level 3: 10-30%
- Level 3 tasks require long reasoning chains with many tool interactions

**WebArena:**
- Real web tasks on self-hosted websites (shopping, forums, GitLab)
- Best agents: ~35-45%
- Notoriously difficult — real web UIs are messy

**Bottom line:** Agents are good at well-defined, tool-rich tasks (coding, research). They struggle with long-horizon, ambiguous tasks requiring common sense and error recovery.

## 2.10 Agentic Coding — The Killer App

**Cursor:** VS Code fork with AI agent mode. Multi-file editing, codebase-aware. 2M+ users.

**Codex CLI (OpenAI, 2025):** Terminal-based coding agent. Open-source. Three modes: suggest / auto-approve / safe. Uses o3/o4-mini.

**Claude Code (Anthropic, 2025):** Terminal-based. Full codebase understanding via indexing. Multi-file editing, git operations, PR creation.

These are the first agent systems achieving genuine daily utility for professionals.

---

# PART 3: RL FOR AGENTS — WHERE IT ALL COMES TOGETHER

## 3.1 The Core Idea

Standard RL for LLMs (RLHF, DPO) optimizes for single-turn response quality. **RL for agents** optimizes for multi-step task completion in environments.

The shift:
```
RLHF:  prompt → single response → human preference score
RLEF:  prompt → [action₁ → observation₁ → action₂ → observation₂ → ...] → task outcome
```

**Actions aren't just text generation — they include:**
- Tool calls (web search, code execution, file operations)
- Planning decisions (which subgoal next?)
- Memory operations (what to remember/retrieve)
- Communication (asking for clarification, delegating)

## 3.2 RL from Environment Feedback (RLEF)

The key innovation: use *environment interactions* as the reward signal instead of human preferences.

**RLEF for Code Agents (arxiv 2410.02089):**
```
Agent generates code → Code executes → Tests pass/fail → Reward = pass rate
```

**RLEF for Web Agents:**
```
Agent navigates website → Performs task → Task succeeds/fails → Reward = completion
```

**Why RLEF > RLHF for agents:**
- RLHF: reward = learned model of subjective preferences (can be hacked)
- RLEF: reward = objective environment outcome (grounded in reality)
- RLEF scales infinitely — no human annotators needed
- RLEF is naturally suited to agentic tasks where success is measurable

## 3.3 How OpenAI Trains o3/o4-mini for Agentic Tool Use

The most sophisticated RL-for-agents system deployed at scale (as of 2025).

**Architecture:** Tool use is integrated directly into the RL training loop. The model's chain-of-thought can include:
- Natural language reasoning
- Python code generation and execution
- Web search queries
- File analysis

All optimized end-to-end via RL with task completion rewards.

**What this means:** The model doesn't follow hard-coded rules about when to use tools. It *discovers* effective tool use strategies through trial and error during RL training.

**Example o3 reasoning trace (conceptual):**
```
Thought: I need to analyze this CSV file. Let me write Python code.
[Invokes code interpreter]
Code: import pandas as pd; df = pd.read_csv('data.csv'); print(df.describe())
Result: [statistics output]
Thought: The mean is unusually high. Let me check for outliers.
[Invokes code interpreter]
Code: outliers = df[df['value'] > df['value'].mean() + 3*df['value'].std()]; print(outliers)
Result: [outlier rows]
Thought: Found 3 outliers. Let me search if this pattern is expected in this domain.
[Invokes web search]
...
```

The key: this entire reasoning-action flow is optimized by RL. The model learned that checking for outliers and searching for domain context leads to better task completion.

## 3.4 DeepSeek-R1's Training Pipeline (The Open Blueprint)

The most detailed publicly documented RL training pipeline for reasoning.

**Stage 1: R1-Zero (pure RL experiment)**
- Start from base model (no SFT)
- Train with GRPO using only: accuracy rewards (auto-verified) + format rewards (<think> tags)
- Result: model spontaneously develops chain-of-thought reasoning
- Emergent behaviors: self-verification, reflection, "aha moments" (model reconsiders and corrects)
- Problems: poor formatting, language mixing, repetition

**Stage 2: Full R1 Pipeline**
1. Cold-start SFT: Fine-tune on thousands of long-CoT examples for readability
2. Reasoning RL: GRPO with rule-based rewards on math, code, logic
3. Rejection sampling: Use RL model to generate high-quality SFT data
4. All-scenario RL: Final GRPO for helpfulness and safety across all domains

**GRPO details:**
- Group size G (number of outputs sampled per prompt)
- Advantage = (reward - group_mean) / group_std
- Same advantage applied to ALL tokens in the response
- KL penalty: direct divergence from reference policy
- No critic model → ~50% memory savings vs PPO

## 3.5 Nous Research Atropos — Open RL Infrastructure

Atropos democratizes RL training for LLM agents. Open-source.

**Server-client architecture:**
```
┌────────────────────────────────┐
│        Training Client          │
│  (GRPO/PPO policy updates)     │
│  - Rollout generation          │
│  - Advantage computation       │
│  - Gradient updates            │
└──────────┬─────────────────────┘
           │ API calls
           │
    ┌──────┴──────┬──────────┬──────────┐
    │ Environment │ Environ. │ Environ. │
    │ Server 1    │ Server 2 │ Server 3 │
    │ (Code exec) │ (Math)   │ (Tools)  │
    │ reset()     │ reset()  │ reset()  │
    │ step()      │ step()   │ step()   │
    │ reward()    │ reward() │ reward() │
    └─────────────┴──────────┴──────────┘
```

**Environment interface:**
- `reset()` → initial observation
- `step(action)` → next observation + reward
- `reward()` → custom reward function

**Community environments:** Code execution (test cases), math (verifiable answers), web navigation, tool use scenarios, text-based games.

**Why this matters:** Anyone can define a custom environment and train an LLM with RL on their specific tasks. You define what "success" looks like; Atropos handles the RL mechanics.

## 3.6 Process Supervision for Agents

Standard outcome rewards only tell you if the final result was right. Process supervision rewards each intermediate step.

**For math (OpenAI's PRM800K):** Each reasoning step gets a correctness label. PRMs trained on this data can guide search at inference time.

**For agents, process rewards need to evaluate:**
- Was this tool call appropriate here?
- Was the tool query well-formulated?
- Was the tool result interpreted correctly?
- Was this planning decision reasonable?

**Challenge:** Labeling intermediate agent steps is much harder than labeling math steps. Correctness of agentic actions is often ambiguous (was this web search query *wrong*, or just suboptimal?).

**Emerging approach:** Use ORMs (outcome reward models) to derive process-level signals automatically. Train on outcome labels, use the model's step-level scores as process rewards. Avoids expensive step-level annotation.

## 3.7 MCTS for Agent Planning

Monte Carlo Tree Search treats agent decision-making as a search problem.

**Agent Q (arxiv 2408.07199) — the standout paper:**
- MCTS explores web interaction trajectories during training
- Model self-critiques trajectory quality
- DPO training on preference pairs from MCTS rollouts
- **Result: 340% improvement** on real-world web booking tasks

**How MCTS works for LLM agents:**
```
1. SELECTION:   Pick which action/reasoning path to explore (UCB balances explore/exploit)
2. EXPANSION:   Generate next step(s) using the LLM
3. SIMULATION:  Complete the trajectory (rollout to task completion)
4. BACKPROP:    Update value estimates based on outcome
```

**The LLM serves dual roles:**
- **Policy prior:** Which actions are worth trying? (reduces branching factor)
- **Value estimator:** How promising is this partial trajectory?

**rStar (2408.06195):** Two small LLMs doing mutual MCTS reasoning — one generates steps, one discriminates. Achieves strong reasoning without fine-tuning.

**AlphaProof (DeepMind):** MCTS + language model for formal mathematical reasoning at IMO competition level.

## 3.8 Test-Time Compute Scaling

Instead of training bigger models, allocate more compute at inference time.

**Key paper: "Scaling LLM Test-Time Compute Optimally" (DeepMind, 2408.03314):**
- Compute-optimal strategies depend on problem difficulty
- Easy problems: minimal extra compute needed
- Hard problems: search with PRMs is most effective

**Methods (from simple to complex):**
1. **Majority voting:** Generate N responses, take the most common answer
2. **Best-of-N:** Generate N responses, pick highest-scored by reward model
3. **Sequential revision:** Generate → evaluate → revise → repeat
4. **Beam search:** Maintain top-K partial solutions, expand at each step
5. **MCTS:** Full tree search with backpropagation

**s1 (Simple Test-Time Scaling):** Just let the model think longer (more tokens). Surprisingly effective.

**Connection to RL:** This is essentially "RL at inference time" — the model explores and exploits using learned value estimates, doing planning without updating weights.

## 3.9 Self-Play for Agent Training

**SPIN (Self-Play Fine-Tuning):** Current model vs previous version. Learns to distinguish its outputs from human data. Converges when the model can no longer tell the difference.

**SPPO (Self-Play Preference Optimization):** Iterative self-play for alignment without a fixed reward model.

**Multi-agent self-play:** Agents improve by interacting with copies of themselves in competitive (debate, negotiation) and cooperative (collaborative problem-solving) settings.

**Key benefit:** Infinitely scalable training signal. Difficulty auto-scales with agent capability.

## 3.10 Reward Design for Agentic Tasks

The hardest part of RL for agents: defining what "good" looks like.

**Reward types:**
- **Outcome rewards:** Task completed? (sparse but objective)
- **Progress rewards:** Getting closer to the goal? (denser but requires shaping)
- **Format rewards:** Proper tool call syntax? Reasoning structure? (auxiliary signal)
- **Efficiency rewards:** Did it in fewer steps? (prevents meandering)
- **Safety rewards:** Avoided dangerous actions? (critical for deployment)

**Best practices (2025 consensus):**
1. Use verifiable rewards where possible (code execution, math verification)
2. Combine outcome rewards with lightweight process supervision
3. Start with dense rewards, gradually sparsify as training progresses
4. Monitor for reward hacking with held-out evaluation
5. GRPO-style group comparison handles reward normalization automatically

## 3.11 WebRL — RL Training for Web Agents (2024)

**Paper: arxiv 2411.02337**

The most complete system for RL-training web navigation agents.

**Key innovations:**
- **Self-evolving curriculum:** Automatically adjusts task difficulty based on agent performance
- **Outcome-supervised reward model:** Trained on successful/failed trajectories
- **Online RL with KL constraints:** Prevents catastrophic forgetting during adaptation
- Achieves state-of-the-art on WebArena
- Trains on Llama-3.1 models

**Why it matters:** Shows that online RL with curriculum learning dramatically outperforms offline approaches for environment-grounded agents.

## 3.12 Verifiable Rewards — The Foundation

The entire RL-for-agents paradigm rests on being able to automatically verify outcomes.

**Where it works well:**
- Code → execute and check test cases
- Math → compare answers to ground truth
- Structured output → schema validation
- Web tasks → check if desired state was reached
- Games → win/lose/score

**Where it struggles:**
- Creative writing → no objective measure of quality
- Open-ended conversation → subjective preferences
- Nuanced reasoning → partial credit is hard to define
- Real-world actions → consequences are delayed/unclear

**This is why math and code dominate RL training for reasoning.** They have the cleanest verifiable reward signals. The open challenge is extending RL to domains without easy verification.

---

# PART 4: THE BIG PICTURE — WHERE THIS IS ALL GOING

## 4.1 The Emerging Training Stack

```
1. Pretraining     → Predict next token (internet-scale data)
2. SFT             → Follow instructions (curated demonstrations)
3. RL Alignment    → Match human preferences (RLHF/DPO/GRPO)
4. RL for Reasoning → Develop chain-of-thought (verifiable rewards, GRPO)
5. RL for Agency   → Learn tool use, planning (environment feedback)
```

Each layer builds on the previous. The frontier is layer 5 — training models that can act in the world.

## 4.2 The Emerging Inference Stack

```
1. Basic inference    → Single forward pass, greedy decoding
2. Chain-of-thought   → Extended reasoning before answering
3. Tool-augmented     → Invoke tools within reasoning
4. Search-augmented   → MCTS/best-of-N/beam search over reasoning paths
5. Adaptive compute   → Scale inference time based on problem difficulty
```

o3-pro and Gemini Deep Think live at layers 4-5.

## 4.3 Open Problems

1. **Reward design for open-ended tasks** — How do you do RL when there's no right answer?
2. **Safety in agentic RL** — RL-trained agents might discover effective but dangerous strategies
3. **Sample efficiency** — RL still requires many rollouts (expensive for large models)
4. **Generalization** — Do RL-trained behaviors transfer to new environments?
5. **Long-horizon credit assignment** — Which of 100 tool calls caused the failure?
6. **Multi-agent RL** — Training teams of agents to collaborate
7. **Continuous learning** — Can agents keep improving from deployment experience?

## 4.4 Key Papers to Read

If you read 5 papers, read these:
1. **DeepSeek-R1** (2501.12948) — The RL training pipeline that changed everything
2. **Let's Verify Step by Step** (2305.20050) — Process vs outcome supervision
3. **Scaling Test-Time Compute** (2408.03314) — Compute-optimal inference
4. **Agent Q** (2408.07199) — MCTS + RL for web agents
5. **Nous Research GRPO blog** (nousresearch.com/grpo-the-rl-algorithm-behind-deepseek-r1) — Clearest GRPO explanation

## 4.5 How You'd Use RL for Your Own Agents

Practical path using available tools:

1. **Pick your task domain** — something with verifiable rewards (coding, data processing, API workflows)
2. **Define your environment** — what are the actions (tool calls), observations (results), and rewards (task success)?
3. **Use Atropos** — Nous Research's open infrastructure handles the RL mechanics
4. **Start with GRPO** — most efficient, no critic model needed
5. **Bootstrap with SFT** — train on demonstrations first, then apply RL
6. **Iterate** — rejection sampling from RL model → new SFT data → more RL

**The minimum viable RL-for-agents pipeline:**
```
1. Base model (Llama 3.x, Qwen, etc.)
2. SFT on task demonstrations
3. Define environment with reward function
4. GRPO training via Atropos
5. Evaluate on held-out tasks
6. Ship it
```

---

*Compiled from research across 30+ papers, blog posts, and technical documents. Sources include arXiv, Nous Research, OpenAI, Anthropic, DeepSeek, Google DeepMind, and academic surveys from 2024-2025.*
