library(ggplot2)
library(tidyverse)

biggest_stack <- 1000
shuffles <- matrix(NA, nrow = biggest_stack, ncol = 3)
colnames(shuffles) <- c("shuff_size", "half", "full")
for (i in 1:biggest_stack) {
  shuffles[i,"shuff_size"] <- i*2
  stack <- c(1, rep(0, i*2 - 1))
  s1 <- stack[1:(length(stack)/2)]
  s2 <- stack[(1 + length(stack)/2):length(stack)]
  stack <- c(rbind(s2,s1))
  shuff_count <- 1
  while (stack[1] == 0) {
    if (stack[length(stack)] == 1) {
      shuffles[i, "half"] <- shuff_count
    }
    s1 <- stack[1:(length(stack)/2)]
    s2 <- stack[(1 + length(stack)/2):length(stack)]
    stack <- c(rbind(s2,s1))
    shuff_count <- shuff_count + 1
  }
  shuffles[i, "full"] <- shuff_count
}
shuffles <- as_tibble(shuffles)

ggplot(data = shuffles) +
  geom_point(aes(x = shuff_size, y = full)) +
  geom_point(aes(x = shuff_size, y = half, colour = 'red'))
