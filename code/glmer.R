### 調査においては不使用
### 一般化線形混合モデル（ロジスティック回帰分析）

library(lme4)
library(ggeffects)
library(tidyverse)
library(MASS)
library(easystats)
library(gridExtra)

data.nd <- read.csv("../out/reformed_notdummy.csv", header=T)
head(data.nd)
attach(data.nd)

f = K_acc_B ~ pos + len_syll + len_mora  + (1 | wType)
plot.cols <- list(c("wType", "pos"), c("len_mora", "wType"), c("len_syll", "wType"), c("len_mora", "pos"), c("len_syll", "pos"))

model.fit <- glmer(f, family = binomial, data = data.nd)
print("summary")
print(summary(model.fit))
print("coef")
print(coef(model.fit))
print("ranef")
print(ranef(model.fit))

p <- list()
for ( l in plot.cols ) {
  model.pred <- ggpredict(model.fit, terms = l, type = "re")
  model.plot <- plot(model.pred)
  p <- c(p, list(model.plot))
}
# par(new = T)
do.call(grid.arrange, p)

# model.pred <- ggpredict(model.fit, type = "re", terms = c("wType", "pos"))
# model.pred %>% as_tibble()
# p1 <- plot(model.pred)
# gridExtra::grid.arrange(p1)

detach(data.nd)
