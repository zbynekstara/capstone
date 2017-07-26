options(max.print = 20000)
questionnaire_raw_file = read.csv("/Users/Zbynda/Desktop/_0_SUMMER/R/data/questionnaire_raw.csv",stringsAsFactors=FALSE)

# excludes color-deficient subject
questionnaire_raw <- questionnaire_raw_file[2:35,1:16]
questionnaire_raw <- questionnaire_raw[-c(33),]
#questionnaire_raw # print
