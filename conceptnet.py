import requests
import time

import concurrent.futures


class ConceptNet(object):

    def __init__(self):
        """Instantiates the ConceptNet wrapper"""
        self.baseUrl = 'http://api.conceptnet.io/'

    def getId(self, text, language='en'):
        """Provides the ID of a text, that can be used to interrogate ConceptNet.
        If the entity is not in conceptnet, returns None

        text: the natural language text
        language: the language of the text, default 'en'

        returns: the ID of the concept searched or None
        """
        url = '{}/uri'.format(self.baseUrl)
        params = {'language': language, 'text': text}
        response = requests.get(url, params=params).json()
        result = response['@id']
        entity = self.getEntity(result)
        if entity:
            return result
        else:
            return None

    def getEntity(self, id, offset=0, limit=20):
        """Provides the entity given its Id, None if it does not exist"""
        url = '{}/{}'.format(self.baseUrl, id)
        params = {'offset': offset, 'limit': limit}
        response = requests.get(url, params=params).json()

        if 'error' in response:
            print(response['error']['details'])
            return None
        else:
            return response

    def relationsBetweenSingle(self, id_a, id_b):
        """Returns the relations (only the '@id') from id_a to id_b, if any"""
        url = '{}/query'.format(self.baseUrl)
        params = {'start': id_a, 'end': id_b}
        response = requests.get(url, params=params).json()

        return [edge['@id'] for edge in response['edges']]

    def relationsBetweenGroups(self, group_a, group_b):
        """Returns all the relations between group_a and group_b, flattened"""
        results = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for a in group_a:
                for b in group_b:
                    futures.append(executor.submit(self.relationsBetweenSingle, a, b))

            for f in concurrent.futures.as_completed(futures):
                results += f.result()

        return set(results)

    def getSuperEdgesSingle(self, id):
        """Returns the Edges in the (id, IsA, ?) relations"""
        url = '{}/query'.format(self.baseUrl)
        params = {'start': id, 'rel': '/r/IsA'}
        response = requests.get(url, params=params).json()
        return [edge['end']['@id'] for edge in response['edges']]

    def getSuperEdgesGroup(self, group_ids):
        """Same as Single, but this time with a group of ids"""
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for id in group_ids:
                futures.append(executor.submit(self.getSuperEdgesSingle, id))
            for f in concurrent.futures.as_completed(futures):
                results += f.result()

        return set(results)

    def classifyRecurrent(self, group_target, group_a, group_b, max_recursions=2):
        """Given a group of ids group_target to be classified against two classes (defined by two groups of ids group_a and group_b),
        this method, for the maximum number of steps max_recursions will try to:
        - see if the group_target has more relations with group_a or group_b. If the counts are the same, then
        - proceeds to all the super edges (following IsA) of group_target and do again the same

        Returns (compare fashion):
        - -1 if the group target has more relations with group_a
        - +1 if the group target has more relations with group_b
        - 0 if after max_step the scores are still the same
        """
        print(max_recursions)
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            a_future = executor.submit(self.relationsBetweenGroups, group_target, group_a)
            b_future = executor.submit(self.relationsBetweenGroups, group_target, group_b)

            now_relations_a = a_future.result()
            now_relations_b = b_future.result()
        #now_relations_a = self.relationsBetweenGroups(group_target, group_a)
        #now_relations_b = self.relationsBetweenGroups(group_target, group_b)

        if len(now_relations_a) < len(now_relations_b):
            print('reason', now_relations_b)
            return -1
        elif len(now_relations_a) > len(now_relations_b):
            print('reason', now_relations_a)
            return 1
        else:
            if max_recursions:
                super_edges = self.getSuperEdgesGroup(group_target)
                print('recurring on', super_edges)
                return self.classifyRecurrent(super_edges, group_a, group_b, max_recursions - 1)
            else:
                return 0
