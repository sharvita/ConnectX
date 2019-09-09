##**************************************************************##
##
## Group 4: Engineering?
## Team Lead: Julia
## Members: Daniel, Kat, Sharvita
##
## Will play Connect 4 on any dimension >= 1x1 semi not stupidly.
## This version is not know for being elegant or algorithmic,
## it just plays Connect 4.  
##
##**************************************************************##


import random
import sys
import json

sys.stderr.write("Connect Four - Python\n")

# This is fragile and relies on the fact that the driver always passes the
# command line arguments in the order --player <p> --width <w> --height <h>.
player = int(sys.argv[2]) # --player <p>
width = int(sys.argv[4]) # --width <w>
height = int(sys.argv[6]) # --height <h>

sys.stderr.write("player = " + str(player) + '\n')
sys.stderr.write(" width = " + str(width) + '\n')
sys.stderr.write("height = " + str(height) + '\n')


def valid_moves(state):
    """Returns the valid moves for the state as a list of integers."""
    grid = state['grid']  #list of lists, the game board by columns starting upper left corner
    moves = []            #list of valid column moves
    offence = []          #list of moves that will win the game for us
    defence = []          #list of opponent moves that will win game
    ok = []               #list of moves that would be good to make
    meh = []              #list of so so moves
    connect = 4           #length of winning sequence
    #in theory we could have only one list, a list of tuples, first element in tuple could be
    #priority of move (1 for offence, 2 for defence, ...) and second element could be column
    #to move in.  After gathering all tuples of moves return column of highest priority.
    #If multiple tuples of equal highest priority found return column with highest frequency.
    #But I'm lazy so we're using multiple lists instead.  

    #If middle of bottom row is empty play there and return.
    #Useful for first or second move of game only.
    r = int(width/2)
    if grid[r][height-1] == 0:
        offence.append(r)
        return offence
    

    #These are the non-full columns, IE can accept a move.
    #At this point available columns/moves are equally weighted at 1.
    for i in range(width):
        if grid[i][0] == 0:
            moves.append(i)


    ##Checking if we received a full game board.  This should never happen
    ##but doesn't hurt to make sure.
    if len(moves) == 0:
        sys.stderr.write("CRITICAL ERROR: WE RECEIVED A FULL GAME BOARD!\n")
        sys.stderr.write("Graceful exit is playing column 0 and hoping ")
        sys.stderr.write("for the best.\n")
        offence.append(0)
        return offence


    #Who is player, who is opponent, and some useful sequences.
    if player == 1:
        opponent = 2
        good = '01010'
        good1 = '00110'
        good2 = '01100'
        bad = '02020'
        bad1 = '00220'
        bad2 = '02200'
    else:
        opponent = 1
        good = '02020'
        good1 = '02200'
        good2 = '00220'
        bad = '01010'
        bad1 = '01100'
        bad2 = '00110'
        
        
    #Vertical placement, cheap and easy and bulletproof
    #First three lines build strings to search for
    #for list in grid (for every column of the game board)
    #   convert column to string (so we can search column(string) for a sub-string)
    #   if statements to check if sub-string (what we built earlier) is inside string(column)
    vert_wn =  '0' + ''.join(str(player) for x in range(connect-1))
    vert_ls =  '0' + ''.join(str(opponent) for x in range(connect-1))
    vert_meh = '0' + ''.join(str(player) for x in range(connect-2))
    r = -1
    for list in grid:
        r += 1
        s = ''.join(str(x) for x in list)
        if vert_wn in s:     offence.append(r)
        elif vert_ls in s:   defence.append(r)
        elif vert_meh in s:  meh.append(r)
        
        
    #Horizontal and diagnol placement
    #The logic for horizontal and diagonal checking is almost identical.  I probably could have built a function
    #for handling these but due to subtle differences I'm not sure it would have made the code more compact.
    for x in range(width-connect+1):
        a = grid[x]                     #grab four columns
        b = grid[x+1]
        c = grid[x+2]
        d = grid[x+3]
        a_first_open = a.count(0) - 1   #find first open slot in those four columns
        b_first_open = b.count(0) - 1
        c_first_open = c.count(0) - 1
        d_first_open = d.count(0) - 1 
        for y in range(height):         #one row at a time, top to bottom
            hor = a[y:y+1] + b[y:y+1] + c[y:y+1] + d[y:y+1]         #list of four horizontal slots
            count = sum(hor)                                        #sum of list
            if opponent not in hor:                                 #if opponent not in the list
                if count == player*3:                                   #if we own three slots in list
                    if hor[0] == 0 and y == a_first_open:   offence.append(x)
                    elif hor[1] == 0 and y == b_first_open: offence.append(x+1)
                    elif hor[2] == 0 and y == c_first_open: offence.append(x+2)
                    elif hor[3] == 0 and y == d_first_open: offence.append(x+3)
                elif count == player*2:                                 #if we own two slots in list
                    if hor[0] == 0 and y == a_first_open:   meh.append(x)
                    if hor[1] == 0 and y == b_first_open:   meh.append(x+1)
                    if hor[2] == 0 and y == c_first_open:   meh.append(x+2)
                    if hor[3] == 0 and y == d_first_open:   meh.append(x+3)
            elif player not in hor and count == opponent*3:         #if we are not in list and opponent owns three slots, and the empty slot is highest zero in the column
                if hor[0] == 0 and y == a_first_open:       defence.append(x)
                elif hor[1] == 0 and y == b_first_open:     defence.append(x+1)
                elif hor[2] == 0 and y == c_first_open:     defence.append(x+2)
                elif hor[3] == 0 and y == d_first_open:     defence.append(x+3)
            if player not in hor and count == opponent*3:           #if we are not in list and opponent owns three slots, but space below open slot is empty and is highest opening, and is in moves already
                if hor[0] == 0 and y+1 == a_first_open and x in moves:     moves.remove(x)
                elif hor[1] == 0 and y+1 == b_first_open and x+1 in moves: moves.remove(x+1)
                elif hor[2] == 0 and y+1 == c_first_open and x+2 in moves: moves.remove(x+2)
                elif hor[3] == 0 and y+1 == d_first_open and x+3 in moves: moves.remove(x+3)                
            if y < height-connect+1: #diagnol checking below
                hor = a[y:y+1] + b[y+1:y+2] + c[y+2:y+3] + d[y+3:y+4]       #backslash diagonal list of four slots
                count = sum(hor)                                            #sum of list
                if opponent not in hor:                                     #if opponent not in the list
                    if count == player*3:                                       #if we own three slots in list
                        if hor[0] == 0 and y == a_first_open:     offence.append(x)
                        elif hor[1] == 0 and y+1 == b_first_open: offence.append(x+1)
                        elif hor[2] == 0 and y+2 == c_first_open: offence.append(x+2)
                        elif hor[3] == 0 and y+3 == d_first_open: offence.append(x+3)
                    elif count == player*2:                                     #if we own two slots in list
                        if hor[0] == 0 and y == a_first_open:     meh.append(x)
                        if hor[1] == 0 and y+1 == b_first_open:   meh.append(x+1)
                        if hor[2] == 0 and y+2 == c_first_open:   meh.append(x+2)
                        if hor[3] == 0 and y+3 == d_first_open:   meh.append(x+3)
                elif player not in hor and count == opponent*3:            #if we are not in list and opponent owns three slots, and the empty slot is highest zero in the column
                    if hor[0] == 0 and y == a_first_open:         defence.append(x)
                    elif hor[1] == 0 and y+1 == b_first_open:     defence.append(x+1)
                    elif hor[2] == 0 and y+2 == c_first_open:     defence.append(x+2)
                    elif hor[3] == 0 and y+3 == d_first_open:     defence.append(x+3)
                if player not in hor and count == opponent*3:              #if we are not in list and opponent owns three slots, but space below open slot is empty and is highest opening, and is in moves already
                    if hor[0] == 0 and y+1 == a_first_open and x in moves:     moves.remove(x)
                    elif hor[1] == 0 and y+2 == b_first_open and x+1 in moves: moves.remove(x+1)
                    elif hor[2] == 0 and y+3 == c_first_open and x+2 in moves: moves.remove(x+2)
                    elif hor[3] == 0 and y+4 == d_first_open and x+3 in moves: moves.remove(x+3)                    
                hor = a[y+3:y+4] + b[y+2:y+3] + c[y+1:y+2] + d[y:y+1]      #forwardslash diaganol list of four slots
                count = sum(hor)                                           #sum of list
                if opponent not in hor:                                    #if opponent not in the list
                    if count == player*3:                                       #if we own three slots in list
                        if hor[0] == 0 and y+3 == a_first_open:   offence.append(x)
                        elif hor[1] == 0 and y+2 == b_first_open: offence.append(x+1)
                        elif hor[2] == 0 and y+1 == c_first_open: offence.append(x+2)
                        elif hor[3] == 0 and y == d_first_open:   offence.append(x+3)
                    elif count == player*2:                                     #if we own two slots in list
                        if hor[0] == 0 and y+3 == a_first_open:   meh.append(x)
                        if hor[1] == 0 and y+2 == b_first_open:   meh.append(x+1)
                        if hor[2] == 0 and y+1 == c_first_open:   meh.append(x+2)
                        if hor[3] == 0 and y == d_first_open:     meh.append(x+3)
                elif player not in hor and count == opponent*3:         #if we are not in list and opponent owns three slots, and the empty slot is highest zero in the column
                    if hor[0] == 0 and y+3 == a_first_open:       defence.append(x)
                    elif hor[1] == 0 and y+2 == b_first_open:     defence.append(x+1)
                    elif hor[2] == 0 and y+1 == c_first_open:     defence.append(x+2)
                    elif hor[3] == 0 and y == d_first_open:       defence.append(x+3)
                if player not in hor and count == opponent*3:           #if we are not in list and opponent owns three slots, but space below open slot is empty and is highest opening, and is in moves already
                    if hor[0] == 0 and y+4 == a_first_open and x in moves:     moves.remove(x)
                    elif hor[1] == 0 and y+3 == b_first_open and x+1 in moves: moves.remove(x+1)
                    elif hor[2] == 0 and y+2 == c_first_open and x+2 in moves: moves.remove(x+2)
                    elif hor[3] == 0 and y+1 == d_first_open and x+3 in moves: moves.remove(x+3)
                
                    
    #For handling sequences that can guarantee victory/defeat in two moves.  Horizontal only.
    #01010 02020 00110 01100 02200 or 00220 on the horizontal.  This works but assumes row
    #beneath is adequately populated, not the best but checking if in moves[] helps.
    #Needs verification that 5 slots beneath the 5 we're looking at are non zero.
    transpose = zip(*grid)
    for list in transpose:
        s = ''.join(str(y) for y in list)
        if good in s:
            x = s.find(good)
            x+=2
            sys.stderr.write("found " + good + " at " + str(x) + "\n")
            if x in moves:
                ok.append(x)
        elif good1 in s:
            x = s.find(good1)
            x+=1
            sys.stderr.write("found " + good1 + " at " + str(x) + "\n")
            if x in moves:
                ok.append(x)
        elif good2 in s:
            x = s.find(good2)
            x+=3
            sys.stderr.write("found " + good2 + " at " + str(x) + "\n")
            if x in moves:
                ok.append(x)
        elif bad in s: 
            x = s.find(bad)
            x+=2
            sys.stderr.write("found " + bad + " at " + str(x) + "\n")
            if x in moves:
                ok.append(x)
        elif bad1 in s:
            x = s.find(bad1)
            x+=1
            sys.stderr.write("found " + bad1 + " at " + str(x) + "\n")
            if x in moves:
                ok.append(x)
        elif bad2 in s: 
            x = s.find(bad2)
            x+=3
            sys.stderr.write("found " + bad2 + " at " + str(x) + "\n")
            if x in moves:
                ok.append(x)


    #Need to clean up meh, might contain opponent setup moves since we've been removing moves in a weird order
    for x in meh:
        if x not in moves:
            meh.remove(x)


    #Time to return a move
    if len(offence) > 0:
        sys.stderr.write("playing offence\n")
        return offence
    elif len(defence) > 0:
        if len(defence) > 1:
            sys.stderr.write("multiple opponent winning moves, no bueno, recommend returning illegal move to crash game\n")
        sys.stderr.write("playing defence\n")
        return defence
    elif len(ok) > 0:
        sys.stderr.write("playing ok\n")
        return ok
    elif len(meh) > 0:
        #select the best (highest frequency) meh move, this method can make gameplay lean to the right
        most = 1
        for x in meh:
            if meh.count(x) >= most:
                most = meh.count(x)
                c = x
        meh.clear()
        meh.append(c)
        sys.stderr.write("playing meh\n")
        return meh
    elif len(moves) > 0:
        sys.stderr.write("playing almost random, tried not to make a bad move\n")
        return moves

    #Verified this needs to be here.  If moves list is empty then all open slots are good
    #setup moves for opponent, no good choices, so just make a random one
    sys.stderr.write("playing random, wouldnt be surprised if opponent wins on next move\n")
    for i in range(width):
        if grid[i][0] == 0:
            moves.append(i)
    return moves

    
# Loop reading the state from the driver and writing a random valid move.
for line in sys.stdin:
    sys.stderr.write(line)
    state = json.loads(line)
    action = {}
    action['move'] = random.choice(valid_moves(state))
    msg = json.dumps(action)
    sys.stderr.write(msg + '\n')
    sys.stdout.write(msg + '\n')
    sys.stdout.flush()


# Be a nice program and close the ports.
sys.stdin.close()
sys.stdout.close()
sys.stderr.close()
