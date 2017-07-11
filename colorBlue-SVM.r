# load the SVM library
library(e1071)

# load the file that contains all the colors collected with the "Do you know blue" campaign
isblue = read.csv("do_you_know_blue_4304colors.csv", header=TRUE,sep=",");
summary(isblue)

# define what are the input variables(r,g,b) and what is the output variable (isblue)
fol <- formula(isblue ~ r + g + b)
# train the SVM model, using all the data
modelsvm <- svm(fol, data=isblue)
modelsvm
# reported 765 support vectors used

# See how well this model predicts on the same data it was trained (calculating Ein)
predictions_svm <- predict(modelsvm, isblue, type="class")
matchessvm <- predictions_svm == isblue$isblue
sum(matchessvm)/nrow(isblue)
# reported around 0.948

# easier way to get the accuracy
mean(predictions_svm == isblue$isblue) 
# around 0.948


# now let's actually have training and testing sets to see what Eout we can get 
randomindexes <- sample(nrow(isblue), 0.9*nrow(isblue))
training <- isblue[randomindexes,]
testing <- isblue[-randomindexes,]
modelsvm_training <- svm(fol, data=training)
modelsvm_training
# reported 689 support vectors used

predictions_svm_testing <- predict(modelsvm_training, testing, type="class")
mean(predictions_svm_testing == testing$isblue)
# reported around 0.942 (for this single testing sample)


# Just out of curiosity, what does the testing sample return if we predict with the full model 
a = predict(modelsvm, testing, type="class")
mean(a == testing$isblue)
# reported around 0.9443, (for the same single testing sample)

# We can see the classification errors more precisely, we can print the "confusion matrix"
table(predictions_svm_testing, testing$isblue)

# We can also plot the svm classification. help(plot.svm)
# args: the model, the data, a formula giving just two parameters to plot (if the parameters are more than 2)
plot(modelsvm_training, training, b ~ g )


# We can also tune parametes (like the cost C, that determines how soft or hard is the boundary)
# this will run a cross-validation algorithm (default= 10-fold?)
tuned <- tune(svm, fol, data = training, ranges = list(cost=c(0.001, 0.01, 0.1, 1, 10, 100)))
# if we want to vary multiple parametes we just list them within list, separated with commas. 
# for example: list(epsilon=seq(0,1, 0.1), cost= 10^(-3:2))

# Summary will show the optimal cost parameter
summary(tuned)

svmfit <- svm(fol, data=training, cost=100)
svmfit
# reports 449 SV

prediction_tuned <- predict(svmfit, testing, type="class")
mean(predictions_svm_testing == testing$isblue)
# reports around 0.949

table(prediction_tuned, testing$isblue)


# Now let's look at the dataset collected from XKCD. It uses 27 different labels for the colors 
# (not just blue or not_blue as before), and it includes almost 200,000 colors!
colors = read.csv("XKCD_colors.csv", header=TRUE,sep=",");
summary(colors)

# check a sample of the colors
colors[10000:10010,]

# define the input and output variables
fol2 = formula(color ~ r + g + b)
modelcolor <- svm(fol2, data=colors) # Takes around 15 mins to run
modelcolor
# reported 30189 support vectors!

# We can now make predicitons, and the model will return a color value
predict(modelcolor, data.frame(r=1,g=2,b=10))       # returns black
predict(modelcolor, data.frame(r=1,g=200,b=10))     # returns green
predict(modelcolor, data.frame(r=200,g=200,b=10))   # returns yellow
predict(modelcolor, data.frame(r=0,g=0,b=50))       # returns dark blue
predict(modelcolor, data.frame(r=0,g=250,b=200))    # returns cyan
predict(modelcolor, data.frame(r=51,g=183,b=176))   # returns teal

# you can also pass it more colors in the data frame. Here we pass 3 colors 
 predict(modelcolor, data.frame(r=c(51,100,33),g=c(0,183,200),b=c(176,10,150))) # returns blue, green, teal

# predict the whole set of colors we have, to see what the Ein is
prediction_colors <- predict(modelcolor, colors) # takes 6 mins to run
mean(prediction_colors == colors$color)
# reports 0.975  pretty good!




