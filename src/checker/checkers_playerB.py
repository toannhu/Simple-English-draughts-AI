# ======================== Class Player =======================================
import copy
import string

DEPTH_LIMIT = 5

# wrapper for alpha-beta info
# v = [move_value, move, max tree depth, # child nodes, # max/beta cutoff, # min/alpha cutoff]
class AB_Value:
    def __init__(self, move_value, move, max_depth, child_nodes, max_cutoff, min_cutoff):
        self.move_value = move_value
        self.move = move
        self.max_depth = max_depth
        self.nodes = child_nodes
        self.max_cutoff = max_cutoff
        self.min_cutoff = min_cutoff

class Move:
    def __init__(self, start, end, jump=False):
            self.start = start
            self.end = end
            self.jump = jump 
            self.jumpOver = [] 
            
class Player:
    def __init__(self, str_name):
        self.str = str_name

    def __str__(self):
        return self.str

    move = []
    
    # Student MUST implement this function
    # The return value should be a move that is denoted by a list of tuples
    def nextMove(self, state): 
        legal = self.calcLegalMoves(state)
        #print(legal)
        if (len(legal)>0):
            # no need for AI if there's only one choice
            if (len(legal)==1):
                choice = legal[0]
                if (isinstance(choice, Move)):
                    return [choice.start,choice.end]
                else:
                    return choice
            else:
                choice = self.alpha_beta(state)
                if ((len(choice) == 0) or (choice is None)):
                    choice = random.randint(0,len(legal)-1)  
                    choice = legal[choice]           
                    return choice
                else:
                    if (isinstance(choice, Move)):
                        return [choice.start,choice.end]
                    else:
                        return choice
                    
        '''
        result = [(2,2),(7,0)]
        actions = self.calcLegalMoves(state)
        for a in actions:
            if (isinstance(a, Move)):
                print(a.jumpOver)
            else:
                print("None")
        return result
    

        
        #result = None
        #state[4][1] = 'b'
        #print(self.calcPos(state))
        print(self.calcLegalMoves(state))
        #print("This is a: ",self.checkOpponent(self.str))
        self.evaluation_function(state)
        return result
        '''
        
    def calcPos(self, state, player):
        pos = []
        for row in range (8):
            for col in range(8):
                if (state[row][col] == player or state[row][col] == player.upper()):
                    pos.append((row,col))
        return pos
    
    def checkOpponent(self, str):
        opponent = "r" if (str == "b") else "b"
        return opponent
    
    def calcLegalMoves(self, state):
        legalMoves = []
        hasJumps = False
        #boardLimit = 0 if player == 0 else BOARD_SIZE-1
        # cell refers to a position tuple (row, col)
        opponent = self.checkOpponent(self.str)
        player = "r" if (opponent == "b") else "b"
        pos = self.calcPos(state,player)
        opponent = self.checkOpponent(self.str)
        player = "r" if (opponent == "b") else "b"
        boardLimit = 0 if player == 'r' else 7
        if (player == "b"):           
            for cell in pos:
                if (state[cell[0]][cell[1]].islower()):
                    #if (cell[0] == boardLimit):
                        #continue
                    if (cell[1] != 7):
                        if (state[cell[0]+1][cell[1]+1] == "." and not hasJumps): #dao nguoc lai? #quan King di dc 4 huong?
                            result = [(cell[0],cell[1]),(cell[0]+1,cell[1]+1)]
                            legalMoves.append(result)
                        # has enemy, can jump it?
                        elif(state[cell[0]+1][cell[1]+1] == opponent):
                            jumps = self.checkJump(state,(cell[0],cell[1]), False)
                            if (len(jumps)!=0):
                                # if first jump, clear out regular moves
                                if not hasJumps:
                                    hasJumps = True
                                    legalMoves = []
                                legalMoves.extend(jumps)
                    # diagonal left, only search if not at left edge of board
                    if (cell[1]!=0):
                        if(state[cell[0]+1][cell[1]-1] == '.' and not hasJumps):
                            result = (cell[0],cell[1]),(cell[0]+1,cell[1]-1)
                            legalMoves.append(result)                    
                        elif(state[cell[0]+1][cell[1]-1] == opponent):
                            jumps = self.checkJump(state,(cell[0],cell[1]), True)
                            if (len(jumps)!=0):
                                if not hasJumps:
                                    hasJumps = True
                                    legalMoves = []                        
                                legalMoves.extend(jumps)
                else: #check King moves?
                    #if (cell[0] == 0 or cell[0] == 7):
                        #continue
                    if (cell[1] != 7):
                        if (state[cell[0]+1][cell[1]+1] == "." and not hasJumps):
                            result = [(cell[0],cell[1]),(cell[0]+1,cell[1]+1)]
                            legalMoves.append(result)
                        # has enemy, can jump it?
                        elif (state[cell[0]+1][cell[1]+1] == opponent):
                            jumps = self.checkKingJump(state,(cell[0],cell[1]), False)
                            if (len(jumps)!=0):
                                # if first jump, clear out regular moves
                                if not hasJumps:
                                    hasJumps = True
                                    legalMoves = []
                                legalMoves.extend(jumps)
                                
                        if (state[cell[0]-1][cell[1]+1] == "." and not hasJumps):
                            result = [(cell[0],cell[1]),(cell[0]-1,cell[1]+1)]
                            legalMoves.append(result)        
                        # has enemy, can jump it?        
                        elif (state[cell[0]-1][cell[1]+1] == opponent):
                            jumps = self.checkKingJump(state,(cell[0],cell[1]), False)
                            if (len(jumps)!=0):
                                # if first jump, clear out regular moves
                                if not hasJumps:
                                    hasJumps = True
                                    legalMoves = []
                                legalMoves.extend(jumps)
                    # diagonal left, only search if not at left edge of board
                    if (cell[1]!=0):
                        if (state[cell[0]+1][cell[1]-1] == '.' and not hasJumps):
                            result = (cell[0],cell[1]),(cell[0]+1,cell[1]-1)
                            legalMoves.append(result)
                        elif (state[cell[0]+1][cell[1]-1] == opponent):
                            jumps = self.checkKingJump(state,(cell[0],cell[1]), True)
                            if (len(jumps)!=0):
                                if not hasJumps:
                                    hasJumps = True
                                    legalMoves = []                        
                                legalMoves.extend(jumps)         
                        
                        if (state[cell[0]-1][cell[1]-1] == '.' and not hasJumps):
                            result = (cell[0],cell[1]),(cell[0]-1,cell[1]-1)
                            legalMoves.append(result)
                        elif (state[cell[0]-1][cell[1]-1] == opponent):
                            jumps = self.checkKingJump(state,(cell[0],cell[1]), True)
                            if (len(jumps)!=0):
                                if not hasJumps:
                                    hasJumps = True
                                    legalMoves = []                        
                                legalMoves.extend(jumps)
        else:          
            for cell in pos:
                if (state[cell[0]][cell[1]].islower()):
                    #if (cell[0] == boardLimit):
                        #continue
                    if (cell[1] != 0):
                        if (state[cell[0]-1][cell[1]-1] == "." and not hasJumps):
                            result = [(cell[0],cell[1]),(cell[0]-1,cell[1]-1)]
                            legalMoves.append(result)
                        # has enemy, can jump it?
                        elif(state[cell[0]-1][cell[1]-1] == opponent):
                            jumps = self.checkJump(state,(cell[0],cell[1]), False)
                            if (len(jumps)!=0):
                                # if first jump, clear out regular moves
                                if not hasJumps:
                                    hasJumps = True
                                    legalMoves = []
                                legalMoves.extend(jumps)
                    # diagonal right, only search if not at right edge of board
                    if (cell[1] != 7):
                        if(state[cell[0]-1][cell[1]+1] == '.' and not hasJumps):
                            result = (cell[0],cell[1]),(cell[0]-1,cell[1]+1)
                            legalMoves.append(result)                    
                        elif(state[cell[0]-1][cell[1]+1] == opponent):
                            jumps = self.checkJump(state,(cell[0],cell[1]), True)
                            if (len(jumps)!=0):
                                if not hasJumps:
                                    hasJumps = True
                                    legalMoves = []                        
                                legalMoves.extend(jumps)
                else:
                    #if (cell[0] == 0 or cell[0] == 7):
                        #continue
                    if (cell[1] != 0):
                        if (state[cell[0]-1][cell[1]-1] == "." and not hasJumps):
                            result = [(cell[0],cell[1]),(cell[0]-1,cell[1]-1)]
                            legalMoves.append(result)
                        # has enemy, can jump it?
                        elif(state[cell[0]-1][cell[1]-1] == opponent):
                            jumps = self.checkKingJump(state,(cell[0],cell[1]), False)
                            if (len(jumps)!=0):
                                # if first jump, clear out regular moves
                                if not hasJumps:
                                    hasJumps = True
                                    legalMoves = []
                                legalMoves.extend(jumps)
                                
                        if (state[cell[0]+1][cell[1]-1] == "." and not hasJumps):
                            result = [(cell[0],cell[1]),(cell[0]+1,cell[1]-1)]
                            legalMoves.append(result)
                        # has enemy, can jump it?
                        elif(state[cell[0]+1][cell[1]-1] == opponent):
                            jumps = self.checkKingJump(state,(cell[0],cell[1]), False)
                            if (len(jumps)!=0):
                                # if first jump, clear out regular moves
                                if not hasJumps:
                                    hasJumps = True
                                    legalMoves = []
                                legalMoves.extend(jumps)
                    # diagonal right, only search if not at right edge of board
                    if (cell[1] != 7):
                        if(state[cell[0]-1][cell[1]+1] == '.' and not hasJumps):
                            result = (cell[0],cell[1]),(cell[0]-1,cell[1]+1)
                            legalMoves.append(result)                    
                        elif(state[cell[0]-1][cell[1]+1] == opponent):
                            jumps = self.checkKingJump(state,(cell[0],cell[1]), True)
                            if (len(jumps)!=0):
                                if not hasJumps:
                                    hasJumps = True
                                    legalMoves = []                        
                                legalMoves.extend(jumps)
                                
                        if(state[cell[0]+1][cell[1]+1] == '.' and not hasJumps):
                            result = (cell[0],cell[1]),(cell[0]+1,cell[1]+1)
                            legalMoves.append(result)                    
                        elif(state[cell[0]+1][cell[1]+1] == opponent):
                            jumps = self.checkKingJump(state,(cell[0],cell[1]), True)
                            if (len(jumps)!=0):
                                if not hasJumps:
                                    hasJumps = True
                                    legalMoves = []                        
                                legalMoves.extend(jumps)
        return legalMoves
    
    
    # enemy is the square we plan to jump over
    # change later to deal with double jumps
    def checkJump(self, state, cell, isLeft):
        jumps = []
        # check boundaries!
        if (cell[0]-1 == 0 or cell[0]+1 == 7):
            return jumps
        #check top left
        opponent = self.checkOpponent(self.str)
        player = "r" if (opponent == "b") else "b"
        if (player == "b"):
            
            if (isLeft):
                if (cell[1]>1 and state[cell[0]+2][cell[1]-2] == "."):
                    temp = Move(cell, (cell[0]+2, cell[1]-2), True)
                    temp.jumpOver = [(cell[0]+1,cell[1]-1)]
                    # can has double jump  
                    if (temp.end[0]-1 > 0 and temp.end[0]+1 < 7):
                        #enemy in top left of new square?
                        if (temp.end[1] > 1 and state[temp.end[0]+1][temp.end[1]-1] == opponent):
                            test = self.checkJump(state,temp.end,True)
                            if (test != []):
                                dbl_temp = copy.deepcopy(temp) #deepcopy needed?
                                dbl_temp.end = test[0].end 
                                dbl_temp.jumpOver.extend(test[0].jumpOver)
                                jumps.append(dbl_temp)              
                        # top right  
                        if (temp.end[1] < 6 and state[temp.end[0]+1][temp.end[1]+1] == opponent):
                            test = self.checkJump(state,temp.end,False)                	
                            if (test != []):
                                dbl_temp = copy.deepcopy(temp) #deepcopy needed?
                                dbl_temp.end = test[0].end 
                                dbl_temp.jumpOver.extend(test[0].jumpOver)
                                jumps.append(dbl_temp)                 
                    jumps.append(temp)

            else:
            #check top right
                if (cell[1] < 6 and state[cell[0]+2][cell[1]+2] == "."):
                    temp = Move(cell, (cell[0]+2, cell[1]+2), True)
                    temp.jumpOver = [(cell[0]+1,cell[1]+1)]
                    # can has double jump?
                    if (temp.end[0]+1 > 0 and temp.end[0]+1 < 7):
                        #enemy in top left of new square?
                        if (temp.end[1] > 1 and state[temp.end[0]+1][temp.end[1]-1] == opponent):
                            test = self.checkJump(state,temp.end,True);
                            if (test != []):
                                dbl_temp = copy.deepcopy(temp) #deepcopy needed?
                                dbl_temp.end = test[0].end 
                                dbl_temp.jumpOver.extend(test[0].jumpOver)
                                jumps.append(dbl_temp)                 			

                        # top right?
                        if (temp.end[1]<6 and state[temp.end[0]+1][temp.end[1]+1] == opponent):
                            test = self.checkJump(state,temp.end, False) 
                            if (test != []):
                                dbl_temp = copy.deepcopy(temp) #deepcopy needed?
                                dbl_temp.end = test[0].end 
                                dbl_temp.jumpOver.extend(test[0].jumpOver)
                                jumps.append(dbl_temp)
                    jumps.append(temp)     
        else:
            if (isLeft):
                if (cell[1]>1 and state[cell[0]-2][cell[1]-2] == "."):
                    temp = Move(cell, (cell[0]-2, cell[1]-2), True)
                    temp.jumpOver = [(cell[0]-1,cell[1]-1)]
                    # can has double jump  
                    if (temp.end[0]-1 > 0 and temp.end[0]+1 < 7):
                        #enemy in top left of new square?
                        if (temp.end[1] > 1 and state[temp.end[0]-1][temp.end[1]-1] == opponent):
                            test = self.checkJump(state,temp.end,True)
                            if (test != []):
                                dbl_temp = copy.deepcopy(temp) #deepcopy needed?
                                dbl_temp.end = test[0].end 
                                dbl_temp.jumpOver.extend(test[0].jumpOver)
                                jumps.append(dbl_temp)              
                        # top right  
                        if (temp.end[1] < 6 and state[temp.end[0]-1][temp.end[1]+1] == opponent):
                            test = self.checkJump(state,temp.end,False)                	
                            if (test != []):
                                dbl_temp = copy.deepcopy(temp) #deepcopy needed?
                                dbl_temp.end = test[0].end 
                                dbl_temp.jumpOver.extend(test[0].jumpOver)
                                jumps.append(dbl_temp)                 
                    jumps.append(temp)

            else:
            #check top right
                if (cell[1] < 6 and state[cell[0]-2][cell[1]+2] == "."):
                    temp = Move(cell, (cell[0]-2, cell[1]+2), True)
                    temp.jumpOver = [(cell[0]-1,cell[1]+1)]
                    # can has double jump?
                    if (temp.end[0]+1 > 0 and temp.end[0]+1 < 7):
                        #enemy in top left of new square?
                        if (temp.end[1] > 1 and state[temp.end[0]-1][temp.end[1]-1] == opponent):
                            test = self.checkKingJump(state,temp.end,True);
                            if (test != []):
                                dbl_temp = copy.deepcopy(temp) #deepcopy needed?
                                dbl_temp.end = test[0].end 
                                dbl_temp.jumpOver.extend(test[0].jumpOver)
                                jumps.append(dbl_temp)                 			

                        # top right?
                        if (temp.end[1]<6 and state[temp.end[0]-1][temp.end[1]+1] == opponent):
                            test = self.checkKingJump(state,temp.end, False) 
                            if (test != []):
                                dbl_temp = copy.deepcopy(temp) #deepcopy needed?
                                dbl_temp.end = test[0].end 
                                dbl_temp.jumpOver.extend(test[0].jumpOver)
                                jumps.append(dbl_temp)
                    jumps.append(temp)
        '''        
        print("Jumps:")
        for mov in jumps:
            print(str(mov.start)+" "+str(mov.end)+" Jump over: "+str(mov.jumpOver))
        '''
        return jumps

    def checkKingJump(self, state, cell, isLeft):
        jumps = []
        opponent = self.checkOpponent(self.str)
        # check boundaries!
        #if (cell[0]-1 == 0 or cell[0]+1 == 7):
            #return jumps
        #check top left
        if (isLeft):
            if (cell[1]>1 and cell[1]<6 and state[cell[0]+2][cell[1]-2] == "."):
                temp = Move(cell, (cell[0]+2, cell[1]-2), True)
                temp.jumpOver = [(cell[0]+1,cell[1]-1)]
                # can has double jump  
                if (temp.end[0]-1 > 0 and temp.end[0]+1 < 7):
                    #enemy in top left of new square?
                    if (temp.end[1] > 1 and state[temp.end[0]+1][temp.end[1]-1] == opponent):
                        test = self.checkKingJump(state,temp.end,True)
                        if (test != []):
                            dbl_temp = copy.deepcopy(temp) #deepcopy needed?
                            dbl_temp.end = test[0].end 
                            dbl_temp.jumpOver.extend(test[0].jumpOver)
                            jumps.append(dbl_temp)              
                    # top right  
                    if (temp.end[1] < 6 and state[temp.end[0]+1][temp.end[1]+1] == opponent):
                        test = self.checkKingJump(state,temp.end,False)                	
                        if (test != []):
                            dbl_temp = copy.deepcopy(temp) #deepcopy needed?
                            dbl_temp.end = test[0].end 
                            dbl_temp.jumpOver.extend(test[0].jumpOver)
                            jumps.append(dbl_temp)                 
                jumps.append(temp)
                
            if (cell[1]>1 and cell[1]<6 and state[cell[0]-2][cell[1]-2] == "."):
                temp = Move(cell, (cell[0]-2, cell[1]-2), True)
                temp.jumpOver = [(cell[0]-1,cell[1]-1)]
                # can has double jump  
                if (temp.end[0]-1 > 0 and temp.end[0]+1 < 7):
                    #enemy in top left of new square?
                    if (temp.end[1] > 1 and state[temp.end[0]-1][temp.end[1]-1] == opponent):
                        test = self.checkKingJump(state,temp.end,True)
                        if (test != []):
                            dbl_temp = copy.deepcopy(temp) #deepcopy needed?
                            dbl_temp.end = test[0].end 
                            dbl_temp.jumpOver.extend(test[0].jumpOver)
                            jumps.append(dbl_temp)              
                    # top right  
                    if (temp.end[1] < 6 and state[temp.end[0]-1][temp.end[1]+1] == opponent):
                        test = self.checkKingJump(state,temp.end,False)                	
                        if (test != []):
                            dbl_temp = copy.deepcopy(temp) #deepcopy needed?
                            dbl_temp.end = test[0].end 
                            dbl_temp.jumpOver.extend(test[0].jumpOver)
                            jumps.append(dbl_temp)                 
                jumps.append(temp)

        else:
        #check top right
            if (cell[1] < 6 and cell[1]>1 and state[cell[0]+2][cell[1]+2] == "."):
                temp = Move(cell, (cell[0]+2, cell[1]+2), True)
                temp.jumpOver = [(cell[0]+1,cell[1]+1)]
                # can has double jump?
                if (temp.end[0]+1 > 0 and temp.end[0]+1 < 7):
                    #enemy in top left of new square?
                    if (temp.end[1] > 1 and state[temp.end[0]+1][temp.end[1]-1] == opponent):
                        test = self.checkKingJump(state,temp.end,True);
                        if (test != []):
                            dbl_temp = copy.deepcopy(temp) #deepcopy needed?
                            dbl_temp.end = test[0].end 
                            dbl_temp.jumpOver.extend(test[0].jumpOver)
                            jumps.append(dbl_temp)                 			

                    # top right?
                    if (temp.end[1]<6 and state[temp.end[0]+1][temp.end[1]+1] == opponent):
                        test = self.checkKingJump(state,temp.end, False) 
                        if (test != []):
                            dbl_temp = copy.deepcopy(temp) #deepcopy needed?
                            dbl_temp.end = test[0].end 
                            dbl_temp.jumpOver.extend(test[0].jumpOver)
                            jumps.append(dbl_temp)
                jumps.append(temp)     
            #check top right
            if (cell[1] < 6 and cell[1]>1 and state[cell[0]-2][cell[1]+2] == "."):
                temp = Move(cell, (cell[0]-2, cell[1]+2), True)
                temp.jumpOver = [(cell[0]-1,cell[1]+1)]
                # can has double jump?
                if (temp.end[0]+1 > 0 and temp.end[0]+1 < 7):
                    #enemy in top left of new square?
                    if (temp.end[1] > 1 and state[temp.end[0]-1][temp.end[1]-1] == opponent):
                        test = self.checkKingJump(state,temp.end,True);
                        if (test != []):
                            dbl_temp = copy.deepcopy(temp) #deepcopy needed?
                            dbl_temp.end = test[0].end 
                            dbl_temp.jumpOver.extend(test[0].jumpOver)
                            jumps.append(dbl_temp)                 			

                    # top right?
                    if (temp.end[1]<6 and state[temp.end[0]-1][temp.end[1]+1] == opponent):
                        test = self.checkKingJump(state,temp.end, False) 
                        if (test != []):
                            dbl_temp = copy.deepcopy(temp) #deepcopy needed?
                            dbl_temp.end = test[0].end 
                            dbl_temp.jumpOver.extend(test[0].jumpOver)
                            jumps.append(dbl_temp)
                jumps.append(temp)
        '''        
        print("Jumps:")
        for mov in jumps:
            print(str(mov.start)+" "+str(mov.end)+" Jump over: "+str(mov.jumpOver))
        '''
        return jumps


    def evaluation_function(self, state):
        player_far, player_home_half, player_opp_half = 0,0,0
        opponent_far, opponent_home_half, opponent_opp_half = 0,0,0 
        opponent = self.checkOpponent(self.str)
        player = "r" if (opponent == "b") else "b"
        if (player == "b"):
            # player pieces
            player_pos = self.calcPos(state,player)
            for cell in player_pos:
                # player pieces at end of board
                if (cell[0] == 7 or state[cell[0]][cell[1]] == "B"):
                    player_far += 1
                # player pieces in opponents end
                # change to "print 'yes' if 0 < x < 0.5 else 'no'"
                elif (3 <= cell[0] < 7):
                    player_opp_half += 1
                else:
                    player_home_half += 1             

            # opponent pieces
            opponent_pos = self.calcPos(state,opponent)
            for cell in opponent_pos:    
                # opp pieces at end of board 
                if (cell[0] == 0 or state[cell[0]][cell[1]] == "R"):
                    opponent_far += 1
                # opp pieces not at own end
                elif (1 <= cell[0] < 5):
                    opponent_opp_half += 1
                else:
                    opponent_home_half += 1
        else:
            # player pieces
            player_pos = self.calcPos(state,player)
            for cell in player_pos:
                # player pieces at end of board
                if (cell[0] == 0 or state[cell[0]][cell[1]] == "B"):
                    player_far += 1
                # player pieces in opponents end
                # change to "print 'yes' if 0 < x < 0.5 else 'no'"
                elif (1 <= cell[0] < 4):
                    player_opp_half += 1
                else:
                    player_home_half += 1             

            # opponent pieces
            opponent_pos = self.calcPos(state,opponent)
            for cell in opponent_pos:    
                # opp pieces at end of board 
                if (cell[0] == 7 or state[cell[0]][cell[1]] == "R"):
                    opponent_far += 1
                # opp pieces not at own end
                elif (3 <= cell[0] < 7):
                    opponent_opp_half += 1
                else:
                    opponent_home_half += 1
        player_score = (7 * player_far) + (5 * player_opp_half)+ (3 * player_home_half)
        opponent_score = (7 * opponent_far) + (5 * opponent_opp_half)+ (3 * opponent_home_half)
        #print("Player Score: ",player_score)
        #print("Opponent Score: ",opponent_score)
        return (player_score - opponent_score)   
      
    
    #calculates the final score for the board
    def calcScore(self, state):
        score = [0,0]
        opponent = self.checkOpponent(self.str)
        player = "r" if (opponent == "b") else "b"
        if (player == "b"):
            #player pieces
            player_pos = self.calcPos(state,player)
            for cell in player_pos:
                #player pieces at end of board - 2 pts
                if (cell[0] == 7 or state[cell[0]][cell[1]] == "B"):
                    score[0] += 2
                #player pieces not at end - 1 pt
                else:
                    score[0] += 1
                
            #opponent pieces
            opponent_pos = self.calcPos(state,opponent)
            for cell in opponent_pos:
                #opponent pieces at end of board - 2 pts
                if (cell[0] == 0 or state[cell[0]][cell[1]] == "R"):
                    score[1] += 2
                #opponent pieces not at end - 1 pt
                else:
                    score[1] += 1
        else:
            #player pieces
            player_pos = self.calcPos(state,player)
            for cell in player_pos:
                #player pieces at end of board - 2 pts
                if (cell[0] == 0 or state[cell[0]][cell[1]] == "R"):
                    score[0] += 2
                #player pieces not at end - 1 pt
                else:
                    score[0] += 1
                
            #opponent pieces
            opponent_pos = self.calcPos(state,opponent)
            for cell in opponent_pos:
                #opponent pieces at end of board - 2 pts
                if (cell[0] == 7 or state[cell[0]][cell[1]] == "B"):
                    score[1] += 2
                #opponent pieces not at end - 1 pt
                else:
                    score[1] += 1
        return score

    
    # returns max value and action associated with value
    def max_value(self, state, alpha, beta, node):
        # if terminalTest(state)
        opponent = self.checkOpponent(self.str)
        player = "r" if (opponent == "b") else "b"
        actions = self.calcLegalMoves(state)
        num_act = len(actions)
        # v <- -inf
        # self, move_value, move, max_depth, total_nodes, max_cutoff, min_cutoff
        v = AB_Value(-999, None, node, 1, 0, 0)
        # depth cutoff
        if (node == DEPTH_LIMIT):
            v.move_value = self.evaluation_function(state)
            # print("Depth Cutoff. Eval value: "+str(v.move_value))
            return v      
        if (len(actions) == 0):
            score = self.calcScore(state)
            if (score[0] > score[1]):
                v.move_value = 100 + (2*score[0]-score[1])
                # print("(max) Terminal Node Score: "+str(v.move_value))
            else:
                v.move_value = -100 + (2*score[0]-score[1])
                # print("(max) Terminal Node Score: "+str(v.move_value))            
            return v
    
        for a in actions:
            newState = copy.deepcopy(state)
            # RESULT(s,a)
            if (isinstance(a, Move)):
                self.player_pos = self.calcPos(state,player)
                self.opponent_pos = self.calcPos(state,opponent)
            new_v = self.min_value(newState, alpha, beta, node+1)
            # compute new values for nodes and cutoffs in recursion
            if (new_v.max_depth > v.max_depth):
                v.max_depth = new_v.max_depth         
            v.nodes += new_v.nodes
            v.max_cutoff += new_v.max_cutoff
            v.min_cutoff += new_v.min_cutoff
            # v <- Max(v, MIN_VALUE(RESULT(s,a), alpha, beta))
            if (new_v.move_value > v.move_value):
               v.move_value = new_v.move_value
               v.move = a
            if (v.move_value >= beta):
               v.max_cutoff += 1
               return v
            if (v.move_value > alpha):
               alpha = v.move_value
        return v
    
    # returns min value
    def min_value(self, state, alpha, beta, node):
        #if terminalTest(state)
        opponent = self.checkOpponent(self.str)
        player = "r" if (opponent == "b") else "b"
        actions = self.calcLegalMoves(state)
        num_act = len(actions)
        # v <- inf
        # self, move_value, move, max_depth, total_nodes, max_cutoff, min_cutoff
        v = AB_Value(999, None, node, 1, 0, 0)
        # depth cutoff
        if (node == DEPTH_LIMIT):
            v.move_value = self.evaluation_function(state)
            #print("Depth Cutoff. Eval value: "+str(v.move_value))
            return v
        if (len(actions)==0):
            # return Utility(state)
            score = self.calcScore(state)
            if (score[0] > score[1]):
                v.move_value = 100 + (2*score[0]-score[1])
                #print("(min) Terminal Node Score: "+str(v.move_value))            
            else:
                v.move_value = -100 + (2*score[0]-score[1])
                #print("(min) Terminal Node Score: "+str(v.move_value))
            return v     
        for a in actions:
            newState = copy.deepcopy(state)
            # RESULT(s,a)
            if (isinstance(a, Move)):
                self.player_pos = self.calcPos(state,player)
                self.opponent_pos = self.calcPos(state,opponent)
            new_v = self.max_value(newState, alpha, beta, node+1)
            #compute new values for nodes and cutoffs in recursion
            if (new_v.max_depth > v.max_depth):
                v.max_depth = new_v.max_depth
            v.nodes += new_v.nodes
            v.max_cutoff += new_v.max_cutoff
            v.min_cutoff += new_v.min_cutoff
            # v <- Min(v, MAX_VALUE(RESULT(s,a), alpha, beta))
            if (new_v.move_value < v.move_value):
                v.move_value = new_v.move_value
                v.move = a
            if (v.move_value <= alpha):
                v.min_cutoff += 1
                return v
            if (v.move_value < beta):
                beta = v.move_value
        return v
    
    # state = board, player
    def alpha_beta(self, state):
        result = self.max_value(state, -999, 999, 0)
        '''
        print("Total nodes generated: "+str(result.nodes))
        print("Max depth: "+str(result.max_depth))
        print("Max Val Cutoffs: "+str(result.max_cutoff))
        print("Min Val Cutoffs: "+str(result.min_cutoff))
        '''
        if (isinstance(result.move, Move)):
            return [result.move.start,result.move.end]
        else:
            return result.move
