# Image cut-outs with SODA for CANFAR platform

Clone this repository:

```
git clone https://github.com/manuparra/image-cutouts-soda-canfar.git
cd image-cutouts-soda-canfar
```

Build the image

``
docker build . 
``

Tag the image with:

```
docker build --tag image-cutouts-soda:headless .  
```

Then push the image to you CANFAR repository of images (harbor, for example).

*Use the labels to identify the type of the session for the user*

