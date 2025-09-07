
API's we are using
- https://api.spacexdata.com/v4/launches
- https://api.spacexdata.com/v4/launchpads
- https://api.spacexdata.com/v4/rockets


Requirements

- Fetch and store launch data from SpaceX API v4
- Implement local caching to minimize API calls
- Handle API errors gracefully
- Use Python 3.8+
- Implement proper error handling
- Write comprehensive unit tests to verify functionality.
- Use type hints
- Provide clear and concise documentation

Features

- Display a list of all launches with key details.
- Allow users to filter launches based on:
    - Date range
    - Rocket name
    - Launch success/failure
    - Launch site
- Calculate success rates by rocket name
- Track the total number of launches for each launch site.
- Monitor launch frequency on a monthly and yearly basis.

Testing Requirements

Write unit tests covering core functionalities, including:
- Fetching data from the SpaceX API.
- Filtering launches by specified criteria.
- Calculating statistics such as success rates or launch frequencies.