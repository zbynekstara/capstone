shapiro.test(accuracy_raw$subject.mean[1:32])
#shapiro.test(accuracy_transf$subject.mean[1:32])
shapiro.test(accuracy_transf_norm$subject.mean[1:32])

shapiro.test(times_raw$subject.mean[1:32])
#shapiro.test(times_transf$subject.mean[1:32])
shapiro.test(times_transf_norm$subject.mean[1:32])

# no questionnaire raw subject means
# no questionnaire transf
shapiro.test(questionnaire_norm$subject.mean[1:32])

library("ggpubr")
ggqqplot(accuracy_raw$subject.mean[1:32])
#ggqqplot(accuracy_transf$subject.mean[1:32])
ggqqplot(accuracy_transf_norm$subject.mean[1:32])

ggqqplot(times_raw$subject.mean[1:32])
#ggqqplot(times_transf$subject.mean[1:32])
ggqqplot(times_transf_norm$subject.mean[1:32])

# no questionnaire raw subject means
# no questionnaire transf
ggqqplot(questionnaire_norm$subject.mean[1:32])
