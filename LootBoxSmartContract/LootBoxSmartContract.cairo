#[contract]
mod LootBox {
    use starknet::get_execution_info;
    use starknet::ContractAddress;
    use traits::Into;
    use box::BoxTrait;
    use option::OptionTrait;

    struct Storage {
        usersTokens: LegacyMap<ContractAddress, u256>,
        usersGems: LegacyMap<ContractAddress, u256>,
        usersGold: LegacyMap<ContractAddress, u256>
    }

    #[constructor]
    fn constructor(masterAddress: ContractAddress) {
        usersTokens::write(masterAddress, 1000000); //make the owner rich
    }

    #[event] //signal loot box opening (currency: 0 = gems, 1 = gold)
    fn lootBoxResult(user: ContractAddress, currency: u8, amount: u256, remainingTokens: u256){}

    #[event] //signal error
    fn notEnoughTokens(user: ContractAddress, remainingTokens: u256){}

    #[event] //tokens sent
    fn tokensSent(sender: ContractAddress, receiver: ContractAddress, remainingTokens: u256){}
    

    #[external]
    fn buyLootBox() {
        let userAddress = get_execution_info().unbox().caller_address; //get user address
        let availableTokens = usersTokens::read((userAddress)); //extract how many tokens the user has

        //execute contract only if the user has enough tokens (assert is very buggy on this version of Starknet, it would be a better option)
        if availableTokens > 0 {
            //pay 1 token
            usersTokens::write(userAddress, usersTokens::read((userAddress)) - 1);

            //here we extract a pseudo random number, based on the hash of the incoming transaction
            let transactionHash = get_execution_info().unbox().tx_info.unbox().transaction_hash; //get the hash of the transaction
            let transactionHash256: u256 = transactionHash.into(); //cast the hash to a 256 integer
            let random = transactionHash256 & 0xfff; //keep only the last 2 digits (range from 0 to 256)
            
            //25% chance of getting gems
            if (random & 0xf) < 4 {
                usersGems::write(userAddress, usersGems::read((userAddress)) + random); //add gems to account
                lootBoxResult(userAddress, 0, random, availableTokens-1);  //signal event
            }
            else {
                usersGold::write(userAddress, usersGold::read((userAddress)) + random); //add gold to account
                lootBoxResult(userAddress, 1, random, availableTokens-1); //signal event
            }
        }
        else {
            notEnoughTokens(userAddress, availableTokens); //error
        }
    }

    #[external]
    fn sendTokens(receiverAddress: ContractAddress, amount: u256) {
        let userAddress = get_execution_info().unbox().caller_address; //get user address
        let availableTokens = usersTokens::read((userAddress)); //extract how many tokens the user has
        if availableTokens < amount {
            notEnoughTokens(userAddress, availableTokens);
        }
        else {
            usersTokens::write(userAddress, availableTokens - amount); //remove tokens from user
            usersTokens::write(receiverAddress, usersTokens::read((receiverAddress)) + amount); //add tokens to the receiver
            tokensSent(userAddress, receiverAddress, availableTokens - amount);
        }
    }

    #[view]
    fn getUserAssets(userAddress: ContractAddress) -> (u256, u256, u256) {
        let tokens = usersTokens::read((userAddress));
        let gems = usersGems::read((userAddress));
        let gold = usersGold::read((userAddress));
        return (tokens, gems, gold);
    }

    #[view]
    fn getLootBoxPrice() -> u256 {
        1
    }
}