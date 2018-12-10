import re
import os
import sys

from glob import iglob
from collections import Counter


def remove_garbage(text):
    text = re.sub(r'\W+', ' ', text)
    text = text.lower()
    return text


def word_freq_corpus():
    counter = Counter()
    for filepath in iglob(os.path.join('../data/seminars_untagged', '*.txt')):
        with open(filepath, 'r') as filehandle:
            words = set(remove_garbage(filehandle.read()).split())
            counter.update(words)

    for word, count in counter.most_common(50):
        print('{}  {}'.format(word, count))


def word_freq_email():
    filename = '../data/seminars_untagged/400.txt'
    x = open(filename).read()
    header = x[:x.find('Abstract: ')]
    body = x[x.find('Abstract: '):]
    words = re.findall(r'\w+', open(filename).read().lower())

    # print(header)
    print(x)
    counts = Counter(words)
    common_words = counts.most_common(10)
    print(common_words)


def header_topic():
    regex = r"(?<=topic:).*"
    matches = re.finditer(regex, header, re.IGNORECASE | re.MULTILINE)

    for matchNum, match in enumerate(matches):
        matchNum = matchNum + 1

        print("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum=matchNum, start=match.start(),
                                                                            end=match.end(), match=match.group()))

        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1

            print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum,
                                                                            start=match.start(groupNum),
                                                                            end=match.end(groupNum),
                                                                            group=match.group(groupNum)))


word_freq_corpus()

word_freq_email()

# header_topic()
