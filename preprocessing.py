import os
from itertools import chain
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
        unigram_path = 'F:\\workspace\\nlp_plagiarism\\dataset\\pan-plagiarism-corpus-2011\\' \
                       'external-detection-corpus\\unigram'
        bigram_path = 'F:\\workspace\\nlp_plagiarism\\dataset\\pan-plagiarism-corpus-2011\\' \
                      'external-detection-corpus\\bigram'
        unigram_source_output_path = f'{unigram_path}\\source_output'
        unigram_suspicious_output_path = f'{unigram_path}\\suspicious_output'
        bigram_source_output_path = f'{bigram_path}\\source_output'
        bigram_suspicious_output_path = f'{bigram_path}\\suspicious_output'

        self.source_parts_dir_name = os.listdir(source_dir_name_path)
        self.suspicious_parts_dir_name = os.listdir(suspicious_dir_name_path)

        self.preprocessing(self.source_parts_dir_name, source_dir_name_path, unigram_source_output_path, 'unigram')
        self.preprocessing(self.suspicious_parts_dir_name, suspicious_dir_name_path, unigram_suspicious_output_path,
                           'unigram')

        self.preprocessing(self.source_parts_dir_name, source_dir_name_path, bigram_source_output_path, 'bigram')
        self.preprocessing(self.suspicious_parts_dir_name, suspicious_dir_name_path, bigram_suspicious_output_path,
                           'biggram')

    def preprocessing(self, dir_name, path, output_folder_path, n_gram):
        significant_token = []
        for part in tqdm(dir_name):
            print("part : ", part)
            dir_part_path = f'{path}\\{part}'
            os.chdir(dir_part_path)
            source_files = [f for f in os.listdir(dir_part_path) if f.endswith('.txt')]
            for file in tqdm(source_files):
                file_name = f'{path}\\{part}\\{file}'
                with open(f'{file_name}', 'r', encoding='utf-8-sig') as txt_file:
                    text = " ".join(line.rstrip().lower() for line in tqdm(txt_file))
                    # print(text)
                paragraph = ''
                name, ext = os.path.splitext(file)
                new_text_file = open(f'{output_folder_path}\\{name}{ext}', "w", encoding='utf-8-sig')

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

                        if n_gram == 'unigram':
                            # Tokenizing to unigrams
                            token_paragraph = word_tokenize(paragraph)
                        else:
                            # Tokenizing to bigram
                            tokens = nltk.word_tokenize(paragraph)
                            token_paragraph = list(nltk.bigrams(tokens))
                            token_paragraph = list(chain.from_iterable(token_paragraph))
                            res = []
                            [res.append(x) for x in token_paragraph if x not in res]
                            # print(res)
                            token_paragraph = res

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

                        # convert token list to string to save in a file
                        token_list_to_string = ' '.join([str(item) for item in lemmatize_token_paragraph])

                        # Write tokens to a file
                        new_text_file.write(token_list_to_string)

                        # Add two lines to the file after each paragraph
                        new_text_file.write('\n\n')
                        paragraph = ''
                        word_counter = 0

                new_text_file.close()
