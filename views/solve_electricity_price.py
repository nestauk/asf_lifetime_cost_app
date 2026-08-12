"""Solving electricity price for lifetime cost parity: sidebar inputs + main content results tabs."""

import os

from PIL import Image  # For loading images

# Get the current directory to load images and other resources
current_dir = os.getcwd()
nesta_asf_logo = Image.open(f"{current_dir}/images/nesta_asf_stacked_logo.png")
