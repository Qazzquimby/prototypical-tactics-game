import asyncio
from pathlib import Path

import pyimgbox as pyimgbox

if __name__ == "__main__":
    gallery = pyimgbox.Gallery(title="prototypical_project")
    result = asyncio.run(gallery.upload(Path("data/images/Ana deck.jpg")))
    print(result)
    print("done")
