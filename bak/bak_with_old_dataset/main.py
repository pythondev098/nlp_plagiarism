import preprocessing
import seeding
import os


def nlp_plagiarism():
    preprocessing.Preprocessing()
    seeding.Seeding()


def create_output_folders():
    path = 'F:\\workspace\\nlp_plagiarism\\dataset\\output'
    if not os.path.exists(f'{path}\\unigram\\source_output'):
        os.makedirs(f'{path}\\unigram\\source_output')
    if not os.path.exists(f'{path}\\unigram\\suspicious_output'):
        os.makedirs(f'{path}\\unigram\\suspicious_output')
    if not os.path.exists(f'{path}\\unigram\\suspicious_dataset'):
        os.makedirs(f'{path}\\unigram\\suspicious_dataset')

    if not os.path.exists(f'{path}\\bigram\\source_output'):
        os.makedirs(f'{path}\\bigram\\source_output')
    if not os.path.exists(f'{path}\\bigram\\suspicious_output'):
        os.makedirs(f'{path}\\bigram\\suspicious_output')
    if not os.path.exists(f'{path}\\bigram\\suspicious_dataset'):
        os.makedirs(f'{path}\\bigram\\suspicious_dataset')


if __name__ == "__main__":
    create_output_folders()
    nlp_plagiarism()

    print("Finished")
