options(max.print = 20000)
accuracy_transf_norm_file = read.csv("/Users/Zbynda/Desktop/_0_SUMMER/R/data/accuracy_transf_norm.csv",stringsAsFactors=FALSE)

# excludes color-deficient subject
accuracy_transf_norm <- accuracy_transf_norm_file[1:34,1:56]
accuracy_transf_norm <- accuracy_transf_norm[-c(33),]
#accuracy_transf_norm # print

# FORMATTING ACCURACY FOR ANOVA:

accuracy_transf_norm_aov_ready <- accuracy_transf_norm[1:32,1:55]

accuracy_transf_norm_aov_format <- data.frame("Subject"=character(1728),"Path"=factor(c(1,2,3)),"Density"=factor(c(1,2,3)),"Traffic"=factor(c(1,2,3)),"Viz"=factor(c(1,2)),"Accuracy"=numeric(1728),stringsAsFactors=FALSE)

rw_counter <- 1
for (rw in 1:nrow(accuracy_transf_norm_aov_ready)) {
  current_row <- accuracy_transf_norm_aov_ready[rw,]

  current_row_subject <- as.character(accuracy_transf_norm_aov_ready[rw,1])

  cl_counter <- 1
  for (cl in 2:ncol(accuracy_transf_norm_aov_ready)) {
    current_cl_name <- strsplit(names(accuracy_transf_norm_aov_ready)[cl],"\\.")[[1]]

    current_cl_path <- NA
    if (grepl("P1",current_cl_name[1])) current_cl_path <- 1
    if (grepl("P2",current_cl_name[1])) current_cl_path <- 2
    if (grepl("P3",current_cl_name[1])) current_cl_path <- 3

    current_cl_density <- NA
    if (grepl("DE",current_cl_name[2])) current_cl_density <- 1
    if (grepl("ME",current_cl_name[2])) current_cl_density <- 2
    if (grepl("SP",current_cl_name[2])) current_cl_density <- 3

    current_cl_traffic <- NA
    if (grepl("HI",current_cl_name[3])) current_cl_traffic <- 1
    if (grepl("ME",current_cl_name[3])) current_cl_traffic <- 2
    if (grepl("LO",current_cl_name[3])) current_cl_traffic <- 3

    current_cl_viz <- NA
    if (grepl("DI",current_cl_name[4])) current_cl_viz <- 1
    if (grepl("GO",current_cl_name[4])) current_cl_viz <- 2

    current_cl_accuracy <- as.double(current_row[cl])

    current_index <- (rw_counter-1)*54 + cl_counter
    
    accuracy_transf_norm_aov_format$Subject[current_index] <- current_row_subject
    accuracy_transf_norm_aov_format$Path[current_index] <- current_cl_path
    accuracy_transf_norm_aov_format$Density[current_index] <- current_cl_density
    accuracy_transf_norm_aov_format$Traffic[current_index] <- current_cl_traffic
    accuracy_transf_norm_aov_format$Viz[current_index] <- current_cl_viz
    accuracy_transf_norm_aov_format$Accuracy[current_index] <- current_cl_accuracy
    
    cl_counter <- cl_counter + 1
  }
  
  rw_counter <- rw_counter + 1
}

# ANOVA CALCULATION:

replications(Accuracy ~ Density*Traffic*Viz, data=accuracy_transf_norm_aov_format)

accuracy_transf_norm_aov <- aov(Accuracy ~ Density*Traffic*Viz, data=accuracy_transf_norm_aov_format)
summary(accuracy_transf_norm_aov)

accuracy_transf_norm_aov_table <- as.data.frame.list(summary(accuracy_transf_norm_aov))

# EFFECT SIZES:

accuracy_transf_norm_aov_table$Effect.Size <- c(numeric(7),NA)
for (rw in 1:nrow(accuracy_transf_norm_aov_table)-1) {
  accuracy_transf_norm_aov_table$Effect.Size[rw] <- (accuracy_transf_norm_aov_table$Sum.Sq[rw])/(accuracy_transf_norm_aov_table$Sum.Sq[rw]+accuracy_transf_norm_aov_table$Sum.Sq[nrow(accuracy_transf_norm_aov_table)])
}
accuracy_transf_norm_aov_table

# POWER ANALYSIS:

# use g*power program instead!
