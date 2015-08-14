#!/bin/sh

ipython nbconvert --to html NgramTutorial.ipynb
ipython nbconvert --to markdown NgramTutorial.ipynb
ipython nbconvert --to python NgramTutorial.ipynb
