from pathlib import Path

data_dir = Path("data").absolute()

site_public_dir = Path("tactics-site").absolute() / "public"
site_images_dir = site_public_dir / "images"
site_tokens_dir = site_images_dir / "tokens"

site_url = "https://tactics.toren.dev"
site_images_url = site_url + "/images"
site_tokens_url = site_images_url + "/tokens"
