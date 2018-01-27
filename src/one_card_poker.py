from extensive_game import ExtensiveGame, ExtensiveGameNode
from example_strategy import random_strategy, always_fold
from best_response import best_response
import numpy as np

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
    def compute_utility(betting_actions, hole_cards):
        """ Given actions in 'betting_actions' and hole_cards in 'hole_cards',
        compute the utility for both players at a terminal node.
        """
        # The bets are 1 (for the ante), then the sum of the even actions (for
        # player 1) and the odd actions (for player 2).
        bets = {1: 1, 2: 1}
        for i, action in enumerate(betting_actions):
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
        if len(action_list) == 0:
            # We are at the root of the tree, so we create a chance node for
            # player 1.
            root = ExtensiveGameNode(0)
            # This node is hidden from player 2
            root.hidden_from = [2]
            for card in cards:
                # Create a game tree below this node.
                root.children[card] = OneCardPoker.create_one_card_tree([card], cards)
                root.chance_probs[card] = 1.0 / len(cards)
            return ExtensiveGame(root)
        elif len(action_list) == 1:
            # We are at a chance node for player 2, so we create this chance
            # node, including its children.
            node = ExtensiveGameNode(0)
            # This node is hidden from player 1
            node.hidden_from = [1]
            for card in cards:
                # Player 2 can't be dealt the card that player 1 was dealt.
                if card == action_list[0]:
                    continue
                # Otherwise create a child node below
                node.children[card] = OneCardPoker.create_one_card_tree(action_list + [card], cards)
                node.chance_probs[card] = 1.0 / (len(cards) - 1.0)
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
            if action_list[3] == 0 or action_list[2] == action_list[3]:
                # The second player folded, or called a bet of 0, or called a
                # bet of 1. Thus this node is terminal.
                node = ExtensiveGameNode(-1)
                hole_cards = {1: action_list[0], 2: action_list[1]}
                node.utility = OneCardPoker.compute_utility(action_list[2:],
                hole_cards)
                return node
            else:
                # The actions were [0,1], and so player 1 gets another chance to
                # call or fold.
                node = ExtensiveGameNode(1)
                node.children[0] = OneCardPoker.create_one_card_tree(action_list + [0], cards)
                node.children[1] = OneCardPoker.create_one_card_tree(action_list + [1], cards)
                return node
        elif len(action_list) == 5:
            # It's player 2's second turn (but this actually must be terminal).
            node = ExtensiveGameNode(-1)
            hole_cards = {1: action_list[0], 2: action_list[1]}
            node.utility = OneCardPoker.compute_utility(action_list[2:],
            hole_cards)
            return node
        assert False

    @staticmethod
    def create_game(n_cards):
        """ Creates the One Card Poker game, with the given number of uniquely
        numbered cards in the deck, numbered 1 up to n_cards.
        """
        game_tree = OneCardPoker.create_one_card_tree([], range(1, n_cards+1))
        info_sets_1 = game_tree.build_information_sets(1)
        info_sets_2 = game_tree.build_information_sets(2)
        return game_tree, info_sets_1, info_sets_2

if __name__ == "__main__":
    game, info_sets_1, info_sets_2 = OneCardPoker.create_game(9)
    #game.print_tree(only_leaves=True)

    # Join the two info set dictionaries. The keys are nodes in the game tree
    # belonging to player 1 or player 2, and the values are the identifier for
    # the information set the node belongs to, from the perspective of the
    # player to play in the node.
    info_set_ids = {}
    for k, v in info_sets_1.items():
        if k.player == 1:
            info_set_ids[k] = v
    for k, v in info_sets_2.items():
        if k.player == 2:
            info_set_ids[k] = v

    print("We compute a random strategy for player 2")
    strategy_2 = random_strategy(game, 2)
    print(strategy_2)
    exploitability_2, br_against_2 = best_response(game, strategy_2, 1, info_set_ids)
    print("The best response against this random strategy has value: {}".format(exploitability_2))
    print("The best response strategy is")
    print(br_against_2)
    n = 1000
    results = game.expected_value(br_against_2, strategy_2, info_set_ids, n)
    print("We now run {} games of this strategy against the best response, and \
    find the mean value for player 1 is {} with standard error {}".format(n,
    np.mean(results), np.std(results) / np.sqrt(n)))
    print(np.mean(results), np.std(results) / np.sqrt(n))

    print("Now consider the strategy where player 2 always folds.")
    strategy_2_0 = always_fold(game, 2)
    exploitability_2_0, br_against_2_0 = best_response(game, strategy_2_0, 1,
    info_set_ids)
    print("The best response against this strategy has value: \
    {}".format(exploitability_2_0))
    print("The best response strategy is")
    print(br_against_2_0)
    results = game.expected_value(br_against_2_0, strategy_2_0, info_set_ids, n)
    print("We now run {} games of this strategy against the best response, and \
    find the mean value for player 1 is {} with standard error {}".format(n,
    np.mean(results), np.std(results) / np.sqrt(n)))
    print(np.mean(results), np.std(results) / np.sqrt(n))
    
    # We can also compute strategies from the other position.
    #strategy_1 = random_strategy(game, 1)
    #print(strategy_1)
    #exploitability_1 = best_response(game, strategy_1, 2, info_set_ids)
    #print(exploitability_1)

    #n = 10000
    #results = game.expected_value(strategy_1, strategy_2, info_set_ids, n)
    #print(np.mean(results), np.std(results) / np.sqrt(n))
