# ACCURACY TRANSF NORM

set.seed(20)
accuracy_transf_norm[1:32,2:55]
accuracy_transf_norm_cluster <- kmeans(accuracy_transf_norm[1:32,2:55], 2, nstart=20)
accuracy_transf_norm_cluster

accuracy_transf_norm_cluster_assignment <- accuracy_transf_norm[1:32,2:55]
accuracy_transf_norm_cluster_assignment$cluster <- accuracy_transf_norm_cluster$cluster
accuracy_transf_norm_cluster_assignment

# TIMES TRANSF NORM # maybe does not matter

set.seed(20)
times_transf_norm[1:32,2:55]
times_transf_norm_cluster <- kmeans(times_transf_norm[1:32,2:55], 2, nstart=20)
times_transf_norm_cluster

times_transf_norm_cluster_assignment <- times_transf_norm[1:32,2:55]
times_transf_norm_cluster_assignment$cluster <- times_transf_norm_cluster$cluster
times_transf_norm_cluster_assignment

# QUESTIONNAIRE NORM

set.seed(20)
questionnaire_norm[1:32,2:16]
questionnaire_norm_cluster <- kmeans(questionnaire_norm[1:32,2:16], 2, nstart=20)
questionnaire_norm_cluster

questionnaire_norm_cluster_assignment <- questionnaire_norm[1:32,2:16]
questionnaire_norm_cluster_assignment$cluster <- questionnaire_norm_cluster$cluster
questionnaire_norm_cluster_assignment

# TOGETHER

subject_clusters <- rbind(c(accuracy_transf_norm[1:32,1]),c(accuracy_transf_norm_cluster_assignment$cluster),c(times_transf_norm_cluster_assignment$cluster),c(questionnaire_norm_cluster_assignment$cluster))
subject_clusters

table(accuracy_transf_norm_cluster_assignment$cluster, questionnaire_norm_cluster_assignment$cluster)

cor.test(as.numeric(accuracy_transf_norm_cluster_assignment$cluster), as.numeric(times_transf_norm_cluster_assignment$cluster))
cor.test(as.numeric(accuracy_transf_norm_cluster_assignment$cluster), as.numeric(questionnaire_norm_cluster_assignment$cluster))
cor.test(as.numeric(times_transf_norm_cluster_assignment$cluster), as.numeric(questionnaire_norm_cluster_assignment$cluster))

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
