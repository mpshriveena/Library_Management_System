<template>
  <div class="body">
    <div class="container">
    <h1>Contact Us</h1>
    <p>Need help? Feel free to contact us.</p>
    <div class="details">
  <p><strong>Email   :</strong> 21f3001238@ds.study.iitm.ac.in</p>
  <p><strong>Address:</strong></p>
  <p>M.P.S.S. Knowledge Junction,</p>
  <p>1/2, XYZ Street,</p>
  <p>KanyaKumari - 000000.</p>
  <p><strong>Contact :</strong> +91 9999999999</p>
</div>
</div>
</div>
</template>

<script>
export default {

}
</script>

<style scoped>
.body {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;

}

.container {
    width: 40%;
    height: auto;
    background: transparent;
    border: 0;
    backdrop-filter: blur(20px);
    color: white;
    border-radius: 10px;
    padding: 50px;
    box-shadow: 0 0 50px 25px rgb(0, 0, 0);
    text-align:center;
}
.details{
  text-align:left;
  padding-left: 31%; 
}
.details p {
    margin: 5px 0; 
  }
  h1{
    text-shadow: 3px 3px 8px rgb(238, 255, 0);
  }
</style>