# Scheduling Policies Simulator

![Travis](https://travis-ci.org/kakugirai/scheduling_policies_simulator.svg?branch=master)

Here is a simple example:

```bash
$ python demo.py -p RR -j 4 -m 8 -q 2 -c
SCHEDULING START
Current time slice of Round Robin policy is 2
Timeline	Job num	  Job process
   1		  Job0		1
   2		  Job1		3
   3		  Job2		6
   4		  Job3		2
   4		  Job0		0
   5		  Job1		1
   6		  Job2		4
   7		  Job3		0
   7		  Job1		0
   8		  Job2		2
   9		  Job2		0
```
As we can see, this program created a random process list with the max length of 8 secs and then it applied the Round Robin scheduling policy (RR) with a 2 secs of time slice which stopped after all jobs reaching the 0 in the list of Job process.

There are severals choices on the policies and the explanation of them could be found when the -h option is specified.
