# ACCURACY RAW

set.seed(20)
accuracy_raw[1:32,2:55]
accuracy_raw_cluster <- kmeans(accuracy_raw[1:32,2:55], 4, nstart=20)
accuracy_raw_cluster

accuracy_raw_cluster_assignment <- accuracy_raw[1:32,2:55]
accuracy_raw_cluster_assignment$cluster <- accuracy_raw_cluster$cluster
accuracy_raw_cluster_assignment

# TIMES RAW # maybe does not matter

set.seed(20)
times_raw[1:32,2:55]
times_raw_cluster <- kmeans(times_raw[1:32,2:55], 2, nstart=20)
times_raw_cluster

times_raw_cluster_assignment <- times_raw[1:32,2:55]
times_raw_cluster_assignment$cluster <- times_raw_cluster$cluster
times_raw_cluster_assignment

# QUESTIONNAIRE RAW

set.seed(20)
questionnaire_raw[1:32,2:16]
questionnaire_raw_cluster <- kmeans(questionnaire_raw[1:32,2:16], 2, nstart=20)
questionnaire_raw_cluster

questionnaire_raw_cluster_assignment <- questionnaire_raw[1:32,2:16]
questionnaire_raw_cluster_assignment$cluster <- questionnaire_raw_cluster$cluster
questionnaire_raw_cluster_assignment

# TOGETHER

subject_clusters <- rbind(c(accuracy_raw[1:32,1]),c(accuracy_raw_cluster_assignment$cluster),c(times_raw_cluster_assignment$cluster),c(questionnaire_raw_cluster_assignment$cluster))
subject_clusters

table(accuracy_raw_cluster_assignment$cluster, questionnaire_raw_cluster_assignment$cluster)

cor.test(as.numeric(accuracy_raw_cluster_assignment$cluster), as.numeric(times_raw_cluster_assignment$cluster))
cor.test(as.numeric(accuracy_raw_cluster_assignment$cluster), as.numeric(questionnaire_raw_cluster_assignment$cluster))
cor.test(as.numeric(times_raw_cluster_assignment$cluster), as.numeric(questionnaire_raw_cluster_assignment$cluster))

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
