import asyncio
import time
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.account.account import Account
from starknet_py.net.models.chains import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair
from starknet_py.contract import Contract
import PySimpleGUI as gui
import webbrowser

TOKENS_SENT = 0x26c7b52e2b50adbd331df67ab21e2c6448783a7b442ac0a0b7afaae2ef88ce
LOOTBOX_BOUGHT = 0x3e98c04afc3e9e5e8d2ce01282731f4886c1ba831261c580d0947c3e0319d9a
NOT_ENOUGH_TOKENS = 0x18b7f21fbc0b80823453c69654ad2c81e059000ef43a6f87b354b45a5ebc279

node = FullNodeClient(node_url="https://starknet-goerli.infura.io/v3/dda8ef6575244eb7a7214cca1b4c822c")

account = Account(
    client=node,
    address="0x04415e87ae0acd543f309ac5381881fa254ae6eba6ff47aaf23a3e3894cc9991",
    key_pair=KeyPair(private_key=0x4c8f535679a167b3b25eed4cccfea27c0368e4765a26d9c1cf1e41ab20f5387, public_key=0x549d8254c94993bbd90d0fcb78f3e9a48dba2e9987b1fd4bd4fc67957b8e75e),
    chain=StarknetChainId.TESTNET,
)

contractAddress = 0x070356a6f62cfe0cdcdb0fd9a7e95baefca1a88bef10612b7a5d50fd6abe2343
contract = Contract.from_address_sync(address=contractAddress, provider=account)

playerAddress = 0x04415e87ae0acd543f309ac5381881fa254ae6eba6ff47aaf23a3e3894cc9991

#buys a loot box and returns whether the transaction succeded or not, and the transaction hash
def buyLootBox():
    invocation = contract.functions["buyLootBox"].invoke_sync(max_fee=int(1e15))
    
    #keep looking for the transaction hash
    transactionFound = False
    while (not transactionFound):
        try:
            event = node.get_transaction_receipt_sync(invocation.hash).events[0] #try to get the transaction from the node
        except:
            time.sleep(1) #if you can't get it, wait 1 second and retry
        else:
            transactionFound = True
    
    #success
    if (event.keys[0] == LOOTBOX_BOUGHT):
        lootboxResult = (event.data[1], event.data[2], event.data[4])
        return (True, hex(invocation.hash), lootboxResult)
    #failure
    else:
        return (False, hex(invocation.hash), (0,0,0))


def sendTokens(address, amount):
    invocation = contract.functions["sendTokens"].invoke_sync(address, amount, max_fee=int(1e15))
    
    #keep looking for the transaction hash
    transactionFound = False
    while (not transactionFound):
        try:
            event = node.get_transaction_receipt_sync(invocation.hash).events[0] #try to get the transaction from the node
        except:
            time.sleep(1) #if you can't get it, wait 1 second and retry
        else:
            transactionFound = True
    
    #success
    if (event.keys[0] == TOKENS_SENT):
        transferResult = (event.data[0], event.data[1], event.data[2])
        return (True, hex(invocation.hash), transferResult)
    #failure
    else:
        return (False, hex(invocation.hash), (0,0,0))


async def getPlayerAssets(address):
    return await contract.functions["getUserAssets"].call(address)


async def getLootBoxPrice():
    return await contract.functions["getLootboxPrice"].call()





font = ("Courier New", 16)

gui.theme("DarkBlue")
sendLayout =    [
                    [
                        gui.Text("Receiver:", font=font),
                        gui.In(size=(50,3), enable_events=True, key="RECEIVER", font=font)
                    ],
                    [
                        gui.Text("Amount:", font=font),
                        gui.In(size=(10,3), enable_events=True, key="AMOUNT", font=font)
                    ],
                    [gui.Button("Send tokens", font=font, key="SEND"), gui.Image("./images/hourglass.png", visible=False, key="SENDING", size=(50,50))]
                ]
assetsLayout =  [
                    [gui.Image("./images/token.png", key="TOKEN_ICON", size=(50,50)), gui.Text("0", font=font, key="TOKENS")],
                    [gui.Image("./images/gold.png", key="GOLD_ICON", size=(50,50)), gui.Text("0", font=font, key="GOLD")],
                    [gui.Image("./images/gem.png", key="GEM_ICON", size=(50,50)), gui.Text("0", font=font, key="GEMS")],
                ]
boxLayout =     [
                    [gui.Text("Last box", font=("Courier New", 20, "underline"))],
                    [gui.Text("", font=font, key="BOX_CONTENT"), gui.Image("./images/missing.png", key="BOX_CONTENT_IMG", size=(50,50))],
                    [gui.Button("Open!", font=font, key="OPEN"), gui.Image("./images/hourglass.png", visible=False, key="OPENING", size=(50,50))]
                ]
viewLayout =    [
                    [gui.Button("View contract", font=font, key="VIEW_CONTRACT")], 
                    [gui.Button("View last transaction", font=font, key="VIEW_TRANSACTION")]
                ]
layout =    [
                [
                    [gui.Text("Layer 2 loot boxes", font=("Arial", 30))], 
                    [gui.HSeparator()],
                    [gui.Column(assetsLayout), gui.VSeparator(), gui.Column(boxLayout), gui.VSeparator(), gui.Column(viewLayout)],
                    [gui.HSeparator()],
                    [sendLayout]
                ]
            ]
window = gui.Window(title="Loot boxes", layout=layout, margins=(100,50))

async def main():
    window.read()
    await updateAssets()
    
    lastTransaction = 0x0 #stores the last transaction hash, in order to show it when "View last transaction" is clicked
    while not window.was_closed():
        event, values = window.read()
        if (event == "VIEW_CONTRACT"):
            webbrowser.open("https://testnet.starkscan.co/contract/" + hex(contractAddress)) #open starkscan page
        elif (event == "VIEW_TRANSACTION"):
            webbrowser.open("https://testnet.starkscan.co/tx/" + lastTransaction) #open starkscan page
        elif (event == "SEND"):
            window["SENDING"].update(visible=True) #show hourglass
            window["SEND"].update(disabled=True) #disable button until the transaction is complete
            window.perform_long_operation(lambda: sendTokens(int(values["RECEIVER"], 16), int(values["AMOUNT"], 10)), "TOKEN_SENT") #initiate token sending operation (will cast a TOKEN_SENT event when done)
        elif (event == "OPEN"): #initiate box opening operation (will cast a LOOTBOX_BOUGHT event when done)
            window["OPENING"].update(visible=True) #show hourglass
            window["OPEN"].update(disabled=True) #disable button until the transaction is complete
            window.perform_long_operation(lambda: buyLootBox(), "LOOTBOX_BOUGHT")
        elif (event == "TOKEN_SENT"):
            window["SENDING"].update(visible=False) #hide hourglass
            success, transaction, transferResult = values["TOKEN_SENT"] #get return value
            lastTransaction = transaction #set last transaction
            if (success):
                _, _, remainingTokens = transferResult
                window["TOKENS"].update(remainingTokens) #update the text of the tokens (we avoid calling updateAssets since we already have all the values)
            window["SEND"].update(disabled=False) #re-enable button
        elif (event == "LOOTBOX_BOUGHT"):
            window["OPENING"].update(visible=False) #show hourglass
            success, transaction, lootboxContent = values["LOOTBOX_BOUGHT"] #get return value
            lastTransaction = transaction #update last transaction
            if (success):
                currency, amount, _ = lootboxContent
                window["BOX_CONTENT"].update(amount) #update box content text
                #update box content image
                if (currency == 0):
                    window["BOX_CONTENT_IMG"].update(filename="./images/gem.png")
                elif (currency == 1):
                    window["BOX_CONTENT_IMG"].update(filename="./images/gold.png")
                await updateAssets() #update player's assets text
            window["OPEN"].update(disabled=False) #re-enable button



#update text based on received assets
async def updateAssets():
    tokens, gems, gold = (await getPlayerAssets(playerAddress))[0] #get the assets of the player
    window["TOKENS"].update(tokens)
    window["GOLD"].update(gold)
    window["GEMS"].update(gems)

if __name__ == "__main__":
    asyncio.run(main())
