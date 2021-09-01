# Multi-Agent Learning

## Code

The code comes into the following six parts:
* Strategies: Different algorithms are defined in Strategies, which (1) decide the next action to take; (2) update the internal state after the payo↵ is received.
* Matrix Suite: Different games are defined in Matrix Suite, which are represented as payoff matrices.
* Game: Two players play against each other in Game, in which they take action and receive payoff based on
Matrix Suite. It is for one game.
* Grand Table: All the games are played between all the pairs of players for the specified number of rounds and restarts. It is for all the games, and it counteracts the randomness of games. The mean average payoff of all the algorithms for the row player are recorded in the grand table.
* Replicator Dynamic: Proportions of all the algorithms are calculated over the evolution and it will be visualized by a evolution graph.
* Nash: Nash equilibria will be generated by the tool Gambit.

## Algorithms

<p float='left'>
	<img src='pix/algorithms.png' width=800>
</p>

## Matrix suites

<p float='left'>
	<img src='pix/matrix.png' width=800>
</p>

## Grand tables

There are in total 12 grand tables generated by di↵erent parameters, which are shown as following:
<p float='left'>
	<img src='pix/grand-table-params.png' width=800>
</p>

"Fixed, Include own strategy" is used to produce the following grand table:
<p float='left'>
	<img src='pix/grand-table-fixed.png' width=800>
</p>

"Random Int, Include own strategy" is used to produce the following grand table:
<p float='left'>
	<img src='pix/grand-table-random-int.png' width=800>
</p>

## Replicator dynamic graphs

2 of the 12 replicator dynamic graphs are shown as following:
<p float='left'>
	<img src='pix/replicator-dynamic.png' width=800>
</p>

## Nash equilibria

2 of the 12 Nash equilibria are shown as following:
<p float='left'>
	<img src='pix/nash.png' width=800>
</p>