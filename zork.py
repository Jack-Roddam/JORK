import math
import mariadb
import pickle

try:    #connects to the database
    scores_db = mariadb.connect(
    host="localhost",
    user="jack",
    password="onion",
    database="Scores"
    )
except mariadb.Error as error:
    print("Something went wrong when connecting to the database: {}".format(error))

class room():
    def __init__(self,directions,description,enemyDesc,items,enemies,doors,visited):
        self.directions = directions
        self.description = description
        self.enemyDesc = enemyDesc
        self.items = items
        self.enemies = enemies
        self.doors = doors
        self.visited = visited
    def getDescription(self):
        return self.description
    def getEnemyDesc(self):
        return self.enemyDesc
    def getDirections(self):
        return self.directions
    def getVisit(self):
        return self.visited
    def setVisit(self,bool):
        self.visited = bool
    def getItems(self):
        return self.items
    def getEnemies(self):
        return self.enemies
    def getDoors(self):
        return self.doors
    def setDescription(self,newdesc):
        self.description = newdesc
    def sortItems(self): #sorts items ina  room using binary serach
        swapped = True
        while swapped == True:
            swapped = False
            for i in range(len(self.items)-1):
                if self.items[i].getName()>self.items[i+1].getName():
                    x = self.items[i]
                    self.items[i] = self.items[i+1]
                    self.items[i+1] = x
                    swapped = True
    def search(self,itemName,array): #checks if the room conatains an item matching the name given by a user using binary search
        found = False
        S = 0
        E = len(array)-1
        while found == False and S<=E:
            M = math.floor((S+E)/2)
            if array[M].getName() == itemName:
                found = True
            elif array[M].getName() < itemName:
                S = M+1
            else:
                E = M-1
        return found
    def getObjectByName(self,itemName,type): #returns item that matches the name given by the user using binary search
        if type == "I":
            array = self.items
        else:
            array = self.enemies
        found = False
        item = None
        S = 0
        E = len(array)-1
        while found == False and S<=E:
            M = math.floor((S+E)/2)
            if array[M].getName() == itemName:
                found = True
                item = array[M]
            elif array[M].getName() < itemName:
                S = M+1
            else:
                E = M-1
        return item
    def addItem(self,item):
        self.items.append(item)
        self.sortItems()
    def removeItem(self,item):
        (self.items).remove(item)
    def removeEnemy(self,enemy):
        self.enemies.remove(enemy)
    def searchDir(self,dir): #linear search to see if given direction is applicable for the room(linear search as there will only be a maximum of four items in the directions array)
        for i in self.directions:
            if i  == dir:
                return True
        return False
            
class item():
    def __init__(self,name):
        self.name = name
    def getName(self):
        return self.name

class message(item):
    def __init__(self,name,text):
        super().__init__(name)
        self.text = text
    def getText(self):
        return self.text

class weapon(item):
    def __init__(self,name,atk):
        super().__init__(name)
        self.atk = atk
    def getAtk(self):
        return self.atk

class food(item):
    def __init__(self,name,hpb):
        super().__init__(name)
        self.hpb = hpb
    def getHpb(self):
        return self.hpb

class key(item):
    def __init__(self,name,doorID):
        super().__init__(name)
        self.doorID = doorID
    def getDoorID(self):
        return self.doorID
    
class door():
    def __init__(self,name,ID,direction):
        self.name = name
        self.ID = ID
        self.locked = True
        self.direction = direction
    def getID(self):
        return self.ID
    def getLocked(self):
        return self.locked
    def getDirection(self):
        return self.direction
    def getName(self):
        return self.name
    def unLock(self):
        self.Locked = False

class player():
    def __init__(self,hp,x,y,inventory,score,moves):
        self.hp = hp
        self.x = x
        self.y = y
        self.inventory = inventory
        self.score = score
        self.moves = moves
        self.tcount = 0
    def getHp(self):
        return self.hp
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getScore(self):
        return self.score
    def getMoves(self):
        return self.moves
    def getTcount(self):
        return self.tcount
    def incrementTcount(self):
        self.tcount += 1
    def addScore(self,num):
        self.score += num
    def incrementMoves(self):
        self.moves += 1
    def setX(self,change):
        self.x += change
    def setY(self,change):
        self.y += change
    def addHp(self,bonus):
        self.hp += bonus
    def getInventory(self):
        return self.inventory
    def showInventory(self): #prints contents of players inventory and stats where required
        if len(self.inventory) == 0:
            return "you got nothing homie"
        else:
            print("you have: ")
            for i in range(len(self.inventory)): #loops through inventory
                print("a " + self.inventory[i].getName())
                if isinstance(self.inventory[i],weapon): #checks if item is of a wepaon type
                    print("^attack points are "+ str(self.inventory[i].getAtk())) # displays that item's attack attribute
                elif isinstance(self.inventory[i],food): #same as for wepaon but with the healing value
                    print("^health bonus points are "+ str(self.inventory[i].getHpb()))
    def sortInv(self): #sorts the inventoory so binary search is apllicable using bubble sort
        swapped = True
        while swapped == True:
            swapped = False
            for i in range(len(self.inventory)-1):
                if self.inventory[i].getName()>self.inventory[i+1].getName() :
                    x = self.inventory[i]
                    self.inventory[i] = self.inventory[i+1]
                    self.inventory[i+1] = x
                    swapped = True
    def searchInv(self,itemname): #checks if an a given name from user matches the name of item in the player sinventory using binary search
        array = self.inventory
        found = False
        S = 0
        E = len(array)-1
        while found == False and S<=E:
            M = math.floor((S+E)/2)
            if array[M].getName() == itemname:
                found = True
            elif array[M].getName() < itemname:
                S = M+1
            else:
                E = M-1
        return  found
    def addToInv(self,item,room):
        self.inventory.append(item)
        plyr.sortInv()
        room.removeItem(item)
    def removeFromInv(self,item):
        self.inventory.remove(item)
    def getItemByName(self,itemName): #returns the item from name of item given by user with a binary search
        array = self.inventory
        found = False
        item = None
        S = 0
        E = len(array)-1
        while found == False and S<=E:
            M = math.floor((S+E)/2)
            if array[M].getName() == itemName:
                found = True
                item = array[M]
            elif array[M].getName() < itemName:
                S = M+1
            else:
                E = M-1
        return item
    def getInvLen(self):
        return(len(self.inventory))

class enemy():
    def __init__(self,name,hp,atk,drops,blockDir,scorePoints):
        self.name =  name
        self.hp = hp
        self.atk = atk
        self.drops = drops
        self.blockDir = blockDir
        self.scorePoints = scorePoints
    def getName(self):
        return self.name
    def getHp(self):
        return self.hp
    def getAtk(self):
        return self.atk
    def getDrops(self):
        return self.drops
    def getBlockDir(self):
        return self.blockDir
    def getScorePoints(self):
        return self.scorePoints
    def takeDmg(self,num):
        self.hp -= num
    def dropItems(self,room): #adds items from enemy to the room so user can take them
        if len(self.drops) > 0:
            print("the fallen adversary dropped:")
            for i in self.drops: #adds all items to be dropped by enemy to room
                room.addItem(i)
                print("a " + i.getName()) # tells user
        else:
            print("the " + self.name + " dropped nothing")

def doorCheck(room,direction): #checks if a door is blocking a given direction and is locked
    if len(room.getDoors()) != 0: #if there are any doors
        for i in room.getDoors(): #loop through doors and see if any block given direction and are locked
            doorDir = i.getDirection()
            if doorDir == direction and i.getLocked() == True:
                return True #signify if door is blocking and locked is blocking or not
    else:
        return False

def enemyBlockCheck(room,direction): #checks if an enemy is blocking a given direction
    if len(room.getEnemies()) != 0: #if there are any enemies
        for i in room.getEnemies(): #loop through enemies and see if any block given direction
            enemyDir = i.getBlockDir()
            for i in enemyDir: # loop through direction blocked by enemy
                if i == direction:
                    return True #signify if enemy is blocking or not
    else:
        return False

def consume(name): #fucntion to consume an item, used as function so as not repeat code in and ouit of fighting
    if plyr.searchInv(name) == True: #chekc if player has given item
        curItem = plyr.getItemByName(name)
        if isinstance(curItem, food): #check  if item given is a consumable item
            hpb = curItem.getHpb()
            playerhp = plyr.getHp()
            if hpb + playerhp > 20: #brings player to max hp if health point bonus is greater than max hp
                plyr.addHp(20-playerhp)
            else:
                plyr.addHp(hpb) #add health bonus to players hp
            plyr.removeFromInv(curItem)
            print("you consumed the {}, your hp is now {}".format(curItem.getName(),plyr.getHp())) #display result
            return True #signifys if "consuming" was successful to indicate what output to return in combat
        else:
            print("you really want to eat that???")
            return False
    else:
        print("you dont have one of those")
        return False
    
def displayDesc(): #function to display the room description
    if len(curRoom.getEnemies()) > 0: #checks if an emeny is present in the room
        print(curRoom.getDescription() + curRoom.getEnemyDesc()) #appends enemy description
    else:
        print(curRoom.getDescription()) #displays description without enemy description
        curRoom.setVisit(True)

#instansiate objects            
note = message("note","dear reader, To whoever may find this, if u are able bodied u must find the 5 lost relics and unite them in the heart of this land to in order to restore peace and end the wars and monsters that besiege the people, i cannot help you do this but i knwo someone can, they must ") #instansiate all the objects(items,enemies,rooms that are present in game)
Kmsg = message("KnightsNote","???")
apple = food("apple",3)
bread = food("bread",5)
CGate = door("castleGate",1,"s")
cgk = key("castleKey",1)
twigs = item("twigs")
rocks = item("rocks")
bW = item("brokenWeapon")
Bdag = weapon("bloodyDagger",1)
Rswrd = weapon("rustySword",4)
hammer = weapon("hammer",3)
BAxe = weapon("battleAxe",19)
looter = enemy("looter",1,0,[bread],[],2)
troll = enemy("troll",5,3,[hammer],["w"],10)
troll1 = enemy("troll",5,3,[hammer],["e"],10)
Gru = enemy("Gru",100,9,[],[],600)
knight = enemy("knight",10,3,[Kmsg,BAxe],["s"],10)
crown = key("crown",3)
jewlS = key("jewledStaff",4)
cerSwo = key("ceremonsialSword",5)
divId = key("divineIdol",6)
orb = key("magicOrb",7)
cped = door("pedastel",3,"s")
jped = door("pedastel",4,"s")
sped = door("pedastel",5,"s")
oped = door("pedastel",6,"s")
dped = door("pedastel",7,"s")
king = enemy("king",5,1,[crown],[],10)
feast = food("feast",20)
window = door("window",2,"n")
wKey = key("windowKey",2)
aMeat = food("assortedMeats",15)
bandit = enemy("bandit",7,3,[aMeat],[],15)
aMeat = food("assortedMeats",10)
fish = food("fish",4)
trident = weapon("trident",5)
mm =  enemy("mermaid",10,5,[trident],["n","w"],25)
icew = enemy("iceWraith",6,2,[],["e","w"],10)
icew1 = enemy("iceWraith",6,2,[],["e","w"],10)
sand = item("sand")
snakeMeat = food("snakeMeat",4)
snake = enemy("snake",6,2,[snakeMeat],[],5)
rock = weapon("abnormalRock",2)
cutlass = weapon("cutlass",7)
mate = enemy("mate",10,5,[cutlass],[],20)
captain = enemy("captain",15,7,[jewlS],[],40)
water = food("water",6)
frostTroll = enemy("frostTroll",8,4,[],[],20)
greatSword = weapon("greatSword",15)
greatWolf = enemy("greatWolf",25,8,[greatSword],["e"],100)
gold = key("goldPieces",8)
hdoor = door("Hermit's door",8,"s")
potion = food("healthPotion",20)
fangs = item("fangs")
wildbeast = enemy("wildBeast",7,3,[fangs],[],15)
fortGate = door("fortGate",9,"e")
champion = enemy("champion",50,8,[cerSwo],[],250)
Golem = enemy("Golem",25,6,[],["n"],75)
throne = item("throne")
ghost = enemy("ghost",15,4,[],["s"],30)
r33 = room(["n","w","s"],"You are in large open field, infront of you lies a soldier clutching a note to his chest(right above the dagger in his heart). A path leads north to a forest, you see tips of mountains far in the east blocked by thick trees and a castle to the south.","another path west leads into more fields behind a lumbering troll",[Bdag,note],[troll],[CGate],False)
r23 = room(["s","e","n"],"you are in forest, a path leads back south to the fields, through the trees you can see a road one of them is an apple tree."," the path east is blocked by a troll",[apple],[troll1],[],False)
r24 = room(["w","s",],"you walk into a clearing, an entrance to the dark of the overgrown forest lies to the south and a hill to steep to climb to your north","",[],[],[],False)
r43 = room(["n","s","w"],"you enter the castle's courtyard, to the your right you see the sign barracks, straight ahead the keep",", guarded by a iron-klad knight",[],[],[],False)
r22 = room(["s","n","w"],"you find yourself on a long road that snakes east round the forest, cutting sharply uphill to the nroth you see snow peaked mountain rise a lonely humble hut stand to your west","",[],[],[],False)
r32 = room(["e","n"],"walking through the field the ground turns to mud and bodies and blood cover the landscape, among the pile of bodies a banner lies by a fallen knight with a gold key around his neck",", u can see another looter across the field",[bW,cgk],[looter],[],False)
r34 = room(["s","n"],"the dark of the forrest surrounds you, you can just see the mouth of a cave to your south, the forest is impenetrable on either side and the mountians rise far too high to climb, a loud roar errupts from the cave","",[twigs],[],[],False)
r44 = room(["n","s"],"The cave, a gloomy dull light eminates from a tunnel ahead",", the shadow of a Gru roars acorss the cave, he will probably eat you ",[rocks],[Gru],[],False)
r42 = room(["e"],"'the barracks' they've ransacked nothing remains bar a solo stand for what might have once been a beautiful sword(now rusty)","",[Rswrd],[],[],False)
r00 = room(["e","s"],"in the base of the tower upon a magnificant shrine stands a divine idol surrounded by praying cultists(an arrangemnt of potions litter the area), u notice a trap door that drops south into a ravine","",[divId,potion,potion,potion],[],[],False)
r01 = room(["e","w","s"],"you walk onto the narrow icy pass. the edge of the glacier lies to your south and the mountain to your east. Striaght a head a twisting tower reaches into the across a thin bridge"," a great wolf with sword betwixt its teeth stands guard",[],[greatWolf],[],False)
r02 = room(["s"],"As you reach the summit after a trecherous climb and the blizzard clears"," u can see a small swirling swarm of iceWraiths, it will be impossible to move through the mountains till there all gone",[],[icew,icew1],[],False)
r10 = room(["s","e"],"standing in this great ravine you feel an enormous sense of belittlment, does this quest even matter. A river runs south into a cave it has slowly bored away."," The frostTroll doesnt seem to have such thoughts as he charges around, up in the mountains the trolls seem far more primitive",[water],[frostTroll],[],False)
r11 = room(["n","w"],"standing a on the huge ice wall u stare over the edge of the glacier, far beneath, you spy a hut, to your north the narrow mountain pass and to the west steep cut back lead down into the ravine","",[],[],[],False)
r12 = room(["s","n","e"],"you continue along the road, it branches out east round the forest and north into the mountains up a crooked path","",[],[],[],False)
r13 = room(["e","w"],"The road: it stretches to the east and west with rising mountains(they look too hard to climb from here) on the other side. A flipped cart lies of the track"," with a bandit looming over",[],[bandit],[],False)
r14 = room(["w","s","e"],"a steep hill leads down to the south into the forest, you wouldnt be able to climb back up, where the road terminates another entrance to the forest opens up","",[],[],[],False)
r15 = room(["e","s","w"],"entering the forest u feel a presence u havnt felt anywhere else before, spectral aparations appear and vanish in the blink of an eye, treading further down the path a battle ready fort appears ahead, another gloomy path leads south","",[apple,apple],[],[fortGate],False)
r16 = room(["e","s"],"the guge wooden spikes of the fort walls rise around corpses lie mangled in numerous ways"," a lone champion standing 8 feet tall in the middle holding a gleaming sword",[champion],[],[],False)
r30 = room(["n","s"],"the river flows north to south through the cave but opens up into a large pool of clear water, at the bottom an open chest","",[gold],[],[],False)
r21 = room(["e"],"the hut is a workshop and is full of windows, the skeleton of a window-smith lies clutching a tempered pane of glass, u wonder if theres actually anything usefull here","",[wKey],[],[],False)
r25 = room(["n","e","s"],"along the forest path the tress begin to block out the sun and you are led into a shadow filled graveyard. the mossy gravestones tell of great warriors and kings, one path continues east and to the south a large cave mouth with the inscription 'the kings road'",", a ghost rises from one such stone and shrieks standing infront of the cave ",[],[ghost],[],False)
r26 = room(["e","n"],"to the west a darker area of the forest to your north an open entrance to the fort","",[],[],[],False)
r20 = room(["n","e"],"following the river through the cave u see an exit east into the fields","",[],[],[],False)
r31 = room(["e","w","s"],"east of the battleground u walk through a field where a river runs(its source a cave to your west) ","",[],[],[],False)
r35 = room(["n","s"],"you enter a glittering cavern, an enormous ornately carved door lies ahead behind 5 stone pedastels, each marked with pictures the first resmebling a crown","",[],[],[cped,dped,jped,oped,sped],False)
r41 = room(["n","s"],"the farther from the river u walk the sparcer the landscape growing ever more arid."," hugry wildBeasts prowl the terrain ",[],[wildbeast,wildbeast],[],False)
r45 = room(["s"],"at the foot of the room sits a large throne","",[throne],[],[],False) #final room option to edn or continue
r46 = room(["s"],"you enter the wreck of the rear half of a large galleon",",2 pirates(the captain and his mate) sit by a chest eating a parrot as the last of their rations",[mate,captain],[],[],False)
r50 = room(["e","s"],"u barge into a hermit's humble abode, he asks if u want to use his door and asks for some shiny gold pieces","",[],[],[hdoor],False)
r51 = room(["n","w"],"the arid landscape quickly turns to stone and an enormous rock wall it seems to be completely featureless apart from a small door built into the wall to the west","",[],[],[],False)
r53 = room(["n"],"inside the castle: an enormous round table surrounded by pompus members of the court and at its head a king, they are all too absorbed in themselves to notice you."," The king is wearing a shiny crown!!!",[king],[feast],[],False)
r54 = room(["n","s","e"],"entering the tunnel you see it forks of to your left as well as continuing, you only see light from ahead","",[],[],[],False)
r55 = room([],"the tunnel leads steeply downhill, u being to slip, then fall, plunging through the darkness you you see the floor of the pit race toward you, u feel helpless stuck in the darkness with no way to go","",[],[],[],False)
r56 = room(["n","s","e"],"the shallow water to your south you now stand on rocks and pebbles the rocks to your east open up into a cave that seems to lead deep underground and ahead on the waters edge by the end of the beach lies a great shipwreck","",[rock],[],[],False)
r60 = room(["n","s"],"on the other side of the air is hot and a dark smoke blooms in the sky, you start the great ascent to the peak of the volcanoe, the east and west both seem impassable as lave streams cut through the rock."," a Golem materialise from the ground and stands before you",[],[Golem],[],False)
r70 = room(["n"],"at the peak of your ascent before the bubbling crater of the volanoe you enter into the mountian into a vast chamber. an old sage peers into a wistfulOrb, it would be inhumane to kill them ","",[],[orb],[],False)
r63 = room(["n","e"],"u stand at the back of the castle. You can see a large window peering into the castle's courtroom","",[],[],[window],False)
r64 = room(["n","e","w"],"ur feet sink into the hot sand of the beach the catsle looms above you atop a hill to the northwest to the north rocky cliffs open up into a tunnel and to your west the beach continues","",[],[],[],False)
r66 = room(["e","n","w"],"trudging through the wet sand water sloshing against your legs",", you see a beuatiful woman holding a trident her lower half a scaly tail, her song lulls you towards her it feel impossible to resist or turn back",[fish],[mm],[],False)
r65 = room(["e","w"],"more beach,more sand. but as u watch it the sand seems to move"," you realise the ground is littered with pale bauge snakes",[sand],[snake,snake,snake,snake],[],False)
map = [[r00, r01, r02, None, None, None, None], 
       [r10, r11, r12, r13, r14, r15, r16], 
       [r20, r21, r22, r23, r24, r25, r26], 
       [r30, r31, r32, r33, r34, r35, None], 
       [None, r41, r42, r43, r44, r45, r46], 
       [r50, r51, None, r53, r54, r55, r56], 
       [r60, None, None, r63, r64, r65, r66],
       [r70]]
print(map)
#pickle.dump(map, open('mapDefault.pkl', 'wb'))
print('welocme to "jork", would u like to play,load game or view high scores')
running = True
while running == True:
    ans = input("play/load/scores/exit: ") # menu
    while ans != "play" and ans != "load" and ans != "scores" and ans != "exit": #menu validation restricted choice
        print("i dont understand that")
        ans = input("play/load/scores: ")
    if ans == "exit":
        running = False
    elif ans == "play" or ans == "load":
        if ans == "play":
            #map = pickle.load(open('./mapDefault.pkl', 'rb'))
            plyr = player(20,3,3,[],0,0)
            #pickle.dump(plyr, open('playerDefault.pkl', 'wb'))
            #plyr = pickle.load(open('./playerDefault.pkl', 'rb'))
            print("Instructions: ")
            print("In this game you can explore the map, collect/use items and fight monsters all through typing commands")
            print("your basic movement is 'go' succeded by .north/n,south/s,west/w and east/e', the rest is basic english, for a list fo command type 'info'")
            print("now that thats out the way, lets get started...")
            print("you awake in an unfamiliar landscape")
        else:
            map = pickle.load(open('./mapSave.pkl', 'rb'))
            plyr = pickle.load(open('./playerSave.pkl', 'rb'))
            print("you already know how the game works, rember info for a list fo commands if u forgot.")
        saved = False
        playing = True
        fleeDir = "0"
        while playing == True:
            curRoom = (map[plyr.getY()][plyr.getX()]) #set CurRoom variable to the room the player is in 
            if curRoom.getVisit() == False: #display description of room if player has just entered
                displayDesc()
                curRoom.setVisit(True)
            command = input("enter command: ")
            if command == "info":
                print("go (n,e,s,w), take, drop, read, consume, use, look, search, fight, stats, inventory(shows your items and attack values of weapons) and killself. many of which will be followed by an item or will prompt you for more inputs, and save game")
            elif command == "look": #redisplay room description 
                displayDesc()            
            elif command == "stats":
                print("score: " +str(plyr.getScore()))
                print("hp: " +str(plyr.getHp()))
                print("moves: "+str(plyr.getMoves()))
            elif command == "search": #display available item in that room
                if len(curRoom.getItems())>0:
                    print("u can see:")
                    for i in curRoom.getItems():
                        print("a " + i.getName())
                else:
                    print("nothing here homie")
            elif command == "inventory": #display contents of players inventory
                print(plyr.showInventory())
            elif command[:2] == "go": #vhnage the room the player is currently in
                if len(command) <= 3: # allows them to enter "go" and then the direction or "go direction"
                    direction = input("where: " )
                    direction = direction[0]
                else:
                    direction = (command[3]).lower()
                if curRoom.searchDir(direction) == True: #checks if chosen direction is available from that room
                    if doorCheck(curRoom,direction) == True: #checks if there is a "locked" "door" in that direction
                        print("there is a locked door in your way")
                    elif enemyBlockCheck(curRoom,direction):
                        print("an enemy blocks your way")
                    else: # moves player's x or y coordinate dependant on direction chosen
                        curRoom.setVisit(False)
                        match direction: # finds direction player is trying to go adn mvoes them to the new room by altering the coordinate
                            case "n":
                                plyr.setY(-1)
                                fleeDir = "s" #sets the value of the fleedirection so if a player chooses the flee option in combat they eill return to previous room
                            case "s":
                                plyr.setY(1)
                                fleeDir = "n"
                            case "e":
                                plyr.setX(1)
                                fleeDir = "w"
                            case "w":
                                plyr.setX(-1)
                                fleeDir = "e"
                else:
                    print("you cant go that way man")
            elif command[:4] == "take": #allows user to put an item into their inventory
                if plyr.getInvLen() == 10: #check if inventory is "full"
                    print("inventory full, drop an item if u want to pick something up")
                else: 
                    if len(command) <= 4: #allows for take then item or take item as input(s)
                        name = input("take what: ")
                    else:
                        name = command[5:] #sets a varibale to the item name form the user
                    items = curRoom.getItems()
                    if curRoom.search(name,items) == True: #checks if there is that item in the current room
                        Titem = curRoom.getObjectByName(name,"I")
                        plyr.addToInv(Titem,curRoom) #puts item into inventory and removes from room
                        print("you take the " + name + " and put it in your inventory")
                    else:
                        print("there isnt one of those here")
            elif command[:4] == "drop": #allows player to remove item from invenory and put in a room
                if len(command) == 4: #allows for "drop" then "item" or "drop item"
                    name = input("drop what: ")
                else:
                    name = command[5:] 
                if plyr.searchInv(name) == True: #same as take but opposite
                    Ditem = plyr.getItemByName(name)
                    plyr.removeFromInv(Ditem)
                    curRoom.addItem(Ditem)
                    print("you dropped the " + name + " on the ground")
                else:
                    print("u dont have one of those")
            elif command[:3] == "use": #allows players to use an item fro its purpose
                if len(command) <= 4: #allows for "use" then "item" or "use item"
                    name = input("use what: ")
                else:
                    name = command[4:] 
                if plyr.searchInv(name) == True: #checks player has that item
                    curItem = plyr.getItemByName(name) #gets the item from name given by user
                    if isinstance(curItem, key) and len(curRoom.getDoors()) != 0: #checks if item is a "key" and if applicable
                        for i in range(len(curRoom.getDoors())):
                            if curRoom.getDoors()[i].getID() == curItem.getDoorID(): 
                                curRoom.getDoors()[i].unLock() #unlocks the door sets locked atribute to false
                                if curRoom.getDoors()[i].getName() == "pedastel": #if key is a treasure and therefore door is actually a pedastel change the output
                                    print("the " + curItem.getName() + " was placed on the pedastel")
                                    plyr.incrementTcount()
                                    plyr.removeFromInv(curItem)
                                    if plyr.getTcount() == 5:
                                        print("the doors slowly open revealing the room behind")
                                else:    
                                    print("the " + curRoom.getDoors()[i].getName() + " was unlocked")
                            elif curRoom.getDoors()[i].getName() != "pedastel": #when in thron room stops repeated "thats the wrong" before finsing correct pedastel i.e. first placed trease was the orb system would output "wrong key" 3 times before saying the orb was palced on the pedastel
                                print("thats the wrong key")
                    else:
                        print("you cant use that here")
                else: 
                    print("you dont have one of those")
            elif command[:7] == "consume":
                if len(command) <= 7:
                    name = input("consume what: ")
                else:
                    name = command[8:]
                consume(name)
            elif command[:4] == "read": #allows players to read a message item
                if len(command) <= 5: #allows for "read" then "item" or "read item"
                    name = input("read what: ")
                else:
                    name = command[5:]
                if plyr.searchInv(name) == True: #checks player has that item
                    curItem = plyr.getItemByName(name) #gets the item from name given by user
                    if isinstance(curItem, message):
                        print("the " + curItem.getName() + " reads:")
                        print(curItem.getText()) #displays the messages message
                    else:
                        print("how are u gonna read that?")
                else:
                    print("you dont have one of those")            
            elif command == "killself": #option to end game
                check = input("you cant be serious, are you sure Y/N: ")
                if check == "Y" or check == "y":
                    name = input("with what: ") #takes weapon from user thye will use
                    if plyr.searchInv(name) == True:
                        curWep = plyr.getItemByName(name) #ret
                        if isinstance(curWep, weapon) == True or name == "banana": # check if given item is a weapon and below if its in inventory
                            print("you plunge the "+ name +" into your heart")
                            print("nice job, you are dead")
                            plyr.addHp(-10) #kills player
                            playing = False #end loop
                        else: 
                            print("an interesting idea, how...?")
                    else:
                        print("you dont have one of those")
                else:
                    print("you've got no balls man, do it")
            elif  command[:5] == "fight": #initiates fight function
                if len(command) <= 6: #allows for "enemy" then "item" or "fight enemey"
                    name = input("fight what: ") #get enemey from user
                else:
                    name = command[6:]
                enemies = curRoom.getEnemies()
                if curRoom.search(name,enemies) == True: #check if given enemy is present
                    wepName = input("with what: ")
                    if plyr.searchInv(wepName) == True:
                        curWep = plyr.getItemByName(wepName) #retrieve instance of weapon if the player has it
                        if isinstance(curWep, weapon) == True: #check if given item is  a weapon
                            curEnemy = curRoom.getObjectByName(name,"E")
                            fighting = True
                            turncount = 0
                            while fighting == True:
                                if plyr.getHp() <= 0: #checks if layer is alive
                                    print("YOU DIED")
                                    fighting = False # ends combat and game
                                    playing = False
                                elif curEnemy.getHp() <= 0: #checks if thhe enemy is dead
                                    print("enemy defeated")
                                    plyr.addScore(curEnemy.getScorePoints()) #give player score
                                    curEnemy.dropItems(curRoom) #add "drops" of the enemy to the room
                                    curRoom.removeEnemy(curEnemy) #remove instance of enemy from the room
                                    fighting = False # end combat
                                else:
                                    if turncount%2 == 0: #checks whos turn it is by seeing if turncount is even or odd
                                        decision = input("attack/heal/flee: ") #options whislt in combat
                                        while decision != "heal" and decision != "flee" and decision != "attack":
                                            decision = input("attack/heal/flee, 3 options: ")
                                        match decision:
                                            case "heal": #allows player to "consume" a food item
                                                name = input("consume what: ")
                                                if consume(name) == False:
                                                    print("you wasted your time failing to heal youself, u missed your chance")
                                            case "flee": #allows player to exit cobat and return to previous room
                                                fled = True
                                                match fleeDir: #operates similar to normal movement
                                                    case "0":
                                                        print("you have nowhere to flee to")
                                                        fled = False
                                                    case "n": 
                                                        plyr.setY(1)
                                                        fleeDir = "s"
                                                    case "s":
                                                        plyr.setY(-1)
                                                        fleeDir = "n"
                                                    case "e":
                                                        plyr.setX(1)
                                                        fleeDir = "w"
                                                    case "w":
                                                        plyr.setX(-1)
                                                        fleeDir = "e"
                                                if fled == True:
                                                    print("like a pathetic child you run away screaming right back the way you came")
                                                    curRoom.setVisit(False)
                                                    fighting = False
                                            case "attack":
                                                curEnemy.takeDmg(curWep.getAtk()) #apply damage of player to enemeies heakth
                                                if curEnemy.getHp() >= 0: #print result of attack
                                                    print("you attacked the {} dealing {} damage it's health is {}".format(curEnemy.getName(),curWep.getAtk(),curEnemy.getHp()))
                                                else:
                                                    print("you attacked the {} dealing {} damage it's health is 0".format(curEnemy.getName(),curWep.getAtk()))
                                    else:           
                                        plyr.addHp(-(curEnemy.getAtk())) #apply enemeies damage to player health
                                        if plyr.getHp() >= 0: #dispay result
                                            print("the {} attacked you dealing {} damage, your health is {}".format(curEnemy.getName(),curEnemy.getAtk(),plyr.getHp()))
                                        else:
                                            print("the {} attacked you dealing {} damage, your health is 0".format(curEnemy.getName(),curEnemy.getAtk()))
                                    turncount+=1
                        else:
                            print("how u gonna fight with that.")
                    else:
                        print("you dont have one of those")
                else:
                    print("there isnt one of those here")
            elif command == "save game":
                print("Note: this game utilises only one save file!")
                print("If u save now you will overwrite a previous save, do u wish to proceed?")
                proceed = input("Y/N: ") #checks if user wants to overwrite the save file
                if proceed == "Y" or proceed == "y":
                    pickle.dump(map, open('mapSave.pkl', 'wb')) #uploads game state to save file
                    pickle.dump(plyr, open('playerSave.pkl', 'wb')) #^
                    playing = False #end game
                    print("your game was saved")
                    saved = True #stops game ending text being displayed and sysytem uploading stats to database when game is exited
                else:
                    print("back to the task at hand then")
            elif command == "sit on throne":
                if curRoom.search("throne",curRoom.getItems()) == True:
                        print("you sit on the old iron throne built on the skulls of your enemies and take dominon of the land, your quest is complete")
                        playing = False
                else:
                    print("there is no throne here")       
            else: # command validation, loops if user enter somethign that isnt a command
                print("sorry i dont understand")
            plyr.incrementMoves()
        if saved == False: # if game has terminated not due to saving progress display the ending sequence
            print("game over...")
            print("score: "+ str(plyr.getScore())) #display score
            print("um good score... you can always play again!")
            initials = input("enter your initials to upload your score: ") #get users initials or name to idnetify score
            try:
                cursor = scores_db.cursor(prepared=True)
                cursor.execute("INSERT INTO scores (score,initials,moves) VALUES (%s,%s,%s)", (plyr.getScore(),initials,plyr.getMoves())) #uplaod users score moves and initials to the database
                scores_db.commit()
                print("score uploaded to db")
                cursor.close()
            except:
                print("there was an error uploading your score to the database")
    elif ans == "scores": #allwos user to view there own previous scores or top 10 scores
        choice = input("top 10 scores(top) or your own(mine): ")
        while choice != "top" and choice != "mine": #menu validation restricted choice
            print("i dont understand that")
            choice = input("top/mine: ")
        if choice == "top":
            cursor = scores_db.cursor(prepared=True)
            try:
                cursor.execute("SELECT initials, score, moves FROM scores ORDER BY score DESC limit 10") # execute the query to retrieve the top 10 scores
                scores_db.commit()
                myresult = cursor.fetchall() # retrieve the results of the query
                if myresult is None:    # check if the query returned any results
                    print("there are no scores")
                else:
                    for row  in myresult:         # iterate over the results
                        print("{}: scr:{}, mvs:{}".format(row[0],row[1],row[2]))
            except:
               print("there was an error in retrieving the data")
            cursor.close()
        else:
            cursor = scores_db.cursor(prepared=True)

            try:
                initials = input("enter initials or name inputed with your score: ") #gte the initials used to identify the users uploaded scores
                cursor.execute("SELECT initials, score, moves FROM scores WHERE initials=%s",(initials,))   # execute the query to retrieve the user's scores
                scores_db.commit()
                myresult2 = cursor.fetchall() # retrieve the results of the query
                if myresult2 is None:     # check if the query returned any results
                    print("you have no scores")
                else:
                    for row in myresult2:         # iterate over the results
                        print("{}: scr:{}, mvs:{}".format(row[0],row[1],row[2]))
            except:
                print("there was an error in retrieving the data")
            cursor.close()

print("Thanks for supporting 'jork'!:)") 
scores_db.close()