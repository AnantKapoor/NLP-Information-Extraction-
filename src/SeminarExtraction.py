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


def main():
    for i in range(184):
        print(i)
        x = open("../data/seminars_untagged/" + str(301 + i) + ".txt").read()
        header = x[:x.find('Abstract: ')]
        body = x[x.find('Abstract: '):]

        email_tagger(x, header, i)
    check_tags_main()


def header_time(header):
    regex = r"([012]?[0-9][:][0-9]{2}?\s?[ap]m)|([012]?[0-9][:][0-9]{2})|([01][0-9]?\s?[ap]m)"

    subst = "<stime>\\0\\1\\2</stime>"

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


def header_location(header):
    regex = r"(?<=place:    )(.*$)"
    subst = "<location>\\1</location>"
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


def header_speaker(header):
    regex = r"(?<=who:      )(.*?)(?=,|-| / |\n)"
    matches = re.finditer(regex, header, re.IGNORECASE | re.MULTILINE)
    speaker = ""
    for matchNum, match in enumerate(matches):
        matchNum = matchNum + 1
        speaker = (match.group())
        break
    if speaker != "":
        return speaker
    else:
        try:
            speaker = stanford_name()
            return speaker
        except:
            # print("failed st tagging")
            return []


def sentence_tagger(new_x):
    regex = r"\s+[A-Za-z,;'\"\s]+[.?!]$"

    subst = "<sentence>\\0</sentence>"
    result = re.sub(regex, subst, new_x, 0, re.IGNORECASE | re.MULTILINE)

    if result:
        return result
        # print(result)


def email_tagger(x, header, i):
    time = header_time(header)
    # print("start time:", time)
    location = header_location(header)
    # print("location:", location)
    speaker = header_speaker(header)
    # print("speaker:", speaker)
    new_x = ""

    if time != "":
        time_regex = r"" + (re.escape(time)) + r""
        time_subst = "<stime>" + time + "</stime>"
        result = re.sub(time_regex, time_subst, x, 0, re.MULTILINE | re.IGNORECASE)

        if result:
            new_x = result

    if location != "":
        loc_regex = re.escape(location)
        loc_subst = "<location>" + location + "</location>"
        result = re.sub(loc_regex, loc_subst, new_x, 0, re.MULTILINE | re.IGNORECASE)

        if result:
            new_x = result

    if speaker != "":
        try:
            speak_regex = re.escape(speaker)
            speak_subst = "<speaker>" + speaker + "</speaker>"
            result = re.sub(speak_regex, speak_subst, new_x, 0, re.MULTILINE | re.IGNORECASE)

            if result:
                new_x = result

        except:
            print("failed to tag speaker")

    tagged = sentence_tagger(new_x)
    print(tagged)
    with open('../data/test_untagged/' + str(301 + i) + '.txt', 'r+') as f:
        # convert to string:
        f.seek(0)
        f.write(tagged)
        f.truncate()


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


def check_tags_main():
    true_positive = 0
    false_positive = 0
    false_negative = 0

    for i in range(184):
        test = open("../data/test_tagged/" + str(301 + i) + ".txt").read()
        my_tagged = open("../data/test_untagged/" + str(301 + i) + ".txt").read()

        mytagged_time = check_all_tags('stime', my_tagged)
        test_time = check_all_tags('stime', test)
        mytagged_location = check_all_tags('location', my_tagged)
        test_location = check_all_tags('location', test)
        mytagged_speaker = check_all_tags('speaker', my_tagged)
        test_speaker = check_all_tags('speaker', test)
        mytagged_sentence = check_all_tags('sentence', my_tagged)
        test_sentence = check_all_tags('sentence', test)
        mytagged_paragraph = check_all_tags('paragraph', my_tagged)
        test_paragraph = check_all_tags('paragraph', test)

        print('mytagged_time', mytagged_time)
        print('test_time', test_time)
        print('test_location', test_location)
        print('mytagged_location', mytagged_location)
        print('mytagged_speaker', mytagged_speaker)
        print('test_speaker', test_speaker)
        print('test_sentence', test_sentence)
        print('mytagged_sentence', mytagged_sentence)
        print('test_paragraph', test_paragraph)

        try:
            i=0
            for i in range(len(mytagged_time)):
                if mytagged_time[i] == test_time[i]:
                    true_positive += 1
                elif mytagged_time[i] != test_time[i]:
                    false_positive += 1
        except:
            print("")
        try:
            i=0
            for i in range(len(test_time)):
                if test_time[i] != mytagged_time[i]:
                    false_negative += 1
        except:
            print("")

        try:
            i = 0
            for i in range(len(mytagged_location)):
                if mytagged_time[i] == test_time[i]:
                    true_positive += 1
                elif mytagged_location[i] != test_location[i]:
                    false_positive += 1
        except:
            print("")
        try:
            i = 0
            for i in range(len(test_location)):
                if test_location[i] != mytagged_location[i]:
                    false_negative += 1
        except:
            print("")
        try:
            i = 0
            for i in range(len(mytagged_speaker)):
                if mytagged_speaker[i] == test_speaker[i]:
                    true_positive += 1
                elif mytagged_speaker[i] != test_speaker[i]:
                    false_positive += 1
        except:
            print("")
        try:
            i = 0
            for i in range(len(test_speaker)):
                if test_speaker[i] != mytagged_speaker[i]:
                    false_negative += 1
        except:
            print("")
        try:
            i = 0
            for i in range(len(mytagged_sentence)):
                if mytagged_sentence[i] == test_sentence[i]:
                    true_positive += 1
                elif mytagged_sentence[i] != test_sentence[i]:
                    false_positive += 1
        except:
            print("")
        try:
            i = 0
            for i in range(len(test_sentence)):
                if test_sentence[i] != mytagged_sentence[i]:
                    false_negative += 1
        except:
            print("")
        try:
            i = 0
            for i in range(len(test_paragraph)):
                if test_paragraph[i] != mytagged_paragraph[i]:
                    false_negative += 1
        except:
            print("")
        try:
            i = 0
            for i in range(len(mytagged_paragraph)):
                if mytagged_paragraph[i] == test_paragraph[i]:
                    true_positive += 1
                elif mytagged_paragraph[i] != test_paragraph[i]:
                    false_positive += 1
        except:
            print("")

    f1_score = f1(precision(true_positive, false_positive), recall(true_positive,false_negative))
    print("f1 score: ", f1_score)

    # print("checked tags")


def check_all_tags(tag, text):
    reg = re.compile(rf'(?<=<{tag}>)([\w\W]+?)(?=</{tag}>)', re.IGNORECASE | re.MULTILINE)

    return reg.findall(text)


def precision(true_p, false_p):

    total_p_p = true_p + false_p
    try:
        pre = true_p / total_p_p
        print("precision:", pre)
        return pre
    except:
        print("precision failed")


def recall(true_p, false_n):

    total_a_p = true_p + false_n
    try:
        rec = true_p / total_a_p
        print("recall: ", rec)
        return rec
    except:
        print("recall failed")


def f1(pre, rec):
    try:
        f1_score = 2 * ((pre * rec) / (pre + rec))
        return f1_score
    except:
        print("f1 calculation failed")

# email_tagger()
# stanford_name()
main()
