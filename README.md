# toposoid-sentence-parser-english-web
This is a WEB API that works as a microservice within the Toposoid project.
Toposoid is a knowledge base construction platform.(see [Toposoid Root Project](https://github.com/toposoid/toposoid.git))
This Microservice analyzes dependency's structure of English sentences and outputs the result in JSON.

[![Test And Build](https://github.com/toposoid/toposoid-sentence-parser-english-web/actions/workflows/action.yml/badge.svg)](https://github.com/toposoid/toposoid-sentence-parser-english-web/actions/workflows/action.yml)

<img width="1151"  src="https://github.com/toposoid/toposoid-sentence-parser-english-web/assets/82787843/622291ce-a45c-4161-aec9-53460833aea0">


## Requirements
* Docker version 20.10.x, or later
* docker-compose version 1.22.x

### Memory requirements For Standalone
* Required: at least 3GB of RAM
* Required: at least 1.24GB of HDD(Docker Image Size)

## Setup For Standalone
```bssh
docker-compose up -d
```
The first startup takes a long time until docker pull finishes.

## Usage
```bash
curl -X POST -H "Content-Type: application/json" -d '{
    "premise": [],
    "claim": [
        {
            "propositionId": "612bf3d6-bdb5-47b9-a3a6-185015c8c414",
            "sentenceId": "4a2994a1-ec7a-438b-a290-0cfb563a5170",
            "knowledge": {
                "sentence": "This is a test.",
                "lang": "en_US",
                "extentInfoJson": "{}",
                "isNegativeSentence": false,
                "knowledgeForImages": []
            }
        }
    ]
}' http://localhost:9007/analyze
```
Currently, isNegativeSentence is always set to false when registering data.

## Note
* This microservice uses 9007 as the default port.
* The meaning of premise is a premise as a proposition, and it corresponds to A of A → B in a logical formula. Therefore, it is set when there is a condition for the claim. Unless there are special conditions, it is not necessary to set the premise.

## License
This program is offered under a commercial and under the AGPL license.
For commercial licensing, contact us at https://toposoid.com/contact.  For AGPL licensing, see below.

AGPL licensing:
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

## Author
* Makoto Kubodera([Linked Ideal LLC.](https://linked-ideal.com/))

Thank you!
