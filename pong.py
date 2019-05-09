import tkinter as tk
from threading import Thread
from time import time, sleep

# Fun facts:
# Max frames per seconds: ~2500000


def center_window(root):
    w = 800
    h = 600
    # get screen width and height
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # calculate position x, y
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))


# TODO: rename class to GameEngine?


class EventHandler:
    def __init__(self, paddle, ball):  # TODO: change params to one App param
        self.paddle = paddle
        self.ball = ball
        self.state = None
        self.thread = None

    # TODO: rename to input handler
    def eventHandler(self, event):
        char = event.char
        state = str(event.type)
        if char == "s":
            if state == "KeyPress":
                self.state = "moveUp"
            else:
                self.state = "still"

        elif char == "w":
            if state == "KeyPress":
                self.state = "moveDown"
            else:
                self.state = "still"

        else:
            pass
        print(event.type, event.char)

    def detectCollisions(self):
        # Ball
        if self.ball.x >= 800 or self.ball.x <= 0:
            self.ball.bounce("y")

        elif self.ball.y <= 0:
            if self.ball.vy < 0:
                self.ball.bounce("x")
        elif self.ball.y >= 600:
            if self.ball.vy > 0:
                self.ball.bounce("x")

        else:
            # Paddle - the +3 is from the ball
            if self.ball.y - self.paddle.y <= 23:
                if self.ball.vx > 0:
                    # and abs(self.ball.y - self.paddle.y) <= 20:
                    if 5 <= self.paddle.x - self.ball.x <= 10:
                        self.ball.bounce("y")
                else:
                    if 5 <= self.ball.x - self.paddle.x <= 10:
                        self.ball.bounce("y")

                    # Check win/lose

    def _run(self):
        iters = 0
        startTime = time()
        # while t - startTime < 1:
        while True:
            if self.state == "moveUp":
                if self.paddle.y + self.paddle.step + 20 < 600:
                    self.paddle.moveUp()

            elif self.state == "moveDown":
                if self.paddle.y - self.paddle.step - 20 >= 0:
                    self.paddle.moveDown()

            self.ball.move()
            self.detectCollisions()
            # t = time()
            # iters += 1
            newTime = time()
            iters += 1
            if newTime - startTime > 1:
                print("FPS:", iters)
                iters = 0
                startTime = newTime
            sleep(0.02)
        # print("iterations:", iters)
        # canvas.update_idletasks()

    def run(self):
        self.thread = Thread(target=self._run)
        # Thread stops when program exits
        self.thread.daemon = True
        self.thread.start()


# Size: 10x40 px


class Paddle:
    step = 10

    def __init__(self, x, y, canvas):
        self.x = x
        self.y = y
        self.canvas = canvas
        self.id = None

        # still, moveUp, moveDown
        self.state = "still"

    def draw(self):
        x, y = self.x, self.y
        self.id = self.canvas.create_rectangle(
            x-5, y-20, x+5, y+20, fill="white")

    def erase(self):
        self.canvas.delete(self.id)
        self.id = None

    def moveUp(self):
        self.y += self.step
        self.erase()
        self.draw()

    def moveDown(self):
        self.y -= self.step
        self.erase()
        self.draw()


class Ball:
    step = 2

    def __init__(self, x, y, vx, vy, canvas):
        self.x = x
        self.y = y
        self.canvas = canvas

        self.vx = vx
        self.vy = vy

        self.id = None

    def draw(self):
        x, y = self.x, self.y
        self.id = self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="white")

    def erase(self):
        self.canvas.delete(self.id)
        self.id = None

    def move(self):
        # Four walls
        self.x += self.vx * self.step
        self.y += self.vy * self.step
        self.erase()
        self.draw()

    # axis is either "x" or "y"
    def bounce(self, axis):
        if axis == "x":
            self.vy *= -1
        elif axis == "y":
            self.vx *= -1

    def getRandomSpeed(self):
        pass

    def getRandomDirection(self):
        pass


if __name__ == "__main__":
    # Prototyping
    root = tk.Tk()
    root.title("Pong")

    canvas = tk.Canvas(root, bg="black")

    canvas.pack(fill="both", expand=True)

    paddle = Paddle(50, 50, canvas)
    paddle.draw()

    ball = Ball(100, 100, 1, 1, canvas)
    ball.draw()

    game = EventHandler(paddle, ball)

    center_window(root)
    canvas.bind("<Key>", game.eventHandler)
    # TODO - method in EventHandler
    canvas.bind("<KeyRelease>", game.eventHandler)
    canvas.focus_set()
    # root.protocol('WM_DELETE_WINDOW', lambda: terminate(root, game))
    game.run()

    root.resizable(False, False)
    root.mainloop()
