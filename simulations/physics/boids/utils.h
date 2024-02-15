#include <random>

struct vector2 {
    float x, y;
    vector2(float x, float y) : x(x), y(y) {}
    vector2() : x(0), y(0) {}

    vector2 operator+(const vector2& p) const {
        return vector2(x + p.x, y + p.y);
    }

    vector2 operator/(const float& f) const {
        return vector2(x / f, y / f);
    }

    vector2 operator-(const vector2& p) const {
        return vector2(x - p.x, y - p.y);
    }

    vector2 operator*(const float& f) const {
        return vector2(x * f, y * f);
    }

    vector2 operator+=(const vector2& p) {
        x += p.x;
        y += p.y;
        return *this;
    }

    vector2 operator-=(const vector2& p) {
        x -= p.x;
        y -= p.y;
        return *this;
    }

    vector2 operator*=(const float& f) {
        x *= f;
        y *= f;
        return *this;
    }

    vector2 operator/=(const float& f) {
        x /= f;
        y /= f;
        return *this;
    }

    float distance(const vector2& p) const {
        return sqrt(pow(x - p.x, 2) + pow(y - p.y, 2));
    }

    float magnitude() const {
        return sqrt(x * x + y * y);
    }

    vector2 normalize() const {
        return *this / magnitude();
    }

    vector2 random_direction() const {
        return vector2(rand() % 100 - 50, rand() % 100 - 50).normalize();
    }

    vector2 set_magnitude(float mag) const {
        return normalize() * mag;
    }

    vector2 limit(float max) const {
        if (magnitude() > max) {
            return set_magnitude(max);
        }
        return *this;
    }
};

struct Color {
    float r, g, b;
    Color(float r, float g, float b) : r(r), g(g), b(b) {}
    Color() : r(0), g(0), b(0) {}

    Color random() const {
        return Color(rand() % 100 / 100.0, rand() % 100 / 100.0, rand() % 100 / 100.0);
    }
};