options(max.print = 20000)
questionnaire_norm_file = read.csv("/Users/Zbynda/Desktop/_0_SUMMER/R/data/questionnaire_norm.csv",stringsAsFactors=FALSE)

# excludes color-deficient subject
questionnaire_norm <- questionnaire_norm_file[2:35,1:17]
questionnaire_norm <- questionnaire_norm[-c(33),]
#questionnaire_norm # print
