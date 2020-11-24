import constraint

class SchedulerConstraint(constraint.Constraint):
    no_simultaneous = 1 # prof cant have simultaneuous class times
    

def no_simultaneous(day1, time1, day2, time2):
    # prof cant have simultaneuous class times
    if day1 == day2 and time1 == time2:
        return False
    return True


def solve():
    professors = ["Gordon", "Hunsberger", "Smith", "Waterman", "Walter", "Meireles", "Gommerstadt", "Lemieszewski", "Ellman", "Lambert", "Saravanan", "Williams"]
    classes = ["101", "102", "144", "145", "195", "203", "224", "240", "241", "314", "315", "331", "365", "377"]
    rooms = ["SP309", "SP105", "NE206", "SP201", "SP206", "SP212", "Asprey Lab"]
    times = ["9:00", "10:30", "12:00", "1:30", "3:10", "4:35"] 
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    labs = [] # todo : add lab times??

    PROBLEM = Problem()
    VARIABLES = ["Professors", "Classes", "Rooms", "Times", "Days"]
    DOMAINS = [professors, classes, rooms, times, days]
    CONSTRAINTS = []

    for i in range(len(VARIABLES)):
        PROBLEM.addVariable(VARIABLES[i], DOMAINS[i])

    problem.addConstraint(FunctionConstraint(no_simultaneous),  )

def main():
    solutions = solve()
    showSolution(solutions)

def showSolution(solution):
    for s in solutions:
        print(s, "\n") # maybe we need sys.stdout.write(s) and import sys, not sure

main()