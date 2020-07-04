# Wiki Racer

[Wiki Racing](https://en.wikipedia.org/wiki/Wikiracing) 
is game where people compete to see how fast they can navigate between two randomly selected
Wikipedia pages by only clicking links in the articles. Wiki Racer uses natural language processing to search the most relevant pages first.

## Example 
Finding the path from [crocodiles](https://en.wikipedia.org/wiki/Crocodile) to [salad](https://en.wikipedia.org/wiki/Salad)
```console
SOLVING: /wiki/crocodile -> /wiki/salad
distance: 0.828, exploring: /wiki/crocodile
distance: 0.267, exploring: /wiki/chicken_as_food
distance: 0.301, exploring: /wiki/lobster
distance: 0.309, exploring: /wiki/sausage
distance: 0.31, exploring: /wiki/steak
distance: 0.211, exploring: /wiki/fried_chicken
distance: 0.252, exploring: /wiki/bean_sprouts_chicken
distance: 0.259, exploring: /wiki/stew
distance: 0.211, exploring: /wiki/fried_fish
distance: 0.301, exploring: /wiki/lobster_(disambiguation)
distance: 0.301, exploring: /wiki/lobster_newberg
distance: 0.206, exploring: /wiki/potato_salad
SOLVED: /wiki/crocodile -> /wiki/sausage -> /wiki/potato_salad -> /wiki/salad (3.6 seconds)
```

## Algorithm
This algorithm is a essentially breadth first search. However when visiting a page only the 4 most relevant pages are 
added to the queue. The cosine distance between two [GloVe]( https://en.wikipedia.org/wiki/GloVe_\(machine_learning\)) word embeddings 
(one for link that could be explored and the target link)
is used to calculate how relevant a page is. The lower the cosine distance the more relevant the page is.

## Potential Further Improvements
1. Currently the the word embeddings are generated using only the first word of each link. So a lot of information is lost
when links contain more than one word. 
2. Implementing a priority queue. 
3. Testing different word embedding models
