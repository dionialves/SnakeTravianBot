import sys
import time
import curses


class App:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.menu = ["Aldeias", "Auto Send FarmList", "Monitor"]
        self.menu_is_open = True
        self.menu_is_selected = 0

        self.menu_set_village = ["Debian", "Arch"]
        self.menu_set_village_is_open = False
        self.menu_set_village_is_selected = 0

        self.village = ''
        self.fields = {}
        self.slots_enabled_for_update = []
        self.fields['Debian'] = {'slot': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 
                                    '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', 
                                    '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', 
                                    '31', '32', '33', '34', '35', '36', '37', '38', '39', '40'], 
                                    'id': ['1', '4', '1', '3', '2', '2', '3', '4', '4', '3', 
                                    '3', '4', '4', '1', '4', '2', '1', '2', '0', '19', 
                                    '20', '22', '23', '10', '23', '15', '0', '11', '13', '17', 
                                    '25', '8', '23', '6', '0', '18', '0', '0', '16', '33'], 
                                'name': ['Bosque', 'Campo de cereais', 'Bosque', 'Mina de ferro', 
                                    'Po�o de Barro', 'Po�o de Barro', 'Mina de ferro', 
                                    'Campo de cereais', 'Campo de cereais', 'Mina de ferro', 
                                    'Mina de ferro', 'Campo de cereais', 'Campo de cereais', 
                                    'Bosque', 'Campo de cereais', 'Po�o de Barro', 'Bosque', 
                                    'Po�o de Barro', 'Zona Livre', 'Quartel', 'Cavalaria', 
                                    'Academia', 'Esconderijo', 'Armaz�m', 'Esconderijo', 
                                    'Edif�cio Principal', 'Zona Livre', 'Celeiro', 'Casa de ferragens', 
                                    'Mercado', 'Resid�ncia', 'Moinho', 'Esconderijo', 'Alvenaria', 
                                    'Zona Livre', 'Embaixada', 'Zona Livre', 'Zona Livre', 
                                    'Ponto de reuni�o militar', 'Pali�ada'], 
                                'level': ['9', '10', '9', '9', '9', '9', '9', '10', '10', '9', '9', 
                                    '10', '9', '9', '9', '10', '9', '10', '0', '10', '10', '6', 
                                    '10', '13', '10', '17', '0', '12', '5', '14', '10', '1', 
                                    '10', '1', '0', '1', '0', '0', '10', '10']}
                                
        self.menu_village = ["Recursos e Edifícios", "Atualizar Aldeia", "Treino de Infantaria", "Treino de Cavalaria"]
        self.menu_village_is_open = False
        self.menu_village_is_selected = 0

        self.menu_resources_and_buildings_is_open = False
        self.menu_update_village_is_open = False

        self.footer = {'(Q)uit': 'q'}
        self.menu_title = ["Menu Principal"]
        self.initial_line_menu = 7
        self.height = 35
        self.width = 80
        self.line = 0

    def run(self):
        curses.curs_set(0)  # Oculta o cursor
        while True:
            self.stdscr.clear()
            curses.start_color()

            # Define as dimensões desejadas da tela (altura, largura)
            self.stdscr.resize(self.height, self.width)

            # Centralize a janela na tela
            y, x = (curses.LINES - self.height) // 2, (curses.COLS - self.width) // 2
            self.stdscr.mvwin(y, x)

            # Desenha as bordas
            self.stdscr.box()

            # Header
            self.stdscr.addstr(1, 2, 'Server:')
            self.stdscr.addstr(2, 2, 'Account:')
            self.stdscr.addstr(3, 2, f'Aldeia: {self.village}')
            self.set_line(self.initial_line_menu-4)
            self.set_menu_title(line=self.initial_line_menu-3)

            # Menus
            if self.menu_is_open:
                self.set_menu(self.initial_line_menu)

            elif self.menu_set_village_is_open:
                self.set_menu_set_village(self.initial_line_menu)

            elif self.menu_village_is_open:
                self.set_menu_village(self.initial_line_menu)
            
            elif self.menu_resources_and_buildings_is_open:
                self.page_resources_and_buildins(self.initial_line_menu)

            elif self.menu_update_village_is_open:
                self.page_update_village(self.initial_line_menu)

            # shortcuts
            self.set_footer()




            self.stdscr.refresh()
            key = self.stdscr.getch()
            
            self.set_shortcuts(key)
            

    def set_menu_title(self, line, add_title=''):
        if add_title:
            self.menu_title.append(add_title)
        
        menu_title = ''
        for i, title in enumerate(self.menu_title):
            if i == 0:
                menu_title = title
            else:
                menu_title = f'{menu_title} -> {title}'
        self.stdscr.addstr(line, 2, menu_title)

    def set_menu(self, line):
        for i, menu in enumerate(self.menu):
            if i == self.menu_is_selected:
                self.stdscr.addstr(i+line, 2, menu, curses.A_REVERSE)
            else:
                self.stdscr.addstr(i+line, 2, menu)

    def set_menu_set_village(self, line):
        for i, menu in enumerate(self.menu_set_village):
            if i == self.menu_set_village_is_selected:
                self.stdscr.addstr(i+line, 2, menu, curses.A_REVERSE)
            else:
                self.stdscr.addstr(i+line, 2, menu)

    def set_menu_village(self, line):
        for i, menu in enumerate(self.menu_village):
            if i == self.menu_village_is_selected:
                self.stdscr.addstr(i+line, 2, menu, curses.A_REVERSE)
            else:
                self.stdscr.addstr(i+line, 2, menu)
    
    def page_resources_and_buildins(self, line):

        list = []
        positionY_01 = line
        positionY_02 = line
        positionX = 2
        for slot in range(0, 40):
            if slot < 9:
                text = f'Id: {slot+1} - ({self.fields[self.village]["level"][int(slot)]}) {self.fields[self.village]["name"][int(slot)]}'
            else:
                text = f'Id:{slot+1} - ({self.fields[self.village]["level"][int(slot)]}) {self.fields[self.village]["name"][int(slot)]}'

            if slot < 18:
                self.stdscr.addstr(positionY_01, positionX, text)
                positionY_01 += 1
                self.slots_enabled_for_update.append(str(slot+1))
            
            elif self.fields[self.village]["level"][int(slot)] != '0' and slot > 17:
                self.stdscr.addstr(positionY_02, positionX+35, text)
                positionY_02 += 1
                self.slots_enabled_for_update.append(str(slot+1))
            
    def page_update_village(self, line):
        self.stdscr.addstr(line, 2, "Pressione a letre (u) para atualizar!")

    def set_line(self, line):
            maxy, maxx = self.stdscr.getmaxyx()
            width_line = int(0.96 * maxx)

            self.stdscr.hline(line, 2, curses.ACS_HLINE, width_line)

    def set_footer(self):
        shortcuts = ''
        for key in self.footer.keys():

            shortcuts = f'{shortcuts}{key}  '
        
        maxy, maxx = self.stdscr.getmaxyx()
        width_line = int(0.96 * maxx)

        self.stdscr.hline(self.height - 3, 2, curses.ACS_HLINE, width_line)
        self.stdscr.addstr(self.height - 2, 2, shortcuts)

    def set_shortcuts(self, key):
        if key == ord('q'):
            self.quit()

        elif key == ord('v'):
            if self.menu_set_village_is_open:
                self.menu_set_village_is_open = False
                self.menu_is_open = True
                del self.footer["voltar"]
                del self.menu_title[-1]

            elif self.menu_village_is_open:
                self.menu_village_is_open = False
                self.menu_set_village_is_open = True
                self.initial_line_menu = 7

            elif self.menu_resources_and_buildings_is_open:
                self.menu_resources_and_buildings_is_open = False
                self.menu_village_is_open = True
                del self.footer["(U)pgrade"]
                del self.footer["(E)m Andamento"]
                del self.footer["(T)odos os Recursos"]
                del self.menu_title[-1]

            elif self.menu_update_village_is_open:
                self.menu_update_village_is_open = False
                self.menu_village_is_open = True
                del self.footer["(U)pdate"]
                del self.menu_title[-1]

        elif key == ord('u'):
            if self.menu_resources_and_buildings_is_open:
                curses.curs_set(1)

                self.stdscr.addstr(28, 2, "Escolha o ID a ser evoluido:")
                curses.echo()

                slot_id = self.stdscr.getstr(28, 31, 30 ).decode('utf-8')
                self.stdscr.addstr(29, 2, "Para qual level:")
                curses.echo()

                to_level = self.stdscr.getstr(29, 19, 30 ).decode('utf-8')
                curses.noecho()
                curses.curs_set(0)
                
                if slot_id.isdigit() and to_level.isdigit() and slot_id in self.slots_enabled_for_update:

                    #logica para chamar a thread de construção
                    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
                    self.stdscr.addstr(30, 2, 'Ordem de construção adicionado na fila', curses.color_pair(1))
                    self.stdscr.refresh()
                    time.sleep(3)
                    
                else:
                    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
                    self.stdscr.addstr(30, 2, 'Erro ao adicionar na fila, verifique os dados informados!', curses.color_pair(1))
                    self.stdscr.refresh()
                    time.sleep(3)

            elif self.menu_update_village_is_open:
                # Criar logina para atualização da aldeia.
                # Seria interessante mostrar o processo de atualização
                # Poderia ser uma barra com % ou mesmo printar os campos sendo atualziados
                pass

        elif self.menu_is_open:
            if key == curses.KEY_DOWN and self.menu_is_selected < len(self.menu) - 1:
                    self.menu_is_selected += 1

            elif key == curses.KEY_UP and self.menu_is_selected > 0:
                self.menu_is_selected -= 1

            elif key == curses.KEY_ENTER or key == 10:
                if self.menu_is_selected == 0:
                    self.menu_set_village_is_open = True
                    self.menu_is_open = False

                    self.menu_title.append('Aldeias')
                    self.footer['(V)oltar'] = 'v'
                    
        elif self.menu_set_village_is_open:
            if key == curses.KEY_DOWN and self.menu_set_village_is_selected < len(self.menu_village) - 1:
                    self.menu_set_village_is_selected += 1

            elif key == curses.KEY_UP and self.menu_set_village_is_selected > 0:
                self.menu_set_village_is_selected -= 1

            elif key == curses.KEY_ENTER or key == 10:
                self.village = self.menu_set_village[self.menu_set_village_is_selected]
                self.menu_set_village_is_open = False
                self.menu_village_is_open = True
                self.initial_line_menu = 8

        elif self.menu_village_is_open:
            if key == curses.KEY_DOWN and self.menu_village_is_selected < len(self.menu_village) - 1:
                    self.menu_village_is_selected += 1

            elif key == curses.KEY_UP and self.menu_village_is_selected > 0:
                self.menu_village_is_selected -= 1

            elif key == curses.KEY_ENTER or key == 10:
                # Menu Resources and Buildings
                if self.menu_village_is_selected == 0:

                    # Desativa o menu da aldeia
                    self.menu_village_is_open = False
                    # Ativa a pagina Resources and Buildings
                    self.menu_resources_and_buildings_is_open = True
                    # Adiciona titulo na pagina ao menu_title
                    self.menu_title.append('Recursos e Edificios')
                    # Adiciona os atalhos
                    self.footer['(U)pgrade'] = 'u'
                    self.footer['(E)m Andamento'] = 'e'
                    self.footer['(T)odos os Recursos'] = 't'

                if self.menu_village_is_selected == 1:
                    self.menu_village_is_open = False
                    self.menu_update_village_is_open = True
                    self.menu_title.append('Atualizar Aldeia')
                    self.footer['(U)pdate'] = 'u'
                    
    
    def quit(self):
        sys.exit()


if __name__ =='__main__':
    curses.wrapper(lambda stdscr: App(stdscr).run())
