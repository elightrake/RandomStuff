# GET LINE BASED ON ODDS
get_line <- function(odds){
  if (odds <= 0.5) {
    line <- (100 - odds*100)/odds
  } else {
    line <- -(odds*100)/(1 - odds)
  }
  return(line)
}

# GET ODDS BASED ON LINE
get_odds <- function(line){
  if (line > 0) {
    these_odds <- 100/(100 + line)
  } else {
    these_odds <- abs(line)/(100 + abs(line))
  }
  return(these_odds)
}


lines <- c(225,-183,120,-265)
odds <- NA
for (i in 1:length(lines)) {
  line <- lines[i]
  these_odds <- get_odds(line)
  odds[i] <- these_odds
}
total_prob <- prod(odds)
odds; total_prob
10/total_prob
mean(odds); sd(odds)
total_prob^(1/length(lines)); (15/342)^(1/length(lines))
1-pnorm((15/407)^(1/length(lines)),mean= mean(odds),sd= sd(odds))
