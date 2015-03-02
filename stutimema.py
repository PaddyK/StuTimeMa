#!/usr/bin/env python
import datetime, getopt, sys

def putDate(path, verb):
    dt  = datetime.datetime.now()
    d   = dt.date()
    t   = dt.time()

    with open(path, 'a') as f:
        f.write(d.strftime("%Y-%m-%d") + "\t" + t.strftime("%H:%M:%S") + "\t" + verb)
        f.write("\n")
#    print(d.strftime("%Y-%m-%d") + "\t" + t.strftime("%H:%M:%S") + "\t" + verb)
    if verb == "start":
        print "You can do this!"

def calcTimeWorked(path):
    with open(path, "r") as f:
        f.seek(-52, 2)
        stamps      = f.read(51).splitlines()
        stamps[0]   = stamps[0][0 : stamps[0].rfind("\t")].replace("\t"," ")
        stamps[1]   = stamps[1][0 : stamps[1].rfind("\t")].replace("\t"," ")
        start   = datetime.datetime.strptime(stamps[0], "%Y-%m-%d %H:%M:%S")
        end     = datetime.datetime.strptime(stamps[1], "%Y-%m-%d %H:%M:%S")
        print "Time studied: " + str(end - start)

def smallReport(path):
    ctr     = 0
    now     = datetime.datetime.now()
    stop    = now
    delta   = datetime.timedelta(0)

    with open(path, 'r') as f:
        while f.tell() != 25:
            ctr = ctr + 1
            f.seek(-26 * ctr, 2)
            date, time, verb = f.read(25).split("\t")
            dt = datetime.datetime.strptime(date + time,"%Y-%m-%d%H:%M:%S")
            if dt.date() < now.date():
                break

            if verb == "stopp":
                stop = dt 
            elif verb == "start":
                delta = delta + stop - dt

    print "Break deserved, you studied: " + str(delta)

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h", ["start", "stop", "today"])
    except getopt.GetoptError:
        print 'stutimema -start|-stop'
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print 'stutimema.py -start|-stop'
            sys.exit()
        elif opt == "--start":
            putDate("timestamps", "start")
        elif opt == "--stop":
            putDate("timestamps", "stopp")
            calcTimeWorked("timestamps")
        elif opt == "--today":
            smallReport("timestamps")

if __name__ == "__main__":
    main(sys.argv[1:])
