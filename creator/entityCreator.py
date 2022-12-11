import itertools
import random

from creator.constants import (
    XMIN,
    XMAX,
    ZMIN,
    ZMAX,
    YHEIGHT,
    BOARDYHEIGHT,
    XCHUNKS,
    YCHUNKS,
)
from domain.figurine import Figurine
from domain.token import Token
from domain.token import ContentToken
from domain.die import Die
from domain.deck import Deck
from domain.complexObject import ComplexObject
from domain.bag import Bag, InfiniteBag
from tts.simpletoken import SimpleToken
from tts.transform import Transform
from tts.die import Die as TTSDie
from tts.deck import Deck as TTSDeck
from tts.board import Board as TTSBoard
from tts.token import Token as TTSToken
from tts.figurine import Figurine as TTSFigurine
from tts.bag import Bag as TTSBag
from reader.content import read_content


def get_random_coord_in_chunk(
    chunk_x: int, chunk_y: int, num_x_chunks: int = XCHUNKS, num_y_chunks: int = YCHUNKS
) -> (int, int):
    if not 0 <= chunk_x < num_x_chunks:
        raise ValueError(
            "Trying to place an object outside the playing field; x-coordinates should be between 0 and "
            + str(int(num_x_chunks - 1))
        )
    if not 0 <= chunk_y < num_y_chunks:
        raise ValueError(
            "Trying to place an object outside the playing field; y-coordinates should be between 0 and "
            + str(int(num_y_chunks - 1))
        )

    width = (XMAX - XMIN) / num_x_chunks
    height = (ZMAX - ZMIN) / num_y_chunks
    random_x_offset = random.uniform(0, width)  # todo, why are these random?
    random_y_offset = random.uniform(0, height)

    x_coord = random_x_offset + XMIN + (chunk_x * width)
    y_coord = random_y_offset + ZMIN + (chunk_y * height)

    return x_coord, y_coord


def place_token(coords, entity):
    if isinstance(entity, ContentToken):
        transform = Transform(
            posX=coords[0],
            posY=YHEIGHT,
            posZ=coords[1],
            rotX=0,
            rotY=180,
            rotZ=0,
            scaleX=entity.size,
            scaleY=entity.size,
            scaleZ=entity.size,
        )
        bs = TTSToken(transform, entity.imagePath)
        return bs
    else:
        transform = Transform(
            coords[0],
            YHEIGHT,
            coords[1],
            0,
            0,
            0,
            entity.size,
            entity.size,
            entity.size,
        )
        bs = SimpleToken(entity.entity, transform, entity.color)
        return bs


def place_figurine(coords, entity):
    transform = Transform(
        coords[0],
        YHEIGHT,
        coords[1],
        0,
        180,
        0,
        entity.size,
        entity.size,
        entity.size,
    )
    bs = TTSFigurine(transform=transform, entity=entity)
    return bs


def place_die(coords, entity):
    transform = Transform(
        coords[0],
        YHEIGHT,
        coords[1],
        0,
        0,
        0,
        entity.size,
        entity.size,
        entity.size,
    )
    die = TTSDie(
        entity.sides,
        entity.color,
        transform,
        entity.customContent,
        entity.imagePath,
    )
    return die


def place_deck(coords, entity):
    transform = Transform(coords[0], YHEIGHT, coords[1], 0, 180, 180, 1, 1, 1)
    deck = TTSDeck(
        transform, entity.name, entity.cards, entity.imagePath, entity.backImagePath
    )
    return deck


def place_board(coords, entity):
    transform = Transform(coords[0], BOARDYHEIGHT, coords[1], 0, 0, 0, 1, 1, 1)
    board = TTSBoard(transform, entity)
    return board


class EntityCreator:
    def __init__(self, all_entities):
        self.all_entities = all_entities

    def findObjectByName(self, name):
        for type_ in self.all_entities:
            if type_.name == name:
                return type_
        raise ValueError("Unknown entity type: " + name)

    def createEntity(self, coords, entity):
        if isinstance(entity, Token):
            return place_token(coords, entity)
        if isinstance(entity, Figurine):
            return place_figurine(coords, entity)
        if isinstance(entity, Die):
            return place_die(coords, entity)
        if isinstance(entity, Deck):
            return place_deck(coords, entity)
        if isinstance(entity, ComplexObject):
            if entity.type.type == "board":
                return place_board(coords, entity)
            else:
                raise ValueError(
                    "Only ComplexTypes of the 'board' type can be placed directly. The others go into a deck! (Tried placing a "
                    + entity.name
                    + ")"
                )
        if isinstance(entity, Bag):
            return self.placeBag(coords, entity)
        raise NotImplementedError(
            "Not sure what to do with this: " + entity.__class__.__name__
        )

    def placeBag(self, coords, entity):
        transform = Transform(
            coords[0],
            BOARDYHEIGHT,
            coords[1],
            0,
            0,
            0,
            entity.size,
            entity.size,
            entity.size,
        )
        bag = TTSBag(
            transform=transform,
            color=entity.color,
            name=entity.name,
            content=self.convertToTTS(coords, entity.content),
            is_infinite=isinstance(entity, InfiniteBag),
        )
        return bag

    def convertToTTS(self, coords, items):
        converted = []
        for item in items:
            converted.append(self.createEntity(coords, item))
        return converted

    def createEntities(self, sheet=None):
        entities = []
        if sheet is None:
            for coord, entity in zip(
                itertools.product(range(14), range(14)), self.all_entities
            ):
                self.createEntity(
                    get_random_coord_in_chunk(coord[0], coord[1]),
                    entity,
                )
                entities.append(entity)
        else:
            for col in range(0, min(14, sheet.ncols)):
                for row in range(0, min(14, sheet.nrows)):
                    content = read_content(sheet.cell(rowx=row, colx=col).value)
                    for item in content:
                        count = int(item[0])
                        object_name = item[1]
                        object_ = self.findObjectByName(object_name)
                        for i in range(count):
                            entities.append(
                                self.createEntity(
                                    get_random_coord_in_chunk(row, col),
                                    object_,
                                )
                            )
        return entities
