from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import csv


class word_search:
    def __init__(self, searched_words,filename):
        self.searched_words = searched_words
        self.filename = filename
        self.descr_list = []
        self.cleaned_words = []

        self.searched_word_count = {el:0 for el in self.searched_words}


    def file_to_list(self):
        with open(self.filename,newline='') as f:
            reader = csv.reader(f)
            self.descr_list = list(reader)

    def tokenize_and_clean(self):
        cachedstopwords = stopwords.words("english")
        tokenizer = RegexpTokenizer(r'\w+')

        descr_no_punct = tokenizer.tokenize(str(self.descr_list))

        self.cleaned_words = [word.lower() for word in descr_no_punct if word.lower() not in cachedstopwords]

    def word_search_counter(self):
        count = 0
        for word in self.cleaned_words:
            for s_word in self.searched_words:
                if s_word == word:
                    self.searched_word_count[s_word] += 1

    def complete(self):
        self.file_to_list()
        print('\n{} jobs have been searched. The result is:\n'.format(len(self.descr_list)))
        self.tokenize_and_clean()
        self.word_search_counter()

        print(self.searched_word_count)

        return self.searched_word_count

# search1 = word_search(keywords_to_search,'Engineer_Canada_JobDescript_2020-04-07.csv')
# search1.complete()


#fdist1 = FreqDist(words)
#
# cleaned_words_count = Counter(cleaned_words)
# print(cleaned_words_count.most_common(30))
