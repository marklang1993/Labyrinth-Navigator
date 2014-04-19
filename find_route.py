## main
cmd=[None]*300
ma=[[0,0,0,0,0,0,0],
    [0,1,1,1,1,3,0],
    [0,1,2,1,2,3,0],
    [0,1,0,1,0,3,0],
    [0,1,2,1,2,3,0],
    [0,1,0,1,0,3,0],
    [0,0,0,0,0,0,0]]
## find_path: initialize
ma_t=[[0,0,0,0,0,0,0],
      [0,3,3,3,3,3,0],
      [0,3,3,3,3,3,0],
      [0,3,3,3,3,3,0],
      [0,3,3,3,3,3,0],
      [0,3,3,3,3,3,0],
      [0,0,0,0,0,0,0]]
ma_i=[[0,0,0,0,0],
      [0,0,0,0,0],
      [0,0,0,0,0],
      [0,0,0,0,0],
      [0,0,0,0,0]] ##internal map
ma_ex=[[1,1,1,1,1],
       [1,1,1,1,1],
       [1,1,1,1,1],
       [1,1,1,1,1],
       [1,1,1,1,1]] ##temporary block
counter_array=0 ##array pointer
fp_finish=0 ##switch for finding route
temp_x = 0
temp_y = 0
## map_process
ma_show=[['X','X','X','X','X','X','X'],
         ['X','X','X','X','X','X','X'],
         ['X','X','X','X','X','X','X'],
         ['X','X','X','X','X','X','X'],
         ['X','X','X','X','X','X','X'],
         ['X','X','X','X','X','X','X'],
         ['X','X','X','X','X','X','X']] ##map_show


def direction(aim_x,aim_y):
    global counter_array
    global fp_finish
    global ma_i
    global ma_ex
    global cmd
    global temp_x
    global temp_y

    ##print counter_array
    counter_direction = 1 ##initialize direction
    ## Left
    if (counter_direction==1 and temp_x>0 and fp_finish == 0):
        if ma_i[temp_y][temp_x-1]==1 and ma_ex[temp_y][temp_x-1]==1:
            cmd[counter_array] = counter_direction
            counter_array = counter_array + 1
            temp_x = temp_x - 1
            ma_ex[temp_y][temp_x]=0
            if temp_x == (aim_x - 1) and temp_y == (aim_y - 1):
                fp_finish = 1
            else:
                direction(aim_x,aim_y)

    counter_direction = counter_direction + 1

    ## Up
    if (counter_direction==2 and temp_y>0 and fp_finish == 0):
        if ma_i[temp_y-1][temp_x]==1 and ma_ex[temp_y-1][temp_x]==1:
            cmd[counter_array] = counter_direction
            counter_array = counter_array + 1
            temp_y = temp_y - 1
            ma_ex[temp_y][temp_x]=0
            if temp_x == (aim_x - 1) and temp_y == (aim_y - 1):
                fp_finish = 1
            else:
                direction(aim_x,aim_y)

    counter_direction = counter_direction + 1
    
    ## Right
    if (counter_direction==3 and temp_x<4 and fp_finish == 0):
        if ma_i[temp_y][temp_x+1]==1 and ma_ex[temp_y][temp_x+1]==1:
            cmd[counter_array] = counter_direction
            counter_array = counter_array + 1
            temp_x = temp_x + 1
            ma_ex[temp_y][temp_x]=0
            if temp_x == (aim_x - 1) and temp_y == (aim_y - 1):
                fp_finish = 1
            else:
                direction(aim_x,aim_y)

    counter_direction = counter_direction + 1
    
    ## Down
    if (counter_direction==4 and temp_y<4 and fp_finish == 0):
        if ma_i[temp_y+1][temp_x]==1 and ma_ex[temp_y+1][temp_x]==1:
            cmd[counter_array] = counter_direction
            counter_array = counter_array + 1
            temp_y = temp_y + 1
            ma_ex[temp_y][temp_x]=0
            if temp_x == (aim_x - 1) and temp_y == (aim_y - 1):
                fp_finish = 1
            else:
                direction(aim_x,aim_y)

    counter_direction = counter_direction + 1
    
    ##No way and not Finish
    if counter_direction==5 and fp_finish == 0:
        counter_array = counter_array - 1
        if cmd[counter_array] == 1:
            temp_x = temp_x + 1
            cmd[counter_array] = 0
        elif cmd[counter_array] == 2:
            temp_y = temp_y + 1
            cmd[counter_array] = 0
        elif cmd[counter_array] == 3:
            temp_x = temp_x - 1
            cmd[counter_array] = 0
        elif cmd[counter_array] == 4:
            temp_y = temp_y - 1
            cmd[counter_array] = 0       


def find_route(current_x,current_y,target_x,target_y):
    global counter_array
    global fp_finish
    global ma
    global ma_t
    global ma_i
    global ma_ex
    global cmd
    global temp_x
    global temp_y
    
    ##transfer some parameter
    aim_x = target_x
    aim_y = 6 - target_y
    position_x = current_x
    position_y = 6 - current_y
    ##transpose map
    for i in range (0,7):
        for j in range (0,7):
            ma_t[i][j] = ma[j][6-i]

    print ma_t
    
    ##transfer map(size)
    for i in range (1,6):
        for j in range (1,6):
            ma_i[i-1][j-1] = ma_t[i][j]

    ##execute
    temp_x = position_x - 1
    temp_y = position_y - 1
    ma_ex[temp_y][temp_x] = 0
    direction(aim_x,aim_y)
    cmd[counter_array] = 0
    ##transfer cmd
    i=0
    while cmd[i]!=0:
        if cmd[i]==1:
            cmd[i]=2
            i=i+1
        elif cmd[i]==2:
            cmd[i]=3
            i=i+1
        elif cmd[i]==3:
            cmd[i]=4
            i=i+1
        elif cmd[i]==4:
            cmd[i]=1
            i=i+1
            
    ##refresh
    ma_ex=[[1,1,1,1,1],
           [1,1,1,1,1],
           [1,1,1,1,1],
           [1,1,1,1,1],
           [1,1,1,1,1]]
    counter_array=0
    fp_finish=0


def clear():
    global cmd
    for i in range (0,300):
        cmd[i]=0


def process_map():
    global ma
    global ma_show
    for i in range (0,7):
        for j in range (0,7):
            if ma[i][j] == 0:
                ma_show[i][j] = 'X'
            elif ma[i][j] == 1:
                ma_show[i][j] = ' '
            else:
                ma_show[i][j] = '?'

    print "processing successfully completed!"


def show_map():
    global ma_show
    for i in range (0,7):
        for j in range (0,7):
            print ma_show[i][j],
        print " "


def rotate_map():
    global ma_show
    ma_temp=[['X','X','X','X','X','X','X'],
             ['X','X','X','X','X','X','X'],
             ['X','X','X','X','X','X','X'],
             ['X','X','X','X','X','X','X'],
             ['X','X','X','X','X','X','X'],
             ['X','X','X','X','X','X','X'],
             ['X','X','X','X','X','X','X']] ##map_show

    for i in range (0,7):
        for j in range (0,7):
            ma_temp[i][j] = ma_show[6-j][i]

    for i in range (0,7):
        for j in range (0,7):
            ma_show[i][j] = ma_temp[i][j]

    print "rotating successfully completed!"
