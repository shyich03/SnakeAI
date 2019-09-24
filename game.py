from random import randint
import numpy as np
import copy

# board: snake:N, blank: 0, food: -1
class Game:
    def __init__(self):
        self.side = 5
        board = [[0] * self.side for i in range(self.side)]
        board[2][2] = 1
        self.board = board
        self.length = 1
        self.head = [2, 2]
        self.move = 0
        # 0 up, 1 right, 2 bot, 3 left
        self.direction = 0
        food = [randint(0, self.side-1), randint(0, self.side-1)]
        validFood = self.board[food[0]][food[1]] == 0
        while not validFood:
            food = [randint(0, self.side-1), randint(0, self.side-1)]
            validFood = self.board[food[0]][food[1]] == 0
        self.food = food
        self.board[food[0]][food[1]] = -1
        self.dist = dist = np.absolute(self.head[0]-self.food[0])+np.absolute(self.head[1]-self.food[1])

    def printBoard(self):
        for i in range(self.side):
            for j in range(self.side):
                if[i,j]==self.food:
                    print('*', end='')
                else:
                    print(self.board[i][j]%10, end = '')
            print("\n")

    # turn: -1 left, 0 fwd, 1 right
    def step(self, turn):
        if (turn+self.direction) % 4 == 3:
            head = [self.head[0], self.head[1]-1]
        elif (turn+self.direction) % 4 == 0:
            head = [self.head[0]-1, self.head[1]]
        elif (turn + self.direction) % 4 == 1:
            head = [self.head[0], self.head[1]+1]
        else:
            head = [self.head[0]+1, self.head[1]]
        if head[0] >= self.side or head[0] < 0 or head[1] >= self.side or head[1] <0:
            self.length = 0
        elif self.board[head[0]][head[1]] > 0:
            self.length = 0
        else:
            self.head = head
            if head == self.food:
                self.length += 1
                self.board[head[0]][head[1]] = self.length
                self.move = 0

                food = [randint(0, self.side - 1), randint(0, self.side - 1)]
                validFood = self.board[food[0]][food[1]] == 0
                while not validFood:
                    food = [randint(0, self.side - 1), randint(0, self.side - 1)]
                    validFood = self.board[food[0]][food[1]] == 0
                self.food = food
                self.board[food[0]][food[1]] = -1
            else:
                for i in range(self.side):
                    for j in range(self.side):
                        if not self.board[i][j] == 0:
                            self.board[i][j] -= 1
                self.board[head[0]][head[1]] = self.length
                self.move += 1
        self.dist = [self.head[0]-self.food[0],self.head[1]-self.food[1]]
        self.direction=(self.direction+turn)%4
        return [self.length, self.dist]

    def best_move(self):
        # i = np.argmax(np.absolute(self.dist))
        # j = self.dist[i]/np.absolute(self.dist[i])
        # # check direction
        # if (i==0 and (1-j)==dir) or (i==1 and (2+j)==dir)
        # if self.board[self.head[0]+(1-i)*j][self.head[1]+i*j] == 0:
        #     return
        score = [0]*3
        for i in range (3):
            new_game = copy.deepcopy(self)
            new_score = new_game.step(i-1)
            print(new_score)
            score[i] = (new_score[0]*self.side*self.side)+(self.side*self.side-np.sum(np.absolute(new_score[1])))
        index = np.argmax(score)-1
        return index


if __name__ == '__main__':
    asd = Game()
    size = 10000
    board_array = [[0] * (asd.side ** 2) for i in range(size)]
    action_array = [[0]  for i in range(size)]
    # asd.step(0)
    # asd.printBoard()
    # print(asd.best_move())
    # print(asd.direction)
    # while True:
    #     print(asd.step(int(input())))
    #     asd.printBoard()
    #     print(asd.best_move())
    for i in range(size):
        asd.step(asd.best_move())
        if asd.length == 0:
            asd = Game()
        board_array[i] = np.reshape(asd.board, asd.side ** 2)
        action_array[i] = asd.best_move()+1
    np.save("board", board_array)
    np.save("action", action_array)
    print("done")




