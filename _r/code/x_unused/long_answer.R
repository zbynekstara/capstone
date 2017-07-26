options(max.print = 20000)
long_answer_file = read.csv("/Users/Zbynda/Desktop/_0_SUMMER/R/data/long_answer.csv",stringsAsFactors=FALSE)

# excludes color-deficient subject
long_answer <- long_answer_file[2:34,1:3]
long_answer <- long_answer[-c(34),]
#long_answer # print
