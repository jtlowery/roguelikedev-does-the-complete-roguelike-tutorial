import tdl

import input_handlers
import entity
import render_functions
import map_utils


def main():
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45

    colors = {
        'dark_wall': (0, 0, 100),
        'dark_ground': (50, 50, 150)
    }

    player = entity.Entity(x=int(screen_width / 2),
                           y=int(screen_height / 2),
                           char='@',
                           color=(255, 255, 255))
    npc = entity.Entity(x=int(screen_width / 2),
                        y=int(screen_height / 2 - 5),
                        char='@',
                        color=(255, 255, 0))
    entities = [npc, player]

    tdl.set_font('consolas12x12_gs_tc.png', greyscale=True, altLayout=True)

    root_console = tdl.init(width=screen_width,
                            height=screen_height,
                            title='Roguelike Tutorial Revised')
    con = tdl.Console(width=screen_width, height=screen_height)

    game_map = tdl.map.Map(width=map_width, height=map_height)
    map_utils.make_map(game_map=game_map)

    while not tdl.event.is_window_closed():
        render_functions.render_all(con, entities,
                                    game_map, root_console,
                                    screen_width, screen_height,
                                    colors)

        tdl.flush()

        render_functions.clear_all(con, entities)

        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
                break
        else:
            user_input = None

        if not user_input:
            continue

        action = input_handlers.handle_keys(user_input)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            if game_map.walkable[player.x + dx, player.y + dy]:
                player.move(dx, dy)

        if exit:
            return True

        if fullscreen:
            tdl.set_fullscreen(not tdl.get_fullscreen())


if __name__ == '__main__':
    main()

