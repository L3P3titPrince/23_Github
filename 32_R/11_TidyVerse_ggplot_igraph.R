"
What is Tidyverse?

Here is a brief introduction:
R is an incredibly powerful programming language for statistical analysis and data science. 
The tidyverse collects some of the most versatile R packages: 
(ggplot2, dplyr, tidyr, readr, purrr, and tibble)

The packages work in harmony to clean, process, model, and visualize data.
While all packages share an underlying design philosophy, grammar, and data structures.
"

##### Part 1: Tidyverse ####

# 1.1: dplyr -----
# Loading packages
install.packages("tidyverse")
library(tidyverse) # both dplyr and ggplot2 are part of the tidyverse

# Input the data we need for this part
# Here is an example dataset from Kaggle
# Make sure you click menu Session -> Set Working Directory -> To Source File Location
df <- read_csv("Lab-1-Data/athlete_events.csv")

# Give a brief view of this dataframe
head(df)
str(df)

# First operator: Filter
# Filter help us filter subset observations
df_new <- df %>%
  filter(Sex == "M")

# Filter with different options
df_new <- df %>%
  filter(Sex == "M", Age == 24)

# Please notice that we use == as the operator

# Arrange
# Arrange helps us sorting with specific col
df_new <- df %>%
  arrange(Age)

# Descending order
df_new <- df %>%
  arrange(desc(Age))

# Now we have two functions, can we combine them?
df_new <- df %>%
  filter(Sex == "M", Age < 24, Height < 150) %>%
  arrange(desc(Age))

# Third funnction: mutate
# Mutate function is used to change or add variable
df_new <- df %>%
  mutate(Age = Age*300, Height = Height/100)

# Add new col with existing cols
df_new <- df %>%
  mutate(BMI = Weight/(Height**2))

# Summarize and group by
df_new <- df[1:100,] %>%
  group_by(Age) %>%
  summarize(weight_mean = mean(Weight),
            weight_sum = sum(Weight))

# 1.2: ggplot -----
# Import the ggplot package
library(ggplot2)

# Select the dataframe we wanna draw picture with
df_nor <- df %>%
  filter(Team == 'Norway')

# first plot
ggplot(df_nor,    # the data set you wanna use
       aes(x=Age, y=Weight)) + geom_point()

# If we find that the points has too much density in low range
ggplot(df_nor,    # the data set you wanna use
       aes(x=Age, y=Weight)) + geom_point() + scale_x_log10()

# Try to contain more information
ggplot(df_nor[1:50,],
       aes(x=Age, y=Weight, color = Sport, size = Height)) + geom_point()

# Or you can choose to start from the 0
ggplot(df_nor[1:50,],
       aes(x=Age, y=Weight, color = Sport, size = Height)) + geom_point() + expand_limits(y=0)

# You can also add in title if you want with: + ggtitle("name of your plot")

"
We have more kinds of plot that we can use in our ggplot package:

scatter plot: geom_piont()

line plot: geom_line()

bar plot: geom_col()

histogram: geom_histogram()   # Here only one input

box plot: geom_boxplot()
"


#### Part 2: igraph ####

# There are 2 common types of network data: adjacency matrix and edgelist
# Here we use clinton e-mail as input data
# Data input
install.packages("igraph")
library(igraph)

# 2.1  Create an undirected social network from an adjacency list. -----
#  (1,2) is the first edge, and (1,3) is the second edge, etc.
g <- graph(edges = c(1,2,1,3,1,4,3,4), n=4, directed = FALSE)
class(g)
g
is.directed(g)
summary(g)
# define some attributes for nodes
V(g)
V(g)$name <- c('Mike', 'Lisa', 'John', 'Frank')
V(g)$gender <- c('M', 'F', 'M', 'M')
summary(g)
E(g)
# plot is a "generic function" in R
# to search for help, use ?plot.igraph
plot(g)


# 2.2 A larger network (Karate club) -----
# https://en.wikipedia.org/wiki/Zachary%27s_karate_club
# The network is defined in a Geography Markup Language (GML) file.
# You can open the file using a text editor. 
g2 <- read.graph(file = "Lab-1-Data/karate.gml", format = "gml")
g2
# number of edges and nodes (vertices)
vcount(g2)
ecount(g2)
# name the nodes as N1, N2, ...
V(g2)$name <- paste0("N", c(1:vcount(g2)))
# plot
plot(g2)
# customize the plots
plot(g2, vertex.label.cex=0.5)
plot(g2, layout=layout.fruchterman.reingold, vertex.size=5, vertex.label=NA)
plot(g2, layout=layout.circle, vertex.size=5, vertex.label=NA)

# degree and degree distribution
degree(g2)

# which node has the highest degree?
V(g2)[which.max(degree(g2))]
V(g2)[degree(g2) == max(degree(g2))]

# degree distributions
hist(degree(g2))
table(degree(g2))
sum(degree.distribution(g2))
barplot(degree.distribution(g2))

# density
graph.density(g2)

# Node 1's 1.5-degree egocentric network
ego(g2, order = 1.5, nodes = 1)
ego(g2, order = 2, nodes = 1)
# ego() lists the nodes, make_ego_graph creates a list of subgraphs
ego_network_1 <- make_ego_graph(g2, order = 1.5, nodes = 1)[[1]]
plot(ego_network_1)
# remove node 1 itself from the ego network
plot(delete_vertices(ego_network_1, v = 1))

# clustering coefficient 
transitivity(g2, type = "local")
transitivity(g2, type = "global")

# transitivity is the same as 
# the density of the 1.5 ego network with the node itself removed
transitivity(g2, type = "local")[1]
graph.density(delete_vertices(ego_network_1, v = 1))
