#include <vector>
#include <cmath>
#include <GLFW/glfw3.h> 
#include <cstdio>

using namespace std;

struct Object {
    int id;
    double x, y;
    Object() : x(0), y(0) {}
    Object(double x, double y) : x(x), y(y) {}

    Object operator+(const Object& p) const {
        return Object(x + p.x, y + p.y);
    }

    Object operator/(const float& f) const {
        return Object(x / f, y / f);
    }
};


class QuadTree {
private:
    Object topLeft, botRight;

    QuadTree* NWTree;
    QuadTree* NETree;
    QuadTree* SWTree;
    QuadTree* SETree;
    static const int CAPACITY = 2;
    vector<Object> objects;
    bool subdivided = false;

public:
    QuadTree(Object topL, Object botR) {
        topLeft = topL;
        botRight = botR;
        NWTree = NETree = SWTree = SETree = nullptr;
    }

    bool inBoundary(Object p) {
        return (p.x >= topLeft.x &&
                p.x <= botRight.x &&
                p.y >= topLeft.y &&
                p.y <= botRight.y);
    }

    bool insert(Object p) {
        if (!inBoundary(p)) return false;

        if (objects.size() < CAPACITY) {
            objects.push_back(p);
            return true;
        }

        if (!subdivided) {
            subdivide();
            subdivided = true;
        }

        if (NWTree->insert(p)) return true;
        if (NETree->insert(p)) return true;
        if (SWTree->insert(p)) return true;
        if (SETree->insert(p)) return true;
    }

    bool contains(Object p) {
        if (!inBoundary(p)) return false;

        for (Object b : objects) {
            if (b.id = p.id) return true;
        }

        if (NWTree == nullptr) return false;

        if (NWTree->contains(p)) return true;
        if (NETree->contains(p)) return true;
        if (SWTree->contains(p)) return true;
        if (SETree->contains(p)) return true;
    }

    void subdivide() {
        Object mid = (topLeft + botRight) / 2.0;
        NWTree = new QuadTree(topLeft, mid);
        NETree = new QuadTree(Object(mid.x, topLeft.y), Object(botRight.x, mid.y));
        SWTree = new QuadTree(Object(topLeft.x, mid.y), Object(mid.x, botRight.y));
        SETree = new QuadTree(mid, botRight);
    }

    bool intersects(Object topL, Object botR) {
        return !(topL.x > botRight.x || botR.x < topLeft.x || topL.y > botRight.y || botR.y < topLeft.y);
    }

    vector<Object> queryRange(Object topL, Object botR) {
        vector<Object> points;
        if (!intersects(topL, botR)) return points;

        for (Object p : objects) {
            if (p.x >= topL.x && p.x <= botR.x && p.y >= topL.y && p.y <= botR.y) {
                points.push_back(p);
            }
        }

        if (NWTree == nullptr) return points;

        vector<Object> NWPoints = NWTree->queryRange(topL, botR);
        vector<Object> NEPoints = NETree->queryRange(topL, botR);
        vector<Object> SWPoints = SWTree->queryRange(topL, botR);
        vector<Object> SEPoints = SETree->queryRange(topL, botR);

        points.insert(points.end(), NWPoints.begin(), NWPoints.end());
        points.insert(points.end(), NEPoints.begin(), NEPoints.end());
        points.insert(points.end(), SWPoints.begin(), SWPoints.end());
        points.insert(points.end(), SEPoints.begin(), SEPoints.end());

        return points;
    }

    void draw() {

        glBegin(GL_LINES);
        glVertex2d(topLeft.x, topLeft.y);     // Top-left
        glVertex2d(botRight.x, topLeft.y);    // Top-right

        glVertex2d(botRight.x, topLeft.y);    // Top-right
        glVertex2d(botRight.x, botRight.y);   // Bottom-right

        glVertex2d(botRight.x, botRight.y);   // Bottom-right
        glVertex2d(topLeft.x, botRight.y);    // Bottom-left

        glVertex2d(topLeft.x, botRight.y);    // Bottom-left
        glVertex2d(topLeft.x, topLeft.y);     // Top-left
        glEnd();


        if (NWTree != nullptr) NWTree->draw();
        if (NETree != nullptr) NETree->draw();
        if (SWTree != nullptr) SWTree->draw();
        if (SETree != nullptr) SETree->draw();
    }
};