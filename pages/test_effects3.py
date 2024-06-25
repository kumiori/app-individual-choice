import streamlit as st

# Set page configuration
st.set_page_config(page_title="Cool CSS/JS Effect",
  page_icon="✨",
  # layout="wide"
  )

# Title of the app
# st.title("Cool CSS/JS Effect in Streamlit")

# Load CSS
with open("pages/effects.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)



def blurscape():
  """docstring for blurscape"""

  # Embed custom HTML, CSS, and JavaScript using st.markdown
  st.markdown("""
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
          <center><h1>Tr∀*st Game</h1></center>
          <center><h2>The Gradient</h2></center>
          <center><h3>to the Steepest Descent</h3></center>
          <br />
          <p>Can we play experimental game designed to explore trust dynamics between humans and financial institutions?</p>
          <p>We explore questions of trust, trustworthiness, and cooperation in social interactions.</p>
          <h3><a href="">Play to Game</a></h3>
          <h3><a href="">Pay to Play</a></h3>
          <h3><a href="">Wait to See</a></h3>
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
                filter='url(#noiseFilterBg)' 
          />
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
        </div>
      </div>

      <script type="text/javascript">
        console.log('DOM loaded');
        document.addEventListener('DOMContentLoaded', () => {
            const interBubble = document.querySelector('.interactive');
            let curX = 0;
            let curY = 0;
            let tgX = 0;
            let tgY = 0;

            const move = () => {
                curX += (tgX - curX) / 20;
                curY += (tgY - curY) / 20;
                interBubble.style.transform = `translate(${Math.round(curX)}px, ${Math.round(curY)}px)`;
                requestAnimationFrame(move);
            };

          window.addEventListener('mousemove', (event) => {
                tgX = event.clientX;
                tgY = event.clientY;
                console.log(tgX, tgY);
            });

            move();
        });
      </script>
  """, unsafe_allow_html=True)

  

# Run the Streamlit app
if __name__ == "__main__":
  blurscape()
  
  from streamlit_extras.stylable_container import stylable_container
  st.markdown("---", unsafe_allow_html=True)
  
  st.markdown("# <center>Introduction<center>", unsafe_allow_html=True)
  with stylable_container(key="card",css_styles="""
                          """):
    with stylable_container(key="content",css_styles="""
                            """):
      st.markdown("# <center>What to trust?<center>", unsafe_allow_html=True)
      """
      Trusting behavior often depends on many factors and it is difficult to estimate. The perceived trustworthiness of the partner plays a role, likewise perceived risks and rewards as well as social norms regarding cooperation and reciprocity. Transparency, clarity, how many other factors? This game allows us, researchers and players, to study how these factors influence decision-making and how trust and cooperation can emerge or break down in different situations.
And, more importantly, to foresee what are the outcomes.    
    """
  
  st.markdown("# <center>Experimental<center>", unsafe_allow_html=True)
  with stylable_container(key="card",css_styles="""
                          """):
    with stylable_container(key="content",css_styles="""
                            """):
      st.markdown("# <center>An empirical approach.<center>", unsafe_allow_html=True)
      """
      `In an infinite-dimensional energy space there are two players: player I and player B. Player I may be many, player B may be Big...`
      
      We set up an simple data hub to visualise, an experimental framework to uncover and analyse, to study: how complex interactions and adaptive behaviors emerge in social systems. The motivation, the design, and the potential of this study will be presented in a scientific paper and is part of a larger research on constrained processes of evolution.
      
      Join the wait list to be invited to play, or pay to play: now. 
      """