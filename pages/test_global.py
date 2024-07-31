import streamlit as st

html_string = """
<script src="//unpkg.com/globe.gl"></script>
"""

# Display the HTML with components.html
# st.components.v1.html(html_string)
    #   .backgroundImageUrl('//unpkg.com/three-globe/example/img/night-sky.png')

st.markdown("# R•evolution is constant")

html_code = """
<head>
  <style> body { margin: 0em; } </style>
  <script src="//unpkg.com/globe.gl"></script>
</head>

<body>
  <div id="globeViz"></div>
  <script>
    // Gen random data
    const N = 10;
    const gData = [...Array(N).keys()].map(() => ({
      lat: (Math.random() - 0.5) * 180,
      lng: (Math.random() - 0.5) * 360,
      size: Math.random() / 3,
      color: ['red', 'white', 'green'][Math.round(Math.random() * 2)]
    }));

    const xData = [
        { "lat": -32.69824013662637, "lng": -34.863964099322956, "size": 0.0993658891116745 },
        { "lat": -22.69824013662637, "lng": -55.863964099322956, "size": 0.0993658891116745 },
        { "lat": -55.69824013662637, "lng": -22.863964099322956, "size": 0.0993658891116745 }
        ];


    console.log("xData", xData);
    console.log("gData", gData);
    const map = Globe()
    (document.getElementById('globeViz'))
      .globeImageUrl('//unpkg.com/three-globe/example/img/earth-night.jpg')
      .pointsData(xData)
      .backgroundColor('rgb(14, 17, 23)')
      .pointAltitude('size')
      
    // Add auto-rotation
    map.controls().autoRotate = true;
    map.controls().autoRotateSpeed = 10.6;
    
  </script>
</body>
"""

# Display the HTML code in Streamlit app
col1, col2 = st.columns(2)
with col1:
    st.components.v1.html(html_code, height=700, width=700)
    
    
import random

cities = [
    {"name": "New York", "latitude": 40.7128, "longitude": -74.0060, "random_number": random.randint(1, 100)},
    {"name": "London", "latitude": 51.5099, "longitude": -0.1180, "random_number": random.randint(1, 100)},
    {"name": "Tokyo", "latitude": 35.6895, "longitude": 139.6917, "random_number": random.randint(1, 100)},
    {"name": "Paris", "latitude": 48.8566, "longitude": 2.3522, "random_number": random.randint(1, 100)},
    {"name": "Sydney", "latitude": -33.8688, "longitude": 151.2093, "random_number": random.randint(1, 100)},
    {"name": "Dubai", "latitude": 25.2769, "longitude": 55.2963, "random_number": random.randint(1, 100)},
    {"name": "Beijing", "latitude": 39.9042, "longitude": 116.4074, "random_number": random.randint(1, 100)},
    {"name": "Rio de Janeiro", "latitude": -22.9068, "longitude": -43.1729, "random_number": random.randint(1, 100)},
    {"name": "Cape Town", "latitude": -33.918861, "longitude": 18.423300, "random_number": random.randint(1, 100)},
    {"name": "Moscow", "latitude": 55.7558, "longitude": 37.6176, "random_number": random.randint(1, 100)},
]

st.json(cities, expanded=False)


# Generate city data
cities = [
    {"name": "New York", "latitude": 40.7128, "longitude": -74.0060, "random_number": random.randint(1, 100)},
    # Add more cities as needed
]

cities = [
    {"name": "x", "lat": -32.69824013662637, "lng": -34.863964099322956, "size": 0.0993658891116745},
    {"name": "x", "lat": -22.69824013662637, "lng": -55.863964099322956, "size": 0.0993658891116745},
    {"name": "x", "lat": -55.69824013662637, "lng": -22.863964099322956, "size": 110.0993658891116745},
    {"name": "New York", "lat": 40.7128, "lng": -74.0060, "size": random.random()},
    {"name": "London", "lat": 51.5099, "lng": -0.1180, "size": random.random()},
    {"name": "Tokyo", "lat": 35.6895, "lng": 139.6917, "size": random.random()},
    {"name": "Paris", "lat": 48.8566, "lng": 2.3522, "size": random.random()},
    {"name": "Sydney", "lat": -33.8688, "lng": 151.2093, "size": random.random()},
    {"name": "Dubai", "lat": 25.2769, "lng": 55.2963, "size": random.random()},
    {"name": "Beijing", "lat": 39.9042, "lng": 116.4074, "size": random.random()},
    {"name": "Rio de Janeiro", "lat": -22.9068, "lng": -43.1729, "size": random.random()},
    {"name": "Cape Town", "lat": -33.918861, "lng": 18.423300, "size": random.random()},
    {"name": "Moscow", "lat": 55.7558, "lng": 37.6176, "size": random.random()},
]


# Generate JavaScript code with city data
javascript_code = f"""
// Gen city data
const cityData = { cities };
const N = 10;

console.log(cityData);

const map = Globe()
(document.getElementById('globeViz'))
  .globeImageUrl('//unpkg.com/three-globe/example/img/earth-night.jpg')
  .pointsData(cityData)
  .backgroundColor('rgb(14, 17, 23)')
  .pointAltitude('size')

// Add auto-rotation
map.controls().autoRotate = true;
map.controls().autoRotateSpeed = 10.6;
"""

# HTML code with embedded JavaScript
html_code = f"""
<head>
  <style> body {{ margin: 0em; }} </style>
  <script src="//unpkg.com/globe.gl"></script>
</head>

<body>
  <div id="globeViz"></div>
  <script>
    { javascript_code }
  </script>
</body>
"""

# Display the HTML code in Streamlit app
col1, col2 = st.columns(2)
with col1:
    st.components.v1.html(html_code, height=700, width=700)
    

javascript_code = """
    const VELOCITY = 9; // minutes per frame

    const sunPosAt = dt => {
      const day = new Date(+dt).setUTCHours(0, 0, 0, 0);
      const t = solar.century(dt);
      const longitude = (day - dt) / 864e5 * 360 - 180;
      return [longitude - solar.equationOfTime(t) / 4, solar.declination(t)];
    };

    let dt = +new Date();
    const solarTile = { pos: sunPosAt(dt) };
    const timeEl = document.getElementById('time');

    const world = Globe()
      (document.getElementById('globeViz'))
      .globeImageUrl('//unpkg.com/three-globe/example/img/earth-dark.jpg')
      .backgroundColor('rgb(14, 17, 23)')
      .tilesData([solarTile])
      .tileLng(d => d.pos[0])
      .tileLat(d => d.pos[1])
      .tileAltitude(0.01)
      .tileWidth(180)
      .tileHeight(180)
      .tileUseGlobeProjection(false)
      .tileMaterial(() => new THREE.MeshLambertMaterial({ color: '#ffff00', opacity: 0.3, transparent: true }))
      .tilesTransitionDuration(0);

    // animate time of day
    requestAnimationFrame(() =>
      (function animate() {
        dt += VELOCITY * 60 * 1000;
        solarTile.pos = sunPosAt(dt);
        world.tilesData([solarTile]);
        timeEl.textContent = new Date(dt).toLocaleString();
        requestAnimationFrame(animate);
      })()
    );

    world.controls().autoRotate = true;
    world.controls().autoRotateSpeed = 10.6;
"""

html_code = f"""
<head>
<style> body {{ margin: 0em; }} </style>
<script src="//unpkg.com/three"></script>
<script src="//unpkg.com/globe.gl"></script>
<script src="//unpkg.com/solar-calculator"></script>

</head>

<body>
<div id="globeViz"></div>
<div id="time"></div>

<script>
    { javascript_code }
</script>
</body>
"""

# Display the HTML code in Streamlit app
col1, col2 = st.columns(2)
with col1:
    st.components.v1.html(html_code, height=700, width=700)


javascript_code = f"""
const VELOCITY = 9; // minutes per frame

const sunPosAt = dt => {{
    const day = new Date(+dt).setUTCHours(0, 0, 0, 0);
    const t = solar.century(dt);
    const longitude = (day - dt) / 864e5 * 360 - 180;
    return [longitude - solar.equationOfTime(t) / 4, solar.declination(t)];
}};

let dt = +new Date();
const solarTile = {{ pos: sunPosAt(dt) }};
const timeEl = document.getElementById('time');

const cityData = { cities };
const N = 10;

const world = Globe()
    (document.getElementById('globeViz'))
    .globeImageUrl('//unpkg.com/three-globe/example/img/earth-dark.jpg')
    .backgroundColor('rgb(14, 17, 23)')
    .tilesData([solarTile])
    .tileLng(d => d.pos[0])
    .tileLat(d => d.pos[1])
    .tileAltitude(0.01)
    .tileWidth(180)
    .tileHeight(180)
    .tileUseGlobeProjection(false)
    .tileMaterial(() => new THREE.MeshLambertMaterial({{ color: '#ffff00', opacity: 0.3, transparent: true }}))
    .tilesTransitionDuration(0)
    .pointsData(cityData)
    .backgroundColor('rgb(14, 17, 23)')
    .pointAltitude('size');

// animate time of day
requestAnimationFrame(() =>
    (function animate() {{
    dt += VELOCITY * 60 * 1000;
    solarTile.pos = sunPosAt(dt);
    world.tilesData([solarTile]);
    timeEl.textContent = new Date(dt).toLocaleString();
    requestAnimationFrame(animate);
    }})()
);

world.controls().autoRotate = true;
world.controls().autoRotateSpeed = 10.6;
"""

html_code = f"""
<head>
<style> body {{ margin: 0em; }} </style>
<script src="//unpkg.com/three"></script>
<script src="//unpkg.com/globe.gl"></script>
<script src="//unpkg.com/solar-calculator"></script>

</head>

<body>
<div id="globeViz"></div>
<div id="time"></div>

<script type="module">
    { javascript_code }
</script>
</body>
"""

# Display the HTML code in Streamlit app
col1, col2 = st.columns(2)
with col1:
    st.components.v1.html(html_code, height=700, width=700)


resonant_cities = [
    {**city, "maxR": random.random()*20+3, "propagationSpeed": (random.random()+.1)*10, "repeatPeriod": random.random()*3000 + 200}
    for city in cities
]

javascript_code = f"""const N = 10;
    const gData = [...Array(N).keys()].map(() => ({{
      lat: (Math.random() - 0.5) * 180,
      lng: (Math.random() - 0.5) * 360,
      maxR: Math.random() * 20 + 3,
      propagationSpeed: (Math.random() - 0.5) * 20 + 1,
      repeatPeriod: Math.random() * 2000 + 200
    }}));
    const data = { resonant_cities }
    const colorInterpolator = t => `rgba(255,100,50,${{Math.sqrt(1-t)}})`;

    const globe = Globe()
      .globeImageUrl('//unpkg.com/three-globe/example/img/earth-night.jpg')
      .ringsData(data)
      .ringColor(() => colorInterpolator)
      .ringMaxRadius('maxR')
      .ringPropagationSpeed('propagationSpeed')
      .ringRepeatPeriod('repeatPeriod')
      (document.getElementById('globeViz'));
"""

html_code = f"""
<head>
<style> body {{ margin: 0em; }} </style>
<script src="//unpkg.com/globe.gl"></script>

</head>

<body>
<div id="globeViz"></div>
<script>
    { javascript_code }
</script>
</body>
"""

# Display the HTML code in Streamlit app
col1, col2 = st.columns(2)
with col1:
    st.components.v1.html(html_code, height=700, width=700)



javascript_code = f"""const N = 10;
    const gData = [...Array(N).keys()].map(() => ({{
      lat: (Math.random() - 0.5) * 180,
      lng: (Math.random() - 0.5) * 360,
      maxR: Math.random() * 20 + 3,
      propagationSpeed: (Math.random() - 0.5) * 20 + 1,
      repeatPeriod: Math.random() * 2000 + 200
    }}));
    const data = { resonant_cities }
    const colorInterpolator = t => `rgba(255,100,50,${{Math.sqrt(1-t)}})`;

    const globe = Globe()
      .globeImageUrl('//unpkg.com/three-globe/example/img/earth-night.jpg')
      .ringsData(data)
      .ringColor(() => colorInterpolator)
      .ringMaxRadius('maxR')
      .ringPropagationSpeed('propagationSpeed')
      .ringRepeatPeriod('repeatPeriod')
      .pointsData(data)
      .backgroundColor('rgb(14, 17, 23)')
      .pointAltitude('size')
      .pointRadius(.3)
      .pointColor(() => 'red')
      
      (document.getElementById('globeViz'));
"""

html_code = f"""
<head>
<style> body {{ margin: 0em; }} </style>
<script src="//unpkg.com/globe.gl"></script>

</head>

<body>
<div id="globeViz"></div>
<script>
    { javascript_code }
</script>
</body>
"""

# Display the HTML code in Streamlit app
col1, col2 = st.columns(2)
with col1:
    st.components.v1.html(html_code, height=700, width=700)
