# specs
*   user can enter an address in an "enter address" view and get back that
    address's lat/long

*   user can center their lat/long and get back an address

*   request to "/" returns a simple static landing page

*   a request to '/geocode' returns users lat/long<a
    href="#details_1">details</a>

# TODO
## /geocode

[x] - create the GeoCode Route
[x] - write a method to parse address string from the request header
    * must escape malicious strings
[x] - returns (AT LEAST) the lat/long in json

## /address
[ ] - parse the lat/long floats
[ ] - return the full address 

## /distance
[ ] - request each address in parallel

### accpetance criteria 
1. if user does not provide a param, an error message is displayed and user is
   asked to return to the main geocode page
2. user input must be santized if user enters any incorrect data

### Nice to have
[ ] - write JS code to do a loading animation during GOOG api wait
[ ] - client side validation
[ ] - xsrf cookie
