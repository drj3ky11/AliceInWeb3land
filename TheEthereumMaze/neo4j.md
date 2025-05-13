Desde la web, con Aura, para no complicar. Si el proyecto escala hay que hacer instalación. Pero las ordenes a cypher son iguales.

```
CREATE CONSTRAINT IF NOT EXISTS FOR (w:Wallet) REQUIRE w.address IS UNIQUE;
```

```
LOAD CSV WITH HEADERS FROM 'https://url-a-tu-csv.csv' AS row
MERGE (origen:Wallet {address: row.Origen})
MERGE (destino:Wallet {address: row.Destino})
CREATE (origen)-[tx:SENT {
  tx_hash: row.`Hash TX`,
  amount: toFloat(row.Cantidad),  // Conversión a número
  token: row.Token
}]->(destino);
```

Podemos visualizar:

```
MATCH (origen:Wallet)-[tx:SENT]->(destino:Wallet)
RETURN origen, tx, destino
LIMIT 50;  // Ajusta según necesidad
```

Buscando un destinatario común a dos wallets:

```
MATCH (w1:Wallet {address: "0xe96be9e5c26c06808eb05dd8cb022908f06eb995"})-[:SENT]->(comun:Wallet)<-[:SENT]-(w2:Wallet {address: "0x69046cae1f50a19dcbbeb4eb888f503bb26aae1e"})
RETURN 
  w1.address AS Emisor1,
  w2.address AS Emisor2,
  comun.address AS DestinoComun,
  [(w1)-[tx1:SENT]->(comun) | {hash: tx1.tx_hash, cantidad: tx1.amount, token: tx1.token}] AS TransaccionesDesdeW1,
  [(w2)-[tx2:SENT]->(comun) | {hash: tx2.tx_hash, cantidad: tx2.amount, token: tx2.token}] AS TransaccionesDesdeW2
  ```
  