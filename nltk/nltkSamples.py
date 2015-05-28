import nltk
from nltk.corpus import gutenberg
from nltk import FreqDist
'''
Please note, you will have to have downloaded the example files using
nltk.download() for this to work. The example texts are not included in the
base install. It does not use any of the graphing abilities, though, so NumPy
and matplotlib are not required.

The program uses NLTK's pre-packaged texts to quickly go over 2 works and
compare the usage of the most common words. The pre-packed texts are already
tokenized, so using them saves us (or saves Python) the work of breaking it into
sentences and then individual words and punctuation. All that is not hard,
particularly from the programmer's perspective (nltk.tokenize.sent_tokenize() 
andn ltk.tokenize.word_tokenize()), but if it comes with premade example files,
might as well use em.

Sorry that the output is kind of messy, it's mostly just to show what the
toolkit can do. Obviously, you would want to work out a better way to display
the data if you were to show it to people.

A couple of interesting sites:
http://streamhacker.com/
http://textminingonline.com/dive-into-nltk-part-i-getting-started-with-nltk

'''
# Import the words for both and, for later, the full text for Moby Dick
emma = gutenberg.words('austen-emma.txt')
moby_dick = gutenberg.words('melville-moby_dick.txt')
moby_dick_full = nltk.Text(nltk.corpus.gutenberg.words('melville-moby_dick.txt'))

# Get a frequency distribution so we can, among other things, get the most
# common words
fd_emma = FreqDist(emma)
fd_moby_dick = FreqDist(moby_dick)

# Get those most common words
emma_top_50 = fd_emma.most_common(50)
moby_dick_top_50 = fd_moby_dick.most_common(50)

# Using a list comprehension, build up a list of the words that are in Emma's
# top 50 words, but not in Moby Dick's top 50
words_in_conflict = [x[0] for x in emma_top_50 if x[0] not in \
                    [y[0] for y in moby_dick_top_50]]

comparison = []

# Go over the words in the list, make a ratio of how often they are used in
# Moby Dick compared to Emma (one of them has to be a float for the division to
# work), then put that in a tuple with the word itself.
# The %.2f is just a placeholder saying put a float to 2 decimal places here
for word in words_in_conflict:
    ratio = (float(fd_moby_dick[word]) / fd_emma[word])*100
    temporary_tuple = (word, "%.2f" % ratio)
    comparison.append(temporary_tuple)

print "Top 50 samples in Emma: ",emma_top_50,"\n"
print "Top 50 samples in Moby Dick: ",moby_dick_top_50,"\n"
print comparison

# Lets us see how the words from the comparison list are contextualized 
# in Moby Dick
for word in words_in_conflict:
    print "Context for %s: " % word
    moby_dick_full.concordance(word)