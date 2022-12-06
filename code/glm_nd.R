### 調査において使用したコード
### 一般化線形モデル（ロジスティック回帰分析）

library(lme4)
library(ggeffects)
library(tidyverse)
library(MASS)
library(easystats)
library(gridExtra)

dat <- read.csv("../out/reformed_notdummy.csv", header=T)
head(dat)
attach(dat)

f = K_acc_B ~ wType + pos + len_syll + len_mora + pmw
plot.cols <- list(c("wType", "pos"), c("len_mora", "wType"), c("len_syll", "wType"), c("len_mora", "pos"), c("len_syll", "pos"))

model.fit <- glm(f, family = binomial, data = dat)
model.step <- step(model.fit)
print("summary:")
print(summary(model.step))
print("オッズ比:")
print(exp(model.step$coefficients))
print("(exp(COEF)-1)*100：")
print((exp(model.step$coefficients)-1)*100)
print("信頼区間:")
print(exp(confint(model.step)))

p <- list()
for ( l in plot.cols ) {
  model.pred <- ggpredict(model.step, terms = l)
  model.plot <- plot(model.pred)
  p <- c(p, list(model.plot))
}
# par(new = T)
do.call(grid.arrange, p)

detach(dat)
