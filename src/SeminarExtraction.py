import re
import nltk
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
#nltk.download()
st = StanfordNERTagger('../english.all.3class.distsim.crf.ser.gz',
                       '../stanford-ner.jar',
                       encoding='utf-8')

x = open("../data/seminars_untagged/304.txt").read()
header = x[:x.find('Abstract: ')]
body = x[x.find('Abstract: '):]
print(header)


def timeextract():
    timeRegEx = r"([012]?[0-9][:][0-9]{2}?\s?[ap]m)|([012]?[0-9][:][0-9]{2})|([01][0-9]?\s?[ap]m)"

    timeMatches = re.finditer(timeRegEx, header, re.MULTILINE | re.IGNORECASE)

    for matchNum, match in enumerate(timeMatches):
        print("Time match was found at {start}-{end}: {match}".format(start=match.start(),
                                                                      end=match.end(), match=match.group()))
        break


def locationextract():
    locationRegEx = r"Place:\s*([^\n]+)"
    locationMatches = re.search(locationRegEx, header, re.MULTILINE | re.IGNORECASE)

    if locationMatches:
        location = locationMatches.group(1)

        print(
            "Location match found at {start}-{end}: {group}".format(start=locationMatches.start(1),
                                                                    end=locationMatches.end(1),
                                                                    group=locationMatches.group(1)))


def stanford_tagger(text):
    tokenized_text = word_tokenize(text)
    classified_text = st.tag(tokenized_text)
    filtered_text = []
    for i in classified_text:
        if i[1] != 'O':
            filtered_text.append(i)

    # for i in range(len(filtered_text)-1):
    #     if i[1] == filtered_text[i+1]:
    #
    #         i = i+(i+1)

    print(filtered_text)


timeextract()
locationextract()
stanford_tagger(header)
