import copy
import time

#defining class for each state of the game
class Setup:

    def __init__(self, n, m, doctors, potions, medicines, path):
        self.n = copy.deepcopy(n)
        self.m = copy.deepcopy(m)
        self.doctors = copy.deepcopy(doctors)
        self.potions = copy.deepcopy(potions)
        self.medicines = copy.deepcopy(medicines)
        self.path = copy.deepcopy(path) 
        self.hash = ''.join([str(self.doctors), str(self.potions)])

    def print_matrix(self):
        print(''.join([str(self.doctors), str(self.potions), str(self.path)]))
        
    def get_hash(self):
        return self.hash
    
    def game_over(self):
        for doctor in self.doctors:
            if doctor[0] != 0 or doctor[1] != self.m - 1:
                return False
        if len(self.potions) != 0:
            return False
        return True

def main():
    #reading from file and building up the board
    f = open("test1.in", "r") 
    [n, m] = map(int, f.readline().split(" "))
    [c, k] = map(int, f.readline().split(" "))
    potions, doctors, medicines, seen_states = [], [], [], 1
    hazards = [[False for i in range(n)] for j in range(m)] 
    for i in range(0, c):
        [x, y] = map(int, f.readline().split(" "))
        potions.append( (n - x - 1, y) )
    for i in range(0, k):
        [x, y] = map(int, f.readline().split(" "))    
        if x == 0 and y == 0:
            doctors.append( (0, 0) )
        medicines.append( (n - x - 1, y) )
    [d] = map(int, f.readline().split(" "))
    for i in range(0, d):
        [x, y] = map(int, f.readline().split(" "))
        hazards[n - x - 1][y] = True
    doctors.append( (n - 1, 0) )
    medicines.sort()
    doctors.sort()
    potions.sort()
    s1 = Setup(n, m, doctors, potions, medicines, "start: ")
    setups = [s1]
    seen_hash = {s1.get_hash()}

    #doing bfs on states starting with s1
    while len(setups) > 0:
        setup_cur = setups.pop(0)
        if setup_cur.game_over():
            print(setup_cur.path)
            break
        for k in range(len(setup_cur.doctors)):
            for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]: #selecting a direction
                x, y = setup_cur.doctors[k][0], setup_cur.doctors[k][1]
                if x == 0 and y == m - 1:
                    continue
                lastmove = '(' + str(x) + ',' + str(y) + ' '
                if (i, j) == (-1, 0):
                    lastmove += "up) "
                elif (i, j) == (1, 0):
                    lastmove += "down) "    
                elif (i, j) == (0, -1):
                    lastmove += "left) "
                elif (i, j) == (0, 1):
                    lastmove += "right) "

                #moving the doctors in said directions (if possible)
                if x + i >= 0 and x + i < n and y + j >= 0 and y + j < m and hazards[x + i][y + j] == False:
                    doctors_new = copy.deepcopy(setup_cur.doctors)
                    potions_new = copy.deepcopy(setup_cur.potions)
                    medicines_new = copy.deepcopy(setup_cur.medicines)
                    path_new = copy.deepcopy(setup_cur.path)
                    x_new = x + i
                    y_new = y + j
                    doctors_new.pop(k)
                    doctors_new.append( (x_new, y_new) )
                    if (x_new, y_new) in medicines_new:
                        medicines_new.remove( (x_new, y_new) )
                        doctors_new.append((0, 0))
                    elif (x_new, y_new) in potions_new:
                        potions_new.remove ( (x_new, y_new))
                    doctors_new.sort()
                    seen_states += 1
                    s_new = Setup(n, m, doctors_new, potions_new, medicines_new, path_new + lastmove)
                    s_new_hash = s_new.get_hash()
                    if s_new_hash not in seen_hash:
                        seen_hash.add(s_new_hash)
                        setups.append(s_new)
    f.close()
    return seen_states
if __name__=="__main__":
    start_time = time.time()
    seen_states = main()
    print("--- %s seconds ---" % (time.time() - start_time))
    print("--- %s states processed ---" % seen_states)