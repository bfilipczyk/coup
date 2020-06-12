"""This module defines GUI."""
import sys
import pygame

button_color = (106, 82, 80)
box_color = (74, 82, 80)


class Button:
    """Button class."""
    def __init__(self, color, x, y, width, height, text=''):
        """Inits object."""
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win):
        """Draws button."""
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

        if self.text != '':
            font = pygame.font.SysFont('Arial', 15)
            text = font.render(self.text, 1, (0, 0, 0))
            text_width, text_height = font.size(self.text)
            win.blit(text, (self.x + (self.width/2.0 - text_width/2.0), self.y + (self.height/2.0 - text_height/2.0)))

    def is_over(self, pos):
        """Checks if cursor is over button."""
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False


class GameGui:
    """Gui class."""
    def __init__(self):
        """Inits gui object."""
        self.screen = pygame.display.set_mode((800, 600))
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 15, bold=True)
        pygame.display.set_caption("coup")

        #drawing actions box
        pygame.draw.rect(self.screen, box_color, (0, 0, 230, 800))
        label = self.font.render("Actions:", 0, (0, 0, 0))
        self.screen.blit(label, (80, 30))
        #making button for each action
        self.b_usa = Button(button_color, 50, 60, 130, 30, 'USA')
        self.b_usa.draw(self.screen)
        self.b_local_businessmen = Button(button_color, 50, 130, 130, 30, 'Local Businessmen')
        self.b_local_businessmen.draw(self.screen)
        self.b_affair = Button(button_color, 50, 200, 130, 30, 'Affair')
        self.b_affair.draw(self.screen)
        self.b_media = Button(button_color, 50, 270, 130, 30, 'Media')
        self.b_media.draw(self.screen)
        self.b_protest = Button(button_color, 50, 340, 130, 30, 'Protest')
        self.b_protest.draw(self.screen)
        self.b_police = Button(button_color, 50, 410, 130, 30, 'Police')
        self.b_police.draw(self.screen)
        self.b_russia = Button(button_color, 50, 480, 130, 30, 'Russia')
        self.b_russia.draw(self.screen)
        self.card1 = None
        self.card2 = None
        self.card3 = None
        self.card4 = None

        #making challenge/block box
        pygame.draw.rect(self.screen, box_color, (570, 310, 230, 290))
        label = self.font.render("Challenge / Block:", 0, (0, 0, 0))
        self.screen.blit(label, (630, 340))
        #buttons
        self.b_yes = Button(button_color, 620, 400, 130, 30, 'Yes')
        self.b_yes.draw(self.screen)
        self.b_no = Button(button_color, 620, 505, 130, 30, 'No')
        self.b_no.draw(self.screen)

    def clear_middle(self, whole=True):
        """Clears messages in middle rectangle."""
        if whole:
            pygame.draw.rect(self.screen, box_color, (250, 180, 300, 220))
        else:
            pygame.draw.rect(self.screen, box_color, (335, 365, 145, 25))

    def refresh_players(self, money, cards, is_bot):
        """Refreshes informations about players."""
        if is_bot:
            pygame.draw.rect(self.screen, box_color, (250, 0, 300, 150))
            name_label = self.font.render("Bottimus", 0, (0, 0, 0))
            self.screen.blit(name_label, (370, 40))
            money_label = self.font.render('Money: ' + str(money), 0, (0, 0, 0))
            self.screen.blit(money_label, (300, 80))
            cards_label = self.font.render('Cards: ' + str(len(cards)), 0, (0, 0, 0))
            self.screen.blit(cards_label, (430, 80))
        else:
            pygame.draw.rect(self.screen, box_color, (250, 420, 300, 180))
            name_label = self.font.render("Player", 0, (0, 0, 0))
            self.screen.blit(name_label, (380, 430))
            money_label = self.font.render('Money: ' + str(money), 0, (0, 0, 0))
            self.screen.blit(money_label, (372, 455))
            cards_label = self.font.render('Cards: ', 0, (0, 0, 0))
            self.screen.blit(cards_label, (380, 480))
            amount = len(cards)
            self.card1 = Button(button_color, 260, 505, 130, 30, cards[0])
            self.card1.draw(self.screen)
            if amount >= 2:
                self.card2 = Button(button_color, 410, 505, 130, 30, cards[1])
                self.card2.draw(self.screen)
                if amount >= 3:
                    self.card3 = Button(button_color, 260, 550, 130, 30, cards[2])
                    self.card3.draw(self.screen)
                    if amount == 4:
                        self.card4 = Button(button_color, 410, 550, 130, 30, cards[3])
                        self.card4.draw(self.screen)
                    else:
                        self.card4 = None
                else:
                    self.card3 = None
                    self.card4 = None
            else:
                self.card2 = None
                self.card3 = None
                self.card4 = None

    def refresh_known_cards(self, cards):
        """Refreshes list of known cards."""
        pygame.draw.rect(self.screen, box_color, (570, 0, 230, 290))
        name_label = self.font.render("Known cards:", 0, (0, 0, 0))
        self.screen.blit(name_label, (630, 30))
        h_tmp = 80
        for card in cards:
            card_label = self.font.render(card, 0, (0, 0, 0))
            self.screen.blit(card_label, (650, h_tmp))
            h_tmp += 50

    def show_text(self, text_nr, name=None, action=None, choice=False):
        """Shows messages in middle."""
        if text_nr == 0:
            name_label = self.font.render("Not enough money", 0, (0, 0, 0))
            self.screen.blit(name_label, (340, 370))
        elif text_nr == 1:
            name_label = self.font.render(name + " chooses action:", 0, (0, 0, 0))
            self.screen.blit(name_label, (315, 195))
        elif text_nr == 2:
            name_label = self.font.render(action, 0, (0, 0, 0))
            self.screen.blit(name_label, (325, 220))
        elif text_nr == 3:
            name_label = self.font.render(name + " do you challenge?", 0, (0, 0, 0))
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
                name_label = self.font.render(name + " does blocks", 0, (0, 0, 0))
                self.screen.blit(name_label, (315, 335))
            else:
                name_label = self.font.render(name + " doesn't blocks", 0, (0, 0, 0))
                self.screen.blit(name_label, (315, 335))
        elif text_nr == 7:
            self.clear_middle()
            name_label = self.font.render("Choose cards to return", 0, (0, 0, 0))
            self.screen.blit(name_label, (315, 195))
        else:
            self.clear_middle()
            name_label = self.font.render(name+" won", 0, (0, 0, 0))
            self.screen.blit(name_label, (315, 195))

    def choose_action(self, money):
        """Checks which action player chooses."""
        while True:
            pygame.display.update()
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.b_usa.is_over(pos):
                        return 'usa'
                    if self.b_local_businessmen.is_over(pos):
                        return "local businessmen"
                    if self.b_affair.is_over(pos):
                        if money >= 7:
                            return "affair"
                        self.show_text(0)
                    if self.b_media.is_over(pos):
                        return "media"
                    if self.b_protest.is_over(pos):
                        if money >= 3:
                            return "protest"
                        self.show_text(0)
                    if self.b_police.is_over(pos):
                        return "police"
                    if self.b_russia.is_over(pos):
                        return 'russia'

    def choose_cards(self):
        """Checks which cards player returns."""
        while True:
            pygame.display.update()
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.card1.is_over(pos):
                        return 0
                    if self.card2.is_over(pos):
                        return 1
                    if self.card3 is not None:
                        if self.card3.is_over(pos):
                            return 2
                        if self.card3 is not None:
                            if self.card4.is_over(pos):
                                return 3

    def block_chall(self):
        """Checks if player blocks/challenges."""
        while True:
            pygame.display.update()
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.b_yes.is_over(pos):
                        return True
                    if self.b_no.is_over(pos):
                        return False

    def refresh(self):
        """Refreshes game screen."""
        pygame.display.update()

    def win_message(self, name):
        """Show win screen."""
        self.show_text(8, name)
        reset = Button(button_color, 335, 285, 130, 30, 'Restart')
        reset.draw(self.screen)
        while True:
            pygame.display.update()
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if reset.is_over(pos):
                        return True
