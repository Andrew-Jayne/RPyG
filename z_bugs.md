## Critical

Double Strike ignores the second part of the attack 

If there is only 1 enemy and it dies to the first attack from double strike, the game softlocks then throws an out of range error, need to have a better exit condition there.

## Major

Seems to be an edge case where an enemy killed by thunderball will have 0 health but not be dead

## Minor
When trying to dismember an enemy where is_dismembered == True, there is no error inidcating why you can not do it



## Trivial
