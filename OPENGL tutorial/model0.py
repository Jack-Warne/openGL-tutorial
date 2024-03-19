import numpy as np
import glm
import pygame as pg

class cube:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.vbo = self.getVBO()
        self.shaderProgram = self.get_shader_program('default')
        self.vao = self.getVAO()
        self.m_model = self.getModelMatrix()
        self.texture = self.get_texture(path = 'textures/test.png')
        self.on_init()
    
    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        #texture.fill('red')
        texture = self.ctx.texture(size=texture.get_size(), components=3,
                                   data = pg.image.tostring(texture, 'RGB'))
        return texture


    def getModelMatrix(self):
        m_model = glm.mat4()
        return m_model
    def on_init(self):
        # light
        self.shaderProgram['light.position'].write(self.app.light.position)
        self.shaderProgram['light.Ia'].write(self.app.light.Ia)
        self.shaderProgram['light.Id'].write(self.app.light.Id)
        self.shaderProgram['light.Is'].write(self.app.light.Is)
        # texture 
        self.shaderProgram['u_texture_0'] = 0
        self.texture.use()
        # mvp
        self.shaderProgram['m_proj'].write(self.app.camera.m_proj)
        self.shaderProgram['m_view'].write(self.app.camera.m_view)
        self.shaderProgram['m_model'].write(self.m_model)
    
    def update(self):
        m_model = glm.rotate(self.m_model, self.app.time * 0.5, glm.vec3(0,1,0))
        self.shaderProgram['m_model'].write(m_model)
        self.shaderProgram['m_view'].write(self.app.camera.m_view)
        self.shaderProgram['camPos'].write(self.app.camera.position)
    def render (self):
        self.update()
        self.vao.render()
    def destroy (self):
        self.vbo.release()
        self.shaderProgram.release()
        self.vao.release()
        # destroy all resources we have created as there is no garbage collector in openGl
    def getVAO(self):
        vao = self.ctx.vertex_array(self.shaderProgram, 
                                    [(self.vbo, '2f 3f 3f', 'in_textcoord_0', 'in_normal','in_position')])
        ''' 
        "3f" is the buffer format, in the buffer each vertex is assigned three float numbers 
        and this group of numbers corresponds to an input attribute called "in_position"
        '''
        return vao
    def getVertexData(self):
        vertices = [(-1,-1,1),  (1,-1,1), (1,1,1), (-1,1,1),
                       (-1,1,-1),  (-1,-1,-1), (1,-1,-1),  (1,1,-1)]
        # the first four sets are for the front square vertices counter clockwise starting at the bottom left (index 0) to top left (index 3)
        # the second four are the back square vertices counter clockwise starting at the top left (index 4) to top right (index 7)
        indices = [(0, 2, 3), (0, 1, 2),
                   (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]
        # in opengl the way of describing vertices is by default anti-clockwise
        
        vertex_data = self.getData(vertices, indices)

        ''' create the texture coordinates for each indice on a square being 1-4 for each square
            then using their indices to describe all the triangles on the cube,
            then use th enumpy model to combine the geometry data and texture coordinates data into one arrray'''
        tex_coord = [(0, 0), (1, 0), (1, 1), (0, 1)]
        tex_coord_indices = [(0, 2, 3), (0, 1, 2),
                             (0, 2, 3), (0, 1, 2),
                             (0, 1, 2), (2, 3, 0),
                             (2, 3, 0), (2, 0, 1),
                             (0, 2, 3), (0, 1, 2),
                             (3, 1, 2), (3, 0, 1),]
        tex_coord_data = self.getData(tex_coord, tex_coord_indices)

        '''Normals are when vertices with perpendicular surfaces, 
           this being our six faces of the cube.
           '''
        normals = [(0,0,1)*6,
                   (1,0,0)*6,
                   (0,0,-1)*6,
                   (-1,0,0)*6,
                   (0,1,0)*6,
                   (0,-1,0)*6,]
        normals = np.array(normals, dtype='f4').reshape(36,3)

        vertex_data = np.hstack([normals, vertex_data])
        vertex_data = np.hstack([tex_coord_data, vertex_data])
        return vertex_data
    
    @staticmethod
    def getData(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype="f4")  

    def getVBO(self):
        vertex_data = self.getVertexData()
        vbo = self.ctx.buffer(vertex_data)
        return vbo
    def get_shader_program(self, shader_name):
        with open(f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()
        with open(f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()
        program = self.ctx.program(vertex_shader = vertex_shader, fragment_shader = fragment_shader)
        return program
    
    class triangle:
        def __init__(self, app):
            self.app = app
            self.ctx = app.ctx
            self.vbo = self.getVBO()
            self.shaderProgram = self.get_shader_program('default')
            self.vao = self.getVAO()
        def render (self):
            self.vao.render()
        def destroy (self):
            self.vbo.release()
            self.shaderProgram.release()
            self.vao.release()
            # destroy all resources we have created as there is no garbage collector in openGl
        def getVAO(self):
            vao = self.ctx.vertex_array(self.shaderProgram, [(self.vbo, '3f', 'in_position')])
            ''' 
            "3f" is the buffer format, in the buffer each vertex is assigned three float numbers 
            and this group of numbers corresponds to an input attribute called "in_position"
            '''
            return vao
        def getVertexData(self):
            vertex_data = [(-0.6, -0.8, 0.0), (0.6, -0.8, 0.0), (0.6, 0.8, 0.0)]
            vertex_data = np.array(vertex_data, dtype="f4")
            return vertex_data
        def getVBO(self):
            vertex_data = self.getVertexData()
            vbo = self.ctx.buffer(vertex_data)
            return vbo
        def get_shader_program(self, shader_name):
            with open(f'shaders/{shader_name}.vert') as file:
                vertex_shader = file.read()
            with open(f'shaders/{shader_name}.frag') as file:
                fragment_shader = file.read()
            program = self.ctx.program(vertex_shader = vertex_shader, fragment_shader = fragment_shader)
            return program