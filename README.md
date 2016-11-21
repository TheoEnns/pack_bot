# PackBot

Author: Theodore Enns, 11/20/16

Summary: pack_bot.py provides dynamic programming solution to the knapsack 0-1.

example usage (for linux):
> $ python src/pack_bot.py http://pkit.wopr.c2x.io:8000/suitcases/rolly http://pkit.wopr.c2x.io:8000/robots/hey-you/parts

### Testing
At the project route, run
> $python -m unittest discover -v

The end output should state all sven tests passed, for example:
>Ran 7 tests in 1.266s
OK


### Notes
  - This code was tested on Windows 10 and Ubuntu 14.04 both using python 2.7.
  - For portability, I avoided using any special python libraries. I chose python primarily because I knew I could easily make http requests without add-on libs and make porting the code from my system to yours as simple as possible (for whichever OS that might be).
  - Given the prompt, I would normally ask an interviewer about how he/she would like me to handle redundant optimal solutions or report error cases such as empty input data sets, but I know people are out on Thanksgiving, so I made my best reasonable assumptions.

