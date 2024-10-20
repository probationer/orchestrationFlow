import html
import html.parser
import random
import asyncio

from utils import askGPT, QUEUES

class Node: 
    def __init__(self, id: str, type: str, subType: str, children: list):
        self.id = id
        self.type = type
        self.subType = subType
        self.children = children

    async def processor(self, parentOutput):
        print(f'Process asyncronsly id: {self.id} type: {self.type} subType: {self.subType}')
        await asyncio.sleep(random.uniform(0.5, 1.0))
        return parentOutput


class TwitteNode(Node):
    '''
        Twitte node fetch and post data according to subtype.
    '''

    async def processor(self, parentData):
        print(f'Twitte Node || id: {self.id} type: {self.type} subType: {self.subType} parentDate: {parentData}')
        if self.subType == 'fetch' or parentData == 'positive': 
            return await self.fetchTwitte()
        elif self.subType == 'post' or parentData == 'negative':
            return await self.postTwitte(parentData)
        else:
            return None

    async def postTwitte(self, sentiment = 'positive', topic = 'current affairs'):
        '''
            Generate twitte for given topic
        '''
        print(f'Posting twitte || id: {self.id} type: {self.type} subType: {self.subType}')
        await asyncio.sleep(random.uniform(2, 4))
        newTwitte = await askGPT(f'Generate a twitte about {topic} with {sentiment} sentiments under 120 characters.')
        return {'text': newTwitte, 'type': 'post'}

    async def fetchTwitte(self):
        '''
            Fetch new messages from twitte
        '''
        print(f'Fetching twitte || id: {self.id} type: {self.type} subType: {self.subType} ')
        await asyncio.sleep(random.uniform(1, 3))
        newTwitte = await askGPT(f'Generate a twitte about current affair under 120 characters.')
        print('fetch twitte : ', newTwitte)
        return {'text': newTwitte, 'type': 'fetch'}


class Formatter(Node):
    '''
        Formatter use the parent output and parse/unparse html data to text for futher process
        Note: parse and unparse should be used. Same function has been used just for demo
    '''
    async def processor(self, parentData):
        print(f'Formatter Node || id: {self.id} type: {self.type} subType: {self.subType} parentData {parentData}')
        if parentData.get('type') == 'fetch':
            return html.unescape(parentData.get('text'))
        elif parentData.get('type') == 'post':
            return html.unescape(parentData.get('text'))
        return parentData


class DecisionNode(Node):
    '''
        Decision node analyze the text and perform sentimental analysis. 
        Then store data to according to the output of the analysis
    '''
    async def processor(self, parentData):
        print(f'Decision Node || id: {self.id} type: {self.type} subType: {self.subType} parentData: {parentData}')
        response = await askGPT(f'Categorize the sentiment of given twitte in "positive", "negative" or "neutral" category. Response in one word.\n Twitte: {parentData}')
        print('Sentiment of twitte: ', response)
        response = response.lower() 
        output = {}
        match response:
            case 'positive':
                await QUEUES['positive_queue'].put(parentData)
                output = {'type': 'twitte', 'subType': 'fetch'}
            case 'negative':
                await QUEUES['negative_queue'].put(parentData)
                output = {'type': 'twitte', 'subType': 'post', 'sentiment': 'positive'}
            case 'neutral':
                await QUEUES['neutral_queue'].put(parentData)
                output = {'type': 'twitte', 'subType': 'fetch', 'sentiment': 'neutral'}
        return output
