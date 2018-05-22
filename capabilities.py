from concepts import Context

context = Context.fromfile('table_b.csv', frmat='csv')
lattice = context.lattice
#lattice.graphviz('normal.png', '.', False, True)

true_capabilities = ['perception', 'navigation', 'learning', 'verbal_interaction', 'information_management']
true_capabilities = ['information_management', 'navigation', 'moving', 'perception', 'learning']
#true_capabilities = ['perception']

# upside down
context_inv = Context(*context.definition().inverted())
lattice_inv = context_inv.lattice

all_properties = context.properties
all_objects = context.objects

def get_candidates(frame_name):
    anticoncept = lattice_inv[frame_name,]
    all_properties = context.properties
    #print(anticoncept)
    to_consider = anticoncept.lower_neighbors
    results = set()
    while to_consider:
        #print(to_consider)
        print('looping')
        new_to_consider = []
        for candidate_link in to_consider:
            simpler_actions, not_requires = candidate_link
            #print(simpler_actions, not_requires)
            requires = [p for p in all_properties if p not in not_requires]
            if all(elem in true_capabilities for elem in requires):
                print('can do', simpler_actions)
                results.update(simpler_actions)
            new_to_consider.extend(candidate_link.lower_neighbors)
        
        to_consider = [candidate for candidate in new_to_consider if candidate is not lattice_inv.infimum]
        
    print(results)

def better(frame_name):
    # what are the abilities needed
    wanted = context.intension([frame_name])
    # its lattice representation
    anticoncept = lattice_inv[frame_name,]
    # what cannot be provided, but was asked for
    cannot_provide = [cap for cap in wanted if cap not in true_capabilities]
    print('things required that cannot be provided: ', cannot_provide)
    if cannot_provide or True:
        # its lattice representation
        boh = lattice_inv[cannot_provide]
        # put together the constraints: we want things that:
        # - do not require more (down from anticoncept)
        # - do not require the things that we cannot provide (down from boh)
        something = anticoncept.meet(boh)
        print('legend: {set of things that can be done} <-> [list of abilities not required by all of them] <=> the upper neighbors (nearest) ')
        print(something)
    else:
        print('I can fulfill', frame_name)

def is_it_possible(frame_name):
    # TODO delete, this is not working
    # what are the abilities needed
    wanted = context.intension([frame_name])
    # its lattice representation
    concept = lattice[frame_name,]
    # what cannot be provided, but was asked for
    can_provide = [cap for cap in wanted if cap in true_capabilities]
    print('things required that can be provided: ', can_provide)
    # its lattice representation
    boh = lattice[can_provide]
    # put together the constraints: we want things that:
    # - do not require more (down from anticoncept)
    # - do not require the things that we cannot provide (down from boh)
    something = concept.join(boh)
    # string representation is {extent} <-> [intent] <=> objects
    print('legend: {set of things that can be done} <-> [list of abilities not required by all of them] <=> the upper neighbors (nearest) ')
    print(something)


# slower, stupid
#get_candidates('Bringing')
# faster, cool idea
better('Bringing')
# does not work because an upper group contains also the members of the descendants.
# Going up to remove some required capabilities, we have in nodes elements that also have other requirements because are labeled down.
# Instead working on the upside-down, the navigation is more natural because going down means to add things that are not required. So meeting with the required things that cannot be provided provides the answers
#is_it_possible('Bringing')
#get_candidates('Perception_active')
better('Perception_active')
#for frame in all_objects:
#    better(frame)