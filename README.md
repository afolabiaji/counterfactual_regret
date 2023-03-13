# Counterfactual Regret (CFR)

This repo is my implementation of the counterfactual regret algorithm outlined in this paper: https://www.ma.imperial.ac.uk/~dturaev/neller-lanctot.pdf

This algorithm is applied to Kuhn Poker, a toy model game. In this game there is a deck of cards: 1, 2 and 3. There are two playes who are dealt one card each at random.

Players ante one chip, and then the players take turns to bet. Each bet places an additional chip into the pot.

If a player bets and the other player chooses to pass, the betting player wins the pot. If both players bet or both pass, then the player with the higher card wins the pot.
