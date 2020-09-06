# Internet-Archive

## Problem Description
As new effort in our mission towards “Universal Access to All Knowledge”, the Internet Archive
is attempting to collect and provide perpetual access to the “scholarly web”: the public record of
research publications and datasets available on the world wide web, interlinked by both
hyperlinks (URLs) and citations. We have a specific focus on “long-tail” open access works
(which may be published in non-English language, outside North America or Europe, in nonSTEM disciplines, from small or informal publishers, not assigned DOIs, not archived in existing
preservation networks, etc).

We have several open engineering and research challenges:
- Validating, re-training, or improving the PDF-to-XML tool we use (GROBID) to work
with long-tail papers. GROBID uses machine learning techniques to extract structured
content from free-form PDFs, including bibliographic metadata and reference lists
- Implementation and training of a fast PDF identification tool, which can score files on
their likelihood of being a research publication, and what stage of publication (eg,
abstract, manuscript, camera ready, OCR scan) the file represents. Ideally the tool would
process hundreds of millions of files and be network (as opposed to CPU) bound.
- Perform a comparative analysis of locality-sensitive hashing techniques to fingerprint and
match research publications, agnostic of file format. For example, match PDF, XML, and
HTML copies of the same document. Outcome would be identification of specific
algorithms and tuning parameters for this task.
- Citation graph analysis at scale (billions of edges) to identify “missing works” in our
bibliographic catalog

## Objective
Our primary objective is to gain practical insight into which methods and tools are actually
effective with our raw content and metadata to increase the coverage and quality of our catalog.
Based on the outcome of this capstone project we will deploy new data processing pipelines
(batch or streaming) as part of our production services.
A stretch goal would be software with sufficient quality and utility to be deployed directly to our
production infrastructure with little modification.


## Description of the Data
The Internet Archive can provide the following datasets in either complete or statistical sample
form:
• Our complete bibliographic catalog of roughly 100 million works, including 600+ million
citation links, in JSON form
3
• Original PDF or extracted XML for 50+ million research publications. Only a subset of
these have been matched to a catalog entry so far
• Samples of a corpus of hundreds of millions of unsorted, raw PDF files from our
historical web archives
• Privacy restrictions vary depending on the specific dataset. Full text of Open Access
publications (either in original PDF or extracted XML format) carry the licenses of their
original works (often as open Creative Commons licenses).
• Bryan, the project liaison at the Internet Archive, will make sure that the data is available.
It is already free and open.
• Some full texts of publications have copyright restrictions (even if collected from public
web archives) and required a data transfer agreement (see below for template).
• Bibliographic metadata and other derived metadata datasets are generally publicly
available from archive.org with the indicated license.
