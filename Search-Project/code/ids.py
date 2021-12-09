import time
seen_hash = {}

def game_over(setup_dict):
    n, m = setup_dict['dimentions']
    for doctor in setup_dict['doctors']:
        if doctor[0] != 0 or doctor[1] != m - 1:
            return False
    if len(setup_dict['potions']) != 0:
        return False
    return True

def dfs(setup_dict, traveled_depth, to_travel_depth, path):
    dfs.counter += 1
    if to_travel_depth == 0:
        if game_over(setup_dict) == True:
            return path
        return None

    doctors_cur = setup_dict['doctors']
    potions_cur = setup_dict['potions']
    medicines_cur = setup_dict['medicines']
    hazards_cur = setup_dict['hazards']
    n, m = setup_dict['dimentions']

    for doctor in doctors_cur: 
        x, y = doctor[0], doctor[1]
        if x == 0 and y == m - 1:
            continue
        for i, j in [(0, 1), (0, -1), (1, 0), (-1, 0)]: #selecting a direction and moving the doctors
            if x + i >= 0 and x + i < n and y + j >= 0 and y + j < m and hazards_cur[x + i][y + j] == False:
                
                lastmove = ''.join(['(', str(x), ',', str(y), ' '])
                if (i, j) == (-1, 0):
                    lastmove += "up) "
                elif (i, j) == (0, 1):
                    lastmove += "right) "    
                elif (i, j) == (1, 0):
                    lastmove += "down) "
                elif (i, j) == (0, -1):
                    lastmove += "left) "
                
                doctors_new = [*doctors_cur]
                potions_new = [*potions_cur]
                medicines_new = [*medicines_cur]
                x_new, y_new = x + i, y + j
                
                doctors_new.remove( doctor )
                doctors_new.append( (x_new, y_new) )
                doctors_new.sort()

                if (x_new, y_new) in medicines_new:
                    medicines_new.remove( (x_new, y_new) )
                    doctors_new.append( (0, 0) )
                elif (x_new, y_new) in potions_new:
                    potions_new.remove( (x_new, y_new) )

                hash_new = ''.join([str(doctors_new), str(potions_new)])
                valid_hash = hash_new in seen_hash
                if valid_hash and seen_hash[hash_new] < traveled_depth: #skipping the visited states
                    continue
                    
                s_new = {
                    "dimentions": (n, m),
                    "doctors": doctors_new,
                    "potions": potions_new,
                    "medicines": medicines_new,
                    "hazards": hazards_cur,
                    "hash": hash_new
                }
                if valid_hash:
                    if seen_hash[hash_new] > traveled_depth :
                        seen_hash[hash_new] = traveled_depth 
                        if (to_travel_depth > 0):
                            dfs_res = dfs(s_new, traveled_depth + 1, to_travel_depth - 1, path)
                            if dfs_res != None:
                                return lastmove + dfs_res
                else:
                    seen_hash[hash_new] = traveled_depth
                    dfs_res = dfs(s_new, traveled_depth + 1, to_travel_depth - 1, path)
                    if dfs_res != None:
                        return lastmove + dfs_res
                del s_new
    return None 

def main():
    #reading from file and building up the states in a dictionary
    dfs.counter = 0
    f = open("test1.in", "r") 
    [n, m] = map(int, f.readline().split(" "))
    [c, k] = map(int, f.readline().split(" "))
    potions, doctors, medicines = [], [], []
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
    s1 = {
        "dimentions": (n, m),
        "doctors": doctors,
        "potions": potions,
        "medicines": medicines,
        "hazards": hazards,
        "hash": ''.join([str(doctors), str(potions)])
    }
    depth = 0
    seen_hash[s1['hash']] = 0
    
    #expanding the DFS depth until a goal is found
    while 1:
        dfs_res = dfs(s1, 1, depth, "")
        if dfs_res != None:
            print(dfs_res)
            break
        depth += 1
        seen_hash.clear()

    f.close()

if __name__=="__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
    print("--- %s states processed ---" % dfs.counter)