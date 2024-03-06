from textraordinary import Textraordinary
import pprint as pp
import textraordinary_parsers as tp
import nltk

# Download the below file before running
# nltk.download('vader_lexicon')

def main():
    tt = Textraordinary()
    tt.load_text('sampleFiles/1989TV.txt', '1989 (TV)')
    tt.load_text('sampleFiles/debut.txt', 'debut')
    tt.load_text('sampleFiles/evermore.txt', 'evermore')
    tt.load_text('sampleFiles/fearlessTV.txt', 'fearless (TV)')
    tt.load_text('sampleFiles/folklore.txt', 'folklore')
    tt.load_text('sampleFiles/lover.txt', 'lover')
    tt.load_text('sampleFiles/midnights.txt', 'midnights')
    tt.load_text('sampleFiles/redTV.txt', 'red (TV)')
    tt.load_text('sampleFiles/reputation.txt', 'reputation')
    tt.load_text('sampleFiles/speaknowTV.txt', 'speak now (TV)')
    #tt.load_text('myfile.json', 'J', parser=tp.json_parser)

    #pp.pprint(tt.data)

    tt.wordcount_sankey(k=3)
    tt.word_clouds()
    tt.radar_chart()


if __name__ == '__main__':
    main()
