import tkinter as tk
import math

# Window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400

# Sine wave parameters
AMPLITUDE = 50  # Height of the sine wave
FREQUENCY = 0.02  # Number of cycles per pixel

# Animation parameters
FRAMERATE = 30  # Frames per second
LINE_SPEED = 5  # Speed of the vertical line (pixels per frame)

class SineWaveApp:

    def __init__(self, root):
        # target vars
        self.target = WINDOW_HEIGHT // 2
        # pid vars
        self.x = 10
        self.y = 100
        self.lx = 100
        self.ly = 100
        self.ya = 0
        self.kP = 0.003
        self.kI = 0.003
        self.kD = 0.003
        self.lP = 0
        self.lI = 0
        self.lD = 0
        self.P = 0
        self.I = 0
        self.D = 0

        # self.error=0
        self.setpoint = 0
        self.previous_error = 0
        self.integral = []

        #
        self.mp = (0,0)


        """Initialize the window and canvas."""
        self.root = root
        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg='white')
        self.canvas.pack()
        
        self.canvas.bind('<Motion>', self.update_mp)

        # Draw the initial horizontal line and sine wave
        self.draw_horizontal_line()
        # self.draw_sine_wave()
        
        # Vertical line state
        self.vertical_line_x = 0  # Initial position of the vertical line

        # Start the animation
        self.animate()
    
    def update_mp(self, event):
        self.mp = (event.x, event.y)

    def draw_horizontal_line(self):
        """Draws a horizontal line in the middle of the window."""
        y_center = WINDOW_HEIGHT // 2
        self.canvas.create_line(0, y_center, WINDOW_WIDTH, y_center, fill='blue', width=2)
    
    def draw_sine_wave(self):
        """Draws a sine wave across the window."""
        y_center = WINDOW_HEIGHT // 2
        points = []

        for x in range(WINDOW_WIDTH):
            y = y_center + AMPLITUDE * math.sin(FREQUENCY * x)
            points.append((x, y))
        
        for i in range(1, len(points)):
            x1, y1 = points[i - 1]
            x2, y2 = points[i]
            self.canvas.create_line(x1, y1, x2, y2, fill='red', width=2)

    def animate(self):
        #
        my = self.mp[1]
        self.target = my
        # last
        self.lx = self.x
        self.ly = self.y
        self.lP = self.P
        self.lI = self.I
        self.lD = self.D

        # P
        error = self.target - self.y
        self.P = self.kP * error
        # I
        self.integral.append(error*(1/FRAMERATE))
        if(len(self.integral)>30):
            self.integral.pop(0) 
        self.I = self.kI * sum(self.integral) 
        # D
        self.D = self.kD * (error - self.previous_error) / (1/FRAMERATE)

        output = self.P+self.I+self.D
        self.ya += output
        self.y  += self.ya

        self.previous_error = error

        # circle
        cir_x1 = self.x-2
        cir_y1 = self.y-2
        cir_x2 = self.x+2
        cir_y2 = self.y+2
        # draw!
        self.x+=LINE_SPEED
        if self.x>WINDOW_WIDTH:
            self.x=0
            self.canvas.create_rectangle(0,0,WINDOW_WIDTH,WINDOW_HEIGHT,fill='white')
        self.canvas.create_line(self.lx,self.ly,self.x,self.y,fill='black',width=2)
        self.canvas.create_oval(cir_x1,cir_y1,cir_x2,cir_y2,outline='black',width=1)
        
        m=100
        self.canvas.create_line(self.lx,self.lP*m+WINDOW_HEIGHT/2,self.x,self.P*m+WINDOW_HEIGHT/2,fill='red',width=1)
        self.canvas.create_line(self.lx,self.lI*m+WINDOW_HEIGHT/2,self.x,self.I*m+WINDOW_HEIGHT/2,fill='green',width=1)
        self.canvas.create_line(self.lx,self.lD*m+WINDOW_HEIGHT/2,self.x,self.D*m+WINDOW_HEIGHT/2,fill='blue',width=1)

        self.canvas.create_rectangle(0,0,100,120,fill='white')
        self.canvas.create_text(30,20,text=f'P={round(self.P,2)}',fill='black',justify='left')
        self.canvas.create_text(30,40,text=f'I={round(self.I,2)}',fill='black',justify='left')
        self.canvas.create_text(30,60,text=f'D={round(self.D,2)}',fill='black',justify='left')
    
        # self.canvas.create_line(self.x,self.y,self.x+100,self.y+100,fill='red',width=1)


        """Animates the vertical line to move across the screen."""
        # Clear the previous vertical line
        self.canvas.delete('vertical_line')
        
        # Draw the new vertical line
        # self.canvas.create_line(self.vertical_line_x, 0, self.vertical_line_x, WINDOW_HEIGHT, 
        #                         fill='green', width=2, tags='vertical_line')
        
        # Move the vertical line
        self.vertical_line_x += LINE_SPEED
        if self.vertical_line_x > WINDOW_WIDTH:
            self.vertical_line_x = 0  # Reset the position to the left

        # Schedule the next frame
        self.root.after(int(1000 / FRAMERATE), self.animate)

def main():
    root = tk.Tk()
    root.title("Sine Wave Application with Moving Line")
    
    # Set the size of the window
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    # root.config(background='black')
    # Create the SineWaveApp
    app = SineWaveApp(root)
    
    # Start the application loop
    root.mainloop()

if __name__ == "__main__":
    main()