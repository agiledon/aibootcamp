# Delete Entities
This topic describes how to delete entities in Milvus.

Milvus supports deleting entities by primary key or complex boolean expressions. Deleting entities by primary key is much faster and lighter than deleting them by complex boolean expressions. This is because Milvus executes queries first when deleting data by complex boolean expressions.

Deleted entities can still be retrieved immediately after the deletion if the consistency level is set lower than Strong.
Entities deleted beyond the pre-specified span of time for Time Travel cannot be retrieved again.
Frequent deletion operations will impact the system performance.

Before deleting entities by comlpex boolean expressions, make sure the collection has been loaded.
Deleting entities by complex boolean expressions is not an atomic operation. Therefore, if it fails halfway through, some data may still be deleted.
Deleting entities by complex boolean expressions is supported only when the consistency is set to Bounded. For details, see Consistency.
## Prepare boolean expression
Prepare the boolean expression that filters the entities to delete.

Milvus supports deleting entities by primary key or complex boolean expressions. For more information on expression rules and supported operators, see Boolean Expression Rules.

### Simple boolean expression
Use a simple expression to filter data with primary key values of 0 and 1:

```python
expr = "book_id in [0,1]"
```

### Complex boolean expression
To filter entities that meet specific conditions, define complex boolean expressions.

Filter entities whose word_count is greater than or equal to 11000:

```python
expr = "word_count >= 11000"
```

Filter entities whose book_name is not Unknown:

```python
expr = "book_name != Unknown"
```

Filter entities whose primary key values are greater than 5 and word_count is smaller than or equal to 9999:

```python
expr = "book_id > 5 && word_count <= 9999"
```

## Delete entities
Delete the entities with the boolean expression you created. Milvus returns the ID list of the deleted entities.
```python
from pymilvus import Collection
collection = Collection("book")      # Get an existing collection.
collection.delete(expr)
```

Parameter	Description
expr	Boolean expression that specifies the entities to delete.
partition_name (optional)	Name of the partition to delete entities from.


# Upsert Entities
This topic describes how to upsert entities in Milvus.

Upserting is a combination of insert and delete operations. In the context of a Milvus vector database, an upsert is a data-level operation that will overwrite an existing entity if a specified field already exists in a collection, and insert a new entity if the specified value doesn’t already exist.

The following example upserts 3,000 rows of randomly generated data as the example data. When performing upsert operations, it's important to note that the operation may compromise performance. This is because the operation involves deleting data during execution.

## Prepare data
First, prepare the data to upsert. The type of data to upsert must match the schema of the collection, otherwise Milvus will raise an exception.

Milvus supports default values for scalar fields, excluding a primary key field. This indicates that some fields can be left empty during data inserts or upserts. For more information, refer to Create a Collection.

```python
# Generate data to upsert

import random
nb = 3000
dim = 8
vectors = [[random.random() for _ in range(dim)] for _ in range(nb)]
data = [
    [i for i in range(nb)],
    [str(i) for i in range(nb)],
    [i for i in range(10000, 10000+nb)],
    vectors,
    [str("dy"*i) for i in range(nb)]
]
```
## Upsert data
Upsert the data to the collection.

```python
from pymilvus import Collection
collection = Collection("book") # Get an existing collection.
mr = collection.upsert(data)
```

Parameter	Description
data	Data to upsert into Milvus.
partition_name (optional)	Name of the partition to upsert data into.
timeout (optional)	An optional duration of time in seconds to allow for the RPC. If it is set to None, the client keeps waiting until the server responds or error occurs.
After upserting entities into a collection that has previously been indexed, you do not need to re-index the collection, as Milvus will automatically create an index for the newly upserted data. For more information, refer to Can indexes be created after inserting vectors?

## Flush data
When data is upserted into Milvus it is updated and inserted into segments. Segments have to reach a certain size to be sealed and indexed. Unsealed segments will be searched brute force. In order to avoid this with any remainder data, it is best to call flush(). The flush() call will seal any remaining segments and send them for indexing. It is important to only call this method at the end of an upsert session. Calling it too often will cause fragmented data that will need to be cleaned later on.

## Limits
Updating primary key fields is not supported by upsert().
upsert() is not applicable and an error can occur if autoID is set to True for primary key fields.