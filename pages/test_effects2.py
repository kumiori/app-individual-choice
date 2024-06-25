import streamlit as st

# Set page configuration
st.set_page_config(page_title="Cool CSS/JS Effect", page_icon="✨", layout="wide")

# Title of the app
st.title("Cool CSS/JS Effect in Streamlit")

# Embed custom HTML, CSS, and JavaScript using st.markdown
st.markdown("""
    <style>
        body {
            background: #2e2e2e;
            color: #f1f1f1;
            font-family: 'Arial', sans-serif;
            text-align: center;
        }

        .card {
            position: relative;
            width: 300px;
            margin: 50px auto;
            background: #1a1a1a;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        }

        .card .noise {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }

        .card .content {
            position: relative;
            padding: 20px;
            z-index: 1;
        }

        .gradient-bg {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
        }

        .gradient-bg .noiseBg {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }

        .svgBlur {
            position: absolute;
            width: 0;
            height: 0;
        }

        .gradients-container {
            position: relative;
            width: 100%;
            height: 100%;
        }

        .gradients-container div {
            position: absolute;
            width: 200px;
            height: 200px;
            border-radius: 50%;
            background: linear-gradient(45deg, rgba(255, 0, 64, 0.5), rgba(255, 204, 0, 0.5), rgba(0, 255, 64, 0.5), rgba(0, 204, 255, 0.5), rgba(255, 0, 255, 0.5), rgba(255, 0, 64, 0.5));
            filter: url(#goo);
            animation: moveInCircle 5s infinite alternate;
        }

        .gradients-container .interactive {
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            animation: none;
        }

        .g1 {
            position: absolute;
            background: radial-gradient(circle at center, rgba(var(--color1), 0.8) 0, rgba(var(--color1), 0) 50%) no-repeat;
            mix-blend-mode: var(--blending);

            width: var(--circle-size);
            height: var(--circle-size);
            top: calc(50% - var(--circle-size) / 2);
            left: calc(50% - var(--circle-size) / 2);

            transform-origin: center center;
            animation: moveVertical 30s ease infinite;

            opacity: 1;
        }

        .g2 {
            position: absolute;
            background: radial-gradient(circle at center, rgba(var(--color2), 0.8) 0, rgba(var(--color2), 0) 50%) no-repeat;
            mix-blend-mode: var(--blending);

            width: var(--circle-size);
            height: var(--circle-size);
            top: calc(50% - var(--circle-size) / 2);
            left: calc(50% - var(--circle-size) / 2);

            transform-origin: calc(50% - 400px);
            animation: moveInCircle 20s reverse infinite;

            opacity: 1;
        }

        .g3 {
            position: absolute;
            background: radial-gradient(circle at center, rgba(var(--color3), 0.8) 0, rgba(var(--color3), 0) 50%) no-repeat;
            mix-blend-mode: var(--blending);

            width: var(--circle-size);
            height: var(--circle-size);
            top: calc(50% - var(--circle-size) / 2 + 200px);
            left: calc(50% - var(--circle-size) / 2 - 500px);

            transform-origin: calc(50% + 400px);
            animation: moveInCircle 40s linear infinite;

            opacity: 1;
        }

        .g4 {
            position: absolute;
            background: radial-gradient(circle at center, rgba(var(--color4), 0.8) 0, rgba(var(--color4), 0) 50%) no-repeat;
            mix-blend-mode: var(--blending);

            width: var(--circle-size);
            height: var(--circle-size);
            top: calc(50% - var(--circle-size) / 2);
            left: calc(50% - var(--circle-size) / 2);

            transform-origin: calc(50% - 200px);
            animation: moveHorizontal 40s ease infinite;

            opacity: 0.7;
        }

        .g5 {
            position: absolute;
            background: radial-gradient(circle at center, rgba(var(--color5), 0.8) 0, rgba(var(--color5), 0) 50%) no-repeat;
            mix-blend-mode: var(--blending);

            width: calc(var(--circle-size) * 2);
            height: calc(var(--circle-size) * 2);
            top: calc(50% - var(--circle-size));
            left: calc(50% - var(--circle-size));

            transform-origin: calc(50% - 800px) calc(50% + 200px);
            animation: moveInCircle 20s ease infinite;

            opacity: 1;
        }

        @keyframes moveInCircle {
        0% {
            transform: rotate(0deg);
        }
        50% {
            transform: rotate(180deg);
        }
        100% {
            transform: rotate(360deg);
        }
        }

        @keyframes moveVertical {
        0% {
            transform: translateY(-50%);
        }
        50% {
            transform: translateY(50%);
        }
        100% {
            transform: translateY(-50%);
        }
        }

        @keyframes moveHorizontal {
        0% {
            transform: translateX(-50%) translateY(-10%);
        }
        50% {
            transform: translateX(50%) translateY(10%);
        }
        100% {
            transform: translateX(-50%) translateY(-10%);
        }
        }

        @keyframes move {
            0% { transform: translate(0, 0); }
            100% { transform: translate(180px, 80px); }
        }

    </style>
    <div class="card">
      <svg 
           viewBox="0 0 100% 100%"
           xmlns='http://www.w3.org/2000/svg'
           class="noise"
           >
        <filter id='noiseFilter'>
          <feTurbulence 
                        type='fractalNoise' 
                        baseFrequency='0.85' 
                        numOctaves='6' 
                        stitchTiles='stitch' />
        </filter>
        <rect
              width='100%'
              height='100%'
              preserveAspectRatio="xMidYMid meet"
              filter='url(#noiseFilter)' />
      </svg>
      <div class="content">
        <h1>Interactive Gradient</h1>
        <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsum tempore unde ex pariatur distinctio laboriosam, dolorem quibusdam aperiam expedita consequuntur dolorum porro vitae earum quos voluptates et maxime. Tempora, mollitia.</p>
      </div>
    </div>
    <div class="gradient-bg">
      <svg 
           viewBox="0 0 100vw 100vw"
           xmlns='http://www.w3.org/2000/svg'
           class="noiseBg"
           >
        <filter id='noiseFilterBg'>
          <feTurbulence 
                        type='fractalNoise'
                        baseFrequency='0.6'
                        stitchTiles='stitch' />
        </filter>
        <rect
              width='100%'
              height='100%'
              preserveAspectRatio="xMidYMid meet"
              filter='url(#noiseFilterBg)' />
      </svg>
      <svg xmlns="http://www.w3.org/2000/svg" class="svgBlur">
        <defs>
          <filter id="goo">
            <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="blur" />
            <feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -8" result="goo" />
            <feBlend in="SourceGraphic" in2="goo" />
          </filter>
        </defs>
      </svg>
      <div class="gradients-container">
        <div class="g1"></div>
        <div class="g2"></div>
        <div class="g3"></div>
        <div class="g4"></div>
        <div class="g5"></div>
        <div class="interactive"></div>
      </div>
    </div>
""", unsafe_allow_html=True)

# Run the Streamlit app
if __name__ == "__main__":
    st.write("Enjoy the cool CSS/JS effect!")
