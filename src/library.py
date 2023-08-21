from domain.bag import Bag
from domain.library import Library
from schema.yaml_parsing import GameSet, RulesDeck


def game_to_library(game):
    library = Library(
        tokens=[],
        dice=[],
        complex_objects=[],
        decks=[],
        bags=[],
    )

    sets_bag = Bag(name="Sets", size=3, color=(1.0, 1.0, 1.0))
    for game_set in game.sets:
        game_set_bag = make_game_set_bag(game_set)
        sets_bag.contained_objects.append(game_set_bag)
    library.bags.append(sets_bag)

    add_game_rules_deck(library, game)

    return library


def make_game_set_bag(game_set: GameSet):
    set_bag = Bag(
        name=game_set.name,
        description=game_set.description,
        size=2,
        color=(0.0, 0.0, 0.0),
    )

    rules_deck = RulesDeck(cards=game_set.rules)
    domain_rules_deck = rules_deck.get_tts_obj(set_name=game_set.name)
    if domain_rules_deck:
        set_bag.contained_objects.append(domain_rules_deck)

    # heroes
    hero_bag = Bag(
        name=f"{game_set.name} heroes",
        size=2,
        color=(0.0, 0.0, 1.0),
    )
    for hero_box in game_set.heroes:
        hero_box_bag = hero_box.get_tts_obj(set_name=game_set.name)
        hero_bag.contained_objects.append(hero_box_bag)
    set_bag.contained_objects.append(hero_bag)

    # maps
    map_bag = Bag(
        name=f"{game_set.name} maps",
        size=2,
        color=(0.0, 1.0, 0.0),
    )
    for map_ in game_set.maps:
        map_bag.contained_objects.append(map_.get_tts_obj())
    set_bag.contained_objects.append(map_bag)

    return set_bag


def add_game_rules_deck(library, game):
    rules_deck = RulesDeck(cards=game.rules)
    domain_rules_deck = rules_deck.get_tts_obj(set_name="core")
    library.bags[0].contained_objects.append(domain_rules_deck)