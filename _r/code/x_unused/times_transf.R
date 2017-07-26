options(max.print = 20000)
times_transf_file = read.csv("/Users/Zbynda/Desktop/_0_SUMMER/R/data/times_transf.csv",stringsAsFactors=FALSE)

# excludes color-deficient subject
times_transf <- times_transf_file[1:34,1:56]
times_transf <- times_transf[-c(33),]
#times_transf # print
