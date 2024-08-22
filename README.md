# MDA shifts           
## Introduction: 
As a volunteer in MDA (the israeli red cross) by my station every volunteer could request to be assigned to a shift, happily the station has a not small amount volunteers, but sadly we have a lot of work, so we need many shifts around the clock, and for the shifts there is a need for volunteers, and more happy volunteers is better. I realized that it could take a few days since the last time people could sign up to shifts, until they publish a schedule, this means some people in MDA are spending important life saving time to deal with this.
Another problem, if many people want a shift, for example on weekends many more people volunteer (this is not a remondations to get injured on weekends :), to decide who gets the shift could be very not fair sometimes, and human error could be not nice to some people (even though everyone here what to give and be nice)
## solution:
Instead to let people deal with scheduling volunteers to shifts, let the code do the job, and create a algorithm that will give the **maximum amount of shifts to maximum amount of volunteers**, this will mean more shifts will have more volunteers, and more lives will be saved.        
### the algorithm:
General point, a volunteer could not two shifts one after each other, because many time shifts don't end on time, and they must begin on time.
1) loop over all shifts, and give the volunteers with least amount of shifts the shift
2) loop over all shifts, and if there is volunteers that did not get the shift, try exchanging him with the volunteer that got the shift that and has the most amount of shifts in the month. If this lowers the standard division of the list of number of shifts that each volunteer got, so switch between the volunteers.
3) do stage 2 until the standard division does not shrink.
## support
Any ideas for upgrading this project will be welcomed, you could contact me by [mail](mailto:yalovbader@gmail.com)  
