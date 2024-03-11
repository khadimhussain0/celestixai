<template>
  <div>
    <!-- Header Section -->
    <header>
      <nav>
        <div class="logo">celestixai</div>
        <ul>
          <li><a href="#features">Features</a></li>
          <li><a href="#how-it-works">How it Works</a></li>
          <li><a href="#benefits">Benefits</a></li>
          <!-- <li><a href="#pricing">Pricing</a></li> -->
          <li><a href="#contact">Contact</a></li>
        </ul>
      </nav>
    </header>

    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <h1>Unlock the Power of AI for Your Business</h1>
        <p>Revolutionize your data with celestixai - Your Gateway to Intelligent Decision Making.</p>
        <router-link to="/auth" class="cta-button">Get Started</router-link>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="features">
      <div class="feature-card">
        <img src="../assets/llama-model.png" alt="LLama Model">
        <h2>LLama Model</h2>
        <p>Fine-tune your data effortlessly with our sophisticated LLama model, achieving unparalleled accuracy in AI predictions.</p>
      </div>

      <!-- <div class="feature-card">
        <img src="../assets/falcon-model.png" alt="Falcon Model">
        <h2>Falcon Model</h2>
        <p>Unleash the potential of the Falcon model for cutting-edge AI capabilities, propelling your business into the future of technology.</p>
      </div> -->

      <div class="feature-card">
        <img src="../assets/mixtral-mistral-model.png" alt="Mixtral and Mistral Models">
        <h2>Mixtral & Mistral Models</h2>
        <p>Select from a diverse range of models like Mixtral and Mistral, tailored to meet the unique demands of your business.</p>
      </div>
    </section>

    <!-- How It Works Section -->
    <section id="how-it-works" class="how-it-works">
      <h2>How It Works</h2>
      <div class="step">
        <img src="../assets/upload-data.png" alt="Upload Data">
        <h3>Upload Your Data</h3>
        <p>Effortlessly upload your datasets using our user-friendly interface, ensuring a seamless integration process.</p>
      </div>

      <div class="step">
        <img src="../assets/fine-tune.png" alt="Fine-Tune Models">
        <h3>Fine-Tune Models</h3>
        <p>Customize AI models for your specific use case with our intuitive fine-tuning process, empowering your data for optimal results.</p>
      </div>

      <div class="step">
        <img src="../assets/deploy.png" alt="Deploy Models">
        <h3>Deploy Models</h3>
        <p>Swiftly deploy your fine-tuned models with a single click, putting the power of AI directly into your hands.</p>
      </div>

      <div class="step">
        <img src="../assets/api-integration.png" alt="API Integration">
        <h3>API Integration</h3>
        <p>Seamlessly integrate your deployed models into your products using our intuitive APIs, enhancing your applications with AI capabilities.</p>
      </div>
    </section>

    <!-- Benefits Section -->
    <section id="benefits" class="benefits">
      <h2>Benefits of celestixai</h2>
      <div class="benefit-card">
        <img src="../assets/upload-data.png" alt="Easy to Use">
        <h3>Easy to Use</h3>
        <p>Our platform provides a user-friendly experience, making AI accessible to all levels of expertise within your organization.</p>
      </div>

      <div class="benefit-card">
        <img src="../assets/upload-data.png" alt="Customizable">
        <h3>Customizable</h3>
        <p>Tailor AI models to your specific business needs, ensuring a personalized and effective solution for your industry.</p>
      </div>

      <div class="benefit-card">
        <img src="../assets/deploy.png" alt="Fast Deployment">
        <h3>Fast Deployment</h3>
        <p>Accelerate your AI implementation with our rapid deployment process, getting you up and running in no time.</p>
      </div>

      <div class="benefit-card">
        <img src="../assets/upload-data.png" alt="Powerful Results">
        <h3>Powerful Results</h3>
        <p>Experience transformative outcomes with our powerful AI models, driving innovation and success for your business.</p>
      </div>
    </section>

    <!-- Get Started Section -->
    <section id="get-started" class="get-started">
      <h2>Get Started Today</h2>
      <p>Join the AI revolution and elevate your business to new heights. Sign up now to unleash the full potential of celestixai.</p>
      <router-link to="/auth" class="cta-button">Sign Up Now</router-link>
    </section>

    <!-- Footer Section -->
    <footer>
      <section id="contact" class="contact">
        <h2>Contact Us</h2>
        <p>Have questions or need assistance? Reach out to us!</p>
        <a href="mailto:info@llmai.com">info@llmai.com</a>
      </section>

      <div class="social-icons">
        <a href="#" target="_blank"><img src="../assets/twitter-icon.png" alt="Twitter"></a>
        <a href="#" target="_blank"><img src="../assets/linkedin-icon.png" alt="LinkedIn"></a>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  methods: {
    redirectToCreateAccount() {
      this.$router.push('/auth');
    },
  },
};
</script>

<style scoped>
/* Global Styles */
body {
  font-family: 'Arial', sans-serif;
  margin: 0;
  padding: 0;
}

/* Header Styles */
header {
  background-color: #292b2c;
  color: #ffffff;
  padding: 1rem;
  text-align: center;
}

nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
}

ul {
  list-style: none;
  display: flex;
}

li {
  margin: 0 1rem;
}

a {
  text-decoration: none;
  color: #ffffff;
}

/* Hero Styles */
.hero {
  background-color: #343a40;
  color: #ffffff;
  text-align: center;
  padding: 3rem 0;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

h1 {
  font-size: 2.5rem;
}

p {
  font-size: 1.2rem;
  margin-top: 1rem;
}

.cta-button {
  display: inline-block;
  background-color: #007bff;
  color: #ffffff;
  padding: 0.5rem 1rem;
  text-decoration: none;
  font-size: 1rem;
  margin-top: 1rem;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.cta-button:hover {
  background-color: #0056b3;
}

/* Features Section Styles */
.features {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  margin: 3rem 0;
}

.feature-card {
  text-align: center;
  margin: 1.5rem;
  padding: 1.5rem;
  border: 1px solid #eaeaea;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: scale(1.05);
}

.feature-card img {
  max-width: 80%;
  height: auto;
  margin-bottom: 1rem;
}

h2 {
  font-size: 1.5rem;
}

/* How It Works Section Styles */
.how-it-works {
  text-align: center;
  margin: 3rem 0;
}

.step {
  margin: 2rem;
  padding: 1.5rem;
  border: 1px solid #eaeaea;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.step:hover {
  transform: scale(1.05);
}

.step img {
  max-width: 80%;
  height: auto;
  margin-bottom: 1rem;
}

/* Benefits Section Styles */
.benefits {
  text-align: center;
  margin: 3rem 0;
}

.benefit-card {
  text-align: center;
  margin: 1.5rem;
  padding: 1.5rem;
  border: 1px solid #eaeaea;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.benefit-card:hover {
  transform: scale(1.05);
}

.benefit-card img {
  max-width: 80%;
  height: auto;
  margin-bottom: 1rem;
}

h3 {
  font-size: 1.2rem;
}

/* Get Started Section Styles */
.get-started {
  text-align: center;
  margin: 3rem 0;
}

/* Footer Styles */
footer {
  background-color: #f8f9fa;
  padding: 3rem 0;
}

.contact {
  text-align: center;
}

.social-icons {
  margin-top: 1.5rem;
}

.social-icons a {
  margin: 0 1rem;
}

.social-icons img {
  width: 30px;
  height: 30px;
  border-radius: 50%;
}
</style>
