#! /usr/bin/python3

# -*- coding: utf-8 -*-
"""
human VS AI models
Input your move in the format: 2,3

@author: Junxiao Song
"""

from __future__ import print_function
import time
import pickle
from game import Board, Game
from mcts_pure import MCTSPlayer as MCTS_Pure
from mcts_alphaZero import MCTSPlayer
from policy_value_net_numpy import PolicyValueNetNumpy
import stacktracer

# from policy_value_net import PolicyValueNet  # Theano and Lasagne
# from policy_value_net_pytorch import PolicyValueNet  # Pytorch
# from policy_value_net_tensorflow import PolicyValueNet # Tensorflow
# from policy_value_net_keras import PolicyValueNet  # Keras


class Human(object):
    """
    human player
    """

    def __init__(self):
        self.player = None

    def set_player_ind(self, p):
        self.player = p

    def get_action(self, board):
        try:
            location = input("Your move: ")
            if isinstance(location, str):  # for python3
                location = [int(n, 10) for n in location.split(",")]
            move = board.location_to_move(location)
        except Exception as e:
            move = -1
        if move == -1 or move not in board.availables:
            print("invalid move")
            move = self.get_action(board)
        return move

    def __str__(self):
        return "Human {}".format(self.player)


def run():
    n = 5
    width, height = 8,8
    try:
        board = Board(width=width, height=height, n_in_row=n)
        game = Game(board)
        start_time = time.perf_counter()
        # ############### human VS AI ###################
        # load the trained policy_value_net in either Theano/Lasagne, PyTorch or TensorFlow

        # best_policy = PolicyValueNet(width, height, model_file = model_file)
        # mcts_player = MCTSPlayer(best_policy.policy_value_fn, c_puct=5, n_playout=400)

        # load the provided model (trained in Theano/Lasagne) into a MCTS player written in pure numpy
        #best_policy = PolicyValueNetNumpy(width, height, policy_param)
        #mcts_player = MCTSPlayer(best_policy.policy_value_fn,
       #                          c_puct=5,
        #                         n_playout=400)  # set larger n_playout for better performance

        # uncomment the following line to play with pure MCTS (it's much weaker even with a larger n_playout)
        mcts_player = MCTS_Pure(c_puct=5, n_playout=16000)

        # human player, input your move in the format: 2,3
        human = MCTS_Pure(c_puct=5, n_playout=16000)

        # set start_player=0 for human first
        _, steps = game.start_play(human, mcts_player, start_player=1, is_shown=1)
        end_time = time.perf_counter()
        print("Steps = ", steps, "Average step time: ", (end_time - start_time) / steps, " 秒.")
    except KeyboardInterrupt:
        print('\n\rquit')


if __name__ == '__main__':
    stacktracer.register_stack_trace_dump()
    run()
