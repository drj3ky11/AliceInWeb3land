from web3 import Web3
import json


w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
UNISWAP_V2_ROUTER = Web3.to_checksum_address('0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D')

# ABI parcial
UNISWAP_ABI = json.loads('''[
    {
        "constant": false,
        "inputs": [
            {"name":"amountOutMin","type":"uint256"},
            {"name":"path","type":"address[]"},
            {"name":"to","type":"address"},
            {"name":"deadline","type":"uint256"}
        ],
        "name":"swapExactETHForTokens",
        "outputs": [{"name":"[]","type":"uint256[]"}],
        "payable": true,
        "stateMutability": "payable",
        "type":"function"
    },
    {
        "constant": false,
        "inputs": [
            {"name":"amountIn","type":"uint256"},
            {"name":"amountOutMin","type":"uint256"},
            {"name":"path","type":"address[]"},
            {"name":"to","type":"address"},
            {"name":"deadline","type":"uint256"}
        ],
        "name":"swapExactTokensForETH",
        "outputs": [{"name":"[]","type":"uint256[]"}],
        "payable": false,
        "stateMutability":"nonpayable",
        "type":"function"
    }
]''')

def get_swaps_in_block(block_number):
    swaps = []
    block = w3.eth.get_block(block_number, full_transactions=True)
    
    for tx in block.transactions:
        if tx['to'] and tx['to'].lower() == UNISWAP_V2_ROUTER.lower():
            try:
                # Decodificar la transacción
                contract = w3.eth.contract(address=UNISWAP_V2_ROUTER, abi=UNISWAP_ABI)
                func_obj, params = contract.decode_function_input(tx['input'])
                
                # Interpretar los parámetros
                swap_data = {
                    'tx_hash': tx['hash'].hex(),
                    'from': tx['from'],
                    'function': func_obj.fn_name,
                    'params': dict(params),
                    'value': w3.from_wei(tx['value'], 'ether'),
                    'block': block_number
                }
                swaps.append(swap_data)
                
            except Exception as e:
                print(f"Error decoding tx {tx['hash'].hex()}: {str(e)}")
    
    return swaps

def main():
    if not w3.is_connected():
        print("No se pudo conectar al nodo Ethereum")
        return

    latest_block = w3.eth.block_number
    start_block = max(0, latest_block - 50)

    print(f"Escaneando bloques del {start_block} al {latest_block}...")

    for block_num in range(start_block, latest_block + 1):
        swaps = get_swaps_in_block(block_num)
        if swaps:
            print(f"\nEncontradas {len(swaps)} swaps en el bloque {block_num}:")
            for swap in swaps:
                print(f"\nTransacción: {swap['tx_hash']}")
                print(f"Función: {swap['function']}")
                print(f"De: {swap['from']}")
                print(f"Valor: {swap['value']} ETH")
                print("Parámetros:")
                for key, value in swap['params'].items():
                    if isinstance(value, bytes):
                        value = value.hex()
                    print(f"  {key}: {value}")

if __name__ == "__main__":
    main()