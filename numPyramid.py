def number_of_pyramid(rows):
  
    for i in range (1,rows +1):
        print(" " *(rows-i)*2, end =" ")

        # print each row of  the grid
        for j in range (1,i +1):
            print(f"{j}", end =" ")  
        for j in range (i-1,0,-1):
            print(f"{j}", end =" ")
        print() 
#mg= int(input(Number of Pyramid:")) 
number_of_pyramid(6)                        