# mcp-server-agribalyse

🌿 **A Model Context Protocol (MCP) server for querying the ADEME Agribalyse 3.1 dataset.**

This MCP server provides tools and resources to interact with the Agribalyse public API, enabling Large Language Models to retrieve and analyze environmental impact data on food products.

> ⚠️ Note: This server is based on the [FastMCP](https://github.com/modelcontextprotocol) framework and is actively maintained. API coverage may evolve.

---

## 🚀 Overview

Agribalyse is a dataset published by ADEME, offering environmental indicators (climate impact, water use, ecotoxicity, etc.) for thousands of food products.

This MCP server allows LLMs to:
- Search food product data.
- Aggregate environmental metrics.
- List possible filter values.
- Understand dataset structure.

---

## 🧰 Tools

| Tool Name              | Description                                                 |
|------------------------|-------------------------------------------------------------|
| `read_lines`           | Query rows from the Agribalyse dataset                      |
| `get_values`           | Get distinct values for a given text field                  |
| `get_metric_agg`       | Compute a single metric (avg, min, etc.) on a numeric field |
| `get_simple_metrics_agg` | Compute metrics on one or more fields at once            |
| `get_words_agg`        | Retrieve most frequent tokens in a text field               |
| `read_schema`          | Get the complete column schema of the dataset               |
| `read_safe_schema`     | Get a reduced version of the column schema                  |
| `read_api_docs`        | Fetch the full OpenAPI specification from the ADEME API     |

---

## 📚 Resources

| URI                                | Description                                           |
|------------------------------------|-------------------------------------------------------|
| `agribalyse://fields`              | List of allowed text fields for querying             |
| `agribalyse://files`               | Available data files published by ADEME              |
| `agribalyse://sample-lines`        | A sample of dataset rows                             |
| `agribalyse://columns/sortables`   | Fields that can be used for sorting                  |
| `agribalyse://metrics/fields`      | Numeric fields usable for aggregation                |
| `agribalyse://metrics/types`       | Supported metric types (avg, sum, percentiles, etc.) |
| `agribalyse://fields/descriptions` | Human-readable descriptions of each dataset column   |

---

## 💬 Prompts

This server also includes predefined prompts for easier interaction:

- `search_product`: Ask for environmental info about a named product
- `ask_stat`: Ask for a specific metric on an indicator
- `compare_products`: Compare two products by one indicator
- `list_field_values`: List possible values of a given field
- `sample_prompt`: Ask to preview sample data
- `explain_indicator`: Ask for an explanation of an indicator
- `custom_query_prompt`: Prompt chain for guided query refinement

---

## 🧪 Debugging
You can inspect server behavior using:
```
npx @modelcontextprotocol/inspector uvx run src/agribalyse/server.py
```

Or follow logs using:
```
mcp dev server.py
```

## 👩‍💻 Maintainer
**Author**: Tracy André

**Organization**: Positive Solutions

**Contact**: tracy.andre@food-pilot.eu

