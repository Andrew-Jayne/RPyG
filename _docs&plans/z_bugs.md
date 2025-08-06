## Critical

## Major
When trying to dismember a dismembered enemy if they are the only living target you have to select them 10 times untill the dumb check uses attack()
    - can be fixed by checking how many living targets are not dismemebred and if it is 0 then return to the user propmt or default attack
    - results in a softlock/exploit because you never exit the dumb check loop, and you attack a dead opponent forever

## Minor


## Trivial

## UI Problems