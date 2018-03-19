import matplotlib.pyplot as plt
import sys
import numpy as np

def create_plot(input_filenames, output_filename):
		for filename in input_filenames:
			with open(filename) as input_file:
				current_values = [float(x) for x in input_file.read().split()]

				plt.plot(current_values, label=filename.split("/")[-1].split(".")[0])
		plt.xlabel("steps")
		plt.ylabel("BLEU")
		plt.legend()
		plt.grid()
		plt.savefig(output_filename)


if __name__ == '__main__':
	output_filename = sys.argv[1]
	input_filenames = sys.argv[2:]
	create_plot(input_filenames, output_filename)
