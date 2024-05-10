import preprocessing
import os


def nlp_plagiarism():
    preprocessing.Preprocessing()


def create_output_folders():
    path = 'F:\\workspace\\nlp_plagiarism\\dataset\\pan-plagiarism-corpus-2011\\external-detection-corpus'
    if not os.path.exists(f'{path}\\unigram\\source_output'):
        os.makedirs(f'{path}\\unigram\\source_output')
    if not os.path.exists(f'{path}\\unigram\\suspicious_output'):
        os.makedirs(f'{path}\\unigram\\suspicious_output')

    if not os.path.exists(f'{path}\\bigram\\source_output'):
        os.makedirs(f'{path}\\bigram\\source_output')
    if not os.path.exists(f'{path}\\bigram\\suspicious_output'):
        os.makedirs(f'{path}\\bigram\\suspicious_output')


if __name__ == "__main__":
    create_output_folders()
    nlp_plagiarism()

    print("Finished")
