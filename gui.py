import pygame, sys


class Button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

        if self.text != '':
            font = pygame.font.SysFont('Arial', 15)
            text = font.render(self.text, 1, (0, 0, 0))
            text_width, text_height = font.size(self.text)
            win.blit(text, (self.x + (self.width/2.0 - text_width/2.0), self.y + (self.height/2.0 - text_height/2.0)))

    def IsOver(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False

class Game_gui():
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 15, bold=True)
        pygame.display.set_caption("coup")

        #drawing actions box
        pygame.draw.rect(self.screen, (74, 82, 80), (0, 0, 230, 800))
        label = self.font.render("Actions:", 0, (0, 0, 0))
        self.screen.blit(label, (80, 30))
        #making button for each action
        self.b_usa = Button((106, 82, 80), 50, 60, 130, 30, 'USA')
        self.b_usa.draw(self.screen)
        self.b_local_businessmen = Button((106, 82, 80), 50, 130, 130, 30, 'Local Businessmen')
        self.b_local_businessmen.draw(self.screen)
        self.b_affair = Button((106, 82, 80), 50, 200, 130, 30, 'Affair')
        self.b_affair.draw(self.screen)
        self.b_media = Button((106, 82, 80), 50, 270, 130, 30, 'Media')
        self.b_media.draw(self.screen)
        self.b_protest = Button((106, 82, 80), 50, 340, 130, 30, 'Protest')
        self.b_protest.draw(self.screen)
        self.b_police = Button((106, 82, 80), 50, 410, 130, 30, 'Police')
        self.b_police.draw(self.screen)
        self.b_russia = Button((106, 82, 80), 50, 480, 130, 30, 'Russia')
        self.b_russia.draw(self.screen)

        #making challange/block box
        pygame.draw.rect(self.screen, (74, 82, 80), (570, 310, 230, 290))
        label = self.font.render("Challange/Block:", 0, (0, 0, 0))
        self.screen.blit(label, (630, 340))
        #buttons
        self.b_yes = Button((106, 82, 80), 620, 400, 130, 30, 'Yes')
        self.b_yes.draw(self.screen)
        self.b_no = Button((106, 82, 80), 620, 505, 130, 30, 'No')
        self.b_no.draw(self.screen)



    def Refresh_Players(self, money, cards, is_bot):

        if is_bot:
            pygame.draw.rect(self.screen, (74, 82, 80), (250, 0, 300, 150))
            name_label = self.font.render("Bottimus", 0, (0, 0, 0))
            self.screen.blit(name_label, (370, 40))
            money_label = self.font.render('Money: ' + str(money), 0, (0, 0, 0))
            self.screen.blit(money_label, (300, 80))
            cards_label = self.font.render('Cards: ' + str(len(cards)), 0, (0, 0, 0))
            self.screen.blit(cards_label, (430, 80))
        else:
            pygame.draw.rect(self.screen, (74, 82, 80), (250, 450, 300, 150))
            name_label = self.font.render("Player", 0, (0, 0, 0))
            self.screen.blit(name_label, (380, 470))
            money_label = self.font.render('Money: ' + str(money), 0, (0, 0, 0))
            self.screen.blit(money_label, (372, 505))
            cards_label = self.font.render('Cards: ' + cards[0] + ' , ' + cards[1], 0, (0, 0, 0))
            self.screen.blit(cards_label, (305, 550))

    def Refresh_known_cards(self, cards):
        pygame.draw.rect(self.screen, (74, 82, 80), (570, 0, 230, 290))
        name_label = self.font.render("Known cards:", 0, (0, 0, 0))
        self.screen.blit(name_label, (630, 30))
        h_tmp = 80
        for card in cards:
            card_label = self.font.render(card, 0, (0, 0, 0))
            self.screen.blit(card_label, (650, h_tmp))
            h_tmp += 50

    def Choose_action(self):
        while True:
            pygame.display.update()
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(pos)
                    if self.b_usa.IsOver(pos):
                        print('usa')
                    if self.b_local_businessmen.IsOver(pos):
                        print('local_businessmen')
                    if self.b_affair.IsOver(pos):
                        print('affair')
                    if self.b_media.IsOver(pos):
                        print('media')
                    if self.b_protest.IsOver(pos):
                        print('protest')
                    if self.b_police.IsOver(pos):
                        print('police')
                    if self.b_russia.IsOver(pos):
                        print('russia')

    def loop(self):
        while True:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)




if __name__ == '__main__':
    g = Game_gui()
    g.Refresh_Players(2, ['Protest', 'Russia'], False)
    g.Refresh_Players(2, ['Protest', 'Russia'], True)
    g.Refresh_known_cards(['Protest', 'Russia', 'Protest', 'Russia'])
    g.Choose_action()
