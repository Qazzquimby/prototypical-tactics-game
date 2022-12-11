from creator.constants import BOARDYHEIGHT


class Transform:
    def __init__(self, posX, posY, posZ, rotX, rotY, rotZ, scaleX, scaleY, scaleZ):
        self.posX = posX
        self.posY = posY
        self.posZ = posZ
        self.rotX = rotX
        self.rotY = rotY
        self.rotZ = rotZ
        self.scaleX = scaleX
        self.scaleY = scaleY
        self.scaleZ = scaleZ

    @classmethod
    def from_size_and_coords(cls, size: float, coords: tuple[int, int] = None):
        if not coords:
            coords = (1, 1)
        transform = cls(
            posX=coords[0],
            posY=BOARDYHEIGHT,
            posZ=coords[1],
            rotX=0,
            rotY=0,
            rotZ=0,
            scaleX=size,
            scaleY=size,
            scaleZ=size,
        )
        return transform

    def as_dict(self):
        return {
            "posX": self.posX,
            "posY": self.posY,
            "posZ": self.posZ,
            "rotX": self.rotX,
            "rotY": self.rotY,
            "rotZ": self.rotZ,
            "scaleX": self.scaleX,
            "scaleY": self.scaleY,
            "scaleZ": self.scaleZ,
        }
