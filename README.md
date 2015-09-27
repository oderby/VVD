# VVD

Leveraging version control software for graph-based languages & tools, such as Grasshopper and Dynamo, has been an elusive topic for far too long. Although there has always been significant interest, it has been a daunting problem to solve. Due to opaque binary file formats and messy XML documents, traditional VCS is of only marginal utility, and not worth the learning curve. 

We believe one of the biggest roadblocks to the adoption of VCS overall, and by the AEC industry in particular, is the lack of a useful, simple UI for visualizing and exploring differences between two files. The ability to see the changes made to a graph, layed out with the original graph, is essential to properly understanding how the definition has changed and evolved as collaborators worked on it. We hope by exploring these issues, we can spur collaboration in the industry and beyond.

VVD ("Vivid") is a set of tools for working with version control software. It consists of 3 different tools, for computing diffs, visualizing them, and applying them to files. These tools are detailed further below, in the Usage section. They are best suited to a collaboration workflow where 2 or more team members are working on the same graph definition asynchronously, and need to merge their respective changes together as they synchronize and finish their respective tasks. 

These tools are built using a combination of C# and IronPython, as well as the open Grasshopper and Dynamo C# SDKs, and the great graphviz tools. This tool was intially built at the TT AEC Technology Hackathon 2015, held in New York City.

## Installation

To fully utilize VVD, you will need to have the following software installed:
* Python 2.7 or greater (does not work with Python 3)
* graphviz and pygraphviz
* .Net 4.0 or greater (to compute and apply diffs)

## Usage

Each tool serves a particular purpose, and we walk through each below, starting with purpose and use case, tool documentation, and several examples.

### Compute Differences
Say you want to see what changed between two different versions of a Grasshopper script, or you need to share your changes with a colleague who has an older version of your definition. The first thing you need to do is compute what's changed - the "diff" (differences). There are two tools for this purpose - one for working with Grasshopper files (diffgraphgh.cmd) and one for working with Dynamo files (diffgraphdy.cmd).

`diffgraphgh.cmd [old_gh_file] [new_gh_file] [gh_diff_file]`

This tool accepts two Grasshopper files (.gh or .ghx) and writes the difference file (a .dsx file, see below for more details) out to the specified `diff_file`. This `diff_file` is what you'll use to apply the changes to another file. The `diffgraphdy.cmd` tool operates in an analogous manner, except for Dynamo.

### Visualize Differences
Say your colleage sent you the diff_file of his work since the last time you synced, and you want to see what he's accomplished. There are several options here. We've built diff viewers for GH and Dynamo, which take a base definition file and a diff file, and display the changes from the diff on top of the base file, in the native tools. (Docs coming soon)

We've also built a standalone diff viewer on top of the graphviz library, which takes Dynamo or Grasshopper files and a diff and renders them in a simple graph viewer.

`vizdiffdy.cmd [dy_file] [dy_diff_file]`

This tool will take a dynamo file and diff file and launch a photo viewer with the resulting png of the differences.

### Apply Differences (merging)
You've gotten the differences from your colleague, and inspected the changes. Now you want to apply those changes to your file. We have made 2 tools, one for each Dynamo and Grasshopper, to take a diff and apply them to a definition.

`applydiffdy.cmd [base_dy_file] [dy_diff_file] [dst_dy_file]`

This tool takes the base Dynamo file and diff file to aply, and the place you want to write the new dynamo file to. It will take the changes in the diff file and *try* to apply them on top of the base file. The `applydiffgh.cmd` tool works in a similar manner for Grasshopper files.

There's no need for the base file here to be the same one the diff was calculated on. However, there is also no guarantee a given diff file will apply cleanly to a given definition. In particular, if the two collaborators made a lot of changes in the same region of the graph, it's likely applying the diff will fail. This tool currently will only succeed if all changes applied cleanly - otherwise it won't make any changes and will alert the user to the failure.

## Basic architecture

(Coming soon)

## Future work
* Code refactor (this was built at a hackathon, afterall!)
* Improve cmdline tools to be smarter, easier to use. 
  - Convert batch files to python
  - Move towards a single, unified tool
* Provide an installer to facilitate installing tools and dependencies
* Expand to other graph-based languages, with open file formats
* Incorporate diff visualization with patch application logic
* Interactive merge - review changes before applying a patchset.
* Diff visualization in the web (git-notes?)
* 3-way diff/merge - smarter merging behavior
  - Report which areas had issues/problems
* Expand on the basic standalone diff viewer
