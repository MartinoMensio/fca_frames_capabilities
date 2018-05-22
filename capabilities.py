import copy
from concepts import Context
from concepts.lattices import Concept

class LatticeSpecification(object):
    """A wrapper for concepts and lattices, that based on a table (rows=frames, columns=required capabilities) """
    
    def __init__(self, csv_location):
        # the Frame-capability lattice
        self.context = Context.fromfile(csv_location, frmat='csv')
        self.lattice = self.context.lattice
        # the Frame-uncapability lattice
        self.context_inv = Context(*self.context.definition().inverted())
        self.lattice_inv = self.context_inv.lattice
        # the list of all capabilities and frames
        self.capabilities = self.context.properties
        self.frames = self.context.objects

    def visualize(self, inverse=False, **kvargs):
        """Call the lattice visualization. 
        
        inverse=True: creates the Frame-capability visualization
        inverse=False: creates the Frame-uncapability visualization
        kwargs: put there all filename,directory,render,view stuff"""
        if inverse:
            return self.lattice_inv.graphviz(**kvargs)
        else:
            return self.lattice.graphviz(**kvargs)

    def get_frame_recommender(self, true_capabilities):
        """Get the FrameRecommender for the selected true_capabilities.
        
        Params:
        - true_capabilities: an array of strings"""
        return FrameRecommender(self, true_capabilities)

class FrameRecommender(object):
    """A class to recommend Frames, from a Lattice and true capabilities"""

    def __init__(self, lattice_specification, true_capabilities):
        """lattice is an instance of Lattice
        
        true_capabilities is an array of capabilities that are"""
        # the LatticeSpecification that generated this recommender
        self.specification = lattice_specification
        self.true_capabilities = true_capabilities
    
    def can_fulfil(self, frame_name, verbose=False, return_bool_only=True):
        if verbose: print('requested:', frame_name)
        # what are the abilities needed
        wanted_cap = self.specification.context.intension([frame_name])
        # what cannot be provided, but was asked for
        cannot_provide_list = [cap for cap in wanted_cap if cap not in self.true_capabilities]
        if verbose: print('\tthings required that cannot be provided: ', cannot_provide_list)
        can_provide = False if cannot_provide_list else True
        if return_bool_only:
            return can_provide
        else:
            return can_provide, cannot_provide_list

    def get_recommendation(self, frame_name, verbose=False):
        # what are the abilities needed
        wanted_cap = self.specification.context.intension([frame_name])
        # what cannot be provided, but was asked for
        cannot_provide_list = [cap for cap in wanted_cap if cap not in self.true_capabilities]
        
        # the lattice representation of the requested frame
        anticoncept = self.specification.lattice_inv[frame_name,]
        # the lattice representation of the missing capabilities
        other = self.specification.lattice_inv[cannot_provide_list]
        # put together the constraints: we want things that:
        # - do not require more (down from anticoncept) (-->simpler<--)
        # - do not require the things that we cannot provide (down from other) (-->feasible<--)
        result_concept = anticoncept.meet(other)
        if verbose:
            print('nearest',result_concept.objects, 'between', result_concept.extent)
        return Recommendation(result_concept, cannot_provide_list)

class Recommendation(object):
    """A recommendation"""
    def __init__(self, concept, reason_missing):
        self.concept = concept
        self.reason_missing = reason_missing
        self.nearest = concept.objects
        self.possible = concept.extent
