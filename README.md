# Inspiry

![alt text](http://s019.radikal.ru/i616/1705/56/9f8dccf9f3ac.png)

## Overview
**Inspiry** is an iOS app that keeps all your memories in one place automatically collecting travels from your Instagram and Twitter.

In this repository you can find an algorithm for this application.

The iOS app implemented by [adanilyak](https://github.com/adanilyak) you can find [here](https://bitbucket.org/project_travel/ios_project_travel).

## Algorithm
You can see an example of an algorithm's execution and uderstand the data format with a help of [tests](https://github.com/mashaka/Inspiry/tree/master/tests).

Major algorithm keypoints:
* Receives as input information user's post from [Instagram API](https://www.instagram.com/developer/) and [Twitter API](https://dev.twitter.com/rest/public).
* Returns list of instances of the [Trip class](https://github.com/mashaka/Inspiry/blob/master/algo/trip.py).
* Updates geodata in posts using [osm_rg_wikidata library](https://github.com/Scitator/osm_rg/tree/wikidata) that uses [Wikidata Query](https://query.wikidata.org/) as source for geodata.
* Finds change of countries and cities.
* Separates "trip hypotheses" based on gaps in time between posts.
* Calculates locations statistics and find local cities and their satelite towns
* Excludes local cities and hypotheses without location
* Excludes very long "trips hypotheses" (rare persons travel longer than 90 days)
* Unites small city trips in a one big country trip
* Wraps results in Trip objects

## Teammates
The whole project was implemented by:
- iOS app: [adanilyak](https://github.com/adanilyak)
- Algorithm: [mashaka](https://github.com/mashaka)
- Website: [AlexeyZhuravlev](https://github.com/AlexeyZhuravlev)
- Backend: [seka17](https://github.com/seka17)
- [osm_rg_wikidata library](https://github.com/Scitator/osm_rg/tree/wikidata): [Scitator](https://github.com/Scitator)
