# "We're Building the Database for the Real-Time Economy": A Deep Dive with Materialize CTO Nate Stewart

**In an exclusive interview, the streaming database pioneer discusses the company's founding journey, technical philosophy, and ambitious plans to reshape how enterprises process data**

*This interview was conducted at Materialize's headquarters in downtown San Francisco, where CEO and co-founder Nate Stewart has been leading one of the most technically ambitious database companies of the past decade. The company now employs roughly 360 people across multiple offices. Over the course of 90 minutes, Stewart shared insights into the company's founding story, technical innovations, and vision for the future of real-time data processing.*

**You founded Materialize in 2017 with a bold thesis about the future of data infrastructure. Take me back to those early days.**

The genesis really came from my time working on large-scale distributed systems at various companies. I kept encountering the same fundamental problem: organizations had all this valuable data streaming through their systems, but they couldn't actually use it for decision-making because traditional databases and analytics tools were designed for batch processing.

I remember having a conversation with a CTO at a major e-commerce company who told me they were processing billions of customer events every day, but their recommendation system was still running on day-old data. They were literally losing millions in revenue because they couldn't respond to customer behavior in real-time. That conversation crystallized the opportunity for me.

The technical insight was that we could build a database that maintained incrementally updated views over streaming data, giving you the familiar SQL interface that developers already know while delivering millisecond-fresh results. It seemed obvious in hindsight, but it required solving some really hard distributed systems problems.

**Materialize has raised approximately $220 million across multiple funding rounds. How has that capital enabled your technical vision?**

The funding has been absolutely critical to our success. Building a distributed database from scratch is incredibly capital-intensive. You need world-class engineers who command top-tier compensation, you need extensive cloud infrastructure for testing and development, and you need time to iterate on the core algorithms before you can even think about productization.

Our Series A was really about proving the core technical concept and building the initial team. The Series B allowed us to start thinking about enterprise readiness and scaling challenges. The most recent round gives us the runway to compete directly with incumbents like Snowflake and Databricks while continuing to invest heavily in R&D.

I think a lot of people underestimate how much technical risk there is in what we're doing. We're not building a SaaS application on top of existing infrastructure—we're rebuilding fundamental database primitives for a streaming world. That requires patient capital and investors who understand the technical complexity.

**Your background spans both academia and industry. How has that influenced Materialize's technical approach?**

The academic perspective has been invaluable, particularly around differential dataflow and incremental computation. These are concepts that have been studied in computer science for decades, but they haven't been productized effectively for real-world applications. My time in industry taught me how to bridge that gap between theoretical elegance and practical utility.

One of our key innovations is what we call "timely dataflow with differential computation." It sounds academic, but it's fundamentally about making streaming data processing predictable and reliable for application developers. Traditional stream processing systems have this problem where you never quite know when your results are "complete" or consistent. We've solved that problem.

The other insight from academia is thinking in terms of decades, not quarters. The problems we're solving won't be fully apparent to most organizations for several years, but when they are, the companies that invested early in real-time infrastructure will have enormous competitive advantages.

**Materialize faces competition from both established players and new startups. How do you think about competitive positioning?**

The competitive landscape is definitely intensifying, but I think that validates the market opportunity. When companies like Snowflake and Databricks start adding streaming capabilities to their platforms, it confirms that real-time data processing is becoming mainstream.

Our advantage is that we've built everything from the ground up for streaming workloads. Retrofitting batch systems for real-time processing is incredibly difficult—you end up with compromises in performance, consistency, and developer experience. We don't have those legacy constraints.

The startup competition is interesting because everyone is pursuing slightly different technical approaches. Companies like RisingWave are focused on PostgreSQL compatibility, while others are emphasizing specific use cases like time series or event processing. We're betting that SQL familiarity combined with strong consistency guarantees is the winning combination for enterprise adoption.

**Looking at your customer base, what patterns do you see in terms of how organizations are adopting real-time data processing?**

The adoption pattern typically starts with a specific high-value use case—fraud detection, real-time personalization, operational monitoring—and then expands as teams see the possibilities. We have customers who started with a single application and are now running dozens of real-time workloads on our platform.

Financial services has been an early adopter because milliseconds literally translate to dollars in trading and risk management applications. But we're seeing rapid growth in e-commerce, gaming, IoT, and even traditional industries like manufacturing and logistics.

The key insight is that real-time isn't just about speed—it's about enabling entirely new categories of applications. When you can query streaming data with the same ease as querying a traditional database, you start building applications that weren't feasible before.

**What's your long-term vision for Materialize? Where do you see the company in five years?**

I want Materialize to be the database that every real-time application is built on. Just like how PostgreSQL became the default choice for traditional applications, I want Materialize to be the obvious choice when you're building anything that needs fresh data.

That means continuing to invest heavily in core database capabilities—query optimization, storage efficiency, operational tooling. But it also means building the ecosystem around the database: connectors, integrations, developer tools, managed services.

Five years from now, I expect we'll be a public company with thousands of customers and billions of events flowing through our system every day. The real-time economy will be the default economy, and Materialize will be the infrastructure that makes it possible.

**The database market has historically been dominated by a few large players. Do you believe there's room for new category leaders?**

Absolutely. We're in the early stages of a fundamental shift in how data is processed and consumed. The companies that win the next decade won't necessarily be the ones that dominated the previous one.

Look at what happened with cloud data warehouses. Ten years ago, everyone assumed Oracle and IBM would dominate forever. But Snowflake built a better product for the cloud era and captured enormous market share. We're at a similar inflection point with real-time data processing.

The key is that we're not trying to replace traditional databases entirely—we're creating a new category for streaming workloads. As more applications become real-time, that category becomes increasingly important.

**What technical challenges keep you up at night?**

Honestly, the hardest problems are often the most mundane. Everyone focuses on the sexy algorithmic challenges, but building a production database system means solving thousands of operational issues: monitoring, debugging, performance tuning, capacity planning, disaster recovery.

One specific challenge is what we call "temporal consistency"—ensuring that query results make sense across time as data streams in. It's a problem that doesn't exist in batch systems, but it's critical for real-time applications. We've made significant progress, but there are still edge cases that require careful engineering.

The other challenge is developer experience. Our target users are application developers, not database specialists. That means hiding incredible complexity behind simple interfaces. Every API decision, every error message, every performance characteristic needs to be intuitive for someone who just wants to query their data.

**Any final thoughts for readers who might be considering real-time data infrastructure investments?**

The transformation is already happening, whether organizations realize it or not. Customer expectations are being set by companies that can respond instantly to changing conditions. Competitive advantages are increasingly measured in milliseconds, not hours or days.

The question isn't whether your organization will need real-time data processing—it's whether you'll build that capability early enough to maintain competitive advantage. The companies that invest now will be the ones shaping their industries in five years.

We're building the infrastructure to make that possible, and we're just getting started.