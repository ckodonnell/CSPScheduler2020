from abc import ABC, abstractmethod
from itertools import combinations
import json


class Constraint():
    def __init__ (self, variables):
        self.variables = variables

    @abstractmethod
    def satisfied(self, assignment):
        ...


class CSP():
    def __init__(self, variables, domains): 
        self.solutionList = [] # list of solutions
        self.variables = variables # list of classes
        self.domains = domains # {class: [[time], [room], [prof]]} dict
        self.constraints = {} # {class: [Constraints]} dict
        for variable in self.variables:
            self.constraints[variable] = []

    def add_constraint(self, constraint):
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable not in CSP")
            else:
                self.constraints[variable].append(constraint) 

    def consistent(self, variable, assignment):
        # assignment is a dictionary {v,d}
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    def backtracking_search(self, assignment = {}):
        # base case: all variables are assigned
        if len(assignment) == len(self.variables):
            return assignment
        
        unassigned = [
            v
            for v in self.variables
            if v not in assignment
        ]

        first = unassigned[0]

        for time in self.domains[first][0]:
            for room in self.domains[first][1]:
                for prof in self.domains[first][2]:
                    for labtime in self.domains[first][3]:
                        local_assignment = assignment.copy()
                        local_assignment[first] = [time, room, prof, labtime]
                        # if we're still consistent, we recurse (continue)
                        if self.consistent(first, local_assignment):
                            result = self.backtracking_search(local_assignment)
                            # if we didn't find the result, we will end up backtracking
                            if result is not None:
                                return result
                                #self.solutionList.append(result)
        #quadruply nested forloop lol
        return None



class connectedClasses(Constraint): #classes that people usually take together should be @ different times
    def __init__(self, class1, class2):
        super().__init__([class1, class2]) #i changed this
        self.class1 = class1
        self.class2 = class2

    def satisfied(self, assignment):
        if self.class1 not in assignment or self.class2 not in assignment:
            return True
            
        if assignment[self.class1][0] == assignment[self.class2][0]: #where 0 represents time?
            return False
        return True

class ProfSameTime(Constraint): #profs cant have two simultaneous classes— would we need to add this constraint for every combo of classes?
    def __init__(self, class1, class2):
        super().__init__([class1, class2])
        self.class1 = class1
        self.class2 = class2

    def satisfied(self, assignment): #if a prof has two simultaneous classes, bad
        if self.class1 not in assignment or self.class2 not in assignment:
            return True
            
        # for class times
        if assignment[self.class1][2] == assignment[self.class2][2] and assignment[self.class1][0] == assignment[self.class2][0]: #where 2 represents prof
            return False
            
        # for lab times
        if assignment[self.class1][2] == assignment[self.class2][2] and assignment[self.class1][3] == assignment[self.class2][3]: #where 2 represents prof
            return False
        return True

class SameRoomSameTime(Constraint): #if 2 classes share the same room at the same time, bad
    def __init__(self, class1, class2):
        super().__init__([class1, class2])
        self.class1 = class1
        self.class2 = class2

    def satisfied(self, assignment):
        if self.class1 not in assignment or self.class2 not in assignment:
            return True
        
        # for class times
        if assignment[self.class1][1] == assignment[self.class2][1] and assignment[self.class1][0] == assignment[self.class2][0]: #where 1 is room, 0 is time
            return False
            
        # for lab times
        if assignment[self.class1][3] == assignment[self.class2][3] and assignment[self.class1][1] == assignment[self.class2][1]:
            return False
        return True

class dontKillOurProfs(Constraint):
    def __init__(self, professors, classes):
        super().__init__(classes)
        self.professors = professors
        #assignment = {class: [time, room, prof]} dict

    def satisfied(self, assignment):
        profs = dict.fromkeys(self.professors, 0) # {professor: num_of_classes} dict
        #print(assignment)
        for element in assignment.values():
            profs[element[2]] = profs[element[2]] + 1
            
        for p in profs:
            if profs[p] > 2:
                return False
        return True

class assignClassToProfessor(Constraint):
    def __init__(self, preferredProfs, classes):
        super().__init__(classes)
        self.preferredProfs = preferredProfs
        self.classes = classes
        #assignment = {class: [time, room, prof]} dict

    def satisfied(self, assignment):
        for c in self.classes:
            if assignment[c][2] in self.preferredProfs:
                return True
            else:
                return False

class everyProfessorHasClass(Constraint):
    def __init__(self, classes):
        super().__init__(classes)
        self.classes = classes

    def satisfied(self, assignment):
        unassignedProfs = ["Gordon", "Hunsberger", "Smith", "Waterman", "Gommerstadt", "Lemieszewski", "Ellman", "Lambert", "Saravanan", "Williams"]
        if len(assignment) == len(self.variables):
            for c in assignment.values():
                if c[2] in unassignedProfs: #aka this prof has already been assigned a class
                    unassignedProfs.remove(c[2])
        else: 
            return True

        if len(unassignedProfs) == 0: # if every professor has a class
            return True
        else: # if all classes are assigned but not all professors have a class
            return False

class classesThatNeedComputers(Constraint):
    def __init__(self, classes, rooms):
        super().__init__(classes)
        self.classes = classes
        self.rooms = rooms

    def satisfied(self, assignment):
        for c in assignment:
            if c in self.classes:
                if assignment[c][1] not in self.rooms:
                    return False
        return True

class classesThatDoNotNeedComputers(Constraint):
    def __init__(self, classes, rooms):
        super().__init__(classes)
        self.classes = classes
        self.rooms = rooms

    def satisfied(self, assignment):
        for c in assignment:
            #print(c)
            if c in self.classes:
                if assignment[c][1] not in self.rooms:
                    return False
        return True
        

class noTwoConsecutive(Constraint): #this is not finished...,,,
    def __init__(self, class1, class2, times):
        super().__init__([class1, class2])
        self.class1 = class1
        self.class2 = class2
        self.times = times

    def satisfied(self, assignment):
        return True

# check if a 1hr15 class block overlaps with a 2-hour lab block
class noTimeOverlap(Constraint):
    def __init__(self, classes):
        super().__init__(classes)
        self.classes = classes
        
    def satisfied(self, assignment):
        """
        a time string consists of:
        time[0] -> "M"
        time[1]    -> " "
        time[2:]   -> "00:00"
        """
        def checkOverlap(time, labtime):
            timeSplit = time.split()
            labtimeSplit = labtime.split()
            if labtimeSplit[0] == timeSplit[0][0] or labtimeSplit == timeSplit[0][2]:
                if labtimeSplit[1] == "9:00" and (timeSplit[1] == "9:00" or timeSplit[1] == "10:30"):
                    return False
                elif labtimeSplit[1] == "1:00" and (timeSplit[1] == "12:00" or timeSplit[1] == "1:30"):
                    return False
                elif labtimeSplit[1] == "3:10" and (timeSplit[1] == "3:10" or timeSplit[1] == "4:35"):
                    return False
            return True
        
        for c in assignment.values():
            if c[3] is not "NO LAB":
                if not checkOverlap(c[0], c[3]):
                    return False
        return True

class noLab(Constraint):
    def __init__(self, classes):
        super().__init__(classes)
        self.classes = classes
        
    def satisfied(self, assignment):
        if c in self.classes and assignment[c][3] != "NO LAB":
            return False
        return True
        
class noLabSameTime(Constraint):
    def __init__(self, class1, class2):
        super().__init__([class1, class2])
        self.class1 = class1
        self.class2 = class2

    def satisfied(self, assignment):
        if self.class1 not in assignment or self.class2 not in assignment:
            return True
            
        if assignment[self.class1][3] == assignment[self.class2][3]:
            return False
        else:
            return True

if __name__ == "__main__":
    professors = ["Gordon", "Hunsberger", "Smith", "Waterman", "Gommerstadt", "Lemieszewski", "Ellman", "Lambert", "Saravanan", "Williams"]
    classes = ["101-51", "101-52", "101-53", "101-54", "102-51", "102-52", "144", "145-51", "145-52", "195", "203", "224", "240", "241", "334"]
    rooms = ["SP309", "SP105", "SP201", "SP206", "SP212"]
    times = ["M/W 9:00", "M/W 10:30", "M/W 12:00", "M/W 1:30", 
             "T/R 9:00", "T/R 10:30", "T/R 12:00", "T/R 1:30", "T/R 3:10", "T/R 4:35", 
             "W/F 9:00", "W/F 10:30", "W/F 12:00", "W/F 1:30"]
    labtimes = ["M 3:10 (LAB)", "T 3:10 (LAB)", "R 3:10 (LAB)", "F 3:10 (LAB)",
                "M 1:00 (LAB)", "T 1:00 (LAB)", "W 1:00 (LAB)", "R 1:00 (LAB)", "F 1:00 (LAB)", 
                "T 9:00 (LAB)", "F 9:00 (LAB)", 
                "M 8:00 (LAB)", "T 8:00 (LAB)", "R 8:00 (LAB)",
                "NO LAB"]
                
    classes_with_labs = ["101-51", "101-52", "101-53", "101-54", "102-51", "102-52", "144", "145-51", "145-52", "203", "224"]
    classes_without_labs = ["195", "240", "241", "334"]
    VARIABLES = classes
    domain = {}
    i = 0
    for clas in classes: 
        domain[clas] = [times, rooms, professors, labtimes] #so a list of lists...

    # CONSTRAINTS START HERE
    scheduler = CSP(VARIABLES, domain)
    combos_101 = combinations(classes[:4], 2)
    for c in list(combos_101):
        scheduler.add_constraint(connectedClasses(c[0], c[1]))

    combos_102_145 = combinations(["102-51", "102-52", "145-51", "145-52"], 2)
    for c in list(combos_102_145):
        scheduler.add_constraint(connectedClasses(c[0], c[1]))

    combos_classes_with_labs = combinations(classes_with_labs, 2)
    for c in list(combos_classes_with_labs):
        scheduler.add_constraint(noLabSameTime(c[0], c[1]))

    #print("classsessssss", classes[0:4])

    scheduler.add_constraint(assignClassToProfessor(["Hunsberger", "Gordon", "Smith"], classes[0:4])) # 101
    scheduler.add_constraint(assignClassToProfessor(["Gommerstadt", "Lemieszewski", "Ellman"], classes[4:6])) # 102
    scheduler.add_constraint(assignClassToProfessor(["Waterman"], ["144", "224"])) # 144
    scheduler.add_constraint(assignClassToProfessor(["Ellman", "Gordon", "Lambert", "Lemieszewski"], classes[7:9])) # 145
    scheduler.add_constraint(assignClassToProfessor(["Saravanan"], ["195"])) # 195
    scheduler.add_constraint(assignClassToProfessor(["Saravanan"], ["203"])) # 203
    scheduler.add_constraint(assignClassToProfessor(["Waterman"], ["224"])) # 224
    scheduler.add_constraint(assignClassToProfessor(["Gordon", "Lambert"], ["240"])) # 240
    scheduler.add_constraint(assignClassToProfessor(["Waterman", "Williams"], ["334"])) # 334
    
    scheduler.add_constraint(classesThatNeedComputers(["101-51", "101-52", "101-53", "101-54", "224", "334"], ["SP309"]))
    scheduler.add_constraint(classesThatDoNotNeedComputers(["102-51", "102-52", "144", "145-51", "145-52", "195", "203", "240", "241"], ["SP105", "SP201", "SP206", "SP212"]))

    scheduler.add_constraint(noLab(classes_without_labs))
    
    scheduler.add_constraint(noTimeOverlap(classes))
    # TODO: optimize this so that it doesn't do O(n^2)
    for c1 in classes:
        for c2 in classes:
            if c1 != c2:
                scheduler.add_constraint(ProfSameTime(c1, c2))
                scheduler.add_constraint(SameRoomSameTime(c1, c2))
    
    scheduler.add_constraint(dontKillOurProfs(professors, classes))
    scheduler.add_constraint(everyProfessorHasClass(classes))
        
    result = scheduler.backtracking_search()
    if result is None:
        print("nnnnnone")
    else:
        print(json.dumps(result, indent=4, sort_keys=True))

# TODO: fix -> all classes are MW
# TODO: add labs/intensives, asprey lab intensives
# TODO: add more class preferences

# final report : when it doesnt find a solution, possibly go to infinite loop