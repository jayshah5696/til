# CREWAI
CrewAi is a llm agent orchatration tool
it provides a certain set of core concepts that are used to build and run AI agents

[documentation](https://docs.crewai.com/)
[doc_gpt](https://chatgpt.com/g/g-qqTuUWsBY-crewai-assistant)
## EXAMPLES
- [alejandaro](https://alejandro-ao.com/crew-ai-crash-course-step-by-step/)
- [crewai_example_repo](https://github.com/crewAIInc/crewAI-examples/tree/main/CrewAI-LangGraph)
## Installation
```bash
pip install crewai
pip install crewai[tools]
```
## Core Concepts
- Agents
- Tasks
- Tools
- Processes
- Crews
- Training
- Memory
- Planning

## TASKS
- tasks are to do list
- for given inputs tasks are exectued by agents
- Properties 
  - description : Kind of prompt for completing of task, you can provide {curly_bracket_input}
  - output: output of the task (you can also add pydentic model)
  - agent: agent that will execute the task
  - async_execution: allow task to run in parallel
  - context: context of the task
- notes:
  - avoid defining vague tasks, break them into smaller tasks
  - iterate multiple time to get it right

## AGENTS
- Agents are the worker that execute the tasks
- mostly are React agents coded in langchain (Thought, Action, Action Input, Observation)
- properties:
    - goal: goal of the agent (what is the agent trying to achieve)
    - backstory: kind of system prompt
    - tools: List of tools
    - verbose: print the output of the agent
    - llm: ask for llm otherwise uses openai

## TOOLS
- Tools are the helper functions that are used by agents to complete the tasks
- properties:
    - description: kind of prompt for the agent to use the tool
    - agent: agent that will use the tool
    - expected_output: expected output of the tool you can also add pydentic model
    - context: context of the tool
    - async_execution: allow tool to run in parallel


## PROCESSES
- Sequential: run the tasks in sequence
- Hierarchical: run the tasks in hierarchy (any task can run by master agent)

## CREWS
- Crews are the group of agents that work together to achieve a goal
- you run this with crew.kickoff()
- final output woudl be the result of the last task
- The way crews of agent work is 
- ```
You are a {task.agent.role}. {task.agent.backstory}. Your goal is {task.agent.goal}. 
You have the following tools at your disposal: {task.agent.tools}. 
Your task is to {task.description}.
```
- also crew add 2 more tasks by default (delegate work to corwroker and ask a question to corwroker),
- you need to manually disable it `allow_delegation=False`




### inputs and outputs
- inputs and output needs to be defined properly for given crew
- outuput would be last task output