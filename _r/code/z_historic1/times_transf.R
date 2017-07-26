options(max.print = 20000)
times = read.csv("/Users/Zbynda/Desktop/_0_SUMMER/R/data/times_transf.csv",stringsAsFactors=FALSE)

# subsets times to exclude color-deficient subject
times <- times[2:33,1:55]
#times # print

# FORMATTING TIMES FOR ANOVA:

times_aov <- data.frame("Subject"=character(1728),"Path"=factor(c(1,2,3)),"Density"=factor(c(1,2,3)),"Traffic"=factor(c(1,2,3)),"Viz"=factor(c(1,2)),"Time"=numeric(1728),stringsAsFactors=FALSE)

rw_counter <- 1
for (rw in 1:nrow(times)) {
  current_row <- times[rw,]
  
  current_row_subject <- as.character(times[rw,1])
  
  cl_counter <- 1
  for (cl in 2:ncol(times)) {
    current_cl_name <- strsplit(names(times)[cl],"\\.")[[1]]
    
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
    
    current_cl_time <- as.double(current_row[cl])
    
    current_index <- (rw_counter-1)*54 + cl_counter
    
    times_aov$Subject[current_index] <- current_row_subject
    times_aov$Path[current_index] <- current_cl_path
    times_aov$Density[current_index] <- current_cl_density
    times_aov$Traffic[current_index] <- current_cl_traffic
    times_aov$Viz[current_index] <- current_cl_viz
    times_aov$Time[current_index] <- current_cl_time
    
    cl_counter <- cl_counter + 1
  }
  
  rw_counter <- rw_counter + 1
}

# ANOVA CALCULATION:

replications(Time ~ Density*Traffic*Viz, data=times_aov)

times_aov_out <- aov(Time ~ Density*Traffic*Viz, data=times_aov)

times_aov_table <- as.data.frame.list(summary(times_aov_out))
summary(times_aov_out)

# EFFECT SIZES:

times_aov_table$Effect.Size <- c(numeric(7),NA)
for (rw in 1:nrow(times_aov_table)-1) {
  times_aov_table$Effect.Size[rw] <- (times_aov_table$Sum.Sq[rw])/(times_aov_table$Sum.Sq[rw]+times_aov_table$Sum.Sq[nrow(times_aov_table)])
}
times_aov_table

# POWER ANALYSIS:

# use g*power program instead!