import pygame as pg
import moderngl as mgl
import sys

class GraphicsEngine:
    def __init__(self, win_size =(1600,900)):
        
        #intitalise pygame  modules
        pg.init()
        
        # window size
        self.WIN_SIZE = win_size
        
        # set opengl attributes
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION , 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        
        # create opengl context
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF) 
        '''double buffering provides two complete colour buffers for use in drawing
        One buffer is displayed while the other is being drawn into.
        When the drawing is complete, the two buffers are swapped so the one for displaying is now for drawing and Vica Versa'''
        
        # detect and use existing openGL context
        self.ctx = mgl.create_context()
        
        # create an object to track time
        self.clock = pg.time.Clock()
    
    def checkEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
    def render(self):
        # clear frame buffer
        self.ctx.clear(color=(0.08, 0.16, 0.18))
        # swap buffers
        pg.display.flip()
        
    def run(self):
        while True:
            self.checkEvents()
            self.render()
            self.clock.tick(60)
            
if __name__ == '__main__':
    app = GraphicsEngine()
    app.run()        
        
        
