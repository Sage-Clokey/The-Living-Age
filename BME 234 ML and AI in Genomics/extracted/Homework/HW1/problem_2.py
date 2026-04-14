import itertools
import numpy as np

TRAIN_DATA = "problem_2_train_data.txt"
VAL_DATA = "problem_2_val_data.txt"

def load_data(input_path):
	# Loads promoter and negative sequences from the input_path.
	# DO NOT modify this function.

	promoter_sequences, negative_sequences = [], []
	with open(input_path) as f:
		for line in f:
			seq, clazz = line.strip().split()
			if clazz == "1":
				promoter_sequences.append(seq)
			elif clazz == "0":
				negative_sequences.append(seq)
			else:
				raise Exception("All class values should be either 0 or 1.")

	return promoter_sequences, negative_sequences

def train_markov_model(sequences, k):
	# Fits a Markov model where each state is a substring of size k.
	# These states are overlapping. So, if a sequence started with "ACTGA"
	# with k = 3, the first few states would be ["ACT", "CTG", "TGA", ...].
	# This Markov model should have neither a start state (assume all states
	# are equally likely at the beginning of the sentence) nor an end state.
	#
	# returns: 
	#	- states: an ordered list of size 4^k of all possible kmers in the Markov model
	# 			  (the specific order of states does not matter)
	#	- transition_matrix: a probability matrix (2D numpy array) with size 4^k by 4^k such that
	# 	                     transition_matrix[row][col] = P(pi_{i + 1} = state[col] | pi_{i} = state[row])
	#							* in the above notation, pi_{i} denotes the ith state in the sequence
	#

	# TODO: implement this function
	pass

def get_log_odds_ratio(seq, states, k, promoter_transition_matrix, negative_transition_matrix):
	# returns: log { P(sequence | promoter sequence model) / P(sequence | negative sequence model) }
	# 
	# Assume that all first states are equally likely. That is, P(pi_{0} = state) = 1 / 4^k for all states

	# TODO: implement this function
	pass

def get_accuracy(promoter_sequences, negative_sequences, states, k, 
				 promoter_transition_matrix, negative_transition_matrix):
	# Determine our model's accuracy on the given sequences.
	# Per our model, we classify a sequence as coming from a promoter iff it has a log odds ratio > 0.

	# TODO: implement this function
	pass

def main():
	train_promoter_sequences, train_negative_sequences = load_data(TRAIN_DATA)
	val_promoter_sequences, val_negative_sequences = load_data(VAL_DATA)

	for k in range(1, 6):
		states, promoter_transition_matrix = train_markov_model(train_promoter_sequences, k)
		_, negative_transition_matrix = train_markov_model(train_negative_sequences, k)

		train_accuracy = get_accuracy(train_promoter_sequences, train_negative_sequences, states, k, 
				promoter_transition_matrix, negative_transition_matrix)
		val_accuracy = get_accuracy(val_promoter_sequences, val_negative_sequences, states, k, 
				promoter_transition_matrix, negative_transition_matrix)

		print("k = {}, train accuracy = {}, val accuracy = {}".format(k, train_accuracy, val_accuracy))



if __name__ == '__main__':
	main()