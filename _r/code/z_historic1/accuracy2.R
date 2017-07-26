options(max.print = 20000)
accuracy2 = read.csv("/Users/Zbynda/Desktop/_0_SUMMER/R/data/accuracy2.csv",stringsAsFactors=FALSE)

accuracy2 <- accuracy2[1:34,]

# FORMATTING ACCURACY FOR ANOVA:

accuracy2_aov <- data.frame("Subject"=character(576),"Density"=factor(c(1,2,3)),"Traffic"=factor(c(1,2,3)),"Viz"=factor(c(1,2)),"Accuracy"=numeric(576),stringsAsFactors=FALSE)

rw_counter <- 1
for (rw in 3:nrow(accuracy2)) {
  current_row <- accuracy2[rw,]
  
  current_row_subject <- as.character(accuracy2[rw,1])
  
  cl_counter <- 1
  for (cl in 2:ncol(accuracy2)) {
    current_cl_density <- NA
    if (grepl("DE",names(accuracy2)[cl])) current_cl_density <- 1
    if (grepl("ME",names(accuracy2)[cl])) current_cl_density <- 2
    if (grepl("SP",names(accuracy2)[cl])) current_cl_density <- 3
    
    current_cl_traffic <- NA
    if (grepl("HI",accuracy2[1,cl])) current_cl_traffic <- 1
    if (grepl("ME",accuracy2[1,cl])) current_cl_traffic <- 2
    if (grepl("LO",accuracy2[1,cl])) current_cl_traffic <- 3
    
    current_cl_viz <- NA
    if (grepl("DI",accuracy2[2,cl])) current_cl_viz <- 1
    if (grepl("GO",accuracy2[2,cl])) current_cl_viz <- 2
    
    current_cl_accuracy <- as.double(current_row[cl])

    current_index <- (rw_counter-1)*18 + cl_counter
    
    accuracy2_aov$Subject[current_index] <- current_row_subject
    accuracy2_aov$Density[current_index] <- current_cl_density
    accuracy2_aov$Traffic[current_index] <- current_cl_traffic
    accuracy2_aov$Viz[current_index] <- current_cl_viz
    accuracy2_aov$Accuracy[current_index] <- current_cl_accuracy
    
    cl_counter <- cl_counter + 1
  }
  
  rw_counter <- rw_counter + 1
}

# ANOVA CALCULATION:

replications(Accuracy ~ Density*Traffic*Viz, data=accuracy2_aov)

accuracy2_aov_out <- aov(Accuracy ~ Density*Traffic*Viz, data=accuracy2_aov)

accuracy2_aov_table <- as.data.frame.list(summary(accuracy2_aov_out))
summary(accuracy2_aov_out)

# EFFECT SIZES:

accuracy2_aov_table$Effect.Size <- c(numeric(7),NA)
for (rw in 1:nrow(accuracy2_aov_table)-1) {
  accuracy2_aov_table$Effect.Size[rw] <- (accuracy2_aov_table$Sum.Sq[rw])/(accuracy2_aov_table$Sum.Sq[rw]+accuracy2_aov_table$Sum.Sq[nrow(accuracy2_aov_table)])
}
accuracy2_aov_table

# POWER ANALYSIS:

# use g*power program instead!
