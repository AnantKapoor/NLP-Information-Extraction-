# 1 INTRODUCTION

Given that this assignment allowed the ability to use any NLP technique
we’ve covered so far, I felt that the most obvious technique was to use
RegEx. In this assignment I have used mainly RegEx in order to complete
the task of tagging the emails with the relevant tags. I have however
augmented this with the use of NER tagging where relevant .

# 2 METHODS
## 2.1 Extracting data from header
For this first part, I used the fact that many of the tagged entities that
were needed were present in the header. This included: time, location
and speaker in some cases. By using simple RegEx (regex look-behinds)
to extract the line after a keyword (’who: ’,’place: ’ and ’time: ’) I was
able to obtain the start time, location and speaker just from the header.
2.1.1 Stanford NER Tagging In the cases where the speaker was not
explicitly mentioned using ’who:’ I implemented the use of the Stanford
NER tagger, which has the ability to extract names and organisations to
a great extent. By using the Stanford tagger I would extract the second
occurring name in the the header. The reasoning behind this was the first
name in the header of every email would always be the name of the sender
of the email. Using this pattern I was able to tag names in the header for
the speaker as the next occurring name in the header would most often be
the speaker.
I am not using this as the primary method of extracting names from
headers, however, as the F1 score in this situation was lower than when
using RegEx as the primary method. Using RegEx look-behinds proved
far more reliable when ’who:’ existed in the header resulting in an f1
score of [0.673] comparing to [0.335] when NER tagging was used
primarily. As well as a accuracy being an issue with Stanford NER, the
time to extract the name using NER is vastly longer than using RegEx
## 2.2 Using data from header to tag body of email
Using the tags assigned to local variables for each relevent entity, I would
use RegEx to search through the entire email again using the contents of
the variables as the RegEx query. Using the re.sub method I was able to
find all instances of time, location and speaker and replace them with the
tagged entities. Since you are not able to use the header to extract any
information relating to sentences or paragraphs, I implemented RegEx
again in order to find sentences. However from implementing this I was
finding visually that my RegEx was very faulty and therefore would have
a low f1 score.

## 2.3 Overwriting existing files
Having Iterated through the entire directory of untagged seminar emails
resulting in a string, I now overwrote the corresponding untagged files in
the directory ’test-untagged’ with the tagged emails. The result of this is
the ability to calculate precision, recall and F1 score of the entity tagging.

## 2.4 Obtaining F1-score
As I now have a directory of emails that I have tagged myself, I can now
directly compare these emails to the pre-tagged data. Using RegEx, I
have extracted all the tags from both directories of emails. For each email,
I compare the list of entity tags obtained from corresponding files. Using
these lists I directly compare them to one another, from this I am able to
obtain the number of instances of true positives, false positives and false
negatives. The total of each of these values from all of the emails are then
used in turn to calculate precision, recall and the F1 score.

# 3 RESULTS
With all entities:
- Precision:0.464
- Recall: 0.456
- F1 score: 0.460 

Without sentences and paragraphs:
- F1-score: 0.835

# 4 CONCLUSION
To conclude there are multiple ways I could improve the overall F1 score.
Rather than just relying on the header, I could have also used the main
body of the email to extract information about entities. These could
include extracting the speaker by searching for text that such as: ’The
speaker will be...’ and for location, ’the seminar will be held at...’. My
sentence tagging and paragraph tagging affected my f1 score the most
with my f1-score being 0.835 without these two entities, with more time
I feel that I would’ve been able to further develop the NLP techniques for
tagging these entities.
Areas where I feel that my entity tagger performed well were my time
tagging (f1: 0.81) and location (f1: 0.91), however I feel that the results
for these are better than other entities as these entities were regularly
easily identified in the header of the email. Therefore I feel that my
underlying method to first extract data from the header was a success,
however given more time I feel that I should have augmented this more
advanced NLP techniques.

