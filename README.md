# MDA shifts           
## Introduction: 
As a volunteer in MDA (the israeli rex cross) in my station every volunteer could request to be assigned to a shift, happily the station has a not small amount volunteers, and sadly we have a lot of work, so we need many shifts around the clock, and for the shifts there is a need for volunteers. I realized that it could take a few days since the last time people could sign up to shifts, until they publish a schedule, this means some people in MDA are spending important life saving time to deal with this.
Another problem, if many people want a shift, for example on weekends more people volunteer, to who to give the shift, this could be very not fair sometimes, and human error could be not nice to some people (even though everyone here what to give and be nice)
## solution:
Instead to let people deal with, let the code do the job, and create a algorithm that will give the **maximum amount of shifts to maximum amount of volunteers**, this will mean more shifts will have more volunteers, and more lives will be saved.        
### the algorithm:
1) loop over all shifts, and give the volunteers with least amount of shifts the shift
2) loop over all shifts, and if there is volunteers that did not get the shift, try exchanging his with the volunteer that got the shift that has the most amount of shifts in the month. If this lowers the standard division of the list of number of shifts that each volunteer got, so switch between the volunteers.
3) do stage 2 until the standard division does not shrink.
## support
Any ideas for upgrading this project will be welcomed, you could contact me by [mail](mailto:yalovbader@gmail.com)  

