package main

type Vector2D struct {
    X int
    Y int
}

func (v Vector2D) Add(vOther Vector2D) Vector2D {
    return Vector2D{X: v.X + vOther.X, Y:v.Y + vOther.Y}
}

func (v Vector2D) Subtract(vOther Vector2D) Vector2D {
    return Vector2D{X: v.X - vOther.X, Y:v.Y - vOther.Y}
}

func (v Vector2D) Multiply(multiplier int) Vector2D {
    return Vector2D{X: v.X*multiplier, Y: v.Y*multiplier}
}

func (v Vector2D) Equals(vOther Vector2D) bool {
    return v.X == vOther.X && v.Y == vOther.Y
}

func (v Vector2D) ManhattanDistance() int {
    if v.X < 0 {
        v.X = -v.X
    } 

    if v.Y < 0 {
        v.Y = -v.Y
    } 

    return v.X + v.Y
}

func (v Vector2D) Normalize() Vector2D {
    if v.X > 0 {
        v.X = 1
    } else if v.X < 0 {
        v.X = -1
    }

    if v.Y > 0 {
        v.Y = 1
    } else if v.Y < 0 {
        v.Y = -1
    }

    return v
}

func (v Vector2D) RotateClockwise() Vector2D {
    return Vector2D{X: -v.Y, Y:v.X}
}

func (v Vector2D) RotateCounterClockwise() Vector2D {
    return Vector2D{X: v.Y, Y:-v.X}
}
