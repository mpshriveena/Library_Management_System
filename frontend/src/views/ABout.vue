<template>
  <div class="body">
    <div class="about-container">
    <h1>About M.P.S.S Knowledge Junction</h1>
    <p>How to use it?</p>
    <br>
    <div class="section">
    <div class="section1">
      <h4>Step 1</h4>
      <br>
      <p>Login using registered email and password.
        If you didn't register yet, click on register link. 
        Provide the necessary information and register. 
        Now login to the website.</p>
        <br>
        <h4>Step 2</h4>
        <br>
        <p>You can now able to see different sections. 
          Click on your favorite section to view the books under the section. 
          You can also see recently added books on the top of sections.
        </p>
      <br>
      <h4>Step 3</h4>
      <br>
      <p> You can see various books inside the selected section. 
        Click on any book to view its details or to request them to read.
      </p>
      <br>
      <h4>Step 4</h4>
      <br>
      <p>If you want to read a book, you must request for it. Click on the request button. Enter number of days you want to request them. 
        Click on "Request". The librarian will go through your request and give you the 
        access to read them based on number of days. After request 
        is granted you can read them. You can also view the status of your book in "My Requests" tab. 

      </p>
    </div>
    <div class="section2">
      <h4>Step5</h4>
      <br>
      <p>After reading your books, kindly return them within the requested number of days. 
        Else the access will be automatically revoked after the requested number of days. 
      </p>
      <br>
      <h4>Step 6</h4>
      <br>
      <p>You can request for only "5" books. If you want to request more number of books, kindly subscribe to our website. 
        To subscribe, click on the "Subscribe" tab on top and pay the subscription amount. 
        After subscription you can request for unlimited number of books.
      </p>
      <br>
      <h4>Step 7</h4>
      <br>
      <p>You can also see your Statistics in the "Stats" tab, contact us using the information given in the 
        "Contact" tab. You can also search for various sections, books and authors. You can also buy books 
        from our website so that you don't need to return them.
      </p>
      <br>
      <h4>Step 8</h4>
      <br>
      <p>Kindly log out after using the website.</p>
    </div>
  </div>
</div>
</div>
</template>

<script>
export default {

}
</script>

<style scoped>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Poppins', 'sans-serif';
}

.body {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;

}

.about-container {
    width: 90%;
    height: 80vh;
    background: transparent;
    border: 0;
    backdrop-filter: blur(20px);
    color: white;
    border-radius: 10px;
    padding: 50px;
    box-shadow: 0 0 50px 25px rgb(0, 0, 0);
    text-align:center;
}
.section{
  display:flex;
  column-gap: 5%;
}
.section1{
  text-align: left;
  padding:20px;
  width:50%;
  height: 60vh;
  border-radius: 10px;
  background: transparent;
  border: 2px solid rgb(255, 255, 255);
}
.section2{
  text-align: left;
  padding:20px;
  width:50%;
  height: 60vh;
  background: transparent;
  border-radius: 10px;
  border: 2px solid rgb(255, 255, 255);
}

h1{
    font-size: 36px;
    text-align: center;
    text-shadow: 3px 3px 8px rgb(189, 3, 3);
}

h3{
  text-shadow: 3px 3px 8px rgb(255, 0, 0);
}
p{
  text-shadow: 3px 3px 8px rgb(0, 0, 0)
}
h4{
  text-shadow: 3px 3px 8px rgb(180, 255, 4)
}
</style>