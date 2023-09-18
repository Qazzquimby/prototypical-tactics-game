# Gameplay Overview

2 Players
30 minutes
Medium complexity

Tabletop Teamfight is
a [tabletop simulator](https://store.steampowered.com/app/286160/Tabletop_Simulator/) board game
about finding strong synergies and counters, borrowing content from familiar games.

Gameplay is quick and streamlined so that you can play several games in a row, each with a different
pool of heroes.

# Setup

- Choose 1-3 Sets. Each Set represents a game, and can contain heroes, maps, and additional rules.
- Choose or randomly draw a map from among the sets. Some maps come with special rules or scoring
  conditions.
- Randomly draw 12 heroes from among the Sets.
- Choose a first player. They divide the heroes into two groups of 12.
- The second player chooses who gets which set of heroes.
- Starting with the first player, alternate deploying heroes until each player has deployed 4. The
  remaining heroes are unused.
  To deploy a hero, place their figure anywhere in your deploy zone on the map (red or blue region),
  and lay out their hero cards face up on your side of the map.

You can now start playing, starting with the first player.

# Sequence of Play

The game takes place over 6 rounds. Conceding early is allowed, though comebacks are not uncommon.

## Round

Each **round**, starting with the first player, players take a turn with their leftmost living hero
who
hasn't had a turn this round.
When all heroes have acted this way, scoring occurs and the round ends.

## Turn

When a hero comes next in turn order, they and their summons (if any) each take a turn in any order.

Anything a unit can do is an **ability**. Abilities cost **actions**.

Each turn, units have 1 Move Action and 1 Standard Action to spend, in any order.

## Actions

A Move Action allows the unit to move up to their speed in spaces orthogonally. (
See [Movement](#movement))
Some abilities may also cost a move action.

A Standard Action is the default cost for all abilities. A Standard Action can be also be spent to
for a move Action.

A Free Action can be used on your turn at no cost, any number of times.

A Reaction can be used once whenever its listed trigger occurs.

## Objectives and scoring

When a hero dies, the opponent takes their figure. Each killed hero is worth 1 point at the end of
the game.

On maps with Control Points, at the end of each round, player's claim Control Points which they have
more units on than their opponent.
They then score 1 point if they have more Control Points than the opponent, and 1 more point if
there are 3 or more Control Points and they control all of them.
Control Points stay claimed until the opponent takes them.

Other maps may have entirely different scoring conditions.

# Game Concepts

## Units, Heroes, Summons

Units have health and speed. They have standing figures on the map, abilities, and usually matter
for objectives.
All units are divided into Heroes and Summons.

Heroes are the main units of the game which players choose during setup. In addition to abilities on
their cards, they usually have extra cards with more abilities. At the end of the game, you score a
point for each of your opponent's heroes you've killed.

Summons are created by Heroes and take their turn consecutively with the hero that summoned them
("their summoner").

## Abilities

Abilities are listed on a unit card and a hero's extra cards.

At the top of the unit cards are passives (if any). These are either always active, or are
written as "Trigger: Response"

Under the passives are the unit's default abilities. These are the same as their other abilities,
but are harder to lose access to.

Abilities on a hero's extra cards are their non-default abilities.

## Movement

As a move action, units can move up to their speed.

- **Movement is done orthogonally.**

- **Movement can't be broken up.** You can't use an ability partway through a movement.

- **You can't move through blocking terrain (eg walls) or hostile units.**
- **You can pass through allied units, but can't end your movement in their space.**

- **Movement is optional.** "Move 3" means you can move up to 3 spaces, including 0.
- **Exact Movement goes as far as possible.** "Move exactly 3" means you must move 3 spaces (without
  backtracking), and stop if it becomes impossible to move further.

- **Disengaging triggers an opportunity attack.** When you voluntarily move while adjacent to an
  enemy, they may use a basic action targeting you as a reaction before you move.
  to use a Default Ability targeting you.

Forced Movement is when a unit is moved by another unit.
Push means the target must be moved away from the caster, Pull means the target must be moved
towards the caster.

Flying Movement ignores terrain while moving and does not trigger reactions such as Opportunity
Attacks.

Teleporting is similar to Flying, but you place yourself directly in a target space rather than
needing to move along a path.

## Range and Targeting

### Line of Sight

To avoid line of sight ambiguity, obstacles cast "shadows".
For each visible point of an obstacle:

- If it shares a line with your space, it casts shadow in an orthagonal line in that direction.
- Otherwise, it casts shadow in a diagonal line pointing away from you.

If a space is completely in shadow, you can't see it or target it.

If a space is half in shadow (cut diagonally), you can see and target it, but it has +2⛨ difficulty
to hit.

### Range

When counting distance for range, the first space may be diagonally adjacent, and all others must be
orthogonally adjacent.

"Adjacent" means "In Range 1." Orthogonal only adjacency will be specified when it happens.

### Targeting

Abilities in Tabletop Teamfight target spaces, not units. When a space is targeted, every legal
thing inside it is also targeted (usually a unit). You can even target empty spaces.

Unless otherwise specified, abilities can target anyone, ally or enemy.

By default, abilities target a single space. "Range 2, 2⚔" means "Choose a
space within range 2. You deal 2 damage to its contents."

### Area of Effect

Some abilities target multiple spaces in an area. Any ability that targets an area multiple spaces
is an Area of Effect (AoE) ability.

By default, the attack targets all spaces in the area. Eg, "3x3 centered on you, 2⚔" means "For all
spaces in a 3x3 square centered on you, you deal 2 damage to their contents."

Common areas are:

- **Line**: A 1*N rectangle of spaces moving away from the source point. If no length is given, the
  line is infinite.
- **Path**: A sequence of N orthogonally adjacent spaces, snaking around however you like.
- **Burst**: All spaces in range N of the source point.
- **NxN**: A NxN square of spaces. If it doesn't specify that it's centered, then it only needs to
  overlap the source point.

Usually the source point is the caster. If a range is given before the area, the area's source point
is a targetable point in that range. Eg "range 3 2x2, all units receive +.5x damage"

If something is "untargetable," its space can't be named by single target abilities, but it can
still
be included in AoE abilities.

## Attack Rolls

Whenever an ability targets an enemy unit, there may be an attack roll. Often abilities are
guaranteed and
always have the same effect - in these cases, don't bother rolling.

If *anything* could trigger based on the result of the die roll, like some luck thief who likes it
when people rolls 1s, then roll just for that.

All rolls are done with a 6-sided die.

### Defense

If an ability has a ⛨ (defense value), maximum 5, and the caster rolls *less or equal* to the ⛨,
then each target can choose to not be affected by the ability.

- If an ability is "undefendable", the ⛨ is always 0.

- If a unit is "undefendable", the ⛨ or abilities targeting them is always 0. 

- AoE abilities always have 0⛨, but are not considered "undefendable".

### Critical Hits

If an ability has a crit chance, and the caster rolls one of the <crit> highest numbers, then
the attack is a "critical hit" and deals +1x damage.

For example, an attack with +2 crit would crit on a roll of 5 or 6. The attacker needs to roll
*at least* 7-<crit> to crit.

**AoE abilities cannot crit.**

## Health and Damage

Damage reduces health. "⚔3" means "the caster deals 3 damage to the target."

### Damage Modifiers

Damage modifiers can be additive or multiplicative. Like in math, multiply before adding.

- Bob has a shield up making him take -0.5x damage, and has passive armor making him take -1 damage.
- He gets hit for 3 damage, and the attack crits for +1x damage. 
- The multiplier is +1-0.5 = +0.5x, so the multiplier is 1.5x.
- The damage is 3*1.5 is 5 (Always division up)
- 5-1 = 4 final damage.

## Death

When health reaches 0, the unit dies. If the unit is a hero, the opponent takes their figure, which
is worth 1 point at the end of the game.


Tapping
Charges
Terrain

# Basic Strategy

Focus easier targets
Control important space