import itertools
import random

from creator.constants import (
    XMIN,
    XMAX,
    ZMIN,
    ZMAX,
    XCHUNKS,
    YCHUNKS,
)
from domain.abstract import DomainEntity
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
    random_x_offset = random.uniform(0, width)
    random_y_offset = random.uniform(0, height)

    x_coord = random_x_offset + XMIN + (chunk_x * width)
    y_coord = random_y_offset + ZMIN + (chunk_y * height)

    return x_coord, y_coord


class EntityCreator:
    def __init__(self, all_entities):
        self.all_entities = all_entities

    def get_domain_entity_by_name(self, name: str) -> DomainEntity:
        for type_ in self.all_entities:
            if type_.name == name:
                return type_
        raise ValueError("Unknown entity type: " + name)

    def create_entities(self, sheet=None) -> list[DomainEntity]:
        if sheet is None:
            return self.all_entities
        else:
            entities = []
            for col in range(0, min(14, sheet.ncols)):
                for row in range(0, min(14, sheet.nrows)):
                    content = read_content(sheet.cell(rowx=row, colx=col).value)
                    for item in content:
                        count = int(item[0])
                        object_name = item[1]
                        domain_entity = self.get_domain_entity_by_name(object_name)
                        for _ in range(count):
                            entities.append(domain_entity)
        return entities
