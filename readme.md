# ogm_utils

Some basic python tools for working with OpenGeoMetadata repositories. Currently only FGDC CSDGM XML metadata is
supported.

## shell scripts
`repofind` and `repowrite` are shell scripts that act as a front end to the utilities.

 `repofind` finds metadata in the repository given the layer id and returns the path as well as a listing of
 metadata types available. Currently, it simply examines `layers.json` to find the path, verifies that it exists and lists
 the contents. 
 
switches: 
* '-r' or '--repository': repository path. Defaults to directory 'REPO_PATH' specified in repo_utils.py.
* '-i' or '--layer_id': unique id for the data layer described by the metadata. REQUIRED


 `repowrite` writes metadata to the repository using a hash of the layer id to create the directory structure.
 Once written, `layers.json` is updated. Using a hash ensures that the path in the repository is computable given the
 layer id. Currently, it uses the FNV-1a hash.  The OpenGeoMetadata repository is specified by
 the constant `REPO_PATH`.

switches:
* '-r' or '--repository': repository path. Defaults to directory 'REPO_PATH' specified in repo_utils.py.
* '-i' or '--layer_id': unique id for the data layer described by the metadata. REQUIRED
* '-m' or '--metadata': path to the xml metadata file. REQUIRED
* '-o' or '--overwrite': boolean 'true' or 'false' to overwrite existing metadata. Defaults to 'false'.


 ## python files
 `repo_utils.py` has functions for working with `layers.json`, writing and finding metadata.

 `repo_dir.py` contains the logic for creating the directory structure. If you would like to use these utilities,
 but require a different directory structure, you can modify this file. Specifically, the functions `get_directory` and
 `get_hash_dir` are dependencies in other scripts.

 `metadata_type.py` contains logic for determining metadata type. It also returns an ElementTree given an XML string.

 `ogp_to_repo.py` queries an OpenGeoportal Solr instance and writes metadata from the response to an OpenGeoMetadata
 repository. The Solr instance is specified by the constant `SOLR_URL`.  The OpenGeoMetadata repository is specified by
 the constant `REPO_PATH` in `repo_utils.py`

