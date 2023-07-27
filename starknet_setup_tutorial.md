# Starknet setup tutorial
In this tutorial we are going to install the [Starknet](https://www.starknet.io/en/what-is-starknet) CLI, deploy and interact with a Starknet smart contract.

This tutorial is for complete newcomers to Starknet and Linux, like me, therefore it is possible that some steps are redundand, or could be carried out in a more efficient way. For any clarification you can contact me at lapofalcone@gmail.com <sup>Possibly use TUTORIAL STARKNET as subject.</sub>

I've personally used these steps to install the CLI. By the way, take into account that Starknet is in development, therefore **things may change quickly** (I published this tutorial In July 2023, as part of [a report about the usage of blockchains for videogames](https://github.com/Lapo9/Layer-2-Blockchains-for-Videogames)).

For example, in this tutorial we install [Cairo](https://book.cairo-lang.org/) (the language in which to write smart contracts on Starknet) version 1.1.1. By the way Starknet will soon support Cairo 2.x.

Users can interact with Starknet via a CLI available for Linux and MacOS. We are going to
see how to create a smart contract and interact with it in Linux.

## Prerequisites
We are going to work on a clean installation of Ubuntu 22.04.2 LTS, installed on a virtual
machine in VirtualBox.

## Install Python3.9
As of July 2023, Starknet CLI can work with Python3.9, but not with Python3.10 yet. Since
Python3.10 is the default version on Ubuntu 22.04.2, we must install Python3.9 and create
a virtual environment for it.
```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa # Python3 .9 is not directly available
sudo apt install python3.9
python3.9 --version # should return Python 3.9.1x
```

Then we have to install some Python3.9 modules:
```bash
sudo apt-get install python3.9-distutils # necessary to install some other modules
sudo apt-get install python3.9-dev # necessary to install some other modules
sudo apt-get install python3.9-venv #to create virtual environments 
```

Now we can create the virtual environment and activate it:
```bash
python3.9 -m venv ∼/cairo_venv
source ∼/cairo_venv/bin/activate
# next lines in the terminal should start with ( cairo_venv )
```

From now on all commands will be run inside the virtual environment, where the default
version of Python is 3.9.

## Install Cairo and Starknet
First, we have to install these dependencies:
```bash
sudo apt install -y libgmp3-dev #for multiple precision arithmetic
sudo apt install git #will be used later on
curl --proto ’= https ’ --tlsv1.2 -sSf https://sh.rustup.rs | sh #Rust
pip install wheel #install if the installation of fastecdsa fails
pip install ecdsa #cryptographic algorithm
pip install fastecdsa #cryptographic algorithm
pip install sympy #symbolic math
```

Now we can install the Starknet CLI:
```bash
pip install cairo-lang
starknet --version #should return 0.12.0
```

And the Cairo compiler <sup>I found out that there is a bug preventing using mappings (`LegacyMapping`) inside contracts. A
workaround is to comment out line 71 at `.cairo/crates/cairo-lang-sierra-gas/src/gas_info.rs`. The
underlying problem has something to do with a check on the estimated gas consumed by the contract.</sup>

```bash
git clone https://github.com/starkware-libs/cairo/.cairo #we download the repo to ∼/.cairo
cd .cairo #we move to the newly created folder
git checkout tags/v1.1.1 #we move to the release branch, v1.1.1 is the last supported version on Starknet
cargo build --all --release #we build the compiler via Cargo
cd .. #we move back to the home folder
```

## Setting up environment variables
To set permanent environment variables we have to append content to `~\.bashrc` file:
```bash
nano ∼/.bashrc # open .bashrc with a text editor
```

Now write these variables at the end of the file:
```bash
export STARKNET_NETWORK=alpha-goerli #the Starknet network we will use (in this case thetestnet)
export STARKNET_WALLET=starkware.starknet.wallets.open_zeppelin.OpenZeppelinAccount #the service to create account contract
export CAIRO_COMPILER_DIR=∼/.cairo/target/release/ #where Cairo compiler is placed
export CAIRO_COMPILER_ARGS=--add-pythonic-hints #Cairo compiler options
```

Now press `Ctrl + X`, then `y` and finally `Enter`.

Now close and re-open the terminal (don’t forget to re-activate the virtual environment when
you re-open the terminal).

You can test if the environment variables we added exist with the command `printenv`.

## Creating an account
To create a Starknet account:
```bash
starknet new_account --account myAccountName
```

This will generate the address and the public-private key pair of the account, which will be
printed in the terminal and also saved to
`~/.starknet_accounts/starknet_open_zeppelin_accounts.json`.

Now we have to add some funds to the account, so that we can use them to deploy the
account contract.

To do so we can use any Starknet faucet, for example: https://faucet.goerli.starknet.
io/.

Then we can check on https://starkscan.co/ that the transaction with the funds is at
least in Pending state.

At this point, we can deploy the account:
```bash
starknet deploy_account --account myAccountName
```

This will return the transaction hash: we must wait until the transaction is accepted on
layer 2.

## Deploying and interacting with a smart contract
To deploy a smart contract, first, we must have some Cairo code. There are some examples
online, such as https://github.com/starknet-edu/deploy-cairo1-demo.

Let’s say we have the code for the contract at `~/src/myContract.cairo`.

First, we have to compile the Cairo code into Sierra bytecode:
```bash
∼/.cairo/target/release/starknet -compile ∼/src/myContract.cairo ∼/src/myContract.json
```

Then, we have to declare the smart contract. This will create a Class object in Starknet,
which is a template containing our code:
```bash
starknet declare -- contract ∼/src/myContract.json --account myAccountName
```

Now we have to wait until the transaction declaring the contract is accepted on layer 2.

Eventually, we have to deploy the contract. A smart contract will be created starting from
the Class.
```bash
starknet deploy --class_hash HASH_OF_THE_PREVIOUSLY_CREATED_CLASS --inputs CONSTRUCTOR_ARGS --account myAccountName
```

As soon as the deploying transaction is accepted on layer 2, we can interact with the account:
```bash
starknet invoke --address SC_ADDRESS --function FUNCTION_NAME --inputs FUNCTION_ARGS --account myAccountName
```

And we can also interact with the read-only functions of the contract via:
```bash
starknet call --address SM_ADDRESS --function FUNCTION_NAME --inputs FUNCTION_ARGS --account myAccountName
```
