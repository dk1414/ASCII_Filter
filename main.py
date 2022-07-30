
from math import ceil
from Button import Button
import pygame
import pygame.camera
from pygame.locals import *

pygame.init()
pygame.camera.init()


dark_to_light = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,`'.                      "


#maps a brightness value to a ascii character
def color_to_char(color):
    ratio = color/255
    return dark_to_light[-int(((len(dark_to_light) - 1) * ratio))]

#returns the average brightness for a group of one or more pixels
def get_average_color(pixels,surface):
    r = 0
    g = 0
    b = 0

    for pixel in pixels:
        color = surface.get_at((pixel[1],pixel[2]))
        r += color[0]
        g += color[1]
        b += color[2]


    return (r + g + b)/(len(pixels)*3)


#takes a pixel array and creates a new pixel array of ascii characters, can also reduce resolution by even factors
def color_to_brightness(pixel_array,dims,factor,surface):
    # initialize empty pixel array with new scaled dims
    x = dims[0]//factor
    y = dims[1]//factor

    new_pixel_array = [[None for i in range(y)] for j in range(x)]

    # now we need to take a factor x factor square of pixels from the pixel_array
    # and convert them into a single pixel in our new_pixel_array
    for row in range(x):
        for col in range(y):
            #pixels will store a group of pixels that will be converted to a single pixel, each will be a tuple that stores the pixel, and its location
            pixels = []

            #the size of the square of pixels to be converted is factor x factor
            for i in range(factor):
                for j in range(factor):
                    pixels.append((pixel_array[row * factor + i][col * factor + j],row * factor + i, col * factor + j))

            avg = get_average_color(pixels,surface)
            new_pixel_array[row][col] = avg
            pixels.clear()


    return new_pixel_array




class Capture(object):
    def __init__(self):

        #default size, value doesn't really matter since it will be changed
        self.size = (352,288)

        #resolution scaling factor, i'll start it a 2 since most webacams have pretty high resolution
        self.r_scaler = 2

        #will be a list of buttons to draw
        self.buttons_list = []


        # this is the same as what we saw before
        self.clist = pygame.camera.list_cameras()
        print(self.clist)

        if not self.clist:
            raise ValueError("Sorry, no cameras detected.")


        self.cam = pygame.camera.Camera(self.clist[0], self.size)

        self.cam.start()


        # create a surface to capture to.  for performance purposes
        # bit depth is the same as that of the display surface.
        self.size = self.cam.get_size()

        if self.size[0] > 500:
            div = 1400
        else:
            div = 1200

        #display width needs to be multiple of width for perfect fit
        scaler = ceil(div//self.size[0])
        self.display = pygame.display.set_mode((self.size[0]*scaler, self.size[1]*scaler), 0)
        pygame.display.set_caption("ASCII Filter")
        pygame_icon = pygame.image.load('icon.png')
        pygame.display.set_icon(pygame_icon)

        self.snapshot = pygame.surface.Surface(self.size, 0, self.display)


        self.chars = []

        self.font_size = 0
        self.font = None
        self.text_font = pygame.font.SysFont("impact", 25)





    def get_and_flip(self):
        # if you don't want to tie the framerate to the camera, you can check
        # if the camera has an image ready.  note that while this works
        # on most cameras, some will never return true.
        if self.cam.query_image():
            self.snapshot = self.cam.get_image(self.snapshot)

        #gets pixel array for the current image
        pixels_arr = pygame.PixelArray(self.snapshot)


        #sets our char list to be a version of pixels_arr where at each location, the brightness of the pixel is stored
        #this function can also reduce the number of pixels by an even scaling factor
        self.chars = color_to_brightness(pixels_arr,self.size,self.r_scaler,self.snapshot)
        pixels_arr.close()

        #determine font size that will make our image fit the screen
        self.font_size = self.display.get_width() // len(self.chars)
        self.font = pygame.font.SysFont("couriernew", self.font_size)


        #reset screen with black
        self.display.fill((0,0,0))

        #for each pixel in chars, replace the brightness with its respective character, then draw it to the screen
        for row,lst in enumerate(self.chars):
            for col,brightness in enumerate(lst):


                char = color_to_char(brightness)

                text = self.font.render(char, True, (255,255,255))
                text_rect = text.get_rect()
                text_rect.topleft = (row * self.font_size,col * self.font_size)
                self.display.blit(text, text_rect)


        for b in self.buttons_list:
            b.draw()





        res_text = self.text_font.render("Resolution", True, (255, 255, 255))
        res_text_rect = res_text.get_rect()
        res_text_rect.topleft = (100,self.display.get_height() - 85)
        self.display.blit(res_text,res_text_rect)




        pygame.display.flip()

    def change_r_scaler(self,num):

        if num > 0:
            if self.r_scaler == 1:
                self.r_scaler = 2
            elif self.r_scaler < 8:
                self.r_scaler += 2
        elif num < 0:
            if self.r_scaler == 2:
                self.r_scaler = 1
            elif self.r_scaler > 2:
                self.r_scaler += num



    def main(self):

        self.buttons_list.append(Button(self.display, "<", 25, 25, (72, self.display.get_height() - 80),lambda: self.change_r_scaler(2)))
        self.buttons_list.append(Button(self.display, ">", 25, 25, (215, self.display.get_height() - 80),lambda: self.change_r_scaler(-2)))

        going = True
        while going:
            events = pygame.event.get()
            for e in events:
                if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                    # close the camera safely
                    self.cam.stop()
                    going = False

            self.get_and_flip()


if __name__ == "__main__":
    cap = Capture()
    cap.main()