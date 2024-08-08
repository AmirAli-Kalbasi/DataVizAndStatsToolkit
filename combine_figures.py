import io
from PIL import Image
import matplotlib.pyplot as plt

def combine_figures(figures, sizes, nrows, ncols, title_font='serif', title_size=16, bold=False, dpi=1):
    # Function to check if a font is available
    def is_font_available(font_name):
        from matplotlib.font_manager import findfont, FontProperties
        return findfont(FontProperties(family=[font_name])) != findfont(FontProperties())

    # Check if the specified font is available, else fall back to default
    if not is_font_available(title_font):
        print(f"WARNING: Font '{title_font}' not found. Falling back to default font.")
        title_font = 'serif'

    # Save the original figures to a buffer with bbox_inches='tight'
    buffers = []
    for fig in figures:
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        buffers.append(buf)

    # Read the buffers as images
    images = [Image.open(buf) for buf in buffers]

    # Get dimensions from input sizes
    widths, heights = zip(*sizes)

    # Calculate total width and max height in inches
    total_width_inch = sum(widths) / dpi
    max_height_inch = max(heights) / dpi

    # Create a new figure with calculated size
    fig = plt.figure(figsize=(total_width_inch, max_height_inch * nrows))

    # Plot the images in the new subplots
    for i in range(len(images)):
        left = sum(widths[:i]) / sum(widths)
        bottom = 1 - ((i // ncols + 1) * max(heights)) / (max(heights) * nrows)
        ax = fig.add_axes([left, bottom, widths[i] / sum(widths), max(heights) / (max(heights) * nrows)])
        ax.imshow(images[i])
        ax.axis('off')
        fontweight = 'bold' if bold else 'normal'
        ax.set_title(f'{chr(65 + i)})', loc='left', fontsize=title_size, fontname=title_font, fontweight=fontweight)

    plt.show()

# Example usage
# sizes = [(400, 800), (600, 800), (900, 800)]
# combine_figures([fig1, fig2, fig3], sizes, 1, 3, title_font='serif', title_size=14, bold=True, dpi=100)
