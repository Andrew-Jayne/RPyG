Need to merge and disolve the message and interaction classes, into a CoreIO module to handle input & output in an abstract context rather than the tight termial coupling.

all the code is there it just needs to be better.

think like a classic API

the UI is there for presentation, but it never creates data, and the data should not be opinonated on HOW it is displaed but should include enough data to let an interface understand how it SHOULD be displayed.