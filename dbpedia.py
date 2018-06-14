from SPARQLWrapper import SPARQLWrapper, JSON
#from surf import Store, Session, ns

"""
class DBPedia(object):
    
    def __init__(self):
        self.store = Store(reader='sparql_protocol', endpoint='http://dbpedia.org/sparql', default_graph='http://dbpedia.org')
        self.session = Session(self.store, [])
        self.session.enable_logging = True
        ns.register(db='http://dbpedia.org/resource')
        ns.register(dbonto='http://dbpedia.org/ontology')

    def get_type(self, name):
        resource = self.session.get_resource(name)
        print(resource)
"""
class DBPedia(object):

    def __init__(self):
        self.sparql_endpoint = "http://dbpedia.org/sparql"
        self.template = """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX rfd: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            SELECT ?type
            WHERE { <http://dbpedia.org/resource/%s> rdf:type ?type }
        """

    def get_types(self, name, filter='dbpedia.org/ontology/'):
        """Gets the rfd:type list with the selected filter.
        The filter is a partial string that must be contained in the URI"""
        sparql = SPARQLWrapper(self.sparql_endpoint)
        query = self.template % name
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        types = []
        for result in results["results"]["bindings"]:
            uri = result['type']['value']
            if filter in uri:
                # take the last part of URI
                last_part = uri.split('/')[-1].split('#')[-1]
                types.append(last_part)
        print(name, types)
        return types

    def get_types_recurrent(self, name):
        # TODO take iteratively the types of the types
        pass

        

def main():
    dbpedia = DBPedia()
    dbpedia.get_types('Book')
    dbpedia.get_types('Mug')
    dbpedia.get_types('Coffee')
    dbpedia.get_types('Kitchen')
    dbpedia.get_types('Building')

if __name__ == '__main__':
    main()
