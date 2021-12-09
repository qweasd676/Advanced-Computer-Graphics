import sys
import numpy as np
import pywavefront
import cv2 
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from time import *
from pywavefront import visualization


# import pywavefront

# scene = pywavefront.Wavefront(
#     "test.obj",
#     create_materials=True,
#     collect_faces=True,
# )

# print("Faces:", scene.mesh_list[0].faces)
# print("Vertices:", scene.vertices)
# print("Format:", scene.mesh_list[0].materials[0].vertex_format)
# print("Vertices:", scene.mesh_list[0].materials[0].vertices)
windowWidth = 800
windowHeight = 600
lightAmbient = [ 0.5,0.5,0.5,1.0 ]
lightDiffuse = [ 0.9,0.9,0.9,1.0 ]
lightSpecular = [ 1.0,1.0,1.0, 1.0 ]
lightPosition = [ 0,1000,1000,1.0 ]
BIGimg = np.zeros( [6000,8000,3] , dtype = np.uint8)

class read_obj:

    def __init__(self,obj_name):
        self.meshes = pywavefront.Wavefront( obj_name, create_materials = True, collect_faces=True)
        self.np_meshes = np.array(list(self.meshes.vertices))

        self.right =  np.max(self.np_meshes[:,0])
        self.left =  np.min(self.np_meshes[:,0])
        self.high =  np.max(self.np_meshes[:,1])
        self.low =  np.min(self.np_meshes[:,1])
        self.far =  np.max(self.np_meshes[:,2])
        self.near =  np.min(self.np_meshes[:,2])
        self.rows,self.cols = self.np_meshes.shape
        self.center = self.np_meshes[int(np.around(self.rows/2)),:]

        # self.width = ( self.right + self.left )/(self.right - self.left)
        # self.height = ( self.high + self.low )/(self.high - self.low)
        

        self.width = (self.right + self.left)/8
        self.height = (self.high + self.low)/8

        self.znear = (np.abs(self.near)+(self.far-self.near))/(np.abs((self.near)+(self.far-self.near)))
    def postion(self):
        pass
        
def display():
    for i in range(10):
        for j in range(10):
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            # glLightfv(GL_LIGHT0, GL_POSITION, lightPosition)
            
            
            
            j_left = -windowWidth/400 + windowWidth/2000*j +0.00000000001
            j_right = -windowWidth/400 + windowWidth/2000*(j+1) 
            i_height = windowHeight/300 - windowHeight/1500*i + 0.00000000001
            i_bottom = windowHeight/300 - windowHeight/1500*(i+1)
            glViewport(0, 0, windowWidth, windowHeight)
            
            # Yashi
            glFrustum(j_left,j_right,i_bottom,i_height,obj_meshes.znear*2,np.abs(obj_meshes.near)+(obj_meshes.far-obj_meshes.near))
            gluLookAt((obj_meshes.left + obj_meshes.right)/2 + (obj_meshes.right - obj_meshes.left) ,(obj_meshes.high + obj_meshes.low) + (obj_meshes.high - obj_meshes.low)/2 ,(obj_meshes.far + obj_meshes.near)/2,(obj_meshes.left + obj_meshes.right)/2 ,(obj_meshes.high + obj_meshes.low)/2,(obj_meshes.far + obj_meshes.near)/2,0,0,1)

            # Sheep
            # glFrustum(j_left,j_right,i_bottom,i_height,obj_meshes.znear,np.abs(obj_meshes.near)+(obj_meshes.far-obj_meshes.near))
            # gluLookAt((obj_meshes.left + obj_meshes.right)/2 + (obj_meshes.right - obj_meshes.left),(obj_meshes.high + obj_meshes.low)/2 + (obj_meshes.high - obj_meshes.low),(obj_meshes.far + obj_meshes.near)/2 +(obj_meshes.far - obj_meshes.near)*4 ,(obj_meshes.left + obj_meshes.right)/2 ,(obj_meshes.high + obj_meshes.low)/2,(obj_meshes.far + obj_meshes.near)/2 +(obj_meshes.far + obj_meshes.near)/2,0,1,0)
            
            # Dog
            # glFrustum(j_left,j_right,i_bottom,i_height,obj_meshes.znear,np.abs(obj_meshes.near)+(obj_meshes.far-obj_meshes.near))
            # gluLookAt((obj_meshes.left + obj_meshes.right)/2 + (obj_meshes.right - obj_meshes.left) ,(obj_meshes.high + obj_meshes.low)/2 + (obj_meshes.high - obj_meshes.low) ,(obj_meshes.far + obj_meshes.near)/2,(obj_meshes.left + obj_meshes.right)/2 ,(obj_meshes.high + obj_meshes.low)/2,(obj_meshes.far + obj_meshes.near)/2,0,0,1)

            glEnable(GL_LIGHTING)  
            glPushMatrix()   
            visualization.draw(obj_meshes.meshes)
            glPopMatrix()
            glDisable(GL_LIGHTING)

            colorBuffer = (GLubyte * 1440000 )(0) # 1440000 == 800*600*3
            glReadPixels(0, 0, windowWidth, windowHeight, GL_BGR, GL_UNSIGNED_BYTE, colorBuffer)

            imgColorflip = np.fromstring(colorBuffer, np.uint8).reshape( 600, 800, 3 )
            imgColor = cv2.flip(imgColorflip, 0) 
            # cv2.imshow("dadas",imgColor)
            BIGimg[i*600:(i+1)*600,j*800:(j+1)*800] = imgColor
            glutSwapBuffers()
            glutPostRedisplay()
            # cv2.waitKey(100)

    # cv2.imshow('dasdas',BIGimg)
    cv2.imwrite('BIGimg.jpg',BIGimg)
    glutSwapBuffers()
    glutPostRedisplay()

    sleep(2)






def reshape(width,height):
    glViewport(0, 0, width, height)

def keyboard( key, x, y ):
    if key == esc:
        sys.exit()


if __name__ == "__main__":

    obj_meshes = read_obj('Yashi.obj')

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutCreateWindow(b'M10907305')
    glutReshapeWindow(windowWidth,windowHeight)
    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, lightAmbient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightAmbient)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightSpecular)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPosition)
    glutMainLoop()