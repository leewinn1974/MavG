from kivy.app import App
from kivy.uix.progressbar import ProgressBar
from kivy.core.text import Label as CoreLabel
from kivy.lang.builder import Builder
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.clock import Clock


class CircularProgressBar(ProgressBar):

    def __init__(self, **kwargs):
        super(CircularProgressBar, self).__init__(**kwargs)

        # Set constant for the bar thickness
        self.thickness = 30

        # Create a direct text representation
        self.label = CoreLabel(text="0%", font_size=self.thickness)

        # Initialise the texture_size variable
        self.texture_size = None

        # Refresh the text
        self.refresh_text()

        # Redraw on innit
        self.draw()

    def draw(self):

        with self.canvas:
            
            # Empty canvas instructions
            self.canvas.clear()

            # Draw no-progress circle
            Color(0.26, 0.26, 0.26)
            Ellipse(pos=self.pos, size=self.size, angle_start =-90, angle_end =90)

            # Draw progress circle, small hack if there is no progress (angle_end = 0 results in full progress)

            Color(1, 0, 0)
            Ellipse(pos=self.pos, size=self.size, angle_start = -90,
                    angle_end = (0.01 if self.value_normalized == 0.5 else (self.value_normalized*180)-90))
                # This value needs to be 0.01 to fix a graphical rendering discontunity at 0

            # Draw the inner circle (colour should be equal to the background)
            Color(0, 0, 0)
            Ellipse(pos=(self.pos[0] + self.thickness / 2, self.pos[1] + self.thickness / 2),
                    size=(self.size[0] - self.thickness, self.size[1] - self.thickness))

            # Center and draw the progress text
            Color(1, 1, 1, 1)
            #added pos[0]and pos[1] for centralizing label text whenever pos_hint is set
            Rectangle(texture=self.label.texture, size=self.texture_size,
                  pos=(self.size[0] / 2 - self.texture_size[0] / 2 + self.pos[0], self.size[1] / 2 - self.texture_size[1] / 2 + self.pos[1]))


    def refresh_text(self):
        # Render the label
        self.label.refresh()

        # Set the texture size each refresh
        self.texture_size = list(self.label.texture.size)

    def set_value(self, value):
        # Update the progress bar value
        self.value = value

        # Update textual value and refresh the texture
        self.label.text = str(int(self.value_normalized*100)) + "%"
        self.refresh_text()

        # Draw all the elements
        self.draw()


class Main(App):

    # Simple animation to show the circular progress bar in action
    def animate(self, dt):
        if self.root.value < 80:
            self.root.set_value(self.root.value + 1)
        else:
            self.root.set_value(0)

    # Simple layout for easy example
    def build(self):
        container = Builder.load_string(
            '''CircularProgressBar:
    size_hint: (None, None)
    height: 200
    width: 200
    max: 80''')

        # Animate the progress bar
        Clock.schedule_interval(self.animate, 0.1)
        
        return container


if __name__ == '__main__':
    Main().run()