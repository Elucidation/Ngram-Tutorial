
# IPython Notebook - N-gram Tutorial

*By Sam Ansari - Aug 13, 2015*

First I'll see how far I can get with N-grams without outside resources

We have a text file for [Pride and Prejudice from Project Gutenberg](https://www.gutenberg.org/ebooks/1342) stored as `pg1342.txt` in the same folder as our notebook. Let's load the text to a string since it's only 701KB, which will fit in memory nowadays. 

    *Note* : If we wanted to be more memory efficient we should parse the text file and store per word, etc.


    with open('pg1342.txt', 'r') as f:
        txt = f.read()
    
    # See the number of characters and the first 50 characters to confirm it is there    
    print len(txt), ',', txt[:50] , '...'

    704149 , ﻿The Project Gutenberg EBook of Pride and Prejud ...
    

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
    2-gram sentence: " and almost have allowed her model of her letter and goodness oh cried elizabeth this event of several years of "
    Start word: he
    2-gram sentence: " he chiefly in oh lizzy continued i could he had been really amiable light as well and within her brother "
    Start word: she
    2-gram sentence: " she is very gentleness as well as usual with this agreement shall never more have long and though it not "
    Start word: when
    2-gram sentence: " when he was not justify the world who are very kind from something was bestowed on looking up the loss "
    Start word: john
    2-gram sentence: " john with cold was first stage of dignity with the letter was convinced from much in the ball at all "
    Start word: never
    2-gram sentence: " never let me jane to her going there but i do not to the most likely that whatever his reserve "
    Start word: i
    2-gram sentence: " i had one of self destined for you must feel the project gutenberg volunteers and of an unpleasant sort of "
    Start word: how
    2-gram sentence: " how many weeks and loving them though it is tolerably till the neighbourhood it to equal to elizabeth could not "
    

**Now that's way more interesting!** Those are starting to look like sentences!

    *Note* It's pretty interesting to see that for the sentence " when he believed him from the amiable but mrs hurst s being ill of being the discussion of course of ", we have hurst s, which we can tell came from Hurst's, an artifact of our stripping away all punctuation but keeping the s.

Let's try a longer sentence


    word = 'it'
    print "Start word: %s" % word
    print "2-gram sentence: \"",
    get2GramSentenceRandom(word, 50)
    print "\""

    Start word: it
    2-gram sentence: " it would be the netherfield for whatever might see mr and show off two years had at dinner was banished and by her inquiries about it was unluckily for my own fault with an unforgiving speech they proposed being married and address that mr denny himself on mr bennet s "
    

Pretty cool, lets see what happens when we go to N-grams above 2.
## Tri-grams and more
Okay, let's create a Ngram generator that can let us make ngrams of arbitrary sizes


    def generateNgram(n=1):
        gram = dict()
        
        # Some helpers to keep us crashing the PC for now
        assert n > 0 and n < 20
        
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
      2-gram: " and opening in such an occasion of a woman must be mr darcy by a "
      2-gram: " he was commissioning her exuberant spirits or next week she feels bingley was persuaded yourself "
      2-gram: " she were over the river in acceding to be obliged to the room no stay "
      2-gram: " when they had a table with louisa i was very confined for supposing his house "
      2-gram: " john with other causes must be secure let me he i am determined if i "
      2-gram: " never without anger could come mr darcy much satisfaction in the intelligence his inquiries after "
      2-gram: " i do me you believe him and though the evening brought a disadvantage in his "
      2-gram: " how many others then returned to know and bent on the address that you what "
    
    Generating 3-gram list... Done
      3-gram: " and indeed but i have mortified mine believe him to see jane what is strong "
      3-gram: " he chose to bear these two eldest daughter she could contain herself which his daughters "
      3-gram: " she said he had often that they who had hoped it may arise chiefly for "
      3-gram: " when you think she might be to welcome to be where where else elizabeth s "
      3-gram: " john told me in a man chapter elizabeth suspected enough for i wonder said she "
      3-gram: " never had been strange yes sir has been valued that he believed to step was "
      3-gram: " i feel how to pratt for preparing to read the praise is a sort of "
      3-gram: " how pleased to us i went on the table while these tastes had been able "
    
    Generating 4-gram list... Done
      4-gram: " and generous good enough to see the carriage was most creditable gentlemanlike man you give "
      4-gram: " he detained in he will believe not have been listened in your hearing this event "
      4-gram: " she told me for continuing their pleasantest preservative she finds miss bennet will make his "
      4-gram: " when mrs forster said miss bingley her affection sometimes one looked the morning mr wickham "
      4-gram: " john told he could think she really too much for it on he wishes and "
      4-gram: " never reach when persons whose mind and so steady candour is my daughters uncommonly fast "
      4-gram: " i shall try to be finer success he has very little delicate a beautiful creature "
      4-gram: " how mr bennet had been too full of his sisters may be urged the happy "
    
    Generating 5-gram list... Done
      5-gram: " and of her a few weeks with the son unless you have nothing but however "
      5-gram: " he now and herself said you never thought of associating with scarlet coat and trust "
      5-gram: " she said lately learned some who is so much as this room she soon forgotten "
      5-gram: " when you would have to their journey from the second time of all that she "
      5-gram: " john told her for my life could be hurt if you must not sixpence of "
      5-gram: " never see as to scotland but of my power and give you must have known "
      5-gram: " i do it is over he was all walking if my mother followed he means "
      5-gram: " how pleasant man quite comfortable on my youngest girl and are not till roused to "
    
    Generating 6-gram list... Done
      6-gram: " and anxiety she stared many pleasant nature shall not thank me less agreeable his coming "
      6-gram: " he offered to whom you will thank god s manners and to everybody was as "
      6-gram: " she would be secure and kitty fretfully when that is all the project gutenberg tm "
      6-gram: " when opposed their relationship to justify it is impossible not hear any rate there is "
      6-gram: " john with an hour s going that scenes but then owned that she spoke and "
      6-gram: " never been made himself in cried elizabeth was then shut the acutest kind as you "
      6-gram: " i am sure said elizabeth was sure they are not and charitable donations in love "
      6-gram: " how could not many circumstances of which nature had been at this desirable for you "
    
    Generating 7-gram list... Done
      7-gram: " and the offer of advantage spent by his having promised to anybody s home and "
      7-gram: " he had no answer and that all the end and where can know more cheerfully "
      7-gram: " she sent them there was uppermost in that horrid man on either but to make "
      7-gram: " when the best but though my aunt leaving wickham would have often disdained the sense "
      7-gram: " john told him in mirth for additional cost and i speak with her daughters i "
      7-gram: " never spoke to appear to give her turn her note aloud and such a period "
      7-gram: " i must abominate writing because you have both must go on this subject of it "
      7-gram: " how she will probably strike into her and was deserved but slightly surveying it is "
    
    Generating 8-gram list... Done
      8-gram: " and though she was instantly on her surprise of the idea of peculiar vexation she "
      8-gram: " he is that consoled her feel it taken leave to the advantage the survivor this "
      8-gram: " she came from the effect on the case the table in town myself but as "
      8-gram: " when sanctioned mr bingley and vexation to mrs bennet accepted but she had the gouldings "
      8-gram: " john told his ankle in the kindness madam he would not affect concern which he "
      8-gram: " never had mentioned earlier that if he had set forth into the mince pies for "
      8-gram: " i could marry without forming any stay at his mind every glance at all the "
      8-gram: " how very much of what to bring them and application was before they should be "
    
    Generating 9-gram list... Done
      9-gram: " and help feeling towards the village when they had not but to me mr bennet "
      9-gram: " he was the gentleman looking for i am sure she left the door jane in "
      9-gram: " she had better for the circumstances to my dear replied jane was scarcely an expostulation "
      9-gram: " when i must be long as marked her to eight o clock and from meryton "
      9-gram: " john with a proper place which we may depend on every wish of thought it "
      9-gram: " never heard mr darcy if you have actually persists in the course of fatigue and "
      9-gram: " i ever induce me so indulgent as the whole of happiness in her progress was "
      9-gram: " how very agreeable woman may elect to hear a relation lady catherine she ever since "
    

You can clearly see the sentences getting better and better with larger n-grams, this correlates to the ngram having more foresight into the sentence structure.


    # Generate 10gram list
    print
    print "Generating %d-gram list..." % n,
    gram10 = generateNgram(10)
    print "Done"

    
    Generating 9-gram list... Done
    

Let's play with the 10gram and see what sort of sentence comes out.


    # Try out a bunch of sentences
    for word in ['and', 'he', 'she', 'when', 'john', 'never', 'i', 'how']:
        print "  %d-gram: \"" % n,
        getNGramSentenceRandom(ngram, word, 100)
        print "\""

      9-gram: " and she said her manner of whose return and i am married before what we may take his wife conducted yourselves so well as much when i entered the same and making her mother as for being hereafter her repeatedly to mrs bennet one of enjoying herself since we know it they are not be killed and once gone jane nor faulty degree of gratitude by letting her heart you so dull as follows having passed she asked her plan could not lady lucas whom nobody in our friend denny denied knowing forgive me against herself she will die of "
      9-gram: " he supposed that colonel fitzwilliam s good brother is not be private care to ask when the morning within ten minutes before they knew myself sincerely i cannot always kept up any of her dear i dare say would not but could not till the matter cried when the country he had any such a family they had many pauses must have him before was meeting her daughters were directed her for he appeared again she could not plain chapter a intercourse a christian but haughty it when persons who does not have long he set amazed at table where "
      9-gram: " she grew on miss bennet accepted a girl it gratified by your porridge and entreating her to return the means unprotected or obtain a capital added what i am not suit as quietly answered in rejecting him with him and the hand with you could not imagine it became perfect composure when mrs bennet looking farther northwards than either or having received soon but i have got up everything right to be by a very sorry however mrs phillips first points she hardly hold her letters you will influence a letter and though in hunsford every moment upon me to "
      9-gram: " when she saw the lady was a project gutenberg tm trademark as good as may we had called economy was able to advantage of it is probably superior to me when the persuasion you are gratefully accepted the danger of a proper civilities bingley were standing and beg leave his kindness mr darcy thought only a very proud but this work of a letter was a little of his return mr darcy who seems he was on the hermitage elizabeth entered the regulars and his sisters to consider poetry as any place that my dressing gown before and miss bingley "
      9-gram: " john with some prettier girls walked about it was distressed but at all that bingley with lizzy said they never yet for a little compassion to prove had ever the more contracted into the bride as they had most improbable event of the greatest satisfaction of all but without ceremony was rather a lively tone which she might expect such confusion said fitzwilliam without knowing that it may lead me to elizabeth when in company for i never to all others were going to make the honour of that he was not altered what is improved and mrs bennet scarcely "
      9-gram: " never seen miss bingley standing on her situation remained therefore soon as before she affectionately taking you again the other warranties of not expect jane constantly so i am not help giving her ease with mutual desire of i had been was alone after an earnest i cannot fix on the point out as much grown girl but as soon satisfied and praise on meeting both sat with whom he i speak with no such behaviour equally ill opinion in elizabeth was forced to stay at rosings in without seeming really believe a companion added she began scolding her through "
      9-gram: " i had such a wish to visit them with him accidentally in which shortly have been considered it is desired effect of their acquaintance still increasing and conciliatory manners and i know not afraid her heart you mean as to the motion of lydia what i must feel something of superior execution he was as well as he should stand by undervaluing their favourable than hurrying instantly understood that led by his dependence when they were to whom he dines here this for incivility though it will be as the united to write very respectable pleasures and elizabeth could call "
      9-gram: " how shall be so soon as warmly but no connections their share of general habits that his gig and when their former my affection to eight o clock in which brought only to set off and pride he had resolved to attribute to be aware that i shall though she did mr bennet have a part i cannot last how sincerely i must require and was attentive to do not her anxious circumspection of her how could have been designed for him my aunt promised letter i believe me so imprudence forgotten there are not receiving so mildly to have "
    

Looks almost like normal sentences if you squint a little! Well, that was fun. Next up let's see some ways to improve upon this.

Instead of just taking the next word every time, we could take the next k words etc.

To be continue...


    
