import preprocessing
import seeding
import os


def nlp_plagiarism():
    training_source_path = '.\\dataset\\pan13-authorship-verification-test-and-training\\' \
                                'pan13-authorship-verification-training-corpus-2013-02-01'
    test_source_path = '.\\dataset\\pan13-authorship-verification-test-and-training\\' \
                       'pan13-authorship-verification-test-corpus2-2013-05-29'

    training_source_dir_name = os.listdir(training_source_path)
    print(training_source_dir_name)
    test_source_dir_name = os.listdir(test_source_path)
    print(test_source_dir_name)

    preprocessing.Preprocessing(training_source_path, test_source_path, training_source_dir_name, test_source_dir_name)
    seeding.Seeding(training_source_path, test_source_path, training_source_dir_name, test_source_dir_name)

#
# def create_output_folders():
#     path = 'F:\\workspace\\nlp_plagiarism\\dataset\\output'
#     if not os.path.exists(f'{path}\\unigram\\source_output'):
#         os.makedirs(f'{path}\\unigram\\source_output')
#     if not os.path.exists(f'{path}\\unigram\\suspicious_output'):
#         os.makedirs(f'{path}\\unigram\\suspicious_output')
#     if not os.path.exists(f'{path}\\unigram\\suspicious_dataset'):
#         os.makedirs(f'{path}\\unigram\\suspicious_dataset')
#
#     if not os.path.exists(f'{path}\\bigram\\source_output'):
#         os.makedirs(f'{path}\\bigram\\source_output')
#     if not os.path.exists(f'{path}\\bigram\\suspicious_output'):
#         os.makedirs(f'{path}\\bigram\\suspicious_output')
#     if not os.path.exists(f'{path}\\bigram\\suspicious_dataset'):
#         os.makedirs(f'{path}\\bigram\\suspicious_dataset')


if __name__ == "__main__":
    # create_output_folders()
    nlp_plagiarism()

    print("Finished")
