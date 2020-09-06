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
