# MapMerger
This tool can be used to assign positive id's to all elements and add a "version" attribute if missing.
If multiple OSM input files are selected the tool will merge them into a single OSM output file. It is also possible to remap negative id's without changing the positive id's.
Elements with "action"="delete" will be ignored. Use the --help command for more information.

### Requires
+ Python 3.8 or higher
+ osmium >=3.2.0
+ lxml,
+ beautifulsoup4,
+ click

### Installation
#### 1. Using pip

```bash
pip install osm-map-merger
```

#### 2. From Source
 Clone source code:
 
 - Using SSH
```bash
git clone git@gitlab.com:tuda-fzd/scenery-representations-and-maps/osm-map-merger.git
```

- Using HTTPS
```bash
git clone https://gitlab.com/tuda-fzd/scenery-representations-and-maps/osm-map-merger.git
```

After cloning the source code run the following command in the root directory of the repository.

```bash
pip install -e .
```

### Execute
To see a list of available commands use:  

```
osm-map-merger --help
```
