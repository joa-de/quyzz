import os
from pathlib import Path
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def create_square_pdf(vocab_list, fr_translations, filename, is_front=True):
    # Create PDF with square cards
    c = canvas.Canvas(filename, pagesize=(9 * cm, 9 * cm))

    # Register the found font with bold and italic variants
    font_name = "DejaVuSans"

    direc = Path(os.path.dirname(__file__)) / "fonts"
    print(direc)

    deja_vu_path = direc / "DejaVuSans.ttf"
    pdfmetrics.registerFont(TTFont(f"{font_name}", deja_vu_path))

    deja_vu_bold_path = direc / "DejaVuSans-Bold.ttf"
    pdfmetrics.registerFont(TTFont(f"{font_name}Bold", deja_vu_bold_path))

    deja_vu_oblique_path = direc / "DejaVuSans-Oblique.ttf"
    pdfmetrics.registerFont(TTFont(f"{font_name}Italic", deja_vu_oblique_path))

    for line in vocab_list:
        # Split the line into parts
        parts = line.split("|")

        # Ensure we have enough parts
        if len(parts) >= 5:
            number = parts[0]
            latin_word = parts[1]
            latin_word_2 = parts[2]
            translation_dutch = parts[3]
            if len(parts[4]) > 0:
                hint = parts[4]
            else:
                hint = " -- "
            word_type = parts[5].strip() if len(parts) > 5 else ""

            # Set font and clear the page
            c.setFont(font_name, 36)

            # Decide what to print based on front or back
            if is_front:
                # Center the number on the front
                c.drawCentredString(4.5 * cm, (4.5 + 1.0) * cm, number)
                c.drawCentredString(4.5 * cm, (4.5 - 1.0) * cm, latin_word)
            else:
                # Prepare lines for the back
                lines = [
                    number,
                    latin_word_2,
                    translation_dutch,
                    f"indice: {hint}",
                    word_type,
                    f"traduction: {fr_translations[int(number)]}",
                ]

                # Calculate vertical position to center text
                total_text_height = len(lines) * 24  # Estimated line height
                start_y = 4.5 * cm + total_text_height / 2

                # Draw each line centered
                for j, text_line in enumerate(lines):
                    c.setFont(font_name, 16)

                    if j == 2:
                        c.setFont(f"{font_name}Bold", 16)
                        if len(text_line) > 25:
                            c.setFont(f"{font_name}Bold", 12)

                    elif len(text_line) > 25:
                        c.setFont(font_name, 12)

                    if j == 5:
                        c.setFont(f"{font_name}Italic", 10)

                    c.drawCentredString(4.5 * cm, start_y - j * 24, text_line)

        # Move to next page
        c.showPage()

    c.save()


# Get the current working directory
current_dir = Path.cwd()
print("Current Directory:", current_dir)


with open(
    current_dir / "vocabularies" / "hoofdstuck4.txt", "r", encoding="utf-8"
) as file:
    vocab_list = file.readlines()

french_translation_filename = "french-translations.txt"
df = pd.read_csv(
    current_dir / "languages" / french_translation_filename, sep="|", header=None
)
translation_dict = df.set_index(0).to_dict()[1]


# Remove any lines that are empty or don't contain the expected number of parts
vocab_list = [line.strip() for line in vocab_list if "|" in line]

# Generate PDFs
create_square_pdf(
    vocab_list, translation_dict, "H4_vocabulary_front_9cm.pdf", is_front=True
)
create_square_pdf(
    vocab_list, translation_dict, "H4_vocabulary_back_9cm.pdf", is_front=False
)

print("PDFs generated: vocabulary_front_9cm.pdf and vocabulary_back_9cm.pdf")
