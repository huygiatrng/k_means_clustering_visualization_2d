import math
import pygame
from random import randint
from sklearn.cluster import KMeans

# initialize all imported pygame modules
pygame.init()
# Set dimension
screen = pygame.display.set_mode((1200, 800))
# Set Caption
pygame.display.set_caption("kmeans visualization")

running = True
clock = pygame.time.Clock()

# Colors set
BACKGROUND = (191, 187, 187)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND_PANEL = (223, 218, 235)
ALGORITHM_BACKGROUND = (255, 255, 102)

RED = (204, 0, 0)
YELLOW = (255, 255, 153)
BLUE = (77, 77, 255)
GREEN = (0, 255, 0)
PURPLE = (255, 0, 255)
SKY = (0, 255, 255)
ORANGE = (255, 125, 25)
GRAPE = (100, 25, 125)
GRASS = (55, 155, 65)
PINK = (204, 0, 102)

COLORS = [RED, YELLOW, BLUE, GREEN, PURPLE, SKY, ORANGE, GRAPE, GRASS, PINK]

k = 1
error_number = 0
points = []
clusters = []
labels = []
error_1 = False
error_2 = False
error_3 = False


def distanceOfTwoPoints(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


# Render text
def render_text(string, size):
    font = pygame.font.SysFont('dejavuserif', size)
    return font.render(string, True, WHITE)


def render_Ktext(string, size):
    font = pygame.font.SysFont('comicsansms', size)
    return font.render(string, True, BLUE)


def render_Errortext(string, size):
    font = pygame.font.SysFont('comicsansms', size)
    return font.render(string, True, RED)


# Functions
def drawPanel():
    pygame.draw.rect(screen, BLACK, (50, 50, 800, 500))
    pygame.draw.rect(screen, BACKGROUND_PANEL, (55, 55, 790, 490))


def drawInterface():
    # PLUS AND MINUS BUTTONS
    pygame.draw.rect(screen, YELLOW, (855, 60, 200, 115))
    pygame.draw.rect(screen, BLACK, (1000, 68, 50, 50))
    pygame.draw.rect(screen, BLACK, (1000, 120, 50, 50))
    screen.blit(render_text('+', 40), (1013, 68))
    screen.blit(render_text('-', 40), (1017, 120))

    # RANDOM AND RUN BUTTONS
    pygame.draw.rect(screen, BLACK, (860, 190, 150, 50))
    pygame.draw.rect(screen, BLACK, (860, 260, 200, 50))
    screen.blit(render_text("RANDOM", 40), (873, 260))
    screen.blit(render_text("RUN", 40), (890, 190))

    # ALGORITHM AND RESET BUTTONS
    pygame.draw.rect(screen, BLACK, (50, 600, 390, 150))
    pygame.draw.rect(screen, ALGORITHM_BACKGROUND, (60, 610, 370, 130))
    pygame.draw.rect(screen, BLACK, (460, 600, 390, 150))
    pygame.draw.rect(screen, RED, (470, 610, 370, 130))
    pygame.draw.rect(screen, (0, 255, 255), (860, 340, 300, 150))
    screen.blit(render_text("RESET", 70), (550, 630))
    screen.blit(render_Ktext("ALGORITHM", 58), (65, 620))
    screen.blit(render_Ktext("Points = " + str(len(points)), 45), (870, 400))
    screen.blit(render_Ktext("Error = " + str(int(error_number)), 45), (870, 350))
    screen.blit(render_Ktext("K = " + str(k), 45), (870, 75))

    # Draw mouse position in panel
    if 55 < mouse_x < 845 and 55 < mouse_y < 545:
        screen.blit(render_Ktext("(" + str(mouse_x - 55) + ", " + str(mouse_y - 55) + ")", 11), (mouse_x + 10, mouse_y))


def drawError():
    global error_1
    global error_2
    if error_1 == True:
        screen.blit(render_Errortext("** Please press RANDOM before RUN **", 20), (200, 260))
    if error_2 == True:
        screen.blit(render_Errortext("** Please set Kmean greater than number of points **", 20), (200, 290))
    if error_3 == True:
        screen.blit(render_Errortext("** Please create points before using ALGORITHM **", 20), (200, 320))


def run():
    # Assign points to clusters and append label
    for point in points:
        listOfDistance = []
        for cluster in clusters:
            listOfDistance.append(distanceOfTwoPoints(point, cluster))
        labels.append(listOfDistance.index(min(listOfDistance)))

    # Update clusters positions

    for i in range(k):
        sumX = 0
        sumY = 0
        count = 0
        for j in range(len(points)):
            if labels[j] == i:
                sumX += points[j][0]
                sumY += points[j][1]
                count += 1
        if count != 0:
            clusters[i] = [int(sumX / count), int(sumY / count)]


def drawPoints():
    for point in points:
        pygame.draw.circle(screen, BLACK, (point[0] + 55, point[1] + 55), 6)
        pygame.draw.circle(screen, WHITE, (point[0] + 55, point[1] + 55), 5)


def drawLines():
    for i in range(len(labels)):
        pygame.draw.line(screen, COLORS[labels[i]], (points[i][0] + 55, points[i][1] + 55),
                         (clusters[labels[i]][0] + 55, clusters[labels[i]][1] + 55),
                         width=3)


def drawLabels():
    for i in range(len(labels)):
        pygame.draw.circle(screen, COLORS[labels[i]], (points[i][0] + 55, points[i][1] + 55), 5)


def random():
    for i in range(k):
        random_point = [randint(0, 790), randint(0, 490)]
        clusters.append(random_point)


def drawClusters():
    for i in range(len(clusters)):
        pygame.draw.circle(screen, BLACK, (clusters[i][0] + 55, clusters[i][1] + 55), 11)
        pygame.draw.circle(screen, COLORS[i], (clusters[i][0] + 55, clusters[i][1] + 55), 10)


def plus_K():
    if k + 1 > 10:
        return k
    else:
        return k + 1


def minus_K():
    if k - 1 < 1:
        return k
    else:
        return k - 1


def calculateErrorNumber():
    global error_number
    error_number = 0
    if clusters != [] and labels != []:
        for i in range(len(points)):
            error_number += distanceOfTwoPoints(points[i], clusters[labels[i]])


while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # Set FPS
    clock.tick(60)
    screen.fill(BACKGROUND)
    # Draw panel
    drawPanel()
    # Draw interface
    drawInterface()

    # End draw interface
    drawLines()
    drawPoints()
    drawLabels()
    drawClusters()
    drawError()

    # Check event if it is trying to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            error_1 = False
            error_2 = False
            error_3 = False
            if 1000 < mouse_x < 1050 and 68 < mouse_y < 118:
                k = plus_K();
                print("PLUS pressed")
            if 1000 < mouse_x < 1050 and 120 < mouse_y < 170:
                k = minus_K();
                print("MINUS pressed")
            if 860 < mouse_x < 1010 and 190 < mouse_y < 240:
                error_number = 0
                if clusters == [] or k > len(points):
                    if clusters == []:
                        error_1 = True
                        continue
                    if k > len(points):
                        error_2 = True
                        continue
                else:
                    error_1 = False
                    error_2 = False
                    calculateErrorNumber()
                    labels = []
                    run()
                print("RUN pressed")
            if 860 < mouse_x < 1060 and 260 < mouse_y < 310:
                error_number = 0
                labels = []
                clusters = []
                random()
                print("RANDOM pressed")
            if 50 < mouse_x < 440 and 600 < mouse_y < 750:
                if k > len(points) or len(points) == 0:
                    if len(points) == 0:
                        error_3 = True
                        continue
                    if k > len(points):
                        error_2 = True
                        continue
                else:
                    error_2 = False
                    error_3 = False
                    kmeans = KMeans(n_clusters=k).fit(points)
                    labels = kmeans.predict(points)
                    clusters = kmeans.cluster_centers_
                    error_number = 0
                    for i in range(len(points)):
                        error_number += distanceOfTwoPoints(points[i], clusters[labels[i]])
                    print("ALGORITHM pressed")
            if 460 < mouse_x < 850 and 600 < mouse_y < 750:
                labels = []
                points = []
                k = 1
                clusters = []
                error_number = 0

                print("RESET pressed")
            if 55 < mouse_x < 845 and 55 < mouse_y < 545:
                labels = []
                point = [mouse_x - 55, mouse_y - 55]
                points.append(point)
                print("ADD POINTS (" + str(mouse_x - 55) + ", " + str(mouse_y - 55) + ")")
    # DrawError

    # Update what happen to the windows (pygame screen)
    pygame.display.flip()

pygame.quit()
