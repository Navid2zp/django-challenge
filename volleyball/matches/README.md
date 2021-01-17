# Matches

### Add/List matches (MatchAPI class):

We used a single class to handle creating a match and creating one. It might be a good idea to separate these two
logics, but we combined them together since there won't be any future changes and to have a simple a reusable code.

### List of match seats (MatchSeatsAPI):

This endpoint should only be used to get the initial details for the seats. there is no state included so in can be
fully cached.

### List of available match seats (MatchAvailableSeatsAPI):

We need a way to check for changes in our seats state and update the frontend accordingly. A websocket would be a better
idea since we can immediately notify other clients in case any change in seats states happened, and we won't need to
query the database again and again. But this method is also fast enough to be used as a work-around.

### Adding seats for the match (MatchAddSeatAPI):

There are different ways to handle this type of requirement. To name a few:

- Adding seats one by one.
- Excluding seats from the stadium.
- Using bulk creates.
- Using ranges.
- etc.

It depends on the frontend and how the admin panel is generated and which one might be easier for admins. A combination
of these options can be used together to make it easier in different situations.

We implemented bulk creating using ranges, but many more options can be added.

#### NOTE on URL endpoints:

Both create match and list matches use the same url but different methods. Other URLs might not have the best namings
either. It was a one-day project without much planning so ...





