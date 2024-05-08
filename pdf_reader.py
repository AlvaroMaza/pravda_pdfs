import PyPDF2
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path, pdf):
    text = ""
    with open(pdf_path + '/' + pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()

    # Save extracted text to a text file
    with open(pdf_path + '/text.txt','w', encoding='utf-8') as file:
        file.write(text)

    return text

# Function to generate word cloud
def generate_wordcloud(text, min_word_length=3):

    # Exclude short words
    words = text.split()
    words = [word for word in words if len(word) >= min_word_length]
    text = ' '.join(words)

    wordcloud = WordCloud(width=800, height=800, 
                          background_color='white', 
                          stopwords=None, 
                          min_font_size=10).generate(text)
    
    # Plot word cloud
    plt.figure(figsize=(8, 8), facecolor=None) 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad=0) 
  
    plt.show()



if __name__ == "__main__":
    # Path to your PDF file
    pdf_path = 'C:/Users/alvar/Desktop/BDE/pravda_pdfs'
    pdf = 'Правда,1927,№8.pdf'

    # Extract text from PDF
    text = extract_text_from_pdf(pdf_path, pdf)

    # Generate word cloud
    generate_wordcloud(text)