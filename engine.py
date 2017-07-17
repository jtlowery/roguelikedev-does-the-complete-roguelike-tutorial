import tdl

import input_handlers
from entity import Entity, get_blocking_entities_at_location
from game_states import GameStates
import render_functions
import map_utils


def main():
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    fov_algorithm = 'BASIC'
    fov_light_walls = True
    fov_radius = 10

    max_monsters_per_room = 3

    colors = {
        'dark_wall': (0, 0, 100),
        'dark_ground': (50, 50, 150),
        'light_wall': (130, 110, 50),
        'light_ground': (200, 180, 50),
        'desaturated_green': (63, 127, 63),
        'darker_green': (0, 127, 0)
    }

    player = Entity(0, 0, '@', (255, 255, 255), 'Player', blocks=True)
    entities = [player]

    tdl.set_font('consolas12x12_gs_tc.png', greyscale=True, altLayout=True)

    root_console = tdl.init(width=screen_width,
                            height=screen_height,
                            title='Roguelike Tutorial Revised')
    con = tdl.Console(width=screen_width, height=screen_height)

    game_map = map_utils.GameMap(width=map_width, height=map_height)
    map_utils.make_map(game_map=game_map,
                       max_rooms=max_rooms,
                       room_min_size=room_min_size,
                       room_max_size=room_max_size,
                       map_width=map_width,
                       map_height=map_height,
                       player=player,
                       entities=entities,
                       max_monsters_per_room=max_monsters_per_room,
                       colors=colors)

    fov_recompute = True

    game_state = GameStates.PLAYERS_TURN

    while not tdl.event.is_window_closed():
        if fov_recompute:
            game_map.compute_fov(x=player.x,
                                 y=player.y,
                                 fov=fov_algorithm,
                                 radius=fov_radius,
                                 light_walls=fov_light_walls)

        render_functions.render_all(con,
                                    entities,
                                    game_map,
                                    fov_recompute,
                                    root_console,
                                    screen_width,
                                    screen_height,
                                    colors)

        tdl.flush()

        render_functions.clear_all(con, entities)

        fov_recompute = False

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

        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if game_map.walkable[destination_x, destination_y]:
                target = get_blocking_entities_at_location(entities,
                                                           destination_x,
                                                           destination_y)
                if target:
                    print('You kick the {} in the shins, '
                          'much to its annoyance!'.format(target.name))
                else:
                    player.move(dx, dy)
                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN

        if exit:
            return True

        if fullscreen:
            tdl.set_fullscreen(not tdl.get_fullscreen())

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity != player:
                    print('The {} ponders the meaning of '
                          'its existence.'.format(entity.name))

            game_state = GameStates.PLAYERS_TURN


if __name__ == '__main__':
    main()

