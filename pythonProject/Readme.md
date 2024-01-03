## Run
To run the program execute:
`python3 fifa-review.py --match 'resources/partido.json' --rules 'resources/rules.json'`

If you want to try with several matches using brasil_1950:
`python3 fifa-review.py --match '../brasil_1950/brasil_spain.json' '../brasil_1950/brasil_sweden.json' '../brasil_1950/brasil_uruguay.json' '../brasil_1950/sweden_spain.json' '../brasil_1950/uruguay_spain.json' '../brasil_1950/uruguay_sweden.json'
'`

The first parameter are the matches played and the second one a list of the rules
. If no rules are given the standard footbal rules are used.