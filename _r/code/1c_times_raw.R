options(max.print = 20000)
times_raw_file = read.csv("/Users/Zbynda/Desktop/_0_SUMMER/R/data/times_raw.csv",stringsAsFactors=FALSE)

# excludes color-deficient subject
times_raw <- times_raw_file[1:34,1:56]
times_raw <- times_raw[-c(33),]
#times_raw # print
