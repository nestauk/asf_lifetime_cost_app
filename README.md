# ASF Heating system lifetime cost app
An interactive Streamlit app for comparing the lifetime costs of heat pumps vs. gas boilers.

**Deployed app:** _not yet deployed (link to the EC2-hosted app will go here)_

## 🧮 Underlying model

This app is a Streamlit front end for [`asf_lifetime_cost_model`](https://github.com/nestauk/asf_lifetime_cost_model), a Python package that contains the core lifetime-cost calculation logic (`HeatingSystem` classes, cost/price/subsidy trajectories). This repo only handles input collection, UI, and presentation. See `model_integration/` in the [Repository structure](#🗂️-repository-structure) below for how the two connect.

The model package is installed as a normal dependency via `requirements.txt`; see [Troubleshooting](#troubleshooting) if you need to pick up changes made to it.

## 🛠️ Setup

1. Clone this repository:

Navigate to the directory where you want to clone the repository and run:

```
git clone git@github.com:nestauk/asf_lifetime_cost_app.git
```

2. Create a conda environment and install requirements:

```
cd asf_lifetime_costs_app
conda create --name asf_lifetime_cost_app python==3.13
conda activate asf_lifetime_cost_app
pip install -r requirements.txt
pip install pre-commit
```

3. Run the dashboard locally with:

```
streamlit run app.py
```

## 🗂️ Repository structure

`app.py` is the entrypoint: it sets up global theming (fonts, CSS, Altair theme) and uses Streamlit's `st.navigation()` / `st.Page()` API to route between the four pages in `views/` (there is no `pages/` auto-discovery folder as routing is explicit).

Each page in `views/` follows the same pattern:
- render a sidebar (`page_sections/sidebar.py`) to build an `AppInputs` object
- pass it to `results/compute.py` to get pandas DataFrames. `results/compute.py` calls into `model_integration/`, which wraps the external [`asf_lifetime_cost_model`](https://github.com/nestauk/asf_lifetime_cost_model) package.
- pass DataFrames to render the results with `page_sections/*_outputs.py` (which use `results/charts.py` for Altair charts).
- `components/` and `config/` are shared, dependency-free utility layers (UI building blocks, defaults/styling) used across the other modules.

<p>

```
app.py                              # Entrypoint: theming + st.navigation() routing to views/

views/                              # One file per page, registered in app.py
├── lifetime_cost_comparison.py     # Main comparison page (heat pump vs gas boiler)
├── solve_subsidy.py                # Subsidy solver page
├── solve_price_ratio.py            # Electricity-gas price ratio solver page
└── methodology.py                  # Static methodology/guide page (no model dependency)

page_sections/                      # Renders individual page sections
├── sidebar.py                      # Builds AppInputs from sidebar widgets (shared across pages)
├── comparison_outputs.py           # Output sections for the comparison page
├── subsidy_solver_outputs.py       # Output sections for the subsidy solver page
├── price_ratio_solver_outputs.py   # Output sections for the price-ratio solver page
└── assumptions_summary.py          # Shared "assumptions" summary + download button (shared across pages)

results/                            # Calculation logic: model outputs -> DataFrames -> charts
├── compute.py                      # Builds DataFrames by calling HeatingSystem methods
└── charts.py                       # Pure Altair chart-building functions

model_integration/                  # Wraps the external asf_lifetime_cost_model package
├── schema.py                       # AppInputs and related input dataclasses
├── systems.py                      # Builds HeatingSystem objects (heat pump, gas boiler)
└── trajectories.py                 # Converts AppInputs into cost/price/subsidy trajectories

components/                         # Shared, model-independent UI helpers
├── layout.py                       # Top bar, banners, page titles, section headings
├── sidebar_builder.py              # Sidebar-specific UI helpers
└── callouts.py                     # Styled callout/divider/context-note renderers

config/                             # Shared, model-independent configuration
├── defaults.py                     # Default values/constants, incl. live price cap getters
├── css_style.py                    # Global CSS injection
└── fonts_setup.py                  # Altair theme registration (fonts, Nesta colour palette)
```

<p>

**Key dependencies between modules**:

| Module | Depends on | Why |
| --- | --- | --- |
| `views/*.py` | `page_sections/sidebar.py` | to build that page's `AppInputs` |
| `views/*.py` | its matching `page_sections/*_outputs.py` | to render that page's results |
| `views/*.py` | `results/compute.py` | to turn inputs into DataFrames |
| `page_sections/sidebar.py` | `model_integration/schema.py`, `model_integration/trajectories.py` | to construct and populate the `AppInputs` object from widget values |
| `page_sections/sidebar.py` | `config/defaults.py` | to pre-fill widgets with default values |
| `page_sections/sidebar.py` | `components/callouts.py`, `components/sidebar_builder.py` | to render sidebar UI elements |
| `results/compute.py` | `model_integration/systems.py`, `model_integration/trajectories.py`, `model_integration/schema.py` | to build `HeatingSystem` objects from `AppInputs` and run their calculations into DataFrames |
| `model_integration/systems.py` | `model_integration/trajectories.py` | to build the cost/price/subsidy trajectories each `HeatingSystem` needs |

## 📢 Contributor guidelines

[Technical and working style guidelines](https://github.com/nestauk/ds-cookiecutter/blob/master/GUIDELINES.md)

## Troubleshooting

**There's been changes to `asf-lifetime-cost-model` and I want to update the package that's installed**

Run:
```
pip uninstall asf-lifetime-cost-model -y
pip install -r requirements.txt --no-cache-dir
```

---

Last updated: Elysia Lucas (18/08/2026)
