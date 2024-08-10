# LnagGraph

## Introduction

Stategraph

## 2 main componenets

- Graph
  - Edges
    - Edges connect nodes
    - Starting Edge ( set_entry_point)
    - Normal Edges ( add_edge)
    - Conditional Edges ( Feedback loops)
      - it can be programmtically
      - or agent can be dependent
      - which node it goes to next 
  - Nodes
    - Agents or tools
    - Agents ( take state as input and write to state as output)
    - Components of the graph
- State (StateGraph)
  - Record of activities that happens inside the graph
  - State is updated by nodes
  - State is defined as dict
  - Its persisted throughout the graph run
  - You can add or replace the dict during run time


Begin with a graph.
Identify task requirements.
Map these to a state.
Determine activities to record in the state.
THen compile the graph


# Building SearchAssist

Search Tools - 
- Tavily Search ( 1000/search per month Free)
- DuckDuckGo ( 1000/search per month Free)
- 
