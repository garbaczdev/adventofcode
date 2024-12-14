package main

import (
	"fmt"
    "image/color"

	common "aoc2024-14/common"

	"github.com/hajimehoshi/ebiten/v2"
)


var MAP_SIZE = common.Vector2D{X: 101, Y: 103}
var SCALE = 5

type Game struct {
    Robots []common.Robot
    MapSize common.Vector2D
    TurnNumber int
    robotsCountMap [][]int
}

// Update proceeds the game state.
func (g *Game) Update() error {
    if ebiten.IsKeyPressed(ebiten.KeyRight) {
        for robotIdx, _ := range g.Robots {
            g.Robots[robotIdx].Move(g.MapSize)
        }
        g.robotsCountMap = common.GetRobotsCountMap(g.Robots, g.MapSize)
        g.TurnNumber++
    }
    if ebiten.IsKeyPressed(ebiten.KeyLeft) {
        for robotIdx, _ := range g.Robots {
            g.Robots[robotIdx].MoveBack(g.MapSize)
        }
        g.robotsCountMap = common.GetRobotsCountMap(g.Robots, g.MapSize)
        g.TurnNumber--
    }
    return nil
}

func (g *Game) Draw(screen *ebiten.Image) {
    for y, row := range g.robotsCountMap {
        for x, count := range row {
            if count == 0 {
                continue
            }
            greenSquare := ebiten.NewImage(SCALE, SCALE)
            greenSquare.Fill(color.RGBA{0, 255, 0, 255})
            op := &ebiten.DrawImageOptions{}
            op.GeoM.Translate(float64(x*SCALE), float64(y*SCALE))
            screen.DrawImage(greenSquare, op)
        }
    }
    fmt.Printf("%d\r", g.TurnNumber)
}

// Layout takes the outside size (e.g., the window size) and returns the (logical) screen size.
// If you don't have to adjust the screen size with the outside size, just return a fixed size.
func (g *Game) Layout(outsideWidth, outsideHeight int) (screenWidth, screenHeight int) {
    return outsideWidth, outsideHeight
}


func main() {
    input := common.GetInput()
    robots := common.ParseInput(input)

    game := &Game{
        Robots: robots,
        MapSize: MAP_SIZE,
        TurnNumber: 0,
    }
    // Specify the window size as you like. Here, a doubled size is specified.
    ebiten.SetWindowSize(MAP_SIZE.X*SCALE, MAP_SIZE.Y*SCALE)
    ebiten.SetWindowTitle("Your game's title")
    // Call ebiten.RunGame to start your game loop.
    if err := ebiten.RunGame(game); err != nil {
        panic(err)
    }

}
