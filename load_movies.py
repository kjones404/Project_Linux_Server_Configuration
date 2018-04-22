#!/usr/bin/env python3

""" Loads Movie Data for Item Catalog Project

This project is part of the Udacity Full Stack Nanodegree program.

"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Collection, Base, MovieItem, User


engine = create_engine('postgresql://catalog:catalog@localhost/moviecatalogs')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def fred():
    # Create Fred
    User1 = User(name="Fred",
                 email="Fred@moviecollections.com")
    session.add(User1)
    session.commit()
    # Create collection for Fred
    collection1 = Collection(name="Fred", user_id=1)
    session.add(collection1)
    session.commit()
    # Add movies to Freds collection
    movieItem1 = MovieItem(title="The Fifth Element",
                           year="1997",
                           img="https://image.tmdb.org/t/p/w342/" +
                           "zaFa1NRZEnFgRTv5OVXkNIZO78O.jpg",
                           description="In 2257, a taxi driver is" +
                           " unintentionally given the task of saving a" +
                           " young girl who is part of the key that will" +
                           " ensure the survival of humanity.",
                           user_id=1,
                           collection=collection1)
    movieItem2 = MovieItem(title="John Wick",
                           year="2014",
                           img="https://image.tmdb.org/t/p/w342/" +
                           "5vHssUeVe25bMrof1HyaPyWgaP.jpg",
                           description="Ex-hitman John Wick comes out of" +
                           " retirement to track down the gangsters that" +
                           " took everything from him.",
                           user_id=1,
                           collection=collection1)
    movieItem3 = MovieItem(title="Guardians of the Galaxy ",
                           year="2014",
                           img="https://image.tmdb.org/t/p/w342/" +
                           "y31QB9kn3XSudA15tV7UWQ9XLuW.jpg",
                           description="Light years from Earth, 26 years" +
                           " after being abducted, Peter Quill finds himself" +
                           " the prime target of a manhunt after discovering" +
                           " an orb wanted by Ronan the Accuser.",
                           user_id=1,
                           collection=collection1)
    movieItem4 = MovieItem(title="The Princess Bride",
                           year="1987",
                           img="https://image.tmdb.org/t/p/w342/" +
                           "gpxjoE0yvRwIhFEJgNArtKtaN7S.jpg",
                           description="In this enchantingly cracked fairy" +
                           " tale, the beautiful Princess Buttercup and the" +
                           " dashing Westley must overcome staggering odds" +
                           " to find happiness amid six-fingered swordsmen," +
                           " murderous princes, Sicilians and rodents of" +
                           " unusual size. But even death can't stop these" +
                           " true lovebirds from triumphing.",
                           user_id=1,
                           collection=collection1)
    movieItem5 = MovieItem(title="Office Space",
                           year="1999",
                           img="https://image.tmdb.org/t/p/w342/" +
                           "iO9aZzrfmMvm3IqkFiQyuuUMLh2.jpg",
                           description="Three office workers strike back at" +
                           " their evil employers by hatching a hapless" +
                           " attempt to embezzle money.",
                           user_id=1,
                           collection=collection1)
    movieItem6 = MovieItem(title="Ghostbusters",
                           year="1984",
                           img="https://image.tmdb.org/t/p/w342/" +
                           "3FS3oBdorgczgfCkFi2u8ZTFfpS.jpg",
                           description="After losing their academic posts" +
                           " at a prestigious university, a team of" +
                           " parapsychologists goes into business as" +
                           " proton-pack-toting ghostbusters who exterminate" +
                           " ghouls, hobgoblins and supernatural pests of" +
                           " all stripes. An ad campaign pays off when a" +
                           " knockout cellist hires the squad to purge her" +
                           " swanky digs of demons that appear to be living" +
                           " in her refrigerator",
                           user_id=1,
                           collection=collection1)
    session.add(movieItem1)
    session.add(movieItem2)
    session.add(movieItem3)
    session.add(movieItem4)
    session.add(movieItem5)
    session.add(movieItem6)
    session.commit()


def bob():
    # Create Bob
    User2 = User(name="Bob",
                 email="Bob@moviecollections.com")
    session.add(User2)
    session.commit()
    # Create a collection for Bob
    collection2 = Collection(name="Bob", user_id=2)
    session.add(collection2)
    session.commit()
    # Add movies to collection
    movieItem21 = MovieItem(title="WALL-E",
                            year="2008",
                            img="https://image.tmdb.org/t/p/w342/" +
                            "9cJETuLMc6R0bTWRA5i7ctY9bxk.jpg",
                            description="WALL-E is the last robot left on an" +
                            " Earth that has been overrun with garbage and" +
                            " all humans have fled to outer space. For 700" +
                            " years he has continued to try and clean up the" +
                            " mess, but has developed some rather" +
                            " interesting human-like qualities. When a ship" +
                            " arrives with a sleek new type of robot, WALL-E" +
                            " thinks he's finally found a friend and stows" +
                            " away on the ship when it leaves.",
                            user_id=2,
                            collection=collection2)
    movieItem22 = MovieItem(title="Up",
                            year="2009",
                            img="https://image.tmdb.org/t/p/w342/" +
                            "nk11pvocdb5zbFhX5oq5YiLPYMo.jpg",
                            description="Carl Fredricksen spent his entire" +
                            " life dreaming of exploring the globe and" +
                            " experiencing life to its fullest. But at age" +
                            " 78, life seems to have passed him by, until" +
                            " a twist of fate (and a persistent 8-year old" +
                            " Wilderness Explorer named Russell) gives him" +
                            " a new lease on life.",
                            user_id=2,
                            collection=collection2)
    movieItem23 = MovieItem(title="Brave",
                            year="2012",
                            img="https://image.tmdb.org/t/p/w342/" +
                            "qhABv2d4NZLhsOOA4iBFM4rfuJC.jpg",
                            description="Merida (Kelly Macdonald), the" +
                            " impetuous but courageous daughter of Scottish" +
                            " King Fergus (Billy Connolly) and Queen Elinor" +
                            " (Emma Thompson), is a skilled archer who wants" +
                            " to carve out her own path in life. Her" +
                            " defiance of an age-old tradition angers the" +
                            " Highland lords and leads to chaos in the" +
                            " kingdom. Merida seeks help from an eccentric" +
                            " witch (Julie Walters), who grants her an" +
                            " ill-fated wish. Now, Merida must discover" +
                            " the true meaning of courage and undo a" +
                            " beastly curse before it's too late.",
                            user_id=2,
                            collection=collection2)
    movieItem24 = MovieItem(title="Ratatouille",
                            year="2007",
                            img="https://image.tmdb.org/t/p/w342/" +
                            "y8y6Fv0k068OnHBZtu949A1t6pj.jpg",
                            description="A rat named Remy dreams of becoming" +
                            " a great French chef despite his family's" +
                            " wishes and the obvious problem of being a rat" +
                            " in a decidedly rodent-phobic profession. When" +
                            " fate places Remy in the sewers of Paris, he" +
                            " finds himself ideally situated beneath a" +
                            " restaurant made famous by his culinary hero," +
                            " Auguste Gusteau. Despite the apparent dangers"
                            " of being an unlikely - and certainly unwanted" +
                            " - visitor in the kitchen of a fine French" +
                            " restaurant, Remy's passion for cooking soon" +
                            " sets into motion a hilarious and exciting rat" +
                            " race that turns the culinary world of Paris" +
                            " upside down.",
                            user_id=2,
                            collection=collection2)
    movieItem25 = MovieItem(title="Finding Nemo",
                            year="2003",
                            img="https://image.tmdb.org/t/p/w342/" +
                            "syPWyeeqzTQIxjIUaIFI7d0TyEY.jpg",
                            description="Nemo, an adventurous young" +
                            " clownfish, is unexpectedly taken from his" +
                            " Great Barrier Reef home to a dentist's office" +
                            " aquarium. It's up to his worrisome father" +
                            " Marlin and a friendly but forgetful fish Dory" +
                            " to bring Nemo home -- meeting vegetarian" +
                            " sharks, surfer dude turtles, hypnotic" +
                            " jellyfish, hungry seagulls, and more along" +
                            " the way.",
                            user_id=2,
                            collection=collection2)
    movieItem26 = MovieItem(title="Piper",
                            year="2016",
                            img="https://image.tmdb.org/t/p/w342/" +
                            "jLRllZsubY8UWpeMyDLVXdRyEWi.jpg",
                            description="A mother bird tries to teach her" +
                            " little one how to find food by herself. In the" +
                            " process, she encounters a traumatic experience" +
                            " that she must overcome in order to survive.",
                            user_id=2,
                            collection=collection2)
    session.add(movieItem21)
    session.add(movieItem22)
    session.add(movieItem23)
    session.add(movieItem24)
    session.add(movieItem25)
    session.add(movieItem26)
    session.commit()


def main():
    bob()
    fred()
    print ("added movie items!")


if __name__ == '__main__':
    # will only be executed when ran directly
    main()
