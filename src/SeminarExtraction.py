import re
import nltk

# x = nltk.data.load("301.txt")
x = open("seminars_untagged/334.txt").read()
header = x[:x.find('Abstract: ')]
body = x[x.find('Abstract: '):]
print(header)

# ################ EXTRACT TIME ################
timeRegEx = r"([012]?[0-9][:][0-9]{2}?\s?[ap]m)|([012]?[0-9][:][0-9]{2})|([01][0-9]?\s?[ap]m)"

timeMatches = re.finditer(timeRegEx, header, re.MULTILINE | re.IGNORECASE)

for matchNum, match in enumerate(timeMatches):

    print("Time match was found at {start}-{end}: {match}".format(start=match.start(),
                                                                        end=match.end(), match=match.group()))
    break


# print(header)




# ################ EXTRACT LOCATION ################
# locationRegEx = r"Place:\s*([^\n]+)"
# locationMatches = re.search(locationRegEx, header, re.MULTILINE | re.IGNORECASE)
#
# if locationMatches:
#     location = locationMatches.group(1)
#
#     print(
#         "Location match found at {start}-{end}: {group}".format(start=locationMatches.start(1),
#                                                        end=locationMatches.end(1),
#                                                        group=locationMatches.group(1)))







