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

func (v Vector2D) RotateClockwise() Vector2D {
    return Vector2D{X: -v.Y, Y:v.X}
}

func (v Vector2D) RotateCounterClockwise() Vector2D {
    return Vector2D{X: v.Y, Y:-v.X}
}

