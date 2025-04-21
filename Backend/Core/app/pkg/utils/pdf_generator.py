import logging
from io import BytesIO
from typing import List, Optional, Tuple

from app.pkg.models import BinaryPrompt
from PIL import Image
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

logger = logging.getLogger(__name__)

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 40  # Page margin on all sides
GAP = 20  # Gap between images
HEADER_HEIGHT = 30  # Height reserved for the header text
MAX_CONTENT_HEIGHT = PAGE_HEIGHT - 2 * MARGIN - HEADER_HEIGHT
MIN_IMAGE_SIZE = 60  # Minimum dimension (width or height) after scaling


def __process_image(data: bytes) -> Optional[Tuple[ImageReader, Tuple[float, float]]]:
    """
    Processes input image bytes and returns an ImageReader along with its dimensions.

    - Converts RGBA/LA images to RGB with white background
    - Ensures the image is in RGB mode
    - Creates a thumbnail within page bounds

    Returns:
        A tuple (ImageReader, (width, height)) or None if processing fails.
    """
    try:
        with Image.open(BytesIO(data)) as img:
            # Convert transparency to white background if necessary
            if img.mode in ("RGBA", "LA"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            elif img.mode != "RGB":
                img = img.convert("RGB")

            # Resize image to fit within page dimensions
            img.thumbnail((PAGE_WIDTH, PAGE_HEIGHT), Image.LANCZOS)
            buffer = BytesIO()

            # Save processed image as JPEG into buffer
            img.save(buffer, format="JPEG", quality=85)
            buffer.seek(0)
            reader = ImageReader(buffer)
            return reader, reader.getSize()
    except Exception as e:
        logger.error(f"Image processing error: {e}")
        return None


def __calculate_layout(
    raw_size: Tuple[float, float],
    result_size: Tuple[float, float],
) -> Tuple[str, float]:
    """
    Determines the best layout (horizontal or vertical) and scale factor to place two images.

    Args:
        raw_size: (width, height) of the original image
        result_size: (width, height) of the processed image

    Returns:
        A tuple (layout, scale) where layout is 'horizontal' or 'vertical'.
    """
    raw_w, raw_h = raw_size
    result_w, result_h = result_size

    # Compute aspect ratios
    raw_ratio = raw_w / raw_h
    result_ratio = result_w / result_h

    # Prefer horizontal layout if either image is portrait
    # Vertical images (ratio < 1) -> horizontal layout (side by side)
    # Horizontal images (ratio >= 1) -> vertical layout (stacked)
    use_horizontal_layout = (raw_ratio < 1.0) or (result_ratio < 1.0)

    # Trying the horizontal layout (side by side)
    if use_horizontal_layout:
        total_width = raw_w + result_w + GAP
        max_height = max(raw_h, result_h)

        # Max possible scale for horizontal placement
        scale = min(
            (PAGE_WIDTH - 2 * MARGIN - GAP) / total_width,
            MAX_CONTENT_HEIGHT / max_height,
        )

        # Ensure scaled dimensions meet minimum size requirements
        if (
            raw_h * scale >= MIN_IMAGE_SIZE
            and result_h * scale >= MIN_IMAGE_SIZE
            and raw_w * scale >= MIN_IMAGE_SIZE
            and result_w * scale >= MIN_IMAGE_SIZE
        ):
            return "horizontal", scale

    # Fallback to vertical stacking if horizontal doesn't fit
    total_height = raw_h + result_h + GAP
    scale = min(
        (MAX_CONTENT_HEIGHT - GAP) / total_height,
        (PAGE_WIDTH - 2 * MARGIN) / max(raw_w, result_w),
    )

    return "vertical", scale


def __draw_page(
    c: canvas.Canvas,
    raw_reader: ImageReader,
    result_reader: ImageReader,
    raw_size: Tuple[float, float],
    result_size: Tuple[float, float],
    header: str,
):
    """
    Draws a single PDF page containing two images with a header.

    Args:
        c: ReportLab canvas instance
        raw_reader: ImageReader for the original image
        result_reader: ImageReader for the processed image
        raw_size: Original image size (width, height)
        result_size: Processed image size (width, height)
        header: Text to display as page header
    """

    # Draw header text at the top
    c.setFont("Helvetica-Bold", 14)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN - 20, header)

    # Determine layout and scaling factor
    layout, scale = __calculate_layout(raw_size, result_size)
    y_pos = PAGE_HEIGHT - MARGIN - HEADER_HEIGHT

    # Calculate scaled dimensions
    raw_w, raw_h = raw_size[0] * scale, raw_size[1] * scale
    result_w, result_h = result_size[0] * scale, result_size[1] * scale

    if raw_h < MIN_IMAGE_SIZE or result_h < MIN_IMAGE_SIZE:
        logger.warning("Images are too small after scaling")

    # Render images based on chosen layout
    if layout == "vertical":
        # Stack images top to bottom
        c.drawImage(
            raw_reader,
            MARGIN,
            y_pos - raw_h,
            raw_w,
            raw_h,
        )
        c.drawImage(
            result_reader,
            MARGIN,
            y_pos - raw_h - GAP - result_h,
            result_w,
            result_h,
        )
    else:
        # Place images side by side
        c.drawImage(
            raw_reader,
            MARGIN,
            y_pos - raw_h,
            raw_w,
            raw_h,
        )
        c.drawImage(
            result_reader,
            MARGIN + raw_w + GAP,
            y_pos - result_h,
            result_w,
            result_h,
        )


def generate_pdf(raw: List[BinaryPrompt], results: List[BinaryPrompt]) -> bytes:
    """
    Generates a multi-page PDF documenting each pair of original and processed images.

    Iterates through raw and result prompts, processes images, and adds pages.

    Args:
        raw: List of BinaryPrompt containing original image bytes and metadata
        results: List of BinaryPrompt containing processed image bytes and metadata

    Returns:
        PDF file as bytes. Returns empty bytes if no valid image pairs found.
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=portrait(A4))

    valid_count = 0
    for idx, (raw_prompt, result_prompt) in enumerate(zip(raw, results), 1):
        try:
            # Process both images
            raw_data = __process_image(raw_prompt.data)
            result_data = __process_image(result_prompt.data)

            if not raw_data or not result_data:
                logger.debug("Skipping invalid images in block %s", idx)
                continue

            raw_reader, raw_size = raw_data
            result_reader, result_size = result_data

            # Start a new page for subsequent items
            if valid_count > 0:
                c.showPage()

            # Format header with timestamp
            date_str = raw_prompt.created_at.strftime("%Y-%m-%d %H:%M")
            header = f"{valid_count + 1}. {date_str}"

            # Draw images and header on page
            __draw_page(c, raw_reader, result_reader, raw_size, result_size, header)
            valid_count += 1

        except Exception as e:
            logger.error("Error processing block %s: %s", idx, e)
            continue

    if valid_count == 0:
        logger.error("No valid blocks to generate PDF")
        return b""

    c.save()
    buffer.seek(0)
    return buffer.getvalue()
