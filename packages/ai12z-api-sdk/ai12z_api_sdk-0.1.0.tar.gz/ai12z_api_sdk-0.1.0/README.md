
# Ai12z-api-SDK

The Ai12z Python SDK provides a convenient way to interact with the Ai12z Rest API service in Python applications.



## Prerequisites
- Python installed
## Installation

To use the Ai12z Python SDK in your Python project, you can install it via pip.

```bash

pip install ai12z

```


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`Base_Url` - "https://dev-api.ai12z.net"



## Usage/Example
- HealthCheck(): Checks the health status of the AI service and prints the response.

- AskAi(String question, Ai12zOptions options): Asks the AI a question with optional parameters and prints the response.

- Search(String query, Ai12zOptions options): Searches for information based on a query with optional parameters and prints the response.

Health Check

Perform a health check on the Ai12z service:

Health Check Sample Request:
```python
 healthckeck_ai_response = Ai12zService().health_check() 
    print("Ai12zHealthCheck Response: ") 
    pprint.pprint(healthckeck_ai_response)
```
Sample Health Check Response:
```python
{
  "status" : "ok",
  "date" : "2024-04-16 - 9:11 PM",
  "my_server_id" : "661e7b62fd3fb017fbaab564",
  "server_time" : "2024-04-17 04:49:45.216747"
}

```
Ask AI

Ask a question to the Ai12z AI service:

Ask Ai Sample Request:
```python
option = Ai12zOptions()
        option.api_key = "YOUR_API_KEY"
        option.format = "REQUIRE_FORMAT"
        query  = "YOUR_QUERY_HERE"
        ask_ai_response = Ai12zService().ask_ai(query, option)
        print("Ai12zAskAi Response: ")
        pprint.pprint(ask_ai_response)

```
Sample Ask Ai Response:

```java
{
  "answer" : "<p style=\"margin: 20px 0;\">Alpesh is the co-founder and Chief Technology Officer (CTO) of ai12z. He is a strategic technology executive known for transforming AI-driven ideas into enterprise-level solutions <a href='https://stage.ai12z.com/about' style='font-size: 70%; color: blue; text-decoration: underline;' target='_blank'  title='About – ai12z'>[r1]</a>.</p>",
  "asset_type" : "web",
  "completion_answer" : "Alpesh is the co-founder and Chief Technology Officer (CTO) of ai12z. He is a strategic technology executive known for transforming AI-driven ideas into enterprise-level solutions[^0^].",
  "context" : [ {
    "metadata" : {
      "asset_type" : "web",
      "created_at" : 1711112991312,
      "description" : "About – ai12z About ai12z ai12z's platform allows you to create and manage next-generation search, chatbots and modern AI applications called copilots. Powered...",
      "lang" : "en-US",
      "name" : "About – ai12z",
      "relevance_score" : 0.82432055,
      "title" : "About – ai12z",
      "url" : "https://stage.ai12z.com/about",
      "wordCount" : 372
    },
    "page_content" : "About – ai12z\n\n About ai12z\n\n ai12z's platform allows you to create and manage next-generation search, chatbots and modern AI applications called copilots. Powered by Generative AI, these intelligent copilots will not only address and respond to your questions but also act as personal digital assistants, making contextual recommendations and helping you complete tasks.\n\nLeadership Team\n\nBill Rogers\nCo-founder & CEO\n\nBill is a visionary entrepreneur with a deep technologist background in AI and digital technologies. Recognized for significantly influencing the evolution of online experiences, Bill founded Ektron and served as its CEO. Under his leadership, Ektron emerged as a pioneering SaaS web content management platform, serving thousands of organizations globally. After Bill sold Ektron to Accel KKR, it merged with Episerver and became part of Optimizely. Venturing further into AI, Bill co-founded and led Orbita as its CEO, pushing the boundaries of advanced conversational AI. Beyond these startups, Bill co-founded several ventures and has had an expansive career in digital signal processing and robotics engineering.\n\nBill holds a Bachelor of Science in Electrical Engineering from Boston University.\n\nAlpesh Patel\nCo-founder & CTO\n\nAlpesh is a strategic technology executive renowned for transforming AI-driven ideas into enterprise-level solutions. As the VP of Engineering and later the SVP of Technology at Ektron, he led pivotal technological shifts, introducing the company's first SaaS offering to pioneering its web content management systems. As CTO and co-founder of Orbita, Alpesh led the architectural design and development of its enterprise-level conversational AI platform. In addition to his roles at these firms, Alpesh's contributions have spanned areas such as voice & bot agents, IoT, and cloud computing, solidifying his reputation as a forward-thinking technologist.\n\nHe earned a Microsoft certification in Azure AI Engineering. Alpesh holds a Bachelor of Science in Computer Science from Daniel Webster College.\n\nNicole Rogers\nCo-founder & CMO\n\nNicole is a technology professional with a background spanning cloud, content management and spatial data. Her experience includes establishing and scaling programs from their start to success, steering team operations, driving go-to-market initiatives, and enhancing partner and analyst relations to boost solution visibility and drive revenue. Nicole has contributed her expertise to companies which include Google, Box, WeWork, Matterport, and Ektron (presently known as Optimizely).\n\nNicole holds a Bachelor of Business Administration in International Business and Marketing from The George Washington University."
  }, {
    "metadata" : {
      "asset_type" : "web",
      "created_at" : 1711112991312,
      "description" : "How Generative AI takes search to the next level – ai12z How Generative AI takes search to the next level by Alpesh October 17, 2023 We've been using search...",
      "lang" : "en-US",
      "name" : "How Generative AI takes search to the next level – ai12z",
      "relevance_score" : 0.80224586,
      "title" : "How Generative AI takes search to the next level – ai12z",
      "url" : "https://stage.ai12z.com/2023/10/17/how-generative-ai-takes-search-to-the-next-level",
      "wordCount" : 387
    },
    "page_content" : "How Generative AI takes search to the next level – ai12z\n\nHow Generative AI takes search to the next level\n\nby\nAlpesh\n\nOctober 17, 2023\n\n We've been using search engines like Google for over 20 years. And we've been trained to type keywords into a search box and wait for results. While this method has served us well, Generative AI (GenAI) offers a more advanced approach. \nLet's first look at the traditional search process: \n Crawling: Web crawlers move across the internet, finding new sites and updated pages. \n Indexing: This step involves analyzing the found content and storing it in a database called the search index. It evaluates elements like keywords, tags, and headers to determine the content's relevance. \n Ranking: When users input a query, the search engine checks the index to find the most relevant web pages. It then ranks these pages and shows them to the user. \n In this system, keywords are essential. They are the terms users put into search engines. Having these keywords on your webpage can boost its visibility in search results. Still, users often have to go through multiple pages from their search results to find what they need. \nGenAI offers a different approach: \n Natural Language Understanding: Instead of just relying on keyword matches, GenAI looks at the meaning and context of a query to better grasp what the user wants. \nSynonym Recognition: Users don't need to type the exact keyword. Terms like “Queen,” “Her Majesty,” and “Monarch” are understood as related. And queries in different languages are understood. \nSummarization:Rather than navigating through a list of web pages to find the answer, GenAI provides concise responses in an answer box directly after a query. This streamlined approach greatly reduces search time and enhances user efficiency. \nUse of Natural Language Processing (NLP): GenAI goes beyond keywords and uses NLP to pinpoint what users are really after, providing more relevant results and reducing the time spent browsing through unrelated sites. \n In short, GenAI focuses more on understanding the user's needs rather than just matching keywords. And as search needs change, users can adjust their queries for better results. \nIt's no longer just relying on keywords but using Natural\n\nInsight\n\nPublished by\nAlpesh\n\nRelatest posts\n Insight\nThe Benefits and Urgency of Embracing Generative AI Now\nSeptember 18, 2023\n\n Insight\nThe Power of Multimodal AI�\nOctober 4, 2023\n\n Deliver amazing experiences.\nWe've helped thousands of companies, just like yours, change their businesses.\n\nTalk to us today"
  }, {
    "metadata" : {
      "asset_type" : "web",
      "created_at" : 1711112991312,
      "description" : "The Benefits and Urgency of Embracing Generative AI Now – ai12z The Benefits and Urgency of Embracing Generative AI Now by Bill September 18, 2023 In today's...",
      "lang" : "en-US",
      "name" : "The Benefits and Urgency of Embracing Generative AI Now – ai12z",
      "relevance_score" : 0.04611975,
      "title" : "The Benefits and Urgency of Embracing Generative AI Now – ai12z",
      "url" : "https://stage.ai12z.com/2023/09/18/the-benefits-and-urgency-of-embracing-generative-ai-now",
      "wordCount" : 462
    },
    "page_content" : "The Benefits and Urgency of Embracing Generative AI Now – ai12z\n\nThe Benefits and Urgency of Embracing Generative AI Now\n\nby\nBill\n\nSeptember 18, 2023\n\n In today's fast-paced digital world, Generative AI (GenAI) has been making waves. It is no longer just a theoretical possibility but a reality that is transforming industries and productivity in significant ways. We'll dive into the multiple benefits that GenAI offers and the urgency for businesses to embrace this technology.\nBreaking Down Generative AI\nGenerative AI is a game-changing technology capable of generating text, images, audio, video, code, and synthetic data in response to prompts, which serve as initial inputs or instructions. But its capabilities are not restricted to mere content creation. GenAI is a reasoning engine that mirrors human-like understanding. It can act as a ‘Copilot' for businesses by streamlining workflows and automating tasks across various productivity and collaboration applications. Furthermore, GenAI can autonomously handle complex tasks without human intervention and can be integrated with other AI models and third-party systems to extend its functionalities.\nWhy Embrace Generative AI?\n Transforming Knowledge Work\nGenAI has the potential to revolutionize knowledge work by unlocking valuable insights from existing data and content within an organization. It allows businesses to decode hidden patterns and understand their performance in a comprehensive manner.\n\nConsider the field of law as an example. Traditionally, lawyers spend countless hours conducting legal research, sifting through hundreds or even thousands of documents and legal texts to find pertinent information. With GenAI, this time-consuming task can be largely automated. GenAI can comprehend the meaning and context of legal documents, analyze patterns, and summarize insights, providing lawyers with the most relevant information. More advanced models can even draft basic legal documents or contracts based on prompts given, automating more routine parts of the legal work.\n\nPersonalization and Improved Customer Support\nGenAI helps offer personalized responses, enhancing user experience and satisfaction. It is capable of providing tailored customer support, leading to improved relationships with customers and heightened loyalty.\n\nTake a multinational corporation, for example. Here, GenAI can significantly enhance customer support by handling real-time, multilingual queries 24/7. It understands and interprets the context and tone of the customer's requests, delivering personalized responses based on their past interactions and preferences. If a customer has faced a specific issue in the past, GenAI recalls this and customizes its support, possibly even anticipating related future queries. Such proactive, personalized service greatly improves customer relationships, boosts satisfaction, and promotes loyalty.\n Efficiency and Productivity Boost\nThrough automation, GenAI increases efficiency and productivity across several sectors. Tasks such as report generation, software development, and marketing that previously required significant human hours can be done more efficiently.\n\nEnhanced Data Analysis\nGenAI can analyze large data sets and derive valuable insights. It can process enormous amounts of data more accurately and quicker than a human, making it an excellent tool for data-driven businesses."
  } ],
  "conversation_id" : "661f54fafd3fb017fbaac062",
  "description" : "About – ai12z About ai12z ai12z's platform allows you to create and manage next-generation search, chatbots and modern AI applications called copilots. Powered...",
  "did_answer" : true,
  "error" : null,
  "insight_id" : "661f54fafd3fb017fbaac063",
  "link" : "https://stage.ai12z.com/about",
  "relevance_score" : "82.43",
  "title" : "About – ai12z"
}
```
Search

Search for information using the Ai12z AI service:

Sample Search Request:
```java
option.api_key = "YOUR_API_KEY"
        option.num_docs = REQUIRE_NUMDOC
        query = "YOUR_QUERY_HERE"
        ask_ai_response = Ai12zService().search(query, option)
        print("Ai12zSearch Response: ")
        pprint.pprint(ask_ai_response)
   

```
Sample Search Response:

```java
{
  "docs" : [ {
    "asset_type" : "web",
    "category" : "",
    "description" : "About – ai12z About ai12z ai12z's platform allows you to create and manage next-generation search, chatbots and modern AI applications called copilots. Powered...",
    "link" : "https://stage.ai12z.com/about",
    "score" : 0.6888790130615234,
    "title" : "About – ai12z"
  }, {
    "asset_type" : "web",
    "category" : "",
    "description" : "How Generative AI takes search to the next level – ai12z How Generative AI takes search to the next level by Alpesh October 17, 2023 We've been using search...",
    "link" : "https://stage.ai12z.com/2023/10/17/how-generative-ai-takes-search-to-the-next-level",
    "score" : 0.6490653157234192,
    "title" : "How Generative AI takes search to the next level – ai12z"
  }, {
    "asset_type" : "web",
    "category" : "",
    "description" : "ai12z – ai12z Generative AI Copilots AI-powered solutions for your business GET STARTED CONTACT US Upload your content Answer questions instantly Automate...",
    "link" : "https://stage.ai12z.com",
    "score" : 0.6250337362289429,
    "title" : "ai12z – ai12z"
  }, {
    "asset_type" : "web",
    "category" : "",
    "description" : "Get Started – ai12z Get Started We're excited to offer you early access to the ai12z platform through our beta program. Please complete the form below to...",
    "link" : "https://stage.ai12z.com/get-started",
    "score" : 0.6060378551483154,
    "title" : "Get Started – ai12z"
  }, {
    "asset_type" : "web",
    "category" : "",
    "description" : "Use Cases – ai12z AI-Powered Business Solutions Harness the power of Generative AI for enhanced customer engagement and streamlined operations. Explore our use...",
    "link" : "https://stage.ai12z.com/use-cases",
    "score" : 0.6052713394165039,
    "title" : "Use Cases – ai12z"
  } ],
  "error" : false,
  "times" : {
    "vdb_retrieval" : 0.09375786781311035
  }
}
```



