options(max.print = 20000)
times2 = read.csv("/Users/Zbynda/Desktop/_0_SUMMER/R/data/times2.csv",stringsAsFactors=FALSE)

times2 <- times2[1:34,]

# FORMATTING TIMES FOR ANOVA:

times2_aov <- data.frame("Subject"=character(576),"Density"=factor(c(1,2,3)),"Traffic"=factor(c(1,2,3)),"Viz"=factor(c(1,2)),"Time"=numeric(576),stringsAsFactors=FALSE)

rw_counter <- 1
for (rw in 3:nrow(times2)) {
  current_row <- times2[rw,]
  
  current_row_subject <- as.character(times2[rw,1])
  
  cl_counter <- 1
  for (cl in 2:ncol(times2)) {
    current_cl_density <- NA
    if (grepl("DE",names(times2[cl]))) current_cl_density <- 1
    if (grepl("ME",names(times2[cl]))) current_cl_density <- 2
    if (grepl("SP",names(times2[cl]))) current_cl_density <- 3
    
    current_cl_traffic <- NA
    if (grepl("HI",times2[1,cl])) current_cl_traffic <- 1
    if (grepl("ME",times2[1,cl])) current_cl_traffic <- 2
    if (grepl("LO",times2[1,cl])) current_cl_traffic <- 3
    
    current_cl_viz <- NA
    if (grepl("DI",times2[2,cl])) current_cl_viz <- 1
    if (grepl("GO",times2[2,cl])) current_cl_viz <- 2
    
    current_cl_time <- as.double(current_row[cl])
    
    current_index <- (rw_counter-1)*18 + cl_counter
    
    times2_aov$Subject[current_index] <- current_row_subject
    times2_aov$Density[current_index] <- current_cl_density
    times2_aov$Traffic[current_index] <- current_cl_traffic
    times2_aov$Viz[current_index] <- current_cl_viz
    times2_aov$Time[current_index] <- current_cl_time
    
    cl_counter <- cl_counter + 1
  }
  
  rw_counter <- rw_counter + 1
}

# ANOVA CALCULATION:

replications(Time ~ Density*Traffic*Viz, data=times2_aov)

times2_aov_out <- aov(Time ~ Density*Traffic*Viz, data=times2_aov)

times2_aov_table <- as.data.frame.list(summary(times2_aov_out))
summary(times2_aov_out)

# EFFECT SIZES:

times2_aov_table$Effect.Size <- c(numeric(7),NA)
for (rw in 1:nrow(times2_aov_table)-1) {
  times2_aov_table$Effect.Size[rw] <- (times2_aov_table$Sum.Sq[rw])/(times2_aov_table$Sum.Sq[rw]+times2_aov_table$Sum.Sq[nrow(times2_aov_table)])
}
times2_aov_table
