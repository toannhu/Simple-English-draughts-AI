# ======================== Class Player =======================================
import copy
import string

DEPTH_LIMIT = 5
#uu tien cho no lam king truoc?
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
    
    def nextMove(self, state): 
        legal = self.calcLegalMoves(state)
        print(legal)
        if (len(legal)>0):
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
        opponent = self.checkOpponent(self.str)
        player = "r" if (opponent == "b") else "b"
        pos = self.calcPos(state,player)
        opponent = self.checkOpponent(self.str)
        player = "r" if (opponent == "b") else "b"
        if (player == "b"):           
            for cell in pos:
                if (state[cell[0]][cell[1]].islower()):
                    if (cell[1] != 7):
                        if (state[cell[0]+1][cell[1]+1] == "." and not hasJumps):
                            result = [(cell[0],cell[1]),(cell[0]+1,cell[1]+1)]
                            legalMoves.append(result)
                        elif(state[cell[0]+1][cell[1]+1] == opponent):
                            jumps = self.checkJump(state,(cell[0],cell[1]), False)
                            if (len(jumps)!=0):
                                if not hasJumps:
                                    hasJumps = True
                                    legalMoves = []
                                legalMoves.extend(jumps)
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
                else: #check King move?
                    if (cell[1] != 7):
                        if (state[cell[0]+1][cell[1]+1] == "." and not hasJumps):
                            result = [(cell[0],cell[1]),(cell[0]+1,cell[1]+1)]
                            legalMoves.append(result)
                        elif (state[cell[0]+1][cell[1]+1] == opponent):
                            jumps = self.checkKingJump(state,(cell[0],cell[1]), False)
                            if (len(jumps)!=0):
                                if not hasJumps:
                                    hasJumps = True
                                    legalMoves = []
                                legalMoves.extend(jumps)
                                
                        if (state[cell[0]-1][cell[1]+1] == "." and not hasJumps):
                            result = [(cell[0],cell[1]),(cell[0]-1,cell[1]+1)]
                            legalMoves.append(result)              
                        elif (state[cell[0]-1][cell[1]+1] == opponent):
                            jumps = self.checkKingJump(state,(cell[0],cell[1]), False)
                            if (len(jumps)!=0):
                                if not hasJumps:
                                    hasJumps = True
                                    legalMoves = []
                                legalMoves.extend(jumps)
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
                    if (cell[1] != 0):
                        if (state[cell[0]-1][cell[1]-1] == "." and not hasJumps):
                            result = [(cell[0],cell[1]),(cell[0]-1,cell[1]-1)]
                            legalMoves.append(result)
                        elif(state[cell[0]-1][cell[1]-1] == opponent):
                            jumps = self.checkJump(state,(cell[0],cell[1]), False)
                            if (len(jumps)!=0):
                                if not hasJumps:
                                    hasJumps = True
                                    legalMoves = []
                                legalMoves.extend(jumps)
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
                    if (cell[1] != 0):
                        if (state[cell[0]-1][cell[1]-1] == "." and not hasJumps):
                            result = [(cell[0],cell[1]),(cell[0]-1,cell[1]-1)]
                            legalMoves.append(result)
                        elif(state[cell[0]-1][cell[1]-1] == opponent):
                            jumps = self.checkKingJump(state,(cell[0],cell[1]), False)
                            if (len(jumps)!=0):
                                if not hasJumps:
                                    hasJumps = True
                                    legalMoves = []
                                legalMoves.extend(jumps)
                                
                        if (state[cell[0]+1][cell[1]-1] == "." and not hasJumps):
                            result = [(cell[0],cell[1]),(cell[0]+1,cell[1]-1)]
                            legalMoves.append(result)
                        elif(state[cell[0]+1][cell[1]-1] == opponent):
                            jumps = self.checkKingJump(state,(cell[0],cell[1]), False)
                            if (len(jumps)!=0):
                                if not hasJumps:
                                    hasJumps = True
                                    legalMoves = []
                                legalMoves.extend(jumps)
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
    
    
    def checkJump(self, state, cell, isLeft):
        jumps = []
        if (cell[0]-1 == 0 or cell[0]+1 == 7):
            return jumps
        opponent = self.checkOpponent(self.str)
        player = "r" if (opponent == "b") else "b"
        if (player == "b"):       
            if (isLeft):
                if (cell[1]>1 and state[cell[0]+2][cell[1]-2] == "."):
                    temp = Move(cell, (cell[0]+2, cell[1]-2), True)
                    temp.jumpOver = [(cell[0]+1,cell[1]-1)]  
                    if (temp.end[0]-1 > 0 and temp.end[0]+1 < 7):
                        if (temp.end[1] > 1 and state[temp.end[0]+1][temp.end[1]-1] == opponent):
                            test = self.checkJump(state,temp.end,True)
                            if (test != []):
                                dbl_temp = copy.deepcopy(temp)
                                dbl_temp.end = test[0].end 
                                dbl_temp.jumpOver.extend(test[0].jumpOver)
                                jumps.append(dbl_temp)              

                        if (temp.end[1] < 6 and state[temp.end[0]+1][temp.end[1]+1] == opponent):
                            test = self.checkJump(state,temp.end,False)                	
                            if (test != []):
                                dbl_temp = copy.deepcopy(temp)
                                dbl_temp.end = test[0].end 
                                dbl_temp.jumpOver.extend(test[0].jumpOver)
                                jumps.append(dbl_temp)                 
                    jumps.append(temp)

            else:
                if (cell[1] < 6 and state[cell[0]+2][cell[1]+2] == "."):
                    temp = Move(cell, (cell[0]+2, cell[1]+2), True)
                    temp.jumpOver = [(cell[0]+1,cell[1]+1)]
                    if (temp.end[0]+1 > 0 and temp.end[0]+1 < 7):
                        if (temp.end[1] > 1 and state[temp.end[0]+1][temp.end[1]-1] == opponent):
                            test = self.checkJump(state,temp.end,True)
                            if (test != []):
                                dbl_temp = copy.deepcopy(temp) 
                                dbl_temp.end = test[0].end 
                                dbl_temp.jumpOver.extend(test[0].jumpOver)
                                jumps.append(dbl_temp)                 			

                        if (temp.end[1]<6 and state[temp.end[0]+1][temp.end[1]+1] == opponent):
                            test = self.checkJump(state,temp.end, False) 
                            if (test != []):
                                dbl_temp = copy.deepcopy(temp)
                                dbl_temp.end = test[0].end 
                                dbl_temp.jumpOver.extend(test[0].jumpOver)
                                jumps.append(dbl_temp)
                    jumps.append(temp)     
        else:
            if (isLeft):
                if (cell[1]>1 and state[cell[0]-2][cell[1]-2] == "."):
                    temp = Move(cell, (cell[0]-2, cell[1]-2), True)
                    temp.jumpOver = [(cell[0]-1,cell[1]-1)] 
                    if (temp.end[0]-1 > 0 and temp.end[0]+1 < 7):
                        if (temp.end[1] > 1 and state[temp.end[0]-1][temp.end[1]-1] == opponent):
                            test = self.checkJump(state,temp.end,True)
                            if (test != []):
                                dbl_temp = copy.deepcopy(temp)
                                dbl_temp.end = test[0].end 
                                dbl_temp.jumpOver.extend(test[0].jumpOver)
                                jumps.append(dbl_temp)               
                        if (temp.end[1] < 6 and state[temp.end[0]-1][temp.end[1]+1] == opponent):
                            test = self.checkJump(state,temp.end,False)                	
                            if (test != []):
                                dbl_temp = copy.deepcopy(temp)
                                dbl_temp.end = test[0].end 
                                dbl_temp.jumpOver.extend(test[0].jumpOver)
                                jumps.append(dbl_temp)                 
                    jumps.append(temp)

            else:
                if (cell[1] < 6 and state[cell[0]-2][cell[1]+2] == "."):
                    temp = Move(cell, (cell[0]-2, cell[1]+2), True)
                    temp.jumpOver = [(cell[0]-1,cell[1]+1)]
                    if (temp.end[0]+1 > 0 and temp.end[0]+1 < 7):
                        if (temp.end[1] > 1 and state[temp.end[0]-1][temp.end[1]-1] == opponent):
                            test = self.checkKingJump(state,temp.end,True);
                            if (test != []):
                                dbl_temp = copy.deepcopy(temp)
                                dbl_temp.end = test[0].end 
                                dbl_temp.jumpOver.extend(test[0].jumpOver)
                                jumps.append(dbl_temp)                 			

                        if (temp.end[1]<6 and state[temp.end[0]-1][temp.end[1]+1] == opponent):
                            test = self.checkKingJump(state,temp.end, False) 
                            if (test != []):
                                dbl_temp = copy.deepcopy(temp)
                                dbl_temp.end = test[0].end 
                                dbl_temp.jumpOver.extend(test[0].jumpOver)
                                jumps.append(dbl_temp)
                    jumps.append(temp)
        return jumps

    def checkKingJump(self, state, cell, isLeft):
        jumps = []
        opponent = self.checkOpponent(self.str)
        if (isLeft):
            if (cell[1]>1 and cell[1]<6 and state[cell[0]+2][cell[1]-2] == "."):
                temp = Move(cell, (cell[0]+2, cell[1]-2), True)
                temp.jumpOver = [(cell[0]+1,cell[1]-1)]
                if (temp.end[0]-1 > 0 and temp.end[0]+1 < 7):
                    if (temp.end[1] > 1 and state[temp.end[0]+1][temp.end[1]-1] == opponent):
                        test = self.checkKingJump(state,temp.end,True)
                        if (test != []):
                            dbl_temp = copy.deepcopy(temp)
                            dbl_temp.end = test[0].end 
                            dbl_temp.jumpOver.extend(test[0].jumpOver)
                            jumps.append(dbl_temp)               
                    if (temp.end[1] < 6 and state[temp.end[0]+1][temp.end[1]+1] == opponent):
                        test = self.checkKingJump(state,temp.end,False)                	
                        if (test != []):
                            dbl_temp = copy.deepcopy(temp)
                            dbl_temp.end = test[0].end 
                            dbl_temp.jumpOver.extend(test[0].jumpOver)
                            jumps.append(dbl_temp)                 
                jumps.append(temp)
                
            if (cell[1]>1 and cell[1]<6 and state[cell[0]-2][cell[1]-2] == "."):
                temp = Move(cell, (cell[0]-2, cell[1]-2), True)
                temp.jumpOver = [(cell[0]-1,cell[1]-1)] 
                if (temp.end[0]-1 > 0 and temp.end[0]+1 < 7):
                    if (temp.end[1] > 1 and state[temp.end[0]-1][temp.end[1]-1] == opponent):
                        test = self.checkKingJump(state,temp.end,True)
                        if (test != []):
                            dbl_temp = copy.deepcopy(temp)
                            dbl_temp.end = test[0].end 
                            dbl_temp.jumpOver.extend(test[0].jumpOver)
                            jumps.append(dbl_temp)                
                    if (temp.end[1] < 6 and state[temp.end[0]-1][temp.end[1]+1] == opponent):
                        test = self.checkKingJump(state,temp.end,False)                	
                        if (test != []):
                            dbl_temp = copy.deepcopy(temp)
                            dbl_temp.end = test[0].end 
                            dbl_temp.jumpOver.extend(test[0].jumpOver)
                            jumps.append(dbl_temp)                 
                jumps.append(temp)

        else:
            if (cell[1] < 6 and cell[1]>1 and state[cell[0]+2][cell[1]+2] == "."):
                temp = Move(cell, (cell[0]+2, cell[1]+2), True)
                temp.jumpOver = [(cell[0]+1,cell[1]+1)]
                if (temp.end[0]+1 > 0 and temp.end[0]+1 < 7):
                    if (temp.end[1] > 1 and state[temp.end[0]+1][temp.end[1]-1] == opponent):
                        test = self.checkKingJump(state,temp.end,True);
                        if (test != []):
                            dbl_temp = copy.deepcopy(temp)
                            dbl_temp.end = test[0].end 
                            dbl_temp.jumpOver.extend(test[0].jumpOver)
                            jumps.append(dbl_temp)                 			

                    if (temp.end[1]<6 and state[temp.end[0]+1][temp.end[1]+1] == opponent):
                        test = self.checkKingJump(state,temp.end, False) 
                        if (test != []):
                            dbl_temp = copy.deepcopy(temp)
                            dbl_temp.end = test[0].end 
                            dbl_temp.jumpOver.extend(test[0].jumpOver)
                            jumps.append(dbl_temp)
                jumps.append(temp)     
            if (cell[1] < 6 and cell[1]>1 and state[cell[0]-2][cell[1]+2] == "."):
                temp = Move(cell, (cell[0]-2, cell[1]+2), True)
                temp.jumpOver = [(cell[0]-1,cell[1]+1)]
                if (temp.end[0]+1 > 0 and temp.end[0]+1 < 7):
                    if (temp.end[1] > 1 and state[temp.end[0]-1][temp.end[1]-1] == opponent):
                        test = self.checkKingJump(state,temp.end,True);
                        if (test != []):
                            dbl_temp = copy.deepcopy(temp)
                            dbl_temp.end = test[0].end 
                            dbl_temp.jumpOver.extend(test[0].jumpOver)
                            jumps.append(dbl_temp)                 			

                    if (temp.end[1]<6 and state[temp.end[0]-1][temp.end[1]+1] == opponent):
                        test = self.checkKingJump(state,temp.end, False) 
                        if (test != []):
                            dbl_temp = copy.deepcopy(temp)
                            dbl_temp.end = test[0].end 
                            dbl_temp.jumpOver.extend(test[0].jumpOver)
                            jumps.append(dbl_temp)
                jumps.append(temp)
        return jumps


    def evaluation_function(self, state):
        player_far, player_home_half, player_opp_half = 0,0,0
        opponent_far, opponent_home_half, opponent_opp_half = 0,0,0 
        opponent = self.checkOpponent(self.str)
        player = "r" if (opponent == "b") else "b"
        if (player == "b"):
            player_pos = self.calcPos(state,player)
            for cell in player_pos:
                if (state[cell[0]][cell[1]] == "B"):
                    player_far += 1
                elif (3 <= cell[0] < 7 and state[cell[0]][cell[1]] == "b"):
                    player_opp_half += 1
                else:
                    player_home_half += 1             

            opponent_pos = self.calcPos(state,opponent)
            for cell in opponent_pos:    
                if (state[cell[0]][cell[1]] == "R"):
                    opponent_far += 1
                elif (1 <= cell[0] < 5 and state[cell[0]][cell[1]] == "r"):
                    opponent_opp_half += 1
                else:
                    opponent_home_half += 1
        else:
            player_pos = self.calcPos(state,player)
            for cell in player_pos:
                if (state[cell[0]][cell[1]] == "B"):
                    player_far += 1
                elif (1 <= cell[0] < 4 and state[cell[0]][cell[1]] == "b"):
                    player_opp_half += 1
                else:
                    player_home_half += 1             

            opponent_pos = self.calcPos(state,opponent)
            for cell in opponent_pos:    
                if (state[cell[0]][cell[1]] == "R"):
                    opponent_far += 1
                elif (3 <= cell[0] < 7 and state[cell[0]][cell[1]] == "r"):
                    opponent_opp_half += 1
                else:
                    opponent_home_half += 1
        player_score = (7 * player_far) + (5 * player_opp_half)+ (3 * player_home_half)
        opponent_score = (7 * opponent_far) + (5 * opponent_opp_half)+ (3 * opponent_home_half)
        return (player_score - opponent_score)   
      
    def calcScore(self, state):
        score = [0,0]
        opponent = self.checkOpponent(self.str)
        player = "r" if (opponent == "b") else "b"
        if (player == "b"):
            player_pos = self.calcPos(state,player)
            for cell in player_pos:
                if (state[cell[0]][cell[1]] == "B"):
                    score[0] += 2
                else:
                    score[0] += 1
                
            opponent_pos = self.calcPos(state,opponent)
            for cell in opponent_pos:
                if (state[cell[0]][cell[1]] == "R"):
                    score[1] += 2
                else:
                    score[1] += 1
        else:
            player_pos = self.calcPos(state,player)
            for cell in player_pos:
                if (state[cell[0]][cell[1]] == "R"):
                    score[0] += 2
                else:
                    score[0] += 1
                
            opponent_pos = self.calcPos(state,opponent)
            for cell in opponent_pos:
                if (state[cell[0]][cell[1]] == "B"):
                    score[1] += 2
                else:
                    score[1] += 1
        return score

    def max_value(self, state, alpha, beta, node):
        opponent = self.checkOpponent(self.str)
        player = "r" if (opponent == "b") else "b"
        actions = self.calcLegalMoves(state)
        num_act = len(actions)
        v = AB_Value(-999, None, node, 1, 0, 0)
        if (node == DEPTH_LIMIT):
            v.move_value = self.evaluation_function(state)
            return v      
        if (len(actions) == 0):
            score = self.calcScore(state)
            if (score[0] > score[1]):
                v.move_value = 100 + (2*score[0]-score[1])
            else:
                v.move_value = -100 + (2*score[0]-score[1])         
            return v
    
        for a in actions:
            newState = copy.deepcopy(state)
            if (isinstance(a, Move)):
                self.player_pos = self.calcPos(state,player)
                self.opponent_pos = self.calcPos(state,opponent)
            new_v = self.min_value(newState, alpha, beta, node+1)
            if (new_v.max_depth > v.max_depth):
                v.max_depth = new_v.max_depth         
            v.nodes += new_v.nodes
            v.max_cutoff += new_v.max_cutoff
            v.min_cutoff += new_v.min_cutoff
            if (new_v.move_value > v.move_value):
               v.move_value = new_v.move_value
               v.move = a
            if (v.move_value >= beta):
               v.max_cutoff += 1
               return v
            if (v.move_value > alpha):
               alpha = v.move_value
        return v
    
    def min_value(self, state, alpha, beta, node):
        opponent = self.checkOpponent(self.str)
        player = "r" if (opponent == "b") else "b"
        actions = self.calcLegalMoves(state)
        num_act = len(actions)
        v = AB_Value(999, None, node, 1, 0, 0)
        if (node == DEPTH_LIMIT):
            v.move_value = self.evaluation_function(state)
            return v
        if (len(actions)==0):
            score = self.calcScore(state)
            if (score[0] > score[1]):
                v.move_value = 100 + (2*score[0]-score[1])        
            else:
                v.move_value = -100 + (2*score[0]-score[1])
            return v     
        for a in actions:
            newState = copy.deepcopy(state)
            if (isinstance(a, Move)):
                self.player_pos = self.calcPos(state,player)
                self.opponent_pos = self.calcPos(state,opponent)
            new_v = self.max_value(newState, alpha, beta, node+1)
            if (new_v.max_depth > v.max_depth):
                v.max_depth = new_v.max_depth
            v.nodes += new_v.nodes
            v.max_cutoff += new_v.max_cutoff
            v.min_cutoff += new_v.min_cutoff
            if (new_v.move_value < v.move_value):
                v.move_value = new_v.move_value
                v.move = a
            if (v.move_value <= alpha):
                v.min_cutoff += 1
                return v
            if (v.move_value < beta):
                beta = v.move_value
        return v
    
    def alpha_beta(self, state):
        result = self.max_value(state, -999, 999, 0)
        if (isinstance(result.move, Move)):
            return [result.move.start,result.move.end]
        else:
            return result.move
