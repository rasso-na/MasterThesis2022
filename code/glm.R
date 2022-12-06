### 調査においては不使用

library(lme4)
library(ggeffects)
library(tidyverse)
library(MASS)
library(easystats)
library(gridExtra)


myglm = function(formula, plotstr, df) {
  
  model.fit <- glm(f, family = binomial, data = df)
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
  for ( l in cols ) {
    model.pred <- ggpredict(model.step, terms = l)
    model.plot <- plot(model.pred)
    p <- c(p, list(model.plot))
  }
  
  do.call(grid.arrange, p)
  
}



df <- read.csv(
  '../out/reformed_original.csv',
  header = T,
  stringsAsFactors = F
)
head(df)
names(df)
str(df)
# df <- df[df$pos=="名詞",]
df

K_acc_A <- ifelse(df$K_acc=='A', 1, 0)
K_acc_B <- ifelse(df$K_acc=='B', 1, 0)

attach(df)

f = K_acc_A ~ wType + pos + len_mora + len_syll
cols <- list(c("wType", "pos"), c("len_mora"), c("len_syll"))

myglm(f, cols, df)
