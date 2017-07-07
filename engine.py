import tdl


def main():
    screen_width = 80
    screen_height = 50

    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    tdl.set_font('consolas12x12_gs_tc.png', greyscale=True, altLayout=True)

    root_console = tdl.init(width=screen_width,
                            height=screen_height,
                            title='Roguelike Tutorial Revised')

    while not tdl.event.is_window_closed():
        root_console.draw_char(player_x, player_y, '@', bg=None, fg=(255, 255, 255))

        tdl.flush()

        root_console.draw_char(player_x, player_y, ' ', bg=None)

        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
                break
        else:
            user_input = None

        if not user_input:
            continue

        if user_input.key == 'ESCAPE':
            return True


if __name__ == '__main__':
    main()

