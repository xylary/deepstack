
class ExtensiveGameNode:
    """ A class for a game node in an extensive form game.
    """
    def __init__(self, player):
        # Which player is to play in the node. Use -1 for terminal, 0 for
        # chance, 1 for player 1, 2 for player 2.
        self.player = player

        # A dictionary of children for the node. Keys are the actions in the
        # node, and values are ExtensiveGameNode objects resulting from taking
        # the action in this node.
        self.children = {}

        # Who can see the actions in this node.
        self.hidden_from = []

        # Utility of the node to each player (as a dictionary). Only relevant
        # for terminal nodes.
        self.utility = {}

        # If the node is a chance node, then store the chance probs. This is a
        # dictionary with keys the actions and probs the probability of choosing
        # this action.
        self.chance_probs = {}

class ExtensiveGame:
    
    def __init__(self, root):
        self.root = root

    @staticmethod
    def print_tree_recursive(node, action_list, only_leaves):
        """ Prints out a list of all nodes in the tree rooted at 'node'.
        """
        if only_leaves and len(node.children) == 0:
            print(action_list, node.utility)
        elif not only_leaves:
            print(action_list)
        for action, child in node.children.items():
            ExtensiveGame.print_tree_recursive(child, action_list + [action],
            only_leaves)

    def print_tree(self, only_leaves=False):
        """ Prints out a list of all nodes in the tree by the list of actions
        needed to get to each node from the root.
        """
        ExtensiveGame.print_tree_recursive(self.root, [], only_leaves)
    
    def build_information_sets(self, player):
        """ Returns a dictionary from nodes to a unique identifier for the
        information set containing the node. This is all for the given player.
        """
        info_set = {}

        # We just recursively walk over the tree using a stack to store the
        # nodes to explore.
        node_stack = [self.root]
        visible_actions_stack = [[]]
        
        # First build the information sets for player 1.
        while len(node_stack) > 0:
            node = node_stack.pop()
            visible_actions = visible_actions_stack.pop()

            # Add the information set for the node, indexed by the
            # visible_actions list, to the information set dictionary. Use a
            # tuple instead of a list so that it is hashable if we want later
            # on.
            info_set[node] = tuple(visible_actions)
            
            for action, child in node.children.items():
                # Add all the children to the node stack and also the visible
                # actions to the action stack. If an action is hidden from the
                # player, then add -1 to signify this.
                node_stack.append(child)
                if player in node.hidden_from:
                    visible_actions_stack.append(visible_actions + [-1])
                else:
                    visible_actions_stack.append(visible_actions + [action])

        return info_set
