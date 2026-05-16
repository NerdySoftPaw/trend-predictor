# Installation

## Via HACS (recommended)

1. Open HACS in Home Assistant
2. **Integrations** → top-right menu → **Custom repositories**
3. Enter URL `https://github.com/NerdySoftPaw/trend-predictor`, category **Integration**
4. Search for **Trend Predictor** and click **Download**
5. Restart Home Assistant

Once Trend Predictor is listed in the HACS default catalog, steps 2–3 are not required.

## Manual installation

1. Download the latest release from the [releases page](https://github.com/NerdySoftPaw/trend-predictor/releases) (`trend_predictor.zip`)
2. Unzip the contents into `config/custom_components/trend_predictor/`
3. Restart Home Assistant

## Setting up the integration

After restarting:

1. **Settings** → **Devices & Services** → **Add Integration**
2. Search for **Trend Predictor**
3. Fill in the configuration dialog (see [Configuration](configuration.md))

Create one integration instance per sensor you want to monitor.
