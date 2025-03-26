# MCP Simple Chatbot

This example demonstrates how to integrate the Model Context Protocol (MCP) into a simple CLI chatbot. The implementation showcases MCP's flexibility by supporting multiple tools through MCP servers and is compatible with any LLM provider that follows OpenAI API standards.

## Requirements

- Python 3.10
- `python-dotenv`
- `requests`
- `mcp`
- `uvicorn`

## Installation

**Install the dependencies(local):**

- Method 1: Install directly from the project directory

```bash
git clone [project repository URL]
cd [project directory]
pip install .
```

**Configure servers(pypi):**

The `servers_config.json` follows the same structure as Claude Desktop, allowing for easy integration of multiple servers.
Here's an example:

```json
{
  "mcpServers": {
    "pubchem": {
      "command": "uvx",
      "args": ["pubchem_mcp_server"]
    }
  }
}
```

## the result of this MCP

```json
{
  "Drug Name": "Aspirin",
  "CAS Number": "50-78-2",
  "Molecular Weight": 180.16,
  "Molecular Formula": "C9H8O4",
  "SMILES": "CC(=O)OC1=CC=CC=C1C(=O)O",
  "Synonyms": [
    "2-(Acetyloxy)benzoic Acid",
    "Acetylsalicylic Acid",
    "Acetysal",
    "Acylpyrin",
    "Aloxiprimum",
    "Aspirin",
    "Colfarit",
    "Dispril",
    "Easprin"
  ],
  "InchI Key": "BSYNRYMUTXBXSQ-UHFFFAOYSA-N",
  "IUPAC Name": "2-acetyloxybenzoic acid",
  "ATC Code": "N02BA01",
  "Details Link": "https://pubchem.ncbi.nlm.nih.gov/compound/2244"
}
```
