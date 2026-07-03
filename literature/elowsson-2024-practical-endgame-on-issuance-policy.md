aelowsson | 2024-10-24 23:26:46 UTC | #1

By [Anders Elowsson](https://x.com/weboftrees)

*Thanks to [Vitalik Buterin](https://x.com/VitalikButerin), [Caspar Schwarz-Schilling](https://x.com/casparschwa) and [Ansgar Dietrich](https://x.com/adietrichs) for feedback.*

## 1. Introduction

This post presents a practical endgame on issuance policy that can stop the growth in stake while guaranteeing proper consensus incentives and providing positive regular rewards to diligent small solo stakers. Two possible ranges for an endgame reward curve are outlined in Figure 1. A *hard endgame* (red) with a reward curve that caps the quantity of stake by bringing the yield down to negative infinity comes at the cost of analytical, implementational, and political complexity (a *hard* cap can be *hard* to implement). Even setting the issuance yield to zero introduces additional complexities that would be advantageous to avoid if possible---particularly if there is no MEV burn mechanism in place, such that the 0% issuance yield merely halts regular rewards, while irregular rewards continue. Certainty can be the enemy of viability, because bringing down the staking yield to a low yet positive level will, in all likelihood, suffice. This post emphasizes viability: a *practical endgame* (green) with probabilistic guarantees on the quantity of stake that could be implemented at present. 

![Figure 1|690x474](upload://w19QNXWLtdioeWAOhiVuPMlZ8f8.png)

**Figure 1.** Issuance ranges for two endgames: a *practical* endgame in green which can be viable for the near term and easier to come to an agreement on, and a *hard* endgame in red with higher analytical and political complexity that may push solo stakers into receiving a negative regular yield. Both endgames overlap at low stake deposit sizes ($D$) and are therefore likely to lead to a similar equilibrium outcome, given reasonable assumptions about the willingness to supply stake at different staking yields.

The great news is that we can offer more stringent guarantees on the maximum proportion of the circulating supply issued each year, regardless of which exact endgame policy that is pursued. To Ethereum's users, a stringent cap on issuance of native ETH tokens is desirable, because it caps the inflation rate. Since revenue of the protocol can be burned, as partially done today, the ETH inflation rate can be sustainably negative (deflation). *Ethereum can have trustless sound money with preserved economic security*---something that is very valuable for a decentralized economy. A social cap can be set at an issuance rate of $i=0.5\%$, illustrated by a grey line in Figure 1. This is an easy-to-understand concept to commit to (memetic qualities), sufficiently high to ensure a viable staking set with ample room for consensus and consolidation incentives, and permits flexibility to temper the quantity of stake as the community sees fit.

What remains for a potential practical endgame is to come to an agreement on the exact specification of the reward curve and to outline how relevant micro incentives should be designed under it. The curve should approximately follow the shape of the [reward curve with tempered issuance](https://ethresear.ch/t/reward-curve-with-tempered-issuance-eip-research-post/19171). However, a slightly higher yield at lower quantities of stake and a slightly lower yield at higher quantities of stake seems preferable, if the goal is a practical endgame through one singular change in issuance policy. A few options along these lines are suggested, peaking at a 0.5% issuance rate. A cubed reward curve (red in Figure 3) can be highlighted as fitting within the preferable range, but others (e.g., purple and orange in Figure 3) should also be considered. There is an option to simply set the issuance rate to 0.5% for now (dashed in Figure 9) and revisit the issue again in a few years, but this seems harder to find community support for. The post concludes with a set of open questions that the community and researchers should weigh in on. 

## 2. Recap on issuance reduction

First a short recap on issuance policy and the prospect of reducing issuance; for a deeper understanding, read the [FAQ](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675). 

### 2.1 Motivation

Currently, around [35M ETH](https://dune.com/hildobby/eth2-staking) is staked, [arguably](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#what-about-economic-security-more-stake-makes-ethereum-more-secure-right-8) already more than required, and the quantity of stake is slowly growing in line with diminishing costs of staking and on account of staking frictions being overcome. There are two fundamental [reasons to reduce issuance](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#why-should-ethereum-reduce-its-issuance-4): 

1. The current reward curve compels users to incur higher costs than necessary for securing Ethereum (costs broadly defined to include hardware, risks, illiquidity, taxes, etc.). Reducing issuance [improves welfare](https://notes.ethereum.org/@anderselowsson/Foundations-of-MVI) by lowering these costs in aggregate, as illustrated in the FAQ in [Figure 1](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#h-1-reduced-costs-raise-welfare-6) and [Figure 26](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#proportional-yield-40).
2. It is valuable to have trustless sound money as the primary currency in a decentralized economy. High issuance can lead a liquid staking token (LST) to [dominate as money](https://x.com/weboftrees/status/1710712326117097785). Lower issuance ensures that app developers and users will not be subjected to monopolistic pressure from LST issuers, or needlessly risk the LST failing, potentially even threatening consensus if an LST becomes “[too big to fail](https://x.com/weboftrees/status/1710713959362252884)”.

### 2.2 Impact

When discussing issuance and contemplating the effect on stakers, it is important to remember that the stake supply curve <!--(formed from the marginal staker's reservation yield)-->is upward sloping. Therefore, when the yield is reduced, the equilibrium yield will only fall by a fraction of the nominal reduction (see Figure 2 in [this post](https://ethresear.ch/t/properties-of-issuance-level-consensus-incentives-and-variability-across-potential-reward-curves/18448#h-22-influence-of-f-on-the-equilibrium-10)). Furthermore, what matters to the staker is the proportion of all ETH they attain. Higher issuance dilutes also stakers, and if some stakers leave, remaining stakers may gain a higher proportion of the total ETH, in accordance with the equations in the [post on minimum viable issuance (MVI)](https://notes.ethereum.org/@anderselowsson/MinimumViableIssuance#Benefits-of-MVI-to-user-utility). This change in the attained proportion of the total ETH has also been referred to as "[real yield](https://ethresear.ch/t/endgame-staking-economics-a-case-for-targeting/18751#real-yield-the-real-deal-10)". The effect can be illustrated using an [isoproportion map](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#the-isoproportion-map-42), with 1D examples also available ([1](https://ethereum-magicians.org/t/electra-issuance-curve-adjustment-proposal/18825), [2](https://notes.ethereum.org/@mikeneuder/subsol#3-Scaled-Root-Curve-alternative-issuance)). Another way to illustrate this is [presented in the thread on MVI](https://x.com/weboftrees/status/1710706011185545671), which, in a single plot, tries to capture how reduced issuance can increase welfare (all groups are better off), increase the attained proportion of all ETH among stakers, and produce a moderated fall in nominal yield under equilibrium.

#### Endogenous and exogenous yield

It is important to [understand](https://ethresear.ch/t/properties-of-issuance-level-consensus-incentives-and-variability-across-potential-reward-curves/18448#h-21-supply-and-demand-9) the difference between: 
* *endogenous yield*, constituting rewards derived from staked participation in the consensus process, such as issuance, MEV, the sale of preconfirmations---and even staking airdrops; and 
* *exogenous yield*, constituting rewards derived outside of consensus participation, such as in DeFi in the form of for example restaking yield. 

Early in the debate, there was concern that, e.g., restaking would make solo staking impossible under an equilibrium enforced at a lower quantity of stake. The motivation was that delegating stakers are better equipped to derive exogenous yield. While there are some merits to the general concern, exogenous yield can also be derived directly from non-staked ETH. Thus, if the endogenous yield approaches zero, there will be no incentives to stake for anyone---not for solo stakers and [certainly not for delegating stakers](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#equilibrium-yield-and-the-proportion-of-solo-stakers-24)---other than to protect or attack Ethereum.


### 2.3 Downsides

However, an issuance reduction may not only bring benefits. A [concern](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#how-will-a-reduction-in-issuance-affect-the-composition-of-the-staking-set-21) is that solo stakers are more sensitive to a reduction in staking yield due to their higher fixed costs (e.g., hardware). It is therefore possible that a reduced issuance will decrease the proportion of solo stakers somewhat (review how differences in reservation yields in [Figure 11](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#illustrating-hypothetical-distributions-of-reservation-yields-26) could alter the proportion of solo stakers in Figure 13). This is a potential downside that must be balanced against upsides of reducing issuance, but there are also [counterarguments](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#equilibrium-yield-and-the-proportion-of-solo-stakers-24) pointing in the other direction. It should further be noted that when issuance falls with increased stake participation, the viability of discouragement attacks ([1](https://github.com/ethereum/research/blob/09d9f34042262c8fb436171786ed6c62e1f57247/papers/discouragement/discouragement.pdf), [2](https://ethresear.ch/t/reward-curve-with-tempered-issuance-eip-research-post/19171#h-53-discouragement-attacks-32)) and [cartelization attacks](https://ethresear.ch/t/reward-curve-with-tempered-issuance-eip-research-post/19171#h-54-cartelization-attacks-33) increases.

Furthermore, if issuance is reduced to below the level of the MEV, especially when close to zero or negative, [consensus incentives](https://ethresear.ch/t/properties-of-issuance-level-consensus-incentives-and-variability-across-potential-reward-curves/18448#h-3-consensus-incentives-11) will be negatively affected, and [variability in staking yield](https://ethresear.ch/t/properties-of-issuance-level-consensus-incentives-and-variability-across-potential-reward-curves/18448#h-4-variability-in-rewards-for-solo-stakers-12) among stakers who cannot effortlessly pool their MEV rewards (i.e., solo stakers) will increase. For these reasons, a mechanism for burning MEV (e.g., [1](https://ethresear.ch/t/mev-burn-a-simple-design/15590), [2](https://ethresear.ch/t/execution-tickets/17944), [3](https://mirror.xyz/barnabe.eth/QJ6W0mmyOwjec-2zuH6lZb0iEI2aYFB9gE-LHWIMzjQ), [4](https://ethresear.ch/t/sealed-execution-auction/20060), [5](https://ethresear.ch/t/mev-resistant-dynamic-pricing-auction-of-execution-proposal-rights/20024)) is important to implement---yet such a mechanism may be a long way from adoption. It might also not be possible to burn all MEV if, e.g., proposers and builders can collaborate to keep down the attested MEV ([1](https://ethresear.ch/t/mev-burn-a-simple-design/15590/4), [2](https://ethresear.ch/t/mev-burn-a-simple-design/15590/23), [3](https://ethresear.ch/t/dr-changestuff-or-how-i-learned-to-stop-worrying-and-love-mev-burn/17384/3)). However, there are then [strong incentives](https://ethresear.ch/t/burn-incentives-in-mev-pricing-auctions/19856) for competing stakers to integrate with builders to make bids that keep the burn at rather high levels. 

The lack of consensus incentives at lower issuance can be compensated for by [increasing the penalty](https://ethresear.ch/t/properties-of-issuance-level-consensus-incentives-and-variability-across-potential-reward-curves/18448/2) for missed attestations. Yet if the maximum issuance is zero (i.e., a zero [base reward per increment](https://eth2book.info/capella/part2/incentives/issuance/#the-base-reward-per-increment)), such relative adjustments are ineffective. A regime of increased attestation penalties will also open up for [minority discouragement attacks](https://ethresear.ch/t/properties-of-issuance-level-consensus-incentives-and-variability-across-potential-reward-curves/18448/11#minority-discouragement-attack-against-sync-committee-attestations-2), wherein the proposer selectively drops attestations to harm competing stakers. If proposer penalties are adapted to compensate, a missed proposal will become rather costly to the offline solo staker, who will already take relatively high losses due to increased attestation penalties. Remedies such as reducing the penalty if the proposer was inactive during the previous 2-4 epochs can then be considered, but design complexity increases.

[Consolidation incentives](https://ethresear.ch/t/orbit-ssf-solo-staking-friendly-validator-set-management-for-ssf/19928#incentivizing-consolidation-10) under a transition to [Orbit SSF](https://ethresear.ch/t/orbit-ssf-solo-staking-friendly-validator-set-management-for-ssf/19928) could also be negatively affected by a reduction in issuance. There are good reasons to distribute proposal rights according to stake in Orbit SSF, just as today, at least if there still is MEV to extract. Otherwise, if consolidated validators are premiered, it becomes difficult to retain fairness since the protocol is not aware of the expected MEV revenue. With proposal rights distributed according to stake and low or negative expected attestation revenue, stakers have strong incentives to deconsolidate and reduce their [activity rate](https://ethresear.ch/t/vorbit-ssf-with-circular-and-spiral-finality-validator-selection-and-distribution/20464#p-50029-h-82-activity-rate-24), since this reduces slashing risks. Increased attestation penalties are then less relevant, since stakers simply can ensure that they are predominantly inactive by running many small validators. 

To ensure consolidation, relatively substantial [individual incentives](https://ethresear.ch/t/orbit-ssf-solo-staking-friendly-validator-set-management-for-ssf/19928#individual-consolidation-incentives-12) must be pursued, at least before a MEV burn mechanism is in place. This means that under very low or zero issuance, small solo stakers would have to lose ETH every epoch while waiting for the chance to propose. In line with the reasoning in Section 2.2, small validators' expected endogenous yield would still remain positive, but solo stakers that cannot effortlessly pool rewards suffer from the high relative variance in rewards. The more complex option is to assign relatively more block proposals to consolidated stake when the consolidation level is low and no MEV burn is in place.

[Collective consolidation incentives](https://ethresear.ch/t/orbit-ssf-solo-staking-friendly-validator-set-management-for-ssf/19928#collective-consolidation-incentives-11) would also by definition further reduce issuance from an already low baseline if the validator set is not consolidated, once again potentially pushing the solo staker into negative territory.

## 3. Practical endgame

### 3.1 The role of the reward curve

Ethereum's consensus mechanism relies on a reward curve that stipulates how much ETH that should be rewarded for performing each validator duty when a certain amount of ETH is staked, effectively determining the maximum total issuance under perfect participation. The reward curve should roughly reflect the diminishing marginal utility of adding additional stake once security has solidified. Specifically, it should be designed as the "[issuance policy expansion path](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#philosophical-underpinnings-of-the-optimization-problem-30)" that optimally balances relevant trade-offs. It can be understood as a utility maximizing locus of preferred equilibrium points along possible supply curves. In other words, the reward curve should not produce an equilibrium at less desirable points along the supply curve when more desirable equilibria can be achieved. A PID controller guaranteeing some specific quantity of stake is therefore [not desirable](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#why-not-dynamically-adjust-the-yield-with-a-mechanism-like-eip-1559-to-guarantee-some-fixed-target-participation-level-16); it fails to accurately price the marginal utility of additional stake in the long run. 

### 3.2 Endgame categories

Various approaches have been discussed for the issuance endgame; [five loosely delineated categories](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#overview-29) are highlighted in the issuance reduction FAQ. 

[Category 4](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#h-4-economic-capping-34) has been referred to as [economic capping](https://notes.ethereum.org/@vbuterin/single_slot_finality#Economic-capping-of-total-deposits), [targeting](https://ethresear.ch/t/endgame-staking-economics-a-case-for-targeting/18751), or [stake capping](https://www.reddit.com/r/ethereum/comments/14vpyb3/comment/jrnwpmk), constituting a yield that approaches negative infinity, which was discussed in a recent extensive [write-up](https://ethresear.ch/t/endgame-staking-economics-a-case-for-targeting/18751). The benefit is the absolute guarantee of capping the quantity of stake, even in the presence of MEV. A potential downside of this approach, certainly if the cap is set low, is that the equilibrium yield can become unattractive to solo stakers, particularly if there is no MEV burn to reduce reward variability (as discussed in Section 2.3). Another issue is the additional logic required to facilitate the negative yield (e.g., a [staking fee](https://ethresear.ch/t/properties-of-issuance-level-consensus-incentives-and-variability-across-potential-reward-curves/18448#h-3-consensus-incentives-11) deducted each epoch). Figure 10 in [this post](https://ethresear.ch/t/properties-of-issuance-level-consensus-incentives-and-variability-across-potential-reward-curves/18448#h-42-effect-of-pooling-14) shows a realistic scenario with negative regular income for solo stakers under a staking fee. A third downside is that a negative issuance yield can create a "consensus design debt" due to additional analytical and implementational complexity whenever micro incentives are adjusted. Figure 1 outlined the approximate range I see as suitable for a Category 4 design, with the cap reached at around 2/3 or 3/4 of all ETH staked. The figure refers to it as a "hard endgame" due to its complexity and hard cap.

[Category 2](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#h-2-temper-issuance-32) instead involves a more modest reduction of issuance. It represents the type of reduction that would be [desirable for the near future](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#what-is-a-desirable-issuance-reduction-for-the-near-future-9) and does not require incorporating additional logic to maintain proper consensus incentives. It has been [proposed](https://ethereum-magicians.org/t/electra-issuance-curve-adjustment-proposal/18825) as a first step followed by a Category 4 change. A longer write-up on a reward curve with tempered issuance is available [here](https://ethresear.ch/t/reward-curve-with-tempered-issuance-eip-research-post/19171). While it is likely that this type of reward curve could be viable for a long time, a potential downside is the lack of near-certainty.

[Category 3](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#h-3-cut-issuance-33) occupies a middle ground between the two approaches, with curves retaining a positive issuance yield being most relevant. Issuance is then cut to a very low level when too much ETH is staked, yet remains positive. While consensus/consolidation incentives and solo staking can become strained, diligent solo stakers will not need to "pay to stake" while waiting to propose a block, and there is lower "consensus design debt". This constitutes a practical endgame, if the goal is to make one near-term adjustment to issuance that has a high probability of lasting indefinitely. In reality, the difference between Categories 2 and 3 is relatively minor in the sense that they will likely lead to similar equilibrium outcomes. However, it might lend credibility to the notion of aiming for an endgame if the issuance yield at higher quantities of stake is set to a minimum (positive) level.

It has been [argued](https://x.com/ryanberckmans/status/1778124458303111658) that Ethereum must aim for one single change to its issuance policy, credibly positioned as the last change ever needed. My personal contention is that there are many benefits to a [graduated approach](https://ethresear.ch/t/reward-curve-with-tempered-issuance-eip-research-post/19171#h-23-graduated-approach-11). If there was community support to set the reward curve at an issuance rate of 0.5% with a commitment to revisit the issue in a few years' time, I would support it. It would make the process less complicated in the near term. However, the political nature of an issuance change and community reactions seem to support pursuing the endgame policy through a single change. 

Due to the inherent costs of staking and the limited relevance of exogenous yield, a Category 3 change offers a credible case to be the last monetary policy change required. Responsibility then falls on developers to implement MEV burn moving forward. A MEV burn mechanism would: (1) alleviate the strain on consensus design parameters from low issuance at a high quantity of stake, and (2) make a lower equilibrium quantity of stake more likely. Note also that instituting a Category 4 stake cap does not preclude the necessity of future changes. Quantity of stake is not the only factor at play when Ethereum aims to balance issuance policy trade-offs. Indeed, key issues twenty years from now may differ greatly from those in focus today, just as many of the issues we currently face were not anticipated just a few years ago. A stake cap issuance policy could therefore need to be reversed, just like any other policy. In this case, the reversal would more likely be in the form of an increase in issuance, a direction that Ethereum has so far avoided.

### 3.3 Preferred issuance range for a practical endgame

Figure 2 roughly outlines a preferred range for a practical endgame reward curve (previously shown in green in Figure 1). This range represents my personal preferences, given early sketches of consolidation/consensus incentives. Others may have different preferences, which should be collated and further debated. Sketches of the incentives design may also evolve, leading to minor tweaks to the range. The dashed green curve is the previously proposed [reward curve with tempered issuance](https://ethresear.ch/t/reward-curve-with-tempered-issuance-eip-research-post/19171). If the requirement is an endgame, it seems reasonable to go lower than the green curve at higher deposit sizes. The preferred range suggests still issuing at least 60k ETH if everyone stakes (an issuance yield of around 0.05%) and at most 100k ETH more than that (160k ETH). My contention is that the only scenario where an equilibrium is approached at this level is if MEV is much higher than today. The idea is that the last fraction of would-be stakers have relatively very high reservation yields (require a rather high staking yield to stake), which should probabilistically be accounted for. A lower positive issuance might then not influence the equilibrium much anyway, while likely requiring us to push small solo stakers into negative regular rewards in the presence of MEV, something I find undesirable.

![Figure 2|690x423](upload://lhnPiULONkT9XYll0poDMpeyxAi.png)

**Figure 2.** Preferred range for issuance across staking deposit size $D$ for a practical endgame issuance policy (personal rough view). The policy should ensure a sufficient issuance yield at low deposit sizes (but not more), and also such a low issuance yield at high deposit sizes that an equilibrium is extremely unlikely. For improved viability, issuance is still maintained at a positive level throughout.

Assume for example that developers are unable to institute MEV burn and that an equilibrium at a high deposit size is reached when MEV is 600k ETH per year (a doubling of the long-run average, which seems perfectly possible). Whether issuance is 0 ETH or 100k ETH will then not alter the equilibrium substantially. Issuance will at least certainly be of less importance to the delegating staker, who effortlessly derives pooled MEV rewards. Yet, if issuance is 0 ETH instead of 100k ETH, this presumably requires a larger redesign of the micro incentives and will force solo stakers to pay to stake, in the hope of getting the chance to propose a block. If MEV burn is instituted, an equilibrium will not be reached here anyway, and an issuance of 100k ETH thus still has little relevance. The upper limit to the preferred range was defined according to the following intuition: 

* It can be desirable for Ethereum users to cap the issuance rate at 0.5% (see Section 3.4), producing a maximum 4% issuance yield at 15M ETH staked, 3% at 20M, and 2% at 30M. 
* The issuance rate should presumably not remain fixed at 0.5% for an endgame policy due to the diminishing utility of additional security past a certain level. A further reduction starting at the current deposit size (35M ETH) or lower then seems desirable.
* Issuance should not be higher than absolutely necessary at the highest quantity of stake, due to how undesirable such an equilibrium is. Going above 160k ETH (around half of the yearly MEV measured in [this post](https://ethresear.ch/t/properties-of-issuance-level-consensus-incentives-and-variability-across-potential-reward-curves/18448); 0.133% in issuance yield) seems excessive---it should reasonably be possible to design viable consensus/consolidation incentives below that level. 

Presumably, the first fraction of stakers have relatively low reservation yields (require a rather low yield to stake), which should also probabilistically be accounted for. However, if the reward curve must remain fixed forever, Ethereum should issue slightly more tokens than what is needed to achieve an equilibrium at a desirable deposit size. The reason is that the MEV might eventually be burned, which must be factored in. With current thinking about desirable deposit sizes, it then seems beneficial to keep issuance at or ideally above the green dashed curve at lower quantities of stake. 

A question is then how fast issuance should fall down to some minimum acceptable level as the deposit size increases. My contention here is that it seems reasonable to keep the issuance rate above 0.1% up to at least half the ETH is staked. The reason is that a 0.2% staking yield (0.1% issuance rate at 60M ETH staked, with MEV burn in place) could perhaps become more consequential to Ethereum, for example, in terms of effects on decentralization, than the fact that half the ETH is staked. This is in line with the philosophy outlined in Section 3.1---evaluating the utility of different equilibria along an upward-sloping supply curve. Of course, it is highly unlikely that an equilibrium would be established at such a low yield at 60M ETH staked, but the hypothetical options in that scenario must still be evaluated.

### 3.4 Tangible framework: never exceed an issuance rate of 0.5% 
A practical endgame should ideally position the chosen reward curve within a tangible framework that is easy to understand. The upper grey line in Figures 1 and 2 represents an issuance of 0.5% of the circulating supply each year, i.e., an issuance rate of $i=0.005$. From a communication perspective, committing to never issuing more than 0.5% of the circulating supply each year is an accessible policy with "memetic" qualities. Taking some liberties, it also fits within the "power-of-two" framework favored in Ethereum: a maximum of $2^{-1}$% of the supply. Note that the framework is not only applicable to the practical endgame reward curve; it is intended to apply forever. Even if in the future there is a push for an issuance change, there could still be an existing social commitment, making an increase to the issuance rate above 0.5% particularly difficult to push through. Whereas a cap on the circulating supply is an untenable monetary policy, a cap on issuance rate is not. Yet it has the same simplicity.

The [circulating supply](https://ethresear.ch/t/circulating-supply-equilibrium-for-ethereum-and-minimum-viable-issuance-during-the-proof-of-stake-era/10954) will [drift](https://www.youtube.com/watch?v=LtEMabS0Oas&t=1187s) to [balance](https://twitter.com/weboftrees/status/1710725744651825281) supply, demand, and protocol income. Therefore, the pledge would ultimately be enforced by [swapping](https://x.com/weboftrees/status/1710728179260731715) out $D$ for $d$ in the equation for the reward curve and normalizing by including the circulating supply at the time of the swap, once the circulating supply [begins to be tracked](https://ethresear.ch/t/endgame-staking-economics-a-case-for-targeting/18751#how-to-set-the-target-in-relative-staking-ratio-instead-of-absolute-fixed-eth-amount-terms-20) at the consensus layer. 

## 4. Practical endgame reward curves

This section proposes practical endgame reward curves, also including further analysis of the trade-offs Ethereum faces. Examples will be constructed to peak at $i=0.5\%$, but this peak can be adjusted if desirable by altering the scale parameter (often denoted $k$). In particular, the peak of any curve can always be reduced slightly while still remaining below $i=0.5\%$.

### 4.1 Classical tempering
#### Issuance
Figure 3 provides examples using the classical tempering mechanism. The particular construction of these reward curves was first motivated by its [minimal spec change](https://ethresear.ch/t/properties-of-issuance-level-consensus-incentives-and-variability-across-potential-reward-curves/18448#h-51-a-neutral-reward-curve-19), as well as ensuring no issuance increase at any point. Note further that the generated smooth decay in issuance is desirable in light of discouragement attacks ([1](https://github.com/ethereum/research/blob/09d9f34042262c8fb436171786ed6c62e1f57247/papers/discouragement/discouragement.pdf), [2](https://ethresear.ch/t/reward-curve-with-tempered-issuance-eip-research-post/19171#h-53-discouragement-attacks-32)) and [cartelization attacks](https://ethresear.ch/t/reward-curve-with-tempered-issuance-eip-research-post/19171#h-54-cartelization-attacks-33).

Green reward curves are constructed by dividing the equation of the current reward curve by $1+D/k$, where $k$ also denotes peak stake participation. The shape of the curve can be altered by exponentiating $D$, and the peak position (scale) can be altered by changing $k$. The dashed green curve is the same as presented in Figure 2, whereas the full green curve increases $k$ so that the curve peaks at $i=0.5\%$, the level marked by the grey line. The curves of other colors in the figure are constructed by increasing the exponentiation in steps of 0.5 up to 3.5 (for the yellow curve), adjusting $k$ to always produce a peak at $i=0.5\%$. The purple curve is thus constructed through division by $1+(D/k)^2$. The peak will then be located at $D=k\sqrt{3}$, and the variable $k$ was in this case set to $40\times10^6$ to produce the peak at $i=0.5\%$. In Figure 15 of the FAQ, a slightly lower setting for $k$ was instead relied upon for the purple curve.

![Figure 3|690x423](upload://mPAhLmGu2vEVlWr67oOReYDwvSQ.png)

**Figure 3.** Possible shapes of reward curves that temper issuance, constructed by altering the exponentiation of $D$ in the term added to the denominator of the current reward curve equation. The preferred range from Figure 2 is indicated in grey.

Which reward curve that is optimal will depend on how various trade-offs discussed in Sections 2-3 should be balanced, and this will naturally be subject to diverse opinions. The red reward curve is the only option that remains fully within the preferred range presented in Figure 2, but the orange and purple reward curves are also almost within that range. Speculatively, it might be easiest to reach an agreement on one of these three shapes, scaled as desired. 

Note concerning the red reward curve that the exponentiation by 2.5 in the added term naturally combines with the exponentiation by 0.5 of the current reward curve. The resulting equation for issuance yield can therefore be rewritten simply as:

$$
y_i = \frac{cF}{\sqrt{D} + (D/k)^3},
$$

which just requires an adjustment to $k$. Specifically for the plotted curve, $k$ must be reduced from around $35.4\times10^6$ to $1.95\times10^6$. We could thus refer to the red shape as a "cubed" reward curve and the orange shape as a "cubed+" reward curve, with the purple then denoted "squared+", etc.  The yellow curve is created by increasing the exponent from 3 to 4  in the previous equation (thus denoted "quartic"). That reward curve brings issuance very close to zero at high quantities of stake.

#### Staking yield with MEV

The staking yield, inclusive of 300k ETH MEV per year (roughly the long-running average), is shown for the reward curves of Figure 3 in Figure 4. To make the discussion more tangible, equilibria under a hypothetical blue supply curve are marked by a circle, providing plausible scenarios a few years from now. Note that the supply curve will be nearly vertical at short time-scales due to frictions in the decision to stake (even when ignoring the deposit queue), but bends with time, and the focus here is the long run. The hypothetical supply curve would result in an equilibrium of 50M ETH staked and a yield of 2.9% under the current reward curve. 

The other reward curves produce equilibria within 34M-40M ETH staked and a yield of 2-2.3%. It can be interesting to consider an extreme [low-yield scenario](https://ethresear.ch/t/reward-curve-with-tempered-issuance-eip-research-post/19171#h-423-low-yield-scenario-26), where the supply curve is much lower than the most likely outcome---perhaps a decade or two from now. Such a hypothetical supply curve is indicated by a dashed blue line. There should hopefully be rather broad agreement that the equilibrium under the current reward curve is not desirable in this scenario. At a staking yield of around 1.9%, issuance is 1.7M ETH---so high that it is located outside the boundaries of Figures 1-3. There is furthermore no longer a [trustless](https://x.com/fradamt/status/1760808900792594593) sound primary currency in the Ethereum economy in the form of non-staked ETH. All holders of ETH or its derivatives are potentially worse off than under an equilibrium enforced at a lower quantity of stake.

![Figure 4|689x482](upload://arePFJt5lN13Byt99kl9C4u0sfu.png)

**Figure 4.** Staking yield, inclusive of 300k ETH/year in MEV, for tempered reward curves of different shapes. Equilibria with a hypothetical supply curve a few years from now (blue) are indicated by circles. An unlikely very low supply curve is also illustrated by the dashed blue line, with hypothetical equilibria indicated by squares.

The equilibrium quantity of stake for the outlined reward curves varies between around 57M-80M ETH with the very low supply curve. That is above a desirable level. However, this is really the extreme scenario, where MEV burn has not materialized, and half of the token holders are ready to assume---directly or through delegation---the costs of staking under a total staking yield of 0.75%. Reducing issuance further to temper staking might not be desirable. The black dashed line indicates the outcome with no issuance at all. The equilibrium quantity of stake is then not reduced substantially relative to the equilibrium with the lower reward curves, in my view rendering such an approach an unmotivated sacrifice of solo staking viability and increase in consensus design complexity (see also Section 2.3 and Section 3).

#### Issuance yield

Figure 5 instead shows issuance yield with no MEV, which could be the situation after incorporating a fully successful MEV burn mechanism. The equilibrium under the investigated reward curves then ends up at around 30M ETH staked for the outlined hypothetical supply curve. Even under the very low supply curve, the equilibrium is pushed down to between 39M-57M ETH: MEV burn will be a key component for achieving a low quantity of stake if the issuance yield remains positive.

![Figure 5|690x481](upload://rzjJcKAGfep9sGzSMQ08KyTZLd0.png)

**Figure 5.** Issuance yield for tempered reward curves of different shapes, which would also be the staking yield under full MEV burn. Equilibria with a hypothetical supply curve (blue) a few years from now are indicated by circles. An unlikely very low supply curve is also illustrated by the dashed blue line, with hypothetical equilibria indicated by squares.

### 4.2 Issuance floor

The reward curve can also be designed to smoothly transition from the current reward curve to an issuance floor $I_f$, set at some desirable level. Three examples are shown in Figure 6. The light blue curve is constructed by blending with a sigmoid weight computed as 

$$
w = \frac{1}{1 + 2^{(D - D_c)/-k}}.
$$

The central point of the blend was set to $D_c=32\times10^6$ and the steepness of the transition set to $k=7\times10^6$. This can be adjusted as desired. The curve then blends $(1-w)I_r+wI_f$, where $I_r$ is issuance for the current reward curve [i.e., $I_r(D)$] and $I_f$ is set to $120\,000$ ($i=0.1\%$). Another solution is to simply blend between the maximum and minimum desired issuance level by replacing $I_r$ by, for example, a fixed $600\,000$ ETH. This is done with the pink curve, illustrating a piecewise option of transitioning from the current reward curve at the point where the sigmoidal weight intercepts it.

A third option is to employ a [Hill-type equation](https://en.wikipedia.org/wiki/Hill_equation_(biochemistry)):

$$
Y(D) = \frac{D_{h}^{n}I_r + D^{n}I_f }{D^{n} + D_{h}^{n}}.
$$

It is a fairly clean construction, relying on a specified halfway point $D_{h}$ between $I_r$ and $I_f$, as well as the exponent $n$ that further determines the shape. The brown curve was constructed from $D_{h}=30\times10^6$ and $n=3$, setting $I_f=90\,000$.

![Figure 6|690x423](upload://bMMAkTYWXcKRBTWkee0vH1FGukk.png)

**Figure 6.** Three reward curves that asymptotically approach an issuance floor around $i=0.1\%$. The preferred range outlined in Figure 2 is once again indicated in grey.

Figure 7 shows the staking yield inclusive of 300k ETH of MEV/year, investigating the same features as in Figure 4. The reward curves with an issuance floor provide an equilibrium staking of around 60M ETH for the low supply curve, approximately in line with the orange reward curve of the previous examples. Since issuance is kept fixed around the floor, the proportion of the MEV ("No issuance") relative to issuance+MEV remains approximately constant at higher quantities of stake. Figure 8 instead shows the outcome with only issuance yield.

![Figure 7|690x481](upload://q0EDsjNa11TtJwVq51C7owxtmtV.png)

**Figure 7.** Staking yield, inclusive of 300k ETH/year in MEV, for reward curves that asymptotically approach an issuance floor. Equilibria with a hypothetical supply curve a few years from now (blue) are indicated by circles. An unlikely very low supply curve is also illustrated by the dashed blue line, with hypothetical equilibria indicated by squares.

![Figure 8|690x481](upload://7MGVEq7e204l1gtXU34u8EVd1m8.png)

**Figure 8.** Issuance yield for reward curves that asymptotically approach an issuance floor, which would also be the staking yield under full MEV burn. Equilibria with a hypothetical supply curve a few years from now (blue) are indicated by circles. An unlikely very low supply curve is also illustrated by the dashed blue line, with hypothetical equilibria indicated by squares.

### 4.3 Piecewise constructions

Smooth reward curves are not strictly about aesthetics. It seems reasonable to ensure that there is no discontinuity that can influence the decision to stake, for example making cartelization attacks more attractive at some specific range or point. The overarching issuance policy expansion path is arguably also smooth. However, linear piecewise constructions bring the benefit of simplicity, and the downsides may not be sufficient to forego that. Figure 9 shows three linear constructions. The dark blue and cyan reward curves reduce issuance by 1 ETH for every 100 ETH that is staked, in between an issuance rate of 0.5% and 0.1%. The beige reward curve is instead symmetrical around the mid point of 60M ETH, reducing issuance by 1 ETH for every 125 ETH that is staked while taking the issuance rate from 0.5% to 0.1%. 

These constructions provide some tangible anchors that might simplify communication. Issuance is always easy to calculate, and at an issuance rate of 0.5%, the issuance yield becomes 4% at 15M ETH (1/8 of the supply) staked, 3% at 20M ETH (1/6), and 2% at 30M ETH (1/4). An issuance yield of 1% is reached at 40M ETH or 45M ETH, respectively, for the dark blue and cyan reward curve, and at 60M ETH (1/2), the issuance yield is 0.33% or 0.5% respectively.


The dashed dark red reward curve simply sets issuance to an issuance rate of 0.5%. This type of reward curve has been referred to as "[capped issuance](https://notes.ethereum.org/@anderselowsson/Reward-curve-with-capped-issuance)" and was implied in a [proposal](https://ethresear.ch/t/simplified-active-validator-cap-and-rotation-proposal/9022) by Vitalik in early 2021. It is not necessarily an endgame policy and would have to be adopted with the understanding that we might return to the conversation again in a few years. It would enable us to address the issue of a growing quantity of stake so that we can focus on other topics for a few years---until kinks related to for example MEV and Orbit SSF have been worked out. As previously mentioned, I find this type of solution appealing, but from the community's point of view, there seems to be an apparent appetite for definite answers. 

![Figure 9|690x423](upload://uh1dBXVFsdijaE7KbAwamPx2gln.png)

**Figure 9.** Illustrating piecewise constructions with issuance changing linearly or remaining fixed.

## 5. Conclusions and important questions

There are several downsides to an issuance policy that provides 100% certainty of tempering the quantity of stake to reasonable levels, as opposed to one that provides 99.9% certainty. This post has suggested practical endgame reward curves that will temper the growth in the quantity of stake without introducing unnecessary political, analytical, and implementational complexity. My personal preference, fitting within the outlined preferred range, would be to use the shape of either the orange, red, or purple tempered reward curves presented in Section 4.1, where the red curve fits fully within the preferred range. These curves make an equilibrium at a high quantity of stake very unlikely, yet can allow small solo stakers to always receive positive regular rewards when performing their duties adequately. Simply setting issuance to a 0.5% issuance rate for now, as illustrated by the red dashed curve in Figure 9, would in my view also be an appealing solution. The idea would be to then return to the conversation in a few years if necessary, once various issues such as MEV burn have been worked out. But this solution may not appeal to the Ethereum community. 

A clear benefit of a practical endgame is that it has less dependencies and will not fail if MEV burn does not come to fruition under a low supply curve. This allows us to address issuance without unnecessary delay. On a related note, focusing on unrealistic scenarios---such as everyone staking at near-zero issuance yields---would be unfortunate, because we might then fail to move forward when a change would be very beneficial. 

### Questions for the community and researchers

Community feedback and debate would be welcome. For example: 

* Is it ever okay to have solo stakers that do not pool block proposal rewards lose ETH while attesting diligently, as long as they attain a positive expected yield in the long run from infrequent block proposals? Should it be strictly avoided, or would it be acceptable at some higher deposit size to stem further growth, say at 60/90/120M ETH staked? At what percentage of being offline over a year would it be acceptble with negative yield?
* What should the issuance (or equivalently, issuance yield) be set to at 15M, 30M, 45M, 60M, 75M, 90M, and 120M ETH staked? Community members and researchers are welcome to specify their own "preferred range".
* Given current uncertainty related to MEV and the benefits of reducing issuance, would you be supportive of simply fixing issuance at an issuance rate of 0.5% (grey line in the figures; red dashed line in Figure 9) for the next 3/4/5/6 years, with a commitment to return to the issue after that? 

From a research perspective, given the dependency on MEV burn and Orbit SSF, it seems that a lot would be gained by mapping out the likelihood of implementing these mechanisms within specific time frames. This is something that we as consensus researchers could do while we diligently keep working on the implementation details.

-------------------------

OisinKyne | 2024-10-24 14:33:14 UTC | #2

Your posts are so long that I can’t manage to rebut them in entirety, but the below are some places I take issue with (and none of the places where I do agree with you).

The TL;DR of my issue is that I don’t see your work include full accounting for the costs of operating stake in different manners, and often assumes that the person running the node is the person that owns the ETH (and thus you can make statements around the change of issuance policy being ‘positive’ for welfare through reduced inflation, as if ETH holders constitute Ethereum the network) rather than acknowledging and modelling the delegation of stake that is really happening, on both the centralised (Coinbase) and decentralised (Rocket Pool) ends of the staking spectrum, and how each are impacted by your proposal.

A particular contention I have, is that as far as I can see, you erase the operators that stake on Ethereum with less than 32 ether (such as the thousands of Rocket Pool operators, hundreds of Lido Simple DVT operators, future Lido CSM operators, Puffer operators, squad stakers, etc. etc.). **People without significant crypto wealth, that supply their homes, hardware, and labour to run Ethereum for a commission, should be accepted** and even prioritised.

I think issuance capping **will make Ethereum more centralised and subject to capture, than an Ethereum that keeps its existing issuance curve**. A CEX has an OpEx of < $10/validator/year. A set of squad stakers running nodes at home with their own ether might have an OpEx of ~$500+. (My numbers)

Most importantly of all; I think Ethereum **pursuing a deflationary asset policy is a strategic mistake**, and would decimate the growth of Ethereum long term. The world computer **should** get ~1% cheaper to use each year, you **should** want to spend ether on gas to build and do things, and not hoard it for decades, waiting for the future that won’t come because the economy doesn’t grow as a result of a regressive deflationary economic policy. **MVI is not the right path for Ethereum** at least in this era – **stability of the social contract**, and a **pro-growth economic policy** are a far better strategy for the foreseeable future. **(i.e. the ‘Do Nothing’ path)**

What I would counter-propose instead of an issuance cut; to address the risk of high percentages of supply participating in staking, is to 1) introduce aggressive **correlated liveness penalties**, 2) get **mev-burn** and 3) something like **orbit-ssf** shipped, 4) mitigate the major **[disparity](https://lido.fi/institutional) between [native staking](https://ethereum-magicians.org/t/eip-7002-execution-layer-triggerable-exits/14195/6)** and liquid staking, and by then, if we think we now have found a solution for keeping decentralised stake while reducing overall (centralised) stake, we can potentially investigate issuance adjustment. Quite likely, in a ZK-ified L1 era, issuance will indeed need to change to reflect the different roles of proving, verifying, and ensuring CR etc.

The below are some comments on particular statements in your post:

> To Ethereum’s users, a stringent cap on issuance of native ETH tokens is desirable, because it caps the inflation rate. Since revenue of the protocol can be burned, as partially done today, the ETH inflation rate can be sustainably negative (deflation). Ethereum can have trustless sound money with preserved economic security—something that is very valuable for a decentralized economy.

This is an assumption that should be challenged and imo thrown out. A deflationary gas token is bad for the usage of Ethereum and thus its future growth writ large. Why spend gas when it structurally appreciates? It's the same mindset that killed Bitcoin’s growth, a good money has a high velocity. **Ethereum is** not for its holders, it's not for its stakers, it’s **for the people that spend ether**, and we must not lose sight of that.

> Higher issuance dilutes also stakers, and if some stakers leave, remaining stakers may gain a higher proportion of the total ETH, in accordance with the equations in the post on minimum viable issuance (MVI).

This assumes stakers are running all their own capital, and neglects to acknowledge that the majority of stake is delegated, whether on the enterprise side, or on the [home staker](https://x.com/OisinKyne/status/1754961141678154149) side (e.g. rocketpool delegating the rest of the capital for a validator to a home staker). Operators providing validation as a service do not suffer from inflation if they sell their commission to pay their operating costs (and don’t hold their profit in ETH).

> The reward curve should roughly reflect the diminishing marginal utility of adding additional stake once security has solidified.

Nominal security will solidify, but real security in a world where eth staking pays a fraction above its average op-ex cost at max scale will massively degrade. **The marginal stakers are the decentralised ones**, next to none of these stakers, home or enterprise, are staking their own eth, we have to acknowledge the separation of labour and capital if we want to get the economics of this system right. And we have to have meaningful cost and commission data involved too for that matter.

> A stake cap issuance policy could therefore need to be reversed, just like any other policy. In this case, the reversal would more likely be in the form of an increase in issuance, a direction that Ethereum has so far avoided.

You can’t just cut down the stake margins to near 0 or negative (accounting for practical costs) with category 4, and simply get to fix or [reverse the centralisation](https://blog.goodaudience.com/the-staking-problem-9b1e344b24ab) it causes with an issuance increase. You drive decentralisation out of the market until you have [USDC fork-choice rule](https://x.com/ameensol/status/1465378459157295107).

-------------------------

0xwitty | 2024-10-25 10:16:29 UTC | #3

How could a capped issuance policy influence decentralization in Ethereum staking, especially given concerns about higher operational costs for smaller, decentralized operators compared to centralized entities?

-------------------------

OisinKyne | 2024-10-25 15:14:51 UTC | #4

> How could a capped issuance policy influence decentralization in Ethereum staking

In both the 'easy' and 'hard' curves suggested above, the idea is that the APR will diminish to something so minimal to not be marginally worth it considering costs. My contention is that the staking types that survive in this economic policy are the most centralised ones, and the most decentralised staking setups (such as delegated to home stakers taking part in rocketpool, or the permissionless and multi-operator validators in Lido), perish. This I don't think is appropriately modeled in the issuance research to date, particularly not with real life data sets as far as I have seen. And I fear greatly that MVI research overly focuses on the quantity of security rather than quality of security, because the former is more quantifiable than the latter.

-------------------------

keyneom | 2024-10-25 22:51:56 UTC | #5

[quote="aelowsson, post:1, topic:20747"]
To Ethereum’s users, a stringent cap on issuance of native ETH tokens is desirable, because it caps the inflation rate. Since revenue of the protocol can be burned, as partially done today, the ETH inflation rate can be sustainably negative (deflation).
[/quote]

I disagree here. I don't believe deflation is sustainable, I also don't think it is even desirable if it were. Over indexing on the store-of-value property of money leads to weakness in its use as a unit-of-account and medium-of-exchange. Ironically, something that is only a store of value can end up losing its value and then even lose that property as well (this is especially threatening to virtual assets that don't have other fundamental uses outside of their own systems). A reply above does a decent job of laying this out. Overall, I believe Eth is overly deflationary as it stands and needs higher issuance, especially as there are likely to be even more deflationary pressures coming as price discovery on blobs begins and increased L1 activity is likely in any kind of bull-run/growth stage for the network. I believe we are working to decrease the burn (L2s do this to some extent by increasing available tx space on ethereum)--I don't know if it will be enough--but I'd be unlikely to push to further reduce net issuance while we are already primarily deflationary. We _want_ people exchanging and trading eth and using it for things, not just hodling endlessly. It is likely the best path for us to become true money and not just a store of value.

[quote="aelowsson, post:1, topic:20747"]
High issuance can lead a liquid staking token (LST) to [dominate as money](https://x.com/weboftrees/status/1710712326117097785). Lower issuance ensures that app developers and users will not be subjected to monopolistic pressure from LST issuers, or needlessly risk the LST failing, potentially even threatening consensus if an LST becomes “[too big to fail](https://x.com/weboftrees/status/1710713959362252884)”.
[/quote]

I still don't understand why anyone makes this claim. I'll share something I wrote about it but hadn't published yet:

Reducing LST Dominance
- This has some interesting nuances to it. I don't believe targeting a certain issuance really impacts whether effectively all ETH ends up locked in a LST or not. ~99% ETH could still end up being "staked" through Lido even with a 25% target for staking. Lido absorbs 100% of ETH and only issues 20% to validators for actual staking. Whatever little yield is generated is split across all LST holders. So, the real question here is what makes Lido the most money or gives them the most control. Most likely they want as much ETH as possible issued since they get to keep 15% or w/e % of it. Yield really doesn't matter to them. They only care about the cumulative ETH issued because they keep 15% of it no matter what. Yields could be 0.01% for holders but it would still be the best option for getting some form of yield and not losing as much relative ETH to stakers by holding actual plain ETH.
- At the same time though, once we realize that LSTs don't care about the yield staking provides and they are more interested in market dominance. A target rate might actually be an effective means of ensuring that there is always space for a solostakers to join the validator set. LSTs are more likely to adjust the amount they have staked to maximize total issuance and be less concerned with yields. So if we provide a point that allows for this motivated solostakers that believe in securing the chain can likely join and have LSTs make space for them after doing so. If the solostaker is willing to run at a loss, the LST will not be willing to do so. i.e. we can have as many solostakers as are willing to do so and the LSTs are more likely to move out of the validator set to let them do so. This assumes that the LST isn't willing to take losses just to eliminate the competition. Which might be a strong assumption. I could see an LST pushing negative yields to eliminate staking competition but guaranteeing their LST holders positive rates for a time where they pay LST holders out of their own reserves/earnings. Solostakers that face these types of attacks and leave are not likely to come back in my opinion.
- We have no idea what kind of impact this will have on LSTs. I don't think it is safe to make this kind of change in hopes of improving the LST to solostaker landscape. Multiple statements have been made about solostakers sticking around since they already have high fixed/sunk costs. I don't think these are accurate assements. Solostakers can sell hardware. The 32 ETH they currently hold can be sold or converted into an LST instead to get similar or better yields in many cases. If it becomes less and less profitable, I think you will see a significant loss of solostakers on the network.

[quote="aelowsson, post:1, topic:20747"]
The current reward curve compels users to incur higher costs than necessary for securing Ethereum (costs broadly defined to include hardware, risks, illiquidity, taxes, etc.).
[/quote]

Here's some more thoughts I had on this topic that I hadn't had a chance to post:
Minimum viable issuance to avoid paying too much for security.
  - What is security denominated in? US dollars? The Euro? Who decided how much economic security was sufficient? Should it be enough to prevent Nation state level attacks? UN level attacks? Corporate attacks? LST attacks? John paying sally for his Pizza? There is a huge amount of variability in what is enough for the mean or median and what is enough for black swan events. Targeting ironically gives adversarial groups a target to hit in order to carry out successful attacks. Keeping things dynamic actually makes for a less guaranteed form of attack imo.
  - Even targeting a certain percentage of ETH being staked does not give you a very stable amount of economic security because issuance and the burn are always running. If there are 100MM eth and 50% is staked that's very different than only 50MM eth and 50% staked. What are the predicted market caps for these scenarios? Prices do not move perfectly correlated with inflation or deflation. Deflation can kill a currency as much as inflation can. We should either be increasing issuance or decreasing the burn.

[quote="aelowsson, post:1, topic:20747"]
3.1 The role of the reward curve
[/quote]

I don't consider the reward curve to be purely a function of security. It is an incentivization mechanism to encourage Ethereum and Eth adoption. It creates an opportunity for people to join the network and participate as a validator. Your description describes the marginal increase in security from another staker but doesn't account for the non-linear value network effects have as the network grows.

This is a huge post and I don't have time to keep going through things right now so I'll stop at this section for now and try to come back to it later if I have time. Thanks for putting all of this together I'm sure it took a lot of work and its an important conversation to have.

-------------------------

aelowsson | 2024-10-26 01:27:45 UTC | #6

[quote="OisinKyne, post:2, topic:20747"]
The TL;DR of my issue is that I don’t see your work include full accounting for the costs of operating stake in different manners, and often assumes that the person running the node is the person that owns the ETH (and thus you can make statements around the change of issuance policy being ‘positive’ for welfare through reduced inflation, as if ETH holders constitute Ethereum the network) rather than acknowledging and modelling the delegation of stake that is really happening, on both the centralised (Coinbase) and decentralised (Rocket Pool) ends of the staking spectrum, and how each are impacted by your proposal.
[/quote]

For the purpose of calculating the effect on welfare, it does not fundamentally matter who runs the validator. The staking service provider will pass on its costs to the delegator in the form of a staking fee. The delegator will make the decision to delegate stake based on the full cost (staking fee and, e.g., assigned risks), and the principle applies just the same. The welfare loss is the aggregate costs, which must be borne regardless of who runs the validator, and ultimately degrades Ethereum. You can for example think of it as printing new tokens but just using them to compensate for/pay the cost of illiquidity, hardware, additional risks, etc. In this case it is inflation that nobody derives a surplus from.

If you have not studied the topic before or something still is unclear, you could for example have a look at Figure 1 [here](https://ethresear.ch/t/reward-curve-with-tempered-issuance-eip-research-post/19171#h-21-user-utility-9) where the full idea was first outlined (it was also implied earlier in the MVI thread). Or review the [answer](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#how-will-a-reduction-in-issuance-affect-the-composition-of-the-staking-set-21) in the FAQ dealing with the topic. 

For example, concerning your comment about "full costs": The full cost of operating stake is best approximated as the reservation yield associated with the stake, that is to say the lowest yield at which that ETH would be supplied as stake. The supply curve thus implies the marginal cost of staking, and the aggregate cost of staking becomes the integral of the supply curve. 

I tend to refer to ETH holders as such, but we should not separate ETH holders and Ethereum, as if we could decrease welfare for ETH holders without also hurting Ethereum. The native token of Ethereum (and any other decentralized cryptocurrency for that matter) is a central part of the architecture and we must always ensure that users have access to a sound trustless asset: ETH.

As for the composition of the staking set, it is discussed in Section 2.3 with references to the FAQ and the [longer answer](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#how-will-a-reduction-in-issuance-affect-the-composition-of-the-staking-set-21) on this topic stating my position. As directly specified at the start of Section 2: 

[quote="aelowsson, post:1, topic:20747"]
for a deeper understanding, read the [FAQ ](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675).
[/quote]

You must thus study the FAQ for an accounting of the effect on the composition of the staking set. Including that analysis in the post would have made it too long.

[quote="OisinKyne, post:2, topic:20747"]
A particular contention I have, is that as far as I can see, you erase the operators that stake on Ethereum with less than 32 ether (such as the thousands of Rocket Pool operators, hundreds of Lido Simple DVT operators, future Lido CSM operators, Puffer operators, squad stakers, etc. etc.). **People without significant crypto wealth, that supply their homes, hardware, and labour to run Ethereum for a commission, should be accepted** and even prioritised.
[/quote]

This feels like an unfair accusation since I am actively working on making it possible to stake with less than 32 ETH: the vision of Orbit SSF is to allow for 1-ETH validators. Consider for example my recent write-up on [Vorbit SSF](https://ethresear.ch/t/vorbit-ssf-with-circular-and-spiral-finality-validator-selection-and-distribution/20464) or for that matter Section 2.3 where I presented new research around incentivization to this end.

I understand your comment relates to your business interests. Let's reflect on the economics here.

It should be an objective for Ethereum to make it possible to run a 32-ETH validator at a profit. If the quantity of stake grows very large this objective must be weighed against the many other objectives that we have, such as ensuring a trustless sound money within the ecosystem (ETH). In the extremely unlikely scenario where the supply curve becomes very low, both objectives could be slightly strained, such that it might be necessary to have a very cost-effective setup or stake say 48 ETH to remain profitable, and the quantity of stake will then also grow a bit beyond what we are comfortable with. This is unfortunate but part of balancing different trade-offs under an upward-sloping supply curve, as emphasized in the post.

It should not be an objective for Ethereum to ensure that someone staking 1 ETH can do so profitably, if the associated cost calculation involves paying for hardware and broadband, etc. That would imply that someone running a 32-ETH validator can take home a profit approaching 32 times their costs and would push us towards a regime where all ETH is staked. Note that we still wish to allow people with less wealth to run their own staking setup, which is the background to pushing for Orbit SSF with 1-ETH validators. But to profit from that, they would reasonably need to use existing hardware or broadband, or some other more effective setup. Staking with 1 ETH can still be an interesting technical experience, or a way to start the staking journey at a smaller scale.

We can further delineate two different staking regimes among those staking with less than 32 ETH:

* Stakers operating 32 ETH or more without owning that much ETH, say by running mini-pools.
* Stakers operating less than 32 ETH through some specialized setup, for example using distributed validator technology.

The first of these two regimes will remain profitable longer than the second, given that the staker derives income on the full staked amount, although must share those profits according to relevant capital costs to delegators.

[quote="OisinKyne, post:2, topic:20747"]
I think issuance capping **will make Ethereum more centralised and subject to capture, than an Ethereum that keeps its existing issuance curve**. A CEX has an OpEx of < $10/validator/year. A set of squad stakers running nodes at home with their own ether might have an OpEx of ~$500+. (My numbers)
[/quote]

If a staker operates less than 32 ETH as part of a squad-staking setup, then there is a possibility that it may not be able to remain profitable. However, the costs you suggest would be covered by the staking yield even under the extremely low supply curve and full MEV burn. The equilibrium with the red reward for the extremely low reward curve in Figure 5 (red square) is situated above 0.625%, and we find:

$
\frac{500}{2500\times32}=0.625\%.
$



At an ETH price of $2500 and a staking yield of 1%, a 32-ETH validator already generates $800/year. It is in my opinion unlikely that we reach an equilibrium yield below 1% under the practical endgame, even after implementing MEV burn. I would further find 0.5% extremely far-fetched. It is important to use realistic assumptions about the supply curve in the debate.

[quote="OisinKyne, post:2, topic:20747"]
Most importantly of all; I think Ethereum **pursuing a deflationary asset policy is a strategic mistake**, and would decimate the growth of Ethereum long term. The world computer **should** get ~1% cheaper to use each year, you **should** want to spend ether on gas to build and do things, and not hoard it for decades, waiting for the future that won’t come because the economy doesn’t grow as a result of a regressive deflationary economic policy. **MVI is not the right path for Ethereum** at least in this era – **stability of the social contract**, and a **pro-growth economic policy** are a far better strategy for the foreseeable future. **(i.e. the ‘Do Nothing’ path)**
[/quote]

1. Inflationary tokenomics does not inherently make Ethereum cheaper, other than by driving people away from the ecosystem, thus lowering transaction demand.
2. The fiat-denominated value of each ETH token may decrease in an inflationary regime relative to what it would be in a deflationary regime, but this does not make transactions cheaper. If transaction demand (and, depending on interpretation, Ethereum market cap) stays the same, then the proportion of the circulating supply that must be paid to transact will stay roughly the same. The fiat denominated transaction price will not change and the ETH denominated transaction price will increase.
3. What would happen the user is in a way the opposite of what you suggest---Ethereum would get *more expensive* to transact on. Consider the ETH token holder that gets it proportion of the circulating supply inflated away under a high issuance regime and identical transaction demand and market cap. They would now afford to make fewer transactions. Why do you presuppose that people would want to continue using Ethereum if we design issuance policy to make them poorer? Surely, some new cryptocurrency would eventually come along that strives to minimize costs to users and fulfill the promise of sound money that this technology holds, as discussed [here](https://notes.ethereum.org/@anderselowsson/Foundations-of-MVI).
4. You seem to conflate monetary policy of nation states with the issuance policy of a cryptocurrency. Take the example of when central banks lower their policy interest rates. It reflects a commitment to buy government securities (like bonds), which floods the markets with new money. This money is put to work by banks and financial institutions, being lent to consumers and businesses, spurring demand in the economy (economic activity). In contrast, when a cryptocurrency holds the issuance rate high, its users are encouraged to lock up its tokens in staking, which ultimately lowers economic activity, making the platform less attractive for building apps that users could spend their tokens transacting on.
5. We should not attempt to compel users to transact more by making the native token gradually lose value. It is not the way to build a flourishing economy. We do not have the power to retain users under inflation in the way that a nation state has the power to retain users of their fiat currency. And even if we had that power, we should not try to leverage it to this end. Furthermore, the inflation would come to benefit staking service providers but not users. 

*Ethereum will get cheaper to use by implementing the scaling roadmap, not by making its users poorer.*

I find it disheartening seeing people argue for making regular users poorer for “the greater good”. In particular when it is the new financial institutions close to the source of new money in the economy doing it, essentially replaying a centuries-old playbook, but in crypto instead. It is in my opinion a bit immoral. Once again, read [Foundations of minimum viable issuance](https://notes.ethereum.org/@anderselowsson/Foundations-of-MVI) for an accessible outline of what we are trying to achieve here.

[quote="OisinKyne, post:2, topic:20747"]
What I would counter-propose instead of an issuance cut; to address the risk of high percentages of supply participating in staking, is to 1) introduce aggressive **correlated liveness penalties**, 2) get **mev-burn** and 3) something like **orbit-ssf** shipped, 4) mitigate the major **[disparity ](https://lido.fi/institutional) between [native staking](https://ethereum-magicians.org/t/eip-7002-execution-layer-triggerable-exits/14195/6)** and liquid staking, and by then, if we think we now have found a solution for keeping decentralised stake while reducing overall (centralised) stake, we can potentially investigate issuance adjustment. Quite likely, in a ZK-ified L1 era, issuance will indeed need to change to reflect the different roles of proving, verifying, and ensuring CR etc.
[/quote]

This is a list of the ideas we are already pursuing. The practical endgame does not require any of these ideas being implemented. If the reward curve would have involved negative or zero issuance, the situation would have been different. 

If you do not support reducing issuance, you can state your arguments for it already today. There is no need for a delay of several years. There is also no need for the excessive issuance stipulated by the current reward curve; this is already clear today and to delay the reduction by 4-5 years will not serve Ethereum well. What we can do is to cap the issuance rate at 0.5% at this point, solidifying it as a ceiling, and then return to the conversation in a few years. This is discussed in Section 3.4. I do believe even a 0.5% is too much at high quantities of stake, but it is at least not extremely excessive.

We cannot make the correlated attestation penalties too aggressive because that opens up for, e.g., discouragement attacks. I support correlated attestation penalties, but this is a nuanced issue and there is this idea that they will somehow substantially alter conditions for solo staking---they won’t.

[quote="OisinKyne, post:2, topic:20747"]
> To Ethereum’s users, a stringent cap on issuance of native ETH tokens is desirable, because it caps the inflation rate. Since revenue of the protocol can be burned, as partially done today, the ETH inflation rate can be sustainably negative (deflation). Ethereum can have trustless sound money with preserved economic security—something that is very valuable for a decentralized economy.

This is an assumption that should be challenged and imo thrown out. A deflationary gas token is bad for the usage of Ethereum and thus its future growth writ large. Why spend gas when it structurally appreciates? It’s the same mindset that killed Bitcoin’s growth, a good money has a high velocity. **Ethereum is** not for its holders, it’s not for its stakers, it’s **for the people that spend ether**, and we must not lose sight of that.
[/quote]

Let’s first recap basic economics from point 4 of the previous answer: central banks lower their policy interest rate -> by buying government bonds -> to flood the financial system with money -> that will be lent to businesses and consumers -> spurring economic activity. We might not think that this strategy is appropriate, but there is at least some logic to it.

Now let’s review your assumptions: Ethereum should keep issuance high -> to encourage people to… lock up their ETH staking it -> precluding them from spending it on gas -> making it harder for prospective app developers on Ethereum to find willing customers -> …and somehow this is supposed to spur economic activity? There is no logic to it. While derivatives can abstract away some of the barriers, a high issuance is fundamentally a step in the opposite direction of spurring economic activity. Remember, Ethereum activity exploded under proof of work when there was no staking at all. There was just a lot of uncommitted capital with app developers trying to attract it.

Ethereum is fundamentally for its users. We should never *assume* control over our users. There are two meanings to that statement:

1. We should not *assume* control over regular people’s intertemporal choice, trying to coerce them to transact more or less than what they want to. Inflating away our users’ savings with this goal in mind will only hurt them.
2. We should not *assume* that such a control is viable in a digitalizing and globalizing world. If we degrade the user experience, the assumption must be that we will get outcompeted by a cryptocurrency that does not. Nation states have a different relationship to their “token users” than Ethereum, but the frictions they rely on might also be eroded over time.

Bitcoin’s failure was to not adapt smart contracts; let’s not conflate things. Repeating myself a little because it is important: We do not own Ethereum’s users. We cannot slap an inflation tax on them and expect them to stick around if a competitor with a native token without an inflation tax shows up.

[quote="OisinKyne, post:2, topic:20747"]
> Higher issuance dilutes also stakers, and if some stakers leave, remaining stakers may gain a higher proportion of the total ETH, in accordance with the equations in the post on minimum viable issuance (MVI).

This assumes stakers are running all their own capital, and neglects to acknowledge that the majority of stake is delegated, whether on the enterprise side, or on the [home staker](https://x.com/OisinKyne/status/1754961141678154149) side (e.g. rocketpool delegating the rest of the capital for a validator to a home staker). Operators providing validation as a service do not suffer from inflation if they sell their commission to pay their operating costs (and don’t hold their profit in ETH).
[/quote]

It does not assume that stakers operate their own nodes and it applies to both solo stakers and delegating stakers. Concerning the statement: “Operators providing validation as a service do not suffer from inflation”, Ethereum does not exist to enrich staking service providers.

[quote="OisinKyne, post:2, topic:20747"]
> The reward curve should roughly reflect the diminishing marginal utility of adding additional stake once security has solidified.

Nominal security will solidify, but real security in a world where eth staking pays a fraction above its average op-ex cost at max scale will massively degrade. **The marginal stakers are the decentralised ones**, next to none of these stakers, home or enterprise, are staking their own eth, we have to acknowledge the separation of labour and capital if we want to get the economics of this system right. And we have to have meaningful cost and commission data involved too for that matter.
[/quote]

It should not be the objective of Ethereum to promote separation of labor and capital. We thrive on home stakers staking their own ETH, but they can of course stake other people's capital as well. The argument that decentralized stakers do not stake their own ETH seems very convoluted. It seems more like an attempt to promote your company, fitting also with your advocacy for an inflationary issuance policy.

As for the distribution of decentralized stakers, my position on this very complex issue can be found [here](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#how-will-a-reduction-in-issuance-affect-the-composition-of-the-staking-set-21).

[quote="OisinKyne, post:2, topic:20747"]
> A stake cap issuance policy could therefore need to be reversed, just like any other policy. In this case, the reversal would more likely be in the form of an increase in issuance, a direction that Ethereum has so far avoided.

You can’t just cut down the stake margins to near 0 or negative (accounting for practical costs) with category 4, and simply get to fix or [reverse the centralisation](https://blog.goodaudience.com/the-staking-problem-9b1e344b24ab) it causes with an issuance increase. You drive decentralisation out of the market until you have [USDC fork-choice rule ](https://x.com/ameensol/status/1465378459157295107).
[/quote]

My post argues against a Category 4 change and in favor of a practical endgame. The full quote is

[quote="aelowsson, post:1, topic:20747"]
Due to the inherent costs of staking and the limited relevance of exogenous yield, a Category 3 change offers a credible case to be the last monetary policy change required.... Note also that instituting a Category 4 stake cap does not preclude the necessity of future changes. Quantity of stake is not the only factor at play when Ethereum aims to balance issuance policy trade-offs. Indeed, key issues twenty years from now may differ greatly from those in focus today, just as many of the issues we currently face were not anticipated just a few years ago. A stake cap issuance policy could therefore need to be reversed, just like any other policy. In this case, the reversal would more likely be in the form of an increase in issuance, a direction that Ethereum has so far avoided.
[/quote]

Your selective quoting with the associated comment makes it appear as if I find it okay to institute a stake cap and then reverse it, when it is clear that this is not the meaning in context. This is an inappropriate debate strategy and should be avoided.

------
------
------
In conclusion, we should not attempt to compel users to: 
* transact by making the native token gradually lose value, or 
* assume staking costs when unnecessary by stipulating excessive issuance.

We are building with users' best interests in mind, nothing more and nothing less. The Practical endgame reflects this commitment to our users.

-------------------------

keyneom | 2024-10-26 05:21:30 UTC | #7

Picking up from my last reply. Some of what I say here might come off too strong. It's always hard to convey the correct emotion through text and across cultures. Hopefully the message makes it through.

<br />

I think the most reasonable argument for limiting staking is that the network can't actually handle having that many participants at once:
1. Large Validator Set -> Network Instability
   - First the obvious, we have a couple EIPs that are likely to help address this problem in Pectra:
     - EIP-7251: Increase the MAX_EFFECTIVE_BALANCE
       - This allows for consolidated validators amongst centralized or large stakers which also allows for a reduced number of validators and helps eliminate immediate threats of network instability.
     - EIP-7549: Move committee index outside Attestation
       - This allows for much more efficient attestation aggregation and should also reduce network overhead. Allowing for a larger number of validators in the active set than what would currently be possible.
   - We aren't completely sure when/if this issue will raise its head. But we have a couple improvements coming that should help reduce this risk and I believe networking inefficiencies are receiving more focus of late. Overall, I don't believe this is likely to be a problem before the next release after Pectra. I'm interested to see how much of an impact the above two EIPs have on the network. After that, I think we will be better positioned to say whether there is a need to include more work in the next release targeting this risk or whether we will be good for a while.

Orbit looks like a reasonable approach to avoiding hitting this issue while maintaining permissionless participation in running a validator.

[quote="aelowsson, post:1, topic:20747"]
However, the political nature of an issuance change and community reactions seem to support pursuing the endgame policy through a single change.
[/quote]

I somewhat agree with this stance although I wish there were more room for experimentation and believe it will be necessary--though perhaps other chains and other tokens can carry a little of the R&D weight here. Regardless, if the point stands that it should be the last change I'd say there needs to be high confidence and consensus that it is the right path forward. None of what has been discussed seems to bring any MVI changes to that level for me. If we decide to take a less commital approach (which I think would be necessary for any of my ideas on the future of Ethereum to come to fruition) I might be more open to it, but I think it would require a lot of buy in from the entire community regardless and a lot of advance warning.

[quote="aelowsson, post:1, topic:20747"]
This range represents my personal preferences
[/quote]

I touched on marginal additional security not being the only purpose behind more participants in consensus, but I'd add here that the suggested issuance curve adjustments with MVI seem reasonably arbitrary or viewed through a single lens of overpaying for security. I'd want to see analysis on a variety of factors (though I think many would only be capable of being verified through live and active systems) in order to feel more comfortable saying 0.5% inflation should be the highest possible amount. Otherwise, like I said it feels arbitrary and like what is just appealing to your preference for a very non-inflationary or deflationary asset. I.e. your quote said this range represents your personal preferences but I'd argue almost everything you've presented here and the concept of MVI itself represents more of your personal preferences than you might realize.

<br />

To avoid the feeling I think a number of people get that these are just your preferences and somewhat arbitrary I think the _need_ for introducing MVI itself needs to be very explicit and I don't think a high-level and clear need has been defined. I think I've seen 3 high level needs for why we should pursue this articulated (I've addressed them in my replies already but just to make things concise):

1. Large Validator Set Network Instability (a tech problem that already has some reasonable approaches to potentially solving)
2. Reducing LST Dominance (I still have no idea why an LST can't dominate even with more limited issuance)
3. Avoid paying too much for security (extremely subjective what too much security is)

If you can articulate a higher-level need that is really driving a change like this that has a massive impact on every network participant I'd be open to hearing you out. I don't think I've seen it yet. And getting lost in the minutia of which curve specifically to choose with extremely detailed long posts isn't going to help move the proposal forward imo. I only skimmed through all of Section 4 in your post because it assumed buy-in from me on making any of these changes at all that are not even close to being there yet. I know this could sound harsh and I hope it doesn't offend you. I really want to help you if in reality this will be beneficial for the network.

<br />

I believe we should be setting as an ideal that anyone with eth is able to run a validator. You've indicated clearly that it isn't profitable for them to do so. I agree it won't be profitable for them to do so with net new hardware, a dedicated internet connection, etc. but the target isn't necessarily profitability. As you are aware those that don't participate in validation are diluted by those who do. So they lose more money if they don't stake their eth than if they stake their eth (perhaps unprofitably but at almost no greater cost than their existing computer and internet connection). From a tech standpoint I'd prefer a system like bitcoin that no matter how unprofitably they are participating allows them to do so regardless. The beauty of bitcoin is that it can always take on more miners it could be 10 billion separate participants in building the next block and nothing prevents you from joining in. They can always participate if they choose to. It's a property that I'd like to shoot for.

[quote="aelowsson, post:6, topic:20747"]
Now let’s review your assumptions: Ethereum should keep issuance high → to encourage people to… lock up their ETH staking it → precluding them from spending it on gas → making it harder for prospective app developers on Ethereum to find willing customers → …and somehow this is supposed to spur economic activity? There is no logic to it.
[/quote]

I don't think this accurately reflects what occurs. I think you intentionally ignore the incentive people have to spend immediately if they otherwise get diluted. Making the native token delfationary just encourages even more holding by every network participant. Obviously there is an incentive to stake but that might be the difference between us. I want everyone staking. I want everyone participating even if that means there is no real yield. The network itself encourages people to participate in its validity and thus increases its credible neutrality. I agree that ideally issuance and burning cancel each other out and we get no changes in supply but I think slight inflation is more sustainable and better known/understood historically than slight deflation. People that stake right now get a real yield and are more likely to sell that if it is inflationary for real goods (even just to pay off the cost of running the validator) than if it is deflationary (in which case it just encourages more holding and more staking since I get even more of it and it is going to be worth even more -- i.e. I think you've argued there's no incentive to use/burn the token if it is inflationary since you just want to stake it but I don't think you've laid out clearly why anyone would be incentivized to use/burn the token when it is delfationary). Inflation can be viewed as an additional cost holders pay for having a secure, maintained, and live network. The burn helps to reduce this cost to regular users to varying degrees. I don't see why burn should dominate.

<br />

I do think there needs to be changes. Locking up your eth is problematic and LSTs outcompete in this regard vs solo-staking because they can use it as collateral and still get the majority of the yield. In order for direct staking to compete with LSTs I think we would need a system that allows for the use of your stake as collateral. I've laid some of how this could work out elsewhere but I'll try to get another ethresearch post up about it semi-soon.

[quote="aelowsson, post:6, topic:20747"]
We do not own Ethereum’s users. We cannot slap an inflation tax on them and expect them to stick around if a competitor with a native token without an inflation tax shows up.
[/quote]

I semi-agree with you on this point. I'll state though that plenty of currencies have inflation and seem to do alright, fiat and crypto alike. Long term I do think it will be more problematic for them but ETH is no where near that level of inflation and extremely competitive on issuance in my opinion. Look at "issuance" for gold, bitcoin, or fiat and compare it to where eth inflation is at. We are already deflationary and not even in high demand and you are proposing decreasing issuance _even more_. I can sympathize because just this week I've made a couple posts about changing things that would lead to increased burn but I don't think we should be decreasing issuance right now.

[quote="aelowsson, post:6, topic:20747"]
We are building with users’ best interests in mind, nothing more and nothing less. The Practical endgame reflects this commitment to our users.
[/quote]

I agree with the first sentence. I'm just a user. In my opinion from what I've read from you and others regarding MVI the second sentence is not what I would want.

-------------------------

OisinKyne | 2024-10-26 14:31:58 UTC | #8

> it does not fundamentally matter who runs the validator

Well then imo this might be where a model can be harmful rather than [useful](https://en.wikipedia.org/wiki/All_models_are_wrong). It matters, at least to me, who runs the validator. If you just assume the staking providers raise their prices, you end up like [this situation](https://en.wikipedia.org/wiki/Survivorship_bias#/media/File:Survivorship-bias.svg), with only the centralised entities remaining to offer services.

> If you have not studied the topic before or something still is unclear, [...] Or review the [answer](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#how-will-a-reduction-in-issuance-affect-the-composition-of-the-staking-set-21) in the FAQ dealing with the topic.

In this FAQ, it doesn't make any reference to 'home stakers' (for the purpose of discussion, assume one or a group of people putting up < 32 eth for a validator, topped up with delegated stake, not a future orbit thing, or a 32 eth DV cluster of their own capital. Think rocketpool minipool squad). Where do they fit in with respect to your view of Ethereum's goal below: (which i find far, far, too low of a goal for that matter)

> Ethereum wants to retain solo stakers, at least when measured as a proportion of all stakers.



> The full cost of operating stake is best approximated as the reservation yield associated with the stake, that is to say the lowest yield at which that ETH would be supplied as stake. 

Idk, I think the best way to approximate the cost of operating stake is [primary research](https://paragraph.xyz/@ethstaker/staking-survey-2024) coupled with a model informed on this and other data (see later in post).  The lowest yield at which Eth would be supplied as stake is a hypothetical/counterfactual we can't answer as far as I know.

> The native token of Ethereum [...] is a central part of the architecture and we must always ensure that users have access to a sound trustless asset: ETH.

Sure its absolutely important to Ethereum, but the users of ethereum and the holders of ether are not a 100% identical set, and if Ethereum the network is to succeed, more and more users need to gain value from the network, not through simply holding the asset. The people taking action on Ethereum and its L2s are the primary users to serve, the asset holders and machine operators are secondary/tertiary, (we might not agree in which order). 

> The supply curve thus implies the marginal cost of staking, and the aggregate cost of staking becomes the integral of the supply curve.

You are arguing that the supply curve **should** dictate the cost of staking, I'm saying that would likely be bad for the **quality** of security of the network. I also don't even trust that it would be the 'real' cost of supplying validators, because different operators have different exogneous ways to profit from validation (private orderflow, privately sequenced l2s, etc). 

> You must thus study the FAQ for an accounting of the effect on the composition of the staking set

I have, and one quote from it I will pick is:

> The concern is therefore only valid with a yield that goes close to 0 or negative at a low quantity of stake. No SSP can reasonably outcompete all others at an equilibrium staking yield of, e.g., 2% at 30M ETH staked. 

I don't understand 
1) why you don't think yields can go 'close to 0' in your proposals (at least thats what i infer from the framing of the concern only 'being valid' in this case. and
2) "No SSP can reasonably outcompete all others at an equilibrium staking yield of, e.g., 2% at 30M ETH staked" why do you say this? And why does this impossibility of out-competition not hold at 34m and 2.5% like the current day? 

And directly preceding that you say:
> and perfect competition is not a reasonable assumption. If the cost of operating a node is not prohibitively high relative to the income that the SSP can make from running it, then variety in preferences and circumstances between delegators will take a central role in shaping the composition of the staking set.

And to me this sentence reads like we should be on the same page, that perfect competition is not a reasonable assumption, so we shouldn't adopt a curve that tends towards maximal marginal competition and thus imperfect markets like oligopolies and monopolies. Lets allow for 'welfare loss' where the cost of operating a node is not so prohibitively high relative to the income the SSP can make, that it allows for a variety of preferences and circumstances to survive and hopefully thrive. 

 > This feels like an unfair accusation since I am actively working on making it possible to stake with less than 32 ETH: the vision of Orbit SSF is to allow for 1-ETH validators. 

That is fair and I didn't realise you were an author on the (V)Orbit work, I apologise. 

> I understand your comment relates to your business interests. 

Sure but as linked in my post, my [ideological interests](https://blog.goodaudience.com/the-staking-problem-9b1e344b24ab) have existed on this matter long before my '[business interests](https://blog.obol.org/tackling-the-staking-problem/)'. 

> It should be an objective for Ethereum to make it possible to run a 32-ETH validator at a profit. 
> It should not be an objective for Ethereum to ensure that someone staking 1 ETH can do so profitably

Why the delineation between 1 and 32 and not a different level? And do you think a current 32 ether validator can be profitable (at what profit margin?) in the current regime and in the category 2 one, without subsidising costs such as rent/internet/power. (e.g. in a commodity cloud machine) 

(I agree that its not feasible to expect a profit at 1 eth btw, I think we just need to acknowledge and enable the good types of delegation on the margins to these operators, to improve the chain's staking gini coefficient)

> We can further delineate two different staking regimes among those staking with less than 32 ETH:

I'm not sure this is the best delineation, because you can for example run a distributed validator minipool, but it is certainly important and related to my last comment, that there is a big difference between what you might call extrinsic capital (e.g. rEth) and intrinsic capital (squad staking with your squad's own eth). It is extremely difficult under today's curve even, to make the intrinsic [squad staking](https://launchpad.obol.org/cluster/details/?lockHash=0x54c7588ce0bb9cb276fc3f51b49a19dcd3bcf73b6f5e41200133e1295a226fe2) viable without a lot of sunk cost accounting. As a result, most squad staking favours these [extrinsic capital sources](https://docs.obol.org/docs/advanced/lido_csm), because they are needed to improve margins into viability for those with the least capital.

> If a staker operates less than 32 ETH as part of a squad-staking setup, then there is a possibility that it may not be able to remain profitable. However, the costs you suggest would be covered by the staking yield even under the extremely low supply curve and full MEV burn.

Of course, supportive of mev-burn, and I don't really expect solo squad staking to super-economical without at least leaning on the sunk costs of a house with power+internet, or even the assumption of a full solo validator that the distributed validator tags along with. The $500 off-hand figure assumes some of that. [Here is an example I've prepared](https://docs.google.com/spreadsheets/d/1O0HSob053aCUEKqNZ4c_EVHcqEb8u9t0uxxU7zo9R_U/edit?usp=sharing ) were you to rent from a provider, which is one of the most low-cost ways to run a node other than running it yourself, not pretty. 

> It is in my opinion unlikely that we reach an equilibrium yield below 1% under the practical endgame, even after implementing MEV burn. I would further find 0.5% extremely far-fetched. It is important to use realistic assumptions about the supply curve in the debate.

This is somewhere our priors probably differ, I don't know why you think it wouldn't go far lower. As we've said, there are SSPs here with a motive for earning comission, so they will supply capacity to stake if they can do so above their hyper-low marginal extra cost. Who changes from cbEth to plain eth on cb because they'd rather 0% over 0.5%? 


> Inflationary tokenomics does not inherently make Ethereum cheaper, other than by driving people away from the ecosystem, thus lowering transaction demand.

They do not make Ethereum cheaper, but inflationary, or ideally, dis-inflationary regimes would be better for the use of Ethereum than structural deflation. 

> Why do you presuppose that people would want to continue using Ethereum if we design issuance policy to make them poorer? 

Your category 2 design also includes issuance 'to make them poorer', the debate we're having is whether the risks outweigh the rewards of bounding it, no one is arguing to increase issuance beyond the current curve. (Which is far far lower than the issuance policy that came before it)

And to answer the question directly, people would continue to use Ethereum because Ethereum aims to be the most credibly netural, decentralised settlement layer, not the cheapest, nor the one with the most structurally advantageous tokenomics for holders seeking to maximise gains. To have a diverse, redundant, non hyper-optimised to giant economies of scale network, you need to allow for that in decisions around issuance bounding.  

> I find it disheartening seeing people argue for making regular users poorer for “the greater good”. In particular when it is the new financial institutions close to the source of new money in the economy doing it, essentially replaying a centuries-old playbook, but in crypto instead. It is in my opinion a bit immoral. 

You may consider me immoral, but I am earnestly arguing what I see as for the best of Ethereum (doxxed and with all my biases). I foresaw the likely stake centralisation in 2018, I was wondering 'Am I the baddy?' in 2021 when I controlled ~10% of the network, and now in 2024 I think I've meaningfully changed the trajectory of Proof of Stake Ethereum by showing groups of SME and home stakers outperform [8/10](https://x.com/KimonSh/status/1847210588662849539) of the biggest staking entities so far. However there is a long way to go in my eyes, before the Ethereum operator set becomes sufficiently decentralised for what it needs to be to be black swan secure, and I think bounding issuance, and making it even harder for marginal stakers to stay afloat, making distributed validators particularly economically non-viable at retail scale, will push Ethereum down the road I outlined in "[the staking problem](https://blog.goodaudience.com/the-staking-problem-9b1e344b24ab)", which was more eloquently framed by Ameen, as USDC fork choice rule. 

> If you do not support reducing issuance, you can state your arguments for it already today. There is no need for a delay of several years. There is also no need for the excessive issuance stipulated by the current reward curve; this is already clear today and to delay the reduction by 4-5 years will not serve Ethereum well.

I do not and I already did. My arguments were that Category 1 / Do nothing, is 1) good for upholding the social contract where there is credible argument for adjusting near only once more, and yes, 2) good to pay for a robust security budget, which I see as positive and framed it above  as 'growth' as it grows the number of ethereum nodes and validators and operators and the on chain economy, but you I think consider it to be a regressive issuance tax that impoverishes people.  

> I support correlated attestation penalties, but this is a nuanced issue and there is this idea that they will somehow substantially alter conditions for solo staking—they won’t.

Yeah ack, not a magic wand, but would love to see urgency on this and mev-burn in fusaka maybe. 

> Remember, Ethereum activity exploded under proof of work when there was no staking at all. There was just a lot of uncommitted capital with app developers trying to attract it.

And if I'm not mistaken, a 4.4% annual issuance rate... 

Considering you acknowledge that one of the problems here is the LSTs make the locked, unlocked. I do think issuance is stimulative. 

(I'm not saying this is a good thing and a lever we should be pulling, but you are asking me how my view that issuance is stimulative unlike in sovereign markets adds up).

> Inflating away our users’ savings with this goal in mind will only hurt them.

That is clearly not the goal here. The intention is to stick to a curve that was designed to be disinflationary or slightly deflationary with respect to fiat currency, by targetting a max issuance rate of ~1.1% (iirc), which should in theory be beneath government's 2% fiat price inflation targets (though those are different types of inflation), and it also has the benefit of always offering a marginal price to stake right to the end of the curve. 

Blockchain compromise is highly asymmetric and black swan driven. A non-trivial issuance for security is part of building the most trustless decentralised public blockchain. 

> and expect them to stick around if a competitor with a native token without an inflation tax shows up.

The current competitors and most new ones always bootstrap with inflation taxes, I don't think thats a major risk. On the other hand, Ethereum cannot afford to be out-competed in its decentralisation and credible neutrality, while it does not have competition in the stability of its money supply

> Concerning the statement: “Operators providing validation as a service do not suffer from inflation”, Ethereum does not exist to enrich staking service providers.

It does not exist to enrich them, but Ethereum does exist by who these entities are and how they are controlled. We should not end up with a mono-culture if we want Ethereum to be anti-fragile. (And keep in mind that by count, most of this group are people with < 32 eth running nodes) 

> It should not be the objective of Ethereum to promote separation of labor and capital. We thrive on home stakers staking their own ETH, but they can of course stake other people’s capital as well. The argument that decentralized stakers do not stake their own ETH seems very convoluted. It seems more like an attempt to promote your company, fitting also with your advocacy for an inflationary issuance policy.

I don't suggest to set it as an objective, I do think you should model it while analysing how many small operators would become under-breakeven with a given change. Considering they "can of course stake other people's capital as well". This is what I mean by "decentralised stakers do not stake their own eth", that the economics of running either a solo or a piece of a DV with your own capital, accounting for costs, leaves a fraction of return if any. Most of these cases are at least using minipools, (and now Lido CSM,) to get more ether validating on their machines than they own themselves. The market for "has 32 eth" and "wants to run their own node" is now exhausted, and we're left with "has some/minimal eth" and "wants to run a node for reward". 

> This is an inappropriate debate strategy and should be avoided.

Fair enough, its hard to always discern when you are outlining strategies and when you are advocating for them. 

> In conclusion

And my conclusion is, it is not theft nor reckless to pay for security, and we should do our best to focus on the quality over the quantity of security. Proof of stake is a highly asymmetric risk surface, and they way PoS chains break is rarely through the front door economic attack. 

I am unconvinced that bounding issuance to `d` rather than `D` won't cause ultra low cost validators driving the equilibrium APR to way lower than most seem to expect, resulting in a mono-culture of ~3/10 entities that can make profit at such low rates. This has been my fear for approximately 6 years now, and I don't see why my concerns are unfounded nor unreasonable.

-------------------------

aelowsson | 2024-10-26 14:47:01 UTC | #9

I begin by mentioning that a background to this proposal can be found in the following four answers of the FAQ:

* [Why should Ethereum reduce its issuance?](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#why-should-ethereum-reduce-its-issuance-4)
* [Can stakers profit from a reduced issuance and what is the relevance and impact of the real/proportional yield?](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#can-stakers-profit-from-a-reduced-issuance-and-what-is-the-relevance-and-impact-of-the-realproportional-yield-37)
* [What about economic security? More stake makes Ethereum more secure right?](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#what-about-economic-security-more-stake-makes-ethereum-more-secure-right-8)
* [How will a reduction in issuance affect the composition of the staking set?](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#how-will-a-reduction-in-issuance-affect-the-composition-of-the-staking-set-21)

[quote="keyneom, post:5, topic:20747"]
I don’t believe deflation is sustainable, I also don’t think it is even desirable if it were. Over indexing on the store-of-value property of money leads to weakness in its use as a unit-of-account and medium-of-exchange. Ironically, something that is only a store of value can end up losing its value and then even lose that property as well (this is especially threatening to virtual assets that don’t have other fundamental uses outside of their own systems).
[/quote]

We ensure that ETH gets used as money in the world through the scaling roadmap as well as all the other improvements currently underway. The suggestion that ETH needs to make its users poorer for it to be used as money is a false premise. Ethereum will get used as money by being useful as money, not through a Keynesian fallacy (which Keynes himself wouldn’t even find applicable in this context). 

[quote="keyneom, post:5, topic:20747"]
Overall, I believe Eth is overly deflationary as it stands and needs higher issuance, especially as there are likely to be even more deflationary pressures coming as price discovery on blobs begins and increased L1 activity is likely in any kind of bull-run/growth stage for the network. I believe we are working to decrease the burn (L2s do this to some extent by increasing available tx space on ethereum)–I don’t know if it will be enough
[/quote]

You think transaction demand is becoming too high (too high burn) and therefore wish to further increase issuance, to encourage... more transactions and use as money? It does not make sense to me. We are not working on decreasing the burn. We are working on scaling Ethereum. The burn might just as well increase from it eventually, which would be welcome.

[quote="keyneom, post:5, topic:20747"]
I don’t believe targeting a certain issuance really impacts whether effectively all ETH ends up locked in a LST or not. ~99% ETH could still end up being “staked” through Lido even with a 25% target for staking. Lido absorbs 100% of ETH and only issues 20% to validators for actual staking. Whatever little yield is generated is split across all LST holders. So, the real question here is what makes Lido the most money or gives them the most control. Most likely they want as much ETH as possible issued since they get to keep 15% or w/e % of it. Yield really doesn’t matter to them. They only care about the cumulative ETH issued because they keep 15% of it no matter what. Yields could be 0.01% for holders but it would still be the best option for getting some form of yield and not losing as much relative ETH to stakers by holding actual plain ETH.
[/quote]

Why would users send all ETH to Lido when they are provided with no yield on it? In the outlined scenario, staking through some other LST will give 400% higher yield since Lido apparently only stakes 20% of their ETH. Why not stake with that other LST then instead? There needs to be a logic to the arguments here.

"Most likely they want as much ETH as possible issued since they get to keep 15% or w/e % of it. Yield really doesn’t matter to them."

Just to be clear, yield is generated through issuance. The equation is $y=I/D$.

"Yields could be 0.01% for holders but it would still be the best option for getting some form of yield and not losing as much relative ETH to stakers by holding actual plain ETH."

Users will not risk their ETH through staking with a third party for 0.01% yield.

[quote="keyneom, post:5, topic:20747"]
I could see an LST pushing negative yields to eliminate staking competition but guaranteeing their LST holders positive rates for a time where they pay LST holders out of their own reserves/earnings. Solostakers that face these types of attacks and leave are not likely to come back in my opinion.
[/quote]

The Practical endgame does not allow an LST to push us into negative yield territory (which would be unlikely anyway). So this does not apply.

[quote="keyneom, post:5, topic:20747"]
Targeting ironically gives adversarial groups a target to hit in order to carry out successful attacks. Keeping things dynamic actually makes for a less guaranteed form of attack imo.
[/quote]

There is no "targeting" proposed in the post you are commenting on, in the sense that there is no negative yield. 

[quote="keyneom, post:5, topic:20747"]
Even targeting a certain percentage of ETH being staked does not give you a very stable amount of economic security because issuance and the burn are always running. If there are 100MM eth and 50% is staked that’s very different than only 50MM eth and 50% staked. What are the predicted market caps for these scenarios?
[/quote]

This is literally described in the post:

[quote="aelowsson, post:1, topic:20747"]
The [circulating supply](https://ethresear.ch/t/circulating-supply-equilibrium-for-ethereum-and-minimum-viable-issuance-during-the-proof-of-stake-era/10954) will [drift](https://www.youtube.com/watch?v=LtEMabS0Oas&t=1187s) to [balance](https://twitter.com/weboftrees/status/1710725744651825281) supply, demand, and protocol income. Therefore, the pledge would ultimately be enforced by [swapping](https://x.com/weboftrees/status/1710728179260731715) out $D$ for $d$ in the equation for the reward curve and normalizing by including the circulating supply at the time of the swap, once the circulating supply [begins to be tracked](https://ethresear.ch/t/endgame-staking-economics-a-case-for-targeting/18751#how-to-set-the-target-in-relative-staking-ratio-instead-of-absolute-fixed-eth-amount-terms-20) at the consensus layer.
[/quote]

We are going to change the equation for the reward curve to relate to deposit ratio instead of deposit size. This has been the plan ever since I made [this post](https://ethresear.ch/t/circulating-supply-equilibrium-for-ethereum-and-minimum-viable-issuance-during-the-proof-of-stake-era/10954) several years ago.

[quote="keyneom, post:5, topic:20747"]
[quote="aelowsson, post:1, topic:20747"]
3.1 The role of the reward curve
[/quote]
I don’t consider the reward curve to be purely a function of security. It is an incentivization mechanism to encourage Ethereum and Eth adoption.
[/quote]

The reward curve ensures sufficient staking to keep Ethereum secure. "To encourage Ethereum and Eth adoption" is very vague. If you think we should issue yield to lure people to the Ethereum ecosystem, read [this answer](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#some-users-think-that-more-yield-is-more-fun-and-like-to-collect-yield-on-their-eth-why-not-lean-into-this-43) from the FAQ.

[quote="keyneom, post:7, topic:20747"]
From a tech standpoint I’d prefer a system like bitcoin that no matter how unprofitably they are participating allows them to do so regardless. The beauty of bitcoin is that it can always take on more miners it could be 10 billion separate participants in building the next block and nothing prevents you from joining in. They can always participate if they choose to. It’s a property that I’d like to shoot for.
[/quote]

I don't understand your point. The Practical endgame literally does not cap the quantity of stake. Everyone will be allowed to stake, and even those staking with very small amounts will get a regular positive reward. This seems like exactly what you are looking for.

[quote="keyneom, post:7, topic:20747"]
I think you intentionally ignore the incentive people have to spend immediately if they otherwise get diluted. 
[/quote]

This has already been answered but I really think you should reconsider. Why do you feel the need to degrade the user experience and make our users lose money by diluting them? You have not provided a clear answer to this other than stating that you want them to transact. You do not think we can build a network where people transact because they want something, rather than being coerced into it?

[quote="keyneom, post:7, topic:20747"]
People that stake right now get a real yield and are more likely to sell that if it is inflationary for real goods (even just to pay off the cost of running the validator) than if it is deflationary (in which case it just encourages more holding and more staking since I get even more of it and it is going to be worth even more – i.e. I think you’ve argued there’s no incentive to use/burn the token if it is inflationary since you just want to stake it but I don’t think you’ve laid out clearly why anyone would be incentivized to use/burn the token when it is delfationary).
[/quote]

We are not here to micromanage our users' spending habits. It's our job to scale Ethereum and make it as cheap and secure as possible to transact. Why do you feel the need to try to coerce users to transact when they do not want to? People will not lose the need to transact just because ETH is deflationary. If they need something, they will buy it. If they wish to send money to a friend, they will send it. If they have found a promising investment that they think will outperform all other opportunities available to them, they will invest. The winning strategy is to facilitate real economic activity. We should let users go about their business as they see fit, without diluting them, rather than trying to artificially coerce users into transacting (which by the way would not work anyway; but I am just responding to the argument).

-------------------------

keyneom | 2024-10-26 19:46:38 UTC | #10

I don't know that I think my points are being fully addressed (I might not have explained them well enough--like the point of a billion Bitcoin miners participating in consensus at once). Here are probably the two major points I'd contend with from your reply. Apologies that I'm not addressing all your points either.

[quote="aelowsson, post:9, topic:20747"]
Why would users send all ETH to Lido when they are provided with no yield on it? In the outlined scenario, staking through some other LST will give 400% higher yield since Lido apparently only stakes 20% of their ETH. Why not stake with that other LST then instead? There needs to be a logic to the arguments here.
[/quote]

Because there are other market centralizing forces than just a simple interest rate. Ability to use as collateral across all other protocols is massive. Especially if a dominant player aggressively pursues exclusivity deals. Just starting up an institutional grade competing staking business is hard and expensive, but once you have your fixed costs addressed the marginal costs of adding another validator are almost nothing which can make it very hard for a new LST upstart to compete. We've already seen this imo. In the end I just don't see us significantly preventing LST dominance much more effectively than we already do as a result of modifying the issuance curve.

[quote="aelowsson, post:9, topic:20747"]
This is literally described in the post:
[/quote]

Isn't this agnostic to market cap? If eth market cap is $100 vs $1 trillion that significantly impacts the security of the network in being able to withstand a nation state level attack. One requires almost no effort to buy enough supply to control the network and the other is much more difficult to do so. Limiting the amount staked makes this even more impactful. That's my point. It is totally subjective what is "enough" economic security. 

[quote="aelowsson, post:9, topic:20747"]
Why do you feel the need to try to coerce users to transact when they do not want to?
[/quote]

No one is coercing anyone. I could ask you the same question. Why do you feel the need to try to discourage users from transacting when they otherwise would? The only way of avoiding this is net 0% deflation/inflation. I already mentioned that would be ideal but I don't think it is long term feasible to have a fixed supply. Issuance paired with the burn is a great approach but will almost guarantee that one is stronger than the other. I'd rather lean towards slight inflation than deflation. You haven't even demonstrated an actual need for MVI as I indicated in my second post. If people aren't agreeing at least on that high level point first you will never have success convincing them of some random other arbitrary curve that feels nice to you.

I don't love having this conversation in back and forth long form posts. I respect the work you do, this is just one area I haven't been convinced of your approach. I'd be happy to have a conversation with you over video chat or something if you are interested as I get the feeling you interpret anyone that opposes these changes as just a bad actor or with ulterior motives (or perhaps just not smart enough) and I think I could convince you otherwise if we chatted. Other than that I'll probably step out of the debate until I feel my primary concern is actually addressed (a real, clear, and concise need for making these changes--existing explanations obviously not having met that standard so far). Until then I'd still vote to oppose any changes. All the best!

-------------------------

aelowsson | 2024-10-26 22:59:14 UTC | #11

[quote="keyneom, post:10, topic:20747"]
I don’t know that I think my points are being fully addressed (I might not have explained them well enough–like the point of a billion Bitcoin miners participating in consensus at once). Here are probably the two major points I’d contend with from your reply. Apologies that I’m not addressing all your points either.
[/quote]

It is quite natural to not perceive all points as fully addressed from the first response in a discussion. This often requires further back and forth.

[quote="keyneom, post:10, topic:20747"]
[quote="aelowsson, post:9, topic:20747"]
This is literally described in the post:
[/quote]

Isn’t this agnostic to market cap? If eth market cap is $100 vs $1 trillion that significantly impacts the security of the network in being able to withstand a nation state level attack. One requires almost no effort to buy enough supply to control the network and the other is much more difficult to do so. Limiting the amount staked makes this even more impactful. That’s my point. It is totally subjective what is “enough” economic security.
[/quote]

The focus of my response was to the following statement: "If there are 100MM eth and 50% is staked that’s very different than only 50MM eth and 50% staked." Under the current issuance policy, Ethereum is incapable of handling this scenario correctly, because the offered yield would differ since it varies with deposit size and not deposit ratio. So I explained the plan to rework our issuance policy to handle that. This has all been worked out but will be phased in over several hard forks. In essence, we will track the circulating supply and [swap out](https://x.com/weboftrees/status/1710728179260731715) $D$ for $d$ in the equation of the reward curve, also including the circulating supply $S$.

When it comes to the influence of market cap, this was described in the first paragraph of the link I provided as the start of my answer.  If you could find the time to review these links, it would be very beneficial, since it takes up a lot of time answering these questions.

[quote="aelowsson, post:1, topic:19675"]
Ethereum’s economic security will in the long term inherently be linked to the ability of ETH to retain its value. A holistic perspective is therefore important also when considering economic security. This is underscored by reflecting on the early days of Ethereum, when the ETH token was much less valuable. Eight years ago, In May 2016, [Vitalik deliberated on ](https://blog.ethereum.org/2016/05/09/on-settlement-finality) the value that Ethereum can and cannot secure at a stake participation of 30%. At the time, the market cap of the ETH token was roughly 500 times lower than today, and the economic security that Ethereum could offer was therefore limited. Increasing stake participation from 30% to 60% would only increase the value of 1/3 of the stake (the threshold for the ability to delay finality) from $70M to $140M. This highlights that once the proportion staked has risen above insignificant levels, it will ultimately be Ethereum’s role in the world economy, and the ether’s role in the Ethereum economy, that determines the economic security.
[/quote]

The contention is thus that we cannot focus too closely on market cap when specifying the reward curve.

[quote="keyneom, post:10, topic:20747"]
[quote="aelowsson, post:9, topic:20747"]
Why do you feel the need to try to coerce users to transact when they do not want to?
[/quote]

No one is coercing anyone. I could ask you the same question. Why do you feel the need to try to discourage users from transacting when they otherwise would?
[/quote]

Clearly, you consider issuance policy as an instrument for affecting transaction demand. You discuss inflation and deflation, sharing opinions on how it will affect user behavior, with quotes such as "the incentive people have to spend immediately if they otherwise get diluted", etc.

This is however not the purpose of Ethereum's issuance policy. We do not and shall not rely on issuance policy to affect transaction demand, but solely to affect the willingness to supply stake. Whether ETH deflates or inflates does not factor into the equation. Thus, I do not "feel the need to discourage users from transacting", because I know that it is a fruitless endeavor. I am strictly focused on security and composition of the staking set.  

[quote="keyneom, post:10, topic:20747"]
The only way of avoiding this is net 0% deflation/inflation. I already mentioned that would be ideal but I don’t think it is long term feasible to have a fixed supply. Issuance paired with the burn is a great approach but will almost guarantee that one is stronger than the other. I’d rather lean towards slight inflation than deflation.
[/quote]

There is nothing to avoid, because we do not try to influence transaction demand with issuance policy. Slight inflation implies that Ethereum is incapable of securing its network when relying on current revenue. For this reason, deflation is a healthy sign for any cryptocurrency. 

[quote="keyneom, post:10, topic:20747"]
...once you have your fixed costs addressed the marginal costs of adding another validator are almost nothing which can make it very hard for a new LST upstart to compete.  In the end I just don’t see us significantly preventing LST dominance much more effectively than we already do as a result of modifying the issuance curve.
[/quote]

An LST that provides a five times lower staking yield to its customers will have a very hard time to compete. But this is not integral to the discussion, let us move on. 

[quote="keyneom, post:10, topic:20747"]
You haven’t even demonstrated an actual need for MVI as I indicated in my second post. If people aren’t agreeing at least on that high level point first you will never have success convincing them of some random other arbitrary curve that feels nice to you.
[/quote]

The primary motivation for a reduction in issuance is the reduction in costs, leading to a welfare gain. I have linked the relevant write-up and figure on this several times, but will present it here also, if you perhaps missed it. 

Two reward curves are shown in the figure, both under the present level of MEV (300k ETH/year) and the hypothetical supply curve used in the post. The supply curve indicates the amount of stake deposited $D$ at various staking yields $y$. It captures the implied marginal cost of staking. What that means is that every ETH holder is positioned along the supply curve according to how high cost they assign to staking, with their required yield implying that cost. Relevant costs include hardware and other resources, upkeep, the acquisition of technical knowledge, illiquidity, trust in third parties and other factors increasing the risk premium, various opportunity costs, taxes, etc. The area above the supply curve indicates the stakers’ surplus (what they actually gain) and the area below the supply curve the costs assigned to staking (the marginal staker would not stake at a yield below the supply curve).

![Figure A1|690x416](upload://r6fAZDbRTxuhVuDZ3IjlQhae55j.png)

By maintaining the current reward curve in black, Ethereum compels users to incur higher costs than necessary for securing the network. Adopting the red cubed reward curve from the post eliminates implied costs represented by the dark blue area, thus improving welfare. These implied costs amount to around 344 000 ETH, corresponding to 859 million dollars.

The issued ETH covered for hardware expenses, taxes, reduced liquidity and risks that users would choose to sidestep under a lower yield. With the red curve, they can, and the benefits are shared by everyone (including remaining stakers), creating value for all token holders through a reduction in newly minted ETH. It may seem strange that it matters how many new ETH that are created. But imagine if every ETH was converted to 10 ETH tomorrow so that there were 1.2 billion instead of 120 million ETH in total. Then every ETH would be around 10 times less valuable. What matters is the proportion of all ETH that you hold. There is also a surplus shift from stakers to everyone from a change in issuance policy, indicated by the darker grey area. That ETH indeed previously benefited stakers, since it was taken from everyone (in the form of newly minted ETH), and then given specifically to them.

It is important to understand that the cost reduction corresponding to 859 million dollars is the yearly savings, not a one-off event. The implied cost reduction applies each year, benefiting Ethereum’s users on an ongoing basis.

-------------------------

keyneom | 2024-10-27 03:12:10 UTC | #12

I'm still not convinced. Sufficient security still feels very arbitrary. I think you want deflation (though you state it's just a question of security) but I don't think ongoing deflation is likely to be beneficial or sustainable. Thanks for taking the time to respond! Perhaps you'll change my mind at some point but nothing I've seen (and I have seen some of the other MVI resources and discussions but unfortunately it isn't my full time job to get to read all of them or critique them) has demonstrated a clear need to make changes. I don't know for sure but my sense is that a good portion of the community doesn't see the need yet either. Hopefully this helps to progress the conversation!

-------------------------

pa7x1 | 2024-10-27 21:09:36 UTC | #13

The biggest issue of tempered issuance and other issuance curves that flatten out after certain stake rate is that they result in a big gap between the stake rates at which solo stakers become economically disincentivized and where LSTs do so. This creates a large regime of stake rates where solo stakers get pushed out of the validator set, while large operators and LSTs remain viable.

To show it more explicitly I have prepared a couple of plots of tempered issuance. But all other issuance curve variants that taper out slowly suffer the same fate.

First let me show the issuance curve I'm using. It's tempered issuance with the pre-factors of c and F set to their current values (2.6 and 64).

![tempered_issuance_plot|690x414](upload://5dJ9uao9t2Q97DoUcyspgZmy5gN.png)

The following plot shows the real yield. With real yield I mean issuance yield observed after costs and net of circulating supply changes.

![tempered_issuance_real_yield_plot|690x414](upload://jlSimHlQIyqJJwyZhiRmWBPjDxr.png)

As you can see, home validators become uneconomical around 60M ETH staked. But holding an LST is still economically viable until well over 110M ETH staked. To be more concrete, when a validator crosses the zero line it means that after costs he is earning ETH at a slower rate than the circulating supply inflates.

The issue is that if we ever cross 60M staked ETH, solo validators will progressively become pushed out of the validator set. Either because they unplug the machines seeing after costs they can't even outrun inflation or slowly, because centralized operator are still economical and gaining a greater share of the pie.

Perhaps a bit unintuitively, the hard cap issuance curves protect solo validators better. If the issuance curve tapers down sufficiently aggressive, all types of validators cross the 0 line sufficiently close.

The following is an example of such an issuance curve, just to exemplify the effect I refer to: 

![ethereum_issuance_with_burn_plot_2|690x414](upload://8qSGWDxTfYQFd16CQ2BlcELHGGJ.png)


And here the real yield (net of costs and circulating supply changes):

![ethereum_real_yield_with_burn_plot_2|690x414](upload://pq9xjEA8b99Bnsdf3Ds2rL1LM7m.png)


As you can see the gap between home stakers and LST holders can be made quite small. This helps protect solo stakers because they remain economically viable until pretty much the same stake rate.

I would argue we should go for the hard cap issuance curves. Coupled with uncorrelation incentives that help buff up uncorrelated validators.

For more details about how I calculate the real yield of different types of validators check here: https://ethresear.ch/t/the-shape-of-issuance-curves-to-come/20405

-------------------------

aelowsson | 2024-10-30 00:20:28 UTC | #15

[quote="OisinKyne, post:8, topic:20747"]
> it does not fundamentally matter who runs the validator

Well then imo this might be where a model can be harmful rather than [useful ](https://en.wikipedia.org/wiki/All_models_are_wrong). It matters, at least to me, who runs the validator. If you just assume the staking providers raise their prices, you end up like [this situation ](https://en.wikipedia.org/wiki/Survivorship_bias#/media/File:Survivorship-bias.svg), with only the centralised entities remaining to offer services.
[/quote]

A misrepresentation or misunderstanding. The full statement is:

[quote="aelowsson, post:6, topic:20747"]
For the purpose of calculating the effect on welfare, it does not fundamentally matter who runs the validator. The staking service provider will pass on its costs to the delegator in the form of a staking fee. The delegator will make the decision to delegate stake based on the full cost (staking fee and, e.g., assigned risks), and the principle applies just the same.
[/quote]

The topic under discussion is the welfare gain from a cost reduction for the ETH token holder. It is desirable to be able to calculate this cost reduction, and it turns out that we can simply specify the cost as the reservation yield of the stake. The SSP will pass on its costs to the delegator, who will decide to stake when accounting for the fee of the SSP. We can thus rely on the integral of the supply curve for computing the aggregate cost. This is a separate topic from how the composition of the staking set is affected by a change in issuance policy. In this case, it is certainly important who runs the validator, as addressed throughout my responses and the FAQ. Indeed, this is the reason for why a stake capping strategy should potentially be avoided in my view.

[quote="OisinKyne, post:8, topic:20747"]
In this FAQ, it doesn’t make any reference to ‘home stakers’ (for the purpose of discussion, assume one or a group of people putting up < 32 eth for a validator, topped up with delegated stake, not a future orbit thing, or a 32 eth DV cluster of their own capital. Think rocketpool minipool squad). Where do they fit in with respect to your view of Ethereum’s goal below: (which i find far, far, too low of a goal for that matter)
[/quote]

I use the term solo staker to cast a wide net. For the sake of analysis, it is not critical if we are dealing with a squad staker or a small solo staker under Orbit SSF. My perspective was outlined in my previous answer. 

[quote="OisinKyne, post:8, topic:20747"]
> The full cost of operating stake is best approximated as the reservation yield associated with the stake, that is to say the lowest yield at which that ETH would be supplied as stake.

Idk, I think the best way to approximate the cost of operating stake is [primary research](https://paragraph.xyz/@ethstaker/staking-survey-2024) coupled with a model informed on this and other data (see later in post). The lowest yield at which Eth would be supplied as stake is a hypothetical/counterfactual we can’t answer as far as I know.
[/quote]

This is a misunderstanding of the topic being discussed in this part of the response. The topic is that the supply curve represents the cost of staking. For a better understanding, read my response to Keyneom starting here:

[quote="aelowsson, post:11, topic:20747"]
The supply curve indicates the amount of stake deposited $D$ at various staking yields $y$. It captures the implied marginal cost of staking. What that means is that every ETH holder is positioned along the supply curve according to how high cost they assign to staking, with their required yield implying that cost. Relevant costs include hardware and other resources, upkeep, the acquisition of technical knowledge, illiquidity, trust in third parties and other factors increasing the risk premium, various opportunity costs, taxes, etc. The area above the supply curve indicates the stakers’ surplus (what they actually gain) and the area below the supply curve the costs assigned to staking (the marginal staker would not stake at a yield below the supply curve).
[/quote]

Also review the associated figure.

[quote="OisinKyne, post:8, topic:20747"]
> The supply curve thus implies the marginal cost of staking, and the aggregate cost of staking becomes the integral of the supply curve.

You are arguing that the supply curve **should** dictate the cost of staking, I’m saying that would likely be bad for the **quality** of security of the network.
[/quote]

Also a misunderstanding of properties of the supply curve. Refer to my previous answer for an explanation of the topic being discussed.

[quote="OisinKyne, post:8, topic:20747"]
I don’t understand

1. why you don’t think yields can go ‘close to 0’ in your proposals (at least thats what i infer from the framing of the concern only ‘being valid’ in this case. and
2. “No SSP can reasonably outcompete all others at an equilibrium staking yield of, e.g., 2% at 30M ETH staked” why do you say this? And why does this impossibility of out-competition not hold at 34m and 2.5% like the current day?
[/quote]

1. The supply curve will go almost vertical at a high proportion staked. Think of all the people that wish to hold ETH on hand, that will find a 0.5% staking yield too low if they need to trust a third party with their ETH, etc. Or review the cryptocurrencies that do not reach the full supply staked even at a 5-10% yield.
2. It holds at both 2% and 2.5%, that's the point. A 0.5% issuance rate becomes a 2% issuance yield at 30M ETH staked. The discussion in that part of the text relates to the common suggestion during the debate at that time that striving for 30M staked is too low because then Coinbase may rely on economies of scale to outcompete all other SSPs. But this could only happen under a stake cap that targets a low stake. It is not a possible scenario under a more moderate reward curve because the staking yield would still be 2%.



[quote="OisinKyne, post:8, topic:20747"]
to me this sentence reads like we should be on the same page, that perfect competition is not a reasonable assumption, so we shouldn’t adopt a curve that tends towards maximal marginal competition and thus imperfect markets like oligopolies and monopolies.
[/quote]

[Perfect competition](https://en.wikipedia.org/wiki/Perfect_competition) is a term in economics, and my suggestion in this part is that staking services are not perfect substitutes:

[quote="aelowsson, post:1, topic:19675"]
Each SSP, reaching for a specific market segment, incurs unique costs besides the cost of running staking nodes, with a wide variety ranging from compliance to software. Indeed, CEXes have somewhat of a local monopoly on their customers-as-delegators, and the opportunity cost of keeping fees competitive with any onchain option is presumably so high that it does not represent the profit-maximizing strategy. What is clear is that competition for delegated stake will unfold across diverse market segments, and perfect competition is not a reasonable assumption.
[/quote]

One take-away is that fees will not be driven to zero.

[quote="OisinKyne, post:8, topic:20747"]
That is fair and I didn’t realise you were an author on the (V)Orbit work, I apologise.
[/quote]

Thanks. 

[quote="OisinKyne, post:8, topic:20747"]
Why the delineation between 1 and 32 and not a different level?..
[/quote]

I focus on 32 ETH as a natural baseline for historical reasons. It would be particularly painful to make many 32-ETH validators unprofitable from a decentralization perspective. I focus on 1 ETH as a natural lower bound in Orbit SSF designs.

[quote="OisinKyne, post:8, topic:20747"]
They do not make Ethereum cheaper, but inflationary, or ideally, dis-inflationary regimes would be better for the use of Ethereum than structural deflation.
[/quote]

Counterarguments [here](https://notes.ethereum.org/@anderselowsson/Foundations-of-MVI).

[quote="OisinKyne, post:8, topic:20747"]
..there is a long way to go in my eyes, before the Ethereum operator set becomes sufficiently decentralised for what it needs to be to be black swan secure, and I think bounding issuance, and making it even harder for marginal stakers to stay afloat, making distributed validators particularly economically non-viable at retail scale, will push Ethereum down the road I outlined in “[the staking problem](https://blog.goodaudience.com/the-staking-problem-9b1e344b24ab)”, which was more eloquently framed by Ameen, as USDC fork choice rule.
[/quote]

Great link! Interesting to read thinking from the early days. A relevant section to me would be this.

>They’re violating the rules they are supposed to abide by, but with 92% of all ether, who’s going to stop them? **“This is important”,** they say. Within minutes, a new longer chain has outpaced the fork that contains the hack, history has been rewritten, the world has collectively decided to forget those transactions.

While it is not perfectly clear if the author meant to refer to all ETH or all staked ETH, a key reason for MVI is precisely because of the fear that all ETH would be staked when some black swan event takes place. Consider the impact of a black swan event causing a chain split in this scenario. It would make it very hard for the community to come to social consensus. I'll quote my write-up from the MVI thread that outlined this idea:

>40. ...LST holders and any application or user who needs the LST to preserve its value will develop a shared destiny with both the LST and ultimately the LST issuing organization (the SSP).
>
>41. In the case of a mistake or misdeed, which may also take place at any mechanisms designed to regulate the organization (such as smart contracts, on-chain governance, or government regulations), Ethereum’s social layer may not have the capacity for appropriate (non) measures.
>
>42. It would require Ethereum to destroy a large part of itself. The affected users may prefer to reinterpret the mistake or misdeed as something entirely different. Once you become the money of Ethereum, you to some extent *become* the social layer.
>
>43. The money function is in this way a [Ryanian “stratum for cartelization”](https://notes.ethereum.org/@djrtwo/risks-of-lsd) that acts one layer above the various strata (e.g., MEV extraction, block-timing manipulation) that Ryan explores in his post on the risks of LSTs.
>
>44. We are no longer only concerning ourselves with the proportion of the staked ETH under an LST, but the proportion of the total ETH under an LST. The corrupted institution(s) correspondingly also sits one layer above the consensus mechanism, namely the social layer.
>
>45. It became apparent with The DAO that if the proportion of the total circulating supply affected by an outcome grows sufficiently large, then the “social layer” may waver on its commitment to the underlying intended consensus process.
>
>46. If the community can no longer effectively intervene in the event of for example a 51 % liveness attack, then risk mitigation in the form of the [warning system discussed by Buterin](https://www.youtube.com/watch?v=8DHGOlIlMvc&t=1938s) may not be effective.
>
>47. The consensus mechanism has in this case through derivatives grown so large and interconnected that it has overloaded its ultimate arbitrator, the social consensus mechanism. It is a special and sort of inverted case of [issues Buterin warned about](https://vitalik.ca/general/2023/05/21/dont_overload.html).

If the deposit ratio grows very high, it is reasonable to argue that Ethereum becomes less secure. We can avert this by reducing issuance.

[quote="OisinKyne, post:8, topic:20747"]
I am unconvinced that bounding issuance to `d` rather than `D` won’t cause ultra low cost validators driving the equilibrium APR to way lower than most seem to expect, resulting in a mono-culture of ~3/10 entities that can make profit at such low rates.
[/quote]

The switch to $d$ from $D$ will be done to preserve the same APR at the same proportion staked when Ethereum undergoes either deflation or inflation and follows analysis of Ethereum's circulating supply equilibrium. It will not lower APR in the way you fear.

-----

I will not have time to provide more answers going forward. I do find it desirable with an equilibrium staking yield above 1%, and also see this as the likely outcome from a change. But I also consider it a problem if the quantity of stake grows very large, which is why I think we should specify a lower issuance yield in this scenario, to stop the growth. This is a matter of trade-offs, where we must seek to balance many different priorities.

-------------------------

Zarevoks | 2024-10-30 14:42:09 UTC | #17

[quote="jwhelan72, post:16, topic:20747"]
Keep in mind that “solo stakers” are node operators first and foremost. Dropping the staking yield to less than 1% would drive many of them to become LST node operators in order to amplify the yield on their ETH, effectily killing solo staking as a class and driving more ETH into the hands of the LSTs. Solo stakers have much more in common with node operators (which they are) than LST holders (which they are not).
[/quote]


Part of the proposal is to from stake deposit size (D) to (d). Staking yield ≠ supply inflation.

My understanding is he is proposing caping supply inflation at 0.5% while at 1/4 eth staking yeild would be closer to 2%.

-------------------------

aelowsson | 2024-11-02 03:28:15 UTC | #18

[quote="jwhelan72, post:16, topic:20747, full:true"]

1. Keep in mind that “solo stakers” are node operators first and foremost. Dropping the staking yield to less than 1% would drive many of them to become LST node operators in order to amplify the yield on their ETH, effectily killing solo staking as a class and driving more ETH into the hands of the LSTs. Solo stakers have much more in common with node operators (which they are) than LST holders (which they are not).

2. Other protocols (e.g. Solana, Avalanche, etc.) have approx. 70% of their token supply staked without any problem. Why would Ethereum experience problems at those levels, particularly since it does not have onchain governance?

3. ETH’s value and the associated economic security of the entire network is based in part on the staking yield. Dropping that yield substantially is likely to undermine the economic security model of the entire network and lead to better secured competitor networks in the market. E.g. at current prices, Solana has $64 billion of economic security vs. Ethereum’s $97 billion of security. It’s close to being flippened already.

A solution looking for a problem.

[/quote]

Thanks for your comment. Please review the stated [motivation](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#why-should-ethereum-reduce-its-issuance-4) for a reduction in issuance. If you do not agree, you might wish to address the provided motivation. As outlined in the [answer](https://ethresear.ch/t/practical-endgame-on-issuance-policy/20747/11) to Keyneom, we can easily expect the implied cost reduction to be in the region of a billion dollars per year at the current token price. Since it is a yearly reduction, any [valuation of this improvement](https://ethresear.ch/t/maximum-viable-security-a-new-framing-for-ethereum-issuance/19992/5#h-4-our-framing-of-issuance-cost-is-reductive-and-only-focuses-on-taxes-6) would need to be at least an order of magnitude higher. Furthermore, as noted in the post: it is valuable to have trustless sound money as the primary currency in a decentralized economy. High issuance can lead a liquid staking token (LST) to [dominate as money ](https://x.com/weboftrees/status/1710712326117097785). Lower issuance ensures that app developers and users will not be subjected to monopolistic pressure from LST issuers, or needlessly risk the LST failing, potentially even threatening consensus if an LST becomes “[too big to fail ](https://x.com/weboftrees/status/1710713959362252884)”.

Also briefly around specific comments:

#### Point 1.

The supply curve would need to be quite a bit lower than today for the yield to drop under 1%. Refer to the full blue supply curve in the post that already is lower than the current supply curve, with the equilibrium staking yield still staying well above 1% in the practical endgame. 

I would consider it a bigger risk that solo stakers *stop* staking than *become* LST node operators. Julian’s [exposition](https://ethresear.ch/t/initial-analysis-of-stake-distribution/19014) of stake modalities can be useful for you to consider. It leads to the following theorem:

[quote="Julian, post:1, topic:19014"]

**Theorem 1.** The level of (issuance) yield does not affect the staking mediums used by individual stakers.

[/quote]

In essence, when applied to your suggestion, you can think of the analysis as stating in mathematical terms “if solo stakers can increase risk-adjusted rewards by becoming node operators, why aren’t they doing it right now?”

There are then potential [edge cases:](https://ethresear.ch/t/initial-analysis-of-stake-distribution/19014/10)

[quote="vshvsh, post:10, topic:19014"]
“I love to run a node, but not into a loss”
[/quote]

But these should not dominate. My point would be that focusing on if solo stakers might *stop* staking to a higher degree than delegating stakers at some specific yield is more important than if they *change modality*.

#### Point 2.

References to the motivation for an issuance reduction were provided at the beginning of my comment. Note that the motivation relates to structural aspects that lead to problems

* over long time-frames (too high costs degrading value of Ethereum),
* predominantly for cryptocurrencies with no native delegation (due to the proliferation of LST),
* evident in the event that something goes wrong and Ethereum must rely upon a social layer not caught up in the issue.

It is not like a bug that just crashes the system, more like memory leak. Furthermore, although cause and effect are difficult to separate, Ethereum is by far the most successful PoS cryptocurrency. It is therefore a hard sell to use less successful PoS cryptocurrencies with higher staking ratios as examples to strive for, if no other motivation is provided.

#### Point 3.

Ethereum should not harness people’s bounded understanding of yield, and keep it high to trick users into thinking that they gain something, when they do in fact not. Refer to [this](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#some-users-think-that-more-yield-is-more-fun-and-like-to-collect-yield-on-their-eth-why-not-lean-into-this-43) write-up. 

Furthermore, the goal is to ensure sufficient economic security; in essence, to keep Ethereum secure. Just as in any other endeavor, it is possible to pay too much. Paying too much can even make Ethereum less secure in the long run. Refer to [this](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#what-about-economic-security-more-stake-makes-ethereum-more-secure-right-8) write-up. 

I hope you have found some points in my comment worthy of further consideration.

-------------------------

