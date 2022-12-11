import pickle

from core import game_to_library
from tests.integration_test import BASIC_GAME


LIBRARY_PICKLE = b'\x80\x04\x95\xac\x08\x00\x00\x00\x00\x00\x00\x8c\x0edomain.library\x94\x8c\x07Library\x94\x93\x94)\x81\x94}\x94(\x8c\x06tokens\x94]\x94(\x8c\x0cdomain.token\x94\x8c\x05Token\x94\x93\x94)\x81\x94}\x94(\x8c\x04name\x94\x8c\tTeam1Pawn\x94\x8c\x06entity\x94\x8c\x04Pawn\x94\x8c\x05color\x94G?\xf0\x00\x00\x00\x00\x00\x00G\x00\x00\x00\x00\x00\x00\x00\x00G\x00\x00\x00\x00\x00\x00\x00\x00\x87\x94\x8c\x04size\x94G?\xf0\x00\x00\x00\x00\x00\x00ubh\t)\x81\x94}\x94(h\x0c\x8c\tTeam2Pawn\x94h\x0eh\x0fh\x10G\x00\x00\x00\x00\x00\x00\x00\x00G\x00\x00\x00\x00\x00\x00\x00\x00G?\xf0\x00\x00\x00\x00\x00\x00\x87\x94h\x12G?\xf0\x00\x00\x00\x00\x00\x00ube\x8c\x04dice\x94]\x94\x8c\ndomain.die\x94\x8c\x03Die\x94\x93\x94)\x81\x94}\x94(h\x0c\x8c\tHealthDie\x94h\x10G?\xf0\x00\x00\x00\x00\x00\x00G?\xf0\x00\x00\x00\x00\x00\x00G?\xf0\x00\x00\x00\x00\x00\x00\x87\x94h\x12G?\xf0\x00\x00\x00\x00\x00\x00\x8c\x05sides\x94G@\x18\x00\x00\x00\x00\x00\x00\x8c\rcustomContent\x94N\x8c\timagePath\x94Nuba\x8c\x0ecomplexObjects\x94]\x94(\x8c\x14domain.complexObject\x94\x8c\rComplexObject\x94\x93\x94)\x81\x94}\x94(h\x0c\x8c\tGameBoard\x94\x8c\x04type\x94\x8c\x12domain.complexType\x94\x8c\x0bComplexType\x94\x93\x94)\x81\x94}\x94(h\x0c\x8c\x05Board\x94h\x12M\xb8\x0bM\xc4\t\x86\x94\x8c\x05shape\x94\x8c\x0cdomain.shape\x94\x8c\x05Shape\x94\x93\x94)\x81\x94}\x94(h\x12K\x07K\x05\x86\x94\x8c\x05areas\x94}\x94(K\x02(K\x00K\x00K\x00K\x00t\x94K\x03(K\x00K\x01K\x00K\x01t\x94K\x04(K\x00K\x02K\x00K\x02t\x94K\x05(K\x00K\x03K\x00K\x03t\x94K\x06(K\x00K\x04K\x00K\x04t\x94K\x07(K\x00K\x05K\x00K\x05t\x94K\x08(K\x00K\x06K\x00K\x06t\x94K\t(K\x01K\x00K\x01K\x00t\x94K\n(K\x01K\x01K\x01K\x01t\x94K\x0b(K\x01K\x02K\x01K\x02t\x94K\x0c(K\x01K\x03K\x01K\x03t\x94K\r(K\x01K\x04K\x01K\x04t\x94K\x0e(K\x01K\x05K\x01K\x05t\x94K\x0f(K\x01K\x06K\x01K\x06t\x94K\x10(K\x02K\x00K\x02K\x00t\x94K\x11(K\x02K\x01K\x02K\x01t\x94K\x12(K\x02K\x02K\x02K\x02t\x94K\x13(K\x02K\x03K\x02K\x03t\x94K\x14(K\x02K\x04K\x02K\x04t\x94K\x15(K\x02K\x05K\x02K\x05t\x94K\x16(K\x02K\x06K\x02K\x06t\x94K\x17(K\x03K\x00K\x03K\x00t\x94K\x18(K\x03K\x01K\x03K\x01t\x94K\x19(K\x03K\x02K\x03K\x02t\x94K\x1a(K\x03K\x03K\x03K\x03t\x94K\x1b(K\x03K\x04K\x03K\x04t\x94K\x1c(K\x03K\x05K\x03K\x05t\x94K\x1d(K\x03K\x06K\x03K\x06t\x94K\x1e(K\x04K\x00K\x04K\x00t\x94K\x1f(K\x04K\x01K\x04K\x01t\x94K (K\x04K\x02K\x04K\x02t\x94K!(K\x04K\x03K\x04K\x03t\x94K#(K\x04K\x04K\x04K\x04t\x94K$(K\x04K\x05K\x04K\x05t\x94K%(K\x04K\x06K\x04K\x06t\x94uub\x8c\x07bgColor\x94G?\xe4\xb4\xb4\xb4\xb4\xb4\xb5G?\xc5\x15\x15\x15\x15\x15\x15G?\xc5\x15\x15\x15\x15\x15\x15\x87\x94\x8c\x08backside\x94h\x1fh+\x8c\x05board\x94ub\x8c\x07content\x94}\x94(K\x02\x8c\x01.\x94K\x03heK\x04heK\x05heK\x06heK\x07heK\x08heK\theK\nheK\x0bheK\x0cheK\rheK\x0eheK\x0fheK\x10heK\x11heK\x12heK\x13heK\x14heK\x15heK\x16heK\x17heK\x18heK\x19heK\x1aheK\x1bheK\x1cheK\x1dheK\x1eheK\x1fheK heK!heK#heK$heK%heuh"\x8c\x00\x94ubh\')\x81\x94}\x94(h\x0c\x8c\x08TestHero\x94h+h.)\x81\x94}\x94(h\x0c\x8c\x08HeroCard\x94h\x12M\xf4\x01M\xf4\x01\x86\x94h3h6)\x81\x94}\x94(h\x12K\x04K\x06\x86\x94h:}\x94(K\x02(K\x00K\x00K\x00K\x03t\x94K\x03(K\x01K\x00K\x01K\x00t\x94K\x04(K\x01K\x01K\x01K\x01t\x94K\x05(K\x02K\x00K\x02K\x00t\x94K\x06(K\x02K\x01K\x02K\x01t\x94K\x07(K\x03K\x00K\x03K\x00t\x94K\x08(K\x03K\x01K\x03K\x01t\x94K\t(K\x05K\x01K\x05K\x02t\x94uubh_h\x1fhaG\x00\x00\x00\x00\x00\x00\x00\x00G\x00\x00\x00\x00\x00\x00\x00\x00G\x00\x00\x00\x00\x00\x00\x00\x00\x87\x94h+\x8c\x04card\x94ubhc}\x94(K\x02hiK\x03\x8c\x05Speed\x94K\x04\x8c\x013\x94K\x05\x8c\x06Health\x94K\x06\x8c\x018\x94K\x07hiK\x08hfK\thfuh"hfubh\')\x81\x94}\x94(h\x0c\x8c\x0bTestAbility\x94h+h.)\x81\x94}\x94(h\x0c\x8c\x07Ability\x94h\x12M\xf4\x01M\xf4\x01\x86\x94h3h6)\x81\x94}\x94(h\x12K\x04K\x06\x86\x94h:}\x94(K\x02(K\x00K\x00K\x00K\x02t\x94K\x03(K\x00K\x03K\x00K\x03t\x94K\x04(K\x01K\x00K\x01K\x03t\x94K\x05(K\x02K\x00K\x04K\x03t\x94K\x06(K\x05K\x01K\x05K\x02t\x94uubh_h\x1fhahzh+\x8c\x04card\x94ubhc}\x94(K\x02h\x83K\x03\x8c\x05Basic\x94K\x04hfK\x05\x8c\x08TestText\x94K\x06hiuh"hfube\x8c\x05decks\x94]\x94\x8c\x0bdomain.deck\x94\x8c\x04Deck\x94\x93\x94)\x81\x94}\x94(h\x0c\x8c\rTestHero deck\x94\x8c\x05cards\x94]\x94(\x8c\x0bdomain.card\x94\x8c\x04Card\x94\x93\x94)\x81\x94}\x94(\x8c\x02id\x94K\x01\x8c\x05count\x94K\x01\x8c\x06object\x94hgubh\xa1)\x81\x94}\x94(h\xa4K\x02h\xa5K\x01h\xa6h\x81ubeh"hf\x8c\rbackImagePath\x94hfuba\x8c\x04bags\x94]\x94(\x8c\ndomain.bag\x94\x8c\x03Bag\x94\x93\x94)\x81\x94}\x94(h\x0c\x8c\x0cTestHero box\x94h\x12G?\xf0\x00\x00\x00\x00\x00\x00h\x10h\x11hc]\x94(\x8c\x0fdomain.figurine\x94\x8c\x08Figurine\x94\x93\x94)\x81\x94}\x94(h\x0c\x8c\x11TestHero figurine\x94h\x12G?\xf0\x00\x00\x00\x00\x00\x00\x8c\nimage_path\x94\x8c\tTestImage\x94ubh\x9aeubh\xae)\x81\x94}\x94(h\x0c\x8c\x07TestSet\x94h\x12G@\x00\x00\x00\x00\x00\x00\x00h\x10hzhc]\x94h\xafaubh\xae)\x81\x94}\x94(h\x0c\x8c\x04Sets\x94h\x12G@\x08\x00\x00\x00\x00\x00\x00h\x10h\x1fhc]\x94h\xbbaubeub.'


def test_game_to_library():
    expected = pickle.loads(LIBRARY_PICKLE)

    game = BASIC_GAME
    library = game_to_library(game)

    # todo remove game board and die and pawns from expected
    expected.tokens = []
    expected.dice = []
    expected.complex_objects = expected.complexObjects
    del expected.complexObjects
    del expected.complex_objects[0]
    assert library == expected
