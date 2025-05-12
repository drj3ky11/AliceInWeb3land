Some notes taken from the yellow paper

## Understanding the yellow paper

**Two basic functions; the first being a globally accessible singleton state, and the second being a virtual machine that applies changes to that state.**
The Ethereum network is subservient to others in terms of one thing only: ether, the native currency for Ethereum. Everything the system can do is bounded up in its ability to expend ether in exchange for gas, which buys a particular amount of system performance in some desired direction

*One to rule them all...*

The world state is a mapping of Ethereum addresses to accounts. Such a mapping consists of two things:

1. addresses
2. account states

1.2 the key functionality of a blockchain with a Turing-complete language and an effectively unlimited inter-transaction storage capability remains unchanged.

2 the key functionality of a blockchain with a Turing-complete language and an effectively unlimited inter-transaction storage capability remains unchanged.
Transactions thus represent a **valid** arc between two states.

4 **World State**. The world state (state), is a mapping between addresses (160-bit identifiers) and account states (a data structure serialised as RLP, see Appendix B).
Though not stored on the blockchain, it is assumed that the implementation will maintain this mapping in a modified Merkle Patricia tree (trie, see Appendix D). The trie requires a simple database backend that maintains a mapping of byte arrays to byte arrays; we name this underlying database the state database.

The account state, σ[a], comprises the following four fields:

* **nonce**: A scalar value equal to the number of transactions sent from this address. For account of address a in state σ, this would be formally denoted σ[a]n
* **balance**: A scalar value equal to the number of Wei owned by this address. Formally denoted σ[a]b .
* **storageRoot**: A 256-bit hash of the root node of a Merkle Patricia tree that encodes the storage contents of the account (a mapping between 256-bit integer values), encoded into the trie as a mapping from the Keccak 256-bit hash of the 256-bit integer keys to the RLP-encoded 256-bit integer values. The hash is formally denoted σ[a]s
* **codeHash**: The hash of the EVM code of this account—this is the code that gets executed should this address receive a message call. All such code fragments are contained in the state database under their corresponding hashes for later retrieval. This hash is formally denoted σ[a]c , and thus the code may be denoted as b, given that KEC(b) = σ[a]c .

**The Transaction**. A transaction (formally, T ) is a single cryptographically-signed instruction constructed by an actor externally to the scope of Ethereum.
+ type: EIP-2718 transaction type; formally Tx
+ nonce: A scalar value equal to the number of transactions sent by the sender; formally Tn .
+ gasPrice Tp
+ gasLimit Tg
+ to
+ value in Wei
+ r, s: Values corresponding to the signature of the transaction and used to determine the sender of the transaction
+ accessList
+ chaiId
+ yParity
Legacy transactions do not have an accessList (TA =()), while chainId and yParity for legacy transactions are combined into a single value.

Additionally, a contract creation transaction (regardless whether legacy or EIP-2930) contains:
**init**: An unlimited size byte array specifying the EVM-code for the account initialisation procedure, formally Ti .
init is an EVM-code fragment; it returns the *body*, a second fragment of code that executes each time the account receives a message call (either through a transaction or due to the internal execution of code). init is executed only once at account  reation and gets discarded immediately thereafter.
In contrast, a message call transaction contains:
**data**: An unlimited size byte array specifying the input data of the message call, formally Td .


**The Block**. The block in Ethereum is the collection of relevant pieces of information (known as the block header ), H, together with information corresponding to the comprised transactions, T, and a set of other block headers U that are known to have a parent equal to the present block’s parent’s parent (such blocks are known as
ommers 2).
+ parentHash: The Keccak 256-bit hash of the parent block’s header, in its entirety
+ ommersHash: The Keccak 256-bit hash of the ommers list portion of this block
+ beneficiary: The 160-bit address to which all fees collected from the successful mining of this block be transferred
+ stateRoot
+ transactionsRoot
+ receiptsRoot
+ logsBloom
+ difficulty
+ number
+ gasLimit
+ gasUsed
+ timestamp
+ extraData
+ mixHash: A 256-bit hash which, combined with the nonce, proves that a sufficient amount of compu tation has been carried out on this block; formally Hm
+ nonce: A 64-bit value which, combined with the mixhash, proves that a sufficient amount of computation has been carried out on this block; formally Hn .

### Transaction

The execution of a transaction is the most complex part of the Ethereum protocol: it defines the state transition function Υ. It is assumed that any transactions executed
first pass the initial tests of intrinsic validity. These include:
(1) The transaction is well-formed RLP, with no additional trailing bytes;
(2) the transaction signature is valid;
(3) the transaction nonce is valid (equivalent to the sender account’s current nonce);
(4) the sender account has no contract code deployed (see EIP-3607 by Feist et al. [2021]);
(5) the gas limit is no smaller than the intrinsic gas, g0 , used by the transaction; and
(6) the sender account balance contains at least the cost, v0 , required in up-front payment.

## Execution Model
The execution model specifies how the system state is altered given a series of bytecode instructions and a small tuple of environmental data.
