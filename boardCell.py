#This is a file that contains the class for a cell on the board.
#it is pretty simple overall.

class boardCell:
    #the idea is that each cell holds the image that it displays, as well as
    #optionally it will hold an image to swap to once this cell becomes shot.
    #It will hold a bool of if there is a ship here or not, and if it is
    #shot or not.
    #it will also hold a name of the thing that is here, such as "Submarine Keel" for example
    #it also hold the ID of the ship it is a part of. This is mainly just for
    #tracking when specific ships sink.
    #also this tracks if it is hit or not

    #these can be passed into init optionally to set them at the start
    def __init__(self, hasShip = False, uncovered = False, cellHit = False, cellName = None, shipID = None, cellImage = "  ", cellImage2 = None):
        self.hasShip = hasShip
        self.uncovered = uncovered
        self.cellName = cellName
        self.shipID = shipID
        self.cellImage = cellImage
        self.cellImage2 = cellImage2
        self.cellHit = cellHit

    #this is a small helper function to return the image of this cell given
    #state
    #it takes the image to be used for unrevealed cells as an arguement.
    def getImage(self, coveredImage = "88"):
        #if the cell is hidden, use the covered up image
        if self.uncovered == False:
            return coveredImage
        
        #if cellImage2 is None, there is no second image, return the first one.
        if self.cellImage2 == None:
            return self.cellImage

        #otherwise, see if this cell is hit or not
        #then return image 2 if the cell is hit
        #1 otherwise
        if self.cellHit:
            return self.cellImage2

        return self.cellImage
