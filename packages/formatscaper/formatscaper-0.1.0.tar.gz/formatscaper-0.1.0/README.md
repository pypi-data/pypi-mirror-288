# Formatscaper

Formatscaper is a tool for generating an overview of the file format landscape composed of the uploads in our research data repository.

The aim here is to assist us with the task of digital preservation; specifically with the task of identifying uploaded files which are in danger of becoming "extinct".


## Dependencies

* Python 3
* [Siegfried](https://github.com/richardlehane/siegfried#install)


## General info

Formatscaper is designed to build up the required context over its lifetime of use, so no particular setup is required.
To get started, simply feed it a list of files to analyze in the [expected format](#input) and let it run.

With every run, the database will be extended with information about file formats that haven't been encountered before.
This effectively builds up a knowledge base of the file formats that are actually present in the system (i.e. the file format landscape).

*Note* that whenever a new format is encountered, formatscaper will not give out a rating about the *risk of obsolescence* for this format.
This task is instead left to the operator, e.g. via the `resultman` command.

However, the **risk** of datasets becoming unusable in the future isn't purely based on the formats in question.
Some of the files in a dataset may be stored in a very outdated or problematic format, but the overall dataset can still be reused just fine without them.
An example would be temporary files that have been added to the dataset on accident.
Thus, each scanned file also has an *impact* assessment attached to them, which again needs to be provided by the operator.
This *impact* assessment can then be used together with the *risk of obsolescence* for its format to calculate the overall *risk assessment*.

*Note*: Since file format detection is effectively still based on heuristics, no identification procedure is infallible - sometimes, even the best guess is wrong.
For such cases, we added a mechanism to override the result detected by siegfried on a per-file basis in the database.


### Example usage

Example `formatscaper` call, with a custom path for the `sf` binary:
```sh
$ formatscaper --sf-binary "${GOPATH}/bin/sf" -i record-files.yaml
```

After formatscaper has collected the results in the database, they can be viewed e.g. via `resultman`:
```sh
$ resultman
```



## Rationale

### Building file format landscapes

Tools for creating an overview of file format landscapes already exist, like [`c3po`](https://peshkira.github.io/c3po/) and [`fitsinn`](https://github.com/datascience/fitsinn).
However, they tend to come with more bells and whistles than we actually require, or are not quite ready for production use yet.


### Using a single source of truth

Often, the file format identification is based on the output of several utilities.
For instance, [FITS](https://projects.iq.harvard.edu/fits/home) wraps a number of individual tools and combines their output into a unified XML structure.
Unfortunately, their results are often in disagreement with each other, which necessitates a de-conflicting strategy.

Instead of following this multi-tool approach, we've decided to rely on a single source of truth only - namely a tool called [Siegfried](https://github.com/richardlehane/siegfried).
It seems to be competitive in its file format identification capabilities (under some definition of "competitive").
Also, it is being used as the source of truth by other software solutions in the space of digital preservation such as [Archivematica](https://github.com/artefactual/archivematica) and [RODA](https://github.com/keeps/roda).
That's certainly good enough for us.


### Detecting endangered formats

It seems to be generally agreed upon that a centrally managed "list of endangered file formats" would be a desirable thing to have.
There have been attempts in creating centralized registries for file formats; for example [PRONOM](https://www.nationalarchives.gov.uk/PRONOM/), GDFR and UDFR, and the ["Just Solve the File Format Problem" wiki](http://fileformats.archiveteam.org/).
Out of these, PRONOM is the most promising candidate.
It even offers a field for the "risk" per format - however, this field does not seem to be populated for any of the registered formats.
Unfortunately, this distinctive lack of availability leaves us little choice but to do it ourselves.

There is no way for us to know all the formats that exist in the world - but luckily, this is also not required!
We only have to know about the formats that are part of our format landscape, which is a much more manageable task.
Thus, we use a "local" list of file formats which is extended every time a new format is encountered.
We manually review this list periodically and annotate formats with a hint about their endangerment status.


### Storing the information outside of Invenio

Invenio provides fields for storing information about the format for each file.
However, we often receive archives such as ZIP files which of course contain a series of other files.
Storing information about the formats of these nested files is not a standard use case and thus there is no obvious or generally agreed-upon way to do it (yet).

Because we try to not extend the semantics of available constructs with non-standard custom meaning, we instead decided to keep this information external.


## Example files

### Input

The input for formatscaper needs to be a list of objects (in YAML format) describing the context of each file to investigate.
This includes the URI of the file, its original file name (which gets discarded by Invenio), and the record which the file is a part of.
```yaml
- filename: hosts
  uri: /etc/hosts
  record: 1234-abcd

- filename: FS Table
  uri: /etc/fstab
  record: abcd-1234

- filename: researchdata.zip
  uri: /mnt/data/de/ad/be/ef/data
  record: abcd-1234
```


### Formats file

Information about the encountered file formats can be exported in YAML format (e.g. as `formats.yml`).
This primarily comprises a unique identifier (PUID) and the *risk of obsolescence* (i.e. the *probability of the format dying out*).
Some context (like a human-readable name and MIME type) per format is also provided here, primarily to make it more understandable for operators.
```yaml
- risk: 1
  mime: text/plain
  name: Plain Text File
  puid: x-fmt/111
- risk: 1
  mime: application/zip
  name: ZIP Format
  puid: x-fmt/263
- risk: 2
  mime: null
  name: Adobe Illustrator CC 2020 Artwork
  puid: fmt/1864
- risk: 3
  mime: application/postscript
  name: Encapsulated PostScript File Format
  puid: fmt/124
- risk: 2
  mime: application/pdf
  name: Acrobat PDF 1.4 - Portable Document Format
  puid: fmt/18
- risk: 1
  mime: image/svg+xml
  name: Scalable Vector Graphics
  puid: fmt/92
- risk: 5
  mime: null
  name: null
  puid: UNKNOWN
```

The PRONOM Persistent Unique Identifier (PUID) can be used to uniquely identify formats.
It can also be used to construct a URL (of the shape `https://www.nationalarchives.gov.uk/PRONOM/${puid}`) pointing to additional information about the format.


### Results

The file format identification results for each file (along with their risk assessment) can also be exported into a YAML file (e.g. `results.yml`).
The resulting file contains information about each investigated file and their identified formats, along with a notes about their risk assessment.
```yaml
- filename: /etc/hosts
  format:
    risk: 1
    mime: text/plain
    name: Plain Text File
    puid: x-fmt/111
  record: 1234-abcd
  impact: 2
- filename: /etc/environment
  format:
    risk: 1
    mime: text/plain
    name: Plain Text File
    puid: x-fmt/111
  record: 1234-abcd
  impact: 3
- filename: /mnt/data/de/ad/be/ef/data
  format:
    risk: 1
    mime: application/zip
    name: ZIP Format
    puid: x-fmt/263
  record: abcd-1234
  impact: 4
- filename: /mnt/data/de/ad/be/ef/data#README.txt
  format:
    risk: 1
    mime: text/plain
    name: Plain Text File
    puid: x-fmt/111
  record: abcd-1234
  impact: 3
- filename: /mnt/data/de/ad/be/ef/data#results.csv
  format:
    risk: 1
    mime: text/csv
    name: Comma Separated Values
    puid: x-fmt/18
  record: abcd-1234
  impact: 5
```

Note that the contents of the ZIP archive are inspected as well, with `#` as the delimiter between the archive's filename and the contained file's name.


## Generating an input file from Invenio

The required information is relatively straight-forward to generate using `invenio shell`:
```python
import yaml
from invenio_rdm_records.proxies import current_rdm_records_service as svc

# get all (published) records in the system
rc = svc.record_cls
recs = [rc(rm.data, model=rm) for rm in rc.model_cls.query.all()]

# get the expected structure from the records
record_files = [
    {"record": r["id"], "filename": fn, "uri": entry.file.file.uri}
    for r in recs
    for fn, entry in r.files.entries.items()
    if r.files.entries
]

# serialize the information as YAML file
with open("record-files.yaml", "w") as f:
    yaml.dump(record_files, f)
```

The above script simply lists all files associated with any published record, but does not consider any unpublished drafts.
Such changes are very straight-forward to implement though.
