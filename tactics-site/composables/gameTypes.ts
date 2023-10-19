export interface Token {
  name: string
  imageUrl: string
  backImageUrl?: string
  text?: string
  size?: number
}

export interface Figurine {
  name: string
  imageUrl: string
  size: number
}

export interface Ability {
  name: string
  text: string
}

export interface Passive extends Ability {
}

export interface Active extends Ability {
}

export interface Card {
  name: string
  tokens?: Token[]
  whiteDice?: number[]
}

export interface UnitCard extends Card, Figurine {
  speed: number
  health: number
  passives?: Passive[]
  default_abilities?: Active[]
}

export interface Hero extends UnitCard {
  description: string
}

export interface RulesCard extends Card {
  text: string
}

export interface AbilityCard extends Card {
  text: string
}

export interface Deck {
  abilities: AbilityCard[]
  units: UnitCard[]
}

export interface HeroDeck extends Hero, Deck {
}

export interface RulesDeck {
  cards: RulesCard[]
}

export interface GameMap {
  name: string
  imagePath: string
  rules?: RulesCard[]
  tokens?: Token[]
  size_?: [number, number]
}

export interface GameSet {
  name: string
  description: string
  rules: RulesCard[]
  heroes: HeroDeck[]
  maps: GameMap[]
}

export interface Game {
  rules: RulesCard[]
  sets: GameSet[]
}

export type HeroImpression = 'Terrible' | 'Great'

export interface HeroReport {
  name: string
  version?: string
  note?: string
  impression?: HeroImpression
}

export interface GameReport {
  redScore?: number
  blueScore?: number
  redHeroes: HeroReport[]
  blueHeroes: HeroReport[]
  map?: string
  note?: string
}
