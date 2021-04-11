from PIL import Image, ImageDraw


def plot_network(nodes, size=(600, 600)):
    im = Image.new('RGB', size, (255, 255, 255))
    draw = ImageDraw.Draw(im)
    for node in nodes:
        c = [[int(node.can.zone[0][i]*size[0]), int(node.can.zone[1][i]*size[1])] for i in range(2)]
        c = c[0] + c[1]
        draw.rectangle(c, outline=(0,0,0))

    return im


def dump_plot_network(nodes, size=(600, 600)):
    im = plot_network(nodes, size)
    im.save('network_plot.png')


def plot_path(nodes, path, size=(600, 600)):
    im = plot_network(nodes, size=size)
    draw = ImageDraw.Draw(im)
    for node in path:
        c = [[int(node.can.zone[0][i]*size[0]), int(node.can.zone[1][i]*size[1])] for i in range(2)]
        c = c[0] + c[1]
        draw.rectangle(c, fill=(255,0,0), outline=(0,0,0))

    return im