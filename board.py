#this is the file used to implement the board class
#a board contains information on placed ships, and can be shot at.

#it uses the ship image info and boardCell classes
from shipASCIIimages import *
from boardCell import boardCell

class Board:
    #this class takes a size on initiation to set itself up
    #it is made up of a bunch of boardCells
    #additionally, this takes a list of the ships involved. At default it uses
    #the normal boats so it doesn't have to have those inputted typically.
    #these are kept track of so that we can know when boats sink
    #it also takes an arguement about if the board should start revealed or not.
    #additionally, it takes an image fo be used for a cell if it is hidden.

    def __init__(self, boardSize = 10, shipsUsed = [1, 2, 3, 4, 5], startRevealed = True, hiddenImage = "88"):
        #as you can see the ships used list is just a list of the ships used
        self.board = []
        for i in range(boardSize):
            temp_list = [] #store the row being built for the board
            for j in range(boardSize):
                temp_list.append(boardCell(uncovered = startRevealed, cellName = "Ocean"))

            self.board.append(temp_list[:])

        #next, given the ships used, fetch their info and build out
        self.boatData = {}

        #this contains a list of boat names, along with how many parts of it are
        #left unsunk
        for shipSize in shipsUsed:
            #add the entry with the fetched name and size of the boat
            shipID = length_to_names[str(shipSize)]
            self.boatData[shipID] = shipSize

        #store the hidden area image
        self.hiddenImage = hiddenImage

    #now, we need to implement the function to check if a board spot is valid
    def isValidLocation(self, x, y):
        #No negative locations allowed
        if x <= -1 or y <= -1:
            return False
    
        board_size = len(self.board)
        #now see if the location is off the board
        if x >= board_size or y >= board_size:
            return False

        #if this all passed, it is a valid location
        return True

    #a helper function that adds to an x,y coordinate pair
    #but, in a given orientation.
    def addOrientation(self, x=0, y=0, amount=1, orientation="NS"):
        #simple if
        if orientation == "NS":
            return x, y + amount

        elif orientation == "EW":
            return x + amount, y

    #this is a function to place a ship onto the board by copying over the right
    #data.
    #this one forcably places the boat. The next version down will do checks before
    #calling this function.
    def placeBoat_forced(self, boatLength=3, orientation = "NS", x=0, y=0):
        #the first thing to do is the fetch up the images and names of the
        #boat
        boatName = length_to_names[str(boatLength)]
        boatImages = eval(boatName + "_" + orientation + "_images")
        boatImages_destroyed = eval(boatName + "_" + orientation + "_images_destroyed")
        boatNames = eval(boatName + "_names")

        #now, sequentially we place each segment of the boat.
        #for each of them, we just skip it if we try to place it outside the map.
        for i in range(boatLength):
            #check if in the board
            new_x, new_y = self.addOrientation(x=x, y=y, amount=i, orientation=orientation)
            if self.isValidLocation(new_x, new_y):
                #now it is valid.
                #modify the board with the correct data
                targetCell = self.board[new_y][new_x]

                targetCell.hasShip = True
                targetCell.cellName = boatNames[i]
                targetCell.shipID = boatName
                targetCell.cellHit = False
                targetCell.cellImage = boatImages[i]
                targetCell.cellImage2 = boatImages_destroyed[i]

    #now, the "safe" version of the place function that checks things beforehand
    def placeBoat(self, boatLength=3, orientation="NS", x=0, y=0, printErrors=False):
        #the first thing to do is the fetch up the images and names of the
        #boat
        boatName = length_to_names[str(boatLength)]
        boatImages = eval(boatName + "_" + orientation + "_images")
        boatImages_destroyed = eval(boatName + "_" + orientation + "_images_destroyed")
        boatNames = eval(boatName + "_names")

        
        #now, sequentially check each cell
        for i in range(boatLength):
            #check if in the board
            new_x, new_y = self.addOrientation(x=x, y=y, amount=i, orientation=orientation)
            if not self.isValidLocation(new_x, new_y):
                #not on the board
                if printErrors:
                    print("Cannot place boat outside of board.")
                    return False

                else:
                    raise ValueError("Cannot place boat outside of board.")

            #check if this is trying to place on top of another boat.
            if self.board[new_y][new_x].hasShip:
                #it does, oops!
                if printErrors:
                    print("Cannot place boat on top of another Boat.")
                    return False

                else:
                    raise ValueError("Cannot place boat on top of another Boat.")

        #if we got here, it is all good, call the placer function.
        self.placeBoat_forced(boatLength=boatLength, orientation= orientation, x=x, y=y)

        #for letting the program know stuff, return True
        return True


    #a function that returns a string array of the board
    def boardPrintString(self):
        temp_list = []
        #build out each row in a string
        for row in self.board:
            temp_string = ""
            #add the image of each row
            for cell in row:
                temp_string += cell.getImage(coveredImage = self.hiddenImage)

            #add the row to the full list
            temp_list.append(temp_string[:])

        return temp_list

    #another thing to help test
    def __str__(self):
        temp_list = self.boardPrintString()
        temp_string = ""
        for row in temp_list:
            temp_string += row + "\n"

        return temp_string

    #lastly, a mini function for testing. It destroys everything in a janky way. Do not use in any final code
    def destroyAll(self):
        for row in self.board:
            for cell in row:
                cell.cellHit = True
            

    #a function to shoot at a location on the map. It will process destroying and ending the game if needed.
    #it will return a string message of what events occurred, as that may be needed, and a bool of if the game is over or not.
    #True means game over
    #False does not
    def hitCell(self, x=0, y=0):
        #first, we ensure that the cell is on the board
        #if not, "miss" and the game goes on
        if not self.isValidLocation(x=x, y=y):
            return "That location is not on the Board. Miss!", False

        #next, we see if that cell has already been hit.
        #if so, alert that it already has been hit, and the game will not end if it has
        #not ended by this point already
        if self.board[y][x].cellHit:
            return "That cell has already been shot! (Miss, technically.)", False
        
        #now, if that location has no boat, update they board and return that message
        if not self.board[y][x].hasShip:
            #update the map
            self.board[y][x].cellHit = True
            self.board[y][x].uncovered = True
            return "You hit nothing. Miss!", False
        
        #You hit something. Make sure though.
        if self.board[y][x].hasShip:
            #the first thing is to update the map
            self.board[y][x].cellHit = True
            self.board[y][x].uncovered = True

            #next, we need to decrement the ship HP thing
            self.boatData[self.board[y][x].shipID] -= 1

            #if the boat sunk, do something special
            if self.boatData[self.board[y][x].shipID] == 0:
                #now, see if all of the boats are sunk!
                allSunk = True
                for boatName, boatHP in self.boatData.items():
                    if boatHP != 0:
                        allSunk = False

                if allSunk:
                    #return the full message and True, the game is over
                    return "You hit the " + self.board[y][x].callName + ". You sunk the " + self.board[y][x].shipID + "! You have sunk all enemy boats! Hit! You win!", True

                #If not, just return that you sunk the ship.
                return "You hit the " + self.board[y][x].callName + ". You sunk the " + self.board[y][x].shipID + "! Hit!", False

            #if not, just return the hit.
            return "You hit the " + self.board[y][x].callName + ". Hit!", False

        #At this point, something has gone wrong. Return an error!
        return "Something wents wrong. (Miss, technically.)"
