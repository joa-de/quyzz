import os
from pathlib import Path
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def split_long_text(text, c, font_name, font_size, max_width=8.5*cm):
    """
    Split text at punctuation marks if it's too wide for the page.
    Returns a list of lines.
    """
    # Set the font to measure text width
    c.setFont(font_name, font_size)
    
    # If text fits, return as single line
    if c.stringWidth(text) <= max_width:
        return [text]
    
    # Look for splitting points
    split_chars = [';', ',']
    
    for split_char in split_chars:
        if split_char in text:
            parts = text.split(split_char)
            # Recombine parts with the split character to maintain punctuation
            lines = []
            current_line = parts[0] + split_char
            
            for part in parts[1:]:
                part = part.strip()
                test_line = current_line + " " + part
                
                if c.stringWidth(test_line) <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = part
            
            if current_line:
                lines.append(current_line)
                
            return lines
    
    # If no punctuation found, return as single line
    return [text]


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
                # Calculate initial vertical position
                start_y = 7 * cm  # Start higher to accommodate multiple lines
                line_spacing = 24  # Space between lines

                # Draw number
                c.setFont(font_name, 16)
                c.drawCentredString(4.5 * cm, start_y, number)
                start_y -= line_spacing

                # Draw latin_word_2
                c.setFont(font_name, 16)
                for line_text in split_long_text(latin_word_2, c, font_name, 16):
                    c.drawCentredString(4.5 * cm, start_y, line_text)
                    start_y -= line_spacing

                # Draw translation_dutch
                c.setFont(f"{font_name}Bold", 16)
                if len(translation_dutch) > 25:
                    c.setFont(f"{font_name}Bold", 12)
                for line_text in split_long_text(translation_dutch, c, f"{font_name}Bold", 
                    12 if len(translation_dutch) > 25 else 16):
                    c.drawCentredString(4.5 * cm, start_y, line_text)
                    start_y -= line_spacing

                # Draw hint
                c.setFont(font_name, 16)
                hint_text = f"indice: {hint}"
                if len(hint_text) > 25:
                    c.setFont(font_name, 12)
                for line_text in split_long_text(hint_text, c, font_name, 
                    12 if len(hint_text) > 25 else 16):
                    c.drawCentredString(4.5 * cm, start_y, line_text)
                    start_y -= line_spacing

                # Draw word type
                c.setFont(font_name, 16)
                c.drawCentredString(4.5 * cm, start_y, word_type)
                start_y -= line_spacing

                # Draw French translation
                c.setFont(f"{font_name}Italic", 10)
                fr_text = f"traduction: {fr_translations[int(number)]}"
                for line_text in split_long_text(fr_text, c, f"{font_name}Italic", 10):
                    c.drawCentredString(4.5 * cm, start_y, line_text)
                    start_y -= line_spacing

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
