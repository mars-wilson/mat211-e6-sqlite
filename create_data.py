"""
This script is for generating data and then exporting ot to json format for the exercise
Not part of the exercise itself.

It does define the overall datatypes.
"""
import json
import random
import datetime
import math

TODAY = datetime.date.today()

store = [
    {"name": 'West Avl',  "kind": 'cafe',   'volume': 1241},
    {"name": 'East Avl',  "kind": 'cafe',   'volume': 842},
    {"name": 'Blk Mtn',   "kind": 'bistro', 'volume': 1590},
    {"name": 'Lexington', "kind": 'cafe',   'volume': 3310},
]

special = [
    # {'date': '2021-10-17', 'store_name': 'West Avl', 'coffee_name': 'volcano', 'price': 3.50}
]

coffee = [  # rating is not to be included in the db.
    {'name': 'volcano',      'type': 'espresso',     'cost_lb': 12.15},
    {'name': 'rumble',       'type': 'dark roast',   'cost_lb': 8.45},
    {'name': 'fling',        'type': 'light roast',  'cost_lb': 9.10},
    {'name': 'expedition',   'type': 'dark roast',   'cost_lb': 11.10},
    {'name': 'sunrise',      'type': 'espresso',     'cost_lb': 7.00},
    {'name': 'blingbling',   'type': 'medium',       'cost_lb': 11.25},
    {'name': 'zzzzzzpao',    'type': 'espresso',     'cost_lb': 12.55},
    {'name': 'joyful smile', 'type': 'latte',        'cost_lb': 9.25},
    {'name': 'spankin',      'type': 'dark roast',   'cost_lb': 10.45},
    {'name': 'bliss',        'type': 'latte',        'cost_lb': 10.85},
    {'name': 'iron fist',    'type': 'espresso',     'cost_lb': 9.55}
]


coffee_ratings = {  # rating is not to be included in the db. Used to calculate customer ratings.
    'volcano': 5,
    'rumble': 3,
    'fling': 4,
    'expedition': 5,
    'sunrise': 3,
    'blingbling': 4,
    'zzzzzzpao': 5,
    'joyful smile': 2,
    'spankin': 4,
    'bliss': 3,
    'iron fist': 5
}

rating = [
    # {'date': '2021-10-17',  'store_name': 'West Avl', 'rating': 2, 'note': 'coffee was too noisy'}
]


comments = {
    1: ['has an acrid, repulsive smell', 'too noisy',
        'my girlfriend dumped me. Im sad.',
        ' it was so bitter and nasty I couldnt drink it.'],
    2: ['This turned out to be awful coffee. ',
        'For me, this  coffee was so unpleasant that I couldnt finish the first cup.',
        'great but I want free reflills'],
    3: ["I mostly always get the morning blend wanted to try out a more darker coffee so tried this one out. Honestly in my opinion the morning blend is way better then this one but that's ok I'll enjoy it anyways.!",
        "First time drinking this coffee and it does have a smooth flavor that isn't bitter but I wouldn't consider this to be bold coffee. ",
        "Taste is ok"],
    4: [" I drink about 6 cups a day and this one doesn't make me feel jittery. ",
        "so went money is tight this is what I drink. Oh! with lots of cream and sugar, that way I can’t really tell the difference-",
        "we only bought it because french roast was NOT available. we wanted to buy french roast. when your used to one roast, another can not take it's place.",
        "Boldy weak taste. ",
        "Whenever I like a product, it gets discontinued. ",
        "she was happy to have her morning coffee.",
        "The previous ones I got were medium to dark roast coffee, but I needed something to drink in the afternoon that is not too strong"],
    5: ["Well I love dark roasted coffee & wanted to try this smooth & bold dark roast, but was kinda of dissatisfied with the flavor I hate to say this bur it was pretty bitter",
        "The previous ones I got were medium to dark roast coffee, but I needed something to drink in the afternoon that is not too strong",
        "I like really strong coffee but sometimes bold or dark roasts just don't live up to the name."
        "At first I didn’t love this coffee. But then I started using that cheap fake creamer that is made with corn syrup solids but somehow isn’t sweet at all and comes in powder form and it transformed this into something really good (they call it coffee mate).",
        "Love this coffee. ",
        "Great coffee, smooth and bold"
    ]
}

def find_special(specials, d, s):
    s = s['name']
    for sp in specials:
        if sp['date'] == d and sp['store_name'] == s:
            return sp
    return {}


def find_coffee(coffees, name):
    if name is None:
        return {}
    for c in coffees:
        if c['name'] == name:
            return c
    print(f"No coffee  named {name}")
    return {}

def generate_specials(special, store, coffee,days=90, specialChance = 0.5):
    for d in range(days):
        for s in store:
            if random.random() < specialChance:
                randomcoffee = random.choice(coffee)
                price = randomcoffee['cost_lb']  //  (random.uniform(1.5,3.3) + 1)
                price = price + random.choice([0.0,0.5,0.25,0.50,0.55,0.75,0.95])
                special.append(  {
                    'date': (TODAY - datetime.timedelta(days=d)).isoformat(),
                    'store_name': s['name'],
                    'coffee_name': randomcoffee['name'],
                    'price': price
                } )


def generate_ratings(ratings, stores, specials, coffees, days=90, ratingChance = 0.01, goodprice = 4):
    maxr = -100000
    minr = 100000
    normalprice = goodprice + 1
    for d in range(days):
        for s in stores:
            dte = (TODAY - datetime.timedelta(days=d)).isoformat()
            special = find_special(specials, dte, s)
            print(f" special for {dte} store {s} is " +
                  (special.get('coffee_name','none') + f" {special.get('price', normalprice):0.2f}"))
            coffee_name = special.get('coffee_name', None)
            coffee = find_coffee(coffees, coffee_name)
            for v in range(s['volume']):
                if random.random() < ratingChance:
                    # skew the rating towards the price a bit.  If there is no special assume the
                    #    price is $1 more than the good price for a coffee.
                    coffeepricerating = coffee_ratings.get(coffee_name, 4) * (goodprice / special.get('price', normalprice))
                    # sqrt compresses the result to bend the distribution towards higher ratings.
                    r = math.sqrt(coffeepricerating * (random.random() + 0.5))
                    for more_randomness in range(3): # add in some extra skewed randomness
                        r += math.sqrt(random.randint(1,5))
                    print(coffeepricerating, r)
                    maxr = maxr if r < maxr else r
                    minr = minr if r > minr else r
                    ratings.append(
                        {
                            'date': dte,
                            'store_name': s['name'],
                            'rating': r,
                            'text': ''
                        })
    print(f"min {minr} max {maxr}  - normalizing 1-5 ")
    for rating in ratings:
        r = rating['rating']
        # scale r to 0..1
        r1 = (r-minr) / (maxr-minr)
        # scale r to 0 to 6.9  so that we'll have more 5 star ratings
        r2 = r1 * 8 + 1
        # trunk to int and change > 5 to 5
        ri = min([5, int(r2)])
        print(r,r1,r2,ri)
        rating['rating'] = ri
        rating['text'] = random.choice(comments.get(ri, ['']))
    print(f"min {minr} max {maxr}  - normalizing 1-5 ")



generate_specials(special, store, coffee)
for s in special:
    print(s)

generate_ratings(rating,store,special,coffee)
for r in rating:
    print(r)


# dump the four tables to json.
with open('data/cafe_reviews.json', 'w') as fp:
    data = {
        'store':  store,
        'special': special,
        'coffee': coffee,
        'rating': rating,
    }
    json.dump(data, fp)

with open('data/stores.csv','w') as fp:
    fp.write(f"name\tkind\tvolume\n")
    for s in store:
        fp.write(f"{s['name']}\t{s['kind']}\t{s['volume']}\n")
with open('data/specials.csv','w') as fp:
    fp.write(f"date\tstore_name\tcoffee_name\tprice\n")
    for s in special:
        fp.write(f"{s['date']}\t{s['store_name']}\t{s['coffee_name']}\t{s['price']}\n")
with open('data/coffees.csv', 'w') as fp:
    fp.write(f"name\ttype\tcost_lb\n")
    for c in coffee:
        fp.write(f"{c['name']}\t{c['type']}\t{c['cost_lb']}\n")
with open('data/ratings.csv', 'w') as fp:
    fp.write(f"date\tstore_name\trating\n")
    for r in rating:
        fp.write(f"{r['date']}\t{r['store_name']}\t{r['rating']}\n")
