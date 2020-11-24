#import constraint
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Dict, List, Optional


class Constraint():
    def __init__ (self, variables):
        self.variables = variables

    @abstractmethod
    def satisfied(self, assignment):
        ...


class CSP():
    def __init__(self, variables, domains): 
        self.variables = variables # list
        self.domains = domains # {Variable: Domain} dict
        self.constraints = {} # {Variable: [Constraints]} dict
        for variable in self.variables:
            self.constraints[variable] = []

    def add_constraint(self, constraint):
        self.constraints[variable].append(constraint)

    def consistent(self, variable, assignment): 
        # assignment is a dictionary {v,d}
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    def backtracking_search(self, assignment):
        # base case: all variables are assigned
        for a in assignment:
            if len(assignment[a]) == len(self.values):
                return assignment
        
        unassigned = [
            v
            for v in self.variables
            if v not in assignment
        ]

        first = unassigned[0]
        #finish...

class cmpu102or145(Constraint): #classes and times?
    def __init__(self):

    def satisfied(self assignment):
        if assignment["102"][0] == assignment["145"][0]:
            return False
        return True



def main():

    professors = ["Gordon", "Hunsberger", "Smith", "Waterman", "Walter", "Meireles", "Gommerstadt", "Lemieszewski", "Ellman", "Lambert", "Saravanan", "Williams"]
    classes = ["101", "102", "144", "145", "195", "203", "224", "240", "241", "314", "315", "331", "365", "377"]
    rooms = ["SP309", "SP105", "NE206", "SP201", "SP206", "SP212", "Asprey Lab"]
    times = ["M/W 9:00", " M/W 10:30", "M/W 12:00", "M/W 1:30", 
             "T/R 9:00", " T/R 10:30", "T/R 12:00", "T/R 1:30", "T/R 3:10", "T/R 4:35", 
             "W/F 9:00", " W/F 10:30", "W/F 12:00", "W/F 1:30" ]
    labs = [] # todo : add lab times??

    VARIABLES = ["Professors", "Classes", "Rooms", "Times", "Days"]
    DOMAINS = [professors, classes, rooms, times, days]
    domain = {}
    i = 0
    for clas in classes: 
        domain[clas] = times


    scheduler = new CSP(VARIABLES, domain, {})

main()