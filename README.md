# ![Alt text](other_resources/oslologo.png)
The oslo (open source loop operator) project is an effort to produce an esoteric open source virtual assistant framework that is:

- meant to be hacked on
- diverse in functionality
- privacy concious
- a stepping stone for creating more sophisticated agents

## why?
- [why is it named a 'loop operator'?](https://github.com/atomdog/oslo/wiki/Some-Background)
## Getting things running
- start by installing required libraries using the requirements.txt and then running startup.py
- the model runs from main.py, once you get to that point
- make sure you add the proper api keys to config.json, critically at least a gmail account
- the gmail account you use doesn't matter, it can be a fake one, so long as OSLO can reach text messages
- if you'd like to disable texting, icloud or other runtime features, use the flags within main as well
- the required models can be found [here](https://mega.nz/folder/KegjSQAC#Xs4SzflsKlT5jeXkuvB06Q)
- the [wiki](https://github.com/atomdog/oslo/wiki/Spinning-things-up) guide on getting started
## Development
- [developer notes](devnotes.md) contains bi-weekly informal entries on progress
- the [jira](https://buspark.atlassian.net/jira/software/projects/OSLO/boards/25/roadmap) has a more formal log
## Resources & related reading
- [wiki](https://github.com/atomdog/oslo/wiki)
- why a local virtual assistant? [what is substitute software as a service?](https://www.gnu.org/philosophy/who-does-that-server-really-serve.html)
