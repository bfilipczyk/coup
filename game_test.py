from game import Game


def main():
    game = Game()
    while True:
        game.reset()
        winner = game.play()
        print("Player ", winner, " won the game")
        print("Input -stop- to end the game")
        if input() == "stop":
            break


if __name__ == '__main__':
    main()


