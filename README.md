# ReinforcementLearning
The alpha beta AI appears to dominate the Q learning AI due to being able to look ahead.
The Q learning AI doesn't look as far ahead as the alpha beta AI due to complexity and time limitations.

## Description:
The driver.py in the AI folder is the main driver of the AIs.
We have provided a log file in a nice tabular format, and we included a 16 experiment file, along with
the graphs that were spit out when running that 16 experiment version. The graphs can be located in
AI/Graphs/16Expr_graph for the 16 experiments version. The reason this is pre ran is because it takes
about a hour and a half to 2 hours to run these 16 experiments.

Taking your time into consideration when you run the driver.py it will run a way shorter version, but to
run the longer version you just comment out the parameters dictionary and uncomment out the other parameters
dictionary then run again.

## Source Code/Files:
- requirements.txt: contains all the libraries I have installed when running this program.
- board.py: source code for the checkers board
- 16Exp_log: log file for the 16 experiments
- Graphs: Directory containing the graphs from the executed program.
- Graphs/16Expr_graph: contains the graph from the 16 experiment attempt
- alpha_beta: The alpha beta class
- checkersplayer.py: contains the player class that both the Q learning and alpha beta AI inherent from.
- driver.py: contains the main code that operates the program
- global_logging.py: just a file included to import global file name across project.
- LogFile.txt: tabulate data
- dataset.json: generated data from the AI. Note this is initially deleted when turned in, run program to show up.
- q_learning.py: File containing class for Q learning AI
- utility_functions.py: file containing multiple utility functions.

## Instructions:
Inside the AI directory just execute:
python driver.py
