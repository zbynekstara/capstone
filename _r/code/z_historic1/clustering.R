# ACCURACY_RAW

options(max.print = 20000)
accuracy_raw = read.csv("/Users/Zbynda/Desktop/_0_SUMMER/R/data/accuracy_raw.csv",stringsAsFactors=FALSE)

head(accuracy_raw)
#ggplot(accuracy, aes(Petal.Length, Petal.Width, color=Species)) + geom_point()

set.seed(20)
accuracy_raw[1:32,2:55]
accuracyCluster <- kmeans(accuracy_raw[1:32,2:55], 5, nstart=20)
accuracyCluster
#table(irisCluster$cluster, iris$Species)

#accuracyCluster$cluster <- as.factor(accuracyCluster$cluster) # convert cluster name into factor
#ggplot(iris, aes(Petal.Length, Petal.Width, color=irisCluster$cluster)) + geom_point() # plot clustering data with cluster name as color

# QUESTIONNAIRE

#options(max.print = 20000)
#accuracy_raw = read.csv("/Users/Zbynda/Desktop/_0_SUMMER/R/data/accuracy_raw.csv",stringsAsFactors=FALSE)

#head(accuracy_raw)
#ggplot(accuracy, aes(Petal.Length, Petal.Width, color=Species)) + geom_point()

set.seed(20)
questionnaire[1:32,2:16]
questionnaireCluster <- kmeans(questionnaire[1:32,2:16], 5, nstart=20)
questionnaireCluster
#table(irisCluster$cluster, iris$Species)

#accuracyCluster$cluster <- as.factor(accuracyCluster$cluster) # convert cluster name into factor
#ggplot(iris, aes(Petal.Length, Petal.Width, color=irisCluster$cluster)) + geom_point() # plot clustering data with cluster name as color

# EXAMPLE

#head(iris) # show begining of iris dataset
#ggplot(iris, aes(Petal.Length, Petal.Width, color=Species)) + geom_point() # plot iris dataset with species as color
#
#set.seed(20)
#irisCluster <- kmeans(iris[,3:4], 3, nstart=20) # clustering for 3 groups
#irisCluster # show clustering result
#table(irisCluster$cluster, iris$Species) # compare clustering result with reality
#
#irisCluster$cluster <- as.factor(irisCluster$cluster) # convert cluster name into factor
#ggplot(iris, aes(Petal.Length, Petal.Width, color=irisCluster$cluster)) + geom_point() # plot clustering data with cluster name as color
