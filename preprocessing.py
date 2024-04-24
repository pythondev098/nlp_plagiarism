import os
from tqdm import tqdm
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

import nltk
import string
import re

nltk.download("stopwords")
stop = set(stopwords.words("english"))
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('corpus')
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')
wordnet_lemmatizer = WordNetLemmatizer()


class Preprocessing:

    def __init__(self):
        self.i = 0
        self.tags = ['JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'NN', 'NNS',
                     'NNP', 'NNPS']
        source_dir_name_path = 'F:\\workspace\\nlp_plagiarism\\dataset\\pan-plagiarism-corpus-2011\\' \
                               'external-detection-corpus\\source-document'
        suspicious_dir_name_path = 'F:\\workspace\\nlp_plagiarism\\dataset\\pan-plagiarism-corpus-2011\\' \
                                   'external-detection-corpus\\suspicious-document'
        self.source_parts_dir_name = os.listdir(source_dir_name_path)
        # suspicious_parts_dir_name = os.listdir(suspicious_dir_name_path)
        self.preprocessing1(source_dir_name_path)
        # self.preprocessing(source_dir_name_path)
        # self.preprocessing(suspicious_dir_name_path)

    def preprocessing(self, path):
        for part in tqdm(self.source_parts_dir_name):
            print("part : ", part)
            dir_part_path = f'{path}\\{part}'
            os.chdir(dir_part_path)
            source_files = [f for f in os.listdir(dir_part_path) if f.endswith('.txt')]
            for file in tqdm(source_files):
                file_name = f'{path}\\{part}\\{file}'
                # print(sss)
                with open(f'{file_name}', 'r', encoding="utf8") as txt_file:
                    # print(txt_file.read())
                    """
                    s = " ".join(line.rstrip().lower() for line in tqdm(txt_file))
                    # s = s.lower()  # downcase
                    tokens = nltk.tokenize.word_tokenize(s)  # split string into words (tokens)
                    tokens = [t for t in tokens if len(t) > 2]  # remove short words, they're probably not useful
                    tokens = [wordnet_lemmatizer.lemmatize(t) for t in tokens]  # put words into base form
                    tokens = [t for t in tokens if t not in stopwords]  # remove stopwords
                    print("tokens: ", tokens)
                    """
                    text = " ".join(line.rstrip().lower() for line in tqdm(txt_file))
                    # print(text)
                    # Remove numbers
                    text = ''.join([i for i in text if not i.isdigit()])
                    # Remove punctuation
                    text = text.translate(str.maketrans('', '', string.punctuation or string.digits))
                    # print(text)
                    # Tokenizing to unigrams
                    token_text = word_tokenize(text)
                    # print(new_text)
                    # Remove stopwords using NLTK
                    new_text_words = [
                        word for word in token_text if word.lower() not in stopwords.words('english')]

                    # Tokenize to bigrams
                    bigrm_tokens = nltk.bigrams(token_text)
                    # print(*map(' '.join, bigrm_tokens), sep=', ')

    def preprocessing1(self, path):
        significant_token = []
        for part in tqdm(self.source_parts_dir_name):
            print("part : ", part)
            dir_part_path = f'{path}\\{part}'
            os.chdir(dir_part_path)
            source_files = [f for f in os.listdir(dir_part_path) if f.endswith('.txt')]
            for file in tqdm(source_files):
                file_name = f'{path}\\{part}\\{file}'
                # print(sss)
                with open(f'{file_name}', 'r', encoding='utf8') as txt_file:
                    text = " ".join(line.rstrip().lower() for line in tqdm(txt_file))
                    # print(text)
                paragraph = ''
                name, ext = os.path.splitext(file)
                new_text_file = open(f'{name}1.{ext}', "w", encoding='utf8')

                word_counter = 0
                for word in text.split():
                    # print(word)
                    if word not in stop:
                        paragraph = paragraph + ' ' + word.lower()
                        word_counter = word_counter + 1

                    if word_counter > 500 and word[-1] == '.':

                        # remove words which contain number
                        paragraph = re.sub(r'\d*\w*\d\w*' or r'\d\w*\d*\w*', '', paragraph).strip()

                        # remove punctuations
                        paragraph = paragraph.translate(str.maketrans('', '', string.punctuation))

                        # Tokenizing to unigrams
                        token_paragraph = word_tokenize(paragraph)

                        # remove short words
                        long_token_paragraph = [item for item in token_paragraph if len(item) > 2]
                        # print(long_token_paragraph)

                        # converting words into a dictionary base form
                        tagged_token = nltk.pos_tag(long_token_paragraph)
                        # print(tagged_token)

                        # Select verb, adverb, adjective and noun
                        for item in tagged_token:
                            if item[1] in self.tags:
                                significant_token.append(item[0])

                        # Convert words into a dictionary base form
                        lemmatize_token_paragraph = [wordnet_lemmatizer.lemmatize(item) for item in significant_token]

                        # Empty significant_token array
                        significant_token = []

                        # Tokenizing to bigram
                        bigrm_tokens = nltk.bigrams(token_paragraph)
                        # print(*map(' '.join, bigrm_tokens), sep=', ')

                        # convert token list to string to save in a file
                        token_list_to_string = ' '.join([str(item) for item in lemmatize_token_paragraph])

                        # Write tokens to a file
                        new_text_file.write(token_list_to_string)

                        # Add two lines to the file after each paragraph
                        new_text_file.write('\n\n')
                        paragraph = ''
                        word_counter = 0

                new_text_file.close()




# Preprocessing()
