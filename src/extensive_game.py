

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
            print("Children: {}".format(node.children))
        elif not only_leaves:
            print(action_list)
            print("Children: {}".format(node.children))
        for action, child in node.children.items():
            ExtensiveGame.print_tree_recursive(child, action_list + [action],
            only_leaves)

    def print_tree(self, only_leaves=False):
        """ Prints out a list of all nodes in the tree by the list of actions
        needed to get to each node from the root.
        """
        ExtensiveGame.print_tree_recursive(self.root, [], only_leaves)
