options(max.print = 20000)
long_answer = read.csv("/Users/Zbynda/Desktop/_0_SUMMER/R/data/long_answer.csv")

# subsets long answer questions to exclude color-deficient subject

long_answer <- long_answer[-c(1,34), ]
long_answer # print
