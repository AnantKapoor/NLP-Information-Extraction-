import re
import nltk
from nltk.tag import StanfordNERTagger
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.chunk import conlltags2tree
from nltk.tree import Tree

# nltk.download()
st = StanfordNERTagger('../english.all.3class.distsim.crf.ser.gz',
                       '../stanford-ner.jar',
                       encoding='utf-8')

x = open("../data/seminars_untagged/301.txt").read()
header = x[:x.find('Abstract: ')]
body = x[x.find('Abstract: '):]
print(header)


def time_extract():
    timeRegEx = r"([012]?[0-9][:][0-9]{2}?\s?[ap]m)|([012]?[0-9][:][0-9]{2})|([01][0-9]?\s?[ap]m)"

    timeMatches = re.finditer(timeRegEx, header, re.MULTILINE | re.IGNORECASE)

    for matchNum, match in enumerate(timeMatches):
        print("Time match was found at {start}-{end}: {match}".format(start=match.start(),
                                                                      end=match.end(), match=match.group()))
        break


def location_extract():
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
    ne_tagged_text = st.tag(tokenized_text)
    return ne_tagged_text


def bio_tagger(ne_tagged):
    bio_tagged = []
    prev_tag = "O"
    for token, tag in ne_tagged:
        if tag == "O":  # O
            bio_tagged.append((token, tag))
            prev_tag = tag
            continue
        if tag != "O" and prev_tag == "O":  # Begin NE
            bio_tagged.append((token, "B-" + tag))
            prev_tag = tag
        elif prev_tag != "O" and prev_tag == tag:  # Inside NE
            bio_tagged.append((token, "I-" + tag))
            prev_tag = tag
        elif prev_tag != "O" and prev_tag != tag:  # Adjacent NE
            bio_tagged.append((token, "B-" + tag))
            prev_tag = tag
    return bio_tagged


def stanford_tree(bio_tagged):
    tokens, ne_tags = zip(*bio_tagged)
    pos_tags = [pos for token, pos in pos_tag(tokens)]

    conlltags = [(token, pos, ne) for token, pos, ne in zip(tokens, pos_tags, ne_tags)]
    ne_tree = conlltags2tree(conlltags)
    return ne_tree


# Parse named entities from tree
def structure_ne(ne_tree):
    ne = []
    for subtree in ne_tree:
        if type(subtree) == Tree:  # If subtree is a noun chunk, i.e. NE != "O"
            ne_label = subtree.label()
            ne_string = " ".join([token for token, pos in subtree.leaves()])
            ne.append((ne_string, ne_label))
    return ne


def stanford_main():
    print(structure_ne(stanford_tree(bio_tagger(stanford_tagger(header)))))


time_extract()
location_extract()
stanford_main()

# stanford_tagger(header)
