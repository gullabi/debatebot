# Debate bot - AIstiny

This project is an attempt at creating a "debate bot" based on the content generated in the twitch "debatesphere," mostly concentrating on the style of the streamer Destiny.

The architecture is based on GPT2 leveraging the DialoGPT codebase, tutorials and models. The repository is structured into 3 parts: tutorial, data and training.

* tutorial: the ipython notebooks and other relevant information
* training: the streamlined training scripts
* data: all the relevant scripts and raw data related to generating the data

Currently, there is only the notebook based on the [Make your own Rick Sanchez (bot) with Transformers and DialoGPT fine-tuning](https://towardsdatascience.com/make-your-own-rick-sanchez-bot-with-transformers-and-dialogpt-fine-tuning-f85e6d1f4e30?gi=cfc48d3ef8cf), it has been revised and updated for the changes in the huggingface. 

## Phase 0, current to do list:

- [X] Check and maintain the Rick Sanchez tutorial notebook.
- [ ] Tutorial notebook should train only for Rick’s responses
- [ ] Create a streamlined training script based on [huggingface](https://github.com/huggingface/transformers/blob/master/examples/pytorch/language-modeling/run_clm.py).
- [ ] Find a new dataset to train that is similar to streamer debates, i.e. lengthy responses allowed.
- [ ] Develop data preparation scripts

---

## Other information:

The initial [Phase 0 reddit post](https://www.reddit.com/r/Destiny/comments/prthfj/aistiny_the_ultimate_debate_bot_phase_0_viability/). 

Current state: Phase 0

This is a project to train an open AI model for the ultimate debate bot/debate bro AIstiny (the name is cringe and preliminary, I am open to suggestions), based on the past debates of Destiny. The architecture uses open source DialoGPT architecture, pretrained models, and the structured subtitles of the youtube videos of Destiny.

This documents is the initial resource document, which has the technical information and most importantly the data gathering efforts, i.e. the video links, and relevant information.


## Tech infrastructure:


### References DialoGPT:

[Make your own Rick Sanchez (bot) with Transformers and DialoGPT fine-tuning](https://towardsdatascience.com/make-your-own-rick-sanchez-bot-with-transformers-and-dialogpt-fine-tuning-f85e6d1f4e30?gi=cfc48d3ef8cf)

[Easy Chatbot with DialoGPT, Machine Learning and HuggingFace Transformers – MachineCurve](https://www.machinecurve.com/index.php/2021/03/16/easy-chatbot-with-dialogpt-machine-learning-and-huggingface-transformers/)

[Github: microsoft/DialoGPT: Large-scale pretraining for dialogue](https://github.com/microsoft/DialoGPT)

[DialoGPT — transformers 4.10.1 documentation](https://huggingface.co/transformers/model_doc/dialogpt.html)


### Further reading:

[🦄 How to build a State-of-the-Art Conversational AI with Transfer-Learning](https://medium.com/huggingface/how-to-build-a-state-of-the-art-conversational-ai-with-transfer-learning-2d818ac26313)

[Practical Applications of Open AI’s GPT-2 Deep Learning Model](https://medium.com/the-research-nest/practical-applications-of-open-ais-gpt-2-deep-learning-model-14701f18a432)

[Latitude-Archives/AIDungeon: Infinite adventures await!](https://github.com/Latitude-Archives/AIDungeon)

[philip-bl/gpt2_chatbot: Chatbot using GPT-2](https://github.com/philip-bl/gpt2_chatbot)


## Data references:

The most intensive part of the process is to create the clean and structured data for Destiny's debates in dialogue format. As a first step we are creating a list of interesting debates. These debates must have good recording quality, preferably 1v1 and relatively less talking over each other (all for better transcription), and be on interesting topics


### List of target debates:

The community contributed list can be found [here](https://docs.google.com/spreadsheets/d/1MNMo7623PTooMu_aVBsio0G7iEfhTwQBlEk_NB270mQ/edit#gid=1266396936). If anyone wants to suggest more videos please fill up [the form](https://docs.google.com/forms/d/12j_fTeYhrCtjJ3NdY7Eud80mEsj2E3uZ9269gltn3LE/).
