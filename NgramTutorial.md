
# IPython Notebook - N-gram Tutorial

I've always wondered how chat bots like [Alice](http://alice.pandorabots.com/) work. Now, they are obviously much more complex than this tutorial will delve into, but we can touch on some of the core principles. One of them is this idea of understanding the relationships between words in sentences. How can we get a machine to understand these relationships?

Turns out there's the right way, and then there's the easy way. The right way involves delving deep into [semantic networks](https://en.wikipedia.org/wiki/Semantic_network) and ontologies, something I'd touched upon in my climate modelling days, but never mind that; We're doing **The Easy Way**.

### The Easy Way

Conversely, the easy way to learn the relationships is by throwing lots of data *en masse* at a machine, and letting it build up a model of the relationships (*this sounds suspiciously like Machine Learning*). 

An even simpler form of that is to track the number of words that are in sequence with one another, and keeping track of the frequency at which this occurs. We're actually starting to describe something that uses [N-grams](https://en.wikipedia.org/wiki/N-gram). An N-gram is a contiguous (*order matters*) sequence of items, which in this case is the words in text.

What we want to do is build up a dictionary of N-grams, which are pairs, triplets or more (*the N*) of words that pop up in the training data, with the value being the number of times they showed up. After we have this dictionary, as a naive example we could actually predict sentences by just randomly choosing words within this dictionary and doing a weighted random sample of the connected words that are part of n-grams within the keys.

Lets see how far we can get with N-grams without outside resources.

---

We have a text file for [Pride and Prejudice from Project Gutenberg](https://www.gutenberg.org/ebooks/1342) stored as `pg1342.txt` in the same folder as our notebook, but also available online directly. Let's load the text to a string since it's only 701KB, which will fit in memory nowadays. 

    *Note* : If we wanted to be more memory efficient we should parse the text file on a line or character by character basis, storing as needed, etc.


```python
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
```

    717575 , ﻿The Project Gutenberg EBook of Pride and Prejud ...
    

Great, now lets split into words into a big list, splitting on anything non-alphanumeric [A-Za-z0-9] (as well as punctuation) and forcing everything lowercase


```python
import re
words = re.split('[^A-Za-z]+', txt.lower())
words = filter(None, words) # Remove empty strings

# Print length of list
print len(words)


```

    125897
    

## Sets
From this we can now generate N-grams, lets start with a 1-gram, basically the set of all the words

    *Note* : One could use a dictionary instead of a set and keeping count of the occurances gives word frequency


```python
import sets

# Create set of all unique words, this throws away any information about frequency however
gram1 = set(words)

print len(gram1)

# Instead of printing all the elements in the set, create an iterator and print 20 elements only
gram1_iter = iter(gram1)
print [gram1_iter.next() for i in xrange(20)]
```

    6528
    ['foul', 'four', 'woods', 'hanging', 'woody', 'looking', 'eligible', 'scold', 'lord', 'meadows', 'sinking', 'leisurely', 'bringing', 'disturb', 'recollections', 'wednesday', 'piling', 'persisted', 'succession', 'tired']
    

Lets try and get the 2-gram now, which is pairs of words. Let's have a quick look to see the last 10 and how they look.


```python
# See the last 10 pairs
for i in xrange(len(words)-10, len(words)-1):
    print words[i], words[i+1]
```

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


```python
word_pairs = [(words[i], words[i+1]) for i in xrange(len(words)-1)]
print len(word_pairs)

gram2 = set(word_pairs)
print len(gram2)

# Print 20 elements from gram2
gram2_iter = iter(gram2)
print [gram2_iter.next() for i in xrange(20)]
```

    125896
    55636
    [('her', 'taste'), ('every', 'kind'), ('five', 'shillings'), ('soothed', 'but'), ('seemed', 'most'), ('fortune', 'it'), ('of', 'thanking'), ('near', 'she'), ('understand', 'from'), ('it', 'looks'), ('have', 'made'), ('lucas', 'he'), ('fail', 'him'), ('new', 'to'), ('nothing', 'but'), ('fearful', 'on'), ('to', 'wander'), ('write', 'rather'), ('of', 'studying'), ('interruption', 'from')]
    

## Frequency

Okay, that was fun, but this isn't enough, we need frequency if we want to have any sense of probabilities, which is what N-grams are about. Instead of using sets, lets create a dictionary with counts


```python
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
```

    [('the', 4507), ('to', 4243), ('of', 3730), ('and', 3658), ('her', 2225), ('i', 2070), ('a', 2012), ('in', 1937), ('was', 1847), ('she', 1710), ('that', 1594), ('it', 1550), ('not', 1450), ('you', 1428), ('he', 1339), ('his', 1271), ('be', 1260), ('as', 1192), ('had', 1177), ('with', 1100)]
    

For Pride and Prejudice, the words 'the', 'to', 'of', and 'and' were the top four most common words. Sounds about right, not too interesting yet, lets see what happens with 2-grams.


```python
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
```

    [(('of', 'the'), 491), (('to', 'be'), 445), (('in', 'the'), 397), (('i', 'am'), 303), (('mr', 'darcy'), 273), (('to', 'the'), 268), (('of', 'her'), 261), (('it', 'was'), 251), (('of', 'his'), 235), (('she', 'was'), 212), (('she', 'had'), 205), (('had', 'been'), 200), (('it', 'is'), 194), (('i', 'have'), 188), (('to', 'her'), 179), (('that', 'he'), 177), (('could', 'not'), 167), (('he', 'had'), 166), (('and', 'the'), 165), (('for', 'the'), 163)]
    

It looks like `"of the"` and `"to be"` are the top two most common 2-grams, sounds good. 

## Next word prediction
What can we do with this? Well lets see what happens if we take a random word from all the words, and build a sentence by just choosing the most common pair that has that word as it's start.


```python
start_word = words[len(words)/4]
print start_word
```

    enough
    

I just went ahead and chose the word that appears $1/4$ of the way into words, random enough.

Now in a loop, iterate through the frequency list (most frequent first) and see if it matches the first word in a pair, if so, the next word is the second element in the word pair, and continue with that word. Stop after N words or the list does not contain that word.

    *Note* : gram2 is a list that contains (key,value) where key is a word pair (first, second),
             so you need element[0][0] for first word and element [0][1] for second word


```python
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
```

    Start word: enough
    2-gram sentence: " enough to be so much as to be so much as to be so much as to be so much "
    

It gets stuck in a loop pretty much straight away. Not very interesting, try out other words and see what happens.


```python
for word in ['and', 'he', 'she', 'when', 'john', 'never', 'i', 'how']:
    print "Start word: %s" % word

    print "2-gram sentence: \"",
    get2GramSentence(word, 20)
    print "\""
```

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


```python
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
```


```python
for word in ['and', 'he', 'she', 'when', 'john', 'never', 'i', 'how']:
    print "Start word: %s" % word

    print "2-gram sentence: \"",
    get2GramSentenceRandom(word, 20)
    print "\""
```

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


```python
word = 'it'
print "Start word: %s" % word
print "2-gram sentence: \"",
get2GramSentenceRandom(word, 50)
print "\""
```

    Start word: it
    2-gram sentence: " it will think anything more disturbed more continued my fair to rosings and her power to her sister was beneath him colonel fitzwilliam i may assure you must be informed by such that betrayed him with the room was too ill opinion constitute my niece s steward and hatfield but "
    

Pretty cool, lets see what happens when we go to N-grams above 2.
## Tri-grams and more
Okay, let's create a Ngram generator that can let us make ngrams of arbitrary sizes


```python
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
```

    [(('i', 'do', 'not'), 62), (('i', 'am', 'sure'), 62), (('project', 'gutenberg', 'tm'), 57), (('as', 'soon', 'as'), 55), (('she', 'could', 'not'), 50), (('that', 'he', 'had'), 37), (('in', 'the', 'world'), 34), (('it', 'would', 'be'), 34), (('i', 'am', 'not'), 32), (('i', 'dare', 'say'), 31), (('the', 'project', 'gutenberg'), 31), (('could', 'not', 'be'), 30), (('it', 'was', 'not'), 30), (('that', 'he', 'was'), 29), (('mr', 'darcy', 's'), 29), (('that', 'it', 'was'), 28), (('on', 'the', 'subject'), 28), (('as', 'well', 'as'), 27), (('would', 'have', 'been'), 27), (('of', 'mr', 'darcy'), 27)]
    

Cool! Okay, let's see a selection of sentences for N-grams with N = 2 to 10 and a few starting words!


```python
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
```

    
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
      3-gram: " john with us on her absence may spend the few minutes in describing the servants "
      3-gram: " never entered into another minute description which i do for moments and dwelling on both "
      3-gram: " i took her sister chapter it will support and miserly father and she looked when "
      3-gram: " how he could be supposing such an expostulation with regard for her sister s will "
    
    Generating 4-gram list... Done
      4-gram: " and her anger soon as before and mentioned her brother gardiner thought she after laughing "
      4-gram: " he had not to us abominably ill qualified to you in this interesting mode to "
      4-gram: " she had a stroll in possession of him he said elizabeth it as for mr "
      4-gram: " when tea mr collins s coming into that is the country one hand that had "
      4-gram: " john told him as sincere but her face as to wish of in that is "
      4-gram: " never be the bingleys they suit perhaps i promised to hear darcy afterwards she for "
      4-gram: " i interrupt her answer asked herself as he may cough for about a little paler "
      4-gram: " how earnestly looking at his intrusion by thinking replied elizabeth was heard you are mistaken "
    
    Generating 5-gram list... Done
      5-gram: " and no intelligence it and kind attentions which comprehended that elizabeth s intentions did not "
      5-gram: " he had i should have a great many years my life was for since he "
      5-gram: " she finished the family without raising his real strong already self conceit and less his "
      5-gram: " when she chose it is attached to or forgetfulness they had no hint of one "
      5-gram: " john with an object there proved that i will visit had a weak understanding the "
      5-gram: " never get them threw a grievous affair as unaffected cordiality and to hear again his "
      5-gram: " i saw it was stationed herself with an invitation was dispatched and concluding that related "
      5-gram: " how differently did seem as good luck i must wait for her family said fitzwilliam "
    
    Generating 6-gram list... Done
      6-gram: " and they are certainly formed such realities as well as ever recede i am at "
      6-gram: " he becomes of light importance in general conversation though this useful to acquire about them "
      6-gram: " she proceeded in every other by whom they may have the same time of the "
      6-gram: " when the name had established all the house as her the attractions miss bennet and "
      6-gram: " john told her distress of all this must wait on what he could not able "
      6-gram: " never deserts him he replied you are undoubtedly by explaining the shocking he put on "
      6-gram: " i do not know elizabeth with him to be ashamed of this address while mr "
      6-gram: " how much more imprudent a little pressing and heard all the companion was prepared to "
    
    Generating 7-gram list... Done
      7-gram: " and the evening which she was convinced that you mention an affectionate friend from your "
      7-gram: " he was determined resolution of a solicitude or frightened at all night and to look "
      7-gram: " she was awkward she returned into one that their concerns of their mother insists upon "
      7-gram: " when looking as to the front a few minutes sooner but three days as much "
      7-gram: " john with both had never heard her residence in quest of her family was all "
      7-gram: " never been her duty of spirits were awakened as much at the conduct would not "
      7-gram: " i declare she had been hurt he knows him to say or violently set forth "
      7-gram: " how i dare say the others as she was now obtained private oh shocking to "
    
    Generating 8-gram list... Done
      8-gram: " and your letter was repeated the coffee and good humour was alone i did not "
      8-gram: " he had been overset already heard with lizzy had they insist on your will influence "
      8-gram: " she was again which miss bingley and economy in the more idea of surprise the "
      8-gram: " when we darcy s reserve and i told that she saw such pretension i feel "
      8-gram: " john told her mother in the terms and what would be materially concerned that he "
      8-gram: " never do not mean my power to understand the world i presume said jane bennet "
      8-gram: " i will be in hopes and well so they will ask too great humility mr "
      8-gram: " how grievous affair on finding herself she contented herself i have led me hear darcy "
    
    Generating 9-gram list... Done
      9-gram: " and i am afraid of introduction at the ball in front of everything he imagined "
      9-gram: " he was every cherished a point but when he deemed indispensably necessary on first week "
      9-gram: " she was in expecting my opinion and i imagine but it is of his enumeration "
      9-gram: " when it was not perhaps you have great favourite walk said he had heard chapter "
      9-gram: " john with admirable calmness he claimed towards one half the end on farther that man "
      9-gram: " never appeared again till they could not formed for mr darcy was thereby at jane "
      9-gram: " i am impatient to say nothing to desire of a liberal man upon herself and "
      9-gram: " how ardently did not account to play she could elizabeth found them word passed in "
    

You can clearly see the sentences getting better and better with larger n-grams, this correlates to the ngram having more foresight into the sentence structure.


```python
# Generate 10gram list
print
print "Generating %d-gram list..." % n,
gram10 = generateNgram(10)
print "Done"
```

    
    Generating 9-gram list... Done
    

Let's play with the 10gram and see what sort of sentence comes out.


```python
# Try out a bunch of sentences
for word in ['and', 'he', 'she', 'when', 'john', 'never', 'i', 'how']:
    print "  %d-gram: \"" % n,
    getNGramSentenceRandom(ngram, word, 100)
    print "\""
```

      9-gram: " and miss lydia s death her brother is gone on tuesday could not long upon others are a quarter of the project gutenberg tm works see how it that blame jane and with her to do not so sensibly and such of him but she who advanced but he repeated conversations occurring the house to longbourn produced the pleasure of all and she wrote as a little silly as if your head by themselves and elizabeth received some ladies in your daughter settled choice and assurances of i assure him or the favourite of the money younger sons cannot do "
      9-gram: " he then to present a neighbourhood for conversation and living might add a sunday and much conversation when he was highly either as often tried hard to express them he persisted in every member of behaviour in every evening for she was convinced on it was sent to be equally evident that you cannot be there was the following tuesday addressed to be in her and gratefully i was not receive a special licence you to cool i suppose and mortification she was most eligible but i have something or destroy all the effect on his county but at the "
      9-gram: " she turned over before we might ruin him abundantly increasing intimacy with elizabeth felt a great reader and his search which went to please i never even inferior to comprehend the room fatigued by starting the top of the longbourn everything declared he had no more for immediately running down sister s good society and elizabeth bennet i was in a situation and herself in five minutes at this said he went after her thoughts from such idle certainly did not appear prominently displaying or make her that he must feel he had very fond the netherfield and she had "
      9-gram: " when she has taken place with real cause of my fair as the time to enjoy himself it will then that it seems to exhibit mary said elizabeth construing all use of it thus began to the desperation of wickham i long enough of my dear friend jane this time of his duty to her with itself he owes his character but i shall send a day you sir william or implied doubt but before you have behaved in her going wherever you have been long to write for this cannot grow sufficiently amused than of my power by the "
      9-gram: " john told her answer asked her she sat with bitter complaints can captivate a long mrs bennet but if i believe him expose himself out with their wretchedness as is nothing to the idea of or to whom i am under such a history and lizzy shall spend a sheet of such a new clothes till i am very composedly lady catherine he began to plague her fears a watering place quite inattentive to do not see him often wished him charlotte said in walking several times a mile from netherfield last night tell you are such friends that they "
      9-gram: " never saw anything like his time this half an alacrity mr collins was the carriage by the carriage her the forsters ever to believe i am satisfied from all was listening to care and was not asking me hear of each of clothes but i shall take your head as affable to take his father was an explanation of him it was attended to take him from this question and dislike of having performed her address to be of hunsford she saw a few domestics and the subject and that to be a respectable and then though i assure the "
      9-gram: " i would make him instantly on the world how she began directly she became pale face and this work with active useful to dancing were seemed to make him in general assurances of seeing as she yes i am convinced of matrimony marriage would go she was to influence that whatever he asked him i thought more than pride he had any purpose to both replied let us abominably rude if your defect in a shorter space of marriage you showed me whilst you must go mr darcy was spent ten minutes he seldom went but did at least of "
      9-gram: " how really attached himself i laugh all their offenses of obtaining a moment and how he was particularly recollect what he walked quietly unmarked by no really believed that if you mean why should go into other objects as she could not much deference i cannot spare you your nephew are mistaken i happened but two of twenty such a good manners beyond youth as sharp as convinced of his glory and had she shook his misfortunes replied endeavouring to revive but the amusements of what she appeared to miss darcy does not been aware of my collection despite these "
    

Looks almost like normal sentences if you squint a little! Well, that was fun. Next up let's see some ways to improve upon this.

Instead of just taking the next word every time, we could take the next k words etc.

To be continue...


```python
# Generate 10gram list
n = 50
print
print "Generating %d-gram list..." % n,
gram30 = generateNgram(n)
print "Done"
```

    
    Generating 50-gram list... Done
    


```python
# Try out a bunch of sentences
for word in ['and', 'he', 'she', 'when', 'john', 'never', 'i', 'how']:
    print "  %d-gram: \"" % n,
    getNGramSentenceRandom(ngram, word, 20)
    print "\""
```

      50-gram: " and can assure you hold the most fortunately had not want of time all this young man s guidance of "
      50-gram: " he and with his affection with elizabeth you were the case is its environs to her rather affected with many "
      50-gram: " she had the sight of amends of repentance and with the shire was satisfied on mrs bennet to the servant "
      50-gram: " when you the two hours together over when they pursued the summer engagements which i will bestow and that in "
      50-gram: " john with her husband quite in the persons sit by discerning such a variety of your circumspection of her at "
      50-gram: " never distinguished no restrictions whatsoever you will do without paying elizabeth we must so little to wait even lydia gaped "
      50-gram: " i always struggled it did he must give in the matter to afford no more lanes hereabouts in edward street "
      50-gram: " how shall never pay a lady catherine seemed quite in hopes of all that she began directly towards a young "
    
