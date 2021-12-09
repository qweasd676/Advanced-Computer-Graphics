import numpy as np
import cv2 as cv

class  obj_parameter:
    def __init__(self):

        self.point_3D = np.zeros((21,21,3), dtype=float)
        self.index = np.zeros((21,21,), dtype=int)
        self.Reverse = 21 * 21
    def image_processing(self):
        self.img_FRONT = cv.imread("FRONT.JPG")
        self.img_REAR = cv.imread("REAR.JPG")
        self.img_combine = np.hstack((self.img_FRONT, self.img_REAR))
        cv.imwrite("image.JPG", self.img_combine)

    def define_mtl(self):# 輸入Kd ka ks illum Ns
        self.mtl = open("3D_VR.mtl",'w')
        self.mtl.write("newmtl 3D_VR\n")
        self.mtl.write("Kd 1.0 1.0 1.0\n")
        self.mtl.write("Ka 0.9 0.9 0.9\n")
        self.mtl.write("Ks 1.0 1.0 1.0\n")
        self.mtl.write("illum 2\n")
        self.mtl.write("Ns 25.6\n")
        self.mtl.write("map_Kd image.JPG\n")
        self.mtl.close()

def vector(start, end):
    v = end - start
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm


def obj_output(f,v,offset,postion):
    for i in range(21):
        for j in range(21):
            f.write('v {0} {1} {2}\n'.format(format(obj_.point_3D[i][j][0]*v, '.5f'),format(obj_.point_3D[i][j][1]*v, '.5f'),format(obj_.point_3D[i][j][2]*v, '.5f')))                                                                                    
            obj_.index[i][j] = i*21 + j + 1 + postion
    f.write("\n")

    for i in range(21):
        for j in range(21):
            standard_x = ((obj_.point_3D[i][j][0] * 0.75 + 200) / (2 * 200))/2 +offset
            standard_y = (v*obj_.point_3D[i][j][1] * 0.75 + 200) / (2 * 200)  
            f.write('vt {0} {1} 0\n'.format(format(standard_x, '.5f'),format(standard_y, '.5f')))                                       
    f.write("\n")

    for i in range(21):
        for j in range(21):
            normal_vector = vector(obj_.point_3D[i][j]*v, np.array([0,0,0]))
            f.write('vn {0} {1} {2}\n'.format(format(normal_vector[0], '.5f'),format(normal_vector[1], '.5f'),format(normal_vector[2], '.5f')))                                                                                
    f.write("\n")


    f.write("usemtl 3D_VR\n")
    for i in range(20):
        for j in range(20):
            if(postion == 0):
                f.write('f {0}/{1}/{2}'.format(obj_.index[i][j], obj_.index[i][j], obj_.index[i][j]))
                f.write(' {0}/{1}/{2}'.format(obj_.index[i][j+1], obj_.index[i][j+1], obj_.index[i][j+1]))
                f.write(' {0}/{1}/{2}\n'.format(obj_.index[i+1][j], obj_.index[i+1][j], obj_.index[i+1][j]))
                f.write('f {0}/{1}/{2}'.format(obj_.index[i+1][j], obj_.index[i+1][j], obj_.index[i+1][j]))
                f.write(' {0}/{1}/{2}'.format(obj_.index[i][j+1], obj_.index[i][j+1], obj_.index[i][j+1]))
                f.write(' {0}/{1}/{2}\n'.format(obj_.index[i+1][j+1], obj_.index[i+1][j+1], obj_.index[i+1][j+1]))
            else:
                f.write('f {0}/{1}/{2}'.format(obj_.index[i][j], obj_.index[i][j], obj_.index[i][j]))
                f.write(' {0}/{1}/{2}'.format(obj_.index[i+1][j], obj_.index[i+1][j], obj_.index[i+1][j]))
                f.write(' {0}/{1}/{2}\n'.format(obj_.index[i][j+1], obj_.index[i][j+1], obj_.index[i][j+1]))      
                f.write('f {0}/{1}/{2}'.format(obj_.index[i+1][j], obj_.index[i+1][j], obj_.index[i+1][j]))   
                f.write(' {0}/{1}/{2}'.format(obj_.index[i+1][j+1], obj_.index[i+1][j+1], obj_.index[i+1][j+1]))
                f.write(' {0}/{1}/{2}\n'.format(obj_.index[i][j+1], obj_.index[i][j+1], obj_.index[i][j+1]))

def obj_create():    
    for i in range(21):
        for j in range(21):           
            r = 200
            phi = np.pi /2 - np.pi*i/(2*20)
            theta = 2*np.pi*j/20
            x = r * np.cos(phi) * np.cos(theta)
            y = r * np.cos(phi) * np.sin(theta)
            z = r * np.sin(phi)
            obj_.point_3D[i][j] = np.array([x,y,z])

    f = open("3D_VR.obj",'w')
    f.write("mtllib 3D_VR.mtl\n")
    obj_output(f,1,0,0) #front
    obj_output(f,-1,0.5,obj_.Reverse) #rear
    f.close()

if __name__ == "__main__":
    obj_ = obj_parameter()
    obj_.image_processing()
    obj_.define_mtl()
    obj_create()
    


