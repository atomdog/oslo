
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

## Thursday, April 14, 2022
### Recent progress
- Fuzzy date, time, extraction, resolution, profile resolution, reference for both, symbolic pre-processing, symbolic pre-pre-processing
- Inflection standardization
- Discovered necessity of editing, rerolling wern, editing, rerolling wern,...
- part 1/3 of nprop implementation (where in runtime, preprocessing)
- Reliable fast TTS 
- Setup: pip install pipwin && pipwin install pyaudio && python cleo.py -s "text to be spoken"
- Install, setup, script
- Failed dockerization (too much change)
- Resetting repo again (too much change)
### Notes
- shelving UI until post github 
- symbolically parsing time is probably NP-hard
- so close to getting to production level
- QA accuracy, recall accuracy, increases as # of symbolic conversions increase

## Thursday, April 28, 2022
### Notes
#### aidan
- fixing up repo is halfway done (dead-end imports gone)
- symbolically parsing time is still probably NP-hard 
- substitution reliant on balancing edits versus accuracy, make it make sense
- "dockerized" working partially, unforeseen drawbacks
- symbolic standardization, states talking to calculus, hugely reliant standardization
- charting things
#### chase
- added punctation handling for playing :, ,, !, ?, .
- fixed bug with playing start of audio experiencing clipping in non-blocking hardware by adding a slight delay
- cleaning up the functionality of adding pauses before/after/between words
- started using the pyaudio interface directly to have our own functions for playing back the generated audio segments
- pulls

## Thursday, May 5th, 2022
## Notes
#### aidan
- some concluding thoughts:
- model architecture json is necessary, it is a language model that gets generated in the wrong place but I don't want to fix it right now
- Kaldi changed versions and changed the recognizer call 

## June 20th, 2022
## Notes
- [svomapping.pdf](svomapping.pdf)
- made landing more aesthetically pleasing
- made a readthedocs
- [demo](https://github.com/atomdog/oslo/blob/main/other_resources/demo.webm)
- amount of integrations causing headaches
- large scope of use, memory; accuracy breaking down
## June 27th, 2022
## Notes
- Added [flags.json](flags.json) to track initialization state as well as enabled integrations
- Added [Dockerfile](Dockerfile)
- Added [dockerize.sh](dockerize.sh) to automatically build docker image
     - Docker image builds to ~ 6.5 gb, using python3 base
     - Known Tensorflow version bug (Thanks to PIP)
- Furthered [SVO mappings](https://github.com/atomdog/svo-trigram-space)
- Identified multiple conflicts between dev repo and this one
- Advanced nprop formal system design significantly (experimentally implementing)
