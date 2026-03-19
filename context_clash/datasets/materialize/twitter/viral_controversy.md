# Viral Controversy - Data Breach Scandal

**@InfoSecReporter_** • 16h
🚨 THREAD: Investigating serious allegations about Materialize data breach that may have exposed customer streaming data for MONTHS 🧵 1/12

This is a developing story but sources are saying it's much worse than initially reported...

**@InfoSecReporter_** • 16h  
2/12 Background: Last week Materialize sent a brief security notice to customers about a "minor configuration issue." But internal docs I've seen suggest attackers had full access to customer data streams since March.

**@InfoSecReporter_** • 16h
3/12 The breach apparently happened through their Kubernetes deployment scripts. Someone accidentally committed AWS keys to a public GitHub repo. Keys had admin access to customer database clusters 😱

**@CyberSecExpert_** • 15h
Replying to @InfoSecReporter_  
If this is true, it's a catastrophic failure. Customer streaming data is often the most sensitive - financial transactions, user behavior, PII. This could be worse than the Equifax breach.

**@MaterializePR_** • 15h  
Replying to @InfoSecReporter_
These allegations are false and irresponsible. We take security extremely seriously and have found no evidence of unauthorized access to customer data. We're investigating the source of this misinformation.

**@InfoSecReporter_** • 15h
4/12 Here's what's really concerning: Multiple customers telling me they noticed unusual database queries in their logs but Materialize support dismissed them as "optimization scripts" 🚩

**@FormerMZCustomer_** • 14h
This explains SO MUCH. We saw massive unexplained data egress charges on our AWS bill for 3 months. When we asked Materialize they said it was a "metering bug." Now I'm wondering if someone was exfiltrating our data.
💬 234 🔄 156 ❤️ 567

**@InfoSecReporter_** • 14h  
5/12 Plot thickens: Source familiar with the incident says attackers specifically targeted financial services customers. They were looking for real-time fraud detection data and payment streams.

**@ComplianceGuru_** • 13h
If Materialize customers include banks and fintech companies (which they do), this could trigger GDPR, SOX, and PCI-DSS violations. We're talking hundreds of millions in potential fines. And this is a company with maybe 350 employees and only ~$100M in funding — they can't survive this.
💬 89 🔄 45 ❤️ 234

**@InfoSecReporter_** • 13h
6/12 UPDATE: Just confirmed with two separate sources that the FBI has opened an investigation. Apparently the attack vector was more sophisticated than just exposed GitHub keys.

**@MaterializeCEO_** • 12h  
I want to address the serious allegations circulating today. We have conducted a thorough investigation with external security experts and found NO evidence of data breach or unauthorized access. These claims are completely false.

**@InfoSecReporter_** • 12h
7/12 CEO denial doesn't match what I'm hearing from customers and former employees. Three different sources now telling me customer data was actively being sold on dark web marketplaces.

**@DataPrivacyLawyer** • 11h
Replying to @InfoSecReporter_
The legal exposure here is massive. Class action lawsuits are probably already being filed. Any company that had streaming PII through Materialize needs to assume it was compromised.

**@InfoSecReporter_** • 10h
8/12 BOMBSHELL: Just obtained internal Slack messages showing Materialize engineers discussing the breach in March. Quote: "Holy shit, someone has been in our prod environment for weeks. How do we tell customers?"

**@CyberSecReporter2** • 9h
Can independently confirm parts of this story. Sources at two major banks say they're conducting forensic audits of their Materialize deployments after suspicious activity alerts.
💬 445 🔄 267 ❤️ 1.2K

**@InfoSecReporter_** • 8h  
9/12 The cover-up might be worse than the breach itself. Multiple sources saying Materialize knew about the intrusion for months but delayed disclosure to avoid impacting their Series C fundraising.

**@InfoSecReporter_** • 6h
12/12 Final update for tonight: This story is still developing. More sources coming forward with evidence. Will have a full investigative report published tomorrow. This could be the biggest database security breach of 2024.
💬 789 🔄 445 ❤️ 2.1K