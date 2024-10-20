### Event-Driven Node Processor
#### Scenario:
You are tasked with building a Python-based system to simulate the processing of an orchestration flow. The flow consists of nodes, each of which has custom fields and children nodes. Each node processes its input asynchronously, decides what action to take, and passes the output to its child nodes. The system will process each node asynchronously and place the results in appropriate queues.

#### Objective:
Build a Python program that processes the provided JSON (see below). The program should:

- Traverse the JSON node-by-node starting from the root.
- Process each node asynchronously.
- Based on the type of node and its output, determine which queue the processed message should go to (for example: queue_a, queue_b, etc.).
- Implement a decision node where different conditions dictate which child node to process next.
- Simulate asynchronous processing using Python’s asyncio library.

#### Requirements:
- Implement node processing asynchronously.
- Process each node based on its type (e.g., twitterNode, someNode, decisionNode, etc.).
    - twitterNode: Simulates fetching or posting tweets.
    - someNode: Processes intermediate steps with simple input/output handling.
    - decisionNode: Evaluates conditions and routes output to appropriate child nodes.
- Once a node is processed, its output should be passed to its child nodes for further processing.
- Use queues (queue_a, queue_b, etc.) to store processed results from nodes.
- Ensure the correct queue is selected based on the output of the decisionNode.




