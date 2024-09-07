#this is just a file that defines the ASCII art for the images, so they can be plaed on the board.
#only for boats, tho.

#additionally, this contains data for the names of the parts of the boats
#notice the image data used

#1x1 boat, "The Tugboat" idk, really

tugBoat_NS_images = ["[]"]

tugBoat_names = ["Tugboat"]

tugBoat_EW_images = ["=="]

tugBoat_NS_images_destroyed = ["[*"]

tugBoat_EW_images_destroyed = ["*="]

#1x2 boat, "Submarine"

submarine_NS_images = ["()",
                       "\\/"]

submarine_names = ["Submarine Bridge", "Submarine Bow"]

submarine_EW_images = ["+O", ":>"]

submarine_NS_images_destroyed = ["( ",
                                 "\\*"]

submarine_EW_images_destroyed = ["+U", ";#"]

#1x3 boat, "Destroyer"

destroyer_NS_images = ["[]",
                       "O]",
                       "[-"]

destroyer_names = ["Destroyer Keel", "Destroyer Bridge", "Destroyer Gun"]

destroyer_EW_images = ["[=", "b:", "T]"]

destroyer_NS_images_destroyed = ["{]",
                                 "Q\\",
                                 "{\\"]

destroyer_EW_images_destroyed = ["[_", "o;", "Y\\"]

#1x4 boat, "Battleship"

battleship_NS_images = ["^]",
                        "[O",
                        "[]",
                        "[v"]

battleship_names = ["Battleship small gun", "Battleship bridge", "Battleship midship", "Battleship big gun"]

battleship_EW_images = ["-[", "P:", "==", "]-"]

battleship_NS_images_destroyed = ["*]",
                                  "*O",
                                  "*]",
                                  "*v"]

battleship_EW_images_destroyed = ["*[", "P;", "*=", "]*"]

#1x5 boat, "Aircraft Carrier"

aircraftCarrier_NS_images = ["/\\",
                             "O]",
                             "[]",
                             "[]",
                             "\\/"]

aircraftCarrier_names = ["Aircraft Carrier keel", "Aircraft Carrier bridge", "Aircraft Carrier runway", "Aircraft Carrier runway", "Aircraft Carrier bow"]

aircraftCarrier_EW_images = ["@<", "b:", "==", "==", ":>"]

aircraftCarrier_NS_images_destroyed = ["*\\",
                                       "O}",
                                       "[*",
                                       "[*",
                                       "\\*"]

aircraftCarrier_EW_images_destroyed = [" <", "b;", "=*", "=*", ";>"]

#lastly a small dictionary that can be used to translate a ship length into
#the name of the ship within this document.

length_to_names = {
        "1" : 'tugBoat',
        "2" : 'submarine',
        "3" : 'destroyer',
        "4" : 'battleship',
        "5" : 'aircraftCarrier'
    }
