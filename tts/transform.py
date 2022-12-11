from creator.constants import BOARDYHEIGHT


class Transform:
    def __init__(
        self, pos_x, pos_y, pos_z, rot_x, rot_y, rot_z, scale_x, scale_y, scale_z
    ):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        self.rot_x = rot_x
        self.rot_y = rot_y
        self.rot_z = rot_z
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.scale_z = scale_z

    @classmethod
    def from_size_and_coords(cls, size: float, coords: tuple[int, int] = None):
        if not coords:
            coords = (1, 1)
        transform = cls(
            pos_x=coords[0],
            pos_y=BOARDYHEIGHT,
            pos_z=coords[1],
            rot_x=0,
            rot_y=0,
            rot_z=0,
            scale_x=size,
            scale_y=size,
            scale_z=size,
        )
        return transform

    def as_dict(self):
        return {
            "posX": self.pos_x,
            "posY": self.pos_y,
            "posZ": self.pos_z,
            "rotX": self.rot_x,
            "rotY": self.rot_y,
            "rotZ": self.rot_z,
            "scaleX": self.scale_x,
            "scaleY": self.scale_y,
            "scaleZ": self.scale_z,
        }
