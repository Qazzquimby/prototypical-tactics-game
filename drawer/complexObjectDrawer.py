import io
from pathlib import Path

import imgkit as imgkit
import jinja2
import pygame

from drawer.textrect import render_fitted_textrect
from drawer.color import convert_tts_to_pygame

EDGE_MARGIN = 25

LEFTRIGHT_MARGIN = 10
TOPBOTTOM_MARGIN = 10

TemplatesPath = Path("data/templates")


def make_empty_image(filepath):
    surf = pygame.Surface((10, 10))
    pygame.image.save(surf, filepath)


class ComplexObjectDrawer:
    def __init__(self, obj, config):
        self.object = obj
        self.config = config
        self.size = obj.type.shape.size

    def draw(self):
        w, h = self.getCardSize()
        self.surf = pygame.Surface((w, h))

        if self.object.type.name == "Ability":
            template = (TemplatesPath / "ability.html").read_text()
            html = jinja2.Template(template).render(
                width=w - 2 * EDGE_MARGIN,
                height=h - 2 * EDGE_MARGIN,
                name=self.object.content[2],
                type=self.object.content[3],
                text=self.object.content[5],
                owner=self.object.content[6],
            )
            image_bytes = imgkit.from_string(
                html, False, options={"format": "png"}, css="data/templates/ability.css"
            )
            image = pygame.image.load(io.BytesIO(image_bytes), "img.png")
            self.surf.blit(image, (0, 0))
        else:
            if isinstance(self.object.type.bgColor, str):
                self.drawImage(
                    self.surf, self.object.type.bgColor, self.surf.get_rect()
                )
            else:
                self.surf.fill(convert_tts_to_pygame(self.object.type.bgColor))
            for key, content in self.object.content.items():
                self.drawContentToArea(content, self.object.type.shape.areas[key])

        self.fullSurf = pygame.Surface((w, h))
        self.fullSurf.fill(convert_tts_to_pygame((0, 0, 0)))

        self.fullSurf.blit(self.surf, (EDGE_MARGIN, EDGE_MARGIN))
        return self.fullSurf

    def getCardSize(self):
        return self.object.type.size

    # note: areas in the shape are actually row, col and not x,y
    def drawContentToArea(self, content, area):
        w, h = self.getCardSize()
        dw = w - (2 * EDGE_MARGIN)
        dh = h - (2 * EDGE_MARGIN)
        rect = pygame.Rect(
            LEFTRIGHT_MARGIN + area[1] * dw / self.size[0],
            TOPBOTTOM_MARGIN + area[0] * dh / self.size[1],
            (area[3] + 1) * dw / self.size[0] - LEFTRIGHT_MARGIN,
            (area[2] + 1) * dh / self.size[1] - TOPBOTTOM_MARGIN,
        )
        if isinstance(content, str) and "\\icon" in content:
            self.drawIcon(self.surf, content, rect)
        elif isinstance(content, str) and "\\image" in content:
            self.drawImage(self.surf, content, rect)
        else:
            self.write(content, rect)

    def write(self, content, rect):
        if isinstance(content, float) and content.is_integer():
            content = int(content)

        # the render function expects a rect with 0,0 topleft.
        rerect = pygame.Rect((0, 0, rect[2] - rect[0], rect[3] - rect[1]))
        surf = render_fitted_textrect(str(content), rerect, (0, 0, 0), (255, 255, 255))
        if not surf:
            raise ValueError(
                "Unable to draw the card. Are you reserving enough space for all your content? Trying to write: "
                + str(content)
            )
        self.surf.blit(surf, rect)

    def baseDrawImage(self, surf, content, rect, type_):
        import pygame

        rerect = pygame.Rect((0, 0, rect[2] - rect[0], rect[3] - rect[1]))
        if type_ == "icon":
            picture = self.obtainIcon(content)
        else:
            picture = self.obtainImage(content)
        # rescale but keep proportions
        origWidth = picture.get_width()
        origHeight = picture.get_height()
        scaleFactor = min(rerect.width / origWidth, rerect.height / origHeight)

        scaledPicture = pygame.transform.scale(
            picture, (int(origWidth * scaleFactor), int(origHeight * scaleFactor))
        )

        surf.blit(scaledPicture, rect)

    def drawIcon(self, surf, content, rect):
        self.baseDrawImage(surf, content, rect, "icon")

    def drawImage(self, surf, content, rect):
        self.baseDrawImage(surf, content, rect, "image")

    def baseObtainImage(self, content, type_, replace, folder):
        name = content.replace(replace, "")
        filename = self.getPathForImage(folder, name)
        try:
            return pygame.image.load(filename)
        except FileNotFoundError:
            if type_ == "icon":
                self.makeIcon(name)
                return self.obtainIcon(content)
            else:
                self.makeImage(name)
                return self.obtainImage(content)

    def obtainIcon(self, content):
        return self.baseObtainImage(content, "icon", "\\icon ", "icons")

    def obtainImage(self, content):
        return self.baseObtainImage(content, "image", "\\image ", "images")

    def makeIcon(self, name):
        self.makeImageBase(name, name + " icon", "icons", "gray")

    def makeImage(self, name):
        self.makeImageBase(name, name, "images", "color")

    def makeImageBase(self, name, query, folder, colorType):
        import requests
        from apiclient.discovery import build

        filepath = self.getPathForImage(folder, name)

        if self.config.developerKey.get() == "":
            make_empty_image(filepath)
            return

        service = build(
            "customsearch", "v1", developerKey=self.config.developerKey.get()
        )
        try:
            res = (
                service.cse()
                .list(
                    q=name + query,
                    cx=self.config.searchId.get(),
                    searchType="image",
                    num=1,
                    fileType="jpg",
                    imgColorType=colorType,
                    safe="off",
                )
                .execute()
            )

            if not "items" in res:
                raise ValueError("Could not find an icon for: " + name)
            else:
                for item in res["items"]:
                    with open(filepath, "wb") as handler:
                        img_data = requests.get(item["link"]).content
                        handler.write(img_data)
        except ValueError:
            make_empty_image(filepath)

    def getPathForImage(self, subfolder, imagename):
        import os

        if not os.path.exists(self.config.imagesDir.get() + "/" + subfolder):
            os.mkdir(self.config.imagesDir.get() + "/" + subfolder)
        return (
            self.config.imagesDir.get()
            + "/"
            + subfolder
            + "/"
            + imagename.replace(" ", "_")
            + ".jpg"
        )
