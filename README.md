# GiftsAI
AI Agent that give the best recommendations for your gifts.

## Requirements
### General

- [x] Private gh repo
- [ ] Proper logging
- [ ] Proper unit tests (check coverage)
- [ ] Database
- [ ] Use Postman for API
- [ ] Deploy to Azure in a docker container, publicly availably
- [ ] No api key uploaded (use env vars)
- [ ] Jenkins/GH Actions/Azure Pipelines - each push runs unit tests + publishes to Azure automatically

### Functional

- [ ] Call chatGPT:
    - send: 
        - idk shen ukve kairagacebi gaq gaketebuli eg miviyvanot bolomde
    - receive:
        - list of categories for amazon
- [ ] Validate & parse chat's response
- [ ] Send to amazon
- [ ] Validate amazon's response
- [ ] Display to user
