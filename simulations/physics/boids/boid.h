#include "utils.h"
#include "quadTree.h"

#define SEPARATION_FORCE 1
#define COHESION_FORCE 1.0
#define ALIGNMENT_FORCE 2.5

struct Boid {
    double x, y;
    vector2 velocity = vector2().random_direction();
    vector2 position = vector2();
    vector2 acceleration = vector2();
    float maxSpeed = 1;
    float maxForce = 0.1;
    float r = 10;
    int id;
    float perceptionRadius = 25.0;
    Color random_color = Color().random();
    Color color = random_color;
    int color_mode = 1;

    Boid(double x, double y, int id, float maxSpeed, float maxForce, float perceptionRadius){
        this->x = x;
        this->y = y;
        this->id = id;
        this->maxSpeed = maxSpeed;
        this->maxForce = maxForce;
        this->perceptionRadius = perceptionRadius;
        position = vector2(x, y);
    }

    void update(vector<Boid>& neighbours){
        vector2 separationVector = vector2();
        vector2 alignmentVector = vector2();
        vector2 cohesionVector = vector2();
        for (auto& b : neighbours){
            if (b.id != id){
                float d = position.distance(b.position);
                if (d <= perceptionRadius){
                    vector2 diff = position - b.position;
                    diff /= d+1e-16;
                    separationVector += diff;
                }
                alignmentVector += b.velocity;
                cohesionVector += b.position;
            }
        }

        int total = neighbours.size();
        align(alignmentVector, total);
        cohesion(cohesionVector, total);
        separation(separationVector, total);
    }

    void align(vector2& steering, int total){
        if (total > 0){
            steering /= total;
            steering = steering.set_magnitude(maxSpeed);
            steering -= velocity;
            steering = steering.limit(maxForce);
        }
        acceleration += steering * ALIGNMENT_FORCE;
    }

    void cohesion(vector2& steering, int total){
        if (total > 0){
            steering /=  total;
            steering -=  position;
            steering = steering.set_magnitude(maxSpeed);
            steering -= velocity;
            steering = steering.limit(maxForce);
        }
        acceleration += steering * COHESION_FORCE;
    }

    void separation(vector2& steering, int total){
        if (total > 0){
            steering /=  total;
            steering = steering.set_magnitude(maxSpeed);
            steering -= velocity;
            steering = steering.limit(0.3);
        }
        acceleration += steering * SEPARATION_FORCE;
    }

    void flock(vector<Boid>& neighbours){
        update(neighbours);

        position += velocity;
        velocity += acceleration;
        velocity = velocity.limit(maxSpeed);
        acceleration *= 0;

        if (position.x > 1) position.x = -1;
        if (position.x < -1) position.x = 1;
        if (position.y > 1) position.y = -1;
        if (position.y < -1) position.y = 1;

    }
    
    void draw(){
        glPointSize(5);
        glColor3f(color.r, color.g, color.b);
        glBegin(GL_POINTS);
        
        glVertex2f(position.x, position.y);
        glEnd();
    }
};