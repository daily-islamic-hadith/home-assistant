# Daily Islamic Hadith Home Assistant Integration

This custom Home Assistant integration provides a daily Islamic Hadith and its explanation (in different supported
languages) as a sensor.

The sensor fetches a Hadith along with an explanation and store them in the sensor's attributes.

## Installation Options

### With HACS

If you have HACS installed on your Home Assistant, you can use it to install the *Daily Islamic Hadith* integration.

1. Go to your HACS dashboard, click on the settings icon (three dots in the top right corner), and select *Custom
Repositories*.  
2. In the *Repository* text field, enter the URL of this repository: https://github.com/daily-islamic-hadith/home-assistant  
3. Then, select *Integration* in the *Type* field and click the *Add* button to complete the setup.

### Manually

For the manual installation, you must copy the custom_components/daily_islamic_hadith folder from this repository to the
custom_components directory of your Home Assistant installation (create it if it does not exist).

### Integration Setup

1. Restart Home Assistant (e.g. From UI go to Settings > System > Hardware > Power button at top right)

2. Install the Integration via Home Assistant UI
    - Go to **Settings > Devices & Services** in the Home Assistant UI.
    - In the bottom right, click the **Add Integration** button to add an integration.
    - Search for **Daily Islamic Hadith**.
    - Click on it to install.

3. Follow the Configuration Flow  
   Once the integration is installed, follow the on-screen prompts to complete the setup. The integration will
   automatically create the necessary sensor.

## How It Works

The integration offers the following:

- A sensor of id `daily_hadith` that contains two important attributes:
   - **`hadith`**: The text of the daily Hadith.
   - **`explanation`**: The explanation of the Hadith.
- A service `fetch_new_hadith` that would update the sensor with a new random hadith whenever called.

`daily_hadith` sensor is updated with a new hadith in two ways:

- Automatically every day at 01:00AM.
- A call to service `fetch_new_hadith`.

You can view these attributes in the entity’s details in the Home Assistant UI or use them in automations and scripts.


## Example

### Viewing the Sensor in Home Assistant

Once the integration is installed and configured, you can check the daily Hadith on your Home Assistant dashboard using
different options:

#### Entities Card

```yaml
type: entities
entities:
  - type: attribute
    entity: sensor.daily_hadith
    attribute: hadith
    name: hadith
  - type: attribute
    entity: sensor.daily_hadith
    attribute: explanation
    name: explanation
```

#### Markdown Card

```yaml
{ % set is_arabic = states.sensor.daily_hadith.attributes[ 'language' ] == 'AR' % }
  { % if is_arabic % }
  { % set align = 'right' % }
  { % else % }
  { % set align = 'left' % }
  { %endif% }
  <table width=100%>
  <tr><td align={{ align }}>{{states.sensor.daily_hadith.attributes['hadith']}}</td></tr>
  </table>
  <table width=100%>
  <tr><td align={{ align }}>{{states.sensor.daily_hadith.attributes['explanation']}}</td></tr>
  </table>
```

#### Markdown Card With card-mod
A sample styling using card-mode (If you have card-mode already installed) 
```yaml
type: markdown
content: |
  {{states.sensor.daily_hadith.attributes['hadith']}}

  {{states.sensor.daily_hadith.attributes['explanation']}}
title: Hadith Of The Day
card_mod:
  style: |
    ha-card {
    text-align: center
    }
    ha-markdown {
      direction: {{ 'rtl' if state_attr('sensor.daily_hadith', 'language') == 'AR' else 'ltr'}};
      text-align: {{ 'right' if  state_attr('sensor.daily_hadith', 'language') == 'AR' else 'left' }};
      font-size: 1.5rem;
      
    }
```

### Using the Hadith in Automations

TBD

## Contributions

Feel free to submit issues or pull requests if you want to improve this integration. Please ensure you follow the Home
Assistant's [component development guidelines](https://developers.home-assistant.io/docs/creating_component_index).

## License

This integration is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Support

If you encounter any issues or need help with installation, feel free to open an issue on
the [GitHub repository](https://github.com/daily-islamic-hadith/home-assistant).