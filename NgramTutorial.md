
# IPython Notebook - N-gram Tutorial

*By Sam Ansari - Aug 13, 2015*

First I'll see how far I can get with N-grams without outside resources

We have a text file for [Pride and Prejudice from Project Gutenberg](https://www.gutenberg.org/ebooks/1342) stored as `pg1342.txt` in the same folder as our notebook. Let's load the text to a string since it's only 701KB, which will fit in memory nowadays. 

    *Note* : If we wanted to be more memory efficient we should parse the text file and store per word, etc.


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

    717575 , ﻿The Project Gutenberg EBook of Pride and Prejud ...
    

Great, now lets split into words into a big list, splitting on anything non-alphanumeric [A-Za-z0-9] (as well as punctuation) and forcing everything lowercase


    import re
    words = re.split('[^A-Za-z]+', txt.lower())
    words = filter(None, words) # Remove empty strings
    
    # Print length of list
    print len(words)
    
    

    125897
    

## Sets
From this we can now generate N-grams, lets start with a 1-gram, basically the set of all the words

    *Note* : One could use a dictionary instead of a set and keeping count of the occurances gives word frequency


    import sets
    
    # Create set of all unique words, this throws away any information about frequency however
    gram1 = set(words)
    
    print len(gram1)
    
    # Instead of printing all the elements in the set, create an iterator and print 20 elements only
    gram1_iter = iter(gram1)
    print [gram1_iter.next() for i in xrange(20)]

    6528
    ['foul', 'four', 'woods', 'hanging', 'woody', 'looking', 'eligible', 'scold', 'lord', 'meadows', 'sinking', 'leisurely', 'bringing', 'disturb', 'recollections', 'wednesday', 'piling', 'persisted', 'succession', 'tired']
    

Lets try and get the 2-gram now, which is pairs of words. Let's have a quick look to see the last 10 and how they look.


    # See the last 10 pairs
    for i in xrange(len(words)-10, len(words)-1):
        print words[i], words[i+1]

    subscribe to
    to our
    our email
    email newsletter
    newsletter to
    to hear
    hear about
    about new
    new ebooks
    

Okay, seems good, lets get all word pairs, and then generate a set of unique pairs from it


    word_pairs = [(words[i], words[i+1]) for i in xrange(len(words)-1)]
    print len(word_pairs)
    
    gram2 = set(word_pairs)
    print len(gram2)
    
    # Print 20 elements from gram2
    gram2_iter = iter(gram2)
    print [gram2_iter.next() for i in xrange(20)]

    125896
    55636
    [('her', 'taste'), ('every', 'kind'), ('five', 'shillings'), ('soothed', 'but'), ('seemed', 'most'), ('fortune', 'it'), ('of', 'thanking'), ('near', 'she'), ('understand', 'from'), ('it', 'looks'), ('have', 'made'), ('lucas', 'he'), ('fail', 'him'), ('new', 'to'), ('nothing', 'but'), ('fearful', 'on'), ('to', 'wander'), ('write', 'rather'), ('of', 'studying'), ('interruption', 'from')]
    

## Frequency

Okay, that was fun, but this isn't enough, we need frequency if we want to have any sense of probabilities, which is what N-grams are about. Instead of using sets, lets create a dictionary with counts


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

    [('the', 4507), ('to', 4243), ('of', 3730), ('and', 3658), ('her', 2225), ('i', 2070), ('a', 2012), ('in', 1937), ('was', 1847), ('she', 1710), ('that', 1594), ('it', 1550), ('not', 1450), ('you', 1428), ('he', 1339), ('his', 1271), ('be', 1260), ('as', 1192), ('had', 1177), ('with', 1100)]
    

For Pride and Prejudice, the words 'the', 'to', 'of', and 'and' were the top four most common words. Sounds about right, not too interesting yet, lets see what happens with 2-grams.


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

    [(('of', 'the'), 491), (('to', 'be'), 445), (('in', 'the'), 397), (('i', 'am'), 303), (('mr', 'darcy'), 273), (('to', 'the'), 268), (('of', 'her'), 261), (('it', 'was'), 251), (('of', 'his'), 235), (('she', 'was'), 212), (('she', 'had'), 205), (('had', 'been'), 200), (('it', 'is'), 194), (('i', 'have'), 188), (('to', 'her'), 179), (('that', 'he'), 177), (('could', 'not'), 167), (('he', 'had'), 166), (('and', 'the'), 165), (('for', 'the'), 163)]
    

It looks like `"of the"` and `"to be"` are the top two most common 2-grams, sounds good. 

## Next word prediction
What can we do with this? Well lets see what happens if we take a random word from all the words, and build a sentence by just choosing the most common pair that has that word as it's start.


    start_word = words[len(words)/4]
    print start_word

    enough
    

I just went ahead and chose the word that appears $1/4$ of the way into words, random enough.

Now in a loop, iterate through the frequency list (most frequent first) and see if it matches the first word in a pair, if so, the next word is the second element in the word pair, and continue with that word. Stop after N words or the list does not contain that word.

    *Note* : gram2 is a list that contains (key,value) where key is a word pair (first, second),
             so you need element[0][0] for first word and element [0][1] for second word


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

    Start word: enough
    2-gram sentence: " enough to be so much as to be so much as to be so much as to be so much "
    

It gets stuck in a loop pretty much straight away. Not very interesting, try out other words and see what happens.


    for word in ['and', 'he', 'she', 'when', 'john', 'never', 'i', 'how']:
        print "Start word: %s" % word
    
        print "2-gram sentence: \"",
        get2GramSentence(word, 20)
        print "\""

    Start word: and
    2-gram sentence: " and the whole of the whole of the whole of the whole of the whole of the whole of the "
    Start word: he
    2-gram sentence: " he had been so much as to be so much as to be so much as to be so much "
    Start word: she
    2-gram sentence: " she was not be so much as to be so much as to be so much as to be so "
    Start word: when
    2-gram sentence: " when she was not be so much as to be so much as to be so much as to be "
    Start word: john
    2-gram sentence: " john with the whole of the whole of the whole of the whole of the whole of the whole of "
    Start word: never
    2-gram sentence: " never be so much as to be so much as to be so much as to be so much as "
    Start word: i
    2-gram sentence: " i am sure i am sure i am sure i am sure i am sure i am sure i am "
    Start word: how
    2-gram sentence: " how much as to be so much as to be so much as to be so much as to be "
    

## Weighted random choice based on frequency
Same thing. Okay, lets randomly choose from the subset of all 2grams that matches the first word, using a weighted-probability based on counts.


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


    for word in ['and', 'he', 'she', 'when', 'john', 'never', 'i', 'how']:
        print "Start word: %s" % word
    
        print "2-gram sentence: \"",
        get2GramSentenceRandom(word, 20)
        print "\""

    Start word: and
    2-gram sentence: " and how he probably more easily believe me i never see how much as that he and pride and unshackled "
    Start word: he
    2-gram sentence: " he proceeded to be impossible chapter more than to do anything elizabeth implacable resentment gave it really believe very rational "
    Start word: she
    2-gram sentence: " she spoke of distinguished trait of him she regarded her earnestly entreated permission if she had given him in this "
    Start word: when
    2-gram sentence: " when there subsisted between the possibility of everything was superseded by a great spirits are cried mr bingley looked and "
    Start word: john
    2-gram sentence: " john told what sort of her and any of companions that whenever they came to conciliate her agitation of wine "
    Start word: never
    2-gram sentence: " never knew that regardless of his character i think you think what had before jane the same intelligible gallantry and "
    Start word: i
    2-gram sentence: " i can have somebody who met and had not been doing very genteel agreeable but my dear said lately made "
    Start word: how
    2-gram sentence: " how her being coherent dearest sister to be happy for the mortification mr bennet that everyone connected with which could "
    

**Now that's way more interesting!** Those are starting to look like sentences!

    *Note* It's pretty interesting to see that for the sentence " when he believed him from the amiable but mrs hurst s being ill of being the discussion of course of ", we have hurst s, which we can tell came from Hurst's, an artifact of our stripping away all punctuation but keeping the s.

Let's try a longer sentence


    word = 'it'
    print "Start word: %s" % word
    print "2-gram sentence: \"",
    get2GramSentenceRandom(word, 50)
    print "\""

    Start word: it
    2-gram sentence: " it will think anything more disturbed more continued my fair to rosings and her power to her sister was beneath him colonel fitzwilliam i may assure you must be informed by such that betrayed him with the room was too ill opinion constitute my niece s steward and hatfield but "
    

Pretty cool, lets see what happens when we go to N-grams above 2.
## Tri-grams and more
Okay, let's create a Ngram generator that can let us make ngrams of arbitrary sizes


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

    [(('i', 'do', 'not'), 62), (('i', 'am', 'sure'), 62), (('project', 'gutenberg', 'tm'), 57), (('as', 'soon', 'as'), 55), (('she', 'could', 'not'), 50), (('that', 'he', 'had'), 37), (('in', 'the', 'world'), 34), (('it', 'would', 'be'), 34), (('i', 'am', 'not'), 32), (('i', 'dare', 'say'), 31), (('the', 'project', 'gutenberg'), 31), (('could', 'not', 'be'), 30), (('it', 'was', 'not'), 30), (('that', 'he', 'was'), 29), (('mr', 'darcy', 's'), 29), (('that', 'it', 'was'), 28), (('on', 'the', 'subject'), 28), (('as', 'well', 'as'), 27), (('would', 'have', 'been'), 27), (('of', 'mr', 'darcy'), 27)]
    

Cool! Okay, let's see a selection of sentences for N-grams with N = 2 to 10 and a few starting words!


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

    
    Generating 2-gram list... Done
      2-gram: " and i am poor eliza bennet to herself and twenty such a second song said "
      2-gram: " he as handsome as soon marry for us hear of it the confinement of his "
      2-gram: " she comes my object has received at them might be quick parts of writing to "
      2-gram: " when elizabeth that pure and with propriety not help seeing that he but it grew "
      2-gram: " john told that must leave than by a solicitude on jane as to dispose of "
      2-gram: " never saw him to the case you would tell my consent to conceal it had "
      2-gram: " i found that when your manners now and she endeavoured in whose northern tour of "
      2-gram: " how heartily did at last finish his family they could not give greater beauty i "
    
    Generating 3-gram list... Done
      3-gram: " and with money what i was now i was finally settled family knew that resignation "
      3-gram: " he began an air which mrs hurst and precipitate closure with her with all that "
      3-gram: " she is the works if i should not the greatest part of her more than "
      3-gram: " when in leaving her ladyship last week at your kindness to wish i certainly to "
      3-gram: " john with us on her absence may spend the few minutes in 

You can clearly see the sentences getting better and better with larger n-grams, this correlates to the ngram having more foresight into the sentence structure.


    # Generate 10gram list
    print
    print "Generating %d-gram list..." % n,
    gram10 = generateNgram(10)
    print "Done"

Let's play with the 10gram and see what sort of sentence comes out.


    # Try out a bunch of sentences
    for word in ['and', 'he', 'she', 'when', 'john', 'never', 'i', 'how']:
        print "  %d-gram: \"" % n,
        getNGramSentenceRandom(ngram, word, 100)
        print "\""

Looks almost like normal sentences if you squint a little! Well, that was fun. Next up let's see some ways to improve upon this.

Instead of just taking the next word every time, we could take the next k words etc.

To be continue...


    # Generate 10gram list
    n = 50
    print
    print "Generating %d-gram list..." % n,
    gram30 = generateNgram(n)
    print "Done"


    # Try out a bunch of sentences
    for word in ['and', 'he', 'she', 'when', 'john', 'never', 'i', 'how']:
        print "  %d-gram: \"" % n,
        getNGramSentenceRandom(ngram, word, 20)
        print "\""


    
