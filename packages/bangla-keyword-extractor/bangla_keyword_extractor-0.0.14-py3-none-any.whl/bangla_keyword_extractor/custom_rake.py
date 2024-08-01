from rake_nltk import Rake

class BanglaRake(Rake):
    def _tokenize_text_to_sentences(self, text):
        return self.sentence_tokenizer.basic_tokenizer(text)
    def _tokenize_sentence_to_words(self, sentence):
        return self.word_tokenizer.basic_tokenizer(sentence)