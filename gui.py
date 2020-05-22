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
        self.c1 = None
        self.c2 = None
        self.c3 = None
        self.c4 = None

        #making challange/block box
        pygame.draw.rect(self.screen, (74, 82, 80), (570, 310, 230, 290))
        label = self.font.render("Challange / Block:", 0, (0, 0, 0))
        self.screen.blit(label, (630, 340))
        #buttons
        self.b_yes = Button((106, 82, 80), 620, 400, 130, 30, 'Yes')
        self.b_yes.draw(self.screen)
        self.b_no = Button((106, 82, 80), 620, 505, 130, 30, 'No')
        self.b_no.draw(self.screen)

    def Clear_Middle(self, whole=True):
        if whole:
            pygame.draw.rect(self.screen, (74, 82, 80), (250, 180, 300, 220))
        else:
            pygame.draw.rect(self.screen, (74, 82, 80), (335, 365, 145, 25))

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
            pygame.draw.rect(self.screen, (74, 82, 80), (250, 420, 300, 180))
            name_label = self.font.render("Player", 0, (0, 0, 0))
            self.screen.blit(name_label, (380, 430))
            money_label = self.font.render('Money: ' + str(money), 0, (0, 0, 0))
            self.screen.blit(money_label, (372, 455))
            cards_label = self.font.render('Cards: ', 0, (0, 0, 0))
            self.screen.blit(cards_label, (380, 480))
            amount = len(cards)
            self.c1 = Button((106, 82, 80), 260, 505, 130, 30, cards[0])
            self.c1.draw(self.screen)
            if amount >= 2:
                self.c2 = Button((106, 82, 80), 410, 505, 130, 30, cards[1])
                self.c2.draw(self.screen)
                if amount >= 3:
                    self.c3 = Button((106, 82, 80), 260, 550, 130, 30, cards[2])
                    self.c3.draw(self.screen)
                    if amount == 4:
                        self.c4 = Button((106, 82, 80), 410, 550, 130, 30, cards[3])
                        self.c4.draw(self.screen)
                    else:
                        self.c4 = None
                else:
                    self.c3 = None
                    self.c4 = None
            else:
                self.c2 = None
                self.c3 = None
                self.c4 = None

    def Refresh_known_cards(self, cards):
        pygame.draw.rect(self.screen, (74, 82, 80), (570, 0, 230, 290))
        name_label = self.font.render("Known cards:", 0, (0, 0, 0))
        self.screen.blit(name_label, (630, 30))
        h_tmp = 80
        for card in cards:
            card_label = self.font.render(card, 0, (0, 0, 0))
            self.screen.blit(card_label, (650, h_tmp))
            h_tmp += 50

    def Show_text(self, text_nr, name=None, action=None, choice=False):
        if text_nr == 0:
            name_label = self.font.render("Not enough money", 0, (0, 0, 0))
            self.screen.blit(name_label, (340, 370))
        elif text_nr == 1:
            name_label = self.font.render(name + " choses action:", 0, (0, 0, 0))
            self.screen.blit(name_label, (315, 195))
        elif text_nr == 2:
            name_label = self.font.render(action, 0, (0, 0, 0))
            self.screen.blit(name_label, (325, 220))
        elif text_nr == 3:
            name_label = self.font.render(name + " do you challange?", 0, (0, 0, 0))
            self.screen.blit(name_label, (315, 245))
        elif text_nr == 4:
            if choice:
                name_label = self.font.render(name + " challenges", 0, (0, 0, 0))
                self.screen.blit(name_label, (315, 275))
            else:
                name_label = self.font.render(name + " doesn't challenges", 0, (0, 0, 0))
                self.screen.blit(name_label, (315, 275))
        elif text_nr == 5:
            name_label = self.font.render(name + " do you block?", 0, (0, 0, 0))
            self.screen.blit(name_label, (315, 305))
        elif text_nr == 6:
            if choice:
                name_label = self.font.render(name + " doesn't blocks", 0, (0, 0, 0))
                self.screen.blit(name_label, (315, 335))
            else:
                name_label = self.font.render(name + " doesn't blocks", 0, (0, 0, 0))
                self.screen.blit(name_label, (315, 335))
        elif text_nr == 7:
            self.Clear_Middle()
            name_label = self.font.render("Choose cards to return", 0, (0, 0, 0))
            self.screen.blit(name_label, (315, 195))
        else:
            self.Clear_Middle()
            name_label = self.font.render(name+" won", 0, (0, 0, 0))
            self.screen.blit(name_label, (315, 195))

    def Choose_action(self, money):
        while True:
            pygame.display.update()
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.b_usa.IsOver(pos):
                        return 0
                    if self.b_local_businessmen.IsOver(pos):
                        return 1
                    if self.b_affair.IsOver(pos):
                        if money >= 7:
                            return 2
                        else:
                            self.Show_text(0)
                    if self.b_media.IsOver(pos):
                        return 3
                    if self.b_protest.IsOver(pos):
                        if money >= 3:
                            return 4
                        else:
                            self.Show_text(0)
                    if self.b_police.IsOver(pos):
                        return 5
                    if self.b_russia.IsOver(pos):
                        return 6

    def Choose_cards(self):
        while True:
            pygame.display.update()
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.c1.IsOver(pos):
                        return 0
                    if self.c2.IsOver(pos):
                        return 1
                    if self.c3.IsOver(pos):
                        return 2
                    if self.c4.IsOver(pos):
                        return 3

    def Block_Chall(self):
        while True:
            pygame.display.update()
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.b_yes.IsOver(pos):
                        return 1
                    if self.b_no.IsOver(pos):
                        return 0

    def Refresh(self):
        pygame.display.update()

    def Win_message(self, name):
        self.Show_text(8, name)
        reset = Button((106, 82, 80), 335, 285, 130, 30, 'Restart')
        reset.draw(self.screen)
        while True:
            pygame.display.update()
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if reset.IsOver(pos):
                        return True


