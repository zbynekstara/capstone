options(max.print = 20000)
accuracy_raw_file = read.csv("/Users/Zbynda/Desktop/_0_SUMMER/R/data/accuracy_raw.csv",stringsAsFactors=FALSE)

#optimal_time <- accuracy[c(34),] # subset accuracy to keep the optimal traversal times row
#optimal_time # print

# excludes color-deficient subject
accuracy_raw <- accuracy_raw_file[1:34,1:56]
accuracy_raw <- accuracy_raw[-c(33),]
#accuracy_raw # print
