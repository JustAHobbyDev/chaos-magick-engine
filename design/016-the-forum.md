# The forum: a mobile-first specification

Status: proposed specification, following [Problem Frames entry #1](PROBLEM_FRAMES.md). Version 0.1.
Date: 2026-09-12.
Related design: [the house](014-the-house-and-its-demons.md), [The Confessor](013-the-confessor.md), [The Herald](015-the-herald.md).
Scope: what the house's members-only community must do, what is built and what is bought, the mobile decisions, the data it holds and under what permission, and how it meets the engine. Nothing here is implemented.

## What it is

A members-only community on the phone, entered from a short-video feed, where a member takes a free thing, joins a room, is read back to through the creed, and is offered what fits. It is a creator-membership community in shape, not a forum in the desktop sense: feed-first, tap-first, one-handed, with rooms rather than threads and sealed teachings rather than archives. The name "forum" stays as the house's word for it; the desktop assumptions do not come with it.

## Build and buy

The Problem Frames analysis found seven frames, four of them commodity and three the house's own. The first phase buys the four and builds the three.

| Frame | First phase | Later |
| --- | --- | --- |
| A Entrance | Built: a house landing service, since it must carry the source marker into the record | Same |
| B Rooms | Bought: a creator-membership platform with rooms, tiers, posts, reactions, moderation, and an API or export | Rebuilt in the house's own app if the platform's fees, data access, or brand limits bite |
| C Confidence channel | Built | Same |
| D Offers and purchases | Bought: the platform's tiers and checkout, with a house-controlled catalogue and prices; the payment provider's webhooks feed entitlements | Own checkout when volume or product mix justify it |
| E The record | Built: the house owns it from day one | Same |
| F Engine bridge | Built, operator-mediated | Automated per demon faculty grants, when the engine has them |
| G Re-engagement | Bought: the platform's push and email; the house's installable web app adds home-screen push | Same |

Platform selection criteria, in order: sells tiers on the web rather than through app-store purchase; exposes members, posts, and purchases through an API or scheduled export; allows the house's own landing page as the entrance; supports per-tier sealed content; has a usable installed web app or, failing that, a native app the house does not depend on for revenue. A platform that fails the first or second criterion is out.

## Mobile

The traffic comes from Instagram, TikTok, and YouTube Shorts, so the first screen is met in those platforms' in-app browsers on a phone held in one hand. Decisions that follow:

- **Installable web app, not a native app, in the first phase.** It installs to the home screen, opens full-screen, and can send push once installed. It sells memberships on the web, outside app-store purchase, which is the reason not to lead with a native app: the stores take a share of digital subscriptions sold in-app and their rules on external payment change without notice. A native app comes later, if retention data says home-screen presence and reliable push are worth it, and it sells nothing in-app when it does.
- **The first screen gives.** The free thing loads within one screen and before any identity step. In-app browsers are slow and interruptible; nothing may precede the gift.
- **One identity step.** Email or a platform sign-in, after the gift, to enter.
- **Install prompt after the second visit**, not the first, and never before the member has something to return for. On iOS the prompt explains the two taps to the home screen, because push is unavailable until then.
- **Vertical media.** Teachings, readings, and offers are laid out for a 9:16 screen: one idea per screen, swipe to continue, tap to reveal. Long text is chunked, not scrolled.
- **Thumb reach.** Primary actions sit at the bottom. Reactions, reply, and the confidence channel are one tap from any post.
- **Offline read.** The last teachings and the member's own readings are cached for reading without signal.
- **Performance budget.** First screen under two seconds on a mid-range phone over cellular; images sized for the screen they are shown on.

## Rooms and tiers

- **Rooms.** The open circle, where every member can read and post. Tier rooms, sealed to a tier. Partner rooms, one per partner, where that partner's referred members gather and the partner can post; the partner sees their own referral counts. Reading rooms, where members discuss readings without disclosing their own data.
- **Tiers.** Set by the operator: open circle, inner circle, named orders as the creed develops. A tier admits rooms, sealed teachings, reading discounts, and early offers. Ascension is a purchase of the next tier.
- **Posts.** Text with an image or short video, reactions, replies. The Confessor's teachings are posts under the house's mask, pinned, some sealed. A sealed teaching shows its title to lower tiers with the tier that unlocks it.
- **Moderation.** The operator removes, pins, mutes, and bans. Members report. Partners moderate their own rooms within the operator's rules.

## The confidence channel

The house's own build, and the most sensitive thing it holds.

- **What it is.** A private channel from a member to the house: a message, a reading request with the data the reading needs, or an answer to a sealed teaching's question.
- **Who sees it.** The member and the operator as Keeper. A demon reads it only if the member's permission covers a model reading it; the channel says this in plain words when the member first opens it, and the terms say it again.
- **What it is for.** Reading that member back through the creed, and offering that member what fits. Nothing else. It is not shared with partners, other members, or anyone outside the house, and it is never assembled with anything from outside the house.
- **Birth data.** Entered only with a reading request, shown to the member as stored, deleted after delivery unless the member keeps it for the next reading.
- **Deletion.** A member deletes any confidence at any time; the house completes hard deletion within the window the operator states. Readings already delivered stay with the member unless they delete those too.
- **Retention.** The operator states a retention schedule for confidences not otherwise deleted, and the machine enforces it.

## Offers and purchases

- **Catalogue.** Memberships by tier, readings by kind, digital assets, physical objects, and ascension products, each with a price set by the operator. The catalogue's text comes from The Scribe and The Oracle through the operator; prices never come from a demon.
- **Placement.** An offer appears to the member it fits: after a reading, the rite that continues it; after a sealed teaching, the tier above; after a confidence about a question, the reading that answers it. Placement rules are the operator's and may be proposed by The Confessor.
- **Checkout.** On the web through the payment provider. Confirmed payment events, and nothing else, grant entitlements: rooms, teachings, downloads, a reading in the queue, an order for fulfilment.
- **Fulfilment.** Digital assets deliver on entitlement. Readings enter the Oracle's queue through the bridge and return through it. Physical objects create an order the operator or a fulfilment service completes and marks.
- **Honesty.** What is sold is named as sold. A reading is offered as practice and entertainment, with the operator's standing disclaimer attached to every reading product.

## The record

The house's funnel instrument and the operator's own.

- **Per member.** Source and referral marker, device class, the free thing taken, entry time, tier and its history, rooms joined, posts and reactions, confidences given (as counts and dates; contents stay in the channel), readings requested and delivered, purchases, permissions granted and withdrawn, notification opt-in.
- **Aggregate.** The funnel by source and by partner: noticed, took, entered, trusted, bought, ascended, returned. Retention by tier. Offer placement to purchase.
- **Ownership.** The machine creates it; the operator owns it; a member sees their own and can ask for deletion; partners see their referral counts and nothing about individuals.
- **Export.** Scheduled export for the operator and, under permission, for the engine bridge. The export is a copy; the record never leaves.

## The engine bridge

Operator-mediated in the first phase, because the engine has no external faculties and the house design keeps publication under grant.

- **Inbound.** A demon's artifact, exported from its store, becomes a draft in the forum's queue: a teaching, a reading, an offer text, a room post. The operator publishes it under the house's mask or declines. The forum records the demon and artifact version as internal authorship; public attribution is the mask's.
- **Outbound.** The record's aggregate and, per member and under permission, the member's activity and confidences, exported as corpus and feedback for the demon whose working needs it: The Confessor for the rooms, The Oracle for a reading, The Herald for entry by source. Confidences cross only under the model-reads permission.
- **Later.** When the engine gains a forum faculty, the same two queues become its inputs and outputs; the operator's grant moves from each item to a standing rule.

## Re-engagement

- **Opt-in.** Push after install, email at entry, each its own permission.
- **What is sent.** A reply to the member, a reading delivered, a sealed teaching for their tier, an offer placed for them, a partner room event. Nothing else without the operator adding a kind.
- **Cadence.** Per kind, set by the operator. Demons may propose a message; the forum sends only what the operator's rules allow.

## What this does not settle

The platform chosen for the commodity frames. The house's name and visual identity. Prices and tiers. The retention window for confidences and the deletion window. Whether partner rooms are in the first phase or the second. The jurisdiction whose data-protection rules the house designs to first. Whether the audience is in fact mostly women on phones, which the record will show within the first month of entrances.
