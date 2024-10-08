import pygame
from datetime import datetime


class InputBox:
    def __init__(self, x, y, w, h, passw=False, text=''):
        self.COLOR_INACTIVE = pygame.Color('lightskyblue3')
        self.COLOR_ACTIVE = pygame.Color('dodgerblue2')
        self.FONT = pygame.font.Font(None, 32)
        self.rect = pygame.Rect(x, y, w, h)
        self.color = self.COLOR_INACTIVE
        self.text = text
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.active = False
        self.passw = passw
        if passw:
            self.visible = False
        self.w = w
        



    def handle_event(self, event):
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                if not self.passw:
                    self.txt_surface = self.FONT.render(self.text, True, self.color)
                else:
                    if not self.visible:
                        self.txt_surface = self.FONT.render("*" * len(self.text), True, self.color)
                    else:
                        self.txt_surface = self.FONT.render(self.text, True, self.color)

    
    def get(self):
        return self.text
        

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.w, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

# Button Class
class Button:
    def __init__(self, win, x, y, text=None, color=None ,textcolor=(0, 0, 0), center = False, autofit= True, fontsize = 20, **kwargs):
        self.win, self.x, self.y, self.color, self.textcolor = win, x, y, color, textcolor

        if text != None: 
            self.text = text
            self.font = pygame.font.SysFont("comicsans", fontsize)
            self.textlabel = self.font.render(self.text, 1, self.textcolor)
            if not autofit: self.width, self.height = kwargs['size'] 
            else: 
                self.width, self.height = self.textlabel.get_size()
                self.width += 5
                self.height += 5
        if center:
            self.x = kwargs['screensize'][0]/2 - self.width/2
            self.y = kwargs['screensize'][1]/2 - self.height/2

    def draw(self):
        self.textlabel = self.font.render(self.text, 1, self.textcolor)
        x = self.x + self.width/2 - self.textlabel.get_size()[0]/2
        y = self.y + self.height/2 - self.textlabel.get_size()[1]/2
        if self.color != None:
            pygame.draw.rect(self.win, self.color, (self.x, self.y, self.width, self.height))
        self.win.blit(self.textlabel, (x , y))
        
    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 < self.y + self.height:
            return True
        else:
            return False
    
class Timer():
    """
    timer.start() - should start the timer
    timer.pause() - should pause the timer
    timer.resume() - should resume the timer
    timer.get() - should return the current time
    """

    def __init__(self):
        self.timestarted = None
        self.timepaused = None
        self.paused = False

    def start(self):
        """ Starts an internal timer by recording the current time """
        self.timestarted = datetime.now()

    def pause(self):
        """ Pauses the timer """
        if self.timestarted is None:
            raise ValueError("Timer not started")
        if self.paused:
            raise ValueError("Timer is already paused")
        self.timepaused = datetime.now()
        self.paused = True

    def resume(self):
        """ Resumes the timer by adding the pause time to the start time """
        if self.timestarted is None:
            raise ValueError("Timer not started")
        if not self.paused:
            return
        pausetime = datetime.now() - self.timepaused
        self.timestarted = self.timestarted + pausetime
        self.paused = False

    def get(self):
        """ Returns a timedelta object showing the amount of time
            elapsed since the start time, less any pauses """
        if self.timestarted is None:
            raise ValueError("Timer not started")
        if self.paused:
            return self.timepaused - self.timestarted
        else:
            return datetime.now() - self.timestarted
