# !/usr/bin/env python
# encoding: utf-8

"""
Run 'python demo.py -p SJFRR -l 5,10,15 -c' as an example
"""

import argparse
import random
import operator

# initialize a new parser object
parser = argparse.ArgumentParser(description="""
                Simulate scheduling policies and compute the turnaround time, response time, and wait time for each job.
                Available scheduling policies:
                First In First Out (FIFO), Short Job First (SJF), Round Robin (RR), Round Robin Short Job First (SJFRR)
                """)

# add options
parser.add_argument("-c", default=False,
                    help="compute the result",
                    action="store_true", dest="solve")
parser.add_argument("-j", "--jobs", default=3,
                    help="number of jobs",
                    action="store", type=int, dest="jobs")
parser.add_argument("-p", "--policy", default="FIFO",
                    help="scheduling policy to use: FIFO(default), SJF, RR, SJFRR",
                    action="store", type=str, dest="policy")
parser.add_argument("-l", "--timelist", default="",
                    help="provide a comma-separated time list of jobs (ex. 6,7,8,9,10)",
                    action="store", type=str, dest="timelist")
parser.add_argument("-m", "--maxlen", default=10,
                    help="max length (10 by default) of a single job",
                    action="store", type=int, dest="maxlen")
parser.add_argument("-q", "--quantum", default=1,
                    help="length of time slice for Round Robin policy",
                    action="store", type=int, dest="quantum")

options = parser.parse_args()


def fifo(runtime_list, timeline=0):
    """definition of the FIFO policy"""
    # [job_1_fisrtrun_time, ..., job_n_fisrtrun_time]
    firstrun_time_list = []
    # [job_1_completion_time, ..., job_n_completion_time]
    completion_time_list = []
    # disply the processes and append the result to the lists above
    for job_num in runtime_list:
        print "\tJob %d\t       %d\t\t%d" % (job_num[0], timeline, timeline + job_num[1])
        firstrun_time_list.append(timeline)
        timeline += job_num[1]
        completion_time_list.append(timeline)
    print "SUMMARY"
    print "\tAverage Turnaround Time: %d" % (sum(completion_time_list) / len(runtime_list))
    print "\tAverage Response Time: %d" % (sum(firstrun_time_list) / len(runtime_list))


def round_robin(runtime_list):
    """definition of the Round Robin policy"""
    # initialize the time
    timeline = 0
    def process(timeline):
        """definition of a recursive closure that prints out the process of RR policy"""
        for job in runtime_list:
            # set the rest job time to 0 if the time slice is longer than the rest process time
            if job[1] > 0:
                if job[1] - options.quantum < 0:
                    job[1] = 0
                else:
                    job[1] -= options.quantum
                    timeline += 1
                print "\t   %d\t\t  Job%d\t\t%d" % (timeline, job[0], job[1])
        # run the clusure recursively
        for job in runtime_list:
            if not job[1] == 0:
                process(timeline)
    process(timeline)


# main switcher of the options
if options.solve:
    # [[job_id_1, runtime_1], ..., [job_id_n, runtime_n]]
    runtime_list = []
    # create a random timelist if the user didn't specify -l option
    if options.timelist == "":
        for job_num in xrange(0, options.jobs):
            runtime = int(options.maxlen * random.random()) + 1
            runtime_list.append([job_num, runtime])
    # append the list that user entered to runtime_list
    elif not options.timelist == "":
        real_time_list = options.timelist.split(",")
        for job_num in xrange(0, len(real_time_list)):
            runtime = int(real_time_list[job_num])
            runtime_list.append([job_num, runtime])
    # run SJF Policy
    if options.policy == "SJF":
        runtime_list = sorted(runtime_list, key=operator.itemgetter(1))
        options.policy = "FIFO"
    # run FIFO Policy
    if options.policy == "FIFO":
        print "SCHEDULING START"
        print "\tJob num\tFirst run time\tCompletion time"
        fifo(runtime_list)
    # run SJF Round Robin Policy
    if options.policy == "SJFRR":
        runtime_list = sorted(runtime_list, key=operator.itemgetter(1))
        options.policy = "RR"
    # run Round Robin Policy
    if options.policy == "RR":
        print "SCHEDULING START"
        print "Current time slice of Round Robin policy is %d" % options.quantum
        print "\tTimeline\tJob num\t  Job process"
        round_robin(runtime_list)
else:
    parser.print_help()

