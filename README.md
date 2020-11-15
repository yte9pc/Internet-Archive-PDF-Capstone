# Internet-Archive

## Problem Description
As new effort in our mission towards “Universal Access to All Knowledge”, the Internet Archive
is attempting to collect and provide perpetual access to the “scholarly web”: the public record of
research publications and datasets available on the world wide web, interlinked by both
hyperlinks (URLs) and citations. We have a specific focus on “long-tail” open access works
(which may be published in non-English language, outside North America or Europe, in nonSTEM disciplines, from small or informal publishers, not assigned DOIs, not archived in existing
preservation networks, etc).

Implementation and training of a fast PDF identification tool, which can score files on
their likelihood of being a research publication, and what stage of publication (eg,
abstract, manuscript, camera ready, OCR scan) the file represents. Ideally the tool would
process hundreds of millions of files and be network (as opposed to CPU) bound.

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
- Original PDF or extracted XML for 50+ million research publications. Only a subset of
these have been matched to a catalog entry so far
- Samples of a corpus of hundreds of millions of unsorted, raw PDF files from our
historical web archives
- Privacy restrictions vary depending on the specific dataset. Full text of Open Access
publications (either in original PDF or extracted XML format) carry the licenses of their
original works (often as open Creative Commons licenses).
- Bryan, the project liaison at the Internet Archive, will make sure that the data is available.
It is already free and open.
