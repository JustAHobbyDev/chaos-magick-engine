# Problem Frames log

Dated, numbered analyses of proposed software, in Jackson's Problem Frames vocabulary, made before design. Entries are never silently edited; a reassessment is a new entry or a dated addendum.

## Entry #1 — 2026-09-12 — The house's forum

Proposal: forum software for the house described in [design 014](014-the-house-and-its-demons.md): a members-only, mobile-first community that the funnel feeds, where The Confessor holds the creed, members confide, and offers are made. The operator's stated constraints: mobile first; traffic arrives from Instagram, TikTok, and YouTube Shorts; the audience is assumed mostly women on phones; native apps are a question.

### Domains

| Domain | Nature | Controlled by | Crosses the boundary | Machine may change it |
| --- | --- | --- | --- | --- |
| Members | Biddable | Themselves | In: taps, posts, replies, confidences, purchases, permissions. Out: rooms, teachings, readings, offers, notifications | No; it can only invite |
| Partners | Biddable | Themselves | In: their room's posts, referred members. Out: their room, their referral counts | No |
| The operator, Magister Null | Biddable | The operator | In: teachings and offers to post, prices, grants, moderation, fulfilment marks. Out: the record, reports, queues | No |
| The demons, through the engine | Biddable, operator-mediated | The engine under operator grant | In: artifacts (teachings, readings, offers, posts) carried by the operator. Out: the record exported as corpus and feedback | No; nothing crosses without a grant |
| Traffic sources (Instagram, TikTok, YouTube) | Causal, external, moving | The platforms | In: a visitor with a referral marker, opened in an in-app browser. Out: nothing | No |
| Phones and their browsers | Causal | Apple, Google, the member | In: viewport, install capability, push permission. Out: the rendered forum | No |
| App stores | Causal, external, moving | Apple and Google | Only if a native app exists: review, distribution, a mandatory share of digital sales, rules on external payment | No |
| Payment provider | Causal, external, contractual | The provider | In: payment events by webhook. Out: checkout requests | No |
| Fulfilment | Biddable and causal, external | The operator and a fulfilment service | In: shipment marks. Out: orders | No |
| Notification channels (push, email) | Causal, external | Platform and provider | Out: messages. In: delivery and opt-out | No |
| Data-protection law and platform terms | Lexical, external | Legislatures and platforms | Constrains what the record may hold and for how long | No |
| The creed and teachings | Lexical | The Confessor via the operator | In as posts, some sealed to a tier | Read only |
| The catalogue and prices | Lexical | The Scribe and The Oracle via the operator; prices by the operator | In as offers | Read only |
| **The member record** | Lexical, machine-owned | The machine; the operator reads it | Created from every member act: source, take, entry, posts, confidences, permissions, purchases, tier | Yes; it is the machine's |
| **Confidences** | Lexical, machine-held, member-authored, sensitive | The member, under permission | Private messages, reading requests, birth data | Held, read back, deleted on request |
| **Entitlements** | Lexical, machine-owned | Derived from payment events and operator marks | Which rooms, teachings, readings, and assets a member may see | Yes |

The last three are the machine's own. Everything above them exists independently. Conflating the member record with the traffic platforms' analytics, or entitlements with the payment provider's state, would be the costly mistake here: the machine must own its record and derive entitlements, not lean on someone else's.

### Frame split

The proposal is seven frames, not one.

| # | Frame | Shape | Domains |
| --- | --- | --- | --- |
| A | Entrance | Transformation then Simple Workpieces | Traffic sources, phones, members, the member record |
| B | Rooms | Commanded Behaviour with Simple Workpieces | Members, partners, operator, creed and teachings, entitlements |
| C | Confidence channel | Simple Workpieces, high sensitivity | Members, operator, confidences, data-protection law, the demons via bridge |
| D | Offers and purchases | Commanded Behaviour over an external causal domain | Members, operator, catalogue, payment provider, fulfilment, entitlements |
| E | The record | Information Display over a machine-owned lexical domain | Operator, member record |
| F | Engine bridge | Transformation, operator-mediated | Demons, operator, creed, catalogue, member record, confidences |
| G | Re-engagement | Required Behaviour over notification channels | Members, phones, notification channels, member record |

A, B, D, and G are commodity: creator-membership platforms do them. C, E, and F are the house's own, and no platform does them in the house's terms.

### Requirements

**A. Entrance.** A visitor arriving from a source with a referral marker, in that platform's in-app browser on a phone, receives the free thing within one screen and can become a member with a single identity step. The source is recorded on the member from the first tap. Out of scope: anything the visitor must read for more than a screen; account creation before the free thing.

**B. Rooms.** A member on a phone can read the rooms their tier admits them to, post, reply, and react with one hand; the Confessor's teachings appear as posts, some sealed to a tier; partners have rooms of their own with their referred members visible to them; the operator can remove, pin, and mute. Out of scope: real-time chat as the primary form; threaded desktop discussion; public rooms visible without membership.

**C. Confidence channel.** A member can confide privately: a message to the house, a reading request, birth data for a reading. What is confided is visible only to that member and the house's Keeper, the operator; it is used only to read that member and to offer them what fits; it is read by the house's demons only under a permission that says a model reads it; it is deleted on the member's request and by a stated schedule otherwise. Out of scope: member-to-member private messaging in the first version; any use of a confidence outside the member's own readings and offers.

**D. Offers and purchases.** An offer is shown to the member it fits, by tier and by what they have shown they want; a purchase completes through the payment provider; entitlements follow confirmed payment and nothing else; the operator sets prices and marks fulfilment. Out of scope: the machine deciding prices; entitlement before confirmation; selling digital memberships through an app store's in-app purchase.

**E. The record.** The operator can see, per member and in aggregate, the path from source through take, entry, posts, confidences given, purchases, and tier, and can export it. Out of scope: analytics about non-members; anything assembled from outside what the member did inside the house.

**F. Engine bridge.** A demon's artifact reaches the forum only through the operator's grant, posted under the house's mask with the demon's authorship recorded internally; the record leaves the forum for the engine only within each member's permission, with confidences excluded unless their permission covers a model reading them. Out of scope: demons posting or reading directly; any automatic publication.

**G. Re-engagement.** A member who has opted in is told, on their phone, when something they would return for exists: a reply, a reading, a sealed teaching for their tier, an offer that fits. Out of scope: notifications to members who did not opt in; frequency set by anyone but the operator.

### Invariance test

- **Traffic sources: moving, and the frames do not lean on them.** Link rules, in-app browsers, and referral parameters change without notice. Frame A depends on them only for a visitor with a marker, and records source as "direct" when the marker is missing. Passes because the dependence is minimal and observable.
- **App stores: moving, unobservable, and a native app would lean on them for the main revenue line.** Store rules on the share taken from digital subscriptions and on external payment links have changed several times in the last three years and differ by jurisdiction; review outcomes cannot be predicted. Memberships are the recurring line of the business. A native app as the primary vehicle fails this test: it aims the business's core at a policy that moves and cannot be seen to move. It does not fail for a later native app that sells nothing in-app and exists for push and presence, once retention justifies it.
- **Payment provider: contractual, observable through webhooks.** Passes.
- **Phones and browsers as a platform for an installable web app: stable enough.** Home-screen installation and web push on both major phone platforms have been supported for several years. Passes, with the caveat that iOS requires installation to the home screen before push, which frame G must design for.
- **The demons: model behaviour moves.** Frame F does not lean on it; the operator's grant is between the demon and the forum. Passes.

### Stakeholder test

The word "forum" borrows from Discourse, phpBB, and Reddit. Their originating stakeholder was a desktop reader of threaded text discussion, moderated by volunteers, with no purchase and no private confession; Discourse's own founding account describes civilized long-form discussion for desktop communities in 2013. The house's stakeholder is a phone user who arrived from a thirty-second vertical video, expects a feed and a tap, and will buy. The pattern does not transfer, and the name should not carry its assumptions into the build: threaded desktop discussion is out of scope above for that reason.

The nearer analogy is the creator-membership community: Patreon, Substack, Mighty Networks, Circle, Skool. Their originating stakeholder is a creator selling tiers to a mobile audience, with posts, rooms, DMs, payments, and apps. That stakeholder matches the operator's on frames A, B, D, and G. It does not match on C, E, and F: those platforms have no confidence channel with permission-scoped use, no funnel record keyed from source to purchase that the operator owns and exports, and no bridge to an engine. The test therefore says: borrow the creator-community shape for the commodity frames, and build the three house frames, rather than either building a forum from scratch or trusting a platform with what it was never built for.

### Open questions — decided here, with reasoning

- **Missing referral marker:** source recorded as "direct"; the visitor is still served. A member is never refused for arriving without provenance.
- **The free thing before or after identity:** before. The first screen gives; the second asks for one identity step (email or a platform sign-in). Asking first loses the visitor the video sent.
- **Partial or pending payment:** no entitlement until the provider confirms. A pending purchase is shown to the member as pending, never as owned.
- **Payment provider unreachable:** checkout fails visibly; nothing is queued as owned; the operator sees the failure in the record.
- **Birth data:** stored only with an explicit reading request, shown to the member as stored, deleted after the reading unless the member keeps it. Sensitive by its nature and, combined with name and email, identifying.
- **Confidence deletion:** hard deletion on request within a stated window the operator sets; readings already delivered to the member are theirs and stay unless they delete those too.
- **A model reads confidences:** disclosed at the confidence channel and in the terms, as its own permission. A member who declines can still confide; the operator reads, the demon does not.
- **Who owns the record's lifecycle:** the machine creates it, the operator owns it, the member can see their own and ask for its deletion. Export to the engine is a copy under permission, never the record itself.
- **Age:** members are adults. Readings, payments, and the confidence channel all argue for it.
- **Notification cadence:** set by the operator per kind, defaulting to only what a member would return for. The demons may propose, never send.
- **Native apps now:** no, by the invariance test. An installable web app first; a native app later, selling nothing in-app, if retention data says presence on the home screen and reliable push are worth the store dependence.
- **Audience assumptions (mostly women, mostly phones):** treated as assumptions to verify from the record's source and device fields, not as facts the build depends on. The mobile-first decision does not rest on them; it rests on where the traffic comes from.

### Carried forward

The specification in [design 016](016-the-forum.md) follows this split. Frames C, E, and F are built by the house; A, B, D, and G are taken from a creator-membership platform in the first phase and rebuilt only when its limits bite. Reassess when a domain changes: a native app, member-to-member messaging, a demon faculty that reaches the forum directly, or a second payment or fulfilment provider.
