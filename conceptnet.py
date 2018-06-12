import requests

class ConceptNet(object):

    def __init__(self):
        """Instantiates the ConceptNet wrapper"""
        self.baseUrl = 'http://api.conceptnet.io/'
    
    def getId(self, text, language='en'):
        """Provides the ID of a text, that can be used to interrogate ConceptNet. Always returns an ID, also if the resource does not exist, check with getEntity(id)
        
        text: the natural language text
        language: the language of the text, default 'en'

        returns: the ID of the concept searched
        """
        url = '{}/uri'.format(self.baseUrl)
        params = {'language': language, 'text': text}
        response = requests.get(url, params=params).json()

        return response['@id']

    def getEntity(self, id, offset=0, limit=20):
        """Provides the entity given its Id, None if it does not exist"""
        url = '{}/{}'.format(self.baseUrl, id)
        params = {'offset': offset, 'limit': limit}
        response = requests.get(url, params=params).json()

        if 'error' in response:
            print(response['error']['details'])
            return None
        else:
            # or return only the edges?
            return response

    def relationsBetweenSingle(self, id_a, id_b):
        """Returns the relations (only the '@id') from id_a to id_b, if any"""
        url = '{}/query'.format(self.baseUrl)
        params = {'node': id_a, 'other': id_b}
        #print(params)
        response = requests.get(url, params=params).json()

        return [edge['@id'] for edge in response['edges']]

    def relationsBetweenGroups(self, group_a, group_b):
        """Returns all the relations between group_a and group_b, flattened"""
        result = []
        for a in group_a:
            for b in group_b:
                result += self.relationsBetweenSingle(a, b)

        return result

    def getSuperEdges(self, id):
        """Returns the Edges in the (id, IsA, ?) relations"""
        url = '{}/query'.format(self.baseUrl)
        params = {'start': id, 'rel': '/r/IsA'}
        response = requests.get(url, params=params).json()
        return [edge['end']['@id'] for edge in response['edges']]