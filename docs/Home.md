# Table of Contents

* [Description](#Description)
* [Requirements](#Requirements)
* [Usage](#Usage)
  * [doc_mj.py](#doc_mjpy)
  * [JSON Schema](#JSON-Schema)
  * [YAML Schema](#YAML-Schema)

## Description

**Doc**ument generation tool to create **Mark**down documents from **JSON**.

The essential goal here is to create a fast way to create consistent looking Mark Down documentation for purpose of posting it to the Wiki on Git Hub.

Generally speaking this release is probably way to early for others to use, however if it works for you awesome!

## Requirements

**Python version**: 3.9 or higher

**Python Modules**:

* **Beartype**: Used to ensure the arguments being passwed between methods and classes are the correct types
* **Jinja2**: For templating

## Usage

If you are looking to integrate into your own code I would look at doc_mj.py under the bin directory.

### doc_mj.py

Example script that reads a directory and then generates the Markdown files and checks them in to the Github Wiki for a project.

```bash
    bin/doc_mj.py <json> <out_dir> <owner> <repository> <message>
    # The following example would generate the Wiki for this project
    bin/doc_mj.py json wiki_docs biggiebk doc_mark_json "Testing template customization setting"
```

### JSON Schema

The following is the basic json schema that is required

```json
    {
      "document": {
        "sections": [
          "title": "I am a title section",
          "pre": [
            "I am the first line",
            "I am the second line"
          ],
          "sections": [
            "title": "I am a sub section",
            "pre": [
              "I am some text of the sub sections"
            ]
          ],
          "post": [
            "I am the post text section"
          ]
        ]
      }
    }
```

### YAML Schema

The following is the basic YAML schema

```yaml
    document:
      sections:
      - title: I am a title section
        pre:
        - I am the first line
        - I am the second line
        sections:
        - title: I am a sub section
          pre: I am some text of the sub sections
        post:
        - I am the post text of section
```

