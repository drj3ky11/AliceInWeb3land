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