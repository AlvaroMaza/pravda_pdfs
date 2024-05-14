import PyPDF2
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re


# Function to load valid Russian words from a file
def load_russian_words(file_path, encoding="utf-8"):
    try:
        with open(file_path, "r", encoding=encoding) as file:
            russian_words = set(word.strip().lower() for word in file)
    except UnicodeDecodeError:
        # If utf-8 fails, try cp1251
        with open(file_path, "r", encoding="cp1251") as file:
            russian_words = set(word.strip().lower() for word in file)
    return russian_words


# Function to extract text from PDF
def extract_text_from_pdf(pdf_path, pdf):
    text = ""
    with open(pdf_path + "/" + pdf, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()

    text = re.sub(r"-\n", "-", text)  # Remove hyphen at end of line
    text = re.sub(r"\n", " ", text)  # Replace new lines with space
    text = re.sub(",", "", text)  # Replace new lines with space
    text = re.sub(r"\.", "", text)  # Replace new lines with space
    text = re.sub(r"»", "", text) 
    text = re.sub(r"«", "", text)

    # Save extracted text to a text file
    with open(pdf_path + "/text.txt", "w", encoding="utf-8") as file:
        file.write(text)

    return text


# Function to merge hyphenated words and check if they exist in Russian
def clean_and_validate_text(text, valid_words):
    words = text.split()
    valid_russian_words = []

    for word in words:
        word = word.lower()  # Convert word to lowercase for comparison
        if "-" in word:
            word = re.sub("-", "", word)  # Replace new lines with space
            if word in valid_words:
                valid_russian_words.append(word)
                print('YES', word)
            else:
                print("NO", word)

    return " ".join(valid_russian_words)


# Function to generate word cloud
def generate_wordcloud(text, min_word_length=5):
    # Exclude short words
    words = text.split()
    words = [word for word in words if len(word) >= min_word_length]
    text = " ".join(words)

    wordcloud = WordCloud(
        width=800,
        height=800,
        background_color="white",
        stopwords=None,
        min_font_size=10,
    ).generate(text)

    # Plot word cloud
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    plt.show()


if __name__ == "__main__":
    # Path to your PDF file
    pdf_path = "C:/Users/alvar/Desktop/BDE/pravda_pdfs"
    pdf = "Правда,1927,№8.pdf"

    # Path to the file with valid Russian words
    valid_words_file = "C:/Users/alvar/Desktop/BDE/pravda_pdfs/russian.txt"

    # Load valid Russian words
    valid_russian_words = load_russian_words(valid_words_file)

    # Extract text from PDF
    text = extract_text_from_pdf(pdf_path, pdf)

    # Clean and validate text
    clean_text = clean_and_validate_text(text, valid_russian_words)

    # Generate word cloud
    generate_wordcloud(clean_text)
