from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

IS_PERSPECTIVE = True  # 透视投影
VIEW = np.array([-0.8, 0.8, -0.8, 0.8, 1.0, 20.0])  # 视景体的left/right/bottom/top/near/far六个面
SCALE_K = np.array([1.0, 1.0, 1.0])  # 模型缩放比例
EYE = np.array([0.0, 0.0, 2.0])      # 眼睛的位置（默认z轴的正方向）
LOOK_AT = np.array([0.0, 0.0, 0.0])  # 瞄准方向的参考点（默认在坐标原点）
EYE_UP = np.array([0.0, 1.0, 0.0])  # 定义对观察者而言的上方（默认y轴的正方向）
WIN_W, WIN_H = 768, 768  # 保存窗口宽度和高度的变量
LEFT_IS_DOWNED = False  # 鼠标左键被按下
MOUSE_X, MOUSE_Y = 0, 0  # 考察鼠标位移量时保存的起始位置


def getposture():
    global EYE, LOOK_AT

    dist = np.sqrt(np.power((EYE - LOOK_AT), 2).sum())
    if dist > 0:
        phi = np.arcsin((EYE[1] - LOOK_AT[1]) / dist)
        theta = np.arcsin((EYE[0] - LOOK_AT[0]) / (dist * np.cos(phi)))
    else:
        phi = 0.0
        theta = 0.0

    return dist, phi, theta

DIST, PHI, THETA = getposture()  # 眼睛与观察目标之间的距离、仰角、方位角

#画环
def drawAnnulus(radiusOut, hTop, hDown, XStart = -0.5, YStart = 0.4):
    glBegin(GL_QUAD_STRIP)
    angle_stepsize = 0.05
    angle = 0.0
    while (angle < 2 * np.pi):
        x1 = radiusOut * np.cos(angle)
        y1 = radiusOut * np.sin(angle)
        glVertex3f(x1 + XStart, hTop, y1 + YStart)
        glVertex3f(x1 + XStart, hDown, y1 + YStart)
        angle = angle + angle_stepsize

    glEnd()

#封盖子
def drawTopAnnulus(radiusOut=0.3, radiusInner=0.1, hTop=0.6, XStart = -0.5, YStart = 0.4):
    angle = 0.0
    angle_stepsize = 0.05
    while (angle < 2 * np.pi):
        angle1 = angle + angle_stepsize
        glBegin(GL_QUAD_STRIP)

        x = radiusOut * np.cos(angle)
        y = radiusOut * np.sin(angle)
        glVertex3f(x + XStart, hTop, y + YStart)

        x = radiusOut * np.cos(angle1)
        y = radiusOut * np.sin(angle1)
        glVertex3f(x + XStart, hTop, y + YStart)

        x1 = radiusInner * np.cos(angle)
        y1 = radiusInner * np.sin(angle)
        glVertex3f(x1 + XStart, hTop, y1 + YStart)

        x1 = radiusInner * np.cos(angle1)
        y1 = radiusInner * np.sin(angle1)
        glVertex3f(x1 + XStart, hTop, y1 + YStart)

        x = radiusOut * np.cos(angle)
        y = radiusOut * np.sin(angle)
        glVertex3f(x + XStart, hTop, y + YStart)

        angle = angle1

        glEnd()

#定义环柱
def cylinder(AnnulusStartX = 0, AnnulusStartY = 0, hTop = 0.1, hDown = 0, radiusOut = 0.3, radiusInner = 0.05):
    # 圆环柱起始位置
    # 圆环柱高度
    # 半径


    # 定义jade材质
    # materiaJade()
    # 外环
    drawAnnulus(radiusOut=radiusOut, hTop=hTop, hDown=hDown, XStart=AnnulusStartX, YStart=AnnulusStartY)
    # 内环
    drawAnnulus(radiusOut=radiusInner, hTop=hTop, hDown=hDown, XStart=AnnulusStartX, YStart=AnnulusStartY)

    # 定义绿色材质
    # materiaGreen()
    # 盖子
    drawTopAnnulus(radiusOut=radiusOut, radiusInner=radiusInner, hTop=hTop, XStart=AnnulusStartX, YStart=AnnulusStartY)
    # 盖子
    drawTopAnnulus(radiusOut=radiusOut, radiusInner=radiusInner, hTop=hDown, XStart=AnnulusStartX, YStart=AnnulusStartY)

# light
def light():

    glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)

    light_position = [0, 0.8, 0, 1]
    light_ambient = [0.1, 0.1, 0.1, 1]
    light_diffuse = [0.2, 0.2, 0.2, 1]
    light_specular = [0.3, 0.3, 0.3, 1]

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    #glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, [0, -1, -1])
    glLightfv(GL_LIGHT0, GL_SPOT_EXPONENT, 0)
    #glLightfv(GL_LIGHT0, GL_SPOT_CUTOFF, 180)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)  # 表示该光源所发出的光，经过非常多次的反射后，最终遗留在整个光照环境中的强度
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)  # 表示该光源所发出的光，照射到粗糙表面时经过漫反射，所得到的光的强度
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)  # 表示该光源所发出的光，照射到光滑表面时经过镜面反射，所得到的光的强度

    light_position = [1, 1, 0, 1]
    light_ambient = [0.2, 0.2, 0.2, 1]
    light_diffuse = [0.2, 0.2, 0.2, 1]
    light_specular = [0.3, 0.3, 0.3, 1]
    glLightfv(GL_LIGHT1, GL_POSITION, light_position)
    glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient)  # 表示该光源所发出的光，经过非常多次的反射后，最终遗留在整个光照环境中的强度
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse)  # 表示该光源所发出的光，照射到粗糙表面时经过漫反射，所得到的光的强度
    glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular)  # 表示该光源所发出的光，照射到光滑表面时经过镜面反射，所得到的光的强度

    light_position = [-1, 1, 0, 1]
    light_ambient = [0.2, 0.2, 0.2, 1]
    light_diffuse = [0.2, 0.2, 0.2, 1]
    light_specular = [0.3, 0.3, 0.3, 1]
    glLightfv(GL_LIGHT2, GL_POSITION, light_position)
    glLightfv(GL_LIGHT2, GL_AMBIENT, light_ambient)  # 表示该光源所发出的光，经过非常多次的反射后，最终遗留在整个光照环境中的强度
    glLightfv(GL_LIGHT2, GL_DIFFUSE, light_ambient)  # 表示该光源所发出的光，照射到粗糙表面时经过漫反射，所得到的光的强度
    glLightfv(GL_LIGHT2, GL_SPECULAR, light_specular)  # 表示该光源所发出的光，照射到光滑表面时经过镜面反射，所得到的光的强度

    light_position = [0, 1, 1, 1]
    light_ambient = [0.2, 0.2, 0.2, 1]
    light_diffuse = [0.2, 0.2, 0.2, 1]
    light_specular = [0.3, 0.3, 0.3, 1]
    glLightfv(GL_LIGHT3, GL_POSITION, light_position)
    glLightfv(GL_LIGHT3, GL_AMBIENT, light_ambient)  # 表示该光源所发出的光，经过非常多次的反射后，最终遗留在整个光照环境中的强度
    glLightfv(GL_LIGHT3, GL_DIFFUSE, light_ambient)  # 表示该光源所发出的光，照射到粗糙表面时经过漫反射，所得到的光的强度
    glLightfv(GL_LIGHT3, GL_SPECULAR, light_specular)  # 表示该光源所发出的光，照射到光滑表面时经过镜面反射，所得到的光的强度

    light_position = [0, 1, -1, 1]
    light_ambient = [0.2, 0.2, 0.2, 1]
    light_diffuse = [0.2, 0.2, 0.2, 1]
    light_specular = [0.3, 0.3, 0.3, 1]
    glLightfv(GL_LIGHT4, GL_POSITION, light_position)
    glLightfv(GL_LIGHT4, GL_AMBIENT, light_ambient)  # 表示该光源所发出的光，经过非常多次的反射后，最终遗留在整个光照环境中的强度
    glLightfv(GL_LIGHT4, GL_DIFFUSE, light_ambient)  # 表示该光源所发出的光，照射到粗糙表面时经过漫反射，所得到的光的强度
    glLightfv(GL_LIGHT4, GL_SPECULAR, light_specular)  # 表示该光源所发出的光，照射到光滑表面时经过镜面反射，所得到的光的强度



    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)
    #glEnable(GL_LIGHT3)
    #glEnable(GL_LIGHT4)
    glEnable(GL_LIGHTING)

# 定义绿色材质
def materiaGreen():
    earth_mat_ambient = [0.0215, 0.1745, 0.0215, 1]
    earth_mat_diffuse = [0.07569, 0.6142, 0.07568, 1]
    earth_mat_specular = [0.633, 0.7278, 0.633, 1]
    earth_mat_shininess = 128*0.6
    glMaterialfv(GL_FRONT, GL_AMBIENT, earth_mat_ambient);
    glMaterialfv(GL_FRONT, GL_DIFFUSE, earth_mat_diffuse);
    glMaterialfv(GL_FRONT, GL_SPECULAR, earth_mat_specular);
    glMaterialf(GL_FRONT, GL_SHININESS, earth_mat_shininess);

# 定义jade材质
def materiaJade():
    earth_mat_ambient = [0.135, 0.2225, 0.1575, 1]
    earth_mat_diffuse = [0.54, 0.89, 0.63, 1]
    earth_mat_specular = [0.31623, 0.31623, 0.31623, 1]
    earth_mat_shininess = 128*0.1
    glMaterialfv(GL_FRONT, GL_AMBIENT, earth_mat_ambient);
    glMaterialfv(GL_FRONT, GL_DIFFUSE, earth_mat_diffuse);
    glMaterialfv(GL_FRONT, GL_SPECULAR, earth_mat_specular);
    glMaterialf(GL_FRONT, GL_SHININESS, earth_mat_shininess);

# 定义黑材质
def materiaBlackRubber():
    earth_mat_ambient = [0.02, 0.02, 0.02, 1]
    earth_mat_diffuse = [0.01, 0.01, 0.01, 1]
    earth_mat_specular = [0.04, 0.04, 0.04, 1]
    earth_mat_shininess = 128*0.25
    glMaterialfv(GL_FRONT, GL_AMBIENT, earth_mat_ambient);
    glMaterialfv(GL_FRONT, GL_DIFFUSE, earth_mat_diffuse);
    glMaterialfv(GL_FRONT, GL_SPECULAR, earth_mat_specular);
    glMaterialf(GL_FRONT, GL_SHININESS, earth_mat_shininess);

def materiaWhitePlastic():
    earth_mat_ambient = [0, 0, 0, 1]
    earth_mat_diffuse = [0.55, 0.55, 0.55, 1]
    earth_mat_specular = [0.7, 0.7, 0.7, 1]
    earth_mat_shininess = 128*0.25
    glMaterialfv(GL_FRONT, GL_AMBIENT, earth_mat_ambient);
    glMaterialfv(GL_FRONT, GL_DIFFUSE, earth_mat_diffuse);
    glMaterialfv(GL_FRONT, GL_SPECULAR, earth_mat_specular);
    glMaterialf(GL_FRONT, GL_SHININESS, earth_mat_shininess);

def materiaBlackRubber():
    earth_mat_ambient = [0.02, 0.02, 0.02, 1]
    earth_mat_diffuse = [0.01, 0.01, 0.01, 1]
    earth_mat_specular = [0.4, 0.4, 0.4, 1]
    earth_mat_shininess = 10
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, earth_mat_ambient);
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, earth_mat_diffuse);
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, earth_mat_specular);
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, earth_mat_shininess);

def materiaIron():
    mat_Ambient = [0.15, 0.15, 0.15, 1]
    mat_diffuse = [0.3, 0.3, 0.3, 1]
    mat_specular = [0.6, 0.6, 0.6, 1]  # 镜面反射参数
    mat_specular = [0.8, 0.8, 0.8, 1]  # 镜面反射参数
    mat_diffuse = [0.8, 0.8, 0.8, 1]
    mat_shiniess = [15]  # 高光指数

    mat_specular = [0.7, 0.7, 0.7, 1.0]  # 镜面反射参数
    mat_Ambient = [0.05, 0.05, 0.05, 1.0]
    mat_diffuse = [0.5, 0.5, 0.5, 1.0]
    mat_shiniess = [10]  # 高光指数
    # mat_emission = [0.2, 0.2, 0.2]

    # 材质属性
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_Ambient)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, mat_shiniess)

def materiaIron1():
    mat_Ambient = [0.15, 0.15, 0.15, 1]
    mat_diffuse = [0.3, 0.3, 0.3, 1]
    mat_specular = [0.6, 0.6, 0.6, 1]  # 镜面反射参数
    mat_shiniess = [15]  # 高光指数

    # 材质属性
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_Ambient)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, mat_shiniess)

#GLU画法
def newDraw():
    materiaIron1()

    # create quadric
    quadratic = gluNewQuadric()
    glTranslatef(0, 0.5, 0)        # 移动绘图原点到光源处

    # draw lower part of cylinder
    glRotatef(90, 1.0, 0.0, 0.0)
    #glTranslatef(0.0, 0.3, 0)
    gluDisk(quadratic, 0.05, 0.3, 128, 128)
    gluCylinder(quadratic, 0.3, 0.3, 0.1, 64, 64)
    gluCylinder(quadratic, 0.05, 0.05, 0.1, 64, 64)
    glTranslatef(0.0, 0, 0.1)
    gluDisk(quadratic, 0.05, 0.3, 128, 128)

    # draw middle part of cylinder
    gluCylinder(quadratic, 0.1, 0.1, 0.9, 64, 64)
    gluCylinder(quadratic, 0.05, 0.05, 0.9, 64, 64)

    # uper
    glTranslatef(0.0, 0, 0.9)
    gluDisk(quadratic, 0.05, 0.3, 64, 64)
    gluCylinder(quadratic, 0.3, 0.3, 0.1, 64, 64)
    gluCylinder(quadratic, 0.05, 0.05, 0.1, 64, 64)
    glTranslatef(0.0, 0, 0.1)
    gluDisk(quadratic, 0.05, 0.3, 64, 64)
    #glutSolidSphere(0.05, 50, 50)  # 绘制球


#画图函数
def display():
    #开启深度测试
    glClearColor(0.0, 0.0, 0.0, 1.0)  # 设置画布背景色。注意：这里必须是4个参数
    glEnable(GL_DEPTH_TEST)  # 开启深度测试，实现遮挡关系
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glDepthFunc(GL_LEQUAL)

    # 设置投影（透视投影）
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glFrustum(VIEW[0], VIEW[1], VIEW[2] * WIN_H / WIN_W, VIEW[3] * WIN_H / WIN_W, VIEW[4], VIEW[5])

    # 设置模型视图
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # 几何变换
    glScale(SCALE_K[0], SCALE_K[1], SCALE_K[2])

    # 设置视点
    gluLookAt(
        EYE[0], EYE[1], EYE[2],
        LOOK_AT[0], LOOK_AT[1], LOOK_AT[2],
        EYE_UP[0], EYE_UP[1], EYE_UP[2]
    )

    # 设置视口
    glViewport(0, 0, WIN_W, WIN_H)


    # 打光
    light()

    # 定义绿色材质
    materiaIron()

    #定义环柱
    #cylinder(AnnulusStartX=0, AnnulusStartY=0, hTop=0.4, hDown=0.3, radiusOut=0.3, radiusInner=0.05)
    #cylinder(AnnulusStartX=0, AnnulusStartY=0, hTop=0.3, hDown=-0.3, radiusOut=0.1, radiusInner=0.05)
    #cylinder(AnnulusStartX=0, AnnulusStartY=0, hTop=-0.3, hDown=-0.4, radiusOut=0.3, radiusInner=0.05)
    #glutSolidSphere(0.3, 100, 100) #球

    # GLU画法
    newDraw()

    #旋转
    # glTranslatef(0.3, -0.3, 0)
    #glRotatef(-20, 1.0, 0.0, 0.0)

    #glFlush()
    # ---------------------------------------------------------------
    glutSwapBuffers()  # 切换缓冲区，以显示绘制内容

def reshape(width, height):
    global WIN_W, WIN_H

    WIN_W, WIN_H = width, height
    glutPostRedisplay()

def mouseclick(button, state, x, y):
    global SCALE_K
    global LEFT_IS_DOWNED
    global MOUSE_X, MOUSE_Y

    MOUSE_X, MOUSE_Y = x, y
    if button == GLUT_LEFT_BUTTON:
        LEFT_IS_DOWNED = state == GLUT_DOWN
    elif button == 3:
        SCALE_K *= 1.05
        glutPostRedisplay()
    elif button == 4:
        SCALE_K *= 0.95
        glutPostRedisplay()

def mousemotion(x, y):
    global LEFT_IS_DOWNED
    global EYE, EYE_UP
    global MOUSE_X, MOUSE_Y
    global DIST, PHI, THETA
    global WIN_W, WIN_H

    if LEFT_IS_DOWNED:
        dx = MOUSE_X - x
        dy = y - MOUSE_Y
        MOUSE_X, MOUSE_Y = x, y

        PHI += 2 * np.pi * dy / WIN_H
        PHI %= 2 * np.pi
        THETA += 2 * np.pi * dx / WIN_W
        THETA %= 2 * np.pi
        r = DIST * np.cos(PHI)

        EYE[1] = DIST * np.sin(PHI)
        EYE[0] = r * np.sin(THETA)
        EYE[2] = r * np.cos(THETA)

        if 0.5 * np.pi < PHI < 1.5 * np.pi:
            EYE_UP[1] = -1.0
        else:
            EYE_UP[1] = 1.0

        glutPostRedisplay()

def keydown(key, x, y):
    global DIST, PHI, THETA
    global EYE, LOOK_AT, EYE_UP
    global IS_PERSPECTIVE, VIEW

    if key in [b'x', b'X', b'y', b'Y', b'z', b'Z']:
        if key == b'x':  # 瞄准参考点 x 减小
            LOOK_AT[0] -= 0.01
        elif key == b'X':  # 瞄准参考 x 增大
            LOOK_AT[0] += 0.01
        elif key == b'y':  # 瞄准参考点 y 减小
            LOOK_AT[1] -= 0.01
        elif key == b'Y':  # 瞄准参考点 y 增大
            LOOK_AT[1] += 0.01
        elif key == b'z':  # 瞄准参考点 z 减小
            LOOK_AT[2] -= 0.01
        elif key == b'Z':  # 瞄准参考点 z 增大
            LOOK_AT[2] += 0.01

        DIST, PHI, THETA = getposture()
        glutPostRedisplay()
    elif key == b'\r':  # 回车键，视点前进
        EYE = LOOK_AT + (EYE - LOOK_AT) * 0.9
        DIST, PHI, THETA = getposture()
        glutPostRedisplay()
    elif key == b'\x08':  # 退格键，视点后退
        EYE = LOOK_AT + (EYE - LOOK_AT) * 1.1
        DIST, PHI, THETA = getposture()
        glutPostRedisplay()

# main
if __name__ =='__main__':
   glutInit()
   glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
   glutInitWindowPosition(100, 100)
   glutInitWindowSize(WIN_W, WIN_H)
   glutCreateWindow("Create Cylinder")
   glClearColor(0.0, 0.0, 0.0, 0.0)
   glutDisplayFunc(display)
   glutReshapeFunc(reshape)  # 注册响应窗口改变的函数reshape()
   glutMouseFunc(mouseclick)  # 注册响应鼠标点击的函数mouseclick()
   glutMotionFunc(mousemotion)  # 注册响应鼠标拖拽的函数mousemotion()
   glutKeyboardFunc(keydown)  # 注册键盘输入的函数keydown()
   glutMainLoop()


#画圆形
# glBegin(GL_POLYGON)
# R = 0.5
# N = 100
# for i in range(N):
#     glVertex2f(R * np.cos(2 * np.pi / N * i), R * np.sin(2 * np.pi / N * i), 0);
# glEnd()