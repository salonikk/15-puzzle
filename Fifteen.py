import sys
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
from random import randint
import sounds


CELL_COUNT = 4
CELL_SIZE = 50
GRID_ORIGINX = 150
GRID_ORIGINY = 150
W_WIDTH = 500
W_HEIGHT = 500


class Fifteen(QWidget):
    def __init__(self):
        super().__init__()
        self.__board = [[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]]
        self.setWindowTitle('Fifteen')
        self.setGeometry(300, 300, W_WIDTH,W_HEIGHT)
        self.numinversions = 0
        self.solvable = False
        self.moves = 0
        self.movesstring = "moves: 0"
        self.stop = False
        while self.solvable is False:
            self.list = []
            self.listint = []
            numbers = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
            k = 15
            for i in range (0, 16):
                num = randint(0,k)
                self.list.append(str(numbers[num]))
                numbers.remove(numbers[num])
                k = k - 1
            print(self.list)
            for i in range(len(self.list)-1, -1, -1):
                 if self.list[i] == '16':
                     self.blanklocation = len(self.list)-i
                     print(self.blanklocation)
            for i in range(0, len(self.list)):
                x = int(self.list[i])
                if x != 16:
                    self.listint.append(x)
            print(self.listint)
            for i in range(len(self.listint)):
                for j in range(i+1, len(self.listint)):
                    if self.listint[j] < self.listint[i]:
                        self.numinversions += 1
            print(self.numinversions)
            if 5 <= self.blanklocation <= 8 or 13 <= self.blanklocation <= 16:
                if self.numinversions % 2 != 0:
                    self.solvable = True
                    print('solvable')
                    sounds.start(self)
                    self.show()
            if 1 <= self.blanklocation <= 4 or 9 <= self.blanklocation <= 12:
                if self.numinversions % 2 == 0:
                    self.solvable = True
                    print('solvable')
                    sounds.start(self)
                    self.show()
            else:
                self.solvable = False
                print('not solvable')


    def gameover(self):
        winning = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16']
        if self.list[0] == winning[0] and self.list[1] == winning[1] and self.list[2] == winning[2] and self.list[3] == winning[3] and self.list[4] == winning[4] and self.list[5] == winning[5] and self.list[6] == winning[6] and self.list[7] == winning[7] and self.list[8] == winning[8] and self.list[9] == winning[9] and self.list[10] == winning[10] and self.list[11] == winning[11] and self.list[12] == winning[12] and self.list[13] == winning[13] and self.list[14] == winning[14] and self.list[15] == winning[15]:
            return True
        else: return False

    def paintEvent(self,event):
        qp = QPainter()
        blackPen = QPen(QBrush(Qt.black), 1)
        qp.begin(self)
        qp.fillRect(event.rect(), Qt.white)

        qp.setPen(blackPen)
        index = 0
        for r in range(len(self.__board)):
            for c in range(len(self.__board[r])):
                    qp.drawRect(GRID_ORIGINX + c * CELL_SIZE, GRID_ORIGINY + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    if self.list[index] == '16':
                        pass
                    else:
                        qp.drawText(GRID_ORIGINX + 20 + c * CELL_SIZE, GRID_ORIGINY + 25 + r * CELL_SIZE, self.list[index])
                    qp.drawText(10, 20, self.movesstring)
                    index = index + 1
        if self.gameover() == True:
            qp.drawText(10, 40, 'Game Over!')
            sounds.make_sound(self)
        qp.end()


    def mousePressEvent(self,event):
        if self.gameover() == False:
            print(self.gameover)
            for i in range(len(self.list)-1, -1, -1):
                if self.list[i] == '16':
                    self.blankindex= i
                        #print(self.blankindex)
            self.blankrow = self.blankindex // 4
            for i in range (0, 4):
                if self.blankindex == 0 + 4*i:
                    self.blankcol = 0
                if self.blankindex == 1 + 4*i:
                     self.blankcol = 1
                if self.blankindex == 2 + 4*i:
                    self.blankcol = 2
                if self.blankindex == 3 + 4*i:
                    self.blankcol = 3
            print(self.blankrow, self.blankcol)
            row = (event.y() - GRID_ORIGINY) // CELL_SIZE
            col = (event.x() - GRID_ORIGINX) // CELL_SIZE
            self.clickindex = int(4*row + col)
            #print(self.clickindex)
            if row > 4 or row < 0 or col > 4 or col < 0:
                pass
            else:
                #print("row: ", row, "column: ", col)
                #print(self.movesstring)
                if row == self.blankrow:
                    sounds.move(self)
                    if self.blankcol == col + 1 or self.blankcol == col - 1:
                        a = self.clickindex
                        b = self.blankindex
                        self.list[self.blankindex] = self.list[a]
                        self.list[self.clickindex] = '16'
                        self.blankindex = a
                        self.clickindex = b
                        self.moves += 1
                        self.movesstring = "moves: " + str(self.moves)

                    elif self.blankcol > col:
                        if self.blankindex == 3 + 4*row:
                            a = self.blankindex
                            b = self.blankindex - 1
                            c = self.blankindex - 2
                            d = self.blankindex - 3
                            self.list[self.blankindex] = self.list[b]
                            self.list[self.blankindex-1] = self.list[c]
                            self.list[self.blankindex-2] = self.list[d]
                            self.blankindex = 4*row + 0
                            self.list[self.blankindex] = '16'
                            self.moves += 3
                            self.movesstring = "moves: " + str(self.moves)
                        if self.blankindex == 2 + 4*row:
                            a = self.blankindex
                            b = self.blankindex - 1
                            c = self.blankindex - 2
                            self.list[self.blankindex] = self.list[b]
                            self.list[self.blankindex-1] = self.list[c]
                            self.blankindex = 4*row + 0
                            self.list[self.blankindex] = '16'
                            self.moves += 2
                            self.movesstring = "moves: " + str(self.moves)
                    elif self.blankcol < col:
                        if self.blankindex == 0 + 4*row:
                            a = self.blankindex
                            b = self.blankindex + 1
                            c = self.blankindex + 2
                            d = self.blankindex + 3
                            self.list[self.blankindex] = self.list[b]
                            self.list[self.blankindex+1] = self.list[c]
                            self.list[self.blankindex+2] = self.list[d]
                            self.blankindex = 4*row + 3
                            self.list[self.blankindex] = '16'
                            self.moves += 3
                            self.movesstring = "moves: " + str(self.moves)
                        if self.blankindex == 1 + 4*row:
                            a = self.blankindex
                            b = self.blankindex + 1
                            c = self.blankindex + 2
                            self.list[self.blankindex] = self.list[b]
                            self.list[self.blankindex+1] = self.list[c]
                            self.blankindex = 4*row + 3
                            self.list[self.blankindex] = '16'
                            self.moves += 2
                            self.movesstring = "moves: " + str(self.moves)


                elif col == self.blankcol:
                    sounds.move(self)
                    if self.blankrow == row + 1 or self.blankrow == row - 1:
                        a = self.clickindex
                        b = self.blankindex
                        self.list[self.blankindex] = self.list[a]
                        self.list[self.clickindex] = '16'
                        self.blankindex = a
                        self.clickindex = b
                        print("blankindex", self.blankindex)
                        self.moves += 1
                        self.movesstring = "moves: " + str(self.moves)

                    elif self.blankrow > row:
                        if self.blankindex == 12 + col:
                            a = self.blankindex
                            b = self.blankindex - 4*1
                            c = self.blankindex - 4*2
                            d = self.blankindex - 4*3
                            self.list[self.blankindex] = self.list[b]
                            self.list[self.blankindex-4*1] = self.list[c]
                            self.list[self.blankindex-4*2] = self.list[d]
                            self.blankindex = col + 0
                            self.list[self.blankindex] = '16'
                            self.moves += 3
                            self.movesstring = "moves: " + str(self.moves)
                        if self.blankindex == 8 + col:
                            a = self.blankindex
                            b = self.blankindex - 4*1
                            c = self.blankindex - 4*2
                            self.list[self.blankindex] = self.list[b]
                            self.list[self.blankindex-4*1] = self.list[c]
                            self.blankindex = col + 0
                            self.list[self.blankindex] = '16'
                            self.moves += 2
                            self.movesstring = "moves: " + str(self.moves)
                    elif self.blankrow < row:
                        if self.blankindex == 0 + col:
                            a = self.blankindex
                            b = self.blankindex + 4*1
                            c = self.blankindex + 4*2
                            d = self.blankindex + 4*3
                            self.list[self.blankindex] = self.list[b]
                            self.list[self.blankindex+4*1] = self.list[c]
                            self.list[self.blankindex+4*2] = self.list[d]
                            self.blankindex = col + 3*4
                            self.list[self.blankindex] = '16'
                            self.moves += 3
                            self.movesstring = "moves: " + str(self.moves)
                        if self.blankindex == 4 + col:
                            a = self.blankindex
                            b = self.blankindex + 4*1
                            c = self.blankindex + 4*2
                            self.list[self.blankindex] = self.list[b]
                            self.list[self.blankindex+4*1] = self.list[c]
                            self.blankindex = col + 3*4
                            self.list[self.blankindex] = '16'
                            self.moves += 2
                            self.movesstring = "moves: " + str(self.moves)
            if self.gameover() is True:
                pass

        self.update()




if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = Fifteen()
  sys.exit(app.exec_())
