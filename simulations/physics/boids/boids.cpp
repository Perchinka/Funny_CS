#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <vector>
#include "boid.h"


#define WIDTH 1400
#define HEIGHT 900
#define BOIDS_AMOUNT 3
#define MAX_SPEED 0.05
#define MAX_FORCE 1
#define PERCEPTION_RADIUS 25

std::vector<Boid> boids;
QuadTree* qtree = nullptr;

int main()
{
    if (!glfwInit())
        return -1;

    GLFWwindow* window = glfwCreateWindow(1400, 900, "GLFW", NULL, NULL);
    if (!window)
    {
        glfwTerminate();
        return -1;
    }

    for (int i = 0; i < BOIDS_AMOUNT; i++){
        float x = (rand() % WIDTH) / (0.5*WIDTH) - 1;
        float y = (rand() % HEIGHT) / (0.5*HEIGHT) - 1;
        Boid b(x, y, i, MAX_SPEED, MAX_FORCE, PERCEPTION_RADIUS);
        boids.push_back(b);
        printf("Boid %d: x = %f, y = %f\n", i, x, y);
    }

    glfwMakeContextCurrent(window);

    int windowWidth, windowHeight;
    glfwGetWindowSize(window, &windowWidth, &windowHeight);
    
    double widthRatio = 2.0 / windowWidth;
    double heightRatio = 2.0 / windowHeight;

    Object topLeft(widthRatio -1.0, heightRatio -1.0);
    Object botRight(widthRatio * windowWidth - 1.0, heightRatio * windowHeight - 1.0);

    // qtree = new QuadTree(topLeft, botRight);
    
    while (!glfwWindowShouldClose(window))
    {
        
        glClear(GL_COLOR_BUFFER_BIT);
        
        for (int i = 0; i < BOIDS_AMOUNT; i++){
            Boid& b = boids[i];
            b.flock(boids);
            b.draw();
        }

        // qtree->draw();
        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    // delete qtree;
    glfwTerminate();
    return 0;
}