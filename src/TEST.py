import re

x = open("seminars_untagged/345.txt").read()
header = x[:x.find('Abstract: ')]
print(header)

locationRegEx = r"Place:\s*([^\n]+)"
locationMatches = re.search(locationRegEx, header, re.MULTILINE | re.IGNORECASE)

if locationMatches:
    print("Match was found at {start}-{end}: {match}".format(start=locationMatches.start(), end=locationMatches.end(),
                                                             match=locationMatches.group()))
    for groupNum in range(0, len(locationMatches.groups())):
        groupNum = groupNum + 1

        print(
            "Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum, start=locationMatches.start(groupNum),
                                                                      end=locationMatches.end(groupNum),
                                                                      group=locationMatches.group(groupNum)))


# regex = r"([012]?[0-9][:][0-9]{2}?\s?[ap]m)|([012]?[0-9][:][0-9]{2})|([01][0-9]?\s?[ap]m)"
#
# test_str = ("Type:     cmu.cs.robotics\n"
#             "Who:      John Bares\n"
#             "          The Robotics Institute\n"
#             "          Carnegie Mellon University\n"
#             "Topic:    Dante II and Beyond: Exploration Robots\n"
#             "Dates:    18-Nov-94\n"
#             "Time:     3:30 PM - 5:00 PM\n"
#             "Place:    ADAMSON WING Auditorium in Baker Hall\n"
#             "Host:     Yangsheng Xu (xu+@cs.cmu.edu)\n"
#             "PostedBy: xu+ on 14-Nov-94 at 08:00 from IUS4.IUS.CS.CMU.EDU (Yangsheng Xu)")
#
# matches = re.finditer(regex, test_str, re.MULTILINE | re.IGNORECASE)
#
# for matchNum, match in enumerate(matches):
#     matchNum = matchNum + 1
#
#     print("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum=matchNum, start=match.start(),
#                                                                         end=match.end(), match=match.group()))
#
#     for groupNum in range(0, len(match.groups())):
#         groupNum = groupNum + 1
#
#         print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum, start=match.start(groupNum),
#                                                                         end=match.end(groupNum),
#                                                                         group=match.group(groupNum)))
#
#
#
