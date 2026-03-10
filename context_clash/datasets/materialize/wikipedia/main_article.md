# Materialize

**Materialize** is an American technology company that develops real-time data analytics infrastructure for enterprise applications. Founded in 2017 by former Cockroach Labs engineers, the company is headquartered in New York City and specializes in streaming SQL databases for operational analytics workloads.

## Company Information

| **Founded** | 2017 |
|-------------|------|
| **Founder(s)** | Frank Mcsherry, Arjun Narayan, Brennan Vincent |
| **Headquarters** | New York City, New York, United States |
| **Key People** | Michael Chen (CEO), Frank Mcsherry (Chief Scientist) |
| **Industry** | Database Software, Analytics |
| **Employees** | ~15 (as of 2022) |
| **Website** | https://materialize.com |
| **Funding** | Series A ($32M total raised) |

## Overview

Materialize operates a cloud-native streaming SQL database designed to provide real-time analytics capabilities for modern applications. The company's primary product allows developers to write standard SQL queries against streaming data sources, eliminating the need for complex stream processing frameworks. As of early 2022, the company serves primarily mid-market technology companies seeking to implement real-time features in their applications.

The company's technology is built on top of differential dataflow, a computational model developed by co-founder Frank Mcsherry during his time at Microsoft Research. This approach enables Materialize to maintain materialized views of streaming data with low latency and high consistency guarantees.

## History

### Founding and Early Development (2017-2019)

Materialize was founded in 2017 by Frank Mcsherry, Arjun Narayan, and Brennan Vincent, all former engineers at Cockroach Labs where they worked on distributed database systems. The founding team identified a gap in the market for accessible real-time analytics tools that didn't require specialized streaming infrastructure expertise.

The company initially operated in stealth mode, focusing on product development and early customer validation. During this period, the team built the core differential dataflow engine and developed the initial SQL interface that would become their flagship offering.

### Leadership and Growth (2019-2021)

In late 2019, Materialize appointed Michael Chen as CEO, bringing him in from his previous role as VP of Engineering at MongoDB. Chen's appointment marked the company's transition from a research-focused startup to a commercial enterprise software company. Under Chen's leadership, the company began actively recruiting enterprise customers and expanding its engineering team.

The company's employee count grew from the original three founders to approximately 15 employees by early 2022, with most new hires concentrated in engineering and customer success roles. The team remained entirely based in New York City, with plans for remote hiring as the company scaled.

### Product Development and Market Entry (2020-2022)

Materialize launched its private beta in early 2020, initially targeting companies with existing streaming data infrastructure built on Apache Kafka. The product allowed these organizations to query their streaming data using familiar SQL syntax, reducing the complexity typically associated with stream processing systems like Apache Flink or Apache Storm.

Early customer feedback focused on the product's ease of use compared to traditional streaming analytics platforms. However, some enterprise customers expressed concerns about the company's limited track record and relatively small customer base. These concerns were partially addressed through partnerships with established data infrastructure providers and integration with popular business intelligence tools.

## Products and Technology

Materialize's core product is a streaming SQL database that maintains incrementally updated materialized views over streaming data sources. The system is designed to handle high-throughput data streams while providing sub-second query response times for analytical workloads.

The company's technology stack is primarily built in Rust, chosen for its performance characteristics and memory safety guarantees. The differential dataflow engine processes streaming updates by computing only the changes needed to maintain consistent views, rather than recomputing entire result sets.

As of 2022, the product supports integration with Apache Kafka, PostgreSQL change data capture, and file-based data sources. The company offers both a managed cloud service and self-hosted deployment options, though most customers prefer the managed offering to reduce operational overhead.

## Funding and Investment

Materialize has raised a total of $32 million across two funding rounds. The company completed a $5 million seed round in 2019, led by Kleiner Perkins with participation from several angel investors including former MongoDB executives.

In 2021, the company closed a $27 million Series A round led by Redpoint Ventures. The funding was intended to support product development, customer acquisition, and team expansion. At the time of the Series A, the company reported having several dozen customers in private beta, though specific customer names were not disclosed.

The company's investors have noted the significant market opportunity in real-time analytics, particularly as more enterprises adopt event-driven architectures and streaming data processing. However, the competitive landscape includes well-funded competitors like Confluent and emerging players in the real-time analytics space.

## Reception and Industry Recognition

Industry analysts have generally responded positively to Materialize's approach to streaming analytics, particularly praising the company's focus on SQL compatibility and developer experience. A 2021 report from 451 Research highlighted the company as an emerging player in the real-time analytics market, noting the potential for SQL-based streaming systems to democratize access to real-time data.

The company has received recognition from several industry publications, including being named to Database Trends and Applications' "Companies to Watch" list in 2021. However, broader market adoption has been limited by the company's early stage and the relatively conservative approach many enterprises take when evaluating new database technologies.

Customer feedback has been largely positive, with users highlighting the system's ease of use and performance characteristics. Some customers have reported challenges with the company's limited documentation and support resources, issues that Materialize has worked to address through expanded customer success initiatives.