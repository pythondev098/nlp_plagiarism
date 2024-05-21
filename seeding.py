import os
# import pandas as pd
import pandas as pd
from tqdm import tqdm


class Seeding:
    def __init__(self):

        # self.path = 'F:\\workspace\\nlp_plagiarism\\dataset\\pan-plagiarism-corpus-2011\\external-detection-corpus'
        self.path = 'F:\\workspace\\nlp_plagiarism\\dataset\\output'
        self.unigram_suspicious_dir_path = f'{self.path}\\unigram\\suspicious_output'
        self.unigram_source_dir_path = f'{self.path}\\unigram\\source_output'
        self.unigram_suspicious_dataset_dir_path = f'{self.path}\\unigram\\suspicious_dataset'
        self.unigram_source_files = [f for f in os.listdir(self.unigram_source_dir_path) if f.endswith('.txt')]
        self.unigram_suspicious_files = [f for f in os.listdir(self.unigram_suspicious_dir_path) if f.endswith('.txt')]
        self.bigram_suspicious_dir_path = f'{self.path}\\bigram\\suspicious_output'
        self.bigram_source_dir_path = f'{self.path}\\bigram\\source_output'
        self.bigram_suspicious_dataset_dir_path = f'{self.path}\\bigram\\suspicious_dataset'
        self.bigram_source_files = [f for f in os.listdir(self.bigram_source_dir_path) if f.endswith('.txt')]
        self.bigram_suspicious_files = [f for f in os.listdir(self.bigram_suspicious_dir_path) if f.endswith('.txt')]
        self.suspicious_paragraph_number = 0
        self.source_paragraph_number = 0
        self.seeding(self.unigram_suspicious_dir_path, self.unigram_source_dir_path,
                     self.unigram_suspicious_dataset_dir_path, self.unigram_source_files, self.unigram_suspicious_files)

        self.seeding(self.bigram_suspicious_dir_path, self.bigram_source_dir_path,
                     self.bigram_suspicious_dataset_dir_path, self.bigram_source_files, self.bigram_suspicious_files)

    def seeding(self, suspicious_dir_path, source_dir_path, suspicious_dataset_dir_path, source_files, suspicious_files):

        suspicious_dir_path = suspicious_dir_path
        suspicious_files = suspicious_files
        source_dir_path = source_dir_path
        source_files = source_files
        suspicious_dataset_dir_path = suspicious_dataset_dir_path

        # print("suspicious_files:\n", suspicious_files)
        # print("source_files:\n", source_files)
        for suspicious_file_name in tqdm(suspicious_files):
            df_seeding_phase = pd.DataFrame(
                columns=['suspicious_file_name', 'suspicious_paragraph_number', 'source_file_name',
                         'source_paragraph_number', 'common_words_number'])

            # file_name = f'{path}\\{part}\\{file}'

            with open(f'{suspicious_dir_path}\\{suspicious_file_name}', 'r', encoding='utf-8-sig') as \
                    suspicious_txt_file:

                self.suspicious_paragraph_number = 0
                for suspicious_paragraph in suspicious_txt_file:

                    for source_file_name in tqdm(source_files):
                        with open(f'{source_dir_path}\\{source_file_name}', 'r', encoding='utf-8-sig') as \
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
                df_seeding_phase.to_csv(f'{suspicious_dataset_dir_path}\\{name}.csv', index=False)

            # print(df_seeding_phase.head())
            # print(df_seeding_phase.columns)
