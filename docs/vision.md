# Vision & Motivation

## The Problem

Social media platforms, particularly Reddit, are increasingly vulnerable to coordinated inauthentic behavior. Groups of accounts (whether bot networks, paid actors, or coordinated campaigns) can create the illusion of grassroots consensus on political, commercial, or social issues.

This "synthetic consensus" distorts public discourse and can:
- Manipulate public opinion
- Suppress genuine dissenting voices
- Artificially amplify fringe viewpoints
- Damage trust in online communities
- Influence real-world decisions and policies

## Why Reddit?

Reddit's structure makes it particularly susceptible to consensus manipulation:

1. **Voting systems**: Coordinated upvoting can push narratives to the top
2. **Anonymity**: Easy to create multiple accounts
3. **Influence**: Popular subreddits shape mainstream conversation
4. **Trust**: Users often assume consensus reflects genuine opinion

## Current Gaps

Existing solutions have limitations:

- **Platform-native tools**: Limited transparency, slow response
- **Simple heuristics**: Easy to game (account age, karma, etc.)
- **Manual review**: Doesn't scale
- **Keyword filtering**: Misses semantic coordination

## Our Approach

**ConsensusWatch** uses advanced NLP and network analysis to detect coordinated behavior patterns that simple metrics miss:

- **Semantic similarity**: Identifies coordinated messaging even when wording differs
- **Temporal patterns**: Detects suspicious timing and burst behaviors
- **Network graphs**: Maps coordination between accounts
- **Explainable AI**: Provides human-readable rationales, not just scores

## Goals

### Primary Goal
Provide researchers, journalists, and platform users with **transparent, explainable tools** to identify potential consensus manipulation.

### Secondary Goals
- Open-source methodology for community scrutiny
- Educate users about manipulation tactics
- Pressure platforms to improve detection
- Advance research in coordinated inauthentic behavior

## Non-Goals

This tool is **not**:
- A definitive "bot detector" (results are probabilistic)
- A harassment tool (no doxxing or account targeting)
- A replacement for platform moderation
- Perfect or infallible (see [limitations.md](limitations.md))

## Use Cases

1. **Researchers**: Study manipulation campaigns and platform dynamics
2. **Journalists**: Investigate suspicious consensus on news stories
3. **Moderators**: Identify potential brigading or coordination
4. **Users**: Critically evaluate thread consensus before forming opinions
5. **Platform teams**: Supplement internal detection systems

## Ethical Considerations

We believe in:
- **Transparency**: Open-source methodology subject to peer review
- **Responsible disclosure**: Report findings constructively
- **Privacy**: Analyze public data only, respect user privacy
- **Humility**: Acknowledge limitations and uncertainty
- **Harm reduction**: Prevent misuse for harassment

## Success Metrics

This project succeeds if it:
1. Accurately identifies coordinated behavior (validated against known cases)
2. Empowers users to think critically about online consensus
3. Contributes to academic understanding of social media manipulation
4. Inspires platform improvements
5. Remains open, accessible, and ethically grounded

## Long-Term Vision

Beyond this MVP:
- Multi-platform support (Twitter, Facebook, etc.)
- Real-time monitoring and alerts
- Community-driven dataset of known manipulation campaigns
- Integration with browser extensions
- Advanced pattern recognition (LLM-generated content, deep fakes)
- Collaborative platform with researchers worldwide

---

**We believe informed, critical engagement with social media is essential for democratic discourse. This tool is one small step toward that goal.**
