from web3 import Web3

# Configuración inicial
NODE_URL = "http://localhost:8545"
DIRECCION = "0x016606Acc6B0cFE537acc221e3bf1bb44B4049Ee"  # Reemplaza con tu dirección
USDT_CONTRACT = "0xdAC17F958D2ee523a2206206994597C13D831ec7"  # USDT en mainnet
USDC_CONTRACT = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"  # USDC en mainnet

# Conectar al nodo
w3 = Web3(Web3.HTTPProvider(NODE_URL))

def get_eth_balance(address):
    balance_wei = w3.eth.get_balance(address)
    return Web3.from_wei(balance_wei, "ether")

def get_erc20_balance(contract_address, address, decimals=6):
    # ABI mínima para balanceOf y decimals
    abi = '''[
        {"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"},
        {"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"type":"function"}
    ]'''
    
    contract = w3.eth.contract(address=contract_address, abi=abi)
    
    # Obtener decimales del token (normalmente 6 para USDT/USDC)
    try:
        decimals = contract.functions.decimals().call()
    except:
        pass  # Usamos el valor por defecto si falla
    
    # Obtener balance
    balance = contract.functions.balanceOf(address).call()
    return balance / 10**decimals

if __name__ == "__main__":
    if w3.is_connected():
        print(f"Conectado a Ethereum Mainnet (Último bloque: {w3.eth.block_number})")
        
        # Balance de ETH
        eth_balance = get_eth_balance(DIRECCION)
        print(f"\nBalance ETH: {eth_balance:.6f}")
        
        # Balance de USDT
        usdt_balance = get_erc20_balance(USDT_CONTRACT, DIRECCION)
        print(f"Balance USDT: {usdt_balance:.2f}")
        
        # Balance de USDC
        usdc_balance = get_erc20_balance(USDC_CONTRACT, DIRECCION)
        print(f"Balance USDC: {usdc_balance:.2f}")
    else:
        print("Error de conexión al nodo")