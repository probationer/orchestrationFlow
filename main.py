import asyncio
from enum import Enum
from typing import Dict, Any

from utils import QUEUES
from node import Node, TwitteNode, DecisionNode, Formatter

class NODE_TYPE(Enum):
    TWITTE = 'twitteNode'
    FOMATTER = 'formatterNode'
    DECISION = 'decisionNode'
    ROOT = 'root'


def parseJsonToFlow(jsonData: Dict[str, Any]) -> Node:

    '''
        Parse json flow to node structure 
    '''

    type = jsonData.get('type', None)
    subType = jsonData.get('subType', None)
    id = jsonData.get('id', None)
    children = [parseJsonToFlow(child) for child in jsonData.get('children', [])]

    node = None
    match type:
        case NODE_TYPE.FOMATTER.value:
            node = Formatter(id, type, subType, children)
        case NODE_TYPE.TWITTE.value:
            node = TwitteNode(id, type, subType, children)
        case NODE_TYPE.DECISION.value:
            node = DecisionNode(id, type, subType, children)
        case NODE_TYPE.ROOT.value:
            node = Node(id, type, subType, children)
        case _ :
            raise ValueError('Unknown node type')
    return node


async def startOrchestration(node: Node, parentOutput):
    '''
        Orchestration flow start
        node: current node
        parentOutput: output of node parent
    '''
    response = await node.processor(parentOutput)
    if (len(node.children) > 0):
        childNode = node.children
        for child in childNode: 
            await startOrchestration(child, response)

async def printQueue(queue: asyncio.Queue, type):
    ''' 
        Std out queue data
    '''
    while True:
        item = await queue.get()
        print(f"{type} consumed ===> : {item}")
        if item == None:
            break

async def main():

    # Load JSON data
    jsonData = {
        "id":"1",
        "type": "root",
        "children": [
            {
                "id":"2",
                "type": "twitteNode",
                "subType": "fetch",
                "children": [
                    {
                        "id":"3",
                        "type": "formatterNode",
                        "subType": "unparse",
                        "children": [
                            {
                                "id":"4",
                                "type": "decisionNode",
                                "subType": "",
                                "children": [
                                    {
                                        "id":"5",
                                        "type": "twitteNode",
                                        "subType": "fetch",
                                        "children": [
                                            {
                                                "id":"6",
                                                "type": "formatterNode",
                                                "subType": "unparse",
                                                "children": [
                                                    {
                                                        "id":"7",
                                                        "type": "decisionNode",
                                                        "subType": "",
                                                        "children": []
                                                    }
                                                ]
                                            }
                                        ]
                                    },
                                    {
                                        "id":"8",
                                        "type": "twitteNode",
                                        "subType": "post",
                                        "children": [{
                                            "id":"9",
                                            "type": "formatterNode",
                                            "subType": "unparse",
                                            "children": [
                                                {
                                                    "id":"12",
                                                    "type": "decisionNode",
                                                    "subType": "",
                                                    "children": []
                                                }
                                            ]
                                        }]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "id":"10",
                "type": "twitteNode",
                "subType": "post",
                "children": [
                    {
                        "id":"11",
                        "type": "formatterNode",
                        "subType": "parse",
                        "children": []
                    }
                ]
                
            }
        ]
    }

    # Parse the JSON to create the node structure
    rootNode = parseJsonToFlow(jsonData)
    print(' ---- Node Object created ---- ')

    # Start the flow with some initial data
    await startOrchestration(rootNode, '')

    # adding None at the end of queue
    await QUEUES["positive_queue"].put(None)
    await QUEUES["negative_queue"].put(None)
    await QUEUES["neutral_queue"].put(None)

    print('------------x--------x--------------')
    await printQueue(QUEUES["positive_queue"], 'positive')
    await printQueue(QUEUES["negative_queue"], 'negative')
    await printQueue(QUEUES["neutral_queue"], 'neutral')


asyncio.run(main())