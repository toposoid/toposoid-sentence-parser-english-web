# toposoid-sentence-parser-english-web
This is a WEB API that works as a microservice within the Toposoid project.
Toposoid is a knowledge base construction platform.(see [Toposoid Root Project](https://github.com/toposoid/toposoid.git))
This Microservice analyzes dependency's structure of English sentences and outputs the result in JSON.

[![Test And Build](https://github.com/toposoid/toposoid-sentence-parser-english-web/actions/workflows/action.yml/badge.svg)](https://github.com/toposoid/toposoid-sentence-parser-english-web/actions/workflows/action.yml)

<img width="1099" src="https://user-images.githubusercontent.com/82787843/163391974-253c45bf-456d-4ef7-afe1-b996c24ea52a.png">


## Requirements
* Docker version 20.10.x, or later
* docker-compose version 1.22.x

### Memory requirements
* Required: at least 6GB of RAM
* Required: 10G or higher of HDD

## Setup
```bssh
docker-compose up -d
```
It takes more than 20 minutes to pull the Docker image for the first time.

## Usage
```bash
curl -X POST -H "Content-Type: application/json" -d '{
    "sentence":"The answer is blown'\''in the wind.", 
    "lang":"en_US", 
    "extentInfoJson":"{}",
    "isNegativeSentence":false, 
}
' http://localhost:9007/analyzeOneSentence
```
Currently, isNegativeSentence is always set to false when registering data.

# Note
* This microservice uses 9007 as the default port.
* The meaning of premise is a premise as a proposition, and it corresponds to A of A → B in a logical formula. Therefore, it is set when there is a condition for the claim. Unless there are special conditions, it is not necessary to set the premise.

## License
toposoid/toposoid-sentence-parser-english-web is Open Source software released under the [Apache 2.0 license](https://www.apache.org/licenses/LICENSE-2.0.html).

## Author
* Makoto Kubodera([Linked Ideal LLC.](https://linked-ideal.com/))

Thank you!
