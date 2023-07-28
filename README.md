# [Layer 2 Blockchains for Videogames](https://github.com/Lapo9/Layer-2-Blockchains-for-Videogames/blob/master/Latex/Layer%202%20blockchains%20for%20videogames.pdf)
As of July 2023, blockchains are becoming increasingly popular, and they are starting to be used in many different fields.

**Videogaming is one such field.**

In [this report](https://github.com/Lapo9/Layer-2-Blockchains-for-Videogames/blob/master/Latex/Layer%202%20blockchains%20for%20videogames.pdf) it will be explored:
- How a blockchain can be used in the world of videogames
- Why more scalable **layer 2** blockchains are needed
- What are **rollups** and why they are particularly well suited for videogames
- What is [**Starknet**](https://www.starknet.io/en/what-is-starknet) and how to deploy a smart contract on it
- A simple implementation of a Starknet [**smart contract to open loot boxes**](https://github.com/Lapo9/Layer-2-Blockchains-for-Videogames/blob/master/LootBoxSmartContract/LootBoxSmartContract.cairo) in a completely transparent way (and a [demo client](https://github.com/Lapo9/Layer-2-Blockchains-for-Videogames/blob/master/LootBoxSmartContract/LootBoxClient.py) to use this smart contract)

![](https://github.com/Lapo9/Layer-2-Blockchains-for-Videogames/blob/master/figures/logo.png)

## Table of contents
### Part I - Blockchain concepts and their limitations
- What is a blockchain 5
    - Transactions
    - Miners
    - Proof of work
    - Journey of a transaction
    - Blockchain programmability
    - Tokens
- Why blockchain can be used in videogames
- Why blockchain cannot be used in videogames
### Part II - Blockchain: layer 2
- Off-chain state channels 12
    - State channels and videogames
- Sidechains
- Rollups
    - Optimistic rollups
        - Entering an optimistic rollup
        - Exiting an optimistic rollup
        - L2 - L1 interaction
        - Optimistic rollups and videogames
    - Zero-knowledge rollups
        - Entering a ZK rollup
        - Exiting a ZK rollup
        - L2 - L1 interaction
        - Intuition on the validity proofs
        - ZK rollups and videogames
### Part III - Starknet
- Account abstraction
- Starknet actors
    - Sequencers
    - Provers
    - Nodes
- Transaction journey
- Starknet setup
    - Prerequisites
    - Install Python3.9
    - Install Cairo and Starknet
    - Setting up environment variables
    - Creating an account
    - Deploying and interacting with a smart contract
- Cairo
    - General concepts
    - Storage
    - Contract sections
### Part - IV - Implementation: immutable loot boxes
- Problem statement
- The smart contract
- The client
### Part V - Appendix
- Merkle trees
  - Merkle proof
