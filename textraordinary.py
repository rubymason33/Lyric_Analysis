"""
filename: textraordinary.py
description: An extensible reusable library for text analysis and comparison
"""

from collections import defaultdict, Counter
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer
import string
import sankey as sk
import pandas as pd
import pprint as pp
from wordcloud import WordCloud
import numpy as np
import plotly.graph_objects as go
import os

class ParsingError(Exception):
    pass

class Textraordinary:

    def __init__(self):
        # string  --> {filename/label --> statistics}
        # "wordcounts" --> {"A": wc_A, "B": wc_B, ....}
        self.data = defaultdict(dict)

    def _save_results(self, label, results):
        for k, v in results.items():
            self.data[k][label] = v

    @staticmethod
    def load_stop_words(stopfile):
        """
        Input argument is text file
        return: a list of stopwords from file """

        stop_words = []
        with open(stopfile, 'r') as file:
            for line in file:
                word = line.strip()
                stop_words.append(word)
        return stop_words

    @staticmethod
    def _default_parser(filename, stopwords_file):
        """ Updated parser that removes punctuation,
        converts to lowercase, removes stop words, and
        counts the occurrences of each word. """

        # nltk.download('vader_lexicon')

        stopwords = Textraordinary.load_stop_words(stopwords_file)

        with open(filename, 'r') as file:
            text = file.read()

        # parser exception
        file, actual_type = os.path.splitext(filename)
        expected_type = '.txt'

        if actual_type != expected_type:
            raise ParsingError(
                'Parser received wrong file type, expected: ' + expected_type + ' got: ' + actual_type
            )


        processed_text = ''.join(
            char.lower() if char != '-' else ' ' for char in text if char not in string.punctuation).split()

        words = [word for word in processed_text if word not in stopwords]

        sia = SentimentIntensityAnalyzer()
        pos, neg, neu = zip(*((sia.polarity_scores(word)['pos'], sia.polarity_scores(word)['neg'],
                               sia.polarity_scores(word)['neu']) for word in words if word in sia.lexicon))
        results = {
            'wordcount': Counter(words),
            'total_words': len(words),
            'unique_words': len(set(words)),
            'mean_word_length': round(sum(len(word) for word in words) / len(words), 5) if len(words) > 0 else 0,
            'sentiment_score': round(
                sum(sia.polarity_scores(word)['compound'] for word in words
                    if word in SentimentIntensityAnalyzer().lexicon) / len(words), 5) if len(words) > 0 else 0,
            'pos': round(sum(pos) / len(words), 5),
            'neg': round(sum(neg) / len(words), 5),
            'neu': round(sum(neu) / len(words), 5),
            'cleaned_text': ' '.join(words)
        }

        return results

    def load_text(self, filename, label=None, parser=None):
        """ Registers a text document with the framework
        Extracts and stores data to be used in later
        visualizations. """

        if parser is None:
            results = Textraordinary._default_parser(filename, 'stopwords/stopwords.txt')
        else:
            results = parser(filename)

        if label is None:
            label = filename

        # store the results of processing one file
        # in the internal state (data)
        self._save_results(label, results)

    def compare_num_words(self):
        """ A DEMONSTRATION OF A CUSTOM VISUALIZATION
        A trivially simple barchart comparing number
        of words in each registered text file. """

        num_words = self.data['numwords']
        for label, nw in num_words.items():
            plt.bar(label, nw)
        plt.show()

    def wordcount_sankey(self, word_list=None, k=5):
        # find most common words
        if word_list is None:
            most_common_words = []
            for label in self.data['wordcount'].keys():
                most_common_words += [tup[0] for tup in self.data['wordcount'][label].most_common(k) if tup[0]
                                      not in most_common_words]
        else:
            most_common_words = word_list

        data = {'text': [], 'word': [], 'word_count': []}

        for word in most_common_words:
            for label in self.data['wordcount'].keys():
                if word in self.data['wordcount'][label]:
                    data['text'].append(label)
                    data['word'].append(word)
                    data['word_count'].append(self.data['wordcount'][label][word])

        skdf = pd.DataFrame(data)

        sk.make_sankey(skdf, 'text', 'word', vals='word_count')  # save='taylorSwiftSankey.png'

    def word_clouds(self, selected_text_list=None, num_row=2, num_col=5):
        if selected_text_list is None:
            selected_text_list = self.data['wordcount'].keys()

        # set up subplots
        fig, axs = plt.subplots(num_row, num_col, figsize=(55, 25))

        # create wc for each text provided
        for i, text in enumerate(selected_text_list):
            row_index = i // num_col
            col_index = i % num_col
            ax = axs[row_index, col_index] if num_row > 1 else axs[col_index]

            word_count = self.data['wordcount'][text]

            # make wc
            wordcloud = WordCloud(background_color='white', width=100, height=100).generate_from_frequencies(word_count)

            # Display the wc in subplot
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.set_title(text, fontsize=100, y=-0.2)
            ax.axis('off')

        plt.show()
        # plt.savefig('TaylorSwiftSongsWordClouds.png')

    def radar_chart(self):
        """ Generate a radar chart for each album with positive, negative, and neutral sentiment scores. """

        neutral_scores = [self.data['neu'][label] for label in self.data['wordcount'].keys()]
        positive_scores = [self.data['pos'][label] for label in self.data['wordcount'].keys()]
        negative_scores = [self.data['neg'][label] for label in self.data['wordcount'].keys()]

        names = list(self.data['wordcount'].keys())

        positive_trace = go.Scatterpolar(
            r=positive_scores + [positive_scores[0]],
            theta=names + [names[0]],
            fill='toself',
            name='Positive'
        )

        negative_trace = go.Scatterpolar(
            r=negative_scores + [negative_scores[0]],
            theta=names + [names[0]],
            fill='toself',
            name='Negative'
        )

        neutral_trace = go.Scatterpolar(
            r=neutral_scores + [neutral_scores[0]],
            theta=names + [names[0]],
            fill='toself',
            name='Neutral'
        )

        layout = go.Layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 0.2]
                )
            ),
            showlegend=True
        )

        fig = go.Figure(data=[positive_trace, negative_trace, neutral_trace], layout=layout)

        fig.show()
        # plt.savefig('taylorSwiftRadarChart.png')


