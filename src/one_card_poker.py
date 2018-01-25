from extensive_game import ExtensiveGame, ExtensiveGameNode

class OneCardPoker(ExtensiveGame):
    """ This is the game described on 'http://www.cs.cmu.edu/~ggordon/poker/'.
    Rules: each player is privately dealt one card from a deck of 'n_cards'
    cards (without replacement). Currently there is one card for each card
    value. Each player antes 1 chip (a forced initial bet). Player 1 then bets
    either 0 or 1. Player 2 can fold (if player 1 bet 1), match player 1's bet,
    or, if player 1 bet 0, then player 2 can raise by betting 1. In the last
    situation, player 1 then gets a chance to match the bet or fold.
    """

    @staticmethod
    def create_chance_node(cards, player):
        """ Returns a node with one child for each card in 'cards', and
        probability uniform across 'cards'.
        """
        next_player = {1: 2, 2: 1}
        # Create a child node for each possible card
        children = {}
        for card in cards:
            children[card] = ExtensiveGameNode(next_player[player])

        # Create the node
        node = ExtensiveGameNode(player, children=children,
        hidden_from=[next_player[player]], chance_probs={card:
        1.0/float(len(cards)) for card in cards})
            
        return node

    @staticmethod
    def compute_utility(action_list, hole_cards):
        """ Given actions in 'action_list' and hole_cards in 'hole_cards',
        compute the utility for both players at a terminal node.
        """
        # The bets are 1 (for the ante), then the sum of the even actions (for
        # player 1) and the odd actions (for player 2).
        bets = {1: 1, 2: 1}
        for i, action in enumerate(action_list):
            bets[(i%2)+1] += action
        winner = 1 if hole_cards[1] > hole_cards[2] else 2
        loser = 2 if hole_cards[1] > hole_cards[2] else 1
        # The winner wins the amount the loser bet, and the loser loses this
        # amount.
        return {winner: bets[loser], loser: -bets[loser]}


    @staticmethod
    def create_one_card_tree(action_list, cards):
        """ Creates a tree for one card Poker. 'cards' is a list of numbers of
        cards, defining the deck. The numbers should be unique. Initially this
        should be called with 'action_list' being an empty list.
        """
        print("Action list: {}".format(action_list))
        if len(action_list) == 0:
            # We are at the root of the tree, so we create a chance node for
            # player 1.
            root = ExtensiveGameNode(1)
            # This node is hidden from player 2
            root.hidden_from = [2]
            for card in cards:
                # Create a game tree below this node.
                root.children[card] = OneCardPoker.create_one_card_tree([card], cards)
            return ExtensiveGame(root)
        elif len(action_list) == 1:
            # We are at a chance node for player 2, so we create this chance
            # node, including its children.
            node = ExtensiveGameNode(2)
            # This node is hidden from player 1
            node.hidden_from = [1]
            for card in cards:
                # Player 2 can't be dealt the card that player 1 was dealt.
                if card == action_list[0]:
                    continue
                # Otherwise create a child node below
                node.children[card] = OneCardPoker.create_one_card_tree(action_list + [card],
                cards)
            return node
        elif len(action_list) == 2:
            # It's player 1's first turn.
            node = ExtensiveGameNode(1)
            node.children[0] = OneCardPoker.create_one_card_tree(action_list + [0], cards)
            node.children[1] = OneCardPoker.create_one_card_tree(action_list + [1], cards)
            return node
        elif len(action_list) == 3:
            # It's player 2's first turn.
            node = ExtensiveGameNode(2)
            node.children[0] = OneCardPoker.create_one_card_tree(action_list + [0], cards)
            node.children[1] = OneCardPoker.create_one_card_tree(action_list + [1], cards)
            return node
        elif len(action_list) == 4:
            # It's player 1's second turn (if the node isn't terminal).
            if action_list[1] == 0 or action_list[0] == action_list[1]:
                # The second player folded, or called a bet of 0, or called a
                # bet of 1. Thus this node is terminal.
                node = ExtensiveGameNode(-1)
                hole_cards = {1: action_list[0], 2: action_list[1]}
                node.utility = OneCardPoker.compute_utility(action_list,
                hole_cards)
                node.children = {}
                return node
            else:
                # The actions were [0,1], and so player 1 gets another chance to
                # call or fold.
                node = ExtensiveGameNode(1)
                node.children[0] = OneCardPoker.create_one_card_tree(action_list
                + [0], cards)
                node.children[1] = OneCardPoker.create_one_card_tree(action_list
                + [1], cards)
                return node
        elif len(action_list) == 5:
            # It's player 2's second turn (but this actually must be terminal).
            node = ExtensiveGameNode(-1)
            hole_cards = {1: action_list[0], 2: action_list[1]}
            node.utility = OneCardPoker.compute_utility(action_list,
            hole_cards)
            node.children = {}
            return node
        assert False

    @staticmethod
    def create_betting_round(action_list, cards):
        """ Creates a tree that gives the actions for each player in the betting
        round. After the two chance actions have been taken (the first private
        to player 1 and the second private to player 2), the remainder of the
        tree is just a copy of the tree this function returns.
        """
        assert len(action_list) <= 3

        #node.children = {}
        #print("Node children: {}".format(node.children))

        # We update node to be the root of a betting round.
        if len(action_list) == 0:
            node = ExtensiveGameNode(2)
            node.player = 1
            node.children[0] = OneCardPoker.create_betting_round(node.children[0], action_list + [0], cards)
            node.children[1] = ExtensiveGameNode(2)
            OneCardPoker.create_betting_round(node.children[1], action_list + [1], cards)
        elif len(action_list) == 1:
            # If there has been 1 action so far, then it's 2's turn. Whatever
            # 1's action was, we can check or bet
            node.children[0] = ExtensiveGameNode(1)
            OneCardPoker.create_betting_round(node.children[0], action_list + [0], cards)
            node.children[1] = ExtensiveGameNode(1)
            OneCardPoker.create_betting_round(node.children[1], action_list + [1], cards)
        elif len(action_list) == 2:
            # 2 actions implies it's 1's turn.
            if action_list[1] == 0 or action_list[0] == action_list[1]:
                # The second player folded, or called a 0-bet, or called a
                # 1-bet. Thus this is a terminal node.
                node.player = -1
                # We now update utility:
                node.utility = OneCardPoker.compute_utility(action_list,
                cards)
                #node.children = {}
            else:
                # The actions were [0,1], and so player 1 gets another chance to
                # call or fold.
                node.children[0] = ExtensiveGameNode(-1)
                OneCardPoker.create_betting_round(node.children[0], action_list + [0], cards)
                node.children[1] = ExtensiveGameNode(-1)
                OneCardPoker.create_betting_round(node.children[1], action_list + [1], cards)
        elif len(action_list) == 3:
            # This is also terminal, so we compute utility again:
            node.utility = OneCardPoker.compute_utility(action_list, cards)
            #node.children = {}
        return
    
    @staticmethod
    def create_game(n_cards):
        """ Creates the ExtensiveGame tree for 1-card poker.
        - n_cards is the number of cards in the deck.
        """
        # We first create the root node. This is a chance node for player 1
        # (so is hidden to player 2).
        root = OneCardPoker.create_chance_node(range(1, n_cards+1), 1)
            
        # Now create a player 2 chance node below each player 1 chance node.
        for action, node in root.children.items():
            root.children[action] = OneCardPoker.create_chance_node([card for
            card in range(1, n_cards+1) if card != action], 2)

        # Create a betting round below each player 2 chance node.
        for card1, node1 in root.children.items():
            for card2 in node1.children:
                new_node = ExtensiveGameNode(1)
                node1.children[card2] = new_node
                OneCardPoker.create_betting_round(new_node, [], {1: card1, 2: card2})
        
        return ExtensiveGame(root)

    
if __name__ == "__main__":
    #game = OneCardPoker.create_game(2)
    game = OneCardPoker.create_one_card_tree([], [1,2])
    #game.print_tree(only_leaves=False)
