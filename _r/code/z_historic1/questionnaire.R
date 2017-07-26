options(max.print = 20000)
questionnaire = read.csv("/Users/Zbynda/Desktop/_0_SUMMER/R/data/questionnaire.csv")

# subsets questionnaire to exclude color-deficient subject

questionnaire <- questionnaire[-c(1,34), ]
questionnaire # print
