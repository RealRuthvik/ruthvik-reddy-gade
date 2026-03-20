# Building an Offline Survival AI System

If the power grid goes down permanently, society collapses. Most statistics say a massive chunk of the population won't make it past the first 30 days. 

We actually have a lot of offline knowledge backed up. You can download the entirety of Wikipedia, WikiMed, and military survival manuals as compressed .zim files via Kiwix. But having the data is not the same as being able to use it. 

If you are injured or need to purify water right now, you don't have time to manually read through 100GB of dense text to figure out what chemical reactions you need. You just need an answer based on what is around you.

I wanted to build a system that solves this. The idea is a localized, offline survival expert program. You tell the system your biome (like a coastal area) and your inventory (driftwood, cooking oil). When you ask how to make soap, it doesn't just give you a generic chemical formula. It reads the local Wikipedia data and tells you to crush seashells for quicklime, burn the driftwood for ash, and mix it with your oil.

Building this is not like making a normal web app. You can't rely on cloud servers or standard APIs because the internet is gone.

The core of this is a Local Retrieval Augmented Generation (RAG) pipeline. I am using a quantized local LLM running through llama.cpp. 

Here is the flow:
1. The user asks a question.
2. The system searches a local vector database (FAISS) containing all the chunks of the offline .zim files.
3. It retrieves the exact paragraphs needed.
4. It feeds those paragraphs to the local LLM along with the user's inventory.
5. The LLM synthesizes a direct answer and cites the exact source.

Citation is critical. If the AI hallucinates a medical procedure, someone could die. It has to show the exact source text so the user can verify it.

The hardest part is the physical hardware. AI takes a lot of compute, and compute takes power. In a grid down scenario, electricity is a luxury. You can't run this on a gaming PC.

The target hardware is a low power single board computer like an Orange Pi 5 or Raspberry Pi. It needs to run off a 12V car battery or a portable solar panel. 

It also acts as a local network hub. The Pi broadcasts its own offline wifi hotspot. It uses a captive portal, just like hotel wifi. Anyone in your survival group with a dead smartphone can connect to the local network, and their browser will automatically open the UI for the survival system. Zero app installation required.

It is a tough project because you are fighting hardware limits, memory constraints, and local Linux networking at the same time. But having a localized, power efficient brain that can turn raw data into actionable survival steps makes the engineering headaches worth it.