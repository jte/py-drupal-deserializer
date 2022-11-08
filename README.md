# py-drupal-deserializer

## What's this?
It's simple module for deserialization of data serialized by Drupal
It looks like this: "a:2:{i:0;s:3:"ABC";i:1;s:4:"DEFG"}"
It was made by reverse-engineering data format because there's no official docs about it. 
I did found the slides talking about it when I already finished the project (see Reference)

## Uses
I used it for deserialization of project attributes in Drupal's UberCart e-commerce solution when porting the orders to Shopify.

## Reference
[Data Serialization with Symfony & Drupal](https://events.drupal.org/sites/default/files/slides/serializer.pdf)
