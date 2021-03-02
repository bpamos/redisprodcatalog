# redisprodcatalog
Redis Product Catalog

## Product Catalog Use Case

In the last session several common Redis use cases were discussed. Now, lets consider using Redis as our primary database for a product catalog for a new online store. It will need to store product details including a name, description, vendor, price, main category and some images.


## Requirements:

* Product information stored in the database should include: name, description, vendor, price, category, images associated with that product.
* Ability to create/update/delete product details
* Ability to find product by ID
* Ability to find products in category X
* Ability to find product by its name or part of its name


## Logical Data Model:

The logical data model is separate from the DBMS being used.
It defines the structure of data elements and to set relationships between them.

* Product Image
    * Id: Number
    * Value: Binary

* Product
    * Id: Number
    * Name: String
    * Description: String
    * Vendor: String
    * Price: Number
    * Currency: String
    * MainCategory: Category (1)
    * Images: Image (0..n)
 
* Category
    * id: Number
    * Name: String
    * Products: Product (0..n)

# Installation

---
Prerequisites: 
* Python 3.8 or later
* Redis OSS and RediSearch
* Docker Desktop
* Mac or Linux

1. Create (and activate) a new environment, named `welltrajconvert` with Python 3.7. If prompted to proceed with the install `(Proceed [y]/n)` type y.

	- __Open a Terminal and Install Redis__: 
	```
	brew install redis
	```
	- __Open a Terminal and Run Redis Search from Docker:__: 
	```
	> docker run -it --rm --name redis-search-2 \
   -p 6379:6379 \
   redislabs/redisearch:2.0.2
	```

Install redisporductcatalog:

    $ git clone https://github.com/bpamos/redisprodcatalog.git
    $ cd redisprodcatalog/
    $ pip install ./
    
	
## Overview


---

1. Create (and activate) a new environment, named `redisproductcatalog` with Python 3.8+

	- __Mac__: 
	```
	conda create -n redisproductcatalog python=3.8
	source activate redisproductcatalog
	```


