# Ngram-Tutorial
Building a basic N-gram generator and predictive sentence generator from scratch using IPython Notebook.

I've always wondered how chat bots like [Alice](http://alice.pandorabots.com/) work. Now, they are obviously much more complex than this tutorial will delve into, but we can touch on some of the core principles. One of them is this idea of understanding the relationships between words in sentences. How can we get a machine to understand these relationships?

Turns out there's the right way, and then there's the easy way. The right way involves delving deep into [semantic networks](https://en.wikipedia.org/wiki/Semantic_network) and ontologies, something I'd touched upon in my climate modelling days, but never mind that; We're doing **The Easy Way**.

The easy way to learn the relationships is by throwing lots of data en masse at a machine, and letting it build up a model of the relationships (this sounds suspiciously like Machine Learning).

An even simpler form of that is to track the number of words that are in sequence with one another, and keeping track of the frequency at which this occurs. We're actually starting to describe something that uses [N-grams](https://en.wikipedia.org/wiki/N-gram). An N-gram is a contiguous (*order matters*) sequence of items, which in this case is the words in text.

What we want to do is build up a dictionary of N-grams, which are pairs, triplets or more (the N) of words that pop up in the training data, with the value being the number of times they showed up. After we have this dictionary, as a naive example we could actually predict sentences by just randomly choosing words within this dictionary and doing a weighted random sample of the connected words that are part of n-grams within the keys.

This notebook is a simple tutorial on seeing how far we can get building an N-gram model without looking at outside resources.

# Viewing
**See the notebook [here](elucidation.github.io/Ngram-Tutorial)**

Or on GitHub: [`NgramTutorial.ipynb`](https://github.com/Elucidation/Ngram-Tutorial/blob/master/NgramTutorial.ipynb).

# Running live
Install [IPython Notebook](https://ipython.org/ipython-doc/3/notebook/index.html). It may be as simple as `pip install "ipython[notebook]"`

Clone or download a zip of this repo to a known location.

Then start your server with `ipython notebook`, navigate to the folder and open the notebook.
