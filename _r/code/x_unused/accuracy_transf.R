options(max.print = 20000)
accuracy_transf_file = read.csv("/Users/Zbynda/Desktop/_0_SUMMER/R/data/accuracy_transf.csv",stringsAsFactors=FALSE)

# excludes color-deficient subject
accuracy_transf <- accuracy_transf_file[1:34,1:56]
accuracy_transf <- accuracy_transf[-c(33),]
#accuracy_transf # print
