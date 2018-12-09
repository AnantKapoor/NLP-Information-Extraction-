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

x = open("../data/seminars_untagged/314.txt").read()
header = x[:x.find('Abstract: ')]
body = x[x.find('Abstract: '):]

print(x)
# print(header)


def header_time():
    regex = r"([012]?[0-9][:][0-9]{2}?\s?[ap]m)|([012]?[0-9][:][0-9]{2})|([01][0-9]?\s?[ap]m)"

    subst = "<stime>\\0\\1\\2<stime>"

    result = re.sub(regex, subst, header, 1, re.MULTILINE | re.IGNORECASE)

    if result:
        # print(result)

        matches = re.finditer(regex, header, re.IGNORECASE | re.MULTILINE)
        start_time = ""
        for matchNum, match in enumerate(matches):
            matchNum = matchNum + 1
            start_time = (match.group())
            break

        # print(start_time)
        return start_time


def header_location():
    regex = r"(?<=place:    )(.*$)"
    subst = "<location>\\1<location>"
    # locationMatches = re.search(locationRegEx, header, re.MULTILINE | re.IGNORECASE)
    result = re.sub(regex, subst, header, 1, re.MULTILINE | re.IGNORECASE)

    if result:
        # print(result)
        matches = re.finditer(regex, header, re.IGNORECASE | re.MULTILINE)
        location = ""
        for matchNum, match in enumerate(matches):
            matchNum = matchNum + 1
            location = (match.group())
            break
        # print(location)
        return location


def header_speaker():
    regex = r"(?<=who:      )(.*?)(?=,|-|\n)"
    matches = re.finditer(regex, header, re.IGNORECASE | re.MULTILINE)
    speaker = ""
    for matchNum, match in enumerate(matches):
        matchNum = matchNum + 1
        speaker = (match.group())
        break
    if speaker != "":
        return speaker
    else:
        speaker = stanford_name()
        return speaker


def email_tagger():
    time = header_time()
    print("start time:", time)
    location = header_location()
    print("location:", location)
    speaker = header_speaker()
    print("speaker:", speaker)
    new_x = ""

    if time != "":
        time_regex = r"" + (re.escape(time)) + r""
        time_subst = "<stime>" + time + "<stime>"
        result = re.sub(time_regex, time_subst, x, 0, re.MULTILINE | re.IGNORECASE)

        if result:
            new_x = result

    if location != "":
        loc_regex = re.escape(location)
        loc_subst = "<location>" + location + "<location>"
        result = re.sub(loc_regex, loc_subst, new_x, 0, re.MULTILINE | re.IGNORECASE)

        if result:
            new_x = result

    if speaker != "":
        speak_regex = re.escape(speaker)
        speak_subst = "<speaker>" + speaker + "<speaker>"
        result = re.sub(speak_regex, speak_subst, new_x, 0, re.MULTILINE | re.IGNORECASE)

        if result:
            new_x = result

    print(new_x)


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


def stanford_name():
    try:
        ner_list = (structure_ne(stanford_tree(bio_tagger(stanford_tagger(header)))))
        person_int = 0
        name = ""
        for i in ner_list:
            if person_int < 2:
                if i[1] == "PERSON":
                    name = i[0]
                    person_int += 1
        # print(ner_list)
        # print(name)
        return name
    except:
        print("Failed Stanford Tagging")


email_tagger()

# stanford_name()
