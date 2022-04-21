
#  **Dev Notes**
## Thursday, March 24, 2022

### Known tasks
- [ ] Fix [clustering](clusterResolve.py) strange behavior
     - Clustering inconsistencies, errors
     - [strange](other_resources/terrible.png) [clustering](other_resources/slightlybetter.png) [errors](other_resources/speechcluster.png)
- [ ] Extensive documentation
     - Code is cryptic, esoteric, and generally confusing in both appearance and function.
     - Draft a getting started page.
- [ ] Finalize live node system
     - Tying changing information (like the current time) to static nodes for quick reference by the [semweb](semweblib.py)
- [ ] Data flows
     - Data must flow upwards from [textflow](textflow.py) for communication between loops
     - Connect the [language loop](languageloop.py) to the [causal model](causal_model.py)
     - Reconnect the speaker-id to [textflow](textflow.py) and update the semantic web to accept it again
- [ ] Forgetfulness
     - [Semantic web](semweblib.py) needs to forget conflicting facts to improve accuracy and time efficiency
     - Dependent on completion of root representation.
- [ ] Runtime
     - Call each loop from a main one.
 - [ ] Deployment
      - Update github
### Recent progress
- Located and removed bug in [clusterResolve](clusterResolve.py)
- Improved Wyze integrations
- Began root representation format
- Optimized audio loop
- Fixed up the repo / serious misplaced code issue
- Organized a little bit
### General notes
- More persistency

## Thursday, April 7, 2022
### Known tasks
- [ ] Fix [clustering](clusterResolve.py) strange behavior
     - Clustering inconsistencies, errors
     - [strange](other_resources/terrible.png) [clustering](other_resources/slightlybetter.png) [errors](other_resources/speechcluster.png)
- [ ] Extensive documentation
     - Code is cryptic, esoteric, and generally confusing in both appearance and function.
     - Draft a getting started page.
- [ ] Finalize live node system
     - Tying changing information (like the current time) to static nodes for quick reference by the [semweb](semweblib.py)
- [x] Data flows
     - Data must flow upwards from [textflow](textflow.py) for communication between loops
     - Connect the [language loop](languageloop.py) to the [causal model](causal_model.py)
     - Reconnect the speaker-id to [textflow](textflow.py) and update the semantic web to accept it again
- [ ] Forgetfulness
     - [Semantic web](semweblib.py) needs to forget conflicting facts to improve accuracy and time efficiency
     - Dependent on completion of root representation.
- [x] Runtime
     - Call each loop from a main one.
 - [ ] Deployment
      - Update github
### Recent progress
- Rewrite of [clusterResolve](clusterResolve.py)
- Began Electron app
- Runtime working
- Fixed up the repo / serious misplaced code issue
- Tested language processing at scale

## Thursday, April 7, 2022
### Recent progress
- Fuzzy date, time, extraction, resolution, profile resolution, reference for both, symbolic pre-processing, symbolic pre-pre-processing
- Inflection standardization
- Discovered necessity of rerolling wern
- part 1/3 of nprop implementation (where in runtime, preprocessing)
- Reliable fast TTS
- Install, setup, script
