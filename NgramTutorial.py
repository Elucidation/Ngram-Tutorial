
# coding: utf-8

# # IPython Notebook - N-gram Tutorial
# 
# I've always wondered how chat bots like [Alice](http://alice.pandorabots.com/) work. Now, they are obviously much more complex than this tutorial will delve into, but we can touch on some of the core principles. One of them is this idea of understanding the relationships between words in sentences. How can we get a machine to understand these relationships?
# 
# Turns out there's the right way, and then there's the easy way. The right way involves delving deep into [semantic networks](https://en.wikipedia.org/wiki/Semantic_network) and ontologies, something I'd touched upon in my climate modelling days, but never mind that; We're doing **The Easy Way**.
# 
# ### The Easy Way
# 
# Conversely, the easy way to learn the relationships is by throwing lots of data *en masse* at a machine, and letting it build up a model of the relationships (*this sounds suspiciously like Machine Learning*). 
# 
# An even simpler form of that is to track the number of words that are in sequence with one another, and keeping track of the frequency at which this occurs. We're actually starting to describe something that uses [N-grams](https://en.wikipedia.org/wiki/N-gram). An N-gram is a contiguous (*order matters*) sequence of items, which in this case is the words in text.
# 
# What we want to do is build up a dictionary of N-grams, which are pairs, triplets or more (*the N*) of words that pop up in the training data, with the value being the number of times they showed up. After we have this dictionary, as a naive example we could actually predict sentences by just randomly choosing words within this dictionary and doing a weighted random sample of the connected words that are part of n-grams within the keys.
# 
# Lets see how far we can get with N-grams without outside resources.
# 
# ---
# 
# We have a text file for [Pride and Prejudice from Project Gutenberg](https://www.gutenberg.org/ebooks/1342) stored as `pg1342.txt` in the same folder as our notebook, but also available online directly. Let's load the text to a string since it's only 701KB, which will fit in memory nowadays. 
# 
#     *Note* : If we wanted to be more memory efficient we should parse the text file on a line or character by character basis, storing as needed, etc.

# In[1]:

# Find the number links by looking on Project Gutenberg in the address bar for a book.
books = {'Pride and Prejudice': '1342',
         'Huckleberry Fin': '76',
         'Sherlock Holmes': '1661'}

book = books['Pride and Prejudice']

# Load text from Project Gutenberg URL
import urllib2
url_template = 'https://www.gutenberg.org/cache/epub/%s/pg%s.txt'

f = urllib2.urlopen(url_template % (book, book), 'r')
txt = f.read()
f.close()
# with  as f:
#     txt = f.read()

# See the number of characters and the first 50 characters to confirm it is there    
print len(txt), ',', txt[:50] , '...'


# Great, now lets split into words into a big list, splitting on anything non-alphanumeric [A-Za-z0-9] (as well as punctuation) and forcing everything lowercase

# In[2]:

import re
words = re.split('[^A-Za-z]+', txt.lower())
words = filter(None, words) # Remove empty strings

# Print length of list
print len(words)



# ## Sets
# From this we can now generate N-grams, lets start with a 1-gram, basically the set of all the words
# 
#     *Note* : One could use a dictionary instead of a set and keeping count of the occurances gives word frequency

# In[3]:

import sets

# Create set of all unique words, this throws away any information about frequency however
gram1 = set(words)

print len(gram1)

# Instead of printing all the elements in the set, create an iterator and print 20 elements only
gram1_iter = iter(gram1)
print [gram1_iter.next() for i in xrange(20)]


# Lets try and get the 2-gram now, which is pairs of words. Let's have a quick look to see the last 10 and how they look.

# In[4]:

# See the last 10 pairs
for i in xrange(len(words)-10, len(words)-1):
    print words[i], words[i+1]


# Okay, seems good, lets get all word pairs, and then generate a set of unique pairs from it

# In[5]:

word_pairs = [(words[i], words[i+1]) for i in xrange(len(words)-1)]
print len(word_pairs)

gram2 = set(word_pairs)
print len(gram2)

# Print 20 elements from gram2
gram2_iter = iter(gram2)
print [gram2_iter.next() for i in xrange(20)]


# ## Frequency
# 
# Okay, that was fun, but this isn't enough, we need frequency if we want to have any sense of probabilities, which is what N-grams are about. Instead of using sets, lets create a dictionary with counts

# In[6]:

gram1 = dict()

# Populate 1-gram dictionary
for word in words:
    if gram1.has_key(word):
        gram1[word] += 1
    else:
        gram1[word] = 1 # Start a new entry with 1 count since saw it for the first time.

# Turn into a list of (word, count) sorted by count from most to least
gram1 = sorted(gram1.items(), key=lambda (word, count): -count)

# Print top 20 most frequent words
print gram1[:20]


# For Pride and Prejudice, the words 'the', 'to', 'of', and 'and' were the top four most common words. Sounds about right, not too interesting yet, lets see what happens with 2-grams.

# In[7]:

gram2 = dict()

# Populate 2-gram dictionary
for i in xrange(len(words)-1):
    key = (words[i], words[i+1])
    if gram2.has_key(key):
        gram2[key] += 1
    else:
        gram2[key] = 1

# Turn into a list of (word, count) sorted by count from most to least
gram2 = sorted(gram2.items(), key=lambda (_, count): -count)

# Print top 20 most frequent words
print gram2[:20]


# It looks like `"of the"` and `"to be"` are the top two most common 2-grams, sounds good. 
# 
# ## Next word prediction
# What can we do with this? Well lets see what happens if we take a random word from all the words, and build a sentence by just choosing the most common pair that has that word as it's start.

# In[8]:

start_word = words[len(words)/4]
print start_word


# I just went ahead and chose the word that appears $1/4$ of the way into words, random enough.
# 
# Now in a loop, iterate through the frequency list (most frequent first) and see if it matches the first word in a pair, if so, the next word is the second element in the word pair, and continue with that word. Stop after N words or the list does not contain that word.
# 
#     *Note* : gram2 is a list that contains (key,value) where key is a word pair (first, second),
#              so you need element[0][0] for first word and element [0][1] for second word

# In[9]:

def get2GramSentence(word, n = 50):
    for i in xrange(n):
        print word,
        # Find Next word
        word = next((element[0][1] for element in gram2 if element[0][0] == word), None)
        if not word:
            break

word = start_word
print "Start word: %s" % word

print "2-gram sentence: \"",
get2GramSentence(word, 20)
print "\""


# It gets stuck in a loop pretty much straight away. Not very interesting, try out other words and see what happens.

# In[10]:

for word in ['and', 'he', 'she', 'when', 'john', 'never', 'i', 'how']:
    print "Start word: %s" % word

    print "2-gram sentence: \"",
    get2GramSentence(word, 20)
    print "\""


# ## Weighted random choice based on frequency
# Same thing. Okay, lets randomly choose from the subset of all 2grams that matches the first word, using a weighted-probability based on counts.

# In[11]:

import random
def weighted_choice(choices):
   total = sum(w for c, w in choices)
   r = random.uniform(0, total)
   upto = 0
   for c, w in choices:
      if upto + w > r:
         return c
      upto += w
    
def get2GramSentenceRandom(word, n = 50):
    for i in xrange(n):
        print word,
        # Get all possible elements ((first word, second word), frequency)
        choices = [element for element in gram2 if element[0][0] == word]
        if not choices:
            break
        
        # Choose a pair with weighted probability from the choice list
        word = weighted_choice(choices)[1]


# In[12]:

for word in ['and', 'he', 'she', 'when', 'john', 'never', 'i', 'how']:
    print "Start word: %s" % word

    print "2-gram sentence: \"",
    get2GramSentenceRandom(word, 20)
    print "\""


# **Now that's way more interesting!** Those are starting to look like sentences!
# 
#     *Note* It's pretty interesting to see that for the sentence " when he believed him from the amiable but mrs hurst s being ill of being the discussion of course of ", we have hurst s, which we can tell came from Hurst's, an artifact of our stripping away all punctuation but keeping the s.
# 
# Let's try a longer sentence

# In[13]:

word = 'it'
print "Start word: %s" % word
print "2-gram sentence: \"",
get2GramSentenceRandom(word, 50)
print "\""


# Pretty cool, lets see what happens when we go to N-grams above 2.
# ## Tri-grams and more
# Okay, let's create a Ngram generator that can let us make ngrams of arbitrary sizes

# In[14]:

def generateNgram(n=1):
    gram = dict()
    
    # Some helpers to keep us crashing the PC for now
    assert n > 0 and n < 100
    
    # Populate N-gram dictionary
    for i in xrange(len(words)-(n-1)):
        key = tuple(words[i:i+n])
        if gram.has_key(key):
            gram[key] += 1
        else:
            gram[key] = 1

    # Turn into a list of (word, count) sorted by count from most to least
    gram = sorted(gram.items(), key=lambda (_, count): -count)
    return gram

trigram = generateNgram(3)
# Print top 20 most frequent ngrams
print trigram[:20]


# Cool! Okay, let's see a selection of sentences for N-grams with N = 2 to 10 and a few starting words!

# In[15]:

def getNGramSentenceRandom(gram, word, n = 50):
    for i in xrange(n):
        print word,
        # Get all possible elements ((first word, second word), frequency)
        choices = [element for element in gram if element[0][0] == word]
        if not choices:
            break
        
        # Choose a pair with weighted probability from the choice list
        word = weighted_choice(choices)[1]
for n in xrange(2,10):
    # Generate ngram list
    print
    print "Generating %d-gram list..." % n,
    ngram = generateNgram(n)
    print "Done"
    
    # Try out a bunch of sentences
    for word in ['and', 'he', 'she', 'when', 'john', 'never', 'i', 'how']:
        print "  %d-gram: \"" % n,
        getNGramSentenceRandom(ngram, word, 15)
        print "\""


# You can clearly see the sentences getting better and better with larger n-grams, this correlates to the ngram having more foresight into the sentence structure.

# In[16]:

# Generate 10gram list
print
print "Generating %d-gram list..." % n,
gram10 = generateNgram(10)
print "Done"


# Let's play with the 10gram and see what sort of sentence comes out.

# In[17]:

# Try out a bunch of sentences
for word in ['and', 'he', 'she', 'when', 'john', 'never', 'i', 'how']:
    print "  %d-gram: \"" % n,
    getNGramSentenceRandom(ngram, word, 100)
    print "\""


# Looks almost like normal sentences if you squint a little! Well, that was fun. Next up let's see some ways to improve upon this.
# 
# Instead of just taking the next word every time, we could take the next k words etc.
# 
# To be continue...

# In[18]:

# Generate 10gram list
n = 50
print
print "Generating %d-gram list..." % n,
gram30 = generateNgram(n)
print "Done"


# In[19]:

# Try out a bunch of sentences
for word in ['and', 'he', 'she', 'when', 'john', 'never', 'i', 'how']:
    print "  %d-gram: \"" % n,
    getNGramSentenceRandom(ngram, word, 20)
    print "\""

