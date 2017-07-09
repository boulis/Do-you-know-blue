# Do-you-know-blue

In 2013, Dan Meyer, Dave Major, and Evan Weinberg created a [contest called "Do you know blue"](http://blog.mrmeyer.com/2013/contest-do-you-know-blue/). This was a math education effort for school students. It is also a great machine learning problem. It basically boils down to: Can you identify if a color is blue from its R, G, B values? You can also read the post from Evan [Students thinking like computer scientists](http://evanweinberg.com/2013/04/19/students-thinking-like-computer-scientists/) to get more info on the education aspect. 

I really liked the educational idea, and when I realised that this was a real machine learning problem (with a hidden larger set of data) I was thrilled. In 2013 I had finished the course [Learning from Data](https://work.caltech.edu/telecourse.html), an excellent machine learning cource that gave me solid foundations expecially on supervised learning and classification problems. A few months afterwards the contest was out and this was a nice way to hone my skills. 

I created a few scripts to test out different ideas. The first one was `colorBlue.py` where I was parsing a text file that included my training points and trying different machine learning techniques. The problem was that I did not have a lot of training data. I got the training points from the information the website provided (30 colours containing blue and not blue examples). If you reloaded the page, then a different set of colours was given, but there were many colours identical to past samples. At the end I got only 140 distinct colors to trian with. All the samples collected are in the file "color blue data". 

140 points for a training sample are not that many, so I went searching further. I tried parsing the data from the [xkcd study](http://blog.xkcd.com/2010/05/03/color-survey-results/). I was also introducing artificial points to move beyond the saturation faces of the rgb-space-cube. I learned more about RegEx doing so. But the results were not promising.

Then I discovered that the Do-you-know-blue website published all the colors that they had in their database as two images Blue-is Blue-is-not. Each image was a collection of tiles of individual colours.  I created another script (`colorBlue-all.py`), that used the PIL library and parsed the images given to obtain 4,304 colors! Linear regression seemed to perform well with different non linear (polynomial) transforms. A cubic transform reached the top of the standings page (this does not say much, as other people were probably using mostly heuristics, not machine learning) 

Initially I explicitly coded the rule for a specific non-linear polynomial transform of degree Q. But this was tedious and error prone (try writing a 4th degree polynomial transformation). One of the nice enhancements I did in the code was to create these transformations automatically. Here's what I did: I used the function `itertools.combinations_with_replacement` to get all the combination of `{r,g,b}` of certain size. I did this for all set sizes starting from size 1.  At the end I add '1' for the 0th size combination. Here's for example how I created the description of the rule as a string: 

```
descr = [reduce(lambda head, tail: head+'*'+tail, subset) for n in range(1, Q+1) for subset in itertools.combinations_with_replacement(['r','g','b'], n)]
descr.insert(0,'1') 
```
Notice how in list comprehension if you have 2 loops the outer loop goes first. Then each set/list we end up with (e.g., ['r','r','g','b'] is a one combination of size 4) gets processed by reduce with a simple lambda function to concatenate them to the string 'r*r*g*b'.

Now to actually transform the r,g,b points I had to take each point and apply the transform. Initially I was thinking of using combination of indexes to create the combinations of a point, but then it dawned on me to just take combinations on the point itself. Here's the reduce function also takes an initialization (3rd argument) so it can create an output even for the empty list. You notice that the n starts from 0 now, not from 1. 
 
``` 
Xnl = numpy.array([[reduce(lambda head, tail: head*tail, subset, 1) for n in range(Q+1) for subset in itertools.combinations_with_replacement(point, n)] for point in x])
```
Very happy with the results. You can run the script with -e flag to output the various rules (inequalities) to enter to the rule box of the website. 

### SVM

I also tried SVM in my python program. It did not perform well however (even with 4304 points), needing ~4290 support vectors. I found it hard to believe that this is really the case, but I did not investigate further. In 2017, I revisited the problem in R (see below) and I realised that I was using hard boundaries SVM (C=infty). This was trying to make the Ein = 0. Since I noticed that the database contains several erroneous entries (colors that are clearly not blue classified as blue, and vice versa) it is no surprise that the hard boundary resulted in so many support vectors. A soft boundary (as I did with R) produces much nicer results.



## Revisited in R

In July 2017, I revisited the problem in R. It was easy to deploy SVM classification in R. The more difficult part was getting the data in. I wrote another Python script (colorBlue-createCSV.py) to create csv files from the images and the xkcd text file I had. It was interesting to see that with SVM I could get around 0.949 accuracy.
