:- dynamic position/4.
:- dynamic wields_weapon/2.
:- dynamic health/1.
:- dynamic has/3.
:- dynamic stepping_on/3.
:- dynamic unsafe_position/2.

action(attack(Direction)) :- position(agent, _, AgentR, AgentC), position(enemy, _, EnemyR, EnemyC),
                             is_close(AgentR, AgentC, EnemyR, EnemyC),  healthy,
                             next_step(AgentR, AgentC, EnemyR, EnemyC, Direction).

action(move_towards_enemy(Direction)) :- position(agent, _, AgentR, AgentC), position(enemy, _, EnemyR, EnemyC),
                                        next_step(AgentR, AgentC, EnemyR, EnemyC, D), healthy,
                                        safe_direction(AgentR, AgentC, D, Direction).

action(run(OppositeDirection)) :- position(agent, _, AgentR, AgentC), position(enemy, _, EnemyR, EnemyC),
                                  is_close(AgentR, AgentC, EnemyR, EnemyC),  \+ healthy,
                                  next_step(AgentR, AgentC, EnemyR, EnemyC, Direction),
                                  opposite(Direction, OD), safe_direction(AgentR, AgentC, OD, OppositeDirection).

action(drink) :- has(agent, potion, health), \+ healthy.

action(pick) :- is_pickable(P), stepping_on(agent, P, health).

action(move_towards_potion(Direction)) :-   position(agent, _, AgentR, AgentC),  position(potion, health, PotionR, PotionC),
                                            next_step(AgentR, AgentC, PotionR, PotionC, D),
                                            safe_direction(AgentR, AgentC, D, Direction). \+ healthy.

% -----------------------------------------------------------------------------------------------

% test the different condition for closeness
% two objects are close if they are at 1 cell distance, including diagonals
is_close(R1,C1,R2,C2) :- R1 == R2, (C1 is C2+1; C1 is C2-1).
is_close(R1,C1,R2,C2) :- C1 == C2, (R1 is R2+1; R1 is R2-1).
is_close(R1,C1,R2,C2) :- (R1 is R2+1; R1 is R2-1), (C1 is C2+1; C1 is C2-1).

% the agent can perform "dangerous" actions - e.g. attack a monster - if its health is above 50%
healthy :- health(H), H > 50.

% compute the direction given the starting point and the target position
% check if the direction leads to a safe position
% D = temporary direction - may be unsafe
% Direction = the definitive direction 
next_step(R1,C1,R2,C2, D) :-
    ( R1 == R2 -> ( C1 > C2 -> D = west; D = east );
    ( C1 == C2 -> ( R1 > R2 -> D = north; D = south);
    ( R1 > R2 ->
        ( C1 > C2 -> D = northwest; D = northeast );
        ( C1 > C2 -> D = southwest; D = southeast )
    ))).
    % safe_direction(R1, C1, D, Direction).

% check if the selected direction is safe
safe_direction(R, C, D, Direction) :- resulting_position(R, C, NewR, NewC, D),
                                      ( safe_position(NewR, NewC) -> Direction = D;
                                      % else, get a new close direction
                                      % and check its safety
                                      close_direction(D, ND), safe_direction(R, C, ND, Direction)
                                      ).

% a square if unsafe if there is a trap or an enemy
unsafe_position(R, C) :- position(wall, _, R, C).
unsafe_position(R, C) :- position(trap, _, R, C).
unsafe_position(R, C) :- position(enemy, _, R, C).
unsafe_position(R, C) :- position(enemy, _, ER, EC), is_close(ER, EC, R, C), \+ healthy.

%%%% known facts %%%%
opposite(north, south).
opposite(south, north).
opposite(east, west).
opposite(west, east).
opposite(northeast, southwest).
opposite(southwest, northeast).
opposite(northwest, southeast).
opposite(southeast, northwest).

resulting_position(R, C, NewR, NewC, north) :-
    NewR is R-1, NewC = C.
resulting_position(R, C, NewR, NewC, south) :-
    NewR is R+1, NewC = C.
resulting_position(R, C, NewR, NewC, west) :-
    NewR = R, NewC is C-1.
resulting_position(R, C, NewR, NewC, east) :-
    NewR = R, NewC is C+1.
resulting_position(R, C, NewR, NewC, northeast) :-
    NewR is R-1, NewC is C+1.
resulting_position(R, C, NewR, NewC, northwest) :-
    NewR is R-1, NewC is C-1.
resulting_position(R, C, NewR, NewC, southeast) :-
    NewR is R+1, NewC is C+1.
resulting_position(R, C, NewR, NewC, southwest) :-
    NewR is R+1, NewC is C-1.

close_direction(north, northeast).
close_direction(northeast, east).
close_direction(east, southeast).
close_direction(southeast, south).
close_direction(south, southwest).
close_direction(southwest, west).
close_direction(west, northwest).
close_direction(northwest, north).

has(agent, _, _) :- fail.

unsafe_position(_,_) :- fail.
safe_position(R,C) :- \+ unsafe_position(R,C).

is_pickable(potion).