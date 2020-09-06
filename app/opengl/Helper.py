from OpenGL.GL import *


def drawXYZaxis():

    glBegin(GL_LINES)

    # z-axis green
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-0.1, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)

    # y-axis green
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, 0.1, 0.0)
    glVertex3f(0.0, 0.0, 0.0)

    # x-axis green
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, 0.1)
    glVertex3f(0.0, 0.0, 0.0)
    glEnd()


def drawBbox(pos, neg):

    glBegin(GL_LINES)

    #
    glVertex3f(pos[0], pos[1], pos[2])
    glVertex3f(pos[0], pos[1], neg[2])

    glVertex3f(pos[0], pos[1], pos[2])
    glVertex3f(pos[0], neg[1], pos[2])

    glVertex3f(pos[0], pos[1], pos[2])
    glVertex3f(neg[0], pos[1], pos[2])

    #
    glVertex3f(neg[0], neg[1], neg[2])
    glVertex3f(pos[0], neg[1], neg[2])

    glVertex3f(neg[0], neg[1], neg[2])
    glVertex3f(neg[0], neg[1], pos[2])

    glVertex3f(neg[0], neg[1], neg[2])
    glVertex3f(neg[0], pos[1], neg[2])

    #
    glVertex3f(pos[0], pos[1], neg[2])
    glVertex3f(pos[0], neg[1], neg[2])

    glVertex3f(neg[0], neg[1], pos[2])
    glVertex3f(neg[0], pos[1], pos[2])

    #
    glVertex3f(pos[0], neg[1], pos[2])
    glVertex3f(pos[0], neg[1], neg[2])

    glVertex3f(pos[0], neg[1], pos[2])
    glVertex3f(neg[0], neg[1], pos[2])

    #
    glVertex3f(neg[0], pos[1], neg[2])
    glVertex3f(neg[0], pos[1], pos[2])

    glVertex3f(neg[0], pos[1], neg[2])
    glVertex3f(pos[0], pos[1], neg[2])

    glEnd()
