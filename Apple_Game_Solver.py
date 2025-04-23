import pyautogui

# Class containing apple placement, distance, maximum, minimum, etc.
class game_information():
    def __init__(self):
        self.apple_matrix = [[0]*17 for _ in range(10)]
        self.x_min,self.y_min = (10000,10000)
        self.x_max,self.y_max = (0,0)
        self.end = 1
    
    ## Print matrix visually
    def matrix_print(self):
        row = len(self.apple_matrix)
        for i in range(row):
            print(*self.apple_matrix[i])
        print('-'*40)
        return 0
    
    ## Make 2d list from screen
    def num_serach(self):
        init_list = []
        
        for num in range(1,10):
            img_file = str(num)+ '.jpg'
            print(img_file)
                   
            for apple in pyautogui.locateAllOnScreen(img_file,confidence=0.95):
                self.x_min = min(self.x_min,apple.left)
                self.y_min = min(self.y_min,apple.top)
                self.x_max = max(self.x_max,apple.left)
                self.y_max = max(self.y_max,apple.top)
                init_list.append((apple.left,apple.top,num)) # (x,y,apple_number)
        
        # Calculate distance each axis
        self.x_dist = (self.x_max - self.x_min) / 17
        self.y_dist = (self.y_max - self.y_min) / 10
        
        # Refine initial list
        for (x,y,number) in init_list:
            # Calculate row and column number by using distance
            col = int((x-self.x_min) // self.x_dist)
            row = int((y-self.y_min) // self.y_dist)
            
            # Prevent out of index
            if col >= 17:
                col = 16
            if row >= 10:
                row = 9
                
            self.apple_matrix[row][col] = number
        return 0
    
    ## Brute force (일단 직선으로 가게 해보기.)
    def brute_force(self):
        while True:
            cnt = 0
            for i in range(10):
                for j in range(17):
                    if self.apple_matrix[i][j] != 0:
                        # x-direction
                        x = j
                        sum = self.apple_matrix[i][j]
                        while sum < 10:
                            x += 1
                            if x >= 17:
                                break
                            sum += self.apple_matrix[i][x]
                            if sum == 10:
                                cnt = 1
                                for _ in range(j,x+1):
                                    self.apple_matrix[i][_] = 0
                                self.matrix_print()
                                self.drag(j,x,i,i)
                            
                        # y-direction
                        y = i
                        sum = self.apple_matrix[i][j]
                        while sum < 10:
                            y += 1
                            if y >= 10:
                                break
                            sum += self.apple_matrix[y][j]
                            if sum == 10:
                                cnt = 1
                                for _ in range(i,y+1):
                                    self.apple_matrix[_][j] = 0
                                self.matrix_print()
                                self.drag(j,j,i,y)
            if not cnt: # 모든 칸에서 가로,세로 직선으로 탐색해서 10개 되는 게 아예 없으면 2xn or nx2 탐색
                self.rectangle_ten()
            
            if self.end:
                self.num_serach()
        return 0
        
    ## Brute force (2xn or nx2의 직사각형 탐색)
    def rectangle_ten(self):
        while not self.end:
            self.end = 1
            for i in range(9):
                for j in range(16):
                    # x-direction (n*2) (j,i) ~ (x,i+1) (가로로 긴 직사각형)
                    x = j
                    sum = self.apple_matrix[i][j] + self.apple_matrix[i+1][j]
                    while sum < 10:
                        x += 1
                        if x >= 17:
                            break
                        sum += self.apple_matrix[i][x] + self.apple_matrix[i+1][x]
                        if sum == 10:
                            self.end = 0
                            for _ in range(j,x+1):
                                self.apple_matrix[i][_] = 0
                                self.apple_matrix[i+1][_] = 0
                            self.matrix_print()
                            self.drag(j,x,i,i+1)
                        
                    # y-direction (2*n) (j,i) ~ (j+1,y) (세로로 긴 직사각형)
                    y = i
                    sum = self.apple_matrix[i][j] + self.apple_matrix[i][j+1]
                    while sum < 10:
                        self.end = 0
                        y += 1
                        if y >= 10:
                            break
                        sum += self.apple_matrix[y][j] + self.apple_matrix[y][j+1]
                        if sum == 10:
                            for _ in range(i,y+1):
                                self.apple_matrix[_][j] = 0
                                self.apple_matrix[_][j+1] = 0
                            self.matrix_print()
                            self.drag(j,j+1,i,y)
        return 0
                
                        
    def drag(self,a,b,c,d):
        x_init = self.x_min + a * self.x_dist + 0.2 * self.x_dist 
        x_final = self.x_min + b * self.x_dist*1.07 + 1.4 * self.x_dist
        y_init = self.y_min + c *self.y_dist + 0.3 * self.y_dist
        y_final = self.y_min + d *self.y_dist*1.1 + 1.5 * self.y_dist
        pyautogui.click(x_init,y_init)
        pyautogui.dragTo(x_final,y_final,0.5,button='left')
        return 0


def main():
    g = game_information()
    g.num_serach()
    g.matrix_print()
    g.brute_force()
    

if __name__ == '__main__':
    main()