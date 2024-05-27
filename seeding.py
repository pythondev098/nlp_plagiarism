import os
import re
import pandas as pd
from tqdm import tqdm


class Seeding:
    def __init__(self, training_source_path, test_source_path, training_source_dir_name, test_source_dir_name):

        self.suspicious_paragraph_number = 0
        self.suspicious_sentence_number = 0
        self.source_paragraph_number = 0
        self.source_sentence_number = 0
        self.training_source_path = training_source_path
        self.test_source_path = test_source_path

        self.training_source_dir_name = training_source_dir_name
        self.test_source_dir_name = test_source_dir_name
        print(training_source_dir_name)
        self.seeding_paragraph(self.training_source_path, 'unigram')
        self.seeding_paragraph(self.training_source_path, 'bigram')
        self.seeding_paragraph(self.test_source_path, 'unigram')
        self.seeding_paragraph(self.test_source_path, 'bigram')

        self.seeding_sentence(self.training_source_path, 'unigram')
        self.seeding_sentence(self.training_source_path, 'bigram')
        self.seeding_sentence(self.test_source_path, 'unigram')
        self.seeding_sentence(self.test_source_path, 'bigram')

    def seeding_paragraph(self, path, n_gram):

        path = path
        list_dir = os.listdir(path)

        for dir_name in list_dir:

            unknown_file = [f for f in os.listdir(f'{path}\\{dir_name}\\paragraph\\{n_gram}\\unknown')
                            if f.endswith('.txt')]
            known_files = [f for f in os.listdir(f'{path}\\{dir_name}\\paragraph\\{n_gram}\\known')
                           if f.endswith('.txt')]
            print("unknown_file", unknown_file)

            for suspicious_file_name in tqdm(unknown_file):
                df_seeding_phase = pd.DataFrame(
                    columns=['suspicious_file_name', 'suspicious_paragraph_number', 'source_file_name',
                             'source_paragraph_number', 'common_words_number'])

                # file_name = f'{path}\\{part}\\{file}'

                with open(f'{path}\\{dir_name}\\paragraph\\{n_gram}\\unknown\\{suspicious_file_name}', 'r',
                          encoding='utf-8-sig') as \
                        suspicious_txt_file:

                    self.suspicious_paragraph_number = 0
                    for suspicious_paragraph in suspicious_txt_file:

                        for source_file_name in tqdm(known_files):
                            with open(f'{path}\\{dir_name}\\paragraph\\{n_gram}\\known\\{source_file_name}', 'r',
                                      encoding='utf-8-sig') as \
                                    source_txt_file:
                                for source_paragraph in source_txt_file:
                                    # print(source_paragraph)
                                    # Find common words between suspicious paragraphs and source paragraphs
                                    common_words = set(suspicious_paragraph.split()) & set(source_paragraph.split())
                                    common_words_number = len(common_words)
                                    # create dataframe for paragraph comparison
                                    new_row = {'suspicious_file_name': suspicious_file_name,
                                               'suspicious_paragraph_number': self.suspicious_paragraph_number,
                                               'source_file_name': source_file_name,
                                               'source_paragraph_number': self.source_paragraph_number,
                                               'common_words_number': common_words_number}
                                    df_seeding_phase = pd.concat([df_seeding_phase, pd.DataFrame([new_row])], axis=0,
                                                                 ignore_index=True)

                                    self.source_paragraph_number = self.source_paragraph_number + 1

                            self.source_paragraph_number = 0

                        self.suspicious_paragraph_number = self.suspicious_paragraph_number + 1

                    name, ext = os.path.splitext(suspicious_file_name)
                    # save the dataframe in csv file
                    # df_seeding_phase.to_csv(f'{suspicious_file_name}.csv', index=False)
                    df_seeding_phase.to_csv(f'{path}\\{dir_name}\\paragraph\\{n_gram}\\paragraph_{name}.csv', index=False)

    def seeding_sentence(self, path, n_gram):

        path = path
        list_dir = os.listdir(path)

        for dir_name in list_dir:

            unknown_file = [f for f in os.listdir(f'{path}\\{dir_name}\\sentence\\{n_gram}\\unknown')
                            if f.endswith('.txt')]
            known_files = [f for f in os.listdir(f'{path}\\{dir_name}\\sentence\\{n_gram}\\known')
                           if f.endswith('.txt')]
            print("unknown_file", unknown_file)

            for suspicious_file_name in tqdm(unknown_file):
                df_seeding_phase = pd.DataFrame(
                    columns=['suspicious_file_name', 'suspicious_paragraph_number', 'source_file_name',
                             'source_paragraph_number', 'common_words_number'])

                # file_name = f'{path}\\{part}\\{file}'

                with open(f'{path}\\{dir_name}\\sentence\\{n_gram}\\unknown\\{suspicious_file_name}', 'r',
                          encoding='utf-8-sig') as \
                        suspicious_txt_file:

                    # with open(filename) as f:
                    # text = suspicious_txt_file.read()
                    #
                    # suspicious_sentences = re.split(r' *[\.\?!][\'"\)\]]* *', text)
                    # print("sentence:\n", sentences)

                    self.suspicious_sentence_number = 0
                    for suspicious_sentence in suspicious_txt_file:

                        for source_file_name in tqdm(known_files):
                            with open(f'{path}\\{dir_name}\\sentence\\{n_gram}\\known\\{source_file_name}', 'r',
                                      encoding='utf-8-sig') as \
                                    source_txt_file:

                                source_text = source_txt_file.read()

                                source_sentences = re.split(r' *[\.\?!][\'"\)\]]* *', source_text)
                                for source_sentence in source_sentences:
                                    # print(source_paragraph)
                                    # Find common words between suspicious paragraphs and source paragraphs
                                    common_words = set(suspicious_sentence.split()) & set(source_sentence.split())
                                    common_words_number = len(common_words)
                                    # create dataframe for paragraph comparison
                                    new_row = {'suspicious_file_name': suspicious_file_name,
                                               'suspicious_paragraph_number': self.suspicious_sentence_number,
                                               'source_file_name': source_file_name,
                                               'source_paragraph_number': self.source_sentence_number,
                                               'common_words_number': common_words_number}
                                    df_seeding_phase = pd.concat([df_seeding_phase, pd.DataFrame([new_row])], axis=0,
                                                                 ignore_index=True)

                                    self.source_sentence_number = self.source_sentence_number + 1

                            self.source_sentence_number = 0

                        self.suspicious_sentence_number = self.suspicious_sentence_number + 1

                    name, ext = os.path.splitext(suspicious_file_name)
                    # save the dataframe in csv file
                    # df_seeding_phase.to_csv(f'{suspicious_file_name}.csv', index=False)
                    df_seeding_phase.to_csv(f'{path}\\{dir_name}\\sentence\\{n_gram}\\sentence_{name}.csv', index=False)
