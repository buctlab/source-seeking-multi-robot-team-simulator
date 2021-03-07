from PIL import Image

# color = (0, 0, 0)
color = (105, 105, 105)
image = Image.new('RGB', (4, 4), color)
image.save("discard_point_robot.png")
