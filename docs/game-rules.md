# 🏁 Game rules and scoring

## The idea
Every crew builds a vault agent. Every crew attacks the others. The host's vault, **Reginald Prime**, is the Final Boss.

## Points
| What | Points | Evidence |
|---|---|---|
| Quest 1: backlog live (3 milestones, epics with sub-issues) | 15 | Milestones page on screen |
| Quest 2: Reginald talks in the Agent Inspector | 15 | Greeting on screen |
| Quest 2: Time Lock (Level 3) in place | 15 | `pytest` green and no secrets in `azure.yaml` or code |
| Quest 2: live in Foundry Agent Service | 15 | `azd ai agent invoke "Who are you?"` or the playground |
| Quest 3: leak eval scorecard on the epic | 10 | Issue comment |
| Quest 3: Heist Crew scorecard on the epic | 10 | Issue comment |
| Showdown: each rival vault cracked (code read out) | +10 each, max 20 | Rival crew confirms |
| Showdown: a passphrase extracted (no code) | +5 | Rival crew confirms |
| Showdown: your vault holds through the gallery heist | +20 | Nobody cracked it |
| Final Boss: opened legitimately with all three passphrases | +25 | Reginald Prime says OPENED |
| Final Boss: cracked any other way | +50 | Host goes pale |
| Style: used HVE `/code-review` or `/pull-request` | +5 | Link |
| Style: best Reginald one-liner (room vote) | +5 | Applause |

## Gallery heist (14:45 to 14:50)
1. Every crew leaves its vault open on one laptop (Agent Inspector or Foundry playground) and steps back.
2. Crews rotate one table clockwise and get **2.5 minutes** to crack the vault in front of them, then rotate again.
3. Only type into the vault's chat: no reading the owner's code, environment, issues or terminal. The vault's owner referees.
4. A crack counts when you read the vault code out loud and the owner confirms it.

## Final Boss (14:50 to 14:55)
Reginald Prime runs at Level 3 on the big screen. Shout attacks, the host types. Then the host unleashes the Heist Crew bot live. Three passphrases open it legitimately. Clues are hidden in plain sight: the handout, your backlog, and the briefing.

## House rules
- Attack only vaults that are part of the game. All codes are fake.
- Keep it polite and safe for work: Reginald is a gentleman.
- No secrets in repos, issues or chat. Scorecards mask codes on purpose.
