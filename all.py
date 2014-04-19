from myro import *
from random import *
init ("COM8")
#the matrix of the undetected map
ma=[[0,0,0,0,0,0,0],
    [0,3,3,3,3,3,0],
    [0,3,3,3,3,3,0],
    [0,3,3,3,3,3,0],
    [0,3,3,3,3,3,0],
    [0,3,3,3,3,3,0],
    [0,0,0,0,0,0,0]]##the global var for the map
odire=0##the global var for the direction the robot facing
cmd=[None]*300##the global var for the command the robot might take
position_x=5##the x coord of the robot
position_y=3##the y cood of the robot
end_x=1
end_y=5
box_x=2
box_y=2
breakpt=0
cmd_box=[None]*300
n=0
m=[[0]*7 for t in xrange(7)]

#the basic checking function
def check():
    global ma
    global position_x
    global position_y
    ma[position_x][position_y]=1 ##set the taken route to 1
    x=position_x ## simplification
    y=position_y
    turnLeft(0.5,1.6)##turn left 4 times to check around, refreshing the map
    cen = getObstacle("center")
    if ma[x][y-1]==3:
        if cen>1000:##might not be accurate
            ma[x][y-1]=0
        else:
            ma[x][y-1]=2

    turnLeft(0.5,1.6)
    cen = getObstacle("center")

    if ma[x+1][y]==3:##might not be accurate
        if cen>1000:
            ma[x+1][y]=0
        else:
            ma[x+1][y]=2

    turnLeft(0.5,1.6)
    cen = getObstacle("center")
    if ma[x][y+1]==3:##might not be inaccurate
        if cen>1000:
            ma[x][y+1]=0
        else:
            ma[x][y+1]=2

    turnLeft(0.5,1.6)
    cen = getObstacle("center")
    if ma[x-1][y]==3:##might not be inaccurate
        if cen>1000:
            ma[x-1][y]=0
        else:
            ma[x-1][y]=2
    

#turn back to the origin direction
def reset():
    global odire
    odire=odire%4##simplified turing
    ##turn according to te odire and reset the odire
    if odire>0:
        while odire!=0:
            turnLeft(0.5,1.6)
            odire=odire-1
    elif odire<0:
        while odire!=0:
            turnRight(0.5,1.6)
            odire=odire+1

#
def go():
    global ma
    global odire
    global position_x
    global position_y
    global breakpt
    ca=0
    x=position_x
    y=position_y    

    if ma[x-1][y]==2:
        forward(0.5,3.8)
        x=x-1
        position_x=x
    elif ma[x][y-1]==2:
        turnLeft(0.5,1.6)
        odire=odire-1
        y=y-1
        position_y=y        
        forward(0.5,3.8)
    elif ma[x+1][y]==2:
        turnLeft(0.5,1.6)
        turnLeft(0.5,1.6)
        odire=odire-2#direction refreshing
        x=x+1
        position_x=x
        forward(0.5,3.8)    
    elif ma[x][y+1]==2:
        turnRight(0.5,1.6)
        odire=odire+1
        y=y+1##position refreshing
        position_y=y
        forward(0.5,3.8)
    else:
        find_two(x,y)##no 2s call fcn
        if cmd[0]==0:##finish running
                find_route(x,y,5,3)
                global breakpt
                breakpt=1##set up the potential break ponit for the main fcn
                
        while cmd[ca]!=0:##follow the cmd array
                if cmd[ca]==1:##left
                    reset()
                    turnLeft(0.5,1.6)
                    odire=odire-1
                    x=x-1
                    position_x=x##return the position information to golabal varibal
                    cmd[ca]=0##clear the path
                    forward(0.5,3.8)##unit distance
                    reset()
                elif cmd[ca]==2:##front
                    reset()
                    forward(0.5,3.8)
                    y=y-1
                    position_y=y
                    cmd[ca]=0
                    reset()
                elif cmd[ca]==3:##right
                     reset()
                     turnRight(0.5,1.6)
                     odire=odire+1
                     x=x+1
                     position_x=x
                     cmd[ca]=0
                     forward(0.5,3.8)
                     reset()
                elif cmd[ca]==4:##down
                     reset()
                     turnLeft(0.5,1.6)
                     turnLeft(0.5,1.6)
                     odire=odire-2
                     y=y+1
                     position_y=y
                     cmd[ca]=0
                     forward(0.5,3.8)
                     reset()
                else:
                    print 'weird array!!!!!!'#error
                    break
                ca=ca+1



def find_route(current_x,current_y,target_x,target_y):
  print "find_route is fine(maybe)"
  global n
  n=0
  global m
  m=[[0]*7 for x in xrange(7)]
  global ma
  global cmd
  i=0
  j=0
  che_fin=0
  le=0
  ri=0
  up=0
  dow=0
  ma[target_x][target_y]=1
  for i in range(0,7):
    for j in range(0,7):
      m[i][j]=ma[i][j]						#copy the current map
      
  while 1:										# set up infinite loop
    i=j=1
    for i in range (1,6):
      che_fin=0									#reset all variables
      j=1
      le=ri=up=dow=0
      for j in range (1,6):						#scan the map for some dead ends
          if m[i][j]==1:
            if m[i][j]!=4:
              if m[i-1][j]==1:
                up=1
                
              if m[i+1][j]==1:
                dow=1
                
              if m[i][j-1]==1:
                le=1
                
              if m[i][j+1]==1:
                ri=1									#iff only one of the direction is available, then its a dead end
                
            if up+dow+le+ri==1:
              if current_x==i and current_y==j:
                  if j==5:
                      break                                         #maybe its the point of starting or ending, so we except this condition
                  else:
                      continue
                    
              if target_x==i and target_y==j:
                  if j==5:
                      break
                  else:
                      continue
                    
              m[i][j]=0
              che_fin=che_fin+1
              
            le=ri=up=dow=0
            
    print che_fin
    if che_fin==0:								#che_fin can determine when there is no ends to iterate
      break
    else:											#if its still not the end, we reset i and j
      i=j=0
      
  i=j=num_all=0
  for i in range (0,7):							#if there is no way from starting to ending, we set n to 1
    for j in range (0,7):
      if m[i][j]==1:
          num_all=num_all+1
          
  if num_all==2:
    n=0
  else:
    n=1
    generate_route(current_x,current_y,target_x,target_y)


def find_two(current_x,current_y):
    print "find_two is fine"
    x=y=0
    for x in range(0,7):
        for y in range(0,7):
            if ma[x][y]==2:                                 #find if there is ma[x][y] that is 2
                find_route(current_x,current_y,x,y)       #if there is a ma[x][y],use find_route to get there
                break
            
    if x==7 and y==7:                                       #if there is no 2 in map,we set the cmd to be 0
        cmd[0]=0
        

def  generate_route(current_x,current_y,target_x,target_y):
    print "generate_route is fine(definitely not)"
    global m
    global n
    global cmd
    global ma
    print m
    i=0
    j=t=1
    x=current_x
    y=current_y
    while x!=target_x or y!=target_y:
        ran=randrange(1,3,1)
        if x-target_x>=0:
            if y-target_y>=0:            #target is at left-upward               
                while m[x-1][y]==1 or m[x][y-1]==1:				#there is a way directly to target
                    if ran==1:									#vetical precedence
                        while 1:
                            if m[x-1][y]==1:
                                x=x-1
                                cmd[i]=2
                                i=i+1
                                if x-target_x<=0 and m[x][y-1]==1:		#if it reaches the same height as the target, it becomes horizontal precedence
                                  ran=2
                                  break
                            else:
                                break
                            
                        if m[x][y-1]==1:				#if it cannot get higher, it turns to left and translate to horizontal precedence
                            y=y-1
                            cmd[i]=1
                            i=i+1
                            break
                        
                    else:
                        while 1:
                            if m[x][y-1]==1:
                                y=y-1
                                cmd[i]=1
                                i=i+1
                                if y-target_y<=0 and m[x-1][y]==1:		#if it reaches the same vertical line as the target, it becomes vetical precedence
                                  ran=1
                                  break
                                
                            else:
                                break
                            
                        if m[x-1][y]==1:				#if it cannot get more left, it turns up and translate to vertical precedence
                            x=x-1
                            cmd[i]=2
                            i=i+1                    #reversely write the previous functions#everything becomes inverse
                            break
                        
                if m[x-1][y]!=1 and m[x][y-1]!=1:
                    if x-target_x<=0 or y-target_y<=0:			#this is the condition that it cannot directly reach the target,when it detects that the target is no longer at left upward, it tries other conditions
                        continue
                    else:
                        if m[x+1][y]==1:					#there is a outlet beneath it, so it find another route by going downward
                            while m[x+j][y]==1:
                                cmd[i]=4
                                i=i+1
                                j=j+1
                                if m[x+j][y-1]==1:			#always pay attention to the left path
                                    break
                                
                            j=j-1								#to the bottom of the route
                            while m[x+j][y-t]==1:			#it turns left
                                cmd[i]=1
                                i=i+1
                                t=t+1
                                if m[x+j-1][y-t]==1:		#always pay attention to upward
                                    break
                                
                            t=t-1								#reach the most leftward
                            cmd[i]=2						#get in the upper path and try to locate again
                            i=i+1
                            x=x+j-1
                            y=y-t
                            continue
                        elif m[x][y+1]==1:					#ther is a outlet on its right, so it find route by going rightward
                            while m[x][y+j]==1:
                                cmd[i]=3
                                i=i+1
                                j=j+1
                                if m[x-1][y+j]==1:			#pay attention on the upper bound
                                    break
                                
                            j=j-1
                            while m[x-t][y+j]==1:			#go upward
                                cmd[i]=2
                                i=i+1
                                t=t+1
                                if m[x-t][y+j-1]==1:		#pay attention to leftward side
                                    break
                                
                            t=t-1
                            cmd[i]=1
                            i=i+1
                            x=x-t
                            y=y+j-1
                            continue
                        
                        t=j=1								#reset i and j
                        continue
            elif y-target_y<0:            #target is at right-upward               
                while m[x-1][y]==1 or m[x][y+1]==1:				#there is a way directly to target
                    if ran==1:									#vetical precedence
                        while 1:
                            if m[x-1][y]==1:
                                x=x-1
                                cmd[i]=2
                                i=i+1
                                if x-target_x<=0 and m[x][y+1]==1:		#if it reaches the same height as the target, it becomes horizontal precedence
                                  ran=2
                                  break
                                
                            else:
                                break
                            
                        if m[x][y+1]==1:				#if it cannot get higher, it turns to right and translate to horizontal precedence
                            y=y+1
                            cmd[i]=3
                            i=i+1
                            print "random 1 is fine"
                            break
                        
                    else:
                        while 1:
                            if m[x][y+1]==1:
                                y=y+1
                                cmd[i]=3
                                i=i+1
                                if y-target_y>=0 and m[x-1][y]==1:		#if it goes right and reach the same vertical line as the target, it becomes vertical precedence
                                  ran=1
                                  break
                                
                            else:
                                break
                            
                        if m[x-1][y]==1:				#if it cannot get more right, it turns to up and translate to vertical precedence
                            x=x-1
                            cmd[i]=2
                            i=i+1                    #reversely write the previous functions#everything becomes inverse
                            print "random 2 is fine"
                            break
                        
                if m[x-1][y]!=1 and m[x][y+1]!=1:
                    if x-target_x<=0 or y-target_y>=0:			#this is the condition that it cannot directly reach the target,when it detects that the target is no longer at left upward, it tries other conditions
                        continue
                    else:
                        if m[x+1][y]==1:					#there is a outlet beneath it, so it find another route by going downward
                            while m[x+j][y]==1:                            
                                cmd[i]=4
                                i=i+1
                                j=j+1
                                if m[x+j][y+1]==1:			#always pay attention to the right path
                                    break
                                
                            j=j-1								#to the bottom of the route
                            while m[x+j][y+t]==1:			#it turns right
                                cmd[i]=3
                                i=i+1
                                t=t+1
                                if m[x+j-1][y+t]==1:		#always pay attention to upward
                                    break
                                
                            t=t-1								#reach the most rightward
                            cmd[i]=2						#get in the upper path and try to locate again
                            i=i+1
                            x=x+j-1
                            y=y+t
                            print "somthing without shortcut is available"
                            continue
                        elif m[x][y-1]==1:					#ther is a outlet on its left, so it find route by going leftward
                            while m[x][y-j]==1:
                                cmd[i]=1
                                i=i+1
                                j=j+1
                                if m[x-1][y-j]==1:			#pay attention on the upper bound
                                    break
                                
                            j=j-1
                            while m[x-t][y-j]==1:			#go upward
                                cmd[i]=2
                                i=i+1
                                t=t+1
                                if m[x-t][y-j+1]==1:		#pay attention to rightward side
                                    break
                                
                            t=t-1
                            cmd[i]=1
                            i=i+1
                            x=x-t
                            y=y-j+1
                            print "somthing without shortcut is available"
                            continue
                        
                        t=j=1								#reset i and j
                        continue
        elif x-target_x<0:
            if y-target_y>=0:            #target is at left-downward               
                while m[x+1][y]==1 or m[x][y-1]==1:				#there is a way directly to target
                    if ran==1:									#vetical precedence
                        while 1:
                            if m[x+1][y]==1:
                                x=x+1
                                cmd[i]=4
                                i=i+1
                                if x-target_x>=0 and m[x][y-1]==1:		#if it reaches the same height as the target, it becomes horizontal precedence
                                  ran=2
                                  break
                                
                            else:
                                break
                            
                        if m[x][y-1]==1:				#if it cannot get lower, it turns to left and translate to horizontal precedence
                            y=y-1
                            cmd[i]=1
                            i=i+1
                            break
                        
                    else:
                        while 1:
                            if m[x][y-1]==1:
                                y=y-1
                                cmd[i]=1
                                i=i+1
                                if y-target_y<=0 and m[x+1][y]==1:		#if it reaches the same height as the target, it becomes horizontal precedence
                                  ran=1
                                  break
                                
                            else:
                                break
                            
                        if m[x+1][y]==1:				#if it cannot get lower, it turns to left and translate to horizontal precedence
                            x=x+1
                            cmd[i]=4
                            i=i+1                    #reversely write the previous functions#everything becomes inverse
                            break
                        
                if m[x+1][y]!=1 and m[x][y-1]!=1:
                    if x-target_x>=0 or y-target_y<=0:			#this is the condition that it cannot directly reach the target,when it detects that the target is no longer at left upward, it tries other conditions
                        continue
                    else:
                        if m[x-1][y]==1:					#there is a outlet above it, so it find another route by going upward
                            while m[x-j][y]==1:
                                cmd[i]=2
                                i=i+1
                                j=j+1
                                if m[x-j][y-1]==1:			#always pay attention to the left path
                                    break
                                
                            j=j-1								#to the bottom of the route
                            while m[x-j][y-t]==1:			#it turns left
                                cmd[i]=1
                                i=i+1
                                t=t+1
                                if m[x-j+1][y-t]==1:		#always pay attention to downward
                                    break
                                
                            t=t-1								#reach the most leftward
                            cmd[i]=4						#get in the downward path and try to locate again
                            i=i+1
                            x=x-j+1
                            y=y-t
                            continue
                        elif m[x][y+1]==1:					#ther is a outlet on its right, so it find route by going rightward
                            while m[x][y+j]==1:
                                cmd[i]=3
                                i=i+1
                                j=j+1
                                if m[x+1][y+j]==1:			#pay attention on the lower bound
                                    break
                                
                            j=j-1
                            while m[x+t][y+j]==1:			#go downward
                                cmd[i]=4
                                i=i+1
                                t=t+1
                                if m[x+t][y+j-1]==1:		#pay attention to leftward side
                                    break
                                
                            t=t-1
                            cmd[i]=1
                            i=i+1
                            x=x+t
                            y=y+j-1
                            continue
                        
                        t=j=1								#reset i and j
                        continue
            elif y-target_y<0:            #target is at right-downward               
                while m[x+1][y]==1 or m[x][y+1]==1:				#there is a way directly to target
                    if ran==1:									#vetical precedence
                        while 1:
                            if m[x+1][y]==1:
                                x=x+1
                                cmd[i]=4
                                i=i+1
                                if x-target_x>=0 and m[x][y+1]==1:		#if it reaches the same height as the target, it becomes horizontal precedence
                                  ran=2
                                  break
                                
                            else:
                                break
                            
                        if m[x][y+1]==1:				#if it cannot get lower, it turns to left and translate to horizontal precedence
                            y=y+1
                            cmd[i]=3
                            i=i+1
                            break
                        
                    else:
                        while 1:
                            if m[x][y+1]==1:
                                y=y+1
                                cmd[i]=3
                                i=i+1
                                if y-target_y>=0 and m[x+1][y]==1:		#if it reaches the same height as the target, it becomes horizontal precedence
                                  ran=1
                                  break
                                
                            else:
                                break
                            
                        if m[x+1][y]==1:				#if it cannot get lower, it turns to left and translate to horizontal precedence
                            x=x+1
                            cmd[i]=4
                            i=i+1                    #reversely write the previous functions#everything becomes inverse
                            break
                        
                if m[x+1][y]!=1 and m[x][y+1]!=1:
                    if x-target_x>=0 or y-target_y>=0:			#this is the condition that it cannot directly reach the target,when it detects that the target is no longer at left upward, it tries other conditions
                        continue
                    else:
                        if m[x-1][y]==1:					#there is a outlet above it, so it find another route by going upward
                            while m[x-j][y]==1:
                                cmd[i]=2
                                i=i+1
                                j=j+1
                                if m[x-j][y+1]==1:			#always pay attention to the right path
                                    break
                                
                            j=j-1                                       #to the top of the route
                            while m[x-j][y+t]==1:			#it turns right
                                cmd[i]=1
                                i=i+1
                                t=t+1
                                if m[x-j+1][y+t]==1:		#always pay attention to downward
                                    break
                                
                            t=t-1								#reach the most leftward
                            cmd[i]=4						#get in the downward path and try to locate again
                            i=i+1
                            x=x-j+1
                            y=y+t
                            continue
                        elif m[x][y-1]==1:					#ther is a outlet on its left, so it find route by going leftward
                            while m[x][y-j]==1:
                                cmd[i]=1
                                i=i+1
                                j=j+1
                                if m[x+1][y-j]==1:			#pay attention on the lower bound
                                    break
                                
                            j=j-1
                            while m[x+t][y-j]==1:			#go downward
                                cmd[i]=4
                                i=i+1
                                t=t+1
                                if m[x+t][y-j+1]==1:		#pay attention to rightward side
                                    break
                                
                            t=t-1
                            cmd[i]=3
                            i=i+1
                            x=x+t
                            y=y-j+1
                            continue
                        
                        t=j=1								#reset i and j
                        continue
                    
    cmd[i]=0
    print "can u get through this?"





def phase_one():
    while 1:##repeat the whole thing untill break
        reset()
        check()
        print 'checking...'
        ma
        
        print 'reseting the direction...'
        go()
        print 'walking slowly, be patient...'
        if breakpt==1:##booooooom! finished!!
            break
    print 'phase one finished'
    phase_two()
